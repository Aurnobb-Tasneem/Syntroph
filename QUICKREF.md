# Syntroph CRM - Quick Reference

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/Aurnobb-Tasneem/Syntroph.git
cd Syntroph
./setup.sh  # or setup.ps1 on Windows

# Create admin user
pnpm api:createsuperuser

# Access the app
# Web: http://localhost:3000
# API: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## 📋 Common Commands

### Development
```bash
pnpm dev              # Start all services
pnpm dev:web          # Web only
pnpm dev:api          # API only
```

### Docker
```bash
pnpm docker:up        # Start containers
pnpm docker:down      # Stop containers
pnpm docker:logs      # View logs
pnpm docker:build     # Rebuild images
```

### Database
```bash
pnpm api:migrate           # Run migrations
pnpm api:makemigrations    # Create migrations
pnpm api:shell             # Django shell
```

### Code Quality
```bash
pnpm lint             # Run linters
pnpm format           # Format code
pnpm check-types      # Type check
pnpm test             # Run tests
```

## 🏗️ Project Structure

```
Syntroph/
├── apps/
│   ├── api/              # Django REST API
│   │   ├── core/         # Django settings
│   │   ├── crm/          # CRM apps (contacts, deals, etc.)
│   │   └── integrations/ # Third-party integrations
│   ├── web/              # Next.js web app
│   └── mcp-server/       # AI server (planned)
├── packages/
│   ├── ui/               # Shared UI components
│   ├── utils/            # Shared utilities
│   └── typescript-config/ # Shared TS configs
└── docker-compose.yml    # Service orchestration
```

## 🔧 Environment Variables

Key variables in `.env`:

```bash
# Database
POSTGRES_PASSWORD=your_password
DATABASE_URL=postgresql://...

# Django
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True

# Next.js
NEXT_PUBLIC_API_URL=http://localhost:8000

# Integrations (optional)
LINKEDIN_CLIENT_ID=...
SLACK_BOT_TOKEN=...
```

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| web | 3000 | Next.js web app |
| api | 8000 | Django REST API |
| postgres | 5432 | PostgreSQL 16 |
| redis | 6379 | Redis cache |

## 📚 API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/register` - Register

### Contacts (planned)
- `GET /api/contacts/` - List contacts
- `POST /api/contacts/` - Create contact
- `GET /api/contacts/{id}/` - Get contact
- `PUT /api/contacts/{id}/` - Update contact
- `DELETE /api/contacts/{id}/` - Delete contact

### Documentation
- `GET /api/docs/` - API documentation (Swagger)
- `GET /api/schema/` - OpenAPI schema

## 🧪 Testing

### Django Tests
```bash
cd apps/api
pytest
pytest --cov=.
```

### Web Tests
```bash
pnpm test --filter=web
```

## 🔍 Debugging

### View Docker logs
```bash
docker-compose logs -f [service-name]
```

### Access containers
```bash
docker-compose exec api bash
docker-compose exec web sh
docker-compose exec postgres psql -U syntroph_user -d syntroph_crm
```

### Django debug
```bash
# In Django shell
pnpm api:shell

# Use ipdb for debugging
import ipdb; ipdb.set_trace()
```

## 🚨 Troubleshooting

### Port already in use
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

### Database issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d
pnpm api:migrate
```

### Node modules issues
```bash
rm -rf node_modules
pnpm install
```

### Python dependencies
```bash
docker-compose exec api pip install -r requirements.txt
```

## 📖 Documentation Files

- `README.md` - Project overview
- `DOCKER.md` - Docker guide
- `CONTRIBUTING.md` - How to contribute
- `ISSUES.md` - Linear/GitHub issues
- `CHANGELOG.md` - Version history

## 🔗 Useful Links

- Repository: https://github.com/Aurnobb-Tasneem/Syntroph
- Issues: https://github.com/Aurnobb-Tasneem/Syntroph/issues
- Django Docs: https://docs.djangoproject.com/
- Next.js Docs: https://nextjs.org/docs
- Turborepo Docs: https://turbo.build/repo/docs

## 💡 Tips

1. Use `pnpm` instead of `npm` for package management
2. Always run migrations after pulling changes
3. Keep `.env` file updated with team values
4. Use Docker for consistent development environment
5. Run `pnpm format` before committing
6. Write tests for new features
7. Add open collaboration comments for complex code

## 🤝 Getting Help

- Check documentation first
- Search existing issues
- Ask in GitHub Discussions
- Open a new issue with details

---

**Quick Reference Version:** 1.0  
**Last Updated:** October 26, 2025
