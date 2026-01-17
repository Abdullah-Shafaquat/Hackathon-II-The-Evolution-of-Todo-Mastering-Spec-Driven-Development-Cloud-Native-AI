'use client';

import type { TaskCategory } from '@/lib/types';

interface CategoryFilterProps {
  selectedCategories: Set<TaskCategory>;
  onCategoryToggle: (category: TaskCategory | 'all') => void;
}

const categories: { value: TaskCategory | 'all'; label: string; icon: string }[] = [
  { value: 'all', label: 'All', icon: '📋' },
  { value: 'personal', label: 'Personal', icon: '👤' },
  { value: 'work', label: 'Work', icon: '💼' },
  { value: 'study', label: 'Study', icon: '📚' },
  { value: 'health', label: 'Health', icon: '💪' },
  { value: 'shopping', label: 'Shopping', icon: '🛒' },
  { value: 'other', label: 'Other', icon: '📌' },
];

export default function CategoryFilter({ selectedCategories, onCategoryToggle }: CategoryFilterProps) {
  return (
    <div className="flex flex-col gap-3">
      <label className="text-sm font-semibold text-slate-200 uppercase tracking-wide flex items-center gap-2">
        <svg className="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
        </svg>
        Filter by Category
      </label>
      <div className="flex flex-wrap gap-2">
        {categories.map((category) => {
          const isSelected = category.value === 'all'
            ? selectedCategories.size === 0
            : selectedCategories.has(category.value as TaskCategory);

          return (
            <button
              key={category.value}
              onClick={() => onCategoryToggle(category.value)}
              className={`
                inline-flex items-center gap-2 px-4 py-2 rounded-xl font-semibold text-sm
                transition-all duration-200 hover:scale-105 active:scale-95 border
                ${isSelected
                  ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/50 shadow-sm shadow-indigo-500/20'
                  : 'bg-slate-700/50 text-slate-300 border-slate-600 hover:border-slate-500 hover:bg-slate-600/50'
                }
              `}
            >
              <span>{category.icon}</span>
              <span>{category.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
