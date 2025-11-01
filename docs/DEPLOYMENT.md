# Zyphron Deployment Guide

## Local Development Setup

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/zyphron.git
cd zyphron

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

### Step 2: Configure Environment

**backend/.env**:
```bash
DATABASE_URL=postgresql://zyphron:zyphron@localhost:5432/zyphron
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
DEBUG=True
```

**frontend/.env.local**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Step 3: Start Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Verify services
docker-compose ps

# Check backend logs
docker-compose logs -f backend

# Check frontend logs
docker-compose logs -f frontend
```

### Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create superuser (optional)
docker-compose exec backend python -c "from app.models import User; from app.core.security import hash_password; ..."
```

### Step 5: Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (zyphron/zyphron)
- **Redis**: localhost:6379

## Production Deployment

### Prerequisites
- Server with 4GB+ RAM
- Docker & Docker Compose
- Domain name (zyphron.space)
- SSL certificate support (Let's Encrypt)

### Step 1: Server Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx & Certbot
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

### Step 2: Clone and Configure

```bash
# Clone repository
git clone https://github.com/yourusername/zyphron.git /opt/zyphron
cd /opt/zyphron

# Create production env files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Update .env files with production values
nano backend/.env
nano frontend/.env.local
```

### Step 3: Generate SSL Certificate

```bash
# Request Let's Encrypt certificate for main domain
sudo certbot certonly --standalone -d zyphron.space -d www.zyphron.space

# Copy certificates to project
sudo cp /etc/letsencrypt/live/zyphron.space/fullchain.pem infrastructure/certs/
sudo cp /etc/letsencrypt/live/zyphron.space/privkey.pem infrastructure/certs/
sudo chown -R $(whoami):$(whoami) infrastructure/certs/
```

### Step 4: Start Production Services

```bash
# Start with production compose file
docker-compose -f infrastructure/docker-compose.prod.yml up -d

# Verify services
docker-compose -f infrastructure/docker-compose.prod.yml ps

# Check logs
docker-compose -f infrastructure/docker-compose.prod.yml logs -f
```

### Step 5: Configure Nginx Main Domain

```bash
# Create Nginx configuration for main domain
sudo nano /etc/nginx/sites-available/zyphron.space
```

**Configuration**:
```nginx
upstream zyphron_frontend {
    server localhost:3000;
}

upstream zyphron_api {
    server localhost:8000;
}

server {
    listen 80;
    server_name zyphron.space www.zyphron.space;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name zyphron.space www.zyphron.space;

    ssl_certificate /etc/letsencrypt/live/zyphron.space/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/zyphron.space/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://zyphron_frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API
    location /api/ {
        proxy_pass http://zyphron_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable configuration
sudo ln -s /etc/nginx/sites-available/zyphron.space /etc/nginx/sites-enabled/

# Test Nginx
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Step 6: Setup Automatic Backups

```bash
# Create backup script
sudo nano /opt/zyphron/scripts/backup.sh
```

**Content**:
```bash
#!/bin/bash
BACKUP_DIR="/opt/zyphron/backups"
DATE=$(date +"%Y%m%d_%H%M%S")

# Backup database
docker-compose -f infrastructure/docker-compose.prod.yml exec -T postgres pg_dump -U zyphron zyphron > "$BACKUP_DIR/db_$DATE.sql"

# Compress backup
gzip "$BACKUP_DIR/db_$DATE.sql"

# Keep only last 7 days
find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_$DATE.sql.gz"
```

```bash
# Make executable
chmod +x /opt/zyphron/scripts/backup.sh

# Add to crontab for daily backups
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/zyphron/scripts/backup.sh") | crontab -
```

### Step 7: Setup Monitoring

```bash
# Install Prometheus for monitoring
docker-compose -f infrastructure/docker-compose.prod.yml up prometheus -d

# Configure Grafana (optional)
docker-compose -f infrastructure/docker-compose.prod.yml up grafana -d
```

### Step 8: Health Checks

```bash
# Verify all services are healthy
curl -s http://localhost:8000/health | jq .
curl -s http://localhost:8000/health/detailed | jq .

# Monitor container status
docker-compose -f infrastructure/docker-compose.prod.yml ps

# Check logs
docker-compose -f infrastructure/docker-compose.prod.yml logs --tail=100
```

## Maintenance

### Database Maintenance

```bash
# Backup database
docker-compose exec postgres pg_dump -U zyphron zyphron > backup.sql

# Restore database
docker-compose exec postgres psql -U zyphron zyphron < backup.sql

# Vacuum database
docker-compose exec postgres vacuumdb -U zyphron zyphron
```

### SSL Certificate Renewal

```bash
# Automatic renewal (runs via cron)
sudo certbot renew --dry-run

# Manual renewal
sudo certbot renew
```

### Scaling

```bash
# Increase backend replicas in production
docker-compose -f infrastructure/docker-compose.prod.yml up -d --scale backend=3

# Monitor load
docker-compose -f infrastructure/docker-compose.prod.yml stats
```

## Troubleshooting

### Container Issues

```bash
# View container logs
docker-compose logs <service>

# Execute command in container
docker-compose exec <service> sh

# Restart container
docker-compose restart <service>

# Rebuild container
docker-compose up --build <service>
```

### Database Connection Issues

```bash
# Check database status
docker-compose exec postgres pg_isready -U zyphron

# Connect to database
docker-compose exec postgres psql -U zyphron -d zyphron
```

### Performance Issues

```bash
# Monitor resource usage
docker-compose stats

# Check database slow queries
docker-compose exec postgres psql -U zyphron zyphron -c "SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;"
```

## Performance Optimization

### Backend Optimization
- Enable query caching with Redis
- Use database indexes
- Implement pagination
- Use connection pooling

### Frontend Optimization
- Enable static file caching
- Minify and bundle code
- Use image optimization
- Implement service workers

### Infrastructure Optimization
- Use CDN for static files
- Enable Gzip compression
- Use HTTP/2
- Implement rate limiting

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable firewall
- [ ] Configure SSH keys
- [ ] Enable SSL/TLS
- [ ] Setup rate limiting
- [ ] Enable CORS properly
- [ ] Rotate secrets regularly
- [ ] Enable logging and monitoring
- [ ] Setup backups
- [ ] Regular security updates

## Support & Documentation

- API Documentation: http://zyphron.space/api/docs
- Architecture: See ARCHITECTURE.md
- Contributing: See CONTRIBUTING.md
- Issues: GitHub Issues
