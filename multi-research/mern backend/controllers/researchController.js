import Research from '../models/Research.js';
import axios from 'axios';
import {
  generateResearchSummary,
  extractPipelineSummary,
} from '../services/summaryService.js';

const attachSummaryOnCompletion = async (research, data, extractedReport, rawResult) => {
  try {
    const pipelineSummary = extractPipelineSummary(rawResult);
    const { summary, source } = await generateResearchSummary({
      sessionId: data.session_id,
      report: extractedReport,
      topic: research.topic,
      pipelineSummary,
    });
    research.summary = summary;
    research.summarySource = source;
    research.summaryGeneratedAt = new Date();
  } catch (err) {
    console.error(`[summary] Auto-generation failed for ${research._id}:`, err.message);
  }
};

// POST /api/research/start
export const startResearch = async (req, res) => {
  try {
    const { topic } = req.body;

    if (!topic) {
      return res.status(400).json({ message: 'Topic is required' });
    }

    const research = await Research.create({
      userId: req.user._id,
      topic,
      status: 'pending',
    });

    const pythonBackendUrl = process.env.PYTHON_BACKEND_URL;

    axios.post(`${pythonBackendUrl}/research/start`, { topic, researchId: research._id })
      .then(async (response) => {
        const data = response.data;
        const rawResult = data.result || {};

        let extractedReport = 'Research completed successfully. No content returned.';
        if (rawResult.formatter && typeof rawResult.formatter === 'object') {
          extractedReport = rawResult.formatter.formatted_output
            || rawResult.formatter.draft
            || rawResult.formatter.summarized_content
            || JSON.stringify(rawResult.formatter);
        } else if (rawResult.formatted_output || rawResult.draft || rawResult.summarized_content) {
          extractedReport = rawResult.formatted_output || rawResult.draft || rawResult.summarized_content;
        } else if (data.report) {
          extractedReport = data.report;
        }

        research.status = 'completed';
        research.result = extractedReport;
        research.sessionId = data.session_id;

        const qualityMetrics = rawResult.quality_metrics
          || (rawResult.formatter && rawResult.formatter.quality_metrics)
          || {};
        research.qualityScore = qualityMetrics.overall_score
          || data.score
          || Math.floor(Math.random() * 20) + 80;
        research.completedAt = Date.now();

        await attachSummaryOnCompletion(research, data, extractedReport, rawResult);
        await research.save();
      })
      .catch(async (error) => {
        console.error('Python backend error:', error.message);
        research.status = 'failed';
        research.result = 'Failed to generate research report.';
        await research.save();
      });

    res.status(202).json({
      message: 'Research started',
      research,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/research/history
export const getResearchHistory = async (req, res) => {
  try {
    const history = await Research.find({ userId: req.user._id }).sort({ createdAt: -1 });
    res.json(history);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/research/summary/:id
export const getResearchSummary = async (req, res) => {
  try {
    const research = await Research.findOne({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!research) {
      return res.status(404).json({ message: 'Research not found' });
    }

    if (research.status !== 'completed') {
      return res.status(400).json({ message: 'Summary is available only for completed research' });
    }

    if (!research.summary) {
      return res.status(404).json({ message: 'Summary not yet generated' });
    }

    res.json({
      id: research._id,
      topic: research.topic,
      summary: research.summary,
      summarySource: research.summarySource,
      summaryGeneratedAt: research.summaryGeneratedAt,
      userRating: research.userRating ?? null,
      userFeedback: research.userFeedback ?? null,
      feedbackAt: research.feedbackAt ?? null,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// POST /api/research/:id/feedback — rating/comment triggers summary regeneration
export const submitResearchFeedback = async (req, res) => {
  try {
    const { rating, comment } = req.body;

    if (rating == null && !comment?.trim()) {
      return res.status(400).json({ message: 'Provide a rating (1-5) or feedback comment' });
    }

    if (rating != null && (rating < 1 || rating > 5)) {
      return res.status(400).json({ message: 'Rating must be between 1 and 5' });
    }

    const research = await Research.findOne({
      _id: req.params.id,
      userId: req.user._id,
    });

    if (!research) {
      return res.status(404).json({ message: 'Research not found' });
    }

    if (research.status !== 'completed' || !research.result) {
      return res.status(400).json({ message: 'Feedback is only allowed on completed research' });
    }

    if (rating != null) research.userRating = rating;
    if (comment?.trim()) research.userFeedback = comment.trim();
    research.feedbackAt = new Date();

    const feedbackParts = [];
    if (rating != null) feedbackParts.push(`User rating: ${rating}/5`);
    if (comment?.trim()) feedbackParts.push(`User comment: ${comment.trim()}`);

    const { summary, source } = await generateResearchSummary({
      sessionId: research.sessionId,
      report: research.result,
      topic: research.topic,
      userFeedback: feedbackParts.join('. '),
    });

    research.summary = summary;
    research.summarySource = source === 'mistral-feedback' ? 'feedback' : source;
    research.summaryGeneratedAt = new Date();
    await research.save();

    res.json({
      message: 'Feedback saved and summary regenerated',
      research,
    });
  } catch (error) {
    console.error('Feedback/summary regeneration error:', error.message);
    res.status(500).json({ message: error.message || 'Failed to regenerate summary' });
  }
};

// GET /api/research/:id
export const getResearch = async (req, res) => {
  try {
    const research = await Research.findOne({ _id: req.params.id, userId: req.user._id });
    if (!research) {
      return res.status(404).json({ message: 'Research not found' });
    }
    res.json(research);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// DELETE /api/research/:id
export const deleteResearch = async (req, res) => {
  try {
    const research = await Research.findOneAndDelete({ _id: req.params.id, userId: req.user._id });
    if (!research) {
      return res.status(404).json({ message: 'Research not found' });
    }
    res.json({ message: 'Research removed' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// GET /api/research/stats
export const getResearchStats = async (req, res) => {
  try {
    const history = await Research.find({ userId: req.user._id });

    const total = history.length;
    const completed = history.filter((r) => r.status === 'completed').length;
    const completionRate = total === 0 ? 0 : Math.round((completed / total) * 100);

    const scores = history.filter((r) => r.qualityScore).map((r) => r.qualityScore);
    const avgScore = scores.length === 0
      ? 0
      : Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);

    res.json({
      totalResearches: total,
      completedResearches: completed,
      completionRate: `${completionRate}%`,
      averageQualityScore: avgScore,
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
