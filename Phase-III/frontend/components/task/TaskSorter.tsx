'use client';

interface TaskSorterProps {
  currentSort: 'date' | 'priority' | 'status' | 'recent';
  onSortChange: (sort: 'date' | 'priority' | 'status' | 'recent') => void;
}

export default function TaskSorter({ currentSort, onSortChange }: TaskSorterProps) {
  return (
    <div className="flex items-center gap-3">
      <label htmlFor="sort" className="text-sm font-semibold text-slate-200 uppercase tracking-wide flex items-center gap-2">
        <svg className="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
        </svg>
        Sort By
      </label>
      <select
        id="sort"
        value={currentSort}
        onChange={(e) => onSortChange(e.target.value as any)}
        className="input cursor-pointer font-medium"
      >
        <option value="recent">Recently Added</option>
        <option value="date">Due Date</option>
        <option value="priority">Priority</option>
        <option value="status">Status</option>
      </select>
    </div>
  );
}
