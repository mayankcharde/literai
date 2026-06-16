import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileSearch, Sparkles, ArrowRight, Lightbulb,
  Bot, BookOpen, FileDown, AlertCircle, Zap,
} from 'lucide-react';
import api from '../services/api';
import ModernSpinner from '../components/ModernSpinner';

const EXAMPLE_TOPICS = [
  'Impact of quantum computing on modern cryptography',
  'Climate change mitigation strategies and economic impacts',
  'Large language models and their applications in healthcare',
  'Future of renewable energy: solar and wind trends',
];

const FEATURES = [
  { icon: Bot, label: 'Multi-Agent AI', desc: 'Coordinated research agents' },
  { icon: BookOpen, label: 'Deep Research', desc: 'Structured, cited reports' },
  { icon: FileDown, label: 'PDF Export', desc: 'Download when complete' },
];

const LOADING_STEPS = [
  'Spawning research agents',
  'Queuing topic analysis',
  'Preparing report pipeline',
];

const ResearchSubmit = () => {
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError('');

    try {
      await api.post('/research/start', { topic });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to start research. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div
      className="max-w-3xl mx-auto py-4 md:py-8 relative"
      style={{ animation: 'slide-up 0.5s ease forwards' }}
    >
      {/* ── Page heading ── */}
      <div className="text-center mb-8 md:mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-5 landing-badge">
          <Zap size={12} />
          New Research Project
        </div>
        <div
          className="inline-flex items-center justify-center w-16 h-16 rounded-2xl mb-5 animate-float"
          style={{
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
            boxShadow: '0 8px 28px rgba(99,102,241,0.4)',
          }}
        >
          <FileSearch size={28} className="text-white" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white tracking-tight mb-2">
          Start New Research
        </h1>
        <p className="text-sm md:text-base max-w-lg mx-auto leading-relaxed" style={{ color: 'var(--chat-meta)' }}>
          Describe your topic below — our multi-agent AI will research, write, and quality-check a full report for you.
        </p>
      </div>

      {/* ── Main form card ── */}
      <div className="rounded-3xl overflow-hidden submit-surface-card">
        <div
          className="h-1.5 w-full"
          style={{ background: 'linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4)' }}
        />

        <div className="p-6 md:p-10">
          {error && (
            <div className="p-4 rounded-2xl mb-6 text-sm flex items-start gap-3 alert-error">
              <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {loading ? (
            <div className="py-10">
              <ModernSpinner
                text="Initializing Agents..."
                subtext="Spinning up the multi-agent research pipeline"
                size="md"
              />
              <div className="mt-8 space-y-3 max-w-md mx-auto">
                {LOADING_STEPS.map((step, i) => (
                  <div
                    key={step}
                    className="flex items-center gap-3 text-sm"
                    style={{
                      color: 'var(--chat-meta)',
                      animation: `slide-up 0.4s ease forwards ${i * 0.15}s`,
                      opacity: 0,
                    }}
                  >
                    <div
                      className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 text-white text-xs font-bold"
                      style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
                    >
                      {i + 1}
                    </div>
                    <div className="flex-1 h-1.5 rounded-full overflow-hidden progress-track">
                      <div
                        className="h-full rounded-full animate-shimmer"
                        style={{
                          background: 'linear-gradient(90deg, transparent, rgba(99,102,241,0.6), transparent)',
                          width: '100%',
                          backgroundSize: '200% 100%',
                        }}
                      />
                    </div>
                    <span className="text-xs w-40 truncate">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-slate-800 dark:text-slate-100 mb-2">
                  Research Topic
                </label>
                <textarea
                  id="research-topic-input"
                  required
                  rows="5"
                  className="input-modern resize-none text-base leading-relaxed"
                  placeholder="e.g., The impact of quantum computing on modern cryptography algorithms..."
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                />
                <div className="flex items-center justify-between mt-2.5 gap-3">
                  <p className="text-xs flex items-center gap-1.5" style={{ color: 'var(--chat-meta)' }}>
                    <Lightbulb size={13} style={{ color: 'var(--accent-text)' }} />
                    Be specific for the most detailed, accurate results.
                  </p>
                  <span
                    className="text-xs font-medium flex-shrink-0 px-2 py-0.5 rounded-md"
                    style={{ background: 'var(--chip-bg)', color: 'var(--accent-text)' }}
                  >
                    {topic.length} chars
                  </span>
                </div>
              </div>

              <div className="rounded-2xl p-4 md:p-5 submit-examples-box">
                <p
                  className="text-xs font-semibold uppercase tracking-wider mb-3"
                  style={{ color: 'var(--accent-text)' }}
                >
                  Try an example
                </p>
                <div className="flex flex-wrap gap-2">
                  {EXAMPLE_TOPICS.map((ex) => (
                    <button
                      key={ex}
                      type="button"
                      onClick={() => setTopic(ex)}
                      className="text-xs px-3 py-2 rounded-xl hover:scale-105 active:scale-95 topic-chip"
                    >
                      {ex.length > 42 ? `${ex.substring(0, 42)}…` : ex}
                    </button>
                  ))}
                </div>
              </div>

              <button
                id="generate-report-btn"
                type="submit"
                disabled={!topic.trim()}
                className="w-full flex items-center justify-center gap-3 py-4 rounded-2xl font-bold text-white text-base transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                style={{
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4)',
                  backgroundSize: '200% 100%',
                  boxShadow: topic.trim() ? '0 8px 32px rgba(99,102,241,0.4)' : 'none',
                }}
              >
                <Sparkles size={20} />
                Generate Research Report
                <ArrowRight size={18} className="opacity-70" />
              </button>

              <p className="text-center text-xs font-medium" style={{ color: 'var(--chat-meta)' }}>
                Typical processing time: 2–5 minutes
              </p>
            </form>
          )}
        </div>
      </div>

      {/* ── Feature strip ── */}
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
        {FEATURES.map(({ icon: Icon, label, desc }) => (
          <div
            key={label}
            className="flex flex-col items-center gap-2.5 py-5 px-4 rounded-2xl text-center submit-feature-card card-hover"
          >
            <div
              className="w-11 h-11 rounded-xl flex items-center justify-center"
              style={{
                background: 'linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.1))',
                border: '1px solid var(--chip-border)',
              }}
            >
              <Icon size={20} style={{ color: 'var(--accent-text)' }} />
            </div>
            <span className="text-sm font-semibold text-slate-800 dark:text-slate-100">{label}</span>
            <span className="text-xs leading-snug" style={{ color: 'var(--chat-meta)' }}>{desc}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResearchSubmit;
