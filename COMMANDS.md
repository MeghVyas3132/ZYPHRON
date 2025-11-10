# ⚡ ZYPHRON QUICK COMMAND REFERENCE

## 🚀 LAUNCH (Do This Now!)

```bash
# One command to launch everything:
chmod +x start-zyphron.sh && ./start-zyphron.sh

# OR manually:
cd frontend && npm install && cd ..
docker-compose up -d
open http://localhost:3000
```

---

## 🌐 ACCESS YOUR SERVICES

| Service | URL | Username | Password |
|---------|-----|----------|----------|
| **Frontend** | http://localhost:3000 | - | - |
| **Backend API** | http://localhost:8000 | - | - |
| **API Docs** | http://localhost:8000/docs | - | - |
| **pgAdmin** | http://localhost:5050 | admin@zyphron.local | zyphron |

---

## 📊 DOCKER COMMANDS

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View all running containers
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f postgres

# Rebuild services
docker-compose build --no-cache

# Enter a container
docker-compose exec frontend bash
docker-compose exec backend bash

# Remove everything (careful!)
docker-compose down -v
```

---

## 🛠️ SETUP COMMANDS

```bash
# Install frontend dependencies
cd frontend && npm install && cd ..

# Generate SSL certificates
./scripts/setup-ssl.sh

# Interactive domain setup
./scripts/setup-domain.sh

# View your public IP (for Hostinger)
curl ifconfig.me

# View your local IP (for router)
ifconfig | grep "inet " | grep -v 127.0.0.1
```

---

## 📈 MONITORING

```bash
# Check service health
docker-compose ps

# View real-time logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f frontend -n 100  # Last 100 lines
docker-compose logs frontend --tail=50

# Database status
docker-compose exec postgres pg_isready -U zyphron

# Redis status
docker-compose exec redis redis-cli ping

# Disk usage
docker system df
```

---

## 🗄️ DATABASE COMMANDS

```bash
# Enter PostgreSQL
docker-compose exec postgres psql -U zyphron -d zyphron

# Useful PostgreSQL commands (once inside):
\dt              # List tables
\d table_name    # Describe table
SELECT * FROM users;  # Query data
\q              # Exit

# Backup database
docker-compose exec postgres pg_dump -U zyphron zyphron > backup.sql

# Restore database
docker-compose exec -T postgres psql -U zyphron zyphron < backup.sql
```

---

## 🧹 MAINTENANCE

```bash
# Clean up Docker (remove unused images/containers)
docker system prune -a

# Update all images
docker-compose pull

# Rebuild everything
docker-compose build --no-cache && docker-compose up -d

# View disk usage
du -sh *
docker system df
```

---

## 🔒 SECURITY

```bash
# Check exposed ports
netstat -tuln | grep LISTEN

# View environment variables (for a service)
docker-compose exec frontend env

# Check service vulnerabilities
docker scan zyphron_frontend
```

---

## 🐛 DEBUGGING

```bash
# Frontend issues
docker-compose logs -f frontend
# Check: http://localhost:3000

# Backend issues
docker-compose logs -f backend
# Check: http://localhost:8000/docs

# Database issues
docker-compose logs -f postgres
docker-compose exec postgres pg_isready

# Redis issues
docker-compose logs -f redis
docker-compose exec redis redis-cli ping

# Nginx issues (once SSL is setup)
docker-compose logs -f nginx
docker-compose exec nginx nginx -t  # Test config

# Port conflicts
lsof -i :3000    # Check port 3000
lsof -i :8000    # Check port 8000
lsof -i :5050    # Check port 5050
```

---

## 📝 WORKFLOW COMMANDS

```bash
# Daily check
docker-compose ps
docker-compose logs -f

# Before pushing to production
docker-compose down
docker-compose build --no-cache
docker-compose up -d
# Test everything at http://localhost:3000

# Deploy SSL
./scripts/setup-ssl.sh

