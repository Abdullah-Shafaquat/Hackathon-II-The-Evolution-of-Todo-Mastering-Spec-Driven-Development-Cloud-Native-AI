'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import type { TaskListResponse } from '@/lib/types';
import TaskForm from '@/components/task/TaskForm';
import TaskList from '@/components/task/TaskList';
import TaskFilters from '@/components/task/TaskFilters';

export default function DashboardPage() {
  const router = useRouter();
  const [taskData, setTaskData] = useState<TaskListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState<any>(null);
  const [currentFilter, setCurrentFilter] = useState<'all' | 'pending' | 'completed'>('all');

  const loadTasks = async (filter?: 'all' | 'pending' | 'completed') => {
    try {
      const filterToUse = filter || currentFilter;
      const data = await api.listTasks(filterToUse);
      setTaskData(data);
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filter: 'all' | 'pending' | 'completed') => {
    setCurrentFilter(filter);
    loadTasks(filter);
  };

  useEffect(() => {
    // Check authentication
    if (!api.isAuthenticated()) {
      router.push('/login');
      return;
    }

    setUser(api.getUser());
    loadTasks();
  }, [router]);

  const handleLogout = () => {
    api.logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl lg:max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-gray-900">Dashboard</h1>
              {user && (
                <p className="text-xs sm:text-sm text-gray-600 truncate max-w-[200px] sm:max-w-none">
                  Welcome, {user.name || user.email}
                </p>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="px-3 sm:px-4 h-11 sm:h-10 text-xs sm:text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl lg:max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Statistics */}
        {taskData && (
          <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md mb-4 sm:mb-6">
            <h2 className="text-base sm:text-lg font-semibold mb-3 sm:mb-4">Task Statistics</h2>
            <div className="grid grid-cols-3 gap-2 sm:gap-4">
              <div className="text-center">
                <div className="text-2xl sm:text-3xl font-bold text-gray-900">{taskData.total}</div>
                <div className="text-xs sm:text-sm text-gray-600">Total</div>
              </div>
              <div className="text-center">
                <div className="text-2xl sm:text-3xl font-bold text-green-600">{taskData.completed}</div>
                <div className="text-xs sm:text-sm text-gray-600">Completed</div>
              </div>
              <div className="text-center">
                <div className="text-2xl sm:text-3xl font-bold text-blue-600">{taskData.pending}</div>
                <div className="text-xs sm:text-sm text-gray-600">Pending</div>
              </div>
            </div>
            {taskData.total > 0 && (
              <div className="mt-3 sm:mt-4">
                <div className="text-xs sm:text-sm text-gray-600">
                  {Math.round((taskData.completed / taskData.total) * 100)}% complete
                </div>
                <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(taskData.completed / taskData.total) * 100}%` }}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
          {/* Task Form */}
          <div>
            <TaskForm onTaskCreated={loadTasks} />
          </div>

          {/* Task List */}
          <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md">
            <h2 className="text-lg sm:text-xl font-bold mb-4">Your Tasks</h2>

            <TaskFilters currentFilter={currentFilter} onFilterChange={handleFilterChange} />

            <TaskList
              tasks={taskData?.tasks || []}
              onTaskUpdated={() => loadTasks()}
              emptyMessage={
                currentFilter === 'all'
                  ? 'No tasks yet!'
                  : `No ${currentFilter} tasks found`
              }
            />
          </div>
        </div>
      </main>
    </div>
  );
}
