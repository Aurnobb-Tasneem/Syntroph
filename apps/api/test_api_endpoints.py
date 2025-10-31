"""
Test CRM API Endpoints

Tests the REST API for Contact, Organization, and Deal models
with multi-tenant support.
"""

import os
import sys
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from core.models import Tenant, TenantMembership
from crm.models import Contact, Organization, Deal
from core.utils import SchemaManager

User = get_user_model()


def create_test_data():
    """Create test tenant and data"""
    print("\n" + "="*60)
    print("SETTING UP TEST DATA")
    print("="*60)
    
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
    schema_manager = SchemaManager()
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
    
    return tenant, admin_user


def test_api_endpoints(tenant, user):
    """Test the API endpoints"""
    print("\n" + "="*60)
    print("TESTING API ENDPOINTS")
    print("="*60)
    
    # Create a test client
    client = Client()
    
    # Login
    login_success = client.login(username=user.email, password='testpass123')
    print(f"\n✓ Login successful: {login_success}")
    
    # Test headers for tenant routing
    headers = {
        'HTTP_X_TENANT_ID': str(tenant.id),
    }
    
    # Test 1: Create an organization
    print("\n" + "-"*60)
    print("TEST 1: Create Organization")
    print("-"*60)
    
    org_data = {
        'name': 'Acme Corporation',
        'domain': 'acme.com',
        'industry': 'technology',
        'employee_count': '51-200',
        'annual_revenue': '5000000.00',
        'email': 'contact@acme.com',
        'phone': '+1-555-0100',
        'lifecycle_stage': 'customer',
    }
    
    response = client.post(
        '/api/organizations/',
        data=json.dumps(org_data),
        content_type='application/json',
        **headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        org_id = response.json()['id']
        print(f"✓ Organization created: {response.json()['name']} (ID: {org_id})")
    else:
        print(f"✗ Error: {response.content.decode()}")
        return
    
    # Test 2: Create contacts
    print("\n" + "-"*60)
    print("TEST 2: Create Contacts")
    print("-"*60)
    
    contacts_data = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@acme.com',
            'phone': '+1-555-0101',
            'job_title': 'CEO',
            'organization': org_id,
            'lifecycle_stage': 'customer',
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@acme.com',
            'phone': '+1-555-0102',
            'job_title': 'CTO',
            'organization': org_id,
            'lifecycle_stage': 'customer',
        }
    ]
    
    contact_ids = []
    for contact_data in contacts_data:
        response = client.post(
            '/api/contacts/',
            data=json.dumps(contact_data),
            content_type='application/json',
            **headers
        )
        
        if response.status_code == 201:
            contact = response.json()
            contact_ids.append(contact['id'])
            print(f"✓ Contact created: {contact['full_name']} ({contact['job_title']})")
        else:
            print(f"✗ Error: {response.content.decode()}")
    
    # Test 3: Create a deal
    print("\n" + "-"*60)
    print("TEST 3: Create Deal")
    print("-"*60)
    
    deal_data = {
        'name': 'Enterprise License Deal',
        'amount': '150000.00',
        'currency': 'USD',
        'stage': 'proposal_sent',
        'probability': 75,
        'organization': org_id,
        'contact': contact_ids[0] if contact_ids else None,
        'expected_close_date': '2025-12-31',
        'description': 'Annual enterprise software license',
    }
    
    response = client.post(
        '/api/deals/',
        data=json.dumps(deal_data),
        content_type='application/json',
        **headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        deal = response.json()
        deal_id = deal['id']
        print(f"✓ Deal created: {deal['name']}")
        print(f"  Amount: ${deal['amount']} {deal['currency']}")
        print(f"  Stage: {deal['stage']}")
        print(f"  Probability: {deal['probability']}%")
        print(f"  Weighted Value: ${deal['weighted_value']}")
    else:
        print(f"✗ Error: {response.content.decode()}")
        return
    
    # Test 4: List contacts
    print("\n" + "-"*60)
    print("TEST 4: List Contacts")
    print("-"*60)
    
    response = client.get('/api/contacts/', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"✓ Found {len(contacts)} contacts:")
        for contact in contacts:
            print(f"  - {contact['full_name']} ({contact['email']})")
    else:
        print(f"✗ Error: {response.content.decode()}")
    
    # Test 5: Get organization with contacts
    print("\n" + "-"*60)
    print("TEST 5: Get Organization Details")
    print("-"*60)
    
    response = client.get(f'/api/organizations/{org_id}/', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        org = response.json()
        print(f"✓ Organization: {org['name']}")
        print(f"  Domain: {org['domain']}")
        print(f"  Industry: {org['industry']}")
        print(f"  Contact Count: {org['contact_count']}")
        print(f"  Deal Count: {org['deal_count']}")
        print(f"  Total Deal Value: ${org['total_deal_value']}")
    else:
        print(f"✗ Error: {response.content.decode()}")
    
    # Test 6: Get pipeline statistics
    print("\n" + "-"*60)
    print("TEST 6: Pipeline Statistics")
    print("-"*60)
    
    response = client.get('/api/deals/pipeline/', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Pipeline Statistics:")
        print(f"  Total Deals: {stats['total_deals']}")
        print(f"  Open Deals: {stats['open_deals']}")
        print(f"  Won Deals: {stats['won_deals']}")
        print(f"  Lost Deals: {stats['lost_deals']}")
        print(f"  Total Value: ${stats['total_value']}")
        print(f"  Weighted Value: ${stats['total_weighted_value']}")
        print(f"  Win Rate: {stats['win_rate']:.2f}%")
    else:
        print(f"✗ Error: {response.content.decode()}")
    
    # Test 7: Mark deal as won
    print("\n" + "-"*60)
    print("TEST 7: Mark Deal as Won")
    print("-"*60)
    
    response = client.post(f'/api/deals/{deal_id}/mark_won/', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        deal = response.json()
        print(f"✓ Deal marked as won:")
        print(f"  Stage: {deal['stage']}")
        print(f"  Closed Date: {deal['actual_close_date']}")
    else:
        print(f"✗ Error: {response.content.decode()}")
    
    # Test 8: Search contacts
    print("\n" + "-"*60)
    print("TEST 8: Search Contacts")
    print("-"*60)
    
    response = client.get('/api/contacts/?search=john', **headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        contacts = response.json()
        print(f"✓ Search results for 'john': {len(contacts)} contacts")
        for contact in contacts:
            print(f"  - {contact['full_name']} ({contact['email']})")
    else:
        print(f"✗ Error: {response.content.decode()}")


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
    print("CRM API ENDPOINT TESTS")
    print("="*60)
    print("Testing REST API with multi-tenant support")
    
    try:
        # Setup
        tenant, user = create_test_data()
        
        # Run tests
        test_api_endpoints(tenant, user)
        
        # Cleanup
        cleanup(tenant)
        
        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60)
        
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
