'use client';

import { Task } from '@/lib/types';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
  emptyMessage?: string;
  selectionMode?: boolean;
  selectedTaskIds?: Set<number>;
  onToggleSelection?: (id: number) => void;
}

export default function TaskList({
  tasks,
  onTaskUpdated,
  emptyMessage = 'No tasks yet!',
  selectionMode,
  selectedTaskIds,
  onToggleSelection
}: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-16 animate-fade-in">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl mb-6 border-2 border-gray-700">
          <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <p className="text-xl font-bold text-white mb-2">{emptyMessage}</p>
        <p className="text-sm text-gray-300">Create your first task to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          style={{ animationDelay: `${index * 0.1}s` }}
          className="animate-fade-in"
        >
          <TaskItem
            task={task}
            onTaskUpdated={onTaskUpdated}
            selectionMode={selectionMode}
            isSelected={selectedTaskIds?.has(task.id)}
            onToggleSelection={onToggleSelection}
          />
        </div>
      ))}
    </div>
  );
}
