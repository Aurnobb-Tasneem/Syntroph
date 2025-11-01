"""
Core Models - PUBLIC SCHEMA ONLY

This file contains ONLY models that live in the 'public' schema.
These are shared across ALL tenants.

Models in this file:
1. Tenant - Represents a company/organization (minimal info)

NOTE: User model is NO LONGER here!
Users now live in TENANT schemas (see crm/models/user.py)
"""

import uuid
from django.db import models


class Tenant(models.Model):
    """
    Tenant Model (Global - lives in 'public' schema)
    
    Represents a company/organization that uses the CRM.
    Each tenant gets its own database schema for data isolation.
    
    Multi-Tenant Architecture:
    - Schema-per-tenant approach
    - Each tenant has isolated data (users, contacts, deals, etc.)
    - Tenants share the same codebase but have separate data
    
    Example:
        Tenant 1: "Acme Corp" → schema: acme_corp, domain: acme
        Tenant 2: "TechStart Inc" → schema: techstart, domain: techstart
        
        Each schema has its own:
        - users table (employees of that company)
        - contacts table (CRM contacts)
        - deals table (sales pipeline)
        - organizations table (CRM companies)
        etc.
    
    Usage:
        # During signup
        tenant = Tenant.objects.create(
            company_name="Acme Corporation",
            schema_name="acme_corp",
            domain="acme",  # acme.syntroph.com
            owner_email="john@acme.com"
        )
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this tenant"
    )
    
    company_name = models.CharField(
        max_length=255,
        help_text="Display name of the company (e.g., 'Acme Corporation')"
    )
    
    schema_name = models.CharField(
        max_length=63,  # PostgreSQL limit for schema names
        unique=True,
        db_index=True,
        help_text="PostgreSQL schema name (e.g., 'acme_corp')"
    )
    
    domain = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="Subdomain for this tenant (e.g., 'acme' for acme.syntroph.com)"
    )
    
    owner_email = models.EmailField(
        help_text="Email of the person who signed up (becomes first admin)"
    )
    
    # Subscription and status
    SUBSCRIPTION_TIERS = [
        ('free', 'Free Tier'),
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    subscription_tier = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_TIERS,
        default='free',
        help_text="Current subscription plan"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this tenant's account is active"
    )
    
    max_users = models.IntegerField(
        default=5,
        help_text="Maximum number of users allowed (based on subscription)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this tenant was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this tenant was last updated"
    )
    
    class Meta:
        db_table = 'tenants'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['domain']),
            models.Index(fields=['schema_name']),
        ]
    
    def __str__(self):
        """String representation"""
        return f"{self.company_name} ({self.domain})"
    
    def get_schema_name_with_prefix(self):
        """
        Get the full PostgreSQL schema name with prefix
        Returns: 'tenant_acme_corp'
        """
        return f"tenant_{self.schema_name}"
    
    def get_subdomain_url(self):
        """
        Get the full subdomain URL
        Returns: 'https://acme.syntroph.com'
        """
        # TODO: Make domain configurable
        return f"https://{self.domain}.syntroph.com"
