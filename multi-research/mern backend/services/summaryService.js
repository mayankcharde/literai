import axios from 'axios';

const MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions';
const SUMMARY_MAX_WORDS = 250;

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
  const base = process.env.PYTHON_BACKEND_URL;
  if (!base) throw new Error('PYTHON_BACKEND_URL is not configured');

  const researchId = sessionId || Date.now().toString(); // Use sessionId or temp id
  try {
    await axios.post(`${base}/research/rag/setup`, {
      research_id: researchId,
      report: report,
      topic: 'Research'
    }, {
      timeout: 90000,
    });
  } catch (err) {
    console.warn('[summary] RAG setup skipped:', err.message);
  }

  try {
    const { data } = await axios.get(`${base}/research/rag/summary`, {
      params: { research_id: researchId },
      timeout: 60000,
    });
    if (data?.summary) return data.summary;
  } catch (pythonErr) {
    console.warn('[summary] Python summary failed:', pythonErr.message);
  }

  // If Python fails, just return a simple summary from report
  return report.slice(0, 500) + (report.length > 500 ? '...' : '');
};

/** Mistral API fallback */
export const fetchMistralSummary = async (report, topic, userFeedback = '') => {
  const apiKey = process.env.MISTRAL_API_KEY;
  if (!apiKey) throw new Error('MISTRAL_API_KEY is not configured');

  const excerpt = report.length > 14000
    ? `${report.slice(0, 14000)}\n...[truncated]`
    : report;

  const prompt = userFeedback
    ? `The user gave this feedback on the previous summary: "${userFeedback}"\n\nRegenerate a better summary (150-250 words, 3-5 bullet points) for this research.\n\nTopic: ${topic}\n\nReport:\n${excerpt}`
    : `Summarize this research in 3-5 bullet points: ${excerpt}`;

  const { data } = await axios.post(
    MISTRAL_API_URL,
    {
      model: process.env.MISTRAL_MODEL || 'mistral-small-latest',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.35,
      max_tokens: 600,
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
