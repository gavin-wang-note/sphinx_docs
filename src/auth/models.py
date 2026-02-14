"""Data models for the authentication module.

This module defines the data models used by the authentication system,
including User and Token models.
"""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class User:
    """User data model.
    
    Attributes:
        id: The unique identifier for the user.
        username: The user's username.
        email: The user's email address.
        role: The user's role (admin, user, etc.).
        is_active: Whether the user account is active.
        last_login: The date and time of the user's last login.
    """
    id: int
    username: str
    email: str
    role: str
    is_active: bool = True
    last_login: Optional[str] = None


@dataclass
class Token:
    """Token data model.
    
    Attributes:
        id: The unique identifier for the token.
        user_id: The ID of the user associated with the token.
        token: The token string.
        expires_at: The date and time when the token expires.
        created_at: The date and time when the token was created.
        is_revoked: Whether the token has been revoked.
    """
    id: int
    user_id: int
    token: str
    expires_at: str
    created_at: str
    is_revoked: bool = False


@dataclass
class Permission:
    """Permission data model.
    
    Attributes:
        id: The unique identifier for the permission.
        name: The name of the permission.
        description: A description of the permission.
    """
    id: int
    name: str
    description: str


@dataclass
class Role:
    """Role data model.
    
    Attributes:
        id: The unique identifier for the role.
        name: The name of the role.
        description: A description of the role.
        permissions: A list of permissions associated with the role.
    """
    id: int
    name: str
    description: str
    permissions: List[Permission] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []
