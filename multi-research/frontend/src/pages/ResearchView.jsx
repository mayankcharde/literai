import React, { useState, useEffect, useRef, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import {
  Download, ArrowLeft, MessageSquare, Send, Bot, User,
  Cpu, FileText, Zap, ChevronDown, BookOpen, AlertCircle, Copy, Check, Star, Sparkles,
} from 'lucide-react';
import api from '../services/api';
import ModernSpinner from '../components/ModernSpinner';
import { ThemeContext } from '../context/ThemeContext';
import { downloadReportPdf, copyReportToClipboard } from '../utils/reportExport';

const ResearchView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { theme } = useContext(ThemeContext);
  const isDark = theme === 'dark';
  const [research, setResearch] = useState(null);
  const [loading, setLoading] = useState(true);

  // Chat state
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [ragReady, setRagReady] = useState(false);
  const [ragInitializing, setRagInitializing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [feedbackRating, setFeedbackRating] = useState(0);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const messagesEndRef = useRef(null);
  const chatInputRef = useRef(null);

  useEffect(() => {
    let interval;
    const fetchResearch = async () => {
      try {
        const { data } = await api.get(`/research/${id}`);
        setResearch(data);
        // Poll if still pending
        if (data.status === 'pending' || data.status === 'processing') {
          interval = setInterval(async () => {
            try {
              const { data: updated } = await api.get(`/research/${id}`);
              setResearch(updated);
              if (updated.status !== 'pending' && updated.status !== 'processing') {
                clearInterval(interval);
              }
            } catch (_) {}
          }, 5000);
        }
      } catch (error) {
        console.error('Error fetching research:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchResearch();
    return () => clearInterval(interval);
  }, [id]);

  // Auto-initialize RAG when research is completed
  useEffect(() => {
    if (research && research.status === 'completed' && research.result && !ragReady) {
      handleInitRag();
    }
  }, [research?.status, research?.result]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (research?.userRating) setFeedbackRating(research.userRating);
    if (research?.userFeedback) setFeedbackComment(research.userFeedback);
  }, [research?.userRating, research?.userFeedback]);

  const handleSubmitFeedback = async (e) => {
    e.preventDefault();
    if (!feedbackRating && !feedbackComment.trim()) return;

    setFeedbackLoading(true);
    setFeedbackMessage('');
    try {
      const { data } = await api.post(`/research/${id}/feedback`, {
        rating: feedbackRating || undefined,
        comment: feedbackComment.trim() || undefined,
      });
      setResearch(data.research);
      setFeedbackMessage('Summary updated based on your feedback.');
    } catch (err) {
      setFeedbackMessage(err.response?.data?.message || 'Failed to submit feedback.');
    } finally {
      setFeedbackLoading(false);
    }
  };

  const handleDownloadPDF = () => {
    if (!research?.result) return;
    downloadReportPdf({
      topic: research.topic,
      result: research.result,
      createdAt: research.createdAt,
      qualityScore: research.qualityScore,
    });
  };

  const handleCopyReport = async () => {
    if (!research?.result) return;
    try {
      await copyReportToClipboard(research.result);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy report:', err);
    }
  };

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim() || !ragReady) return;

    const userMessage = { type: 'user', text: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion('');
    setChatLoading(true);

    try {
      const { data } = await api.post('/rag/ask', {
        researchId: id,
        question: userMessage.text,
      });
      setMessages((prev) => [
        ...prev,
        { type: 'bot', text: data.answer, confidence: data.confidence, sources: data.sources },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { type: 'bot', text: 'Sorry, I encountered an error answering your question.', error: true },
      ]);
    } finally {
      setChatLoading(false);
      chatInputRef.current?.focus();
    }
  };

  const handleInitRag = async () => {
    if (ragInitializing || ragReady) return;
    setRagInitializing(true);
    try {
      await api.post('/rag/setup', { researchId: id });
      setRagReady(true);
      setMessages([{ type: 'bot', text: '✅ RAG system ready! I have indexed this research report. Ask me anything about it.' }]);
    } catch (err) {
      console.error('RAG init error:', err);
      setMessages([{ type: 'bot', text: '❌ Failed to initialize the RAG system. Please try again.', error: true }]);
      setRagInitializing(false);
    } finally {
      setRagInitializing(false);
    }
  };

  /* ── Loading state ── */
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[70vh]">
        <div className="glass rounded-3xl p-12">
          <ModernSpinner text="Fetching Research..." subtext="Loading from database" />
        </div>
      </div>
    );
  }

  if (!research) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <AlertCircle size={48} className="text-red-400" />
        <h2 className="text-xl font-semibold text-slate-600 dark:text-slate-300">Research not found</h2>
        <button onClick={() => navigate('/dashboard')} className="btn-primary">
          <ArrowLeft size={16} /> Back to Dashboard
        </button>
      </div>
    );
  }

  if (research.status === 'pending' || research.status === 'processing') {
    return (
      <div className="flex items-center justify-center min-h-[70vh]">
        <div
          className="rounded-3xl p-12 text-center max-w-md w-full mx-4"
          style={{
            background: 'linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08))',
            border: '1px solid rgba(99,102,241,0.2)',
            backdropFilter: 'blur(20px)',
          }}
        >
          <ModernSpinner
            text="Agents are researching..."
            subtext="This usually takes 2–5 minutes. You can navigate away."
            size="lg"
          />
          <div className="mt-8 flex items-center justify-center gap-2 text-xs text-slate-400">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            Auto-refreshing every 5 seconds
          </div>
        </div>
      </div>
    );
  }

  /* ── Main layout ── */
  return (
    <div
      className="flex flex-col gap-5"
      style={{ minHeight: 'calc(100vh - 4rem)', animation: 'slide-up 0.4s ease forwards' }}
    >
      {/* ── Report header ── */}
      <div
        className="px-4 md:px-8 py-4 flex items-center justify-between gap-3 flex-shrink-0 sticky top-0 z-10 rounded-3xl"
        style={{
          background: isDark ? 'rgba(15,23,42,0.92)' : 'rgba(255,255,255,0.85)',
          backdropFilter: 'blur(12px)',
          border: isDark ? '1px solid rgba(99,102,241,0.18)' : '1px solid rgba(99,102,241,0.12)',
        }}
      >
        <div className="flex items-center gap-3 min-w-0">
          <button
            onClick={() => navigate(-1)}
            id="back-btn"
            className="p-2 rounded-xl hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors flex-shrink-0"
          >
            <ArrowLeft size={20} className="text-slate-600 dark:text-slate-300" />
          </button>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <BookOpen size={16} className="text-indigo-500 flex-shrink-0" />
              <h1
                className="font-bold text-sm md:text-base truncate text-slate-800 dark:text-white"
                title={research.topic}
              >
                {research.topic}
              </h1>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              {new Date(research.createdAt).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
              {research.qualityScore ? ` · Quality: ${research.qualityScore}/10` : ''}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-shrink-0">
          <button
            id="copy-report-btn"
            onClick={handleCopyReport}
            disabled={!research.result}
            title="Copy full report"
            className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium transition-all hover:scale-105 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed"
            style={{
              background: copied ? 'var(--status-completed-bg)' : 'var(--chip-bg)',
              border: `1px solid ${copied ? 'var(--status-completed-border)' : 'var(--chip-border)'}`,
              color: copied ? 'var(--status-completed)' : 'var(--accent-text)',
            }}
          >
            {copied ? <Check size={15} /> : <Copy size={15} />}
            <span className="hidden sm:inline">{copied ? 'Copied!' : 'Copy'}</span>
          </button>
          <button
            id="download-pdf-btn"
            onClick={handleDownloadPDF}
            disabled={!research.result}
            className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-medium flex-shrink-0 transition-all hover:scale-105 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed"
            style={{
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
              color: 'white',
              boxShadow: '0 4px 12px rgba(99,102,241,0.3)',
            }}
          >
            <Download size={15} />
            <span className="hidden sm:inline">Export PDF</span>
          </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-5">
        {/* ══════════════════════════════
            RAG CHAT PANEL (FIRST)
        ══════════════════════════════ */}
        <div
          className="w-full lg:w-96 flex flex-col rounded-3xl overflow-hidden flex-shrink-0"
          style={{
            height: 'clamp(450px, 60vh, 700px)',
            background: isDark ? 'rgba(15,23,42,0.9)' : 'rgba(255,255,255,0.9)',
            border: isDark ? '1px solid rgba(139,92,246,0.2)' : '1px solid rgba(139,92,246,0.15)',
            backdropFilter: 'blur(20px)',
            boxShadow: isDark ? '0 8px 40px rgba(0,0,0,0.4)' : '0 8px 40px rgba(139,92,246,0.08)',
          }}
        >
          {/* Chat header */}
          <div
            className="px-5 py-4 flex items-center gap-3 flex-shrink-0"
            style={{
              background: 'var(--chat-header-bg)',
              borderBottom: '1px solid var(--surface-divider)',
            }}
          >
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', boxShadow: '0 4px 12px rgba(99,102,241,0.3)' }}
            >
              <MessageSquare size={17} className="text-white" />
            </div>
            <div>
              <h3 className="font-bold text-slate-800 dark:text-white text-sm">Ask the Report</h3>
              <p className="text-xs" style={{ color: 'var(--chat-meta)' }}>
                {ragReady ? (
                  <span className="flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
                    RAG system ready
                  </span>
                ) : 'Initialize to start chatting'}
              </p>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 relative">
            {!ragReady ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center">
                {ragInitializing ? (
                  <ModernSpinner text="Initializing RAG..." subtext="Indexing report chunks" size="sm" />
                ) : (
                  <>
                    <div
                      className="w-16 h-16 rounded-2xl flex items-center justify-center mb-5 animate-float"
                      style={{
                        background: 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15))',
                        border: '1px solid rgba(99,102,241,0.2)',
                      }}
                    >
                      <Cpu size={30} className="text-indigo-500" />
                    </div>
                    <h4 className="font-bold text-base text-slate-800 dark:text-white mb-2">RAG Not Initialized</h4>
                    <p className="text-sm text-slate-400 mb-6 leading-relaxed max-w-xs">
                      Enable AI-powered question answering for this specific research report.
                    </p>
                    <button
                      id="init-rag-btn"
                      onClick={handleInitRag}
                      className="flex items-center gap-2 px-6 py-3 rounded-2xl font-semibold text-white text-sm transition-all hover:scale-105 active:scale-95"
                      style={{
                        background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                        boxShadow: '0 4px 20px rgba(99,102,241,0.4)',
                      }}
                    >
                      <Zap size={16} />
                      Initialize RAG
                    </button>
                  </>
                )}
              </div>
            ) : (
              <>
                {messages.length === 0 && (
                  <div className="flex flex-col items-center justify-center h-full gap-3 text-sm" style={{ color: 'var(--chat-meta)' }}>
                    <ChevronDown size={24} className="opacity-40 animate-bounce" />
                    <p>Ask anything about this report!</p>
                  </div>
                )}

                {messages.map((msg, idx) => (
                  <div key={idx} className={`flex gap-2.5 ${msg.type === 'user' ? 'flex-row-reverse' : ''}`} style={{ animation: 'slide-up 0.25s ease forwards' }}>
                    <div
                      className={`w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0 text-white text-xs`}
                      style={{
                        background: msg.type === 'user'
                          ? 'linear-gradient(135deg, #6366f1, #8b5cf6)'
                          : 'linear-gradient(135deg, #8b5cf6, #a855f7)',
                        boxShadow: '0 2px 8px rgba(99,102,241,0.3)',
                      }}
                    >
                      {msg.type === 'user' ? <User size={13} /> : <Bot size={13} />}
                    </div>

                    <div
                      className={`max-w-[78%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
                        msg.type === 'user'
                          ? `rounded-tr-sm chat-user-bubble`
                          : msg.error
                            ? 'rounded-tl-sm chat-bot-bubble chat-bot-bubble--error'
                            : 'rounded-tl-sm chat-bot-bubble'
                      }`}
                    >
                      <p>{msg.text}</p>
                      {msg.confidence && (
                        <div
                          className="mt-1.5 pt-1.5 border-t text-xs flex items-center gap-1"
                          style={{ borderColor: 'var(--chat-bot-border)', color: 'var(--chat-meta)' }}
                        >
                          <Zap size={10} />
                          {(msg.confidence * 100).toFixed(0)}% confidence
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {chatLoading && (
                  <div className="flex gap-2.5">
                    <div
                      className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0"
                      style={{ background: 'linear-gradient(135deg, #8b5cf6, #a855f7)' }}
                    >
                      <Bot size={13} className="text-white" />
                    </div>
                    <div className="rounded-2xl rounded-tl-sm px-4 py-3 flex gap-1.5 items-center chat-bot-bubble">
                      {[0, 1, 2].map((i) => (
                        <div
                          key={i}
                          className="w-2 h-2 rounded-full"
                          style={{
                            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                            animation: `pulse 1.2s ease-in-out infinite ${i * 0.2}s`,
                          }}
                        />
                      ))}
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Chat input */}
          <div className="p-3 flex-shrink-0 chat-footer">
            <form onSubmit={handleAskQuestion} className="flex gap-2">
              <input
                ref={chatInputRef}
                id="chat-input"
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                disabled={!ragReady}
                placeholder={ragReady ? 'Ask anything about this report...' : 'Initialize RAG first...'}
                className="flex-1 text-sm px-4 py-2.5 rounded-xl outline-none transition-all chat-input-field focus:ring-2 focus:ring-indigo-500/40"
              />
              <button
                id="send-chat-btn"
                type="submit"
                disabled={!ragReady || chatLoading || !question.trim()}
                className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all hover:scale-105 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed"
                style={{
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  boxShadow: '0 4px 12px rgba(99,102,241,0.3)',
                }}
              >
                <Send size={15} className="text-white" />
              </button>
            </form>
          </div>
        </div>

        {/* ══════════════════════════════
            REPORT PANEL
        ══════════════════════════════ */}
        <div
          className="flex-1 flex flex-col rounded-3xl overflow-hidden"
          style={{
            background: isDark ? 'rgba(15,23,42,0.9)' : 'rgba(255,255,255,0.92)',
            backdropFilter: 'blur(20px)',
            border: isDark ? '1px solid rgba(99,102,241,0.18)' : '1px solid rgba(99,102,241,0.12)',
            boxShadow: isDark ? '0 8px 40px rgba(0,0,0,0.4)' : '0 8px 40px rgba(99,102,241,0.08)',
          }}
        >
          {/* Report body */}
          <div className="flex-1 overflow-y-auto p-4 md:p-10 space-y-6">
            {research.summary && (
              <div
                className="max-w-3xl mx-auto rounded-2xl p-5 md:p-6"
                style={{
                  background: 'var(--chip-bg)',
                  border: '1px solid var(--chip-border)',
                }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles size={16} style={{ color: 'var(--accent-text)' }} />
                  <h2 className="text-sm font-bold text-slate-800 dark:text-white uppercase tracking-wide">
                    Quick Summary
                  </h2>
                  {research.summaryGeneratedAt && (
                    <span className="text-xs ml-auto" style={{ color: 'var(--chat-meta)' }}>
                      {new Date(research.summaryGeneratedAt).toLocaleDateString()}
                    </span>
                  )}
                </div>
                <div className="text-sm leading-relaxed whitespace-pre-wrap" style={{ color: 'var(--chat-bot-text)' }}>
                  {research.summary}
                </div>
              </div>
            )}

            {/* Feedback — regenerates summary */}
            <div
              className="max-w-3xl mx-auto rounded-2xl p-5 md:p-6"
              style={{
                background: 'var(--surface-elevated)',
                border: '1px solid var(--surface-elevated-border)',
              }}
            >
              <h3 className="text-sm font-bold text-slate-800 dark:text-white mb-3">Rate this report</h3>
              <form onSubmit={handleSubmitFeedback} className="space-y-4">
                <div className="flex items-center gap-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      type="button"
                      onClick={() => setFeedbackRating(star)}
                      className="p-1 transition-transform hover:scale-110"
                      aria-label={`Rate ${star} stars`}
                    >
                      <Star
                        size={22}
                        className={star <= feedbackRating ? 'fill-amber-400 text-amber-400' : 'text-slate-300 dark:text-slate-600'}
                      />
                    </button>
                  ))}
                </div>
                <textarea
                  value={feedbackComment}
                  onChange={(e) => setFeedbackComment(e.target.value)}
                  rows={3}
                  placeholder="Optional: tell us what to improve — summary will regenerate..."
                  className="input-modern resize-none text-sm w-full"
                />
                <div className="flex items-center gap-3 flex-wrap">
                  <button
                    type="submit"
                    disabled={feedbackLoading || (!feedbackRating && !feedbackComment.trim())}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
                  >
                    {feedbackLoading ? 'Regenerating...' : 'Submit & Regenerate Summary'}
                  </button>
                  {feedbackMessage && (
                    <p className="text-xs" style={{ color: 'var(--chat-meta)' }}>{feedbackMessage}</p>
                  )}
                </div>
              </form>
            </div>

            {research.result ? (
              <div className="report-content max-w-3xl mx-auto">
                <h2 className="text-lg font-bold text-slate-800 dark:text-white mb-4">Full Report</h2>
                <ReactMarkdown>{research.result}</ReactMarkdown>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full gap-3 text-slate-400">
                <FileText size={48} className="opacity-40" />
                <p className="text-lg font-medium">No report content available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResearchView;
