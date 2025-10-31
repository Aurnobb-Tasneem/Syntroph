import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.models import Tenant, User
from core.utils import SchemaManager

print('🧹 Cleaning all test data...')

# Drop test schemas
for tenant in Tenant.objects.all():
    if 'test' in tenant.schema_name or tenant.schema_name in ['acme_corp', 'techstart_inc']:
        print(f'   Dropping schema: {tenant.schema_name}')
        SchemaManager.drop_tenant_schema(tenant.schema_name)
        tenant.delete()

# Delete test users
User.objects.filter(username__startswith='test_').delete()

print('✅ Cleanup complete')
