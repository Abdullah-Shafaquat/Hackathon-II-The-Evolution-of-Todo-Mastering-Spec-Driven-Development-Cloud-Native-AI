'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import Header from '@/components/layout/Header';
import ChatInterface from '@/components/chat/ChatInterface';
import ConversationList from '@/components/chat/ConversationList';

/**
 * Chat Page
 * AI-powered todo assistant chat interface
 *
 * Features:
 * - Protected route (requires authentication)
 * - Natural language task management
 * - Persistent conversation history
 * - Real-time AI responses with tool execution
 */
export default function ChatPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | undefined>();

  useEffect(() => {
    // Check authentication
    if (!api.isAuthenticated()) {
      router.push('/login');
      return;
    }

    setLoading(false);
  }, [router]);

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          {/* Animated loading spinner */}
          <div className="relative w-20 h-20 mx-auto mb-6">
            <div className="absolute inset-0 border-4 border-gray-800 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-transparent border-t-white rounded-full animate-spin"></div>
          </div>

          {/* Loading text with animation */}
          <div className="flex items-center justify-center gap-2">
            <span className="text-white text-lg font-medium">Loading</span>
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black flex flex-col">
      {/* Header */}
      <Header />

      {/* Floating Sidebar Toggle Button (Mobile Only) */}
      <button
        onClick={() => setSidebarOpen(!sidebarOpen)}
        className="lg:hidden fixed bottom-6 right-6 z-40 w-14 h-14 bg-gradient-to-br from-blue-600 to-purple-600 text-white rounded-full shadow-2xl hover:scale-110 transition-transform duration-300 flex items-center justify-center"
        aria-label="Toggle conversation history"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Main Content with Sidebar */}
      <main className="flex-1 flex overflow-hidden">
        {/* Conversation List Sidebar */}
        <ConversationList
          currentConversationId={currentConversationId}
          onSelectConversation={(id) => setCurrentConversationId(id)}
          onNewConversation={() => setCurrentConversationId(undefined)}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        {/* Chat Interface */}
        <div className="flex-1 flex flex-col">
          <ChatInterface
            conversationId={currentConversationId}
            onConversationIdChange={(id) => setCurrentConversationId(id)}
          />
        </div>
      </main>
    </div>
  );
}
