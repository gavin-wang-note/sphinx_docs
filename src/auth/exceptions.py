"""Exception classes for the authentication module.

This module defines custom exception classes used by the authentication system.
"""


class AuthenticationError(Exception):
    """Base exception class for authentication errors.
    
    This exception is raised when there's an error during the authentication process.
    """
    
    def __init__(self, message: str, code: int = 401):
        """Initialize the authentication error.
        
        Args:
            message: The error message.
            code: The HTTP status code associated with the error.
        """
        super().__init__(message)
        self.message = message
        self.code = code


class PermissionError(AuthenticationError):
    """Exception raised when a user doesn't have the required permissions.
    
    This exception is raised when a user tries to access a resource or perform an action
    for which they don't have the necessary permissions.
    """
    
    def __init__(self, message: str = "Insufficient permissions", code: int = 403):
        """Initialize the permission error.
        
        Args:
            message: The error message.
            code: The HTTP status code associated with the error.
        """
        super().__init__(message, code)


class TokenError(AuthenticationError):
    """Exception raised when there's an error with a token.
    
    This exception is raised when a token is invalid, expired, or otherwise invalid.
    """
    
    def __init__(self, message: str = "Invalid token", code: int = 401):
        """Initialize the token error.
        
        Args:
            message: The error message.
            code: The HTTP status code associated with the error.
        """
        super().__init__(message, code)


class UserNotFoundError(AuthenticationError):
    """Exception raised when a user is not found.
    
    This exception is raised when an authentication operation tries to access a user
    that doesn't exist in the system.
    """
    
    def __init__(self, message: str = "User not found", code: int = 404):
        """Initialize the user not found error.
        
        Args:
            message: The error message.
            code: The HTTP status code associated with the error.
        """
        super().__init__(message, code)
