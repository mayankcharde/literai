import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import {
  FileText, CheckCircle, Clock, XCircle, TrendingUp, BarChart2,
  BookOpen, ChevronRight, Sparkles, ArrowRight, Activity, Calendar,
} from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import ModernSpinner from '../components/ModernSpinner';

const STAT_ACCENTS = [
  { id: 'stat-total', accent: 'dashboard-accent--indigo' },
  { id: 'stat-rate', accent: 'dashboard-accent--emerald' },
  { id: 'stat-quality', accent: 'dashboard-accent--violet' },
];

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [stats, setStats] = useState({
    totalResearches: 0,
    completedResearches: 0,
    completionRate: '0%',
    averageQualityScore: 0,
  });
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, historyRes] = await Promise.all([
          api.get('/research/stats'),
          api.get('/research/history'),
        ]);
        setStats(statsRes.data);
        setHistory(historyRes.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getStatusConfig = (status) => {
    switch (status) {
      case 'completed':
        return {
          icon: CheckCircle,
          color: 'var(--status-completed)',
          bg: 'var(--status-completed-bg)',
          label: 'Completed',
          border: 'var(--status-completed-border)',
        };
      case 'pending':
      case 'processing':
        return {
          icon: Clock,
          color: 'var(--status-processing)',
          bg: 'var(--status-processing-bg)',
          label: 'Processing',
          border: 'var(--status-processing-border)',
          spin: true,
        };
      case 'failed':
        return {
          icon: XCircle,
          color: 'var(--status-failed)',
          bg: 'var(--status-failed-bg)',
          label: 'Failed',
          border: 'var(--status-failed-border)',
        };
      default:
        return {
          icon: FileText,
          color: 'var(--status-default)',
          bg: 'var(--status-default-bg)',
          label: status,
          border: 'var(--status-default-border)',
        };
    }
  };

  const processingCount = history.filter(
    (h) => h.status === 'pending' || h.status === 'processing'
  ).length;

  const statCards = [
    {
      id: 'stat-total',
      title: 'Total Researches',
      value: stats.totalResearches,
      icon: FileText,
      desc: 'All-time projects',
      trend: `${stats.completedResearches} completed`,
    },
    {
      id: 'stat-rate',
      title: 'Completion Rate',
      value: stats.completionRate,
      icon: TrendingUp,
      desc: 'Success rate',
      trend: 'Across all reports',
    },
    {
      id: 'stat-quality',
      title: 'Avg Quality Score',
      value: stats.averageQualityScore || '—',
      icon: BarChart2,
      desc: 'Report quality',
      trend: 'AI-evaluated metric',
    },
  ];

  const today = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="rounded-3xl p-12 dashboard-glass">
          <ModernSpinner text="Loading Dashboard..." />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-4" style={{ animation: 'slide-up 0.5s ease forwards' }}>
      {/* ── Welcome banner ── */}
      <section className="dashboard-hero dashboard-glass rounded-3xl overflow-hidden">
        <div className="dashboard-hero__gradient" />
        <div className="relative px-6 md:px-8 py-7 md:py-8">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="min-w-0">
              <div className="flex items-center gap-2 mb-3">
                <span className="dashboard-pill">
                  <Activity size={13} />
                  Dashboard
                </span>
                <span className="text-xs hidden sm:inline-flex items-center gap-1.5" style={{ color: 'var(--chat-meta)' }}>
                  <Calendar size={12} />
                  {today}
                </span>
              </div>
              <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-slate-900 dark:text-white tracking-tight mb-2">
                Welcome back{user?.name ? `, ${user.name.split(' ')[0]}` : ''}
              </h1>
              <p className="text-sm md:text-base max-w-xl" style={{ color: 'var(--chat-meta)' }}>
                Track your AI research projects, monitor quality scores, and launch new reports from one place.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 flex-shrink-0">
              <Link
                to="/submit"
                id="new-research-btn"
                className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl font-semibold text-white text-sm transition-all hover:scale-[1.02] active:scale-95"
                style={{
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                  boxShadow: '0 8px 28px rgba(99,102,241,0.35)',
                }}
              >
                <Sparkles size={17} />
                New Research
                <ArrowRight size={15} className="opacity-80" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stat cards ── */}
      <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
        {statCards.map((card, i) => {
          const Icon = card.icon;
          const accent = STAT_ACCENTS[i]?.accent ?? 'dashboard-accent--indigo';

          return (
            <div
              key={card.id}
              id={card.id}
              className={`dashboard-stat-card dashboard-glass rounded-2xl overflow-hidden card-hover ${accent}`}
              style={{ animation: `slide-up 0.45s ease forwards ${i * 0.08}s`, opacity: 0 }}
            >
              <div className="dashboard-stat-card__bar" />
              <div className="p-6">
                <div className="flex items-start justify-between gap-4 mb-5">
                  <div className="dashboard-stat-icon">
                    <Icon size={20} className="text-white" />
                  </div>
                  <span className="dashboard-stat-tag">{card.desc}</span>
                </div>
                <p className="text-sm font-medium mb-1" style={{ color: 'var(--chat-meta)' }}>
                  {card.title}
                </p>
                <p className="text-3xl font-bold tracking-tight dashboard-stat-value">
                  {card.value}
                </p>
                <p className="text-xs mt-2" style={{ color: 'var(--chat-meta)' }}>
                  {card.trend}
                </p>
              </div>
            </div>
          );
        })}
      </section>

      {/* ── Recent research ── */}
      <section className="dashboard-glass rounded-3xl overflow-hidden">
        <div
          className="px-6 md:px-8 py-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
          style={{ borderBottom: '1px solid var(--surface-divider)' }}
        >
          <div className="flex items-center gap-3">
            <div className="dashboard-section-icon">
              <BookOpen size={16} className="text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-800 dark:text-white">Recent Research</h2>
              <p className="text-xs mt-0.5" style={{ color: 'var(--chat-meta)' }}>
                {stats.completedResearches} completed · {processingCount} in progress
              </p>
            </div>
          </div>
          <span className="dashboard-count-badge">{history.length} total</span>
        </div>

        {history.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 px-6 gap-5">
            <div className="dashboard-empty-icon animate-float">
              <FileText size={30} style={{ color: 'var(--accent-text)' }} />
            </div>
            <div className="text-center max-w-sm">
              <p className="font-semibold text-slate-800 dark:text-white text-lg">No research yet</p>
              <p className="text-sm mt-1.5" style={{ color: 'var(--chat-meta)' }}>
                Launch your first multi-agent research report and it will appear here.
              </p>
            </div>
            <Link
              to="/submit"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl text-sm font-semibold text-white transition-all hover:scale-105"
              style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
            >
              <Sparkles size={16} /> Start Your First Report
            </Link>
          </div>
        ) : (
          <div>
            {history.map((item, idx) => {
              const config = getStatusConfig(item.status);
              const StatusIcon = config.icon;
              const isClickable = item.status === 'completed';
              const formattedDate = new Date(item.createdAt).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric',
              });

              const rowClass = `group flex items-center gap-4 px-6 md:px-8 py-4 transition-all duration-200 ${
                isClickable
                  ? 'hover:bg-indigo-50/40 dark:hover:bg-indigo-500/10 cursor-pointer'
                  : 'cursor-default opacity-85'
              }`;

              const rowStyle = {
                borderBottom: idx < history.length - 1 ? '1px solid var(--surface-divider)' : 'none',
                animation: `slide-up 0.4s ease forwards ${idx * 0.04}s`,
                opacity: 0,
              };

              const rowInner = (
                <>
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                    style={{ background: config.bg, border: `1px solid ${config.border}` }}
                  >
                    <StatusIcon
                      size={18}
                      style={{ color: config.color, animation: config.spin ? 'spin 2s linear infinite' : undefined }}
                    />
                  </div>

                  <div className="flex-1 min-w-0">
                    <h4 className="font-semibold text-slate-800 dark:text-white truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                      {item.topic}
                    </h4>
                    {item.summary && (
                      <p className="text-xs mt-1 line-clamp-2 leading-relaxed" style={{ color: 'var(--chat-meta)' }}>
                        {item.summary}
                      </p>
                    )}
                    <p className="text-xs mt-0.5" style={{ color: 'var(--chat-meta)' }}>
                      {formattedDate}
                    </p>
                  </div>

                  <div className="flex items-center gap-3 flex-shrink-0">
                    {item.qualityScore && (
                      <span className="dashboard-score hidden sm:inline-flex">{item.qualityScore}</span>
                    )}
                    <span
                      className="px-3 py-1 text-xs font-semibold rounded-full whitespace-nowrap"
                      style={{ background: config.bg, color: config.color, border: `1px solid ${config.border}` }}
                    >
                      {config.label}
                    </span>
                    {isClickable && (
                      <ChevronRight
                        size={18}
                        className="text-slate-300 dark:text-slate-600 group-hover:text-indigo-500 dark:group-hover:text-indigo-400 group-hover:translate-x-0.5 transition-all"
                      />
                    )}
                  </div>
                </>
              );

              return isClickable ? (
                <Link
                  to={`/research/${item._id}`}
                  key={item._id}
                  id={`research-item-${item._id}`}
                  className={rowClass}
                  style={rowStyle}
                >
                  {rowInner}
                </Link>
              ) : (
                <div key={item._id} id={`research-item-${item._id}`} className={rowClass} style={rowStyle}>
                  {rowInner}
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
