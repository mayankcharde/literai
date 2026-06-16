import React, { useContext } from 'react';
import { useLocation } from 'react-router-dom';
import { ThemeContext } from '../context/ThemeContext';
import SideRays from './dashboardbg';

const PageBackground = () => {
  const { pathname } = useLocation();
  const { theme } = useContext(ThemeContext);
  const isDark = theme === 'dark';

  const isDashboard = pathname === '/dashboard';
  const isSubmit = pathname === '/submit';

  if (!isDashboard && !isSubmit) return null;

  if (isDashboard) {
    return (
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none" aria-hidden="true">
        <SideRays
          speed={2}
          rayColor1={isDark ? '#818cf8' : '#6366f1'}
          rayColor2={isDark ? '#a78bfa' : '#8b5cf6'}
          intensity={isDark ? 2.8 : 2.2}
          spread={2.4}
          origin="top-right"
          tilt={-10}
          saturation={1.6}
          blend={0.65}
          falloff={1.35}
          opacity={isDark ? 0.92 : 0.75}
        />
        <div className={`dashboard-page-scrim ${isDark ? 'dashboard-page-scrim--dark' : 'dashboard-page-scrim--light'}`} />
      </div>
    );
  }

  return (
    <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none" aria-hidden="true">
      <SideRays
        speed={1.1}
        rayColor1={isDark ? '#818cf8' : '#e0e7ff'}
        rayColor2={isDark ? '#a78bfa' : '#dbeafe'}
        intensity={isDark ? 1.0 : 0.65}
        spread={2.8}
        origin="top-left"
        tilt={6}
        saturation={isDark ? 1.2 : 1.0}
        blend={0.65}
        falloff={1.8}
        opacity={isDark ? 0.38 : 0.22}
      />
      <div className={`submit-page-scrim ${isDark ? 'submit-page-scrim--dark' : 'submit-page-scrim--light'}`} />
    </div>
  );
};

export default PageBackground;
