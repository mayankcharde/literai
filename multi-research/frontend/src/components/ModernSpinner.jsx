import React, { useEffect, useState } from 'react';

const LOADING_PHRASES = [
  'Synthesizing data...',
  'Analyzing sources...',
  'Building insights...',
  'Connecting patterns...',
  'Crafting intelligence...',
];

const ModernSpinner = ({ text = 'Loading...', subtext = '', size = 'md' }) => {
  const [phraseIndex, setPhraseIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPhraseIndex((prev) => (prev + 1) % LOADING_PHRASES.length);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const sizeMap = {
    sm: { outer: 56, mid: 44, inner: 32, dot: 8 },
    md: { outer: 88, mid: 68, inner: 50, dot: 12 },
    lg: { outer: 120, mid: 96, inner: 72, dot: 16 },
  };

  const s = sizeMap[size] || sizeMap.md;

  return (
    <div className="flex flex-col items-center justify-center gap-6 select-none">
      {/* Spinner rings */}
      <div
        className="relative flex items-center justify-center"
        style={{ width: s.outer, height: s.outer }}
      >
        {/* Ripple glow pulse */}
        <div
          className="absolute rounded-full opacity-20"
          style={{
            width: s.outer,
            height: s.outer,
            background: 'radial-gradient(circle, #6366f1, transparent 70%)',
            animation: 'ripple 2s ease-out infinite',
          }}
        />
        <div
          className="absolute rounded-full opacity-15"
          style={{
            width: s.outer,
            height: s.outer,
            background: 'radial-gradient(circle, #8b5cf6, transparent 70%)',
            animation: 'ripple 2s ease-out infinite 0.7s',
          }}
        />

        {/* Outer ring — gradient stroke */}
        <svg
          className="absolute"
          style={{
            width: s.outer,
            height: s.outer,
            animation: 'spin 2.5s linear infinite',
          }}
          viewBox={`0 0 ${s.outer} ${s.outer}`}
        >
          <defs>
            <linearGradient id="ring-grad-outer" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#6366f1" stopOpacity="1" />
              <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.1" />
            </linearGradient>
          </defs>
          <circle
            cx={s.outer / 2}
            cy={s.outer / 2}
            r={s.outer / 2 - 3}
            fill="none"
            stroke="url(#ring-grad-outer)"
            strokeWidth="3"
            strokeLinecap="round"
            strokeDasharray={`${(s.outer / 2 - 3) * 2 * Math.PI * 0.75} ${(s.outer / 2 - 3) * 2 * Math.PI * 0.25}`}
          />
        </svg>

        {/* Middle ring — reverse spin */}
        <svg
          className="absolute"
          style={{
            width: s.mid,
            height: s.mid,
            animation: 'spin 1.8s linear infinite reverse',
          }}
          viewBox={`0 0 ${s.mid} ${s.mid}`}
        >
          <defs>
            <linearGradient id="ring-grad-mid" x1="100%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#a855f7" stopOpacity="1" />
              <stop offset="60%" stopColor="#ec4899" stopOpacity="0.5" />
              <stop offset="100%" stopColor="#a855f7" stopOpacity="0" />
            </linearGradient>
          </defs>
          <circle
            cx={s.mid / 2}
            cy={s.mid / 2}
            r={s.mid / 2 - 2.5}
            fill="none"
            stroke="url(#ring-grad-mid)"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeDasharray={`${(s.mid / 2 - 2.5) * 2 * Math.PI * 0.6} ${(s.mid / 2 - 2.5) * 2 * Math.PI * 0.4}`}
          />
        </svg>

        {/* Inner ring — fast spin */}
        <svg
          className="absolute"
          style={{
            width: s.inner,
            height: s.inner,
            animation: 'spin 1.2s linear infinite',
          }}
          viewBox={`0 0 ${s.inner} ${s.inner}`}
        >
          <circle
            cx={s.inner / 2}
            cy={s.inner / 2}
            r={s.inner / 2 - 2}
            fill="none"
            stroke="#06b6d4"
            strokeWidth="2"
            strokeLinecap="round"
            strokeDasharray={`${(s.inner / 2 - 2) * 2 * Math.PI * 0.4} ${(s.inner / 2 - 2) * 2 * Math.PI * 0.6}`}
            opacity="0.8"
          />
        </svg>

        {/* Core glowing dot */}
        <div
          className="rounded-full"
          style={{
            width: s.dot,
            height: s.dot,
            background: 'radial-gradient(circle, #e0e7ff, #6366f1)',
            boxShadow: `0 0 ${s.dot * 1.5}px ${s.dot / 2}px rgba(99,102,241,0.8), 0 0 ${s.dot * 3}px rgba(139,92,246,0.4)`,
            animation: 'pulse 1.5s ease-in-out infinite',
          }}
        />
      </div>

      {/* Text area */}
      <div className="flex flex-col items-center gap-2 text-center">
        <p
          className="font-semibold text-base"
          style={{
            background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          {text}
        </p>

        {/* Rotating phrases */}
        <p
          key={phraseIndex}
          className="text-xs text-slate-400 dark:text-slate-500"
          style={{ animation: 'slide-up 0.4s ease forwards' }}
        >
          {subtext || LOADING_PHRASES[phraseIndex]}
        </p>

        {/* Animated progress dots */}
        <div className="flex gap-1.5 mt-1">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className="rounded-full"
              style={{
                width: 5,
                height: 5,
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                animation: `pulse 1.4s ease-in-out infinite ${i * 0.2}s`,
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ModernSpinner;
