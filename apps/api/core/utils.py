"""
Tenant Schema Management Utilities
===================================

This module provides utilities for managing PostgreSQL schemas in a multi-tenant environment.

What this does:
- Creates separate database schemas for each tenant
- Clones table structure from a template
- Manages schema lifecycle (create, delete, list)
- Ensures data isolation between tenants

Schema Strategy:
- public schema: Global data (users, tenants, tenant_memberships)
- tenant_* schemas: Tenant-specific data (contacts, deals, etc.)

Example:
    # Create a schema for a new tenant
    create_tenant_schema('acme_corp')
    
    # This creates: tenant_acme_corp schema
    # With tables: contacts, deals, organizations, etc.
"""

from django.db import connection, transaction
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SchemaManager:
    """
    Manages PostgreSQL schemas for multi-tenant isolation
    
    This class handles:
    - Creating new tenant schemas
    - Cloning table structures
    - Dropping tenant schemas
    - Listing existing schemas
    - Switching between schemas
    """
    
    SCHEMA_PREFIX = 'tenant_'
    PUBLIC_SCHEMA = 'public'
    
    # Tables that should be cloned to tenant schemas
    # These will be created in Phase 2 (CRM models)
    TENANT_TABLES = [
        # CRM Core
        'contacts',
        'organizations',
        'deals',
        'activities',
        'tasks',
        'notes',
        
        # Custom Fields
        'custom_fields',
        'custom_field_values',
        
        # Pipeline
        'pipelines',
        'pipeline_stages',
        
        # Future: Add more as we build them
    ]
    
    @classmethod
    def create_tenant_schema(cls, schema_name, create_tables=False):
        """
        Create a new schema for a tenant
        
        Args:
            schema_name: Name of the schema (without 'tenant_' prefix)
            create_tables: Whether to create tenant tables (default: False)
                          Set to True once we have CRM models
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> SchemaManager.create_tenant_schema('acme_corp')
            True
        """
        full_schema_name = f"{cls.SCHEMA_PREFIX}{schema_name}"
        
        try:
            with connection.cursor() as cursor:
                # Check if schema already exists
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = %s
                """, [full_schema_name])
                
                if cursor.fetchone():
                    logger.warning(f"Schema {full_schema_name} already exists")
                    return False
                
                # Create the schema
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{full_schema_name}"')
                logger.info(f"Created schema: {full_schema_name}")
                
                # Create tables if requested
                if create_tables:
                    cls._create_tenant_tables(full_schema_name)
                
                return True
                
        except Exception as e:
            logger.error(f"Error creating schema {full_schema_name}: {e}")
            return False
    
    @classmethod
    def _create_tenant_tables(cls, schema_name):
        """
        Create tenant-specific tables in the schema
        
        This will be used in Phase 2 when we have CRM models.
        For now, it's a placeholder.
        
        Args:
            schema_name: Full schema name (including prefix)
        """
        logger.info(f"Creating tables in schema {schema_name}...")
        
        # TODO: In Phase 2, we'll run migrations for tenant tables
        # For now, we just log that we would create them
        
        for table in cls.TENANT_TABLES:
            logger.info(f"  - Would create table: {schema_name}.{table}")
        
        # Future implementation:
        # 1. Set search_path to the tenant schema
        # 2. Run Django migrations for CRM models
        # 3. Create indexes and constraints
    
    @classmethod
    def drop_tenant_schema(cls, schema_name, cascade=True):
        """
        Delete a tenant schema and all its data
        
        ⚠️ WARNING: This permanently deletes ALL data for the tenant!
        
        Args:
            schema_name: Name of the schema (without 'tenant_' prefix)
            cascade: Whether to drop all objects in the schema (default: True)
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> SchemaManager.drop_tenant_schema('acme_corp')
            True
        """
        full_schema_name = f"{cls.SCHEMA_PREFIX}{schema_name}"
        
        try:
            with connection.cursor() as cursor:
                cascade_clause = "CASCADE" if cascade else "RESTRICT"
                cursor.execute(f'DROP SCHEMA IF EXISTS "{full_schema_name}" {cascade_clause}')
                logger.info(f"Dropped schema: {full_schema_name}")
                return True
                
        except Exception as e:
            logger.error(f"Error dropping schema {full_schema_name}: {e}")
            return False
    
    @classmethod
    def schema_exists(cls, schema_name):
        """
        Check if a tenant schema exists
        
        Args:
            schema_name: Name of the schema (without 'tenant_' prefix)
        
        Returns:
            bool: True if schema exists, False otherwise
        """
        full_schema_name = f"{cls.SCHEMA_PREFIX}{schema_name}"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = %s
                """, [full_schema_name])
                
                return cursor.fetchone() is not None
                
        except Exception as e:
            logger.error(f"Error checking schema {full_schema_name}: {e}")
            return False
    
    @classmethod
    def list_tenant_schemas(cls):
        """
        List all tenant schemas
        
        Returns:
            list: List of schema names (without prefix)
        
        Example:
            >>> SchemaManager.list_tenant_schemas()
            ['acme_corp', 'techstart_inc']
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name LIKE %s
                    ORDER BY schema_name
                """, [f"{cls.SCHEMA_PREFIX}%"])
                
                schemas = [row[0].replace(cls.SCHEMA_PREFIX, '') 
                          for row in cursor.fetchall()]
                return schemas
                
        except Exception as e:
            logger.error(f"Error listing schemas: {e}")
            return []
    
    @classmethod
    def set_search_path(cls, schema_name):
        """
        Set the PostgreSQL search_path to a specific schema
        
        This tells PostgreSQL which schema to use for queries.
        Used by middleware to route requests to the correct tenant.
        
        Args:
            schema_name: Name of the schema (without 'tenant_' prefix)
                        Or 'public' for the public schema
        
        Example:
            >>> SchemaManager.set_search_path('acme_corp')
            >>> # Now queries will use tenant_acme_corp schema
        """
        if schema_name == cls.PUBLIC_SCHEMA:
            full_schema_name = cls.PUBLIC_SCHEMA
        else:
            full_schema_name = f"{cls.SCHEMA_PREFIX}{schema_name}"
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO "{full_schema_name}", public')
                logger.debug(f"Set search_path to: {full_schema_name}")
                
        except Exception as e:
            logger.error(f"Error setting search_path to {full_schema_name}: {e}")
            raise
    
    @classmethod
    def get_current_schema(cls):
        """
        Get the current schema from search_path
        
        Returns:
            str: Current schema name (without prefix)
        
        Example:
            >>> SchemaManager.get_current_schema()
            'acme_corp'
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SHOW search_path")
                search_path = cursor.fetchone()[0]
                
                # Extract the first schema from search_path
                first_schema = search_path.split(',')[0].strip().strip('"')
                
                if first_schema.startswith(cls.SCHEMA_PREFIX):
                    return first_schema.replace(cls.SCHEMA_PREFIX, '')
                else:
                    return cls.PUBLIC_SCHEMA
                    
        except Exception as e:
            logger.error(f"Error getting current schema: {e}")
            return cls.PUBLIC_SCHEMA


class TenantSchemaContext:
    """
    Context manager for temporarily switching to a tenant schema
    
    Usage:
        with TenantSchemaContext('acme_corp'):
            # All queries here use tenant_acme_corp schema
            contacts = Contact.objects.all()
        
        # Back to original schema
    """
    
    def __init__(self, schema_name):
        """
        Initialize context manager
        
        Args:
            schema_name: Tenant schema name (without 'tenant_' prefix)
        """
        self.schema_name = schema_name
        self.original_schema = None
    
    def __enter__(self):
        """Enter the context - switch to tenant schema"""
        self.original_schema = SchemaManager.get_current_schema()
        SchemaManager.set_search_path(self.schema_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context - restore original schema"""
        SchemaManager.set_search_path(self.original_schema)
        return False


# Utility functions for convenience

def create_tenant_schema(tenant):
    """
    Create a schema for a Tenant model instance
    
    Args:
        tenant: Tenant model instance
    
    Returns:
        bool: True if successful
    
    Example:
        >>> tenant = Tenant.objects.get(name='Acme Corp')
        >>> create_tenant_schema(tenant)
        True
    """
    return SchemaManager.create_tenant_schema(tenant.schema_name)


def drop_tenant_schema(tenant):
    """
    Drop a schema for a Tenant model instance
    
    ⚠️ WARNING: This permanently deletes ALL data!
    
    Args:
        tenant: Tenant model instance
    
    Returns:
        bool: True if successful
    """
    return SchemaManager.drop_tenant_schema(tenant.schema_name)


def with_tenant_schema(schema_name):
    """
    Decorator to execute a function in a tenant schema
    
    Usage:
        @with_tenant_schema('acme_corp')
        def get_contacts():
            return Contact.objects.all()
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with TenantSchemaContext(schema_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator
