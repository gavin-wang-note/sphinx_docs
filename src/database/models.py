"""Database models for the Sphinx Documentation system.

This module defines the ORM (Object-Relational Mapping) functionality for the
Sphinx Documentation system.
"""

from typing import Any, Optional, Dict, List
from dataclasses import dataclass

from .core import Database, fetchone, fetchall, execute, QueryError


class Field:
    """Database field definition.
    
    This class defines a database field with its type and constraints.
    """
    
    def __init__(self, field_type: str, primary_key: bool = False, nullable: bool = True, 
                 default: Optional[Any] = None, unique: bool = False):
        """Initialize a database field.
        
        Args:
            field_type: The SQL data type of the field.
            primary_key: Whether the field is a primary key.
            nullable: Whether the field can be null.
            default: The default value for the field.
            unique: Whether the field value must be unique.
        """
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.unique = unique
    
    def to_sql(self, name: str) -> str:
        """Convert the field definition to SQL.
        
        Args:
            name: The name of the field.
            
        Returns:
            A SQL string defining the field.
        """
        sql_parts = [name, self.field_type]
        
        if self.primary_key:
            sql_parts.append("PRIMARY KEY")
        
        if not self.nullable:
            sql_parts.append("NOT NULL")
        
        if self.default is not None:
            if isinstance(self.default, str):
                sql_parts.append(f"DEFAULT '{self.default}'")
            else:
                sql_parts.append(f"DEFAULT {self.default}")
        
        if self.unique:
            sql_parts.append("UNIQUE")
        
        return " ".join(sql_parts)


class ModelMetaclass(type):
    """Metaclass for Model classes.
    
    This metaclass processes field definitions and creates table information.
    """
    
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)
        
        # Extract fields from attributes
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
        
        # Remove fields from attrs
        for field_name in fields:
            del attrs[field_name]
        
        # Set table name (lowercase class name by default)
        table_name = attrs.get("__tablename__", name.lower())
        attrs["__tablename__"] = table_name
        attrs["__fields__"] = fields
        
        return super().__new__(cls, name, bases, attrs)


class Model(metaclass=ModelMetaclass):
    """Base class for database models.
    
    This class provides the basic ORM functionality for database models.
    """
    
    __tablename__: str
    __fields__: Dict[str, Field]
    
    def __init__(self, **kwargs):
        """Initialize a model instance with field values.
        
        Args:
            kwargs: Field values for the model.
        """
        for field_name in self.__fields__:
            setattr(self, field_name, kwargs.get(field_name))
    
    def __repr__(self):
        """Return a string representation of the model instance.
        
        Returns:
            A string representation of the model instance.
        """
        field_reprs = [f"{field}={getattr(self, field)}" for field in self.__fields__]
        return f"{self.__class__.__name__}({', '.join(field_reprs)})"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model instance to a dictionary.
        
        Returns:
            A dictionary containing the model's field values.
        """
        return {field: getattr(self, field) for field in self.__fields__}
    
    @classmethod
    def create_table(cls, db: Optional[Database] = None) -> None:
        """Create the database table for the model.
        
        Args:
            db: Optional Database instance. If not provided, uses the default.
        """
        columns = {name: field.to_sql(name) for name, field in cls.__fields__.items()}
        if db:
            db.create_table(cls.__tablename__, columns)
        else:
            from .core import get_db
            get_db().create_table(cls.__tablename__, columns)
    
    @classmethod
    def find(cls, id: Any) -> Optional["Model"]:
        """Find a model instance by its primary key.
        
        Args:
            id: The primary key value.
            
        Returns:
            A model instance if found, None otherwise.
        """
        # Find primary key field
        primary_key = None
        for name, field in cls.__fields__.items():
            if field.primary_key:
                primary_key = name
                break
        
        if not primary_key:
            raise QueryError("No primary key defined for model")
        
        query = f"SELECT * FROM {cls.__tablename__} WHERE {primary_key} = ?"
        result = fetchone(query, (id,))
        
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def find_all(cls, limit: Optional[int] = None, offset: Optional[int] = None) -> List["Model"]:
        """Find all model instances.
        
        Args:
            limit: Optional limit on the number of results.
            offset: Optional offset for pagination.
            
        Returns:
            A list of model instances.
        """
        query = f"SELECT * FROM {cls.__tablename__}"
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"
        
        results = fetchall(query)
        return [cls(**result) for result in results]
    
    def save(self) -> None:
        """Save the model instance to the database.
        
        If the instance already exists (has a primary key value), it updates the record.
        Otherwise, it creates a new record.
        """
        # Check if this is an existing record
        primary_key = None
        primary_key_value = None
        for name, field in self.__fields__.items():
            if field.primary_key:
                primary_key = name
                primary_key_value = getattr(self, name)
                break
        
        if primary_key and primary_key_value is not None:
            # Update existing record
            self._update()
        else:
            # Create new record
            self._insert()
    
    def _insert(self) -> None:
        """Insert a new record into the database.
        
        This method is called by save() for new records.
        """
        fields = [name for name in self.__fields__ if getattr(self, name) is not None]
        values = [getattr(self, name) for name in fields]
        
        placeholders = ", ".join(["?"] * len(fields))
        query = f"INSERT INTO {self.__tablename__} ({', '.join(fields)}) VALUES ({placeholders})"
        
        cursor = execute(query, tuple(values))
        
        # Set primary key if it's auto-increment
        for name, field in self.__fields__.items():
            if field.primary_key:
                setattr(self, name, cursor.lastrowid)
                break
    
    def _update(self) -> None:
        """Update an existing record in the database.
        
        This method is called by save() for existing records.
        """
        # Find primary key
        primary_key = None
        primary_key_value = None
        for name, field in self.__fields__.items():
            if field.primary_key:
                primary_key = name
                primary_key_value = getattr(self, name)
                break
        
        if not primary_key:
            raise QueryError("No primary key defined for model")
        
        # Prepare update fields
        update_fields = [name for name in self.__fields__ if name != primary_key]
        update_values = [getattr(self, name) for name in update_fields]
        update_values.append(primary_key_value)
        
        set_clause = ", ".join([f"{name} = ?" for name in update_fields])
        query = f"UPDATE {self.__tablename__} SET {set_clause} WHERE {primary_key} = ?"
        
        execute(query, tuple(update_values))
    
    def delete(self) -> None:
        """Delete the model instance from the database.
        
        This method deletes the record associated with this model instance.
        """
        # Find primary key
        primary_key = None
        primary_key_value = None
        for name, field in self.__fields__.items():
            if field.primary_key:
                primary_key = name
                primary_key_value = getattr(self, name)
                break
        
        if not primary_key or primary_key_value is None:
            raise QueryError("Cannot delete: no primary key value set")
        
        query = f"DELETE FROM {self.__tablename__} WHERE {primary_key} = ?"
        execute(query, (primary_key_value,))


# Example usage
class User(Model):
    """Example User model.
    
    This model demonstrates how to define a database model with fields.
    """
    __tablename__ = "users"
    
    id = Field("INTEGER", primary_key=True, nullable=False)
    username = Field("TEXT", unique=True, nullable=False)
    email = Field("TEXT", unique=True, nullable=False)
    password_hash = Field("TEXT", nullable=False)
    created_at = Field("DATETIME", default="CURRENT_TIMESTAMP")
    updated_at = Field("DATETIME", default="CURRENT_TIMESTAMP")
