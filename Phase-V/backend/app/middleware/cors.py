"""
CORS Middleware Configuration
Handles Cross-Origin Resource Sharing for frontend-backend communication
"""

import re
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings


def configure_cors(app):
    """
    Configure CORS middleware for the FastAPI application

    Allows requests from multiple frontend URLs with credentials (cookies, auth headers)
    Required for JWT token-based authentication across different origins

    Supports:
    - Local development (localhost:3000)
    - Production (Vercel)
    - Hugging Face Spaces (*.hf.space)

    Args:
        app: FastAPI application instance
    """
    # Parse allowed origins from comma-separated string
    allowed_origins = [
        origin.strip()
        for origin in settings.ALLOWED_ORIGINS.split(",")
        if origin.strip()
    ]

    # Check if we have wildcard patterns (like *.hf.space)
    has_wildcard = any("*" in origin for origin in allowed_origins)

    if has_wildcard:
        # Use allow_origin_regex for wildcard support
        # Convert patterns to regex
        regex_patterns = []
        exact_origins = []

        for origin in allowed_origins:
            if "*" in origin:
                # Convert wildcard to regex pattern
                pattern = origin.replace(".", r"\.").replace("*", r"[a-zA-Z0-9-]+")
                regex_patterns.append(pattern)
            else:
                exact_origins.append(origin)

        # Combine into single regex
        combined_regex = "|".join([f"^{p}$" for p in regex_patterns])
        if exact_origins:
            exact_pattern = "|".join([f"^{re.escape(o)}$" for o in exact_origins])
            combined_regex = f"{combined_regex}|{exact_pattern}" if combined_regex else exact_pattern

        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=combined_regex,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
