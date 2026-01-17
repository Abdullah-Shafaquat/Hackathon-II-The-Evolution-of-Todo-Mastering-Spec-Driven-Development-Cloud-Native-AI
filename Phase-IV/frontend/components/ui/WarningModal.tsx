'use client';

import { useEffect } from 'react';
import { createPortal } from 'react-dom';

interface WarningModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmText?: string;
  cancelText?: string;
  isLoading?: boolean;
  variant?: 'danger' | 'warning';
}

export default function WarningModal({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  isLoading = false,
  variant = 'danger'
}: WarningModalProps) {
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

  // Handle ESC key to close modal
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !isLoading) {
        onClose();
      }
    };

    if (isOpen) {
      window.addEventListener('keydown', handleEsc);
    }

    return () => {
      window.removeEventListener('keydown', handleEsc);
    };
  }, [isOpen, isLoading, onClose]);

  if (!isOpen) return null;

  // Make sure we're in browser environment
  if (typeof document === 'undefined') return null;

  const colors = {
    danger: {
      icon: 'text-red-400',
      iconBg: 'bg-red-500/20',
      iconBorder: 'border-red-500/30',
      button: 'bg-red-600 hover:bg-red-700',
      title: 'text-red-300'
    },
    warning: {
      icon: 'text-orange-400',
      iconBg: 'bg-orange-500/20',
      iconBorder: 'border-orange-500/30',
      button: 'bg-orange-600 hover:bg-orange-700',
      title: 'text-orange-300'
    }
  };

  const colorScheme = colors[variant];

  const modalContent = (
    <>
      {/* Backdrop - Blocks all background interaction */}
      <div
        className="fixed inset-0 bg-black/80 backdrop-blur-md z-[9998] animate-fade-in"
        onClick={(e) => {
          e.stopPropagation();
          if (!isLoading) onClose();
        }}
      />

      {/* Modal - Perfectly Centered */}
      <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 pointer-events-none">
        <div
          className="relative bg-gradient-to-br from-gray-900 to-black border-2 border-gray-800 rounded-2xl shadow-2xl max-w-md w-full animate-scale-in pointer-events-auto"
          onClick={(e) => e.stopPropagation()}
        >
        {/* Warning Icon */}
        <div className="flex justify-center pt-8 pb-4">
          <div className={`w-16 h-16 ${colorScheme.iconBg} ${colorScheme.iconBorder} border-2 rounded-full flex items-center justify-center animate-pulse`}>
            <svg
              className={`w-8 h-8 ${colorScheme.icon}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          </div>
        </div>

        {/* Content */}
        <div className="px-6 sm:px-8 pb-6">
          {/* Title */}
          <h2 className={`text-2xl sm:text-3xl font-bold text-center mb-4 ${colorScheme.title}`}>
            {title}
          </h2>

          {/* Message */}
          <p className="text-base sm:text-lg text-gray-300 text-center leading-relaxed mb-8">
            {message}
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3">
            {/* Cancel Button */}
            <button
              onClick={onClose}
              disabled={isLoading}
              className="flex-1 px-6 py-3.5 bg-gray-800 text-white border-2 border-gray-700 rounded-xl hover:bg-gray-700 hover:border-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-base font-bold transition-all duration-300 hover:scale-105 active:scale-95"
            >
              {cancelText}
            </button>

            {/* Confirm Button */}
            <button
              onClick={onConfirm}
              disabled={isLoading}
              className={`flex-1 px-6 py-3.5 ${colorScheme.button} text-white rounded-xl disabled:opacity-50 disabled:cursor-not-allowed text-base font-bold transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg flex items-center justify-center gap-2`}
            >
              {isLoading ? (
                <>
                  <svg
                    className="animate-spin h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Processing...
                </>
              ) : (
                confirmText
              )}
            </button>
          </div>
        </div>

        {/* Bottom decoration line */}
        <div className={`h-2 ${variant === 'danger' ? 'bg-gradient-to-r from-red-600 to-red-500' : 'bg-gradient-to-r from-orange-600 to-orange-500'} rounded-b-2xl`} />
        </div>
      </div>
    </>
  );

  // Render modal using Portal to ensure it's always at document body level
  return createPortal(modalContent, document.body);
}
