# Zyphron Architecture Documentation

## System Overview

Zyphron is a **production-ready deployment platform** that enables users to deploy any repository type with minimal configuration. The platform autodetects technologies, manages infrastructure, and provides comprehensive DevOps/SRE capabilities.

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Nginx Reverse  │
│     Proxy       │ (Subdomain routing, SSL/TLS, Load balancing)
└────┬────────┬───┘
     │        │
     ▼        ▼
┌─────────┐ ┌─────────────┐
│Frontend │ │   Backend   │
│Next.js  │ │   FastAPI   │
└────┬────┘ └─────┬───────┘
     │            │
     │     ┌──────┴────────┬─────────────┐
     │     ▼               ▼             ▼
     │ ┌────────┐    ┌─────────┐    ┌──────────┐
     │ │Database│    │  Redis  │    │ Docker   │
     │ │Postgres│    │ Cache   │    │ Daemon   │
     │ └────────┘    └─────────┘    └──────────┘
     │
     └───────────► User's Deployed Container (app1.zyphron.space)
```

## Core Components

### 1. Frontend (Next.js)
- **Purpose**: User interface for deployment, monitoring, and management
- **Features**:
  - Authentication (signup/login)
  - Dashboard with deployment list
  - One-click deployment form
  - Real-time monitoring and metrics
  - Rollback controls
  - Uptime tracking and analytics

### 2. Backend (FastAPI)
- **Purpose**: Core business logic and orchestration
- **Key Modules**:
  - **Authentication**: JWT-based with role-based access control
  - **Deployment Engine**: Repository analysis, Docker orchestration
  - **Language/Framework Detection**: Automated analysis
  - **Environment Management**: Secure credential handling
  - **Monitoring**: Health checks, uptime tracking
  - **Subdomain Management**: DNS and Nginx configuration
  - **API Routes**: RESTful endpoints for all operations

### 3. Database (PostgreSQL)
- **Purpose**: Persistent storage
- **Tables**:
  - `users`: User accounts and authentication
  - `deployments`: Deployment records and status
  - `monitoring_logs`: Health checks and metrics
  - `subdomains`: Subdomain reservations
  - `api_keys`: API key management

### 4. Cache (Redis)
- **Purpose**: Session management, background task queue
- **Use Cases**:
  - User sessions
  - Celery task queue for deployments
  - Real-time metrics caching

### 5. Docker Engine
- **Purpose**: Container orchestration
- **Operations**:
  - Building images from repositories
  - Running containers with proper isolation
  - Managing multi-container deployments
  - Health monitoring and auto-restart

### 6. Nginx
- **Purpose**: Reverse proxy and load balancing
- **Functions**:
  - Route requests to subdomains
  - SSL/TLS termination (Let's Encrypt)
  - Load balancing between backend instances
  - Security headers and rate limiting

## Deployment Pipeline

```
Step 1: User initiates deployment
  ↓
Step 2: Repo validation and analysis
  ├─ Clone repository
  ├─ Detect languages
  ├─ Detect frameworks
  ├─ Identify database requirements
  ├─ Extract environment variables
  ├─ Build dependency tree
  └─ Validate configurations
  ↓
Step 3: Environment setup
  ├─ Check subdomain availability
  ├─ Request missing env variables (popup)
  ├─ Validate and encrypt credentials
  └─ Store securely in database
  ↓
Step 4: Build phase
  ├─ Generate Dockerfile (or use custom)
  ├─ Build Docker image
  ├─ Run tests in isolated environment
  ├─ Scan for vulnerabilities (optional)
  └─ Tag and prepare for deployment
  ↓
Step 5: Deployment phase
  ├─ Create container from image
  ├─ Set up networking (Docker bridge)
  ├─ Configure environment variables
  ├─ Mount volumes if needed
  ├─ Start container with health checks
  └─ Update database with container ID
  ↓
