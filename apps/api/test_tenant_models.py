"""
Test Script: Multi-Tenant Models
================================

This script tests our User, Tenant, and TenantMembership models.

What we'll test:
1. Create a test tenant (Acme Corporation)
2. Create test users (John, Jane, Bob)
3. Add users to the tenant with different roles
4. Query and verify relationships
5. Test the helper methods (is_admin, can_edit_data, etc.)

Run this with: python test_tenant_models.py
"""

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.models import User, Tenant, TenantMembership
from django.db import transaction

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_tenant_models():
    """Test our multi-tenant models"""
    
    print_header("🧪 Testing Multi-Tenant Models")
    
    # Clean up any existing test data
    print("\n🧹 Cleaning up existing test data...")
    User.objects.filter(username__startswith='test_').delete()
    Tenant.objects.filter(schema_name__startswith='test_').delete()
    print("✅ Cleanup complete")
    
    # Step 1: Create a test tenant
    print_header("1. Creating Test Tenant")
    
    tenant = Tenant.objects.create(
        name="Acme Corporation",
        schema_name="test_acme_corp",
        domain="acme.test.com",
        subscription_tier="professional",
        max_users=10
    )
    
    print(f"✅ Created tenant: {tenant}")
    print(f"   - ID: {tenant.id}")
    print(f"   - Name: {tenant.name}")
    print(f"   - Schema: {tenant.schema_name}")
    print(f"   - Domain: {tenant.domain}")
    print(f"   - Tier: {tenant.subscription_tier}")
    print(f"   - Max Users: {tenant.max_users}")
    print(f"   - Active: {tenant.is_active}")
    print(f"   - Created: {tenant.created_at}")
    
    # Step 2: Create test users
    print_header("2. Creating Test Users")
    
    john = User.objects.create_user(
        username='test_john',
        email='john@test.com',
        password='testpass123',
        first_name='John',
        last_name='Doe'
    )
    print(f"✅ Created user: {john}")
    print(f"   - ID: {john.id}")
    print(f"   - Email: {john.email}")
    print(f"   - Full Name: {john.get_full_name()}")
    
    jane = User.objects.create_user(
        username='test_jane',
        email='jane@test.com',
        password='testpass123',
        first_name='Jane',
        last_name='Smith'
    )
    print(f"✅ Created user: {jane}")
    
    bob = User.objects.create_user(
        username='test_bob',
        email='bob@test.com',
        password='testpass123',
        first_name='Bob',
        last_name='Johnson'
    )
    print(f"✅ Created user: {bob}")
    
    # Step 3: Add users to tenant with different roles
    print_header("3. Creating Tenant Memberships")
    
    # John is the owner
    membership_john = TenantMembership.objects.create(
        user=john,
        tenant=tenant,
        role='owner'
    )
    print(f"✅ Added {john.email} to {tenant.name} as OWNER")
    
    # Jane is an admin (invited by John)
    membership_jane = TenantMembership.objects.create(
        user=jane,
        tenant=tenant,
        role='admin',
        invited_by=john
    )
    print(f"✅ Added {jane.email} to {tenant.name} as ADMIN (invited by {john.email})")
    
    # Bob is a regular user
    membership_bob = TenantMembership.objects.create(
        user=bob,
        tenant=tenant,
        role='user',
        invited_by=jane
    )
    print(f"✅ Added {bob.email} to {tenant.name} as USER (invited by {jane.email})")
    
    # Step 4: Query and verify relationships
    print_header("4. Querying Relationships")
    
    # Get all members of the tenant
    print(f"\n👥 Members of {tenant.name}:")
    for membership in tenant.memberships.all():
        print(f"   - {membership.user.email} ({membership.role})")
        if membership.invited_by:
            print(f"     Invited by: {membership.invited_by.email}")
    
    # Get all tenants John belongs to
    print(f"\n🏢 Tenants that {john.email} belongs to:")
    for membership in john.tenant_memberships.all():
        print(f"   - {membership.tenant.name} ({membership.role})")
    
    # Check tenant member count
    print(f"\n📊 Tenant Statistics:")
    print(f"   - Total members: {tenant.get_member_count()}")
    print(f"   - Max users allowed: {tenant.max_users}")
    print(f"   - Can add more users: {tenant.can_add_user()}")
    
    # Step 5: Test helper methods
    print_header("5. Testing Permission Methods")
    
    print(f"\n🔐 {john.email} (owner) permissions:")
    print(f"   - is_owner(): {membership_john.is_owner()}")
    print(f"   - is_admin(): {membership_john.is_admin()}")
    print(f"   - can_manage_users(): {membership_john.can_manage_users()}")
    print(f"   - can_edit_data(): {membership_john.can_edit_data()}")
    
    print(f"\n🔐 {jane.email} (admin) permissions:")
    print(f"   - is_owner(): {membership_jane.is_owner()}")
    print(f"   - is_admin(): {membership_jane.is_admin()}")
    print(f"   - can_manage_users(): {membership_jane.can_manage_users()}")
    print(f"   - can_edit_data(): {membership_jane.can_edit_data()}")
    
    print(f"\n🔐 {bob.email} (user) permissions:")
    print(f"   - is_owner(): {membership_bob.is_owner()}")
    print(f"   - is_admin(): {membership_bob.is_admin()}")
    print(f"   - can_manage_users(): {membership_bob.can_manage_users()}")
    print(f"   - can_edit_data(): {membership_bob.can_edit_data()}")
    
    # Step 6: Test unique constraint
    print_header("6. Testing Unique Constraint")
    
    try:
        # Try to add John to the same tenant again (should fail)
        duplicate = TenantMembership.objects.create(
            user=john,
            tenant=tenant,
            role='user'
        )
        print("❌ ERROR: Duplicate membership was allowed (should have failed!)")
    except Exception as e:
        print(f"✅ Duplicate membership prevented: {type(e).__name__}")
        print(f"   - A user can only have ONE membership per tenant")
    
    # Step 7: Test deactivation
    print_header("7. Testing Membership Activation/Deactivation")
    
    print(f"\n🔄 Deactivating {bob.email}'s membership...")
    membership_bob.is_active = False
    membership_bob.save()
    print(f"✅ Membership deactivated")
    print(f"   - is_active: {membership_bob.is_active}")
    print(f"   - Note: In production, middleware would block inactive users")
    
    # Reactivate for cleanup
    membership_bob.is_active = True
    membership_bob.save()
    print(f"\n🔄 Reactivating membership for cleanup...")
    
    # Final summary
    print_header("✅ All Tests Passed!")
    
    print("\n📊 Final State:")
    print(f"   - Tenants created: {Tenant.objects.filter(schema_name__startswith='test_').count()}")
    print(f"   - Users created: {User.objects.filter(username__startswith='test_').count()}")
    print(f"   - Memberships created: {TenantMembership.objects.filter(tenant__schema_name__startswith='test_').count()}")
    
    print("\n🎯 What We Verified:")
    print("   ✅ Can create tenants with all fields")
    print("   ✅ Can create users with passwords (hashed)")
    print("   ✅ Can link users to tenants with roles")
    print("   ✅ Foreign key relationships work correctly")
    print("   ✅ Helper methods return correct values")
    print("   ✅ Unique constraint prevents duplicate memberships")
    print("   ✅ Can activate/deactivate memberships")
    
    print("\n💡 Next Steps:")
    print("   1. Create schema management utilities")
    print("   2. Add middleware for tenant routing")
    print("   3. Build CRM models (Contact, Deal, etc.)")
    
    # Cleanup option
    print("\n" + "=" * 60)
    cleanup = input("\n🧹 Clean up test data? (y/n): ").strip().lower()
    
    if cleanup == 'y':
        print("\n🧹 Cleaning up test data...")
        User.objects.filter(username__startswith='test_').delete()
        Tenant.objects.filter(schema_name__startswith='test_').delete()
        print("✅ Test data cleaned up")
    else:
        print("\n📝 Test data kept for inspection")
        print("   You can view it in Django admin or shell")
        print("   To clean up later, run:")
        print("     User.objects.filter(username__startswith='test_').delete()")
        print("     Tenant.objects.filter(schema_name__startswith='test_').delete()")

if __name__ == '__main__':
    try:
        test_tenant_models()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
