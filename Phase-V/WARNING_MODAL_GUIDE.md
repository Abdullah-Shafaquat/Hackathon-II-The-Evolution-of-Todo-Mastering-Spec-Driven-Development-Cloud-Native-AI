# Warning Modal Component - Documentation

## Overview
A reusable warning modal component for critical actions that require user confirmation. The modal appears centered on the screen with a dimmed backdrop, ensuring users cannot accidentally perform dangerous actions.

---

## Features

### ✅ User Experience
- **Centered Display**: Modal appears in the center of the screen
- **Dimmed Background**: Semi-transparent black backdrop with blur effect
- **Clear Visual Hierarchy**: Warning icon, title, message, and action buttons
- **Prevents Accidents**: Requires explicit confirmation before proceeding
- **Smooth Animations**: Fade-in and scale-in effects for professional feel
- **Keyboard Support**: ESC key closes the modal (when not loading)
- **Backdrop Click**: Clicking outside closes the modal (when not loading)

### ✅ Visual Design
- **Warning Icon**: Pulsing triangle warning icon at the top
- **Color Variants**:
  - `danger` (red) - For destructive actions like delete
  - `warning` (orange) - For cautionary actions
- **Responsive**: Works perfectly on mobile and desktop
- **Consistent Styling**: Matches the app's overall design language
- **Bottom Accent**: Colored gradient bar at the bottom for emphasis

### ✅ Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Focus Management**: Traps focus within modal
- **Screen Reader Friendly**: Proper semantic HTML
- **Loading States**: Prevents multiple submissions
- **Body Scroll Lock**: Prevents background scrolling

---

## Component API

### Props

```typescript
interface WarningModalProps {
  isOpen: boolean;           // Controls modal visibility
  onClose: () => void;       // Called when user cancels
  onConfirm: () => void;     // Called when user confirms
  title: string;             // Modal title (e.g., "Delete Task?")
  message: string;           // Warning message to display
  confirmText?: string;      // Confirm button text (default: "Confirm")
  cancelText?: string;       // Cancel button text (default: "Cancel")
  isLoading?: boolean;       // Shows loading state (default: false)
  variant?: 'danger' | 'warning'; // Color scheme (default: 'danger')
}
```

---

## Usage Examples

### Example 1: Single Task Delete
```tsx
import WarningModal from '@/components/ui/WarningModal';

function TaskItem({ task }) {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleDelete = async () => {
    setLoading(true);
    try {
      await api.deleteTask(task.id);
      // Handle success
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
      setShowDeleteModal(false);
    }
  };

  return (
    <>
      <button onClick={() => setShowDeleteModal(true)}>
        Delete Task
      </button>

      <WarningModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
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
```

### Example 2: Bulk Delete
```tsx
<WarningModal
  isOpen={showBulkDeleteModal}
  onClose={() => setShowBulkDeleteModal(false)}
  onConfirm={confirmBulkDelete}
  title="Delete Multiple Tasks?"
  message={`Are you sure you want to delete ${count} tasks? This action cannot be undone.`}
  confirmText="Yes, Delete All"
  cancelText="Cancel"
  isLoading={loading}
  variant="danger"
/>
```

### Example 3: Data Loss Warning
```tsx
<WarningModal
  isOpen={showWarning}
  onClose={() => setShowWarning(false)}
  onConfirm={handleDiscard}
  title="Unsaved Changes"
  message="You have unsaved changes. Are you sure you want to leave? All changes will be lost."
  confirmText="Discard Changes"
  cancelText="Keep Editing"
  variant="warning"
/>
```

### Example 4: Account Action
```tsx
<WarningModal
  isOpen={showLogoutModal}
  onClose={() => setShowLogoutModal(false)}
  onConfirm={handleLogout}
  title="Confirm Logout"
  message="Are you sure you want to logout? You will need to sign in again to access your tasks."
  confirmText="Yes, Logout"
  cancelText="Stay Logged In"
  variant="warning"
/>
```

---

## Current Implementations

### 1. TaskItem Component
**Location**: `frontend/components/task/TaskItem.tsx`

**Use Case**: Single task deletion

**Implementation**:
- Shows modal when user clicks delete button
- Displays task title in background (dimmed)
- Confirms before permanently deleting task

### 2. Dashboard Bulk Actions
**Location**: `frontend/app/dashboard/page.tsx`

**Use Case**: Bulk task deletion

**Implementation**:
- Shows modal when user clicks "Delete" in bulk action bar
- Displays number of selected tasks
- Confirms before deleting multiple tasks at once

---

## Design Specifications

### Colors

**Danger Variant (Red):**
- Icon: `text-red-400`
- Icon Background: `bg-red-500/20`
- Icon Border: `border-red-500/30`
- Button: `bg-red-600` → `hover:bg-red-700`
- Title: `text-red-300`
- Bottom Accent: Red gradient

