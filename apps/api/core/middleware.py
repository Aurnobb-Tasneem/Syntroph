"""
Tenant Routing Middleware
==========================

This middleware automatically routes requests to the correct tenant schema
based on the request headers or domain.

How it works:
1. Extract tenant identifier from request (domain, subdomain, or header)
2. Look up the Tenant in the database
3. Set the PostgreSQL search_path to the tenant's schema
4. Process the request (views use tenant's data automatically)
5. Reset search_path after request

Tenant Identification Methods:
- Domain-based: acme.syntroph.com → tenant with domain='acme.syntroph.com'
- Subdomain-based: acme.syntroph.com → tenant with schema_name='acme'
- Header-based: X-Tenant-ID header → tenant with id or schema_name

Example Request Flow:
    1. Request to: https://acme.syntroph.com/api/contacts
    2. Middleware identifies: tenant = 'acme'
    3. Sets: search_path = 'tenant_acme, public'
    4. View queries: Contact.objects.all()
    5. PostgreSQL returns: Contacts from tenant_acme.contacts table
    6. Response sent with Acme's data
    7. Middleware resets: search_path = 'public'
"""

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.conf import settings
from core.models import Tenant
from core.utils import SchemaManager
import logging

logger = logging.getLogger(__name__)


class TenantRoutingMiddleware(MiddlewareMixin):
    """
    Middleware to route requests to the correct tenant schema
    
    This middleware must be placed AFTER AuthenticationMiddleware
    so we can access request.user for tenant identification.
    
    Add to settings.py MIDDLEWARE:
        'core.middleware.TenantRoutingMiddleware',
    """
    
    # Paths that don't require tenant context (use public schema)
    PUBLIC_PATHS = [
        '/admin/',
        '/api/auth/',
        '/api/tenants/',
        '/api/users/register/',
        '/api/users/login/',
        '/api/docs/',
        '/api/schema/',
        '/health/',
        '/static/',
        '/media/',
    ]
    
    def process_request(self, request):
        """
        Process incoming request and set tenant schema
        
        Args:
            request: HttpRequest object
        
        Returns:
            None if successful, HttpResponse if error
        """
        # Check if this is a public path (no tenant needed)
        if self._is_public_path(request.path):
            SchemaManager.set_search_path(SchemaManager.PUBLIC_SCHEMA)
            request.tenant = None
            return None
        
        # Try to identify the tenant
        tenant = self._identify_tenant(request)
        
        if not tenant:
            # No tenant identified - return error
            logger.warning(f"No tenant identified for path: {request.path}")
            return JsonResponse({
                'error': 'Tenant not identified',
                'message': 'Please provide a valid tenant domain or X-Tenant-ID header'
            }, status=400)
        
        if not tenant.is_active:
            # Tenant is inactive
            logger.warning(f"Inactive tenant accessed: {tenant.schema_name}")
            return JsonResponse({
                'error': 'Tenant inactive',
                'message': 'This tenant account is currently inactive'
            }, status=403)
        
        # Set the search_path to the tenant's schema
        try:
            SchemaManager.set_search_path(tenant.schema_name)
            request.tenant = tenant
            logger.debug(f"Request routed to tenant: {tenant.schema_name}")
            
        except Exception as e:
            logger.error(f"Error setting schema for tenant {tenant.schema_name}: {e}")
            return JsonResponse({
                'error': 'Schema error',
                'message': 'Unable to access tenant data'
            }, status=500)
        
        return None
    
    def process_response(self, request, response):
        """
        Reset search_path after request is processed
        
        Args:
            request: HttpRequest object
            response: HttpResponse object
        
        Returns:
            HttpResponse object
        """
        # Reset to public schema
        try:
            SchemaManager.set_search_path(SchemaManager.PUBLIC_SCHEMA)
        except Exception as e:
            logger.error(f"Error resetting schema: {e}")
        
        return response
    
    def _is_public_path(self, path):
        """
        Check if the request path is public (doesn't need tenant)
        
        Args:
            path: Request path string
        
        Returns:
            bool: True if public path
        """
        return any(path.startswith(public_path) for public_path in self.PUBLIC_PATHS)
    
    def _identify_tenant(self, request):
        """
        Identify the tenant from request
        
        Tries multiple methods in order:
        1. X-Tenant-ID header (schema_name or UUID)
        2. X-Tenant-Schema header (schema_name)
        3. Domain/subdomain matching
        4. User's default tenant (if authenticated)
        
        Args:
            request: HttpRequest object
        
        Returns:
            Tenant object or None
        """
        tenant = None
        
        # Method 1: X-Tenant-ID header (UUID or schema_name)
        tenant_id = request.headers.get('X-Tenant-ID')
        if tenant_id:
            try:
                # Try as UUID first
                from uuid import UUID
                tenant = Tenant.objects.get(id=UUID(tenant_id))
                logger.debug(f"Tenant identified by X-Tenant-ID (UUID): {tenant.schema_name}")
                return tenant
            except (ValueError, Tenant.DoesNotExist):
                # Try as schema_name
                try:
                    tenant = Tenant.objects.get(schema_name=tenant_id)
                    logger.debug(f"Tenant identified by X-Tenant-ID (schema): {tenant.schema_name}")
                    return tenant
                except Tenant.DoesNotExist:
                    pass
        
        # Method 2: X-Tenant-Schema header (schema_name only)
        tenant_schema = request.headers.get('X-Tenant-Schema')
        if tenant_schema:
            try:
                tenant = Tenant.objects.get(schema_name=tenant_schema)
                logger.debug(f"Tenant identified by X-Tenant-Schema: {tenant.schema_name}")
                return tenant
            except Tenant.DoesNotExist:
                pass
        
        # Method 3: Domain matching
        host = request.get_host()
        try:
            tenant = Tenant.objects.get(domain=host)
            logger.debug(f"Tenant identified by domain: {tenant.schema_name}")
            return tenant
        except Tenant.DoesNotExist:
            pass
        
        # Method 4: Subdomain matching (e.g., acme.syntroph.com → acme)
        if '.' in host:
            subdomain = host.split('.')[0]
            try:
                tenant = Tenant.objects.get(schema_name=subdomain)
                logger.debug(f"Tenant identified by subdomain: {tenant.schema_name}")
                return tenant
            except Tenant.DoesNotExist:
                pass
        
        # Method 5: User's default tenant (if authenticated)
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Get user's first active tenant membership
            from core.models import TenantMembership
            membership = TenantMembership.objects.filter(
                user=request.user,
                is_active=True
            ).select_related('tenant').first()
            
            if membership and membership.tenant.is_active:
                tenant = membership.tenant
                logger.debug(f"Tenant identified by user default: {tenant.schema_name}")
                return tenant
        
        # No tenant identified
        return None


