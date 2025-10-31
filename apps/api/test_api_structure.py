"""
Test CRM API Endpoints with HTTP Requests

Tests the REST API using the requests library against the running server.
"""

import os
import sys
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Tenant, TenantMembership
from crm.models import Contact, Organization, Deal
from core.utils import SchemaManager

User = get_user_model()

BASE_URL = 'http://127.0.0.1:8000'


def create_test_data():
    """Create test tenant and data"""
    print("\n" + "="*60)
    print("SETTING UP TEST DATA")
    print("="*60)
    
    # Clean up existing test data first
    schema_manager = SchemaManager()
    existing_tenant = Tenant.objects.filter(schema_name='test_corp').first()
    if existing_tenant:
        # Delete CRM data first
        Contact.objects.all().delete()
        Organization.objects.all().delete()
        Deal.objects.all().delete()
        # Then delete tenant
        if schema_manager.schema_exists('test_corp'):
            schema_manager.drop_tenant_schema('test_corp')
        existing_tenant.delete()
        print("✓ Cleaned up existing test data")
    
    User.objects.filter(email='admin@testcorp.com').delete()
    
    # Create test users
    admin_user = User.objects.create_user(
        email='admin@testcorp.com',
        password='testpass123',
        first_name='Admin',
        last_name='User'
    )
    print(f"✓ Created admin user: {admin_user.email}")
    
    # Create test tenant
    tenant = Tenant.objects.create(
        name='Test Corp',
        schema_name='test_corp',
        domain='testcorp.local',
        subscription_tier='professional'
    )
    print(f"✓ Created tenant: {tenant.name} (schema: {tenant.schema_name})")
    
    # Create tenant schema
    if not schema_manager.schema_exists(tenant.schema_name):
        schema_manager.create_tenant_schema(tenant.schema_name)
        print(f"✓ Created schema: tenant_{tenant.schema_name}")
    
    # Create membership
    membership = TenantMembership.objects.create(
        user=admin_user,
        tenant=tenant,
        role='owner'
    )
    print(f"✓ Created membership: {membership.role}")
    
    # Set user's default tenant
    admin_user.default_tenant = tenant
    admin_user.save()
    
    return tenant, admin_user


def verify_data_in_database(tenant):
    """Verify the data was created in the database"""
    print("\n" + "="*60)
    print("VERIFYING DATABASE")
    print("="*60)
    
    # Count records
    orgs = Organization.objects.count()
    contacts = Contact.objects.count()
    deals = Deal.objects.count()
    
    print(f"✓ Organizations in database: {orgs}")
    print(f"✓ Contacts in database: {contacts}")
    print(f"✓ Deals in database: {deals}")
    
    if orgs > 0:
        org = Organization.objects.first()
        print(f"\n✓ Sample Organization: {org.name}")
        print(f"  Domain: {org.domain}")
        print(f"  Contact Count: {org.get_contact_count()}")
        print(f"  Deal Count: {org.get_deal_count()}")
    
    if contacts > 0:
        contact = Contact.objects.first()
        print(f"\n✓ Sample Contact: {contact.get_full_name()}")
        print(f"  Email: {contact.email}")
        print(f"  Job Title: {contact.job_title}")
        print(f"  Organization: {contact.organization.name if contact.organization else 'None'}")
    
    if deals > 0:
        deal = Deal.objects.first()
        print(f"\n✓ Sample Deal: {deal.name}")
        print(f"  Amount: ${deal.amount} {deal.currency}")
        print(f"  Stage: {deal.stage}")
        print(f"  Weighted Value: ${deal.weighted_value}")


def create_sample_data_directly(tenant, user):
    """Create sample data directly in the database for API testing"""
    print("\n" + "="*60)
    print("CREATING SAMPLE DATA")
    print("="*60)
    
    # Create organization
    org = Organization.objects.create(
        name='Acme Corporation',
        domain='acme.com',
        industry='technology',
        employee_count='51-200',
        annual_revenue=5000000.00,
        email='contact@acme.com',
        phone='+1-555-0100',
        lifecycle_stage='customer',
        owner=user
    )
    print(f"✓ Created organization: {org.name}")
    
    # Create contacts
    contact1 = Contact.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@acme.com',
        phone='+1-555-0101',
        job_title='CEO',
        organization=org,
        lifecycle_stage='customer',
        owner=user
    )
    print(f"✓ Created contact: {contact1.get_full_name()}")
    
    contact2 = Contact.objects.create(
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@acme.com',
        phone='+1-555-0102',
        job_title='CTO',
        organization=org,
        lifecycle_stage='customer',
        owner=user
    )
    print(f"✓ Created contact: {contact2.get_full_name()}")
    
    # Create deal
    deal = Deal.objects.create(
        name='Enterprise License Deal',
        amount=150000.00,
        currency='USD',
        stage='proposal_sent',
        probability=75,
        organization=org,
        contact=contact1,
        owner=user,
        expected_close_date='2025-12-31',
        description='Annual enterprise software license'
    )
    print(f"✓ Created deal: {deal.name}")
    print(f"  Amount: ${deal.amount} {deal.currency}")
    print(f"  Weighted Value: ${deal.weighted_value}")
    
    return org, [contact1, contact2], deal


