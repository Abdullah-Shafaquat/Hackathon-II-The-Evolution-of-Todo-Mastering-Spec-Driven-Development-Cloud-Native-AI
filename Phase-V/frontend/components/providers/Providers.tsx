'use client';

import { ReactNode } from 'react';
import { ToastProvider } from '@/components/ui/ToastContainer';
import { VoiceProvider } from '@/contexts/VoiceContext';

interface ProvidersProps {
  children: ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  return (
    <ToastProvider>
      <VoiceProvider>
        {children}
      </VoiceProvider>
    </ToastProvider>
  );
}
