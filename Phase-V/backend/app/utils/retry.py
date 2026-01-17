"""
Retry Utilities
Implements exponential backoff for API calls
"""

import time
import logging
from typing import Callable, Any, TypeVar, Optional
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
):
    """
    Decorator that retries a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        exponential_base: Base for exponential backoff calculation
        max_delay: Maximum delay between retries in seconds
        exceptions: Tuple of exception types to catch and retry

    Returns:
        Decorated function with retry logic

    Example:
        @retry_with_exponential_backoff(
            max_retries=3,
            exceptions=(openai.RateLimitError, openai.APIError)
        )
        def call_openai_api():
            return client.chat.completions.create(...)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            retries = 0
            delay = initial_delay

            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1

                    if retries > max_retries:
                        logger.error(
                            f"Function {func.__name__} failed after {max_retries} retries. "
                            f"Last error: {str(e)}"
                        )
                        raise

                    # Calculate next delay with exponential backoff
                    wait_time = min(delay * (exponential_base ** (retries - 1)), max_delay)

                    logger.warning(
                        f"Function {func.__name__} failed (attempt {retries}/{max_retries}). "
                        f"Retrying in {wait_time:.2f} seconds. Error: {str(e)}"
                    )

                    time.sleep(wait_time)

            # This should never be reached, but for type safety
            raise Exception(f"Unexpected error in retry logic for {func.__name__}")

        return wrapper
    return decorator


def async_retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
):
    """
    Async decorator that retries a coroutine with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        exponential_base: Base for exponential backoff calculation
        max_delay: Maximum delay between retries in seconds
        exceptions: Tuple of exception types to catch and retry

    Returns:
        Decorated async function with retry logic
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio
            retries = 0
            delay = initial_delay

            while retries <= max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1

                    if retries > max_retries:
                        logger.error(
                            f"Async function {func.__name__} failed after {max_retries} retries. "
                            f"Last error: {str(e)}"
                        )
                        raise

                    # Calculate next delay with exponential backoff
                    wait_time = min(delay * (exponential_base ** (retries - 1)), max_delay)

                    logger.warning(
                        f"Async function {func.__name__} failed (attempt {retries}/{max_retries}). "
                        f"Retrying in {wait_time:.2f} seconds. Error: {str(e)}"
                    )

                    await asyncio.sleep(wait_time)

            # This should never be reached, but for type safety
            raise Exception(f"Unexpected error in retry logic for {func.__name__}")

        return wrapper
    return decorator
