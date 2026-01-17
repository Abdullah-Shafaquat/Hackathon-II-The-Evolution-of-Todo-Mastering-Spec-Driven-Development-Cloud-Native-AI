'use client';

import { useState, useEffect } from 'react';

export default function Clock() {
  const [time, setTime] = useState('');
  const [date, setDate] = useState('');

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();

      // Format time in Pakistan timezone (PKT GMT+5)
      const timeOptions: Intl.DateTimeFormatOptions = {
        timeZone: 'Asia/Karachi',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      };

      const dateOptions: Intl.DateTimeFormatOptions = {
        timeZone: 'Asia/Karachi',
        weekday: 'long',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      };

      const timeString = now.toLocaleTimeString('en-US', timeOptions);
      const dateString = now.toLocaleDateString('en-US', dateOptions);

      setTime(timeString);
      setDate(dateString);
    };

    // Update immediately
    updateClock();

    // Update every second
    const interval = setInterval(updateClock, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center gap-3 bg-gradient-to-br from-gray-900 to-black border border-gray-700 rounded-lg px-4 py-2.5 shadow-lg animate-fade-in">
      {/* Clock Icon */}
      <div className="relative">
        <svg
          className="w-6 h-6 text-white animate-pulse-slow"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
      </div>

      {/* Time and Date */}
      <div className="flex flex-col">
        <div className="flex items-baseline gap-2">
          <span className="text-lg font-bold text-white tracking-wide font-mono">
            {time}
          </span>
          <span className="text-xs font-semibold text-gray-400 uppercase">
            PKT
          </span>
        </div>
        <span className="text-xs text-gray-500 font-medium">
          {date}
        </span>
      </div>
    </div>
  );
}
