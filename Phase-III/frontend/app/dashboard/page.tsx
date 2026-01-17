'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import type { TaskListResponse, TaskCategory } from '@/lib/types';
import TaskForm from '@/components/task/TaskForm';
import TaskList from '@/components/task/TaskList';
import TaskFilters from '@/components/task/TaskFilters';
import TaskSorter from '@/components/task/TaskSorter';
import CategoryFilter from '@/components/task/CategoryFilter';
import DailySummary from '@/components/task/DailySummary';
import Header from '@/components/layout/Header';
import WarningModal from '@/components/ui/WarningModal';
import { requestNotificationPermission, showOverdueNotification, showDueTodayNotification } from '@/lib/notifications';

export default function DashboardPage() {
  const router = useRouter();
  const [taskData, setTaskData] = useState<TaskListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentFilter, setCurrentFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'date' | 'priority' | 'status' | 'recent'>('recent');
  const [selectedCategories, setSelectedCategories] = useState<Set<TaskCategory>>(new Set());
  const [selectedTaskIds, setSelectedTaskIds] = useState<Set<number>>(new Set());
  const [selectionMode, setSelectionMode] = useState(false);
  const [showBulkDeleteModal, setShowBulkDeleteModal] = useState(false);

  const loadTasks = async (filter?: 'all' | 'pending' | 'completed') => {
    try {
      const filterToUse = filter || currentFilter;
      console.log('Loading tasks with filter:', filterToUse);
      const data = await api.listTasks(filterToUse);
      console.log('Tasks loaded:', data);
      setTaskData(data);
      setError('');
    } catch (err) {
      console.error('Error loading tasks:', err);
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filter: 'all' | 'pending' | 'completed') => {
    setCurrentFilter(filter);
    loadTasks(filter);
  };

  // Handler for category filter toggle
  const handleCategoryToggle = (category: TaskCategory | 'all') => {
    if (category === 'all') {
      setSelectedCategories(new Set());
    } else {
      setSelectedCategories(prev => {
        const next = new Set(prev);
        if (next.has(category)) {
          next.delete(category);
        } else {
          next.add(category);
        }
        return next;
      });
    }
  };

  // Handler for task selection toggle
  const handleTaskSelectionToggle = (taskId: number) => {
    setSelectedTaskIds(prev => {
      const next = new Set(prev);
      if (next.has(taskId)) {
        next.delete(taskId);
      } else {
        next.add(taskId);
      }
      return next;
    });
  };

  // Handler for selecting all visible tasks
  const handleSelectAll = () => {
    const allIds = new Set(filteredTasks.map(t => t.id));
    setSelectedTaskIds(allIds);
  };

  // Handler for clearing selection
  const handleClearSelection = () => {
    setSelectedTaskIds(new Set());
    setSelectionMode(false);
  };

  // Handler for bulk complete
  const handleBulkComplete = async () => {
    if (selectedTaskIds.size === 0) return;

    setLoading(true);
    try {
      // Update all selected tasks to completed status
      await Promise.all(
        Array.from(selectedTaskIds).map(id =>
          api.updateTask(id, { status: 'completed', completed: true })
        )
      );

      // Clear selection and reload tasks
      setSelectedTaskIds(new Set());
      setSelectionMode(false);
      await loadTasks();

      // Show success message
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to complete tasks');
    } finally {
      setLoading(false);
    }
  };

  // Handler to show bulk delete confirmation modal
  const handleBulkDelete = () => {
    if (selectedTaskIds.size === 0) return;
    setShowBulkDeleteModal(true);
  };

  // Handler to confirm and execute bulk delete
  const confirmBulkDelete = async () => {
    setLoading(true);
    try {
      // Delete all selected tasks
      await Promise.all(
        Array.from(selectedTaskIds).map(id => api.deleteTask(id))
      );

      // Clear selection and reload tasks
      setSelectedTaskIds(new Set());
      setSelectionMode(false);
      setShowBulkDeleteModal(false);
      await loadTasks();

      // Show success message
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete tasks');
    } finally {
      setLoading(false);
    }
  };

  // Filter and sort tasks
  const filteredTasks = (() => {
    let tasks = taskData?.tasks || [];

    // Filter by search query (including category and priority)
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      tasks = tasks.filter(task =>
        task.title.toLowerCase().includes(query) ||
        (task.description && task.description.toLowerCase().includes(query)) ||
        (task.category && task.category.toLowerCase().includes(query)) ||
        (task.priority && task.priority.toLowerCase().includes(query))
      );
    }

    // Filter by selected categories
    if (selectedCategories.size > 0) {
      tasks = tasks.filter(task => task.category && selectedCategories.has(task.category));
    }

    // Sort tasks
    const sortedTasks = [...tasks].sort((a, b) => {
      // Overdue tasks always first
      const isOverdue = (dueDate: string | null | undefined, completed: boolean) => {
        if (!dueDate || completed) return false;
        return new Date(dueDate) < new Date();
      };

      const aOverdue = isOverdue(a.due_date, a.completed);
      const bOverdue = isOverdue(b.due_date, b.completed);

      if (aOverdue && !bOverdue) return -1;
      if (!aOverdue && bOverdue) return 1;

      // Then by selected sort option
      switch (sortBy) {
        case 'recent':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();

        case 'date':
          if (!a.due_date && !b.due_date) return 0;
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();

        case 'priority':
          const priorityOrder: Record<string, number> = { high: 3, medium: 2, low: 1 };
          const aPriority = a.priority ? priorityOrder[a.priority] || 0 : 0;
          const bPriority = b.priority ? priorityOrder[b.priority] || 0 : 0;
          return bPriority - aPriority;

        case 'status':
          if (a.completed === b.completed) return 0;
          return a.completed ? 1 : -1;

        default:
          return 0;
      }
    });

    return sortedTasks;
  })();

  useEffect(() => {
    // Check authentication
    if (!api.isAuthenticated()) {
      router.push('/login');
      return;
    }

    loadTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router]);

  // Request notification permission and show notifications for overdue/due tasks
  useEffect(() => {
    // Request permission on mount
    requestNotificationPermission();

    // Show notifications when task data is loaded
    if (taskData && taskData.tasks.length > 0) {
      const today = new Date().toISOString().split('T')[0];

      // Check for overdue tasks
      const overdueTasks = taskData.tasks.filter(t =>
        t.due_date && !t.completed && new Date(t.due_date) < new Date(today)
      );

      // Check for tasks due today
      const dueTodayTasks = taskData.tasks.filter(t =>
        t.due_date === today && !t.completed
      );

      // Show notifications (only once per session using sessionStorage)
      if (overdueTasks.length > 0 && !sessionStorage.getItem('overdue-notified')) {
        showOverdueNotification(overdueTasks);
        sessionStorage.setItem('overdue-notified', 'true');
      }

      if (dueTodayTasks.length > 0 && !sessionStorage.getItem('due-today-notified')) {
        showDueTodayNotification(dueTodayTasks);
        sessionStorage.setItem('due-today-notified', 'true');
      }
    }
  }, [taskData]);


  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-center">
          {/* Animated loading spinner */}
          <div className="relative w-20 h-20 mx-auto mb-6">
            <div className="absolute inset-0 border-4 border-slate-700 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-transparent border-t-indigo-500 rounded-full animate-spin"></div>
          </div>

          {/* Loading text with animation */}
          <div className="flex items-center justify-center gap-2">
            <span className="text-slate-100 text-lg font-medium">Loading</span>
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
              <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
              <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="min-h-screen bg-slate-900 animate-fade-in">
        {/* Header */}
        <Header />

        <main className="max-w-7xl lg:max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 lg:py-8">
        {error && (
          <div className="bg-red-900/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-xl mb-6 animate-slide-down">
            {error}
          </div>
        )}

        {/* Enhanced Reminder Banner - Overdue & Due Today */}
        {taskData && (() => {
          const today = new Date().toISOString().split('T')[0];
          const overdueTasks = taskData.tasks.filter(t =>
            t.due_date && !t.completed && new Date(t.due_date) < new Date(today)
          );
          const dueTodayTasks = taskData.tasks.filter(t =>
            t.due_date === today && !t.completed
          );
          const hasReminders = overdueTasks.length > 0 || dueTodayTasks.length > 0;

          if (!hasReminders) return null;

          return (
            <div className={`bg-gradient-to-r ${
              overdueTasks.length > 0
                ? 'from-red-900/30 via-orange-900/30 to-red-900/30 border-red-500/50'
                : 'from-purple-900/30 via-blue-900/30 to-purple-900/30 border-purple-500/50'
            } border-2 rounded-2xl p-4 sm:p-6 mb-6 animate-scale-in shadow-2xl ${
              overdueTasks.length > 0 ? 'shadow-red-500/20' : 'shadow-purple-500/20'
            }`}>
              <div className="flex items-start gap-4">
                <div className={`shrink-0 w-12 h-12 rounded-xl flex items-center justify-center border-2 ${
                  overdueTasks.length > 0
                    ? 'bg-red-500/20 border-red-500/50'
                    : 'bg-purple-500/20 border-purple-500/50'
                }`}>
                  <svg className={`w-6 h-6 ${overdueTasks.length > 0 ? 'text-red-300' : 'text-purple-300'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <h3 className="text-lg sm:text-xl font-bold text-white mb-2 flex items-center gap-2">
                    {overdueTasks.length > 0 && (
                      <span className="text-red-300">⚠️ {overdueTasks.length} Overdue</span>
                    )}
                    {overdueTasks.length > 0 && dueTodayTasks.length > 0 && (
                      <span className="text-gray-400">•</span>
                    )}
                    {dueTodayTasks.length > 0 && (
                      <span className="text-purple-300">📅 {dueTodayTasks.length} Due Today</span>
                    )}
                  </h3>
                  <p className="text-sm sm:text-base text-gray-300 mb-3">
                    {overdueTasks.length > 0 && (
                      <span className="font-bold text-red-300">
                        {overdueTasks.length} task{overdueTasks.length > 1 ? 's are' : ' is'} overdue!
                      </span>
                    )}
                    {overdueTasks.length > 0 && dueTodayTasks.length > 0 && ' '}
                    {dueTodayTasks.length > 0 && (
                      <span>
                        {overdueTasks.length > 0 ? 'Also, ' : ''}
                        <span className="font-bold text-purple-300">{dueTodayTasks.length}</span> task{dueTodayTasks.length > 1 ? 's are' : ' is'} due today.
                      </span>
                    )}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {[...overdueTasks.slice(0, 2), ...dueTodayTasks.slice(0, 3)].slice(0, 3).map(task => {
                      const isOverdue = task.due_date && new Date(task.due_date) < new Date(today);
                      return (
                        <div key={task.id} className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm border ${
                          isOverdue
                            ? 'bg-red-900/50 border-red-700'
                            : 'bg-gray-900/50 border-gray-700'
                        }`}>
                          <span className={`inline-block w-2 h-2 rounded-full ${
                            task.priority === 'high' ? 'bg-red-400' :
                            task.priority === 'medium' ? 'bg-yellow-400' :
                            'bg-blue-400'
                          }`}></span>
                          <span className="text-white font-medium">{task.title.length > 30 ? task.title.substring(0, 30) + '...' : task.title}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          );
        })()}

        {/* Statistics */}
        {taskData && (
          <div className="card bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700 p-5 sm:p-6 rounded-2xl mb-6 animate-scale-in">
            <h2 className="text-lg sm:text-xl font-bold mb-4 sm:mb-5 text-slate-100">Task Statistics</h2>
            <div className="grid grid-cols-3 gap-3 sm:gap-4">
              <div className="bg-gradient-to-br from-slate-700 to-slate-800 p-3 sm:p-4 rounded-xl border border-slate-600 text-center transform hover:scale-105 transition-all duration-200 hover:border-slate-500">
                <div className="text-3xl sm:text-4xl font-black text-slate-100 mb-1">{taskData.total}</div>
                <div className="text-xs sm:text-sm font-semibold text-slate-300">Total</div>
              </div>
              <div className="bg-gradient-to-br from-emerald-700/20 to-emerald-800/20 p-3 sm:p-4 rounded-xl border border-emerald-500/50 text-center transform hover:scale-105 transition-all duration-200 hover:border-emerald-400">
                <div className="text-3xl sm:text-4xl font-black text-emerald-300 mb-1">{taskData.completed}</div>
                <div className="text-xs sm:text-sm font-semibold text-emerald-200">Completed</div>
              </div>
              <div className="bg-gradient-to-br from-blue-700/20 to-blue-800/20 p-3 sm:p-4 rounded-xl border border-blue-500/50 text-center transform hover:scale-105 transition-all duration-200 hover:border-blue-400">
                <div className="text-3xl sm:text-4xl font-black text-blue-300 mb-1">{taskData.pending}</div>
                <div className="text-xs sm:text-sm font-semibold text-blue-200">Pending</div>
              </div>
            </div>
            {taskData.total > 0 && (
              <div className="mt-5 sm:mt-6 animate-fade-in">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-slate-300">Progress</span>
                  <span className="text-sm font-bold text-slate-100">
                    {Math.round((taskData.completed / taskData.total) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden border border-slate-600">
                  <div
                    className="bg-gradient-to-r from-indigo-500 to-indigo-600 h-3 rounded-full transition-all duration-500 ease-out shadow-sm"
                    style={{ width: `${(taskData.completed / taskData.total) * 100}%` }}
                  />
                </div>
              </div>
            )}
          </div>
        )}

        {/* Daily Summary */}
        {taskData && (
          <div className="mb-6 animate-fade-in">
            <DailySummary tasks={taskData.tasks} />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Task Form */}
          <div className="order-2 lg:order-1">
            <TaskForm onTaskCreated={loadTasks} />
          </div>

          {/* Task List */}
          <div className="order-1 lg:order-2 card bg-gradient-to-br from-slate-800 to-slate-900 border-slate-700 p-6 sm:p-8 rounded-2xl animate-fade-in">
            <div className="mb-6">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/30">
                  <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">Your Tasks</h2>
              </div>
              <div className="h-1.5 w-24 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
            </div>

            {/* Search Bar */}
            <div className="mb-4">
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <input
                  type="text"
                  placeholder="Search tasks by title, description, category, or priority..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="input w-full pl-10 pr-10"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery('')}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-200 transition-colors"
                    aria-label="Clear search"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>
              {searchQuery && (
                <p className="mt-2 text-xs text-slate-400">
                  Found {filteredTasks.length} task{filteredTasks.length !== 1 ? 's' : ''} matching "{searchQuery}"
                </p>
              )}
            </div>

            <TaskFilters currentFilter={currentFilter} onFilterChange={handleFilterChange} />

            {/* Sorting and Category Filtering */}
            <div className="mt-6 space-y-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <TaskSorter currentSort={sortBy} onSortChange={setSortBy} />
              </div>
              <CategoryFilter
                selectedCategories={selectedCategories}
                onCategoryToggle={handleCategoryToggle}
              />
            </div>

            {/* Bulk Action Bar */}
            {selectionMode && selectedTaskIds.size > 0 && (
              <div className="mt-6 bg-blue-900/30 border-2 border-blue-500 rounded-xl p-4 sm:p-5 animate-scale-in shadow-lg">
                <div className="flex flex-col gap-4">
                  {/* Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
                        <svg className="w-6 h-6 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <div>
                        <span className="text-white font-bold text-lg block">
                          {selectedTaskIds.size} task{selectedTaskIds.size > 1 ? 's' : ''} selected
                        </span>
                        <span className="text-blue-200 text-sm">
                          Choose an action to perform on selected tasks
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={handleClearSelection}
                      className="text-gray-400 hover:text-white transition-colors"
                      title="Close"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={handleSelectAll}
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-all duration-300 font-semibold text-sm"
                      title="Select all visible tasks"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                      </svg>
                      Select All ({filteredTasks.length})
                    </button>

                    <button
                      onClick={handleBulkComplete}
                      disabled={loading}
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-bold text-sm shadow-lg"
                      title="Mark selected tasks as completed"
                    >
                      {loading ? (
                        <>
                          <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                          Processing...
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                          </svg>
                          Complete
                        </>
                      )}
                    </button>

                    <button
                      onClick={handleBulkDelete}
                      disabled={loading}
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-bold text-sm shadow-lg"
                      title="Delete selected tasks permanently"
                    >
                      {loading ? (
                        <>
                          <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                          </svg>
                          Deleting...
                        </>
                      ) : (
                        <>
                          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                          Delete
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Selection Mode Toggle Button */}
            {!selectionMode && filteredTasks.length > 0 && (
              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => setSelectionMode(true)}
                  className="inline-flex items-center gap-2 px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-300 font-bold text-sm shadow-lg hover:shadow-xl hover:scale-105"
                  title="Enable multi-select mode to perform bulk actions"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                  <span>Select Multiple Tasks</span>
                  <span className="ml-1 px-2 py-0.5 bg-blue-500 rounded text-xs">Bulk Actions</span>
                </button>
              </div>
            )}

            <div className="mt-6">
              <TaskList
                tasks={filteredTasks}
                onTaskUpdated={() => loadTasks()}
                selectionMode={selectionMode}
                selectedTaskIds={selectedTaskIds}
                onToggleSelection={handleTaskSelectionToggle}
                emptyMessage={
                  searchQuery
                    ? `No tasks found matching "${searchQuery}"`
                    : currentFilter === 'all'
                    ? 'No tasks yet!'
                    : `No ${currentFilter} tasks found`
                }
              />
            </div>
          </div>
        </div>
        </main>
      </div>

      {/* Bulk Delete Warning Modal - Outside main container for proper centering */}
      <WarningModal
        isOpen={showBulkDeleteModal}
        onClose={() => setShowBulkDeleteModal(false)}
        onConfirm={confirmBulkDelete}
        title="Delete Multiple Tasks?"
        message={`Are you sure you want to delete ${selectedTaskIds.size} task${selectedTaskIds.size > 1 ? 's' : ''}? This action cannot be undone and all selected tasks will be permanently removed.`}
        confirmText="Yes, Delete All"
        cancelText="Cancel"
        isLoading={loading}
        variant="danger"
      />
    </>
  );
}