# Check DNS propagation
nslookup yourdomain.com
dig yourdomain.com
curl -v https://yourdomain.com 2>&1 | grep "subject="

# Monitor in real-time
watch -n 1 'docker-compose ps'
```

---

## 🔍 SYSTEM INFO

```bash
# Your IPs
echo "Local IP:" && ifconfig | grep "inet " | grep -v 127.0.0.1
echo "Public IP:" && curl ifconfig.me

# Current directory
pwd

# Zyphron version
cat package.json | grep version

# Docker info
docker --version
docker-compose --version
npm --version
node --version
```

---

## 🚀 PRODUCTION DEPLOYMENT

```bash
# 1. Generate certificates
./scripts/setup-ssl.sh

# 2. Update .env files with production secrets
# Edit frontend/.env.production
# Edit backend/.env.production

# 3. Build production images
docker-compose -f docker-compose.prod.yml build

# 4. Start production
docker-compose -f docker-compose.prod.yml up -d

# 5. View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 💾 QUICK BACKUPS

```bash
# Backup everything
mkdir -p backups
docker-compose exec postgres pg_dump -U zyphron zyphron > backups/db_$(date +%Y%m%d_%H%M%S).sql
tar -czf backups/frontend_$(date +%Y%m%d_%H%M%S).tar.gz frontend/
tar -czf backups/backend_$(date +%Y%m%d_%H%M%S).tar.gz backend/

# List backups
ls -lh backups/

# Restore database
docker-compose exec -T postgres psql -U zyphron zyphron < backups/db_TIMESTAMP.sql
```

---

## ⚡ ONE-LINERS

```bash
# Start and watch logs
docker-compose up && docker-compose logs -f

# Restart everything
docker-compose restart

# Update and restart
docker-compose pull && docker-compose up -d

# Clean and rebuild
docker-compose down -v && docker-compose build --no-cache && docker-compose up -d

# Check all services are healthy
docker-compose ps | grep -i "up"

# Find and kill port conflicts
lsof -i :3000 | awk 'NR!=1 {print $2}' | xargs kill -9

# View real-time resource usage
docker stats
```

---

## 📞 EMERGENCY COMMANDS

```bash
# Service won't start? Hard reset
docker-compose down
docker system prune -a
docker volume prune
docker-compose build --no-cache
docker-compose up -d

# Lost connection? Check network
docker network ls
docker network inspect zyphron_network

# Port stuck? Release it
lsof -i :PORT_NUMBER | grep LISTEN | awk '{print $2}' | xargs kill -9

# Database corrupted? Restore
docker-compose exec postgres pg_dump -U zyphron zyphron > backup.sql
docker-compose down -v
docker-compose up -d postgres
docker-compose exec -T postgres psql -U zyphron zyphron < backup.sql
```

---

## 📋 HELPFUL RESOURCES

```bash
# View this file
cat << 'EOF'
Quick Reference: See /Users/meghvyas/Desktop/ZYPHRON/START_HERE.md
Status Report: See /Users/meghvyas/Desktop/ZYPHRON/ZYPHRON_STATUS.md
Domain Setup: See /Users/meghvyas/Desktop/ZYPHRON/DOMAIN_SETUP_SUMMARY.md
EOF
```

---

## ✅ YOUR INSTANT CHECKLIST

```bash
✓ Local IP: 192.168.1.7
✓ Frontend: Next.js ready
✓ Backend: FastAPI ready
✓ Database: PostgreSQL ready
✓ Viewer: pgAdmin ready
✓ Cache: Redis ready
✓ Proxy: Nginx configured
✓ SSL: Scripts ready

→ Next: npm install && docker-compose up -d
→ Then: open http://localhost:3000
→ Enjoy! 🎉
```

---

**Saved at**: `/Users/meghvyas/Desktop/ZYPHRON/`  
**Last Updated**: November 11, 2025
