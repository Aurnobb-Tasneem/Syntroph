"""
CRM Models Package

This package contains all CRM models that live in tenant schemas.
"""

from .contact import Contact
from .organization import Organization
from .deal import Deal

__all__ = ['Contact', 'Organization', 'Deal']
