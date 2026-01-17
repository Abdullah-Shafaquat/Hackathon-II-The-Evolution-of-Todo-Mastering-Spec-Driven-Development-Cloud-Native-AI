/**
 * TypeScript Type Definitions
 * Shared interfaces for API requests and responses
 */

// User Types
export interface User {
  id: string;
  email: string;
  name?: string;
  created_at?: string;
}

// Authentication Types
export interface SignupRequest {
  email: string;
  password: string;
  name?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
  remember_me?: boolean;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

// Task Types
export type TaskPriority = 'low' | 'medium' | 'high';
export type TaskCategory = 'personal' | 'work' | 'study' | 'health' | 'shopping' | 'other';
export type TaskStatus = 'pending' | 'in_progress' | 'completed';

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  status?: TaskStatus;
  due_date?: string | null;
  priority?: TaskPriority;
  category?: TaskCategory;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  due_date?: string;
  priority?: TaskPriority;
  category?: TaskCategory;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  status?: TaskStatus;
  due_date?: string | null;
  priority?: TaskPriority;
  category?: TaskCategory;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  completed: number;
  pending: number;
}

// API Error Response
export interface APIError {
  detail: string;
}
