# Zyphron - Production-Ready Deployment Platform

A comprehensive, DevOps-oriented platform for deploying any repository (frontend, backend, full-stack) with minimal user interaction. Built with production-ready infrastructure, monitoring, and SRE capabilities.

## 🎯 Features

### Core Deployment
- **One-Click Deployment**: Upload repo and deploy with a single click
- **Intelligent Detection**: Automatic language, framework, and dependency detection
- **Multi-Service Support**: Frontend, Backend, Database, and any other services
- **Containerization**: Automatic Docker image generation and optimization
- **Testing Pipeline**: Integrated build, test, and validation pipeline

### DevOps & SRE
- **Uptime Monitoring**: 24/7 health checks and monitoring
- **Automatic Rollback**: Instant rollback on container failure
- **Custom Subdomains**: Deploy on custom subdomains (app1.zyphron.space)
- **SSL/TLS**: Automatic certificate management with Let's Encrypt
- **Performance Metrics**: Real-time monitoring and analytics

### Multi-Language Support
- **Frontend**: React, Vue, Next.js, Angular, Svelte, etc.
- **Backend**: Python, Node.js, Go, Java, Rust, C#, PHP, etc.
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, etc.

### Security & Access Control
- **Role-Based Access**: Fine-grained user permissions
- **Secure Credentials**: Encrypted environment variable storage
- **Session Management**: JWT-based authentication

## 📁 Project Structure

```
zyphron/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── core/              # Configuration, security
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── api/               # API routes
│   │   ├── services/          # Business logic
│   │   │   ├── deployment/    # Deployment engine
│   │   │   ├── detection/     # Language/framework detection
│   │   │   ├── monitoring/    # Health checks, uptime
│   │   │   ├── docker/        # Docker operations
│   │   │   ├── subdomain/     # Subdomain management
│   │   │   └── notification/  # WebSocket, email notifications
│   │   └── main.py            # FastAPI app
│   ├── tests/                 # Unit and integration tests
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend container
│   └── .env.example           # Example environment variables
│
├── frontend/                  # Next.js application
│   ├── app/
│   │   ├── auth/              # Authentication pages
│   │   ├── dashboard/         # User dashboard
│   │   ├── deployments/       # Deployment management
│   │   ├── monitoring/        # Monitoring & stats
│   │   └── layout.tsx         # Main layout
│   ├── components/
│   │   ├── auth/              # Auth components
│   │   ├── forms/             # Forms
│   │   ├── charts/            # Charts & metrics
│   │   └── common/            # Reusable components
│   ├── hooks/                 # Custom React hooks
│   ├── services/              # API client services
│   ├── context/               # Context API for state
│   ├── types/                 # TypeScript types
│   ├── package.json           # Node dependencies
│   ├── Dockerfile             # Frontend container
│   └── .env.local.example     # Example env vars
│
├── docker/
│   ├── Dockerfile.template    # Template for user repos
│   ├── docker-compose.yml     # Multi-container orchestration
│   └── nginx/                 # Nginx configs
│
├── infrastructure/
│   ├── nginx.conf             # Nginx reverse proxy
│   ├── docker-compose.prod.yml# Production setup
│   ├── backup/                # Backup scripts
│   └── monitoring/            # Monitoring setup
│
├── scripts/
│   ├── setup.sh               # Initial setup
│   ├── deploy.sh              # Deployment helper
│   ├── migrate.sh             # Database migrations
│   └── health-check.sh        # Health check script
│
├── docs/
│   ├── ARCHITECTURE.md        # System design
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── API.md                 # API documentation
│   ├── LANGUAGE_SUPPORT.md    # Supported languages
│   └── SRE.md                 # SRE features guide
│
├── .github/
│   └── workflows/             # CI/CD pipelines
│
├── docker-compose.yml         # Local development
└── .env.example               # Main env file template
```

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT + OAuth2
- **Async**: asyncio + aiohttp
- **Validation**: Pydantic V2
- **Testing**: pytest

### Frontend
- **Framework**: Next.js (React)
- **Styling**: TailwindCSS + Shadcn/UI
- **State Management**: Zustand / Context API
- **API Client**: TanStack Query + Axios
- **Monitoring**: Sentry
- **Real-time**: WebSocket

### DevOps & Infrastructure
- **Containerization**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **SSL/TLS**: Certbot + Let's Encrypt
- **Monitoring**: Prometheus + Grafana (future)
- **Logging**: ELK Stack / Loki (future)
- **CI/CD**: GitHub Actions / GitLab CI

### Detection & Analysis
- **Language Detection**: Regex patterns + ML (future)
- **Dockerfile Generation**: Template-based system
- **Dependency Analysis**: ast + regex parsing

## 🚀 Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/zyphron.git
cd zyphron

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Update .env with your settings
python -m alembic upgrade head

# Setup frontend
cd ../frontend
npm install
cp .env.local.example .env.local

# Run local development
docker-compose up -d

# Access
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## 📊 System Architecture

### Deployment Flow
```
1. User uploads/connects repo
   ↓
2. Detect language, framework, dependencies
   ↓
3. Check subdomain availability
   ↓
4. Request environment variables if needed
   ↓
5. Build Docker image (with testing)
   ↓
6. Run tests & validations
   ↓
7. Push to container registry
   ↓
8. Deploy container(s)
   ↓
9. Configure nginx & SSL
   ↓
10. Start monitoring & health checks
   ↓
11. Live deployment accessible
```

### Multi-Container Architecture
```
For Full-Stack Apps:
- Frontend Container (React/Vue/etc)
  └─ Nginx Port 3000
- Backend Container (Node/Python/etc)
  └─ Service Port 5000/8000
- Database Container (PostgreSQL/MySQL/etc)
  └─ DB Port 5432/3306
- Redis Container (optional)
  └─ Cache Port 6379
  
All connected via Docker Network & Nginx Reverse Proxy
```

## 🔐 Security Considerations

1. **Environment Variables**: Encrypted storage with rotation
2. **Container Security**: Non-root user, minimal base images
3. **Network**: Internal networking, external via nginx
4. **SSL/TLS**: Always encrypted communication
5. **Rate Limiting**: API rate limiting to prevent abuse
6. **Secrets Management**: HashiCorp Vault integration (future)

## 📈 SRE Features Roadmap

- [x] Health checks & uptime monitoring
- [x] Automatic rollback system
- [x] Deployment logs & analytics
- [ ] Resource optimization (CPU, Memory)
- [ ] Auto-scaling (future)
- [ ] Distributed tracing
- [ ] Performance profiling
- [ ] Cost analytics
- [ ] Budget alerts

## 🌐 Deployment Orchestration (Future)

```
AWS (Main Orchestrator)
├─ Small repos < 500MB
├─ Main backend logic
└─ Route & balance traffic

GCP
└─ Mid-sized repos (500MB - 5GB)

Oracle VM
└─ Large repos > 5GB
```

## 🤝 Contributing

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - See LICENSE file

## 📧 Contact

For questions or support, reach out to: support@zyphron.space

---

**Built with ❤️ for the DevOps community**
