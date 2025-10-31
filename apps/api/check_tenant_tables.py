"""
Check the structure of Tenant and TenantMembership tables
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

def show_table_structure(table_name):
    """Display the structure of a database table"""
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print(f"\n{'=' * 60}")
    print(f"📋 Table: {table_name}")
    print('=' * 60)
    
    for col in columns:
        col_id, name, col_type, not_null, default, pk = col
        markers = []
        if pk:
            markers.append("PRIMARY KEY")
        if not_null and not pk:
            markers.append("NOT NULL")
        if default:
            markers.append(f"DEFAULT {default}")
        
        marker_str = f" ({', '.join(markers)})" if markers else ""
        print(f"  ✓ {name:<20} {col_type:<15} {marker_str}")

# Show structure of our new tables
show_table_structure('tenants')
show_table_structure('tenant_memberships')

print("\n" + "=" * 60)
print("✅ Multi-Tenant Database Structure Complete!")
print("=" * 60)