Step 6: Infrastructure setup
  ├─ Generate Nginx configuration
  ├─ Create SSL certificate (Let's Encrypt)
  ├─ Enable Nginx site configuration
  ├─ Reload Nginx (zero-downtime)
  └─ Point subdomain to deployment
  ↓
Step 7: Monitoring initialization
  ├─ Start health checks (every 30 seconds)
  ├─ Begin uptime tracking
  ├─ Configure auto-rollback on failure
  ├─ Set up performance monitoring
  └─ Notify user of success
  ↓
Deployment Complete - Live on subdomain.zyphron.space
```

## Multi-Container Architecture

For full-stack repositories:

```
Full-Stack App
├─ Frontend Container (React/Next.js/Vue)
│  └─ Port: 3000
├─ Backend Container (Node/Python/Go)
│  └─ Port: 5000/8000/3001
├─ Database Container (PostgreSQL/MySQL)
│  └─ Port: 5432/3306
└─ Redis Container (optional)
   └─ Port: 6379

All connected via Docker Network (internal)
↓
Nginx Reverse Proxy (External Entry Point)
├─ Listens on: 80, 443
├─ Routes requests to appropriate container
├─ Terminates SSL/TLS
└─ Provides subdomain access
```

## Supported Languages & Frameworks

### Frontend
- React, Vue.js, Angular, Next.js, Nuxt, Svelte, Solid.js

### Backend
- Python (FastAPI, Django, Flask)
- Node.js (Express, NestJS, Fastify)
- Go, Rust, Java (Spring), C# (.NET), PHP (Laravel), Ruby (Rails)

### Databases
- PostgreSQL, MySQL, MongoDB, Redis, SQLite, Cassandra

### Other Services
- Message Queues (RabbitMQ, Kafka)
- Search engines (Elasticsearch)
- Cache layers (Memcached)

## Environment Variable Detection

The system automatically detects required environment variables by scanning:
- `process.env.VARIABLE` (JavaScript/Node.js)
- `os.getenv('VARIABLE')` (Python)
- Environment configuration files
- Docker environment sections
- Comments in code

Users are presented a popup to provide missing credentials.

## SRE & DevOps Features

### Monitoring
- **Uptime Checking**: Health checks every 30 seconds
- **Response Time Tracking**: Performance metrics
- **Resource Monitoring**: CPU, Memory, Disk usage
- **Error Logging**: Comprehensive error tracking
- **Alerting**: Notifications on failures

### Reliability
- **Automatic Rollback**: Revert to previous version on container crash
- **Health Checks**: Ensure container is running properly
- **Resource Limits**: Prevent resource exhaustion
- **Rate Limiting**: Prevent abuse
- **Backup Management**: Automated backups

### Scaling (Future)
- Horizontal scaling (multiple replicas)
- Load balancing
- Auto-scaling based on metrics
- Canary deployments

## Security Architecture

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- OAuth2 integration (future)
- API key management

### Data Protection
- Encrypted environment variable storage
- TLS/SSL for all communications
- Secure session management
- Password hashing (bcrypt)

### Container Security
- Non-root container execution
- Minimal base images
- Network isolation
- Resource limits

### API Security
- Rate limiting
- CORS configuration
- Input validation
- SQL injection prevention

## Deployment Architecture - Future (Multi-Cloud)

```
Main Orchestrator (AWS)
├─ Small Repos (<500MB)
├─ Authentication & API Gateway
├─ Monitoring & Analytics
└─ Load Balancing & Routing

Mid-Size Repos (GCP)
├─ 500MB - 5GB
├─ Kubernetes cluster
└─ Auto-scaling

Large Repos (Oracle VM)
├─ >5GB
├─ Dedicated instances
└─ Custom configurations
```

## API Structure

```
/api/v1/
├─ /health                          # System health
├─ /users/
│  ├─ POST /register                # User registration
│  ├─ POST /login                   # User login
│  ├─ GET /me                       # Current user info
│  └─ PUT /me                       # Update profile
├─ /deployments/
│  ├─ POST /                        # Create deployment
│  ├─ GET /                         # List deployments
│  ├─ GET /{id}                     # Get deployment
│  ├─ DELETE /{id}                  # Delete deployment
│  └─ POST /{id}/rollback           # Rollback deployment
├─ /subdomains/
│  ├─ POST /check-availability      # Check subdomain
│  └─ GET /{id}                     # Get subdomain info
└─ /monitoring/
   ├─ GET /deployments/{id}/uptime
   ├─ GET /deployments/{id}/health-checks
   ├─ GET /deployments/{id}/performance
   └─ POST /deployments/{id}/check   # Trigger check
```

## Performance Considerations

- Frontend: Static file caching, CDN ready
- Backend: Async operations with Celery
- Database: Connection pooling, query optimization
- Cache: Redis for session management and rate limiting
- Container: Resource limits to prevent issues
- Nginx: Gzip compression, HTTP/2, connection pooling

## Error Handling & 100% Success Rate

The system achieves high reliability through:
1. **Pre-flight Validation**: Verify requirements before deployment
2. **Rollback on Failure**: Automatic reversion on any error
3. **Comprehensive Logging**: Track every step for debugging
4. **Health Verification**: Ensure service is running post-deployment
5. **Container Restart**: Auto-restart on unexpected termination
6. **Monitoring & Alerts**: Immediate notification of issues
7. **Manual Rollback**: User can trigger rollback at any time

## Database Schema Highlights

- **Audit Trails**: All actions logged with timestamps
- **Deployment History**: Track all versions
- **Encryption**: Sensitive data encrypted at rest
- **Indexes**: Optimized for common queries
- **Foreign Keys**: Data integrity through relationships
- **Soft Deletes**: Preserve historical data

This architecture ensures production-ready deployment, scalability, security, and comprehensive DevOps capabilities.
