"""Example module for Sphinx documentation."""

class ExampleClass:
    """Example class to demonstrate API documentation."""
    
    def __init__(self, name: str):
        """Initialize the example class.
        
        Args:
            name: The name of the example.
        """
        self.name = name
    
    def get_name(self) -> str:
        """Get the name of the example.
        
        Returns:
            The name of the example.
        """
        return self.name
    
    def set_name(self, name: str) -> None:
        """Set the name of the example.
        
        Args:
            name: The new name of the example.
        """
        self.name = name

def example_function(a: int, b: int) -> int:
    """Example function to demonstrate API documentation.
    
    Args:
        a: First integer.
        b: Second integer.
    
    Returns:
        The sum of a and b.
    """
    return a + b

def another_function(text: str, repeat: int = 1) -> str:
    """Another example function.
    
    Args:
        text: The text to repeat.
        repeat: Number of times to repeat (default: 1).
    
    Returns:
        The repeated text.
    """
    return text * repeat
