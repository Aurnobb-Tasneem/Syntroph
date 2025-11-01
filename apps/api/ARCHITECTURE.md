# Multi-Tenant Architecture - Development Guide

## 🏗️ Architecture Overview

### Schema Separation

**PUBLIC Schema** (Shared across all tenants):
```
📁 public/
  ├── tenants          ← Tenant registry
  ├── auth_*           ← Django auth system tables
  ├── django_*         ← Django system tables
  └── [NO CRM DATA]    ← Users/Contacts/Deals are NOT here!
```

**TENANT Schemas** (Isolated per tenant):
```
📁 tenant_acme/
  ├── users            ← Acme employees only
  ├── contacts         ← Acme CRM contacts
  ├── organizations    ← Acme CRM companies
  └── deals            ← Acme sales pipeline

📁 tenant_techstart/
  ├── users            ← TechStart employees only
  ├── contacts         ← TechStart CRM contacts
  ├── organizations    ← TechStart CRM companies
  └── deals            ← TechStart sales pipeline
```

## 📝 Key Concepts

### User Model Location
- ❌ **OLD**: User in `core.models` (public schema)
- ✅ **NEW**: User in `crm.models` (tenant schema)

### Tenant Membership
- ❌ **OLD**: TenantMembership table linking users to tenants
- ✅ **NEW**: Users exist ONLY in their tenant's schema

### Signup Flow
- ❌ **OLD**: User creates account → joins tenant
- ✅ **NEW**: Signup creates tenant + schema + owner user

### User Creation
- ❌ **OLD**: Users can self-register
- ✅ **NEW**: Only admins can create users (like NSU IT!)

## 🚀 Development Workflows

### 1. Creating a New Tenant

```bash
cd apps/api/scripts
python create_tenant.py

# Interactive prompts:
Company Name: Acme Corporation
Subdomain: acme
Owner Email: admin@acme.com
Owner Password: SecurePass123!
Owner First Name: John
Owner Last Name: Doe

# This creates:
# 1. Tenant record in PUBLIC schema
# 2. tenant_acme PostgreSQL schema
# 3. Tables: users, contacts, organizations, deals
# 4. Owner user in tenant_acme.users
```

### 2. Checking Database Structure

```bash
cd apps/api/scripts

# View all schemas and tables
python check_postgres_db.py

# View specific tenant's data
python check_tenant_tables.py acme
```

### 3. Creating Test Scripts

**✅ DO THIS:**
```bash
# Create scripts in the scripts/ folder
cd apps/api/scripts
touch my_test_script.py
```

**❌ DON'T DO THIS:**
```bash
# Don't create scripts in main codebase
cd apps/api
touch my_test_script.py  # ❌ Wrong!
```

### 4. Clean Database Reset

```bash
cd apps/api/scripts

# WARNING: This deletes EVERYTHING!
python drop_all_tables.py

# Then recreate structure
cd ..
python manage.py migrate
```

## 🔐 User Roles

### Role Hierarchy
1. **OWNER** - Created during signup, full control
2. **ADMIN** - Can manage users and settings
3. **MANAGER** - Can view all data, manage team
4. **SALESPERSON** - Can manage own contacts/deals

### Permissions
```python
user.is_owner()           # True for owner
user.is_admin_or_owner()  # True for owner/admin
user.can_create_users()   # True for owner/admin
user.can_manage_users()   # True for owner/admin
user.can_view_all_data()  # True for owner/admin/manager
```

## 📊 Database Queries

### Querying Users (Tenant-Specific)

```python
from crm.models import User

# In tenant context (middleware sets schema)
users = User.objects.all()  # Gets users from current tenant only

# Users in tenant_acme cannot see users in tenant_techstart
```

### Querying Across Schemas (Admin Only)

```python
from django.db import connection
from core.utils import SchemaManager

# Switch to specific tenant
with connection.cursor() as cursor:
    cursor.execute("SET search_path TO tenant_acme, public")
    users = User.objects.all()  # Now queries tenant_acme
```

## 🛠️ Common Tasks

### Adding a New CRM Model

1. Create model in `crm/models/`
2. Model will auto-create in tenant schemas
3. Run migrations (applies to all existing tenants)

```python
# crm/models/activity.py
class Activity(models.Model):
    # This will exist in tenant schemas, not public
    pass
```

### Middleware Flow

```
1. Request arrives at: acme.syntroph.com
2. Middleware extracts subdomain: "acme"
3. Find tenant: Tenant.objects.get(domain="acme")
4. Set schema: connection.set_schema("tenant_acme")
5. All queries now hit tenant_acme schema
6. User can only see their tenant's data
```

## ⚠️ Important Rules

### ✅ DO:
- Create all test scripts in `apps/api/scripts/`
- Use tenant-specific queries for CRM data
- Create users only through admin interface
- Test tenant isolation regularly

### ❌ DON'T:
- Put CRM models in public schema
- Allow users to self-register
- Create test scripts outside scripts/ folder
- Bypass tenant middleware

## 📁 File Organization

```
apps/api/
├── core/
│   ├── models.py          ← Tenant model ONLY
│   ├── middleware.py      ← Tenant routing
│   ├── db_router.py       ← Schema routing
│   └── utils.py           ← Schema management
├── crm/
│   └── models/
│       ├── user.py        ← User model (tenant schema)
│       ├── contact.py     ← Contact model (tenant schema)
│       ├── organization.py ← Org model (tenant schema)
│       └── deal.py        ← Deal model (tenant schema)
├── scripts/               ← All test/utility scripts (gitignored)
│   ├── create_tenant.py
│   ├── check_postgres_db.py
│   └── test_*.py
└── backup/                ← Backup files (gitignored)
```

## 🧪 Testing Tenant Isolation

```bash
cd apps/api/scripts

# Create two tenants
python create_tenant.py  # Create acme
python create_tenant.py  # Create techstart

# Verify isolation
python test_tenant_isolation.py  # TODO: Create this script
```

## 🔄 Migration Strategy

### For Existing Tenants
When you create a new model:
1. Run `python manage.py makemigrations`
2. For each existing tenant, run migrations in their schema
3. New tenants will get tables automatically

### Example
```python
from core.models import Tenant
from django.db import connection

for tenant in Tenant.objects.all():
    schema = f"tenant_{tenant.schema_name}"
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {schema}, public")
        # Run migrations here
```

## 📞 Getting Help

If you're unsure:
1. Check this guide
2. Look at `scripts/README.md`
3. Review test scripts for examples
4. Ask team members

---

**Last Updated**: November 2, 2025  
**Architecture Version**: 2.0 (Schema-Per-Tenant)
