'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import type { Task, TaskUpdate } from '@/lib/types';
import { useToast } from '@/components/ui/ToastContainer';
import { formatPakistanTime } from '@/lib/timeUtils';
import WarningModal from '@/components/ui/WarningModal';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: () => void;
  selectionMode?: boolean;
  isSelected?: boolean;
  onToggleSelection?: (id: number) => void;
}

export default function TaskItem({ task, onTaskUpdated, selectionMode, isSelected, onToggleSelection }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [editData, setEditData] = useState<TaskUpdate>({
    title: task.title,
    description: task.description || '',
    due_date: task.due_date || undefined,
    priority: task.priority,
    category: task.category,
  });
  const [loading, setLoading] = useState(false);
  const { success, error } = useToast();

  const handleToggleComplete = async () => {
    setLoading(true);
    try {
      await api.toggleComplete(task.id);
      success(task.completed ? 'Task marked as incomplete' : 'Task marked as complete');
      onTaskUpdated();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Failed to toggle completion');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus: 'pending' | 'in_progress' | 'completed') => {
    setLoading(true);
    try {
      await api.updateTask(task.id, { status: newStatus });
      const statusLabels = {
        pending: 'Pending',
        in_progress: 'In Progress',
        completed: 'Completed'
      };
      success(`Task status changed to ${statusLabels[newStatus]}`);
      onTaskUpdated();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Failed to update task status');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = async () => {
    setLoading(true);
    try {
      await api.updateTask(task.id, editData);
      setIsEditing(false);
      success('Task updated successfully');
      onTaskUpdated();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    try {
      await api.deleteTask(task.id);
      success('Task deleted successfully');
      onTaskUpdated();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Failed to delete task');
    } finally {
      setLoading(false);
    }
  };

  if (isEditing) {
    return (
      <div className="card bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700 p-6 sm:p-8 animate-slide-up">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/30">
              <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </div>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100">
              Edit Task
            </h3>
          </div>
          <div className="h-1.5 w-24 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">Title</label>
            <input
              type="text"
              value={editData.title}
              onChange={(e) => setEditData({ ...editData, title: e.target.value })}
              className="input w-full"
              maxLength={200}
              placeholder="Enter task title"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              Description <span className="text-slate-400 text-xs font-normal">(Optional)</span>
            </label>
            <textarea
              value={editData.description}
              onChange={(e) => setEditData({ ...editData, description: e.target.value })}
              className="input w-full resize-none"
              rows={4}
              placeholder="Enter task description (optional)"
            />
          </div>

          {/* Due Date Picker */}
          <div>
            <label className="block text-sm font-semibold text-slate-200 mb-2">
              Due Date <span className="text-slate-400 text-xs font-normal">(Optional)</span>
            </label>
            <input
              type="date"
              value={editData.due_date || ''}
              onChange={(e) => setEditData({ ...editData, due_date: e.target.value || undefined })}
              className="input w-full"
              min={new Date().toISOString().split('T')[0]}
            />
          </div>

          {/* Priority and Category */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-slate-200 mb-2">Priority</label>
              <select
                value={editData.priority}
                onChange={(e) => setEditData({ ...editData, priority: e.target.value as any })}
                className="input w-full cursor-pointer"
              >
                <option value="low">🔵 Low Priority</option>
                <option value="medium">🟡 Medium Priority</option>
                <option value="high">🔴 High Priority</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-200 mb-2">Category</label>
              <select
                value={editData.category}
                onChange={(e) => setEditData({ ...editData, category: e.target.value as any })}
                className="input w-full cursor-pointer"
              >
                <option value="personal">👤 Personal</option>
                <option value="work">💼 Work</option>
                <option value="study">📚 Study</option>
                <option value="health">💪 Health</option>
                <option value="shopping">🛒 Shopping</option>
                <option value="other">📌 Other</option>
              </select>
            </div>
          </div>

          <div className="flex gap-4 pt-4">
            <button
              onClick={handleEdit}
              disabled={loading}
              className="btn btn-primary flex-1 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Saving...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Save Changes
                </>
              )}
            </button>
            <button
              onClick={() => setIsEditing(false)}
              disabled={loading}
              className="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Render warning modal for delete confirmation
  if (showDeleteConfirm) {
    return (
      <>
        {/* Show the task card in background */}
        <div className="card group bg-gradient-to-br rounded-2xl p-5 sm:p-6 transition-all duration-300 animate-fade-in from-slate-800 to-slate-900 border-slate-700 hover:border-slate-600 opacity-50">
          {/* Task content (simplified for background) */}
          <div className="flex items-start gap-3 sm:gap-4">
            <div className="flex-1 min-w-0">
              <h3 className="text-base sm:text-lg font-bold text-slate-100 mb-2">
                {task.title}
              </h3>
            </div>
          </div>
        </div>

        {/* Warning Modal */}
        <WarningModal
          isOpen={showDeleteConfirm}
          onClose={() => setShowDeleteConfirm(false)}
          onConfirm={handleDelete}
          title="Delete Task?"
          message="This action cannot be undone. The task will be permanently removed from your list."
          confirmText="Yes, Delete"
          cancelText="Cancel"
          isLoading={loading}
          variant="danger"
        />
      </>
    );
  }

  // Check if task is overdue
  const isOverdue = task.due_date && !task.completed && new Date(task.due_date) < new Date();
  const isDueToday = task.due_date === new Date().toISOString().split('T')[0] && !task.completed;

  return (
    <div className={`card group bg-gradient-to-br rounded-2xl p-5 sm:p-6 transition-all duration-300 animate-fade-in ${
      isOverdue
        ? 'from-red-900/20 to-red-800/20 border-red-500/50 hover:border-red-400 hover:shadow-lg hover:shadow-red-500/20'
        : isDueToday
        ? 'from-purple-900/20 to-purple-800/20 border-purple-500/50 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20'
        : 'from-slate-800 to-slate-900 border-slate-700 hover:border-slate-600'
    }`}>
      <div className="flex items-start gap-3 sm:gap-4">
        {/* Selection Checkbox (only in selection mode) */}
        {selectionMode && (
          <input
            type="checkbox"
            checked={isSelected}
            onChange={() => onToggleSelection?.(task.id)}
            className="mt-1 h-5 w-5 sm:h-6 sm:w-6 bg-slate-700 border-2 border-indigo-500 text-indigo-500 rounded-md focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-900 cursor-pointer transition-all duration-200 hover:scale-110 checked:bg-indigo-600 checked:border-indigo-600"
          />
        )}

        {/* Completion Checkbox (hidden in selection mode) */}
        {!selectionMode && (
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleComplete}
            disabled={loading}
            className="mt-1 h-5 w-5 sm:h-6 sm:w-6 bg-slate-700 border-2 border-slate-500 text-indigo-500 rounded-md focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-900 cursor-pointer disabled:opacity-50 transition-all duration-200 hover:scale-110 checked:bg-indigo-600 checked:border-indigo-600"
          />
        )}

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3 className={`text-base sm:text-lg font-bold break-words mb-2 ${task.completed ? 'line-through text-slate-400' : 'text-slate-100'}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm sm:text-base break-words leading-relaxed ${task.completed ? 'text-slate-500' : 'text-slate-300'}`}>
              {task.description}
            </p>
          )}

          {/* Priority and Category Badges */}
          <div className="flex flex-wrap items-center gap-2 mt-3">
            {/* Priority Badge */}
            {task.priority && (
              <span className={`badge ${
                task.priority === 'high' ? 'badge-danger' :
                task.priority === 'medium' ? 'badge-warning' :
                'badge-info'
              }`}>
                {task.priority === 'high' && '🔴'}
                {task.priority === 'medium' && '🟡'}
                {task.priority === 'low' && '🔵'}
                {task.priority.toUpperCase()}
              </span>
            )}

            {/* Category Badge */}
            {task.category && (
              <span className="badge badge-primary">
                {task.category === 'work' && '💼'}
                {task.category === 'personal' && '👤'}
                {task.category === 'study' && '📚'}
                {task.category === 'health' && '💪'}
                {task.category === 'shopping' && '🛒'}
                {task.category === 'other' && '📌'}
                {task.category.charAt(0).toUpperCase() + task.category.slice(1)}
              </span>
            )}

            {/* Due Date Badge */}
            {task.due_date && (
              <span className={`badge ${
                isOverdue ? 'badge-danger' :
                isDueToday ? 'badge-warning' :
                'badge-info'
              }`}>
                📅 {new Date(task.due_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
            )}
          </div>

          {/* Status Toggle Buttons */}
          <div className="flex flex-wrap items-center gap-2 mt-3">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wide">Status:</span>
            <div className="flex gap-1.5">
              <button
                onClick={() => handleStatusChange('pending')}
                disabled={loading || task.status === 'pending'}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 ${
                  task.status === 'pending'
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/50 shadow-sm'
                    : 'bg-slate-700/50 text-slate-400 border border-slate-600 hover:bg-slate-600/50 hover:border-slate-500 hover:text-slate-300'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                ⏸️ Pending
              </button>
              <button
                onClick={() => handleStatusChange('in_progress')}
                disabled={loading || task.status === 'in_progress'}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 ${
                  task.status === 'in_progress'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/50 shadow-sm'
                    : 'bg-slate-700/50 text-slate-400 border border-slate-600 hover:bg-slate-600/50 hover:border-slate-500 hover:text-slate-300'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                🔄 In Progress
              </button>
              <button
                onClick={() => handleStatusChange('completed')}
                disabled={loading || task.status === 'completed'}
                className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 ${
                  task.status === 'completed'
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 shadow-sm'
                    : 'bg-slate-700/50 text-slate-400 border border-slate-600 hover:bg-slate-600/50 hover:border-slate-500 hover:text-slate-300'
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                ✅ Completed
              </button>
            </div>
          </div>

          <div className="flex items-center gap-2 mt-3 sm:mt-4 pt-2 sm:pt-3 border-t border-slate-700/50">
            <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <p className="text-xs sm:text-sm text-slate-300 font-medium">
              {formatPakistanTime(task.created_at)}
            </p>
          </div>
        </div>

        {/* Status Badge */}
        <span
          className={`shrink-0 px-3 sm:px-4 py-1.5 sm:py-2 text-xs font-bold rounded-lg border transition-all duration-200 ${
            task.completed
              ? 'bg-slate-700/50 border-slate-600 text-slate-400'
              : 'bg-indigo-500/20 border-indigo-500/50 text-indigo-300 shadow-sm'
          }`}
        >
          {task.completed ? '✓ Done' : '● Active'}
        </span>

        {/* Action Buttons */}
        <div className="shrink-0 flex gap-1 sm:gap-2">
          <button
            onClick={() => {
              setEditData({
                title: task.title,
                description: task.description || '',
                due_date: task.due_date || undefined,
                priority: task.priority,
                category: task.category,
              });
              setIsEditing(true);
            }}
            className="p-2 sm:p-2.5 text-slate-400 hover:text-indigo-400 hover:bg-slate-700/50 rounded-lg transition-all duration-200 hover:scale-110 opacity-70 group-hover:opacity-100"
            title="Edit task"
          >
            <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>

          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="p-2 sm:p-2.5 text-slate-400 hover:text-red-400 hover:bg-slate-700/50 rounded-lg transition-all duration-200 hover:scale-110 opacity-70 group-hover:opacity-100"
            title="Delete task"
          >
            <svg className="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
