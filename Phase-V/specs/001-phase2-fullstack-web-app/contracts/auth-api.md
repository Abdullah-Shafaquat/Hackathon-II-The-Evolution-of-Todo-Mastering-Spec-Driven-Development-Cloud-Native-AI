# Authentication API Contract

**Feature**: `001-phase2-fullstack-web-app` | **API**: Authentication Endpoints
**Base URL**: `/api/auth` | **Version**: 1.0.0

## Overview

This contract defines the authentication API endpoints for user registration, login, logout, and session management using JWT tokens with Better Auth.

## Endpoints

### POST /api/auth/signup

Register a new user account.

**Request**:
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"  // Optional
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `email` | string | ✅ Yes | Valid email format (RFC 5322) | User's email address |
| `password` | string | ✅ Yes | Min 8 characters | User's password (will be hashed) |
| `name` | string | ❌ No | Max 100 characters | Display name |

**Success Response (201 Created)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MDk0NzIwMDB9.signature",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJleHAiOjE3MTE5NTYwMDB9.signature",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-30T10:00:00Z"
  }
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT access token (7-day expiry) |
| `refresh_token` | string | JWT refresh token (30-day expiry) |
| `token_type` | string | Always "bearer" |
| `user` | object | User profile data (see UserResponse schema) |

**Error Responses**:

```json
// 400 Bad Request - Invalid email format
{
  "detail": "Invalid email format"
}

// 400 Bad Request - Password too short
{
  "detail": "Password must be at least 8 characters long"
}

// 409 Conflict - Email already registered
{
  "detail": "Email already registered. Please log in or use a different email."
}

// 500 Internal Server Error - Server error
{
  "detail": "Internal server error"
}
```

**Status Codes**:
- `201 Created`: User successfully registered and logged in
- `400 Bad Request`: Validation error (invalid email, password too short)
- `409 Conflict`: Email already exists
- `500 Internal Server Error`: Database or server error

---

### POST /api/auth/login

Authenticate existing user and issue JWT tokens.

**Request**:
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "remember_me": true  // Optional, default false
}
```

**Request Schema**:
| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `email` | string | ✅ Yes | Valid email format | Registered email |
| `password` | string | ✅ Yes | - | User's password |
| `remember_me` | boolean | ❌ No | Default: false | Extend session duration |

**Success Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-30T10:00:00Z"
  }
}
```

**Response Schema**: Same as signup response

**Error Responses**:

```json
// 400 Bad Request - Missing credentials
{
  "detail": "Email and password are required"
}

// 401 Unauthorized - Invalid credentials
{
  "detail": "Invalid email or password"
}

// 500 Internal Server Error
{
  "detail": "Internal server error"
}
```

**Status Codes**:
- `200 OK`: Successfully authenticated
- `400 Bad Request`: Missing email or password
- `401 Unauthorized`: Invalid credentials
- `500 Internal Server Error`: Database or server error

---

### POST /api/auth/logout

Log out user and invalidate JWT tokens.

**Request**:
```http
POST /api/auth/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Authentication**: ✅ Required (JWT token in Authorization header)

**Success Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses**:

```json
// 401 Unauthorized - Missing or invalid token
{
  "detail": "Invalid or expired token"
}
```

**Status Codes**:
- `200 OK`: Successfully logged out
- `401 Unauthorized`: Missing or invalid JWT token

**Note**: For stateless JWT approach, logout is client-side only (delete token from storage). Backend can optionally maintain token blacklist for revoked tokens (Phase III).

---

### GET /api/auth/me

Get current authenticated user profile.

**Request**:
```http
GET /api/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Authentication**: ✅ Required (JWT token in Authorization header)

**Success Response (200 OK)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-12-30T10:00:00Z"
}
```

**Response Schema** (UserResponse):
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | User UUID |
| `email` | string | User email |
| `name` | string \| null | Display name (null if not provided) |
| `created_at` | string | ISO 8601 datetime |

**Error Responses**:

```json
// 401 Unauthorized - Missing or invalid token
{
  "detail": "Invalid or expired token"
}

