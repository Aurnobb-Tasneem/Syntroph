"""
Django App Configuration for CRM App
"""

from django.apps import AppConfig


class CrmConfig(AppConfig):
    """
    Configuration for the CRM application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'
    verbose_name = 'Customer Relationship Management'
    
    def ready(self):
        """
        This method runs when Django starts
        """
        # Import signals if we add them later
        pass
