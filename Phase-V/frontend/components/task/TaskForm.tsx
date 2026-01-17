'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import type { TaskCreate, TaskPriority, TaskCategory } from '@/lib/types';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import { useToast } from '@/components/ui/ToastContainer';

interface TaskFormProps {
  onTaskCreated: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
    due_date: undefined,
    priority: 'medium',
    category: 'other'
  });
  const [loading, setLoading] = useState(false);
  const { success, error } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.createTask(formData);
      setFormData({
        title: '',
        description: '',
        due_date: undefined,
        priority: 'medium',
        category: 'other'
      });
      success('Task created successfully!');
      onTaskCreated();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="card bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700 p-6 sm:p-8 animate-slide-up"
    >
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/30">
            <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">
            Add New Task
          </h2>
        </div>
        <div className="h-1.5 w-24 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
      </div>

      <div className="space-y-6">
        {/* Title Input */}
        <Input
          label="Title"
          id="title"
          type="text"
          required
          maxLength={200}
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          placeholder="Buy groceries, Finish report..."
          fullWidth
        />

        {/* Description Textarea */}
        <Textarea
          label="Description"
          id="description"
          rows={4}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="Add optional details about your task..."
          helperText="Optional"
          fullWidth
        />

        {/* Due Date Picker */}
        <div>
          <label
            htmlFor="due_date"
            className="block text-sm font-semibold text-slate-200 mb-2"
          >
            Due Date <span className="text-slate-400 text-xs font-normal">(Optional)</span>
          </label>
          <input
            type="date"
            id="due_date"
            value={formData.due_date || ''}
            onChange={(e) => setFormData({ ...formData, due_date: e.target.value || undefined })}
            className="input w-full"
            min={new Date().toISOString().split('T')[0]}
          />
        </div>

        {/* Priority and Category Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Priority Selector */}
          <div>
            <label
              htmlFor="priority"
              className="block text-sm font-semibold text-slate-200 mb-2"
            >
              Priority
            </label>
            <select
              id="priority"
              value={formData.priority}
              onChange={(e) => setFormData({ ...formData, priority: e.target.value as TaskPriority })}
              className="input w-full cursor-pointer"
            >
              <option value="low">🔵 Low Priority</option>
              <option value="medium">🟡 Medium Priority</option>
              <option value="high">🔴 High Priority</option>
            </select>
          </div>

          {/* Category Selector */}
          <div>
            <label
              htmlFor="category"
              className="block text-sm font-semibold text-slate-200 mb-2"
            >
              Category
            </label>
            <select
              id="category"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value as TaskCategory })}
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

        {/* Submit Button */}
        <Button
          type="submit"
          loading={loading}
          fullWidth
          variant="primary"
          className="mt-8"
        >
          <span className="flex items-center justify-center gap-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            <span className="font-semibold">Create Task</span>
          </span>
        </Button>
      </div>
    </form>
  );
}
