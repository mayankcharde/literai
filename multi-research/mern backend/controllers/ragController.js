import ResearchSession from '../models/ResearchSession.js';
import Research from '../models/Research.js';
import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

// In-memory storage for report chunks
const reportChunks = new Map();

const MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions';
const MISTRAL_API_KEY = process.env.MISTRAL_API_KEY;

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

    // Split report into chunks
    const chunks = [];
    const chunkSize = 1000;
    const overlap = 200;
    const text = research.result;
    
    for (let i = 0; i < text.length; i += chunkSize - overlap) {
      chunks.push({
        id: `chunk-${i}`,
        text: text.slice(i, i + chunkSize),
      });
    }

    reportChunks.set(researchId, chunks);
    
    res.json({
      status: "success",
      message: "RAG system initialized successfully",
      chunkCount: chunks.length,
      reportLength: text.length
    });
  } catch (error) {
    console.error('RAG setup error:', error);
    res.status(500).json({ message: error.message });
  }
};

// Simple keyword-based search
const findRelevantChunks = (query, chunks, topK = 5) => {
  const queryWords = query.toLowerCase().split(/\s+/).filter(w => w.length > 2);
  const scoredChunks = chunks.map(chunk => {
    let score = 0;
    const chunkText = chunk.text.toLowerCase();
    queryWords.forEach(word => {
      if (chunkText.includes(word)) score++;
    });
    return { ...chunk, score };
  });
  
  return scoredChunks
    .filter(c => c.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
};

// Generate answer using Mistral API
const generateAnswerWithMistral = async (question, relevantChunks, fullReport) => {
  // Build context from relevant chunks
  const context = relevantChunks.length > 0
    ? relevantChunks.map(c => c.text).join("\n\n---\n\n")
    : fullReport.slice(0, 4000);

 const systemPrompt = `You are a helpful, friendly, and professional research assistant for a Multi-Agent Research System. Your primary role is to answer questions based on the provided research report, but you can also use your general knowledge when questions are outside the report's scope.

PRIORITY RULES:
1. FIRST PRIORITY: If the question is DIRECTLY related to the report content → Answer using ONLY information from the report
2. SECOND PRIORITY: If the question is PARTIALLY related to the report → Combine report information with your general knowledge, clearly indicating what comes from the report vs. general knowledge
3. THIRD PRIORITY: If the question is COMPLETELY OUTSIDE the report's scope → Answer using your general knowledge (Mistral's training data), but clearly state that the answer is based on general knowledge, not the report

HANDLING DIFFERENT SCENARIOS:

Scenario 1: Question Fully Addressed in Report
- Answer using ONLY report information
- Start with: "According to the research report..."
- Reference specific findings and sections
- Use bullet points or numbered lists when appropriate
- Keep answers concise (150-300 words)

Scenario 2: Question Partially Addressed in Report
- Use report information where available
- Supplement with general knowledge for missing parts
- Clearly separate: "The report mentions [X]. Additionally, based on general knowledge, [Y]."
- Be transparent about what comes from the report vs. external knowledge

Scenario 3: Question Outside Report Scope (Out-of-Box Questions)
- Answer using your general knowledge (Mistral's training data)
- Begin with: "The research report doesn't cover this topic, but based on general knowledge..."
- Provide a clear, informative response
- Use conversational, professional language
- Offer to help with report-related questions: "Is there anything about [report topic] I can help with?"

GENERAL RESPONSE GUIDELINES:
- Use clear, friendly, and conversational language
- Keep answers concise but informative (150-300 words)
- For complex topics, break down into 2-4 key points
- Use bullet points or numbered lists when presenting multiple items
- Reference the report when applicable

EXAMPLES:

Example 1 (Report-based question):
User: "What are the main findings about quantum computing?"
Response: "According to the research report, the key findings on quantum computing include three main advancements: (1) improved qubit coherence times, (2) error correction protocols, and (3) scalable architectures. The report emphasizes that these developments could revolutionize cryptography by 2030."

Example 2 (Partially report-based question):
User: "How does quantum computing compare to classical computing?"
Response: "The research report mentions that quantum computers can solve certain problems exponentially faster than classical computers, particularly in cryptography. Additionally, based on general knowledge, classical computers process information using bits (0s and 1s), while quantum computers use qubits that can exist in multiple states simultaneously. This quantum advantage is called superposition."

Example 3 (Out-of-scope question):
User: "What is the best pizza in New York?"
Response: "The research report doesn't cover pizza or food recommendations—it focuses on quantum computing applications in cryptography. However, based on general knowledge, some of New York's most famous pizzerias include Lombardi's, Di Fara, and Joe's Pizza. Each offers a unique style with loyal followings. Is there anything about quantum computing I can help you with instead?"

REMEMBER:
- You are a versatile research assistant
- You prioritize report information when available
- You can answer any question using general knowledge when necessary
- Always be transparent about the source of your information
- Stay helpful, professional, and conversational`;

  const userPrompt = `Here is the research report context:\n\n${context}\n\nQuestion: ${question}\n\nAnswer based on the context above.`;

  try {
    if (!MISTRAL_API_KEY) {
      // Fallback without Mistral API
      return {
        answer: relevantChunks.length > 0
          ? `Here's what I found in the report:\n\n${relevantChunks.map(c => c.text).join("\n\n")}`
          : `The research report doesn't contain specific information about that. Is there something else about this research I can help you with?`,
        confidence: 0.5,
        sources: relevantChunks.map((c, i) => `Section ${i + 1}`)
      };
    }

    const response = await axios.post(
      MISTRAL_API_URL,
      {
        model: process.env.MISTRAL_MODEL || 'mistral-small-latest',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt }
        ],
        temperature: 0.4,
        max_tokens: 1000,
      },
      {
        headers: {
          Authorization: `Bearer ${MISTRAL_API_KEY}`,
          'Content-Type': 'application/json',
        },
        timeout: 30000,
      }
    );

    const answer = response.data.choices?.[0]?.message?.content?.trim() || 'Sorry, I could not generate an answer.';
    return {
      answer,
      confidence: relevantChunks.length > 0 ? 0.8 : 0.5,
      sources: relevantChunks.map((c, i) => `Section ${i + 1}`)
    };
  } catch (error) {
    console.warn('Mistral API error, using fallback:', error.message);
    // Fallback answer
    return {
      answer: relevantChunks.length > 0
        ? `Here's what I found in the report:\n\n${relevantChunks.map(c => c.text).join("\n\n")}`
        : `The research report doesn't contain specific information about that. Is there something else about this research I can help you with?`,
      confidence: 0.5,
      sources: relevantChunks.map((c, i) => `Section ${i + 1}`)
    };
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

    let chunks = reportChunks.get(researchId);
    
    // If not set up yet, create chunks temporarily
    if (!chunks || chunks.length === 0) {
      const tempChunks = [];
      const chunkSize = 1000;
      const overlap = 200;
      const text = research.result || '';
      
      for (let i = 0; i < text.length; i += chunkSize - overlap) {
        tempChunks.push({
          id: `chunk-${i}`,
          text: text.slice(i, i + chunkSize),
        });
      }
      chunks = tempChunks;
    }

    const relevantChunks = findRelevantChunks(question, chunks);
    const answerData = await generateAnswerWithMistral(question, relevantChunks, research.result || '');

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
      confidence: answerData.confidence,
      sources: answerData.sources,
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
