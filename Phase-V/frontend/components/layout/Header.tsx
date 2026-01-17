'use client';

import { useRouter, usePathname } from 'next/navigation';
import { useState } from 'react';
import UserProfileModal from '@/components/ui/UserProfileModal';
import WarningModal from '@/components/ui/WarningModal';
import { api } from '@/lib/api';

interface HeaderProps {
  title?: string;
  subtitle?: string;
  showAuth?: boolean;
  showNavigation?: boolean;
}

export default function Header({
  title,
  subtitle,
  showAuth = true,
  showNavigation = true
}: HeaderProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [showLogoutModal, setShowLogoutModal] = useState(false);
  const [user, setUser] = useState<any>(null);

  // Get user info if authenticated
  const isAuthenticated = api.isAuthenticated();
  const currentUser = isAuthenticated ? api.getUser() : null;

  // Auto-detect page title if not provided
  const getPageTitle = () => {
    if (title) return title;

    switch(pathname) {
      case '/dashboard': return 'Dashboard';
      case '/chat': return 'AI Assistant';
      case '/login': return 'Welcome Back';
      case '/signup': return 'Get Started';
      default: return 'Task Manager';
    }
  };

  // Get page subtitle
  const getPageSubtitle = () => {
    if (subtitle) return subtitle;

    switch(pathname) {
      case '/dashboard': return 'Manage your tasks efficiently';
      case '/chat': return 'Get help with your tasks';
      case '/login': return 'Sign in to your account';
      case '/signup': return 'Create your account';
      default: return 'Organize your life, one task at a time';
    }
  };

  const handleLogout = () => {
    setShowLogoutModal(true);
  };

  const confirmLogout = () => {
    api.logout();
    setShowLogoutModal(false);
    router.push('/login');
  };

  // Navigation items for authenticated users
  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
    { label: 'AI Chat', path: '/chat', icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' },
  ];

  // Get initials for profile avatar
  const getInitials = () => {
    if (!currentUser) return '?';
    if (currentUser.name) {
      return currentUser.name
        .split(' ')
        .map((n: string) => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    return currentUser.email[0].toUpperCase();
  };

  // Determine background based on page
  const isDashboard = pathname === '/dashboard';
  const headerBg = isDashboard
    ? 'bg-gradient-to-r from-slate-800 to-slate-900 border-b border-slate-700'
    : 'bg-gradient-to-r from-gray-900 to-black border-b border-gray-800';

  return (
    <>
      <header className={`sticky top-0 z-30 ${headerBg} shadow-lg backdrop-blur-sm bg-opacity-95`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Left: Logo and Title */}
            <div className="flex items-center gap-4">
              {/* Logo/Brand */}
              <button
                onClick={() => router.push(isAuthenticated ? '/dashboard' : '/')}
                className="flex items-center gap-2 group"
              >
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg transform group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div className="hidden sm:block">
                  <h1 className="text-lg font-bold text-white group-hover:text-blue-400 transition-colors">
                    {getPageTitle()}
                  </h1>
                  <p className="text-xs text-gray-400 -mt-1">
                    {getPageSubtitle()}
                  </p>
                </div>
              </button>

              {/* Navigation (only for authenticated users) */}
              {isAuthenticated && showNavigation && (
                <nav className="hidden md:flex items-center gap-2 ml-8">
                  {navItems.map((item) => (
                    <button
                      key={item.path}
                      onClick={() => router.push(item.path)}
                      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                        pathname === item.path
                          ? 'bg-blue-600 text-white shadow-lg'
                          : 'text-gray-300 hover:text-white hover:bg-gray-800'
                      }`}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                      </svg>
                      <span>{item.label}</span>
                    </button>
                  ))}
                </nav>
              )}
            </div>

            {/* Right: User Actions */}
            <div className="flex items-center gap-3">
              {isAuthenticated && showAuth ? (
                <>
                  {/* User Profile Button */}
                  <button
                    onClick={() => {
                      setUser(currentUser);
                      setShowProfileModal(true);
                    }}
                    className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-gray-600 rounded-lg transition-all duration-300 group"
                  >
                    {/* Avatar */}
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow-lg group-hover:scale-110 transition-transform duration-300">
                      {getInitials()}
                    </div>

                    {/* Name (hidden on mobile) */}
                    <div className="hidden sm:flex flex-col items-start">
                      <span className="text-sm font-semibold text-white">
                        {currentUser?.name || currentUser?.email.split('@')[0]}
                      </span>
                      <span className="text-xs text-gray-400">
                        View Profile
                      </span>
                    </div>

                    {/* Chevron */}
                    <svg className="w-4 h-4 text-gray-400 group-hover:text-white transition-colors hidden sm:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {/* Logout Button */}
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg"
                  >
                    <span className="hidden sm:inline">Logout</span>
                    <svg className="w-5 h-5 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                  </button>
                </>
              ) : (
                <>
                  {/* Login/Signup buttons for non-authenticated users */}
                  {pathname !== '/login' && pathname !== '/signup' && (
                    <>
                      <button
                        onClick={() => router.push('/login')}
                        className="px-4 py-2 text-gray-300 hover:text-white text-sm font-medium transition-colors"
                      >
                        Login
                      </button>
                      <button
                        onClick={() => router.push('/signup')}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold rounded-lg transition-all duration-300 hover:scale-105 shadow-lg"
                      >
                        Sign Up
                      </button>
                    </>
                  )}
                </>
              )}
            </div>
          </div>

          {/* Mobile Navigation (only for authenticated users) */}
          {isAuthenticated && showNavigation && (
            <div className="md:hidden border-t border-gray-800 py-2">
              <nav className="flex items-center gap-2">
                {navItems.map((item) => (
                  <button
                    key={item.path}
                    onClick={() => router.push(item.path)}
                    className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all duration-300 ${
                      pathname === item.path
                        ? 'bg-blue-600 text-white'
                        : 'text-gray-400 hover:text-white hover:bg-gray-800'
                    }`}
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                    </svg>
                    <span>{item.label}</span>
                  </button>
                ))}
              </nav>
            </div>
          )}
        </div>
      </header>

      {/* User Profile Modal */}
      {user && (
        <UserProfileModal
          isOpen={showProfileModal}
          onClose={() => setShowProfileModal(false)}
          user={user}
        />
      )}

      {/* Logout Confirmation Modal */}
      <WarningModal
        isOpen={showLogoutModal}
        onClose={() => setShowLogoutModal(false)}
        onConfirm={confirmLogout}
        title="Confirm Logout"
        message="Are you sure you want to logout? You will need to sign in again to access your tasks."
        confirmText="Yes, Logout"
        cancelText="Stay Logged In"
        variant="warning"
      />
    </>
  );
}
