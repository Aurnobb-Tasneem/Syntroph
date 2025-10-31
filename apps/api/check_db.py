"""
Check database tables created by Django migrations
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

# Get database tables
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print("📋 Database Tables Created:")
print("=" * 50)
for table in tables:
    print(f"✅ {table[0]}")

print("\n" + "=" * 50)
print(f"Total: {len(tables)} tables")

# Check if users table exists and has the correct structure
print("\n🔍 Users Table Structure:")
print("=" * 50)
cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()

for col in columns:
    col_id, name, col_type, not_null, default, pk = col
    pk_marker = " (PRIMARY KEY)" if pk else ""
    null_marker = " NOT NULL" if not_null else ""
    print(f"  {name}: {col_type}{pk_marker}{null_marker}")
