# Syntroph CRM

A modern, full-stack CRM platform built for enterprise-grade customer relationship management.

## 🏗️ Architecture

- **Backend**: Django 5.2 with Django REST Framework
- **Web Frontend**: Next.js 16 with React 19
- **Mobile**: Kotlin (Android) - *Coming Soon*
- **Database**: PostgreSQL 16
- **Cache/Queue**: Redis 7
- **MCP Server**: Model Context Protocol integration - *Planned*
- **Type Safety**: oRPC for end-to-end type safety
- **Monorepo**: Turborepo with pnpm workspaces
- **Code Quality**: Biome for linting and formatting

## 🚀 Features

### Current
- Monorepo setup with Turborepo
- Docker containerization for all services
- Django REST API with PostgreSQL
- Next.js web application
- Redis caching layer

### Planned Integrations
- 📧 Email integration (SMTP/SendGrid)
- 💼 LinkedIn API integration
- 💬 Slack workspace integration
- 📞 VOIP service integration
- 🤖 MCP (Model Context Protocol) server for AI capabilities
- 📱 Kotlin mobile application

## 🛠️ Tech Stack

### Backend
- Django 5.2
- Django REST Framework
- PostgreSQL 16
- Redis 7
- Celery (planned for async tasks)
- JWT Authentication

### Frontend
- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS 4
- oRPC for type-safe API calls

### DevOps
- Docker & Docker Compose
- Turborepo
- Biome (linting & formatting)
- GitHub Actions (CI/CD) - *Coming Soon*

## 📦 Project Structure

```
Syntroph/
├── apps/
│   ├── api/              # Django backend
│   ├── web/              # Next.js web app
│   └── mobile/           # Kotlin mobile app (planned)
├── packages/
│   ├── config/           # Shared configs
│   ├── ui/               # Shared UI components
│   ├── utils/            # Shared utilities
│   └── typescript-config/ # Shared TS configs
└── docker-compose.yml    # Multi-service orchestration
```

## 🚦 Getting Started

### Prerequisites

- Node.js >= 18
- Python >= 3.12
- Docker & Docker Compose
- pnpm >= 9.0.0

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aurnobb-Tasneem/Syntroph.git
   cd Syntroph
   ```

2. **Install dependencies**
   ```bash
   # Install Node dependencies
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start with Docker (Recommended)**
   ```bash
   # Build and start all services
   pnpm docker:up

   # Run database migrations
   pnpm api:migrate

   # Create Django superuser
   pnpm api:createsuperuser
   ```

5. **Access the applications**
   - Web App: http://localhost:3000
   - API: http://localhost:8000
   - API Admin: http://localhost:8000/admin
   - API Docs: http://localhost:8000/api/docs

### Development

**Run all services:**
```bash
pnpm dev
```

**Run specific service:**
```bash
# Web only
pnpm dev:web

# API only (without Docker)
pnpm dev:api
```

**Docker commands:**
```bash
# View logs
pnpm docker:logs

# Stop services
pnpm docker:down

# Rebuild containers
pnpm docker:build
```

## 🧪 Testing

```bash
# Run all tests
pnpm test

# Run API tests
cd apps/api && pytest
```

## 📝 Code Quality

```bash
# Lint all projects
pnpm lint

# Format code
pnpm format

# Type check
pnpm check-types
```

## 🗂️ Database Management

```bash
# Create migrations
pnpm api:makemigrations

# Apply migrations
pnpm api:migrate

# Access Django shell
pnpm api:shell
```

## 🤝 Contributing

We welcome contributions! This is an open collaboration project.

### Guidelines
1. Follow the existing code structure
2. Use Biome for formatting
3. Write tests for new features
4. Update documentation as needed
5. Add descriptive comments for complex logic
6. Keep commits atomic and well-described

### Development Workflow
1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📋 Roadmap

### Phase 1: Core Setup ✅
- [x] Monorepo structure
- [x] Docker configuration
- [x] Django API setup
- [x] Next.js web app
- [x] PostgreSQL integration

### Phase 2: Core CRM Features (In Progress)
- [ ] Contact management
- [ ] Company management
- [ ] Deal pipeline
- [ ] Activity tracking
- [ ] User authentication

### Phase 3: Integrations
- [ ] LinkedIn API
- [ ] Email integration
- [ ] Slack integration
- [ ] VOIP service
- [ ] Calendar sync

### Phase 4: Advanced Features
- [ ] MCP server for AI features
- [ ] Mobile app (Kotlin)
- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] Custom workflows

## 📄 License

[MIT License](LICENSE)

## 🙋‍♂️ Support

For questions and support, please open an issue on GitHub.

---

**Built with ❤️ for open collaboration**