class TenantPermissionMiddleware(MiddlewareMixin):
    """
    Middleware to check user has access to the requested tenant
    
    This must be placed AFTER TenantRoutingMiddleware
    and AFTER AuthenticationMiddleware.
    
    Validates that:
    - User is authenticated (for non-public paths)
    - User has an active membership in the tenant
    - User's role allows access to the requested resource
    """
    
    def process_request(self, request):
        """
        Check if user has permission to access the tenant
        
        Args:
            request: HttpRequest object
        
        Returns:
            None if allowed, HttpResponse if denied
        """
        # Skip public paths
        if not hasattr(request, 'tenant') or request.tenant is None:
            return None
        
        # Check if user is authenticated
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            logger.warning(f"Unauthenticated access to tenant: {request.tenant.schema_name}")
            return JsonResponse({
                'error': 'Authentication required',
                'message': 'You must be logged in to access this tenant'
            }, status=401)
        
        # Check if user has membership in this tenant
        from core.models import TenantMembership
        try:
            membership = TenantMembership.objects.get(
                user=request.user,
                tenant=request.tenant,
                is_active=True
            )
            request.tenant_membership = membership
            logger.debug(f"User {request.user.email} accessing {request.tenant.schema_name} as {membership.role}")
            
        except TenantMembership.DoesNotExist:
            logger.warning(f"User {request.user.email} has no access to tenant: {request.tenant.schema_name}")
            return JsonResponse({
                'error': 'Access denied',
                'message': 'You do not have access to this tenant'
            }, status=403)
        
        return None


# Development-only middleware to show current tenant
class TenantDebugMiddleware(MiddlewareMixin):
    """
    Development middleware to add tenant info to response headers
    
    Only use in development! Remove in production.
    
    Adds headers:
    - X-Current-Tenant: schema_name
    - X-Current-User: email
    - X-User-Role: role in tenant
    """
    
    def process_response(self, request, response):
        """Add debug headers to response"""
        
        if not settings.DEBUG:
            return response
        
        # Add tenant info
        if hasattr(request, 'tenant') and request.tenant:
            response['X-Current-Tenant'] = request.tenant.schema_name
        
        # Add user info
        if hasattr(request, 'user') and request.user.is_authenticated:
            response['X-Current-User'] = request.user.email
        
        # Add role info
        if hasattr(request, 'tenant_membership') and request.tenant_membership:
            response['X-User-Role'] = request.tenant_membership.role
        
        return response
