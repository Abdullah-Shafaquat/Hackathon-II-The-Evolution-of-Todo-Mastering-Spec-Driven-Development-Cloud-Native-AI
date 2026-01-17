'use client';

import { useEffect, useRef } from 'react';

interface UserProfileDropdownProps {
  isOpen: boolean;
  onClose: () => void;
  onViewProfile: () => void;
  onLogout: () => void;
  user: {
    email: string;
    name?: string;
  };
  buttonRef?: React.RefObject<HTMLElement>;
}

export default function UserProfileDropdown({
  isOpen,
  onClose,
  onViewProfile,
  onLogout,
  user,
  buttonRef
}: UserProfileDropdownProps) {
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        buttonRef?.current &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        onClose();
      }
    };

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen, onClose, buttonRef]);

  if (!isOpen) return null;

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

  return (
    <div
      ref={dropdownRef}
      className="absolute right-0 top-full mt-2 w-72 sm:w-80 bg-gradient-to-br from-gray-900 via-black to-gray-900 border-2 border-white rounded-2xl shadow-2xl shadow-white/20 z-50 animate-scale-in overflow-hidden"
    >
      {/* User Info Section */}
      <div className="p-5 border-b border-gray-700">
        <div className="flex items-center gap-4">
          {/* Avatar */}
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-white to-gray-400 rounded-full blur opacity-75"></div>
            <div className="relative w-14 h-14 rounded-full bg-gradient-to-br from-white via-gray-200 to-gray-300 border-2 border-black flex items-center justify-center shadow-xl">
              <span className="text-xl font-black text-black">{getInitials()}</span>
            </div>
          </div>

          {/* User Details */}
          <div className="flex-1 min-w-0">
            <h3 className="text-base font-bold text-white truncate mb-1">
              {user.name || 'User'}
            </h3>
            <p className="text-xs text-gray-400 truncate">
              {user.email}
            </p>
            <div className="mt-2 inline-flex items-center gap-1.5 px-2.5 py-1 bg-gray-800 rounded-lg border border-gray-700">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
              <span className="text-xs font-semibold text-gray-300">Active</span>
            </div>
          </div>
        </div>
      </div>

      {/* Menu Options */}
      <div className="p-2">
        {/* View Full Profile */}
        <button
          onClick={() => {
            onViewProfile();
            onClose();
          }}
          className="w-full flex items-center gap-3 px-4 py-3 text-left text-white hover:bg-gray-800 rounded-xl transition-all duration-200 group"
        >
          <div className="w-9 h-9 bg-gray-800 group-hover:bg-gray-700 rounded-lg flex items-center justify-center transition-colors">
            <svg className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <div className="flex-1">
            <div className="font-semibold text-sm">View Full Profile</div>
            <div className="text-xs text-gray-400 group-hover:text-gray-300">See your complete details</div>
          </div>
          <svg className="w-4 h-4 text-gray-500 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>

        {/* Divider */}
        <div className="h-px bg-gray-800 my-2"></div>

        {/* Logout */}
        <button
          onClick={() => {
            onLogout();
            onClose();
          }}
          className="w-full flex items-center gap-3 px-4 py-3 text-left text-white hover:bg-red-600/10 hover:border-red-600/50 rounded-xl transition-all duration-200 group border border-transparent"
        >
          <div className="w-9 h-9 bg-gray-800 group-hover:bg-red-600 rounded-lg flex items-center justify-center transition-all">
            <svg className="w-5 h-5 text-gray-400 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </div>
          <div className="flex-1">
            <div className="font-semibold text-sm group-hover:text-red-400 transition-colors">Logout</div>
            <div className="text-xs text-gray-400 group-hover:text-gray-300">Sign out of your account</div>
          </div>
        </button>
      </div>
    </div>
  );
}
