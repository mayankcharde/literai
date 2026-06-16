import React, { useContext, useState, useEffect } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { ThemeContext } from '../context/ThemeContext';
import {
  LogOut, LayoutDashboard, PlusCircle, Sun, Moon, Menu, X,
  Sparkles, ChevronRight, User2,
} from 'lucide-react';
import PageBackground from './PageBackground';

const Layout = () => {
  const { user, logout } = useContext(AuthContext);
  const { theme, toggleTheme } = useContext(ThemeContext);
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Close sidebar on route change
  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    const isDashboard = location.pathname === '/dashboard';
    document.body.classList.toggle('dashboard-route', isDashboard);
    return () => document.body.classList.remove('dashboard-route');
  }, [location.pathname]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, desc: 'Overview' },
    { name: 'New Research', path: '/submit', icon: PlusCircle, desc: 'Start a report' },
  ];

  const isActive = (path) =>
    path === '/dashboard' ? location.pathname === '/dashboard' : location.pathname.startsWith(path);

  const showPageBg = location.pathname === '/dashboard' || location.pathname === '/submit';

  return (
    <div className="min-h-screen flex transition-colors duration-300">
      {/* Decorative background orbs — research view only */}
      {!showPageBg && (
        <>
          <div
            className="bg-orb"
            style={{ width: 500, height: 500, background: 'radial-gradient(circle, #6366f1, transparent)', top: '-100px', left: '-100px' }}
          />
          <div
            className="bg-orb"
            style={{ width: 400, height: 400, background: 'radial-gradient(circle, #8b5cf6, transparent)', bottom: '10%', right: '-80px', animationDelay: '3s' }}
          />
        </>
      )}

      {/* ── MOBILE TOPBAR ── */}
      <div
        className={`md:hidden fixed top-0 left-0 right-0 z-40 flex items-center justify-between px-4 h-16 transition-all duration-300 ${
          scrolled ? 'glass shadow-xl' : 'bg-transparent'
        }`}
      >
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
          >
            <Sparkles size={16} className="text-white" />
          </div>
          <span
            className="text-xl font-bold"
            style={{
              background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            Literai
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full glass-sm hover:scale-110 transition-transform"
          >
            {theme === 'dark'
              ? <Sun size={18} className="text-amber-400" />
              : <Moon size={18} className="text-slate-600" />}
          </button>
          <button
            id="hamburger-menu-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-full glass-sm hover:scale-110 transition-transform"
          >
            {sidebarOpen
              ? <X size={22} className="text-slate-700 dark:text-slate-300" />
              : <Menu size={22} className="text-slate-700 dark:text-slate-300" />}
          </button>
        </div>
      </div>

      {/* ── MOBILE OVERLAY ── */}
      {sidebarOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* ── SIDEBAR ── */}
      <aside
        id="sidebar-nav"
        className={`
          fixed top-0 left-0 h-full w-72 z-40 flex flex-col
          transition-transform duration-300 ease-in-out
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}
        style={{
          background: theme === 'dark'
            ? 'linear-gradient(180deg, rgba(15,23,42,0.97) 0%, rgba(10,10,30,0.98) 100%)'
            : 'linear-gradient(180deg, rgba(255,255,255,0.97) 0%, rgba(248,250,255,0.98) 100%)',
          backdropFilter: 'blur(24px)',
          WebkitBackdropFilter: 'blur(24px)',
          borderRight: theme === 'dark'
            ? '1px solid rgba(99,102,241,0.15)'
            : '1px solid rgba(99,102,241,0.1)',
          boxShadow: '8px 0 40px rgba(0,0,0,0.15)',
        }}
      >
        {/* Sidebar header */}
        <div className="px-6 pt-8 pb-6">
          <div className="flex items-center gap-3 mb-1">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg"
              style={{
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                boxShadow: '0 4px 15px rgba(99,102,241,0.4)',
              }}
            >
              <Sparkles size={20} className="text-white" />
            </div>
            <div>
              <h1
                className="text-2xl font-bold leading-none"
                style={{
                  background: 'linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                }}
              >
                Literai
              </h1>
              <p className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">AI Research Platform</p>
            </div>
          </div>

          {/* Glowing divider */}
          <div
            className="h-px mt-5"
            style={{ background: 'linear-gradient(90deg, transparent, #6366f1, transparent)' }}
          />
        </div>

        {/* Nav links */}
        <nav className="flex-1 px-4 space-y-1.5">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const active = isActive(link.path);
            return (
              <Link
                key={link.name}
                to={link.path}
                id={`nav-${link.name.toLowerCase().replace(' ', '-')}`}
                className="relative flex items-center gap-3 px-4 py-3.5 rounded-2xl group overflow-hidden transition-all duration-200"
                style={{
                  background: active
                    ? 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1))'
                    : 'transparent',
                  border: active ? '1px solid rgba(99,102,241,0.25)' : '1px solid transparent',
                }}
              >
                {/* Active glow */}
                {active && (
                  <div
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 rounded-r-full"
                    style={{ background: 'linear-gradient(to bottom, #6366f1, #8b5cf6)' }}
                  />
                )}

                <div
                  className={`p-2 rounded-xl transition-all duration-200 ${
                    active
                      ? 'text-white shadow-lg'
                      : 'text-slate-500 dark:text-slate-400 group-hover:text-indigo-600 dark:group-hover:text-indigo-400'
                  }`}
                  style={active ? {
                    background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                    boxShadow: '0 4px 12px rgba(99,102,241,0.4)',
                  } : {}}
                >
                  <Icon size={18} />
                </div>

                <div className="flex-1">
                  <p className={`text-sm font-semibold ${
                    active
                      ? 'text-slate-900 dark:text-white'
                      : 'text-slate-600 dark:text-slate-300 group-hover:text-slate-900 dark:group-hover:text-white'
                  }`}>
                    {link.name}
                  </p>
                  <p className="text-xs text-slate-400 dark:text-slate-500">{link.desc}</p>
                </div>

                {active && (
                  <ChevronRight size={14} className="text-indigo-400 opacity-60" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Sidebar footer */}
        <div className="p-4 mt-auto">
          <div
            className="rounded-2xl p-4 mb-3"
            style={{
              background: theme === 'dark'
                ? 'rgba(99,102,241,0.07)'
                : 'rgba(99,102,241,0.05)',
              border: '1px solid rgba(99,102,241,0.12)',
            }}
          >
            {/* User info */}
            <div className="flex items-center gap-3 mb-3">
              <div
                className="w-9 h-9 rounded-full flex items-center justify-center text-white text-sm font-bold flex-shrink-0"
                style={{ background: 'linear-gradient(135deg, #6366f1, #8b5cf6)' }}
              >
                {user?.name?.charAt(0)?.toUpperCase() || <User2 size={16} />}
              </div>
              <div className="min-w-0">
                <p className="text-sm font-semibold text-slate-800 dark:text-slate-100 truncate">
                  {user?.name || 'User'}
                </p>
                <p className="text-xs text-slate-400 truncate">{user?.email}</p>
              </div>
              {/* Theme toggle */}
              <button
                onClick={toggleTheme}
                className="ml-auto p-1.5 rounded-lg hover:bg-white/50 dark:hover:bg-slate-800/50 transition-colors flex-shrink-0"
              >
                {theme === 'dark'
                  ? <Sun size={16} className="text-amber-400" />
                  : <Moon size={16} className="text-slate-500" />}
              </button>
            </div>

            {/* Logout */}
            <button
              id="logout-btn"
              onClick={handleLogout}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-[1.02] active:scale-95"
              style={{
                background: 'linear-gradient(135deg, rgba(239,68,68,0.1), rgba(220,38,38,0.1))',
                border: '1px solid rgba(239,68,68,0.2)',
                color: '#ef4444',
              }}
            >
              <LogOut size={15} />
              Sign Out
            </button>
          </div>
        </div>
      </aside>

      {/* ── MAIN CONTENT ── */}
      <main className={`flex-1 md:ml-72 min-h-screen relative z-10 ${showPageBg && location.pathname === '/dashboard' ? 'dashboard-page-active' : ''}`}>
        <PageBackground />
        <div className="relative z-10 pt-20 md:pt-0 p-4 md:p-8 min-h-screen">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Layout;