**Warning Variant (Orange):**
- Icon: `text-orange-400`
- Icon Background: `bg-orange-500/20`
- Icon Border: `border-orange-500/30`
- Button: `bg-orange-600` → `hover:bg-orange-700`
- Title: `text-orange-300`
- Bottom Accent: Orange gradient

### Layout

```
┌─────────────────────────────────────┐
│         [Warning Icon]              │  ← Pulsing triangle
│                                     │
│       Warning Title Text            │  ← Colored based on variant
│                                     │
│   This is the warning message that  │  ← Gray text
│   explains what will happen...      │
│                                     │
│  [Cancel Button] [Confirm Button]  │  ← Two clear actions
│                                     │
│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│  ← Colored accent bar
└─────────────────────────────────────┘
```

### Responsive Behavior

**Mobile (<640px):**
- Buttons stack vertically
- Smaller padding
- Full width container
- Touch-friendly button sizes

**Desktop (≥640px):**
- Buttons side by side
- Larger padding
- Max width: 28rem (448px)
- Hover effects enabled

---

## Animations

### Entry Animation
- **Backdrop**: Fades in (opacity 0 → 1)
- **Modal**: Scales in from 95% to 100% + fade in
- **Duration**: ~200-300ms
- **Easing**: Cubic bezier for smooth motion

### Loading State
- **Spinner**: Rotating animation
- **Button**: Disabled with reduced opacity
- **Text**: Changes to "Processing..." or similar

### Exit Animation
- **Backdrop**: Fades out
- **Modal**: Scales out (implicit via React removal)

---

## Best Practices

### When to Use
✅ **Use for:**
- Destructive actions (delete, remove, clear)
- Data loss scenarios (discard changes, reset)
- Critical account actions (logout, delete account)
- Actions that cannot be undone
- Bulk operations affecting multiple items

❌ **Don't use for:**
- Simple confirmations (use toast instead)
- Non-critical actions
- Actions that can be easily undone
- Informational messages (use alerts)

### Writing Good Messages

**Good Examples:**
- "This action cannot be undone. The task will be permanently removed."
- "You have unsaved changes. All changes will be lost if you continue."
- "Deleting 5 tasks will permanently remove them from your list."

**Bad Examples:**
- "Are you sure?" (too vague)
- "Click yes to continue" (explains button, not consequence)
- "This is a warning" (states obvious, doesn't explain)

### Button Labels

**Good Examples:**
- "Yes, Delete" / "Cancel"
- "Discard Changes" / "Keep Editing"
- "Yes, Delete All" / "Cancel"

**Bad Examples:**
- "OK" / "Cancel" (OK is vague)
- "Yes" / "No" (doesn't describe action)
- "Confirm" / "Deny" (too formal)

---

## Technical Details

### Dependencies
- React hooks: `useState`, `useEffect`
- No external libraries required
- Uses Tailwind CSS for styling

### Performance
- Lightweight component (~5KB)
- No heavy animations
- Prevents body scroll leak
- Proper cleanup on unmount

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Requires JavaScript enabled

---

## Future Enhancements

Possible improvements for future versions:

1. **Custom Icons**: Allow passing custom icon component
2. **Sound Effects**: Optional sound for critical warnings
3. **Auto-close**: Optional timeout for less critical warnings
4. **Multiple Buttons**: Support for 3+ action buttons
5. **Checkboxes**: "Don't show this again" option
6. **Themes**: Support for dark/light theme variants
7. **Animation Options**: Allow customizing animation styles

---

## Testing Checklist

When implementing the warning modal, test:

- [ ] Modal opens correctly
- [ ] Backdrop dims the background
- [ ] Warning icon displays with correct color
- [ ] Title and message are readable
- [ ] Buttons are correctly labeled
- [ ] Cancel button closes modal
- [ ] Confirm button executes action
- [ ] Loading state works correctly
- [ ] ESC key closes modal (when not loading)
- [ ] Clicking backdrop closes modal (when not loading)
- [ ] Body scroll is locked when open
- [ ] Mobile view looks correct
- [ ] Desktop view looks correct
- [ ] Animations are smooth
- [ ] Multiple modals don't conflict

---

## Summary

The WarningModal component provides a **consistent, user-friendly way to confirm critical actions** throughout the application. It:

✅ **Prevents accidental actions** with clear confirmation
✅ **Looks professional** with smooth animations
✅ **Works everywhere** with responsive design
✅ **Stays consistent** with app design language
✅ **Easy to use** with simple API
✅ **Accessible** with keyboard and screen reader support

Use this component whenever users need to confirm potentially dangerous or irreversible actions!
