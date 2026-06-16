import React, { useState, useContext, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import AuthPageLayout from '../components/AuthPageLayout';
import { UserPlus, Mail, Lock, User, Sparkles, Eye, EyeOff, CheckCircle } from 'lucide-react';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { user, register } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) navigate('/dashboard', { replace: true });
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create account. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const passwordStrength = password.length === 0 ? 0 : password.length < 6 ? 1 : password.length < 10 ? 2 : 3;
  const strengthColors = ['', '#ef4444', '#f59e0b', '#10b981'];
  const strengthLabels = ['', 'Weak', 'Fair', 'Strong'];

  return (
    <AuthPageLayout>
      <div
        className="rounded-3xl overflow-hidden"
        style={{
          background: 'rgba(15,23,42,0.85)',
          border: '1px solid rgba(139,92,246,0.2)',
          backdropFilter: 'blur(24px)',
          boxShadow: '0 25px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(139,92,246,0.05) inset',
        }}
      >
          {/* Top gradient bar */}
          <div
            className="h-1"
            style={{ background: 'linear-gradient(90deg, #8b5cf6, #6366f1, #06b6d4)' }}
          />

          <div className="p-8 md:p-10">
            {/* Header */}
            <div className="text-center mb-8">
              <div
                className="inline-flex items-center justify-center w-14 h-14 rounded-2xl mb-4 animate-float"
                style={{
                  background: 'linear-gradient(135deg, #8b5cf6, #6366f1)',
                  boxShadow: '0 8px 25px rgba(139,92,246,0.5)',
                }}
              >
                <Sparkles size={26} className="text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-1">Create Account</h1>
              <p className="text-slate-400 text-sm">Join Literai and start researching with AI</p>
            </div>

            {error && (
              <div
                className="p-3.5 rounded-2xl mb-6 text-sm"
                style={{
                  background: 'rgba(239,68,68,0.1)',
                  border: '1px solid rgba(239,68,68,0.25)',
                  color: '#f87171',
                }}
              >
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Full Name */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Full Name</label>
                <div className="relative">
                  <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    id="register-name"
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="John Doe"
                    className="w-full pl-10 pr-4 py-3 rounded-xl text-sm outline-none transition-all"
                    style={{
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(139,92,246,0.2)',
                      color: 'white',
                    }}
                    onFocus={(e) => (e.target.style.borderColor = 'rgba(139,92,246,0.6)')}
                    onBlur={(e) => (e.target.style.borderColor = 'rgba(139,92,246,0.2)')}
                  />
                </div>
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Email</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    id="register-email"
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full pl-10 pr-4 py-3 rounded-xl text-sm outline-none transition-all"
                    style={{
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(139,92,246,0.2)',
                      color: 'white',
                    }}
                    onFocus={(e) => (e.target.style.borderColor = 'rgba(139,92,246,0.6)')}
                    onBlur={(e) => (e.target.style.borderColor = 'rgba(139,92,246,0.2)')}
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1.5">Password</label>
                <div className="relative">
                  <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    id="register-password"
                    type={showPass ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-10 py-3 rounded-xl text-sm outline-none transition-all"
                    style={{
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(139,92,246,0.2)',
                      color: 'white',
                    }}
                    onFocus={(e) => (e.target.style.borderColor = 'rgba(139,92,246,0.6)')}
                    onBlur={(e) => (e.target.style.borderColor = 'rgba(139,92,246,0.2)')}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPass(!showPass)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                  >
                    {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>

                {/* Password strength bar */}
                {password.length > 0 && (
                  <div className="mt-2 space-y-1">
                    <div className="flex gap-1.5">
                      {[1, 2, 3].map((level) => (
                        <div
                          key={level}
                          className="flex-1 h-1 rounded-full transition-all duration-300"
                          style={{
                            background: passwordStrength >= level
                              ? strengthColors[passwordStrength]
                              : 'rgba(255,255,255,0.1)',
                          }}
                        />
                      ))}
                    </div>
                    <p className="text-xs" style={{ color: strengthColors[passwordStrength] }}>
                      {strengthLabels[passwordStrength]} password
                    </p>
                  </div>
                )}
              </div>

              {/* Benefits list */}
              <div
                className="rounded-xl p-3 space-y-1.5"
                style={{ background: 'rgba(99,102,241,0.05)', border: '1px solid rgba(99,102,241,0.1)' }}
              >
                {['Unlimited AI research reports', 'RAG-powered question answering', 'PDF export & history'].map((b, i) => (
                  <div key={i} className="flex items-center gap-2 text-xs text-slate-400">
                    <CheckCircle size={12} className="text-violet-400 flex-shrink-0" />
                    {b}
                  </div>
                ))}
              </div>

              {/* Submit */}
              <button
                id="register-submit-btn"
                type="submit"
                disabled={loading}
                className="w-full flex items-center justify-center gap-2 py-3.5 rounded-xl font-bold text-white transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed"
                style={{
                  background: loading
                    ? 'rgba(139,92,246,0.4)'
                    : 'linear-gradient(135deg, #8b5cf6, #6366f1)',
                  boxShadow: loading ? 'none' : '0 4px 20px rgba(139,92,246,0.4)',
                }}
              >
                {loading ? (
                  <>
                    <div
                      className="w-4 h-4 rounded-full border-2 border-white/30 border-t-white"
                      style={{ animation: 'spin 0.8s linear infinite' }}
                    />
                    Creating Account...
                  </>
                ) : (
                  <>
                    <UserPlus size={18} />
                    Create Account
                  </>
                )}
              </button>
            </form>

            <p className="text-center text-slate-500 text-sm mt-6">
              Already have an account?{' '}
              <Link
                to="/login"
                className="font-semibold hover:text-white transition-colors"
                style={{ color: '#a78bfa' }}
              >
                Sign in
              </Link>
            </p>
            <p className="text-center mt-3">
              <Link to="/" className="text-xs text-slate-500 hover:text-slate-300 transition-colors">
                &larr; Back to home
              </Link>
            </p>
          </div>
        </div>
    </AuthPageLayout>
  );
};

export default Register;
