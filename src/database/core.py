"""Core database functionality.

This module provides the core database connectivity and query functionality for the
Sphinx Documentation system.
"""

import sqlite3
from typing import Optional, Dict, Any, List
from contextlib import contextmanager


class ConnectionError(Exception):
    """Exception raised when there's an error connecting to the database.
    
    This exception is raised when the database connection fails for any reason.
    """
    pass


class QueryError(Exception):
    """Exception raised when there's an error executing a database query.
    
    This exception is raised when a database query fails to execute properly.
    """
    pass


class Database:
    """Database connection and query manager.
    
    This class provides a high-level interface for connecting to a database and
    executing queries.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """Initialize the database connection.
        
        Args:
            db_path: The path to the database file. Defaults to in-memory database.
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> None:
        """Establish a connection to the database.
        
        Raises:
            ConnectionError: If the connection fails.
        """
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {e}")
    
    def disconnect(self) -> None:
        """Close the database connection.
        
        Raises:
            ConnectionError: If there's an error closing the connection.
        """
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except sqlite3.Error as e:
                raise ConnectionError(f"Failed to disconnect from database: {e}")
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions.
        
        Yields:
            The database connection within a transaction.
            
        Raises:
            QueryError: If the transaction fails.
        """
        if not self.connection:
            self.connect()
        
        try:
            yield self.connection
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise QueryError(f"Transaction failed: {e}")
    
    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> sqlite3.Cursor:
        """Execute a SQL query.
        
        Args:
            query: The SQL query to execute.
            params: Optional parameters for the query.
            
        Returns:
            A sqlite3 Cursor object with the query results.
            
        Raises:
            QueryError: If the query execution fails.
        """
        if not self.connection:
            self.connect()
        
        try:
            if params:
                return self.connection.execute(query, params)
            return self.connection.execute(query)
        except sqlite3.Error as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def executemany(self, query: str, params: List[Dict[str, Any]]) -> sqlite3.Cursor:
        """Execute a SQL query multiple times with different parameters.
        
        Args:
            query: The SQL query to execute.
            params: A list of parameter dictionaries.
            
        Returns:
            A sqlite3 Cursor object with the query results.
            
        Raises:
            QueryError: If the query execution fails.
        """
        if not self.connection:
            self.connect()
        
        try:
            return self.connection.executemany(query, params)
        except sqlite3.Error as e:
            raise QueryError(f"Query execution failed: {e}")
    
    def fetchone(self, query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Execute a query and fetch a single row.
        
        Args:
            query: The SQL query to execute.
            params: Optional parameters for the query.
            
        Returns:
            A dictionary representing the fetched row, or None if no row was found.
        """
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetchall(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a query and fetch all rows.
        
        Args:
            query: The SQL query to execute.
            params: Optional parameters for the query.
            
        Returns:
            A list of dictionaries representing the fetched rows.
        """
        cursor = self.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """Create a new table in the database.
        
        Args:
            table_name: The name of the table to create.
            columns: A dictionary where keys are column names and values are SQL column definitions.
            
        Raises:
            QueryError: If the table creation fails.
        """
        columns_sql = ", ".join([f"{name} {definition}" for name, definition in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
        self.execute(query)


# Create a default database instance
_default_db = Database("./sphinx.db")


# Expose public functions
def get_db() -> Database:
    """Get the default database instance.
    
    Returns:
        The default Database instance.
    """
    return _default_db


def connect() -> None:
    """Connect to the default database.
    
    Raises:
        ConnectionError: If the connection fails.
    """
    _default_db.connect()


def disconnect() -> None:
    """Disconnect from the default database.
    
    Raises:
        ConnectionError: If the disconnection fails.
    """
    _default_db.disconnect()


def execute(query: str, params: Optional[Dict[str, Any]] = None) -> sqlite3.Cursor:
    """Execute a query on the default database.
    
    Args:
        query: The SQL query to execute.
        params: Optional parameters for the query.
        
    Returns:
        A sqlite3 Cursor object with the query results.
    """
    return _default_db.execute(query, params)


def fetchone(query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Fetch a single row from the default database.
    
    Args:
        query: The SQL query to execute.
        params: Optional parameters for the query.
        
    Returns:
        A dictionary representing the fetched row, or None if no row was found.
    """
    return _default_db.fetchone(query, params)


def fetchall(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Fetch all rows from the default database.
    
    Args:
        query: The SQL query to execute.
        params: Optional parameters for the query.
        
    Returns:
        A list of dictionaries representing the fetched rows.
    """
    return _default_db.fetchall(query, params)
