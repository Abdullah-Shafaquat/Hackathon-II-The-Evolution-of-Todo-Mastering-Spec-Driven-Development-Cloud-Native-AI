'use client';

interface TaskFiltersProps {
  currentFilter: 'all' | 'pending' | 'completed';
  onFilterChange: (filter: 'all' | 'pending' | 'completed') => void;
}

export default function TaskFilters({ currentFilter, onFilterChange }: TaskFiltersProps) {
  const filters: Array<{ value: 'all' | 'pending' | 'completed'; label: string }> = [
    { value: 'all', label: 'All Tasks' },
    { value: 'pending', label: 'Pending' },
    { value: 'completed', label: 'Completed' },
  ];

  return (
    <div className="flex gap-2 sm:gap-3 mb-6 flex-wrap">
      {filters.map((filter) => (
        <button
          key={filter.value}
          onClick={() => onFilterChange(filter.value)}
          className={`px-4 sm:px-5 py-2 sm:py-2.5 rounded-xl font-bold text-sm sm:text-base transition-all duration-300 ${
            currentFilter === filter.value
              ? 'bg-white text-black shadow-xl scale-105'
              : 'bg-gray-700 text-gray-200 border-2 border-gray-600 hover:bg-gray-600 hover:text-white hover:border-gray-500 hover:scale-105'
          }`}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}
