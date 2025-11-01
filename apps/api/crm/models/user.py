"""
User Model - TENANT SCHEMA

This User model lives in TENANT schemas, NOT in public schema.
Each tenant has their own users table with complete isolation.

Key Concepts:
- Users are tenant-specific (cannot access other tenants)
- Only admins can create users
- First user (owner) is created during tenant signup
- Roles: OWNER, ADMIN, MANAGER, SALESPERSON

Example:
    tenant_acme_corp schema → users table → Acme employees
    tenant_techstart schema → users table → TechStart employees
"""

import uuid
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    """
    Custom User Manager for tenant-specific users
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        
        # Use email as username
        if 'username' not in extra_fields:
            extra_fields['username'] = email
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser (for Django admin)
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'owner')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User Model (Lives in TENANT schema)
    
    Each tenant has their own users table with complete data isolation.
    
    Role Hierarchy:
    - OWNER: Person who signed up, full control
    - ADMIN: Can manage users and all settings
    - MANAGER: Can manage team, view all data
    - SALESPERSON: Can manage own contacts/deals
    
    Key Features:
    - Email-based authentication
    - UUID primary keys
    - Role-based permissions
    - Created by admin tracking
    - Cannot access other tenants
    
    Usage:
        # Admin creating a new user
        user = User.objects.create_user(
            email='john@example.com',
            password='secure_password',
            first_name='John',
            last_name='Doe',
            role='salesperson',
            created_by=admin_user
        )
    """
    
    # Use UUID as primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this user"
    )
    
    # Override email to make it required and unique
    email = models.EmailField(
        unique=True,
        help_text="User's email address (must be unique within tenant)"
    )
    
    # Role system
    ROLE_CHOICES = [
        ('owner', 'Owner'),  # Created during signup, full control
        ('admin', 'Administrator'),  # Can manage users and settings
        ('manager', 'Manager'),  # Can view all data, manage team
        ('salesperson', 'Salesperson'),  # Can manage own deals/contacts
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='salesperson',
        help_text="User's role within the organization"
    )
    
    # Track who created this user (for admin accountability)
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        help_text="Admin who created this user account"
    )
    
    # Additional fields
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="User's phone number"
    )
    
    # Use custom manager
    objects = UserManager()
    
    # Use email as username field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove email from required fields since it's the USERNAME_FIELD
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        """String representation"""
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """Returns the user's full name"""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email
    
    def is_owner(self):
        """Check if user is the tenant owner"""
        return self.role == 'owner'
    
    def is_admin_or_owner(self):
        """Check if user has admin privileges"""
        return self.role in ['owner', 'admin']
    
    def can_create_users(self):
        """Check if user can create other users"""
        return self.role in ['owner', 'admin']
    
    def can_manage_users(self):
        """Check if user can edit/delete users"""
        return self.role in ['owner', 'admin']
    
    def can_view_all_data(self):
        """Check if user can view all contacts/deals"""
        return self.role in ['owner', 'admin', 'manager']
