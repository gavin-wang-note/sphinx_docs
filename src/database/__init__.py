"""Database module for Sphinx Documentation.

This module provides database connectivity and ORM functionality for the Sphinx Documentation system.
"""

__version__ = '1.0.0'
__all__ = ['Database', 'Model', 'Field', 'ConnectionError']

from .core import Database, ConnectionError
from .models import Model, Field
