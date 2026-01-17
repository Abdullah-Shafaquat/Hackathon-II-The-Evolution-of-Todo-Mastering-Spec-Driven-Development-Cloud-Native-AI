/**
 * Browser Notifications Utility
 * Handles browser push notifications for overdue and due tasks
 */

import type { Task } from './types';

/**
 * Request notification permission from the user
 * Should be called once when the app loads
 */
export async function requestNotificationPermission(): Promise<boolean> {
  // Check if notifications are supported
  if (!('Notification' in window)) {
    console.warn('Browser notifications are not supported');
    return false;
  }

  // Check current permission status
  if (Notification.permission === 'granted') {
    return true;
  }

  if (Notification.permission === 'denied') {
    return false;
  }

  // Request permission
  try {
    const permission = await Notification.requestPermission();
    return permission === 'granted';
  } catch (error) {
    console.error('Error requesting notification permission:', error);
    return false;
  }
}

/**
 * Show notification for overdue tasks
 */
export function showOverdueNotification(tasks: Task[]): void {
  if (!('Notification' in window) || Notification.permission !== 'granted') {
    return;
  }

  if (tasks.length === 0) {
    return;
  }

  const count = tasks.length;
  const title = `${count} Task${count > 1 ? 's' : ''} Overdue!`;

  const taskList = tasks
    .slice(0, 3)
    .map(t => `• ${t.title}`)
    .join('\n');

  const body = count <= 3
    ? `${taskList}`
    : `${taskList}\n...and ${count - 3} more`;

  try {
    const notification = new Notification(title, {
      body,
      icon: '/icon.png', // Add your app icon
      badge: '/badge.png', // Add your app badge
      tag: 'overdue-tasks', // Prevents duplicate notifications
      requireInteraction: true, // Keeps notification visible until user interacts
      vibrate: [200, 100, 200], // Vibration pattern for mobile devices
    });

    // Auto-close after 10 seconds
    setTimeout(() => notification.close(), 10000);

    // Handle notification click - focus the window
    notification.onclick = function() {
      window.focus();
      this.close();
    };
  } catch (error) {
    console.error('Error showing notification:', error);
  }
}

/**
 * Show notification for tasks due today
 */
export function showDueTodayNotification(tasks: Task[]): void {
  if (!('Notification' in window) || Notification.permission !== 'granted') {
    return;
  }

  if (tasks.length === 0) {
    return;
  }

  const count = tasks.length;
  const title = `${count} Task${count > 1 ? 's' : ''} Due Today`;

  const taskList = tasks
    .slice(0, 3)
    .map(t => `• ${t.title}`)
    .join('\n');

  const body = count <= 3
    ? `${taskList}\n\nDon't forget to complete them!`
    : `${taskList}\n...and ${count - 3} more`;

  try {
    const notification = new Notification(title, {
      body,
      icon: '/icon.png',
      badge: '/badge.png',
      tag: 'due-today-tasks',
      vibrate: [200],
    });

    // Auto-close after 8 seconds
    setTimeout(() => notification.close(), 8000);

    // Handle notification click
    notification.onclick = function() {
      window.focus();
      this.close();
    };
  } catch (error) {
    console.error('Error showing notification:', error);
  }
}

/**
 * Check if notifications are enabled
 */
export function areNotificationsEnabled(): boolean {
  return 'Notification' in window && Notification.permission === 'granted';
}

/**
 * Get notification permission status
 */
export function getNotificationStatus(): 'granted' | 'denied' | 'default' | 'unsupported' {
  if (!('Notification' in window)) {
    return 'unsupported';
  }
  return Notification.permission;
}
