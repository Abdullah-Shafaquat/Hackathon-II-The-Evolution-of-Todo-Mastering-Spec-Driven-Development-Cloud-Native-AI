"""
Rate Limiting Middleware
Implements per-user rate limiting for API endpoints
"""

from fastapi import HTTPException, status, Request
from typing import Dict, Callable
from datetime import datetime, timedelta
from collections import defaultdict
import time


class RateLimiter:
    """
    Simple in-memory rate limiter using sliding window algorithm.

    For production, consider using Redis for distributed rate limiting.
    """

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Store: user_id -> list of request timestamps
        self.requests: Dict[str, list[float]] = defaultdict(list)

    def _cleanup_old_requests(self, user_id: str, current_time: float):
        """Remove requests outside the current time window."""
        cutoff_time = current_time - self.window_seconds
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if timestamp > cutoff_time
        ]

    def check_rate_limit(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit.

        Args:
            user_id: User identifier

        Returns:
            True if request allowed, False if rate limit exceeded
        """
        current_time = time.time()

        # Clean up old requests
        self._cleanup_old_requests(user_id, current_time)

        # Check if under limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False

        # Record this request
        self.requests[user_id].append(current_time)
        return True

    def get_retry_after(self, user_id: str) -> int:
        """
        Get seconds until rate limit resets.

        Args:
            user_id: User identifier

        Returns:
            Seconds to wait before retrying
        """
        if not self.requests[user_id]:
            return 0

        current_time = time.time()
        oldest_request = min(self.requests[user_id])
        reset_time = oldest_request + self.window_seconds

        retry_after = max(0, int(reset_time - current_time))
        return retry_after


# Global rate limiter instance (30 requests per minute per user)
chat_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)


def rate_limit_check(user_id: str) -> None:
    """
    Check rate limit and raise HTTPException if exceeded.

    Args:
        user_id: User identifier to check

    Raises:
        HTTPException 429: Too many requests (rate limit exceeded)
    """
    if not chat_rate_limiter.check_rate_limit(user_id):
        retry_after = chat_rate_limiter.get_retry_after(user_id)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Please try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)}
        )
