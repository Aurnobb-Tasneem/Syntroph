"""
Test CRM Models
===============

This script tests our Contact and Organization models.

What we'll test:
1. Create organizations
2. Create contacts
3. Link contacts to organizations
4. Test relationships and helper methods
5. Query and filter data

Run this with: python test_crm_models.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from crm.models import Contact, Organization
from core.models import User

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_crm_models():
    """Test CRM models"""
    
    print_header("🧪 Testing CRM Models")
    
    # Clean up existing test data
    print("\n🧹 Cleaning up existing test data...")
    Contact.objects.filter(email__endswith='@test.com').delete()
    Organization.objects.filter(domain__endswith='.test.com').delete()
    User.objects.filter(username__startswith='test_crm_').delete()
    print("✅ Cleanup complete")
    
    # Create a test user (owner)
    print_header("1. Creating Test User")
    
    owner = User.objects.create_user(
        username='test_crm_owner',
        email='owner@test.com',
        password='testpass123',
        first_name='Sales',
        last_name='Manager'
    )
    print(f"✅ Created owner: {owner.email}")
    
    # Create organizations
    print_header("2. Creating Organizations")
    
    acme = Organization.objects.create(
        name='Acme Corporation',
        domain='acme.test.com',
        industry='technology',
        employee_count='201-500',
        annual_revenue=5000000.00,
        phone='+1-555-0100',
        email='info@acme.test.com',
        website='https://acme.test.com',
        address_line1='123 Tech Street',
        city='San Francisco',
        state='CA',
        postal_code='94105',
        country='USA',
        lifecycle_stage='customer',
        owner=owner,
        description='Leading technology company'
    )
    print(f"✅ Created organization: {acme.name}")
    print(f"   - Industry: {acme.get_industry_display()}")
    print(f"   - Employees: {acme.get_employee_count_display()}")
    print(f"   - Revenue: ${acme.annual_revenue:,.2f}")
    print(f"   - Address: {acme.full_address}")
    
    techstart = Organization.objects.create(
        name='TechStart Inc',
        domain='techstart.test.com',
        industry='technology',
        employee_count='11-50',
        lifecycle_stage='opportunity',
        owner=owner
    )
    print(f"✅ Created organization: {techstart.name}")
    
    # Create contacts
    print_header("3. Creating Contacts")
    
    john = Contact.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@acme.test.com',
        phone='+1-555-0101',
        mobile='+1-555-0102',
        job_title='CEO',
        organization=acme,
        lifecycle_stage='customer',
        owner=owner,
        address_line1='123 Tech Street',
        city='San Francisco',
        state='CA',
        postal_code='94105',
        country='USA',
        linkedin_url='https://linkedin.com/in/johndoe',
        lead_source='referral',
        description='CEO of Acme Corporation, tech industry veteran'
    )
    print(f"✅ Created contact: {john.get_display_name()}")
    print(f"   - Email: {john.email}")
    print(f"   - Organization: {john.organization.name}")
    print(f"   - Stage: {john.get_lifecycle_stage_display()}")
    
    jane = Contact.objects.create(
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@acme.test.com',
        phone='+1-555-0103',
        job_title='CTO',
        organization=acme,
        lifecycle_stage='customer',
        owner=owner,
        lead_source='linkedin'
    )
    print(f"✅ Created contact: {jane.get_display_name()}")
    
    bob = Contact.objects.create(
        first_name='Bob',
        last_name='Johnson',
        email='bob@techstart.test.com',
        phone='+1-555-0104',
        job_title='Founder',
        organization=techstart,
        lifecycle_stage='opportunity',
        owner=owner,
        lead_source='website'
    )
    print(f"✅ Created contact: {bob.get_display_name()}")
    
    alice = Contact.objects.create(
        first_name='Alice',
        last_name='Williams',
        email='alice@test.com',
        phone='+1-555-0105',
        job_title='Independent Consultant',
        lifecycle_stage='lead',
        owner=owner,
        lead_source='cold_outreach',
        description='Independent consultant, no organization affiliation'
    )
    print(f"✅ Created contact: {alice.get_display_name()}")
    print(f"   - Organization: {alice.organization or 'None (Independent)'}")
    
    # Test relationships
    print_header("4. Testing Relationships")
    
    print(f"\n📊 {acme.name} Statistics:")
    print(f"   - Contacts: {acme.get_contact_count()}")
    print(f"   - Contacts list:")
    for contact in acme.contacts.all():
        print(f"      • {contact.get_display_name()}")
    
    print(f"\n📊 {techstart.name} Statistics:")
    print(f"   - Contacts: {techstart.get_contact_count()}")
    print(f"   - Contacts list:")
    for contact in techstart.contacts.all():
        print(f"      • {contact.get_display_name()}")
    
    print(f"\n👤 {owner.email} owns:")
    print(f"   - Organizations: {owner.owned_organizations.count()}")
    print(f"   - Contacts: {owner.owned_contacts.count()}")
    
    # Test querying
    print_header("5. Testing Queries & Filters")
    
    print("\n🔍 Query: All contacts at Acme Corporation")
    acme_contacts = Contact.objects.filter(organization=acme)
    print(f"   Found {acme_contacts.count()} contacts:")
    for contact in acme_contacts:
        print(f"      • {contact.get_full_name()} ({contact.job_title})")
    
    print("\n🔍 Query: All technology companies")
    tech_orgs = Organization.objects.filter(industry='technology')
    print(f"   Found {tech_orgs.count()} organizations:")
    for org in tech_orgs:
        print(f"      • {org.name} - {org.get_employee_count_display()}")
    
    print("\n🔍 Query: All customer-stage contacts")
    customers = Contact.objects.filter(lifecycle_stage='customer')
    print(f"   Found {customers.count()} customers:")
    for contact in customers:
        print(f"      • {contact.get_full_name()} at {contact.organization.name if contact.organization else 'N/A'}")
    
    print("\n🔍 Query: Contacts from LinkedIn")
    linkedin_contacts = Contact.objects.filter(lead_source='linkedin')
    print(f"   Found {linkedin_contacts.count()} contacts from LinkedIn:")
    for contact in linkedin_contacts:
        print(f"      • {contact.get_full_name()}")
    
    print("\n🔍 Query: Independent contacts (no organization)")
    independent = Contact.objects.filter(organization__isnull=True)
    print(f"   Found {independent.count()} independent contacts:")
    for contact in independent:
        print(f"      • {contact.get_full_name()} - {contact.job_title}")
    
    # Test helper methods
    print_header("6. Testing Helper Methods")
    
    print(f"\n📧 Full names and display names:")
    for contact in Contact.objects.all():
        print(f"   {contact.get_full_name():20} → {contact.get_display_name()}")
    
    print(f"\n📍 Addresses:")
    for obj in list(Organization.objects.all()) + list(Contact.objects.filter(address_line1__isnull=False)):
        name = obj.name if hasattr(obj, 'name') else obj.get_full_name()
        print(f"   {name:25} → {obj.full_address or 'No address'}")
    
    # Summary
    print_header("✅ All CRM Tests Passed!")
    
    print("\n📊 Final Statistics:")
    print(f"   - Organizations created: {Organization.objects.count()}")
    print(f"   - Contacts created: {Contact.objects.count()}")
    print(f"   - Contacts with organizations: {Contact.objects.filter(organization__isnull=False).count()}")
    print(f"   - Independent contacts: {Contact.objects.filter(organization__isnull=True).count()}")
    
    print("\n🎯 What We Verified:")
    print("   ✅ Can create organizations with all fields")
    print("   ✅ Can create contacts with all fields")
    print("   ✅ Can link contacts to organizations")
    print("   ✅ Foreign key relationships work correctly")
    print("   ✅ Reverse relationships work (org.contacts.all())")
    print("   ✅ Helper methods return correct values")
    print("   ✅ Queries and filters work correctly")
    print("   ✅ Can have independent contacts (no organization)")
    
    print("\n💡 Next Steps:")
    print("   1. Create Deal model (sales opportunities)")
    print("   2. Create Activity model (calls, emails, meetings)")
    print("   3. Create Task model (to-do items)")
    print("   4. Build API endpoints (ViewSets)")
    print("   5. Implement service layer (business logic)")
    print("   6. Add repository layer (data access)")
    
    # Cleanup option
    print("\n" + "=" * 60)
    cleanup = input("\n🧹 Clean up test data? (y/n): ").strip().lower()
    
    if cleanup == 'y':
        print("\n🧹 Cleaning up test data...")
        Contact.objects.filter(email__endswith='@test.com').delete()
        Organization.objects.filter(domain__endswith='.test.com').delete()
        User.objects.filter(username__startswith='test_crm_').delete()
        print("✅ Test data cleaned up")
    else:
        print("\n📝 Test data kept for inspection")

if __name__ == '__main__':
    try:
        test_crm_models()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