// 404 Not Found - User not found (edge case)
{
  "detail": "User not found"
}
```

**Status Codes**:
- `200 OK`: User profile retrieved successfully
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: User no longer exists (rare edge case)

---

## Authentication Flow

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Frontend   │         │  Backend    │         │  Database   │
└─────────────┘         └─────────────┘         └─────────────┘
      │                       │                       │
      │ POST /auth/signup     │                       │
      │──────────────────────>│                       │
      │                       │ INSERT user           │
      │                       │──────────────────────>│
      │                       │<──────────────────────│
      │                       │ Generate JWT          │
      │<──────────────────────│                       │
      │ Store token           │                       │
      │ (localStorage/cookie) │                       │
      │                       │                       │
      │ POST /tasks (with JWT)│                       │
      │──────────────────────>│                       │
      │                       │ Verify JWT            │
      │                       │ Extract user_id       │
      │                       │ SELECT tasks          │
      │                       │──────────────────────>│
      │                       │<──────────────────────│
      │<──────────────────────│                       │
      │                       │                       │
      │ POST /auth/logout     │                       │
      │──────────────────────>│                       │
      │ Delete token          │                       │
      │<──────────────────────│                       │
```

## JWT Token Structure

### Access Token (7-day expiry)

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",  // User ID
  "email": "user@example.com",                     // User email
  "iat": 1704011400,                               // Issued at (Unix timestamp)
  "exp": 1704616200                                // Expires at (7 days later)
}
```

### Refresh Token (30-day expiry)

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",  // User ID
  "type": "refresh",                               // Token type
  "iat": 1704011400,                               // Issued at
  "exp": 1706603400                                // Expires at (30 days later)
}
```

## Security Considerations

### Password Storage
- Passwords MUST be hashed using bcrypt (handled by Better Auth)
- Password hashes MUST NEVER be returned in API responses
- Minimum password length: 8 characters

### Token Management
- Access tokens expire after 7 days
- Refresh tokens expire after 30 days
- Tokens MUST be transmitted over HTTPS only in production
- Frontend SHOULD store tokens in httpOnly cookies for security (or localStorage for simplicity)

### CORS
- Backend MUST allow only frontend domain in CORS configuration
- `Access-Control-Allow-Origin` MUST match `FRONTEND_URL` environment variable
- `Access-Control-Allow-Credentials: true` required for auth headers

### Rate Limiting
- Login endpoint: 5 requests per minute per IP
- Signup endpoint: 3 requests per minute per IP
- Prevents brute force attacks

## Error Response Format

All authentication endpoints follow consistent error format:

```typescript
interface APIError {
  detail: string | Array<{field: string, message: string}>
}
```

**Single Error**:
```json
{
  "detail": "Invalid email or password"
}
```

**Validation Errors**:
```json
{
  "detail": [
    {"field": "email", "message": "Invalid email format"},
    {"field": "password", "message": "Password too short"}
  ]
}
```

## Frontend Integration

### API Client Example

```typescript
import { AuthResponse, LoginRequest, SignupRequest } from '@/lib/types';

class AuthAPI {
  private baseURL = process.env.NEXT_PUBLIC_API_URL;

  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await fetch(`${this.baseURL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(`${this.baseURL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return response.json();
  }

  async logout(token: string): Promise<void> {
    await fetch(`${this.baseURL}/api/auth/logout`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
  }

  async getCurrentUser(token: string): Promise<User> {
    const response = await fetch(`${this.baseURL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) {
      throw new Error('Failed to get user');
    }

    return response.json();
  }
}

export const authAPI = new AuthAPI();
```

## Testing

### Signup Test Cases

1. ✅ Valid signup with all fields → 201 with tokens
2. ✅ Valid signup without name → 201 with tokens, name=null
3. ❌ Invalid email format → 400 validation error
4. ❌ Password too short (<8 chars) → 400 validation error
5. ❌ Duplicate email → 409 conflict error
6. ❌ Missing required fields → 400 validation error

### Login Test Cases

1. ✅ Valid credentials → 200 with tokens
2. ✅ Valid credentials with remember_me → 200 with extended tokens
3. ❌ Invalid email → 401 unauthorized
4. ❌ Invalid password → 401 unauthorized
5. ❌ Non-existent user → 401 unauthorized
6. ❌ Missing credentials → 400 validation error

### Logout Test Cases

1. ✅ Valid token → 200 success
2. ❌ Missing token → 401 unauthorized
3. ❌ Invalid token → 401 unauthorized
4. ❌ Expired token → 401 unauthorized

### Get Current User Test Cases

1. ✅ Valid token → 200 with user data
2. ❌ Missing token → 401 unauthorized
3. ❌ Invalid token → 401 unauthorized
4. ❌ Expired token → 401 unauthorized

---

**Contract Status**: ✅ FINAL
**Last Updated**: 2025-12-30
**Version**: 1.0.0
