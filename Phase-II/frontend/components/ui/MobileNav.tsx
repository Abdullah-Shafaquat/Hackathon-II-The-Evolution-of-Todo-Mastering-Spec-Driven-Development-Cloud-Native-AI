'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavLink {
  href: string;
  label: string;
}

interface MobileNavProps {
  links: NavLink[];
  onLogout?: () => void;
  userName?: string;
}

export default function MobileNav({ links, onLogout, userName }: MobileNavProps) {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const toggleMenu = () => setIsOpen(!isOpen);
  const closeMenu = () => setIsOpen(false);

  return (
    <nav className="relative">
      {/* Desktop Navigation - hidden on mobile */}
      <div className="hidden lg:flex items-center gap-6">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`px-3 py-2 text-sm font-medium rounded-md transition-colors ${
              pathname === link.href
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            {link.label}
          </Link>
        ))}

        {userName && (
          <div className="text-sm text-gray-600 border-l pl-6">
            {userName}
          </div>
        )}

        {onLogout && (
          <button
            onClick={onLogout}
            className="px-4 h-10 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            Logout
          </button>
        )}
      </div>

      {/* Mobile Hamburger Button - visible on mobile/tablet */}
      <div className="lg:hidden flex items-center gap-4">
        {userName && (
          <span className="text-xs text-gray-600 truncate max-w-[120px]">
            {userName}
          </span>
        )}

        <button
          onClick={toggleMenu}
          className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 transition-colors"
          aria-expanded={isOpen}
          aria-label="Toggle navigation menu"
        >
          {/* Hamburger Icon */}
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="2"
            stroke="currentColor"
            aria-hidden="true"
          >
            {isOpen ? (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            ) : (
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6h16M4 12h16M4 18h16"
              />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="lg:hidden fixed inset-0 bg-black bg-opacity-25 z-40"
            onClick={closeMenu}
            aria-hidden="true"
          />

          {/* Menu Panel */}
          <div className="lg:hidden absolute right-0 top-12 w-64 bg-white rounded-lg shadow-lg z-50 py-2 border border-gray-200">
            <div className="px-4 py-3 border-b border-gray-200">
              <p className="text-sm font-medium text-gray-900">Menu</p>
            </div>

            <div className="py-2">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={closeMenu}
                  className={`block px-4 py-3 text-sm font-medium transition-colors ${
                    pathname === link.href
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </div>

            {onLogout && (
              <div className="border-t border-gray-200 pt-2 px-4 pb-3">
                <button
                  onClick={() => {
                    closeMenu();
                    onLogout();
                  }}
                  className="w-full h-11 px-4 text-sm font-medium text-red-700 bg-red-50 border border-red-200 rounded-md hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </nav>
  );
}
