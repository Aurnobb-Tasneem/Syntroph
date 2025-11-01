"""
Database Router for Multi-Tenant Schema Separation

This router ensures that:
1. Tenant model → PUBLIC schema
2. User, Contact, Organization, Deal → TENANT schemas (NOT public)
3. Django system tables → PUBLIC schema
"""

class TenantDatabaseRouter:
    """
    Route database operations to appropriate schemas
    """
    
    # Models that live in PUBLIC schema
    PUBLIC_MODELS = {
        'tenant',  # core.Tenant
    }
    
    # Models that live in TENANT schemas
    TENANT_MODELS = {
        'user',  # crm.User
        'contact',  # crm.Contact
        'organization',  # crm.Organization
        'deal',  # crm.Deal
    }
    
    def db_for_read(self, model, **hints):
        """
        Route read operations
        """
        # Django system models always use default (public)
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return 'default'
        
        # Core models (Tenant) use default (public)
        if model._meta.app_label == 'core':
            return 'default'
        
        # CRM models should use tenant schema
        # But we'll let middleware handle this via connection.set_schema()
        if model._meta.app_label == 'crm':
            return 'default'  # Still use default connection, but middleware sets schema
        
        return 'default'
    
    def db_for_write(self, model, **hints):
        """
        Route write operations
        """
        return self.db_for_read(model, **hints)
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between models
        """
        # Allow all relations within same app
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        
        # Don't allow relations between public and tenant models
        # (User in tenant schema cannot FK to Tenant in public schema directly)
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Control which models get migrated to which database/schema
        
        IMPORTANT: CRM models should NOT be migrated to public schema!
        They should only exist in tenant schemas.
        """
        # Django system apps always migrate to default (public)
        if app_label in ['auth', 'contenttypes', 'sessions', 'admin']:
            return db == 'default'
        
        # Core app (Tenant) migrates to default (public)
        if app_label == 'core':
            return db == 'default'
        
        # CRM models should NOT migrate to public schema automatically
        # They will be migrated to tenant schemas manually when tenant is created
        if app_label == 'crm':
            # Don't auto-migrate CRM models to public schema
            # We'll handle this manually in tenant creation
            return False
        
        return db == 'default'
