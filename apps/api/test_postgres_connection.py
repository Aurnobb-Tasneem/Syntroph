"""
Test PostgreSQL Connection
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

print("\n" + "=" * 60)
print("  🐘 PostgreSQL Connection Test")
print("=" * 60)

try:
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    
    print(f"\n✅ Successfully connected to PostgreSQL!")
    print(f"\n📊 Connection Details:")
    print(f"   Engine: {connection.settings_dict['ENGINE']}")
    print(f"   Database: {connection.settings_dict['NAME']}")
    print(f"   Host: {connection.settings_dict['HOST']}")
    print(f"   Port: {connection.settings_dict['PORT']}")
    print(f"   User: {connection.settings_dict['USER']}")
    
    print(f"\n🎯 PostgreSQL Version:")
    print(f"   {version}")
    
    print("\n" + "=" * 60)
    print("✅ Ready to run migrations!")
    print("=" * 60 + "\n")
    
except Exception as e:
    print(f"\n❌ Connection failed: {e}\n")
    print("💡 Make sure:")
    print("   1. Docker containers are running (docker ps)")
    print("   2. .env file has correct DATABASE_URL")
    print("   3. PostgreSQL is accepting connections on port 5432")
