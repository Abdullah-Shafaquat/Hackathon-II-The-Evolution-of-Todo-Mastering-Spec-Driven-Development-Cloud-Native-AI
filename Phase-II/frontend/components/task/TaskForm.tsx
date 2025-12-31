'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import type { TaskCreate } from '@/lib/types';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';

interface TaskFormProps {
  onTaskCreated: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await api.createTask(formData);
      setFormData({ title: '', description: '' });
      onTaskCreated();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 sm:p-6 rounded-lg shadow-md">
      <h2 className="text-lg sm:text-xl font-bold mb-4">Add New Task</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        <Input
          label="Title"
          id="title"
          type="text"
          required
          maxLength={200}
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          placeholder="Buy groceries"
          fullWidth
        />

        <Textarea
          label="Description"
          id="description"
          rows={3}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="Milk, eggs, bread..."
          helperText="Optional task details"
          fullWidth
        />

        <Button
          type="submit"
          loading={loading}
          fullWidth
          variant="primary"
        >
          Create Task
        </Button>
      </div>
    </form>
  );
}
