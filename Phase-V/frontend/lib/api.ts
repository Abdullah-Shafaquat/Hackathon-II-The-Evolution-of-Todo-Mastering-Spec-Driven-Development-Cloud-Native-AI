/**
 * API Client
 * Handles all backend API communications with automatic JWT token management
 */

import type {
  SignupRequest,
  LoginRequest,
  AuthResponse,
  TaskCreate,
  TaskUpdate,
  Task,
  TaskListResponse,
  APIError
} from './types';

import type {
  ChatRequest,
  ChatResponse,
  Conversation,
  Message
} from './types/chat';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * API Client Class
 * Manages authentication tokens and API requests
 */
class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Get stored access token from localStorage
   */
  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  /**
   * Store authentication tokens in localStorage
   */
  private setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  /**
   * Clear authentication tokens from localStorage
   */
  private clearTokens(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  /**
   * Make authenticated API request
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error: APIError = await response.json().catch(() => ({
        detail: 'An error occurred'
      }));
      throw new Error(error.detail);
    }

    return response.json();
  }

  // Authentication Methods

  /**
   * Register a new user account
   */
  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    this.setTokens(response.access_token, response.refresh_token);
    if (typeof window !== 'undefined') {
      localStorage.setItem('user', JSON.stringify(response.user));
    }

    return response;
  }

  /**
   * Login with email and password
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });

    this.setTokens(response.access_token, response.refresh_token);
    if (typeof window !== 'undefined') {
      localStorage.setItem('user', JSON.stringify(response.user));
    }

    return response;
  }

  /**
   * Logout and clear tokens
   */
  logout(): void {
    this.clearTokens();
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }

  /**
   * Get stored user data
   */
  getUser() {
    if (typeof window === 'undefined') return null;
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }

  // Task Methods

  /**
   * Create a new task
   */
  async createTask(data: TaskCreate): Promise<Task> {
    return this.request<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Get all tasks for the authenticated user
   */
  async listTasks(filter?: 'all' | 'pending' | 'completed'): Promise<TaskListResponse> {
    const queryParam = filter ? `?filter=${filter}` : '';
    return this.request<TaskListResponse>(`/api/tasks${queryParam}`);
  }

  /**
   * Get a single task by ID
   */
  async getTask(id: number): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}`);
  }

  /**
   * Update an existing task
   */
  async updateTask(id: number, data: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Toggle task completion status
   */
  async toggleComplete(id: number): Promise<Task> {
    return this.request<Task>(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
    });
  }

  /**
   * Delete a task
   */
  async deleteTask(id: number): Promise<void> {
    await fetch(`${this.baseURL}/api/tasks/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${this.getToken()}`,
      },
    });
  }

  // Chat Methods

  /**
   * Send a chat message to the AI assistant
   * Creates a new conversation if conversation_id not provided
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const user = this.getUser();
    if (!user) {
      throw new Error('User not authenticated');
    }

    return this.request<ChatResponse>(`/api/${user.id}/chat`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get all conversations for the authenticated user
   */
  async getConversations(limit: number = 20, offset: number = 0): Promise<{
    conversations: Conversation[];
    total: number;
    limit: number;
    offset: number;
  }> {
    const user = this.getUser();
    if (!user) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/${user.id}/conversations?limit=${limit}&offset=${offset}`);
  }

  /**
   * Get conversation history with all messages
   */
  async getConversationHistory(conversationId: string): Promise<{
    conversation: Conversation;
    messages: Message[];
  }> {
    const user = this.getUser();
    if (!user) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/${user.id}/conversations/${conversationId}`);
  }

  /**
   * Delete a conversation and all its messages
   */
  async deleteConversation(conversationId: string): Promise<void> {
    const user = this.getUser();
    if (!user) {
      throw new Error('User not authenticated');
    }

    const response = await fetch(`${this.baseURL}/api/${user.id}/conversations/${conversationId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${this.getToken()}`,
      },
    });

    if (!response.ok && response.status !== 204) {
      const error: APIError = await response.json().catch(() => ({
        detail: 'Failed to delete conversation'
      }));
      throw new Error(error.detail);
    }
  }
}

// Export singleton instance
export const api = new APIClient();
export default api;
