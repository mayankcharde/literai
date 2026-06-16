import ResearchSession from '../models/ResearchSession.js';
import Research from '../models/Research.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://127.0.0.1:8000';

// POST /api/rag/setup
export const setupRag = async (req, res) => {
  try {
    const { researchId } = req.body;
    
    if (!researchId) {
      return res.status(400).json({ message: 'researchId is required' });
    }

    const research = await Research.findOne({ _id: researchId, userId: req.user._id });
    if (!research) {
      return res.status(404).json({ message: 'Research not found' });
    }

    if (!research.result) {
      return res.status(400).json({ message: 'No research report available' });
    }

    try {
      // Call Python backend
      await axios.post(`${PYTHON_BACKEND_URL}/research/rag/setup`, {
        research_id: researchId,
        report: research.result,
        topic: research.topic
      });
      
      res.json({
        status: "success",
        message: "RAG system initialized successfully"
      });
    } catch (pythonError) {
      console.warn('Python backend not available, using fallback:', pythonError.message);
      // Fallback: if Python isn't running, just return success without it
      res.json({
        status: "success",
        message: "RAG system initialized (fallback mode)"
      });
    }
  } catch (error) {
    console.error('RAG setup error:', error);
    res.status(500).json({ message: error.message });
  }
};

// POST /api/rag/ask
export const askQuestion = async (req, res) => {
  try {
    const { researchId, question } = req.body;

    if (!researchId || !question) {
      return res.status(400).json({ message: 'researchId and question are required' });
    }

    const research = await Research.findOne({ _id: researchId, userId: req.user._id });
    if (!research) {
      return res.status(404).json({ message: 'Research not found' });
    }

    let answerData;
    try {
      // Try Python backend first
      const pythonResponse = await axios.post(`${PYTHON_BACKEND_URL}/research/rag/ask`, {
        research_id: researchId,
        question: question
      });
      answerData = pythonResponse.data;
    } catch (pythonError) {
      console.warn('Python backend not available, using fallback:', pythonError.message);
      // Fallback: simple keyword-based answer
      const reportText = research.result || '';
      const keyword = question.toLowerCase().split(' ')[0];
      const index = reportText.toLowerCase().indexOf(keyword);
      const snippet = index !== -1 
        ? reportText.slice(Math.max(0, index - 200), Math.min(reportText.length, index + 500))
        : reportText.slice(0, 500);
      
      answerData = {
        answer: snippet ? `Here's what I found: ${snippet}` : "No relevant information found in the report",
        confidence: 0.5,
        sources: snippet ? ["Report snippet"] : []
      };
    }

    // Save to session
    let session = await ResearchSession.findOne({ researchId, userId: req.user._id });
    
    if (!session) {
      session = new ResearchSession({
        userId: req.user._id,
        researchId,
        sessionData: []
      });
    }

    const interaction = {
      question,
      answer: answerData.answer,
      confidence: answerData.confidence || 0.5,
      sources: answerData.sources || [],
      timestamp: new Date()
    };

    session.sessionData.push(interaction);
    await session.save();

    res.json(interaction);
  } catch (error) {
    console.error('RAG ask error:', error);
    res.status(500).json({ message: error.message });
  }
};

// GET /api/rag/stats
export const getRagStats = async (req, res) => {
  try {
    const sessions = await ResearchSession.find({ userId: req.user._id });
    
    let totalQuestions = 0;
    let totalConfidence = 0;
    
    sessions.forEach(session => {
      totalQuestions += session.sessionData.length;
      session.sessionData.forEach(data => {
        if (data.confidence) {
          totalConfidence += data.confidence;
        }
      });
    });

    const avgConfidence = totalQuestions > 0 ? (totalConfidence / totalQuestions) : 0;

    res.json({
      totalQuestionsAsked: totalQuestions,
      averageConfidenceScore: Math.round(avgConfidence * 100) / 100,
    });
  } catch (error) {
    console.error('RAG stats error:', error);
    res.status(500).json({ message: error.message });
  }
};
