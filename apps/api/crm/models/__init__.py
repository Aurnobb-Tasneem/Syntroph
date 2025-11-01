"""
CRM Models Package

This package contains all CRM-related models that live in TENANT schemas.
"""

from .user import User
from .contact import Contact
from .organization import Organization
from .deal import Deal

__all__ = ['User', 'Contact', 'Organization', 'Deal']
