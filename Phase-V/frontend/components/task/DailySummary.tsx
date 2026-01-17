'use client';

import type { Task } from '@/lib/types';

interface DailySummaryProps {
  tasks: Task[];
}

export default function DailySummary({ tasks }: DailySummaryProps) {
  const today = new Date().toISOString().split('T')[0];

  // Calculate overdue tasks (not completed, due date in the past)
  const overdue = tasks.filter(t =>
    t.due_date && !t.completed && new Date(t.due_date) < new Date(today)
  ).length;

  // Calculate tasks due today (not completed)
  const dueToday = tasks.filter(t =>
    t.due_date === today && !t.completed
  ).length;

  // Calculate tasks completed today (updated_at is today and completed)
  const completedToday = tasks.filter(t => {
    if (!t.completed) return false;
    const updatedToday = t.updated_at?.startsWith(today);
    return updatedToday;
  }).length;

  // Calculate total pending tasks
  const pending = tasks.filter(t => !t.completed).length;

  // Calculate in progress tasks
  const inProgress = tasks.filter(t => t.status === 'in_progress').length;

  const MetricCard = ({
    value,
    label,
    icon,
    color,
    isActive
  }: {
    value: number;
    label: string;
    icon: string;
    color: string;
    isActive?: boolean;
  }) => (
    <div className={`
      group relative overflow-hidden
      p-5 rounded-2xl text-center
      transition-all duration-300
      hover:scale-105 hover:-translate-y-1
      ${isActive
        ? `bg-${color}-500/10 border-2 border-${color}-500/50 shadow-lg shadow-${color}-500/20`
        : 'bg-slate-800/50 border-2 border-slate-700/50'}
    `}>
      <div className="relative z-10">
        <div className={`text-4xl sm:text-5xl font-black mb-2 transition-colors ${
          isActive ? `text-${color}-400` : 'text-slate-400'
        }`}>
          {value}
        </div>
        <div className="text-sm font-semibold text-slate-300 flex items-center justify-center gap-2">
          <span className="text-lg">{icon}</span>
          {label}
        </div>
      </div>
      {/* Subtle gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/0 via-white/0 to-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl" />
    </div>
  );

  return (
    <div className="card bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700 p-6 sm:p-8 animate-slide-up">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/30">
            <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 className="text-2xl sm:text-3xl font-bold text-slate-100">
            Today&apos;s Summary
          </h3>
        </div>
        <div className="h-1.5 w-32 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        <MetricCard
          value={overdue}
          label="Overdue"
          icon="⚠️"
          color="red"
          isActive={overdue > 0}
        />
        <MetricCard
          value={dueToday}
          label="Due Today"
          icon="📅"
          color="purple"
          isActive={dueToday > 0}
        />
        <MetricCard
          value={completedToday}
          label="Completed"
          icon="✅"
          color="green"
          isActive={completedToday > 0}
        />
        <MetricCard
          value={inProgress}
          label="In Progress"
          icon="🔄"
          color="yellow"
          isActive={inProgress > 0}
        />
        <MetricCard
          value={pending}
          label="Pending"
          icon="📝"
          color="blue"
          isActive={pending > 0}
        />
        <MetricCard
          value={tasks.length}
          label="Total"
          icon="📋"
          color="slate"
          isActive={true}
        />
      </div>

      {/* Quick Insights */}
      {(overdue > 0 || dueToday > 0 || completedToday > 0) && (
        <div className="pt-6 border-t border-slate-700/50">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Quick Insights
          </p>
          <div className="flex flex-wrap gap-2">
            {overdue > 0 && (
              <span className="inline-flex items-center gap-2 px-4 py-2 bg-red-500/10 text-red-300 rounded-xl border border-red-500/30 font-semibold text-sm hover:bg-red-500/20 transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Focus on {overdue} overdue task{overdue > 1 ? 's' : ''}
              </span>
            )}
            {dueToday > 0 && (
              <span className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/10 text-purple-300 rounded-xl border border-purple-500/30 font-semibold text-sm hover:bg-purple-500/20 transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {dueToday} task{dueToday > 1 ? 's' : ''} need attention today
              </span>
            )}
            {completedToday > 0 && (
              <span className="inline-flex items-center gap-2 px-4 py-2 bg-green-500/10 text-green-300 rounded-xl border border-green-500/30 font-semibold text-sm hover:bg-green-500/20 transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Great job! {completedToday} completed today
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
