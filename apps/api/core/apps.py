"""
Django App Configuration for Core App

This file tells Django about the 'core' app and its settings.
Every Django app needs an apps.py file to be properly registered.

What this does:
- Defines the app name as 'core'
- Sets up any app-specific configuration
- Can be used to run code when the app starts (using ready() method)
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration for the Core application
    
    This class is referenced in settings.py INSTALLED_APPS as 'core.apps.CoreConfig'
    or simply as 'core' (Django will find this automatically)
    """
    
    # Use BigAutoField for auto-incrementing IDs (modern Django default)
    # Note: Our User model uses UUID, but this applies to any models that don't specify
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of the app (must match the folder name)
    name = 'core'
    
    # Human-readable name for Django admin
    verbose_name = 'Core Application'
    
    def ready(self):
        """
        This method runs when Django starts
        
        Use this to:
        - Register signals
        - Import models
        - Run startup code
        
        Example:
            from . import signals  # Import signal handlers
        """
        pass  # Nothing needed here yet
