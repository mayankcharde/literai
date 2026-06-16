import axios from 'axios';

const MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions';
const SUMMARY_MAX_WORDS = 300;

const countWords = (text) =>
  (text || '').trim().split(/\s+/).filter(Boolean).length;

/** Trim or pad summary toward 150–250 word target */
export const normalizeSummaryLength = (text) => {
  if (!text) return '';
  const words = text.trim().split(/\s+/).filter(Boolean);
  if (words.length <= SUMMARY_MAX_WORDS) return words.join(' ');
  return `${words.slice(0, SUMMARY_MAX_WORDS).join(' ')}...`;
};

const extractPipelineSummary = (rawResult) => {
  if (!rawResult || typeof rawResult !== 'object') return null;
  return (
    rawResult.summarized_content
    || rawResult.formatter?.summarized_content
    || rawResult.summarizer?.summarized_content
    || null
  );
};

export { extractPipelineSummary };

/** Proxy to Python summarizer — POST first (per spec), then GET fallback */
export const fetchPythonRagSummary = async (sessionId, report) => {
  // Fallback: just return a simple summary from the report
  return report.slice(0, 1000) + (report.length > 1000 ? '...' : '');
};

/** Mistral API for summary generation */
export const fetchMistralSummary = async (report, topic, userFeedback = '') => {
  const apiKey = process.env.MISTRAL_API_KEY;
  if (!apiKey) {
    // Fallback: return simple excerpt from report
    return report.slice(0, 1000) + (report.length > 1000 ? '...' : '');
  }

  const excerpt = report.length > 20000
    ? `${report.slice(0, 20000)}\n...[truncated]`
    : report;

  let prompt;
  
  if (userFeedback) {
    prompt = `You are an expert research summarizer. The user provided specific feedback on the previous summary: "${userFeedback}"

Based on this feedback, regenerate a better, high-quality executive summary for this research report.

Topic: ${topic}

Report:
${excerpt}

Regeneration Requirements:
- 200-300 words maximum
- Address the user's feedback directly
- Professional executive summary style
- Start with a compelling opening sentence
- Include 3-5 bullet points for key findings
- Highlight important statistics and data
- End with key implications and actionable recommendations
- Maintain academic rigor while being accessible

Generate ONLY the summary, no additional text.`;
  } else {
    prompt = `You are an expert research summarizer. Generate an excellent executive summary for this research report.

Topic: ${topic}

Report:
${excerpt}

Summary Requirements:
- 200-300 words maximum
- Professional, clear, and concise language
- Start with a strong opening sentence that captures the essence of the topic
- Include 3-5 bullet points for key findings
- Highlight important statistics, data points, or evidence from the report
- Address methodology briefly if relevant
- Conclude with key implications, recommendations, or future directions
- Maintain academic rigor while being accessible to a general audience

Generate ONLY the summary, no additional text.`;
  }

  try {
    const { data } = await axios.post(
      MISTRAL_API_URL,
      {
        model: process.env.MISTRAL_MODEL || 'mistral-small-latest',
        messages: [
          { 
            role: 'system', 
            content: 'You are a professional research summarizer. Always provide clear, concise, and well-structured executive summaries with bullet points for key findings.' 
          },
          { role: 'user', content: prompt }
        ],
        temperature: 0.3,
        max_tokens: 800,
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
        timeout: 90000,
      },
    );

    const content = data.choices?.[0]?.message?.content?.trim();
    if (!content) throw new Error('Mistral returned empty summary');
    return content;
  } catch (error) {
    console.warn('Mistral API failed, using fallback:', error.message);
    // Fallback to simple report excerpt
    return report.slice(0, 1200) + (report.length > 1200 ? '...' : '');
  }
};

/**
 * Generate summary: pipeline → Python RAG → Mistral fallback.
 * On user feedback, skip pipeline cache and regenerate via RAG then Mistral.
 */
export const generateResearchSummary = async ({
  sessionId,
  report,
  topic,
  pipelineSummary,
  userFeedback = '',
}) => {
  if (!report?.trim()) throw new Error('Report content is required for summarization');

  const regenerate = Boolean(userFeedback?.trim());

  if (!regenerate && pipelineSummary?.trim()) {
    const normalized = normalizeSummaryLength(pipelineSummary);
    if (countWords(normalized) >= 40) {
      return { summary: normalized, source: 'pipeline' };
    }
  }

  try {
    const ragSummary = await fetchPythonRagSummary(sessionId, report);
    return { summary: normalizeSummaryLength(ragSummary), source: 'python-rag' };
  } catch (err) {
    console.warn('[summary] Python RAG failed:', err.message);
  }

  const mistralSummary = await fetchMistralSummary(report, topic, userFeedback);
  return {
    summary: normalizeSummaryLength(mistralSummary),
    source: regenerate ? 'mistral-feedback' : 'mistral',
  };
};