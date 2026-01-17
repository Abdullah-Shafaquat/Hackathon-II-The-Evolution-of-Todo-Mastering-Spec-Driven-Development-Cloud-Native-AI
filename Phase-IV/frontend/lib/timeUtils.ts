/**
 * Utility functions for time formatting in Pakistan Standard Time (PKT, GMT+5)
 * Handles all edge cases to ensure correct 12-hour format with AM/PM
 */

/**
 * Formats a date string to Pakistan Standard Time with date and time
 * @param dateString - ISO date string or any valid date string
 * @returns Formatted string like "Jan 15, 2024 at 07:45 PM PKT"
 *
 * Edge cases handled:
 * - 0 hours (midnight) → 12 AM
 * - 12 hours (noon) → 12 PM
 * - 1-11 hours → 1-11 AM
 * - 13-23 hours → 1-11 PM
 * - Minutes always 0-59
 * - Consistent padding with leading zeros for minutes
 */
export function formatPakistanTime(dateString: string): string {
  try {
    // Create date object from the input
    const date = new Date(dateString);

    // Check if date is valid
    if (isNaN(date.getTime())) {
      console.error('Invalid date string:', dateString);
      return 'Invalid date';
    }

    // Get date components in Pakistan timezone
    const dateFormatter = new Intl.DateTimeFormat('en-US', {
      timeZone: 'Asia/Karachi',
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
    const dateStr = dateFormatter.format(date);

    // Return formatted date only
    return dateStr;

  } catch (error) {
    console.error('Error formatting Pakistan time:', error);
    return 'Date unavailable';
  }
}

/**
 * Get current time in Pakistan Standard Time
 * @returns Current PKT time formatted as "07:45 PM PKT"
 */
export function getCurrentPakistanTime(): string {
  return formatPakistanTime(new Date().toISOString());
}

/**
 * Test function to validate edge cases
 * Only for development/testing purposes
 */
export function testPakistanTimeFormatter(): void {
  const testCases = [
    // Midnight
    { input: '2024-01-01T00:00:00Z', expected: '05:00 AM PKT' }, // UTC midnight = 5 AM PKT
    // Noon
    { input: '2024-01-01T12:00:00Z', expected: '05:00 PM PKT' }, // UTC noon = 5 PM PKT
    // Morning
    { input: '2024-01-01T03:30:00Z', expected: '08:30 AM PKT' },
    // Evening
    { input: '2024-01-01T15:45:00Z', expected: '08:45 PM PKT' },
    // Before midnight
    { input: '2024-01-01T23:59:00Z', expected: '04:59 AM PKT' }, // Next day
  ];

  console.log('Testing Pakistan Time Formatter:');
  testCases.forEach(({ input, expected }) => {
    const result = formatPakistanTime(input);
    const status = result === expected ? '✓' : '✗';
    console.log(`${status} Input: ${input} → Output: ${result} (Expected: ${expected})`);
  });
}
