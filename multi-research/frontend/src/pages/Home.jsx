import React, { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';
import Lightfall from '../components/Background';
import {
  Sparkles, ArrowRight, Bot, BookOpen, MessageSquare, FileDown,
  Zap, BarChart2, Shield, Sun, Moon, ChevronRight, LayoutDashboard,
  Search, Cpu, FileText, GitBranch, Network,
} from 'lucide-react';

const FEATURES = [
  {
    icon: Bot,
    title: 'Multi-Agent Research',
    desc: 'Coordinated AI agents research, analyze, and synthesize information into structured reports.',
  },
  {
    icon: BookOpen,
    title: 'Deep Literature Review',
    desc: 'Comprehensive topic coverage with organized sections, citations, and quality scoring.',
  },
  {
    icon: MessageSquare,
    title: 'RAG-Powered Q&A',
    desc: 'Ask questions about any completed report and get instant, context-aware answers.',
  },
  {
    icon: FileDown,
    title: 'PDF Export',
    desc: 'Download polished research reports ready to share or reference offline.',
  },
  {
    icon: BarChart2,
    title: 'Quality Insights',
    desc: 'Track completion rates, quality scores, and research history from your dashboard.',
  },
  {
    icon: Shield,
    title: 'Secure & Private',
    desc: 'Your research projects are tied to your account and accessible only to you.',
  },
];

const STEPS = [
  {
    icon: Search,
    step: '01',
    title: 'Submit a Topic',
    desc: 'Describe what you want researched — the more specific, the better the report.',
  },
  {
    icon: Cpu,
    step: '02',
    title: 'Agents Work for You',
    desc: 'Our multi-agent pipeline researches, writes, and quality-checks your report.',
  },
  {
    icon: FileText,
    step: '03',
    title: 'Read, Ask & Export',
    desc: 'Review your report, chat with RAG, and export to PDF anytime.',
  },
];

const AGENT_ROLES = [
  'Orchestrator', 'Planner', 'Searcher', 'Analyzer',
  'Writer', 'Fact Checker', 'Reviewer', 'Summarizer', 'Formatter',
];

const Home = () => {
  const { user, loading } = useContext(AuthContext);
  const { theme, toggleTheme } = useContext(ThemeContext);
  const navigate = useNavigate();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    if (!loading && user) {
      navigate('/dashboard', { replace: true });
    }
  }, [user, loading, navigate]);

  if (loading || user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div
          className="w-8 h-8 rounded-full border-2 border-indigo-200 border-t-indigo-500"
          style={{ animation: 'spin 0.8s linear infinite' }}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-x-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 z-0 pointer-events-none" aria-hidden="true">
        <Lightfall
          className="w-full h-full"
          colors={theme === 'dark'
            ? ['#6366f1', '#8b5cf6', '#06b6d4']
            : ['#A6C8FF', '#818cf8', '#c4b5fd']}
          backgroundColor={theme === 'dark' ? '#080b14' : '#f1f5f9'}
          speed={0.35}
          streakCount={2}
          glow={theme === 'dark' ? 1.1 : 0.75}
          density={0.55}
          twinkle={0.9}
          zoom={3}
          backgroundGlow={theme === 'dark' ? 0.45 : 0.25}
          opacity={theme === 'dark' ? 0.9 : 0.65}
          mouseInteraction={false}
        />
        <div className="absolute inset-0 landing-bg-scrim" />
      </div>

      <div className="relative z-10">
      {/* ── Navbar ── */}
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled ? 'landing-nav--scrolled' : ''
        }`}
      >
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center transition-transform group-hover:scale-105"
              style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', boxShadow: '0 4px 14px rgba(99,102,241,0.35)' }}
            >
              <Sparkles size={18} className="text-white" />
            </div>
            <span className="text-xl font-bold landing-brand">Literai</span>
          </Link>

          <nav className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-medium landing-nav-link">Features</a>
            <a href="#architecture" className="text-sm font-medium landing-nav-link">Architecture</a>
            <a href="#how-it-works" className="text-sm font-medium landing-nav-link">How it works</a>
          </nav>

          <div className="flex items-center gap-2 sm:gap-3">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-xl landing-icon-btn"
              aria-label="Toggle theme"
            >
              {theme === 'dark'
                ? <Sun size={18} className="text-amber-400" />
                : <Moon size={18} className="text-slate-600" />}
            </button>
            <Link
              to="/login"
              className="hidden sm:inline-flex text-sm font-semibold px-4 py-2 rounded-xl landing-nav-link"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="inline-flex items-center gap-1.5 text-sm font-semibold px-4 py-2.5 rounded-xl text-white transition-all hover:scale-105 active:scale-95"
              style={{
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                boxShadow: '0 4px 16px rgba(99,102,241,0.35)',
              }}
            >
              Get Started
              <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </header>

      {/* ── Hero ── */}
      <section className="relative pt-28 pb-16 md:pt-36 md:pb-24 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            <div style={{ animation: 'slide-up 0.6s ease forwards' }}>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-6 landing-badge">
                <Zap size={12} />
                AI-Powered Research Platform
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-[3.25rem] font-extrabold leading-[1.1] tracking-tight mb-5 text-slate-900 dark:text-white">
                Research smarter with{' '}
                <span className="landing-gradient-text">multi-agent AI</span>
              </h1>

              <p className="text-base sm:text-lg leading-relaxed mb-8 max-w-lg" style={{ color: 'var(--chat-meta)' }}>
                Literai turns any topic into a comprehensive research report — written by coordinated AI agents,
                enriched with RAG Q&amp;A, and ready to export in minutes.
              </p>

              <div className="flex flex-col sm:flex-row gap-3 mb-8">
                <Link
                  to="/register"
                  className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl font-bold text-white text-sm transition-all hover:scale-[1.02] active:scale-95"
                  style={{
                    background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4)',
                    backgroundSize: '200% 100%',
                    boxShadow: '0 8px 30px rgba(99,102,241,0.35)',
                  }}
                >
                  <Sparkles size={18} />
                  Start Free
                  <ArrowRight size={16} className="opacity-80" />
                </Link>
                <Link
                  to="/login"
                  className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl font-semibold text-sm landing-secondary-btn"
                >
                  Sign In
                  <ChevronRight size={16} />
                </Link>
              </div>

              <div className="flex flex-wrap gap-6 text-sm" style={{ color: 'var(--chat-meta)' }}>
                <span className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  No credit card required
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
                  Reports in 2–5 minutes
                </span>
              </div>
            </div>

            {/* Hero preview card */}
            <div
              className="relative"
              style={{ animation: 'slide-up 0.6s ease forwards 0.15s', opacity: 0 }}
            >
              <div className="landing-preview-card rounded-3xl p-6 md:p-8">
                <div className="flex items-center gap-3 mb-5">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center"
                    style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
                  >
                    <FileText size={18} className="text-white" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-800 dark:text-white">Sample Report</p>
                    <p className="text-xs" style={{ color: 'var(--chat-meta)' }}>Quantum Computing &amp; Cryptography</p>
                  </div>
                  <span
                    className="ml-auto text-xs font-semibold px-2.5 py-1 rounded-full"
                    style={{ background: 'var(--status-completed-bg)', color: 'var(--status-completed)', border: '1px solid var(--status-completed-border)' }}
                  >
                    Completed
                  </span>
                </div>

                <div className="space-y-3 mb-5">
                  {['Executive Summary', 'Key Findings', 'Methodology', 'Conclusion'].map((section, i) => (
                    <div
                      key={section}
                      className="flex items-center gap-3 px-3 py-2.5 rounded-xl"
                      style={{ background: 'var(--chip-bg)', border: '1px solid var(--chip-border)' }}
                    >
                      <div
                        className="w-6 h-6 rounded-lg flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
                        style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
                      >
                        {i + 1}
                      </div>
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-200">{section}</span>
                      <ChevronRight size={14} className="ml-auto opacity-40" />
                    </div>
                  ))}
                </div>

                <div
                  className="flex items-center gap-2 px-4 py-3 rounded-2xl text-sm"
                  style={{ background: 'var(--chat-bot-surface)', border: '1px solid var(--chat-bot-border)', color: 'var(--chat-bot-text)' }}
                >
                  <MessageSquare size={15} style={{ color: 'var(--accent-text)' }} />
                  <span className="opacity-80">Ask: &quot;What are the main risks?&quot;</span>
                </div>
              </div>

              <div
                className="absolute -bottom-4 -left-4 sm:-left-6 px-4 py-3 rounded-2xl landing-preview-card"
                style={{ animation: 'float 6s ease-in-out infinite' }}
              >
                <p className="text-xs" style={{ color: 'var(--chat-meta)' }}>Quality Score</p>
                <p className="text-2xl font-bold" style={{ color: 'var(--accent-text)' }}>94%</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section id="features" className="py-16 md:py-24 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12 md:mb-16">
            <p className="text-sm font-semibold mb-2" style={{ color: 'var(--accent-text)' }}>Features</p>
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              Everything you need for AI research
            </h2>
            <p className="text-base max-w-2xl mx-auto" style={{ color: 'var(--chat-meta)' }}>
              From topic submission to interactive Q&amp;A — Literai handles the full research workflow.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div
                key={title}
                className="landing-feature-card rounded-2xl p-6 card-hover"
              >
                <div
                  className="w-11 h-11 rounded-xl flex items-center justify-center mb-4"
                  style={{ background: 'var(--chip-bg)', border: '1px solid var(--chip-border)' }}
                >
                  <Icon size={20} style={{ color: 'var(--accent-text)' }} />
                </div>
                <h3 className="text-base font-bold text-slate-800 dark:text-white mb-2">{title}</h3>
                <p className="text-sm leading-relaxed" style={{ color: 'var(--chat-meta)' }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Agent Architecture ── */}
      <section id="architecture" className="py-16 md:py-24 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-10 lg:gap-14 items-center">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-5 landing-badge">
                <Network size={12} />
                Multi-Agent Pipeline
              </div>
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4 leading-tight">
                Orchestrated agents working in sync
              </h2>
              <p className="text-base leading-relaxed mb-6" style={{ color: 'var(--chat-meta)' }}>
                Every research report runs through a coordinated graph of specialized agents —
                from planning and search to writing, fact-checking, review, and final formatting.
              </p>
              <ul className="space-y-3 mb-8">
                {[
                  'Orchestrator routes tasks across the agent graph',
                  'Feedback loops refine quality before delivery',
                  'Each agent has a dedicated role in the pipeline',
                ].map((item) => (
                  <li key={item} className="flex items-start gap-2.5 text-sm" style={{ color: 'var(--chat-bot-text)' }}>
                    <GitBranch size={15} className="flex-shrink-0 mt-0.5" style={{ color: 'var(--accent-text)' }} />
                    {item}
                  </li>
                ))}
              </ul>
              <div className="flex flex-wrap gap-2">
                {AGENT_ROLES.map((agent) => (
                  <span
                    key={agent}
                    className="text-xs font-medium px-2.5 py-1 rounded-lg landing-agent-chip"
                  >
                    {agent}
                  </span>
                ))}
              </div>
            </div>

            <div className="flex justify-center lg:justify-end">
              <div className="landing-diagram-card rounded-3xl p-4 sm:p-6 w-full max-w-sm lg:max-w-md">
                <div
                  className="flex items-center justify-between mb-4 px-1"
                >
                  <p className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--chat-meta)' }}>
                    Agent Workflow
                  </p>
                  <span
                    className="text-[10px] font-bold px-2 py-0.5 rounded-full"
                    style={{ background: 'var(--chip-bg)', color: 'var(--accent-text)', border: '1px solid var(--chip-border)' }}
                  >
                    LIVE GRAPH
                  </span>
                </div>
                <div className="rounded-2xl overflow-hidden bg-white dark:bg-slate-900/50 p-2 sm:p-3">
                  <img
                    src="/images/agent-workflow.png"
                    alt="Literai multi-agent research workflow showing orchestrator, planner, searcher, analyzer, writer, fact checker, reviewer, summarizer, and formatter agents"
                    className="landing-diagram-image"
                    loading="lazy"
                  />
                </div>
                <p className="text-center text-xs mt-4 leading-relaxed" style={{ color: 'var(--chat-meta)' }}>
                  Solid lines show primary flow · dashed lines show feedback &amp; revision loops
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── How it works ── */}
      <section id="how-it-works" className="py-16 md:py-24 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12 md:mb-16">
            <p className="text-sm font-semibold mb-2" style={{ color: 'var(--accent-text)' }}>How it works</p>
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              Three steps to your report
            </h2>
            <p className="text-base max-w-xl mx-auto" style={{ color: 'var(--chat-meta)' }}>
              Simple, fast, and fully automated.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {STEPS.map(({ icon: Icon, step, title, desc }, i) => (
              <div key={step} className="relative">
                {i < STEPS.length - 1 && (
                  <div
                    className="hidden md:block absolute top-10 left-[calc(50%+2rem)] w-[calc(100%-4rem)] h-px"
                    style={{ background: 'linear-gradient(90deg, var(--chip-border), transparent)' }}
                  />
                )}
                <div className="landing-feature-card rounded-2xl p-6 text-center h-full">
                  <div
                    className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4"
                    style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)', boxShadow: '0 6px 20px rgba(99,102,241,0.3)' }}
                  >
                    <Icon size={24} className="text-white" />
                  </div>
                  <span className="text-xs font-bold tracking-widest mb-2 block" style={{ color: 'var(--accent-text)' }}>
                    STEP {step}
                  </span>
                  <h3 className="text-lg font-bold text-slate-800 dark:text-white mb-2">{title}</h3>
                  <p className="text-sm leading-relaxed" style={{ color: 'var(--chat-meta)' }}>{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-16 md:py-20 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div
            className="rounded-3xl p-8 md:p-12 text-center relative overflow-hidden"
            style={{
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #7c3aed)',
              boxShadow: '0 20px 60px rgba(99,102,241,0.35)',
            }}
          >
            <div
              className="absolute inset-0 opacity-20 pointer-events-none"
              style={{ background: 'radial-gradient(circle at 30% 50%, white, transparent 60%)' }}
            />
            <div className="relative">
              <h2 className="text-2xl md:text-3xl font-bold text-white mb-3">
                Ready to start researching?
              </h2>
              <p className="text-indigo-100 text-sm md:text-base mb-8 max-w-lg mx-auto">
                Create your free account and generate your first AI research report in minutes.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <Link
                  to="/register"
                  className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-2xl font-bold text-indigo-700 bg-white text-sm transition-all hover:scale-105 active:scale-95"
                >
                  <Sparkles size={18} />
                  Create Free Account
                </Link>
                <Link
                  to="/login"
                  className="inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-2xl font-semibold text-white text-sm border border-white/30 hover:bg-white/10 transition-all"
                >
                  <LayoutDashboard size={18} />
                  Sign In
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t py-10 px-4 sm:px-6" style={{ borderColor: 'var(--surface-divider)' }}>
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div
              className="w-7 h-7 rounded-lg flex items-center justify-center"
              style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
            >
              <Sparkles size={14} className="text-white" />
            </div>
            <span className="font-bold landing-brand text-lg">Literai</span>
          </div>
          <p className="text-xs" style={{ color: 'var(--chat-meta)' }}>
            &copy; {new Date().getFullYear()} Literai. AI Research Platform.
          </p>
          {/* <div className="flex items-center gap-4 text-sm">
            <Link to="/login" className="landing-nav-link font-medium">Sign In</Link>
            <Link to="/register" className="font-semibold" style={{ color: 'var(--accent-text)' }}>Register</Link>
          </div> */}
        </div>
      </footer>
      </div>
    </div>
  );
};

export default Home;
