'use client';

import { useEffect } from 'react';
import { createPortal } from 'react-dom';

interface UserProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: {
    email: string;
    name?: string;
  };
}

export default function UserProfileModal({ isOpen, onClose, user }: UserProfileModalProps) {
  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Make sure we're in browser environment
  if (typeof document === 'undefined') return null;

  // Get initials for profile picture
  const getInitials = () => {
    if (user.name) {
      return user.name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    }
    return user.email[0].toUpperCase();
  };

  const modalContent = (
    <>
      {/* Animated Backdrop - Blocks all background interaction */}
      <div
        className="fixed inset-0 bg-gradient-to-br from-black/60 via-purple-900/40 to-blue-900/40 backdrop-blur-md z-[9998] animate-fade-in"
        onClick={onClose}
      />

      {/* Small Elegant Modal - Top Right Corner */}
      <div className="fixed top-20 right-6 z-[9999] w-[90%] max-w-sm sm:w-80 animate-float-in">
        {/* Decorative background effect */}
        <div className="absolute -inset-4 bg-gradient-to-r from-purple-500/10 via-transparent to-blue-500/10 blur-xl animate-pulse-slow"></div>
        
        <div
          className="relative bg-gradient-to-br from-gray-900/95 via-black/95 to-gray-900/95 border border-gray-800/50 rounded-2xl shadow-2xl shadow-purple-500/20 overflow-hidden backdrop-blur-xl pointer-events-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Glowing border effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/5 to-transparent animate-shimmer"></div>
          
          {/* Header with elegant styling */}
          <div className="relative px-4 pt-4 pb-3 border-b border-gray-800/50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {/* Profile avatar with glow */}
                <div className="relative group">
                  <div className="absolute -inset-1 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full blur opacity-30 group-hover:opacity-50 transition-opacity duration-300"></div>
                  <div className="relative w-10 h-10 rounded-full bg-gradient-to-br from-white via-gray-100 to-gray-300 flex items-center justify-center border-2 border-gray-800 shadow-lg">
                    <span className="text-sm font-black text-gray-900">{getInitials()}</span>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-sm font-bold text-white tracking-wide">User Profile</h3>
                  <div className="h-0.5 w-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mt-1"></div>
                </div>
              </div>
              
              {/* Elegant close button */}
              <button
                onClick={onClose}
                className="relative p-2 text-gray-400 hover:text-white bg-gray-900/50 hover:bg-gray-800/50 rounded-xl transition-all duration-300 group border border-gray-800/50 hover:border-gray-700/50"
                aria-label="Close"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/0 to-transparent group-hover:via-purple-500/20 transition-all duration-500"></div>
                <svg className="relative w-4 h-4 transform group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Content with glassmorphism effect */}
          <div className="relative p-4">
            {/* User Details - Elegant Cards */}
            <div className="space-y-3">
              {/* Name Card */}
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-xl blur group-hover:blur-sm transition-all duration-500"></div>
                <div className="relative bg-gray-900/60 rounded-xl p-3 border border-gray-800/50 backdrop-blur-sm group-hover:border-gray-700/50 transition-all duration-300">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-lg flex items-center justify-center border border-purple-500/30">
                      <svg className="w-4 h-4 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-400 uppercase tracking-widest">Name</label>
                      <div className="h-0.5 w-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mt-0.5"></div>
                    </div>
                  </div>
                  <p className="text-sm font-semibold text-white ml-11 truncate bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-300">
                    {user.name || 'Not provided'}
                  </p>
                </div>
              </div>

              {/* Email Card */}
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-cyan-500/10 rounded-xl blur group-hover:blur-sm transition-all duration-500"></div>
                <div className="relative bg-gray-900/60 rounded-xl p-3 border border-gray-800/50 backdrop-blur-sm group-hover:border-gray-700/50 transition-all duration-300">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-lg flex items-center justify-center border border-blue-500/30">
                      <svg className="w-4 h-4 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-400 uppercase tracking-widest">Email</label>
                      <div className="h-0.5 w-4 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full mt-0.5"></div>
                    </div>
                  </div>
                  <p className="text-xs font-medium text-gray-300 ml-11 truncate group-hover:text-white transition-colors duration-300">
                    {user.email}
                  </p>
                </div>
              </div>

              {/* Status Card */}
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-green-500/10 to-emerald-500/10 rounded-xl blur group-hover:blur-sm transition-all duration-500"></div>
                <div className="relative bg-gray-900/60 rounded-xl p-3 border border-gray-800/50 backdrop-blur-sm group-hover:border-gray-700/50 transition-all duration-300">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-lg flex items-center justify-center border border-green-500/30">
                      <svg className="w-4 h-4 text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                    </div>
                    <div>
                      <label className="text-xs font-medium text-gray-400 uppercase tracking-widest">Status</label>
                      <div className="h-0.5 w-4 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full mt-0.5"></div>
                    </div>
                  </div>
                  <div className="ml-11">
                    <span className="inline-flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-300 text-xs font-semibold rounded-lg border border-green-500/30 shadow-lg shadow-green-500/10">
                      <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-gradient-to-r from-green-400 to-emerald-400"></span>
                      </span>
                      Active • Verified
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Elegant Action Button */}
            <button
              onClick={onClose}
              className="relative w-full mt-4 px-6 py-3 bg-gradient-to-r from-gray-900 to-black text-white text-sm font-semibold rounded-xl transition-all duration-300 group overflow-hidden border border-gray-800/50 hover:border-purple-500/50 hover:scale-[1.02] active:scale-[0.98] shadow-xl shadow-black/30"
            >
              {/* Button background effects */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/0 to-transparent group-hover:via-purple-500/20 transition-all duration-500"></div>
              <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-transparent to-blue-500/0 group-hover:from-purple-500/10 group-hover:to-blue-500/10 transition-all duration-500"></div>
              
              <span className="relative flex items-center justify-center gap-2">
                <svg className="w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
                Continue
              </span>
            </button>
          </div>
        </div>
      </div>

      {/* Add these animations to your global CSS or Tailwind config */}
      <style jsx global>{`
        @keyframes float-in {
          0% {
            opacity: 0;
            transform: scale(0.9);
          }
          100% {
            opacity: 1;
            transform: scale(1);
          }
        }
        
        @keyframes shimmer {
          0% {
            background-position: -200% center;
          }
          100% {
            background-position: 200% center;
          }
        }
        
        @keyframes pulse-slow {
          0%, 100% {
            opacity: 0.1;
          }
          50% {
            opacity: 0.2;
          }
        }
        
        .animate-float-in {
          animation: float-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        .animate-shimmer {
          background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(168, 85, 247, 0.1) 20%,
            rgba(59, 130, 246, 0.1) 40%,
            transparent 60%
          );
          background-size: 200% 100%;
          animation: shimmer 3s infinite linear;
        }
        
        .animate-pulse-slow {
          animation: pulse-slow 4s ease-in-out infinite;
        }
      `}</style>
    </>
  );

  // Render modal using Portal to ensure it's always at document body level
  return createPortal(modalContent, document.body);
}