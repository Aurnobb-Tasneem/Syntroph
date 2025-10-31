"""
Check PostgreSQL Database Structure
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

print("\n" + "=" * 60)
print("  📊 PostgreSQL Database Structure")
print("=" * 60)

with connection.cursor() as cursor:
    # List all tables in public schema
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    
    print(f"\n🗄️  PUBLIC SCHEMA (Global Data) - {len(tables)} tables:")
    print("=" * 60)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"   ✅ {table[0]:<35} ({count} rows)")
    
    # List all schemas
    cursor.execute("""
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
        ORDER BY schema_name;
    """)
    schemas = cursor.fetchall()
    
    print(f"\n🏢 ALL SCHEMAS - {len(schemas)} total:")
    print("=" * 60)
    for schema in schemas:
        print(f"   📁 {schema[0]}")
    
    print("\n" + "=" * 60)
    print("✅ Database Ready for Multi-Tenant CRM!")
    print("=" * 60)
    
    print("\n💡 What's Next:")
    print("   1. Create a tenant → Automatic schema creation")
    print("   2. Add users to tenant → User-tenant relationships")
    print("   3. Create contacts/orgs → Data in tenant schema")
    print("   4. Middleware routes requests → Automatic isolation")
