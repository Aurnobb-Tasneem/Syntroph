"""
Core Models for Syntroph CRM

This file contains the GLOBAL models that live in the 'public' schema.
These models are shared across ALL tenants.

Models in this file:
1. User - The global user identity (extends Django's AbstractUser)
2. Tenant - Represents a company/organization (will be created next)
3. TenantMembership - Links users to tenants with roles (will be created next)

Why UUIDs?
- Better for distributed systems
- No sequential ID leaks (security)
- Easier to merge databases if needed
"""

import uuid
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    """
    Custom User Manager to allow email-based authentication
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        Uses email as username if username not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        
        # Use email as username if not provided
        if 'username' not in extra_fields:
            extra_fields['username'] = email
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User Model (Global - lives in 'public' schema)
    
    This model extends Django's AbstractUser, which already includes:
    - username
    - email
    - password (hashed)
    - first_name
    - last_name
    - is_staff (can access admin)
    - is_active (account enabled/disabled)
    - date_joined
    
    We're adding:
    - UUID as primary key (instead of integer)
    - Additional fields can be added here as needed
    
    Usage:
        # Create a new user
        user = User.objects.create_user(
            username='john@example.com',
            email='john@example.com',
            password='secure_password'
        )
        
        # The password is automatically hashed by Django
        # Never store plain text passwords!
    
    Note: After creating this model, you MUST:
    1. Update settings.py: AUTH_USER_MODEL = 'core.User'
    2. Run: python manage.py makemigrations
    3. Run: python manage.py migrate
    """
    
    # Use UUID as primary key instead of auto-incrementing integer
    # This is better for security and distributed systems
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this user"
    )
    
    # Override email to make it required and unique
    # By default, Django's AbstractUser allows duplicate emails
    email = models.EmailField(
        unique=True,
        help_text="User's email address (must be unique)"
    )
    
    # Use custom manager that allows email-based authentication
    objects = UserManager()
    
    # Tell Django to use email as the username field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove email from required fields since it's the USERNAME_FIELD
    
    class Meta:
        db_table = 'users'  # Name of the table in the database
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']  # Newest users first
    
    def __str__(self):
        """
        String representation of the user
        This is what shows up in the Django admin
        """
        return f"{self.email} ({self.username})"
    
    def get_full_name(self):
        """
        Returns the user's full name
        Example: "John Doe"
        """
        return f"{self.first_name} {self.last_name}".strip()


class Tenant(models.Model):
    """
    Tenant Model (Global - lives in 'public' schema)
    
    Represents a company/organization that uses the CRM.
    Each tenant gets its own database schema for data isolation.
    
    Multi-Tenant Architecture:
    - Schema-per-tenant approach
    - Each tenant has isolated data (contacts, deals, etc.)
    - Tenants share the same codebase but have separate data
    
    Example:
        Tenant 1: "Acme Corp" → schema: tenant_acme_corp
        Tenant 2: "TechStart Inc" → schema: tenant_techstart_inc
        
        Each schema has its own:
        - contacts table
        - deals table
        - organizations table
        etc.
    
    Usage:
        # Create a new tenant
        tenant = Tenant.objects.create(
            name="Acme Corporation",
            schema_name="acme_corp",
            domain="acme.syntroph.com"
        )
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this tenant"
    )
    
    name = models.CharField(
        max_length=255,
        help_text="Company/Organization name (e.g., 'Acme Corporation')"
    )
    
    schema_name = models.CharField(
        max_length=63,  # PostgreSQL schema name limit
        unique=True,
        help_text="Database schema name (e.g., 'tenant_acme_corp'). Must be unique."
    )
    
    domain = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="Custom domain for this tenant (e.g., 'acme.syntroph.com')"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Is this tenant active? Inactive tenants cannot access the system."
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this tenant was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this tenant was last updated"
    )
    
    # Subscription/billing fields (for future use)
    subscription_tier = models.CharField(
        max_length=50,
        default='free',
        choices=[
            ('free', 'Free'),
            ('starter', 'Starter'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        help_text="Subscription plan tier"
    )
    
    max_users = models.IntegerField(
        default=5,
        help_text="Maximum number of users allowed for this tenant"
    )
    
    class Meta:
        db_table = 'tenants'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.schema_name})"
    
    def get_member_count(self):
        """
        Returns the number of users in this tenant
        """
        return self.memberships.count()
    
    def can_add_user(self):
        """
        Check if this tenant can add more users
        """
        return self.get_member_count() < self.max_users


class TenantMembership(models.Model):
    """
    TenantMembership Model (Global - lives in 'public' schema)
    
    Links Users to Tenants with roles.
    One user can belong to multiple tenants with different roles.
    
    Example:
        John (User) → Acme Corp (Tenant) → Role: Admin
        John (User) → TechStart (Tenant) → Role: User
        Jane (User) → Acme Corp (Tenant) → Role: User
    
    Roles:
    - owner: Full control, billing, can delete tenant
    - admin: Can manage users, settings, all data
    - manager: Can manage data, limited settings access
    - user: Can view/edit data (respects RBAC permissions)
    - guest: Read-only access
    
    Usage:
        # Add a user to a tenant
        membership = TenantMembership.objects.create(
            user=john,
            tenant=acme_corp,
            role='admin'
        )
        
        # Check user's role in a tenant
        if membership.role == 'admin':
            # User has admin privileges
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this membership"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_memberships',
        help_text="The user who is a member of the tenant"
    )
    
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='memberships',
        help_text="The tenant this user belongs to"
    )
    
    role = models.CharField(
        max_length=20,
        choices=[
            ('owner', 'Owner'),
            ('admin', 'Administrator'),
            ('manager', 'Manager'),
            ('user', 'User'),
            ('guest', 'Guest'),
        ],
        default='user',
        help_text="User's role in this tenant"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Is this membership active? Inactive members cannot access the tenant."
    )
    
    joined_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the user joined this tenant"
    )
    
    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invited_memberships',
        help_text="The user who invited this member"
    )
    
    class Meta:
        db_table = 'tenant_memberships'
        verbose_name = 'Tenant Membership'
        verbose_name_plural = 'Tenant Memberships'
        ordering = ['-joined_at']
        # Ensure a user can only have ONE membership per tenant
        unique_together = [['user', 'tenant']]
        indexes = [
            models.Index(fields=['user', 'tenant']),
            models.Index(fields=['tenant', 'role']),
        ]
    
    def __str__(self):
        return f"{self.user.email} → {self.tenant.name} ({self.role})"
    
    def is_owner(self):
        """Check if this membership has owner privileges"""
        return self.role == 'owner'
    
    def is_admin(self):
        """Check if this membership has admin privileges"""
        return self.role in ['owner', 'admin']
    
    def can_manage_users(self):
        """Check if this membership can add/remove users"""
        return self.role in ['owner', 'admin']
    
    def can_edit_data(self):
        """Check if this membership can edit data"""
        return self.role in ['owner', 'admin', 'manager', 'user']
