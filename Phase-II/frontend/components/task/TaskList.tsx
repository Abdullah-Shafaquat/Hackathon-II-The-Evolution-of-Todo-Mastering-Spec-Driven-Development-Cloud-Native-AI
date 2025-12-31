'use client';

import { Task } from '@/lib/types';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
  emptyMessage?: string;
}

export default function TaskList({ tasks, onTaskUpdated, emptyMessage = 'No tasks yet!' }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-lg font-medium">{emptyMessage}</p>
        <p className="text-sm mt-2">Create your first task to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onTaskUpdated={onTaskUpdated}
        />
      ))}
    </div>
  );
}
