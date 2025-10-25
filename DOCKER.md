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

**Need help?** Open an issue on GitHub.
