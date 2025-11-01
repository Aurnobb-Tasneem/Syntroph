# Syntroph CRM - Docker Quick Start

This guide will help you get Syntroph CRM running with Docker.

## Prerequisites

- Docker Desktop installed
- Docker Compose installed
- 4GB+ RAM available

## Quick Start

1. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Run initial migrations**
   ```bash
   docker-compose exec api python manage.py migrate
   ```

4. **Create admin user**
   ```bash
   docker-compose exec api python manage.py createsuperuser
   ```

5. **Access applications**
   - Web: http://localhost:3000
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin

## Services

| Service | Port | Description |
|---------|------|-------------|
| web | 3000 | Next.js web application |
| api | 8000 | Django REST API |
| postgres | 5432 | PostgreSQL database |
| redis | 6379 | Redis cache |

## Common Commands

### View logs
```bash
docker-compose logs -f [service-name]
```

### Restart a service
```bash
docker-compose restart [service-name]
```

### Stop all services
```bash
docker-compose down
```

### Rebuild containers
```bash
docker-compose build
docker-compose up -d
```

### Access Django shell
```bash
docker-compose exec api python manage.py shell
```

### Run tests
```bash
docker-compose exec api pytest
```

## Troubleshooting

### Port already in use
Change the port mapping in `docker-compose.yml`

### Database connection issues
Check that PostgreSQL is healthy:
```bash
docker-compose ps postgres
```

### Container won't start
Check logs:
```bash
docker-compose logs [service-name]
```

## Next Steps

1. Configure integrations in `.env`
2. Create CRM models and endpoints
3. Build web UI components
4. Set up CI/CD pipeline

---

## ⚠️ IMPORTANT: Data Persistence

### ✅ YOUR DATA IS SAFE!

**Question**: Does my data vanish when Docker is stopped or crashed?

**Answer**: **NO!** Your data is stored in **Docker Volumes** which persist on your hard drive.

### How It Works

Your `docker-compose.yml` defines persistent volumes:

```yaml
volumes:
  postgres-data:  # PostgreSQL data persists here
  redis-data:     # Redis data persists here
```

### Safe Operations (Data is Preserved)

✅ **These commands keep your data:**
```bash
docker-compose down              # Stops containers, KEEPS data
docker-compose stop              # Stops containers, KEEPS data
docker stop syntroph-postgres    # Stops container, KEEPS data
```

✅ **These events keep your data:**
- Shutting down your PC
- Docker Desktop crash
- Windows restart
- Container crashes

### Dangerous Operations (Data Loss)

❌ **Only these will DELETE your data:**
```bash
docker-compose down -v           # The -v flag DELETES volumes
docker volume rm syntroph_postgres-data  # Explicit deletion
```

### Where Is Your Data Stored?

**Windows Location**:
```
C:\ProgramData\Docker\volumes\
├── syntroph_postgres-data\_data\  ← Your database is here
└── syntroph_redis-data\_data\     ← Your Redis data is here
```

This data persists even when:
- Docker is stopped
- Containers are removed
- Your PC is shut down

### Verifying Data After Restart

```bash
# Start Docker services
docker-compose up -d postgres redis

# Check your data is still there
cd apps/api
python check_postgres_db.py
```

You'll see all your:
- ✅ Tenants
- ✅ Users
- ✅ Contacts, Organizations, Deals
- ✅ Database schemas

### Backup Strategy (Recommended)

Even though volumes persist, regular backups are good practice:

```bash
# Create PostgreSQL backup
docker exec syntroph-postgres pg_dump -U syntroph_user syntroph_crm > backup_$(date +%Y%m%d).sql

# Restore from backup
docker exec -i syntroph-postgres psql -U syntroph_user syntroph_crm < backup_20251101.sql
```

### Summary

| Action | Data Status |
|--------|-------------|
| `docker-compose down` | ✅ **SAFE** - Data preserved |
| `docker-compose stop` | ✅ **SAFE** - Data preserved |
| Shutdown PC | ✅ **SAFE** - Data preserved |
| Docker crash | ✅ **SAFE** - Data preserved |
| `docker-compose down -v` | ❌ **DANGER** - Data deleted |
| Delete volume manually | ❌ **DANGER** - Data deleted |

**Your data is safe unless you explicitly delete volumes with `-v` flag!**

---

**Need help?** Open an issue on GitHub.
