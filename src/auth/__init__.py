"""Authentication module for Sphinx Documentation.

This module provides authentication functionality for the Sphinx Documentation system,
including user authentication, token management, and permission checks.
"""

__version__ = '1.0.0'
__all__ = ['authenticate', 'generate_token', 'verify_token', 'PermissionError']

from .core import authenticate, generate_token, verify_token
from .exceptions import PermissionError
