"""Core authentication functionality.

This module contains the core authentication logic for the Sphinx Documentation system.
"""

import datetime
import jwt
import hashlib
from typing import Optional, Dict, Any
from dataclasses import dataclass

from .exceptions import AuthenticationError, PermissionError
from .models import User, Token


@dataclass
class AuthResult:
    """Authentication result data class.
    
    Attributes:
        user: The authenticated user.
        token: The JWT token for the user.
        expires_at: The token expiration time.
    """
    user: User
    token: str
    expires_at: datetime.datetime


class AuthManager:
    """Authentication manager for handling authentication operations.
    
    This class provides methods for user authentication, token generation,
    and token verification.
    """
    
    def __init__(self, secret_key: str, token_expiry_hours: int = 24):
        """Initialize the authentication manager.
        
        Args:
            secret_key: The secret key for JWT token generation.
            token_expiry_hours: The token expiration time in hours.
        """
        self.secret_key = secret_key
        self.token_expiry_hours = token_expiry_hours
    
    def authenticate(self, username: str, password: str) -> AuthResult:
        """Authenticate a user with username and password.
        
        Args:
            username: The username for authentication.
            password: The password for authentication.
            
        Returns:
            An AuthResult object containing the authenticated user and token.
            
        Raises:
            AuthenticationError: If authentication fails.
        """
        # In a real implementation, this would check against a database
        if not username or not password:
            raise AuthenticationError("Username and password are required")
        
        # Simulate user lookup
        if username != "admin":
            raise AuthenticationError("User not found")
        
        # Simulate password check
        if not self._verify_password(password, "$2b$12$9XQ2aW3Z4y5V6U7T8S9R0E"):
            raise AuthenticationError("Invalid password")
        
        user = User(id=1, username="admin", email="admin@example.com", role="admin")
        token, expires_at = self.generate_token(user)
        
        return AuthResult(user=user, token=token, expires_at=expires_at)
    
    def generate_token(self, user: User) -> tuple[str, datetime.datetime]:
        """Generate a JWT token for a user.
        
        Args:
            user: The user to generate a token for.
            
        Returns:
            A tuple containing the JWT token and expiration time.
        """
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=self.token_expiry_hours)
        
        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": expires_at,
            "iat": datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        return token, expires_at
    
    def verify_token(self, token: str) -> User:
        """Verify a JWT token and return the associated user.
        
        Args:
            token: The JWT token to verify.
            
        Returns:
            The user associated with the token.
            
        Raises:
            AuthenticationError: If token verification fails.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Simulate user lookup
            return User(
                id=payload["user_id"],
                username=payload["username"],
                email=f"{payload['username']}@example.com",
                role=payload["role"]
            )
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password.
        
        Args:
            password: The plain text password.
            hashed_password: The hashed password.
            
        Returns:
            True if the password matches, False otherwise.
        """
        # In a real implementation, this would use bcrypt or similar
        return hashlib.md5(password.encode()).hexdigest() == hashed_password


# Create a default auth manager instance
_auth_manager = AuthManager(secret_key="your-secret-key-change-me-in-production")


# Expose public functions
def authenticate(username: str, password: str) -> AuthResult:
    """Authenticate a user with username and password.
    
    Args:
        username: The username for authentication.
        password: The password for authentication.
        
    Returns:
        An AuthResult object containing the authenticated user and token.
        
    Raises:
        AuthenticationError: If authentication fails.
    """
    return _auth_manager.authenticate(username, password)


def generate_token(user: User) -> tuple[str, datetime.datetime]:
    """Generate a JWT token for a user.
    
    Args:
        user: The user to generate a token for.
        
    Returns:
        A tuple containing the JWT token and expiration time.
    """
    return _auth_manager.generate_token(user)


def verify_token(token: str) -> User:
    """Verify a JWT token and return the associated user.
    
    Args:
        token: The JWT token to verify.
        
    Returns:
        The user associated with the token.
        
    Raises:
        AuthenticationError: If token verification fails.
    """
    return _auth_manager.verify_token(token)
