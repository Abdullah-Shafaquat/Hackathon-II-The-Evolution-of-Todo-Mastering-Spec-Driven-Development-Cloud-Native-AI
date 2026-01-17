'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';

export default function Home() {
  const router = useRouter();

  const handleGetStarted = () => {
    if (api.isAuthenticated()) {
      router.push('/dashboard');
    } else {
      router.push('/signup');
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black overflow-hidden">
      {/* Hero Section */}
      <div className="flex min-h-screen flex-col items-center justify-center px-6 py-12 sm:px-12 lg:px-24 relative">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/5 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        {/* Content */}
        <div className="text-center max-w-4xl mx-auto relative z-10">
          {/* Main heading */}
          <div className="mb-8 animate-fade-in">
            <h1 className="text-6xl sm:text-7xl lg:text-8xl font-bold mb-6 text-white tracking-tight">
              Task Master
            </h1>
            <div className="h-1 w-32 bg-white mx-auto rounded-full"></div>
          </div>

          {/* Subtitle */}
          <p className="text-xl sm:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto leading-relaxed animate-fade-in" style={{ animationDelay: '0.1s' }}>
            Organize your life with elegance. A powerful, minimal todo application designed for productivity.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-20 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <button
              onClick={handleGetStarted}
              className="group px-8 py-4 bg-white text-black font-bold text-lg rounded-xl hover:bg-gray-100 transition-all duration-300 shadow-2xl hover:shadow-white/20 hover:scale-105 active:scale-95"
            >
              <span className="flex items-center justify-center gap-2">
                Get Started
                <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
            </button>
            <Link
              href="/login"
              className="px-8 py-4 bg-transparent text-white font-bold text-lg rounded-xl border-2 border-white hover:bg-white hover:text-black transition-all duration-300 shadow-lg hover:shadow-white/20 hover:scale-105 active:scale-95"
            >
              Sign In
            </Link>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {/* Feature 1 */}
            <div className="group p-8 bg-gradient-to-br from-gray-900 to-black border-2 border-gray-800 rounded-2xl hover:border-white transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-white/10 animate-fade-in" style={{ animationDelay: '0.3s' }}>
              <div className="mb-4">
                <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Secure Authentication</h3>
              <p className="text-gray-400 leading-relaxed">
                Industry-standard JWT authentication keeps your tasks private and secure
              </p>
            </div>

            {/* Feature 2 */}
            <div className="group p-8 bg-gradient-to-br from-gray-900 to-black border-2 border-gray-800 rounded-2xl hover:border-white transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-white/10 animate-fade-in" style={{ animationDelay: '0.4s' }}>
              <div className="mb-4">
                <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Smart Task Management</h3>
              <p className="text-gray-400 leading-relaxed">
                Create, organize, and track tasks with timestamps in Pakistan Standard Time
              </p>
            </div>

            {/* Feature 3 */}
            <div className="group p-8 bg-gradient-to-br from-gray-900 to-black border-2 border-gray-800 rounded-2xl hover:border-white transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-white/10 animate-fade-in" style={{ animationDelay: '0.5s' }}>
              <div className="mb-4">
                <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-7 h-7 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Real-time Sync</h3>
              <p className="text-gray-400 leading-relaxed">
                PostgreSQL database ensures your data is always saved and accessible
              </p>
            </div>
          </div>
        </div>

        {/* Footer tagline */}
        <div className="absolute bottom-8 left-0 right-0 text-center animate-fade-in" style={{ animationDelay: '0.6s' }}>
          <p className="text-gray-500 text-sm">
            Built with modern technology for maximum productivity
          </p>
        </div>
      </div>
    </main>
  );
}