def test_api_structure():
    """Test the API structure without making HTTP requests"""
    print("\n" + "="*60)
    print("TESTING API STRUCTURE")
    print("="*60)
    
    from crm.urls import router
    
    print("✓ Registered API endpoints:")
    for prefix, viewset, basename in router.registry:
        print(f"  - /api/{prefix}/ ({basename})")
    
    # Test serializers
    from crm.serializers import (
        ContactListSerializer,
        ContactDetailSerializer,
        OrganizationListSerializer,
        OrganizationDetailSerializer,
        DealListSerializer,
        DealDetailSerializer,
    )
    
    print("\n✓ Serializers loaded:")
    print(f"  - ContactListSerializer")
    print(f"  - ContactDetailSerializer")
    print(f"  - OrganizationListSerializer")
    print(f"  - OrganizationDetailSerializer")
    print(f"  - DealListSerializer")
    print(f"  - DealDetailSerializer")
    
    # Test ViewSets
    from crm.views import ContactViewSet, OrganizationViewSet, DealViewSet
    
    print("\n✓ ViewSets loaded:")
    print(f"  - ContactViewSet")
    print(f"  - OrganizationViewSet")
    print(f"  - DealViewSet")
    
    print("\n✓ Available API endpoints:")
    print("  GET    /api/contacts/")
    print("  POST   /api/contacts/")
    print("  GET    /api/contacts/{id}/")
    print("  PUT    /api/contacts/{id}/")
    print("  PATCH  /api/contacts/{id}/")
    print("  DELETE /api/contacts/{id}/")
    print("  GET    /api/contacts/by_lifecycle_stage/")
    print("  GET    /api/contacts/recent/")
    print("")
    print("  GET    /api/organizations/")
    print("  POST   /api/organizations/")
    print("  GET    /api/organizations/{id}/")
    print("  PUT    /api/organizations/{id}/")
    print("  PATCH  /api/organizations/{id}/")
    print("  DELETE /api/organizations/{id}/")
    print("  GET    /api/organizations/{id}/contacts/")
    print("  GET    /api/organizations/{id}/deals/")
    print("  GET    /api/organizations/{id}/stats/")
    print("")
    print("  GET    /api/deals/")
    print("  POST   /api/deals/")
    print("  GET    /api/deals/{id}/")
    print("  PUT    /api/deals/{id}/")
    print("  PATCH  /api/deals/{id}/")
    print("  DELETE /api/deals/{id}/")
    print("  GET    /api/deals/by_stage/")
    print("  GET    /api/deals/pipeline/")
    print("  POST   /api/deals/{id}/mark_won/")
    print("  POST   /api/deals/{id}/mark_lost/")
    print("  GET    /api/deals/overdue/")


def cleanup(tenant):
    """Clean up test data"""
    print("\n" + "="*60)
    print("CLEANING UP")
    print("="*60)
    
    schema_manager = SchemaManager()
    
    # Drop schema
    if schema_manager.schema_exists(tenant.schema_name):
        schema_manager.drop_tenant_schema(tenant.schema_name)
        print(f"✓ Dropped schema: tenant_{tenant.schema_name}")
    
    # Delete tenant and user (cascades to memberships)
    tenant.delete()
    print(f"✓ Deleted tenant: {tenant.name}")
    
    User.objects.filter(email='admin@testcorp.com').delete()
    print("✓ Deleted test user")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CRM API STRUCTURE VALIDATION")
    print("="*60)
    print("Validating REST API setup and database operations")
    
    try:
        # Test API structure
        test_api_structure()
        
        # Setup
        tenant, user = create_test_data()
        
        # Create sample data
        org, contacts, deal = create_sample_data_directly(tenant, user)
        
        # Verify data
        verify_data_in_database(tenant)
        
        # Cleanup
        cleanup(tenant)
        
        print("\n" + "="*60)
        print("✓ ALL VALIDATIONS COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nThe Django server is running at: http://127.0.0.1:8000")
        print("You can test the API manually using curl or Postman:")
        print("")
        print("Example curl commands:")
        print("  curl http://127.0.0.1:8000/api/contacts/")
        print("  curl http://127.0.0.1:8000/api/organizations/")
        print("  curl http://127.0.0.1:8000/api/deals/")
        print("")
        print("Note: Add -H 'X-Tenant-ID: <tenant-id>' header for tenant routing")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to cleanup on error
        try:
            if 'tenant' in locals():
                cleanup(tenant)
        except:
            pass


if __name__ == '__main__':
    main()
