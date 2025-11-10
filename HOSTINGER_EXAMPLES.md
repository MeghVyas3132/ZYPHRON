# Configuration Examples & Templates

## Hostinger Domain Setup Examples

### Example 1: Simple Setup (One Backend)

**Your Setup:**
- Domain: `example.com` (from Hostinger)
- Frontend: `https://example.com` (Next.js)
- Backend: `https://api.example.com` (FastAPI)

**Hostinger DNS Records:**
```
Type | Name | Value         | TTL
-----|------|---------------|-----
A    | @    | 203.0.113.50  | 3600
A    | www  | 203.0.113.50  | 3600
A    | api  | 203.0.113.50  | 3600
```

**Nginx Routes:**
```
example.com → localhost:3000 (Frontend)
api.example.com → localhost:8000 (Backend API)
```

---

### Example 2: Multiple Backends (App Platform)

**Your Setup:**
- Domain: `myapp.com`
- Frontend: `https://myapp.com` (Dashboard)
- Backend 1: `https://app1.myapp.com` (API)
- Backend 2: `https://app2.myapp.com` (API)
- Admin: `https://admin.myapp.com` (Admin Panel)

**Hostinger DNS Records:**
```
Type | Name  | Value        | TTL
-----|-------|--------------|-----
A    | @     | 203.0.113.50 | 3600
A    | www   | 203.0.113.50 | 3600
A    | *     | 203.0.113.50 | 3600
```

The wildcard `*` matches: app1, app2, admin, anything.myapp.com

**Nginx Routes:**
```
myapp.com → localhost:3000 (Frontend)
app1.myapp.com → localhost:8000 (Backend)
app2.myapp.com → localhost:8000 (Backend)
admin.myapp.com → localhost:8000 (Backend)
(nginx passes X-Subdomain header to backend for routing)
```

---

### Example 3: Separate Services on Subdomains

**Your Setup:**
- Frontend: `https://app.company.com`
- API Gateway: `https://api.company.com`
- WebSocket: `https://ws.company.com`
- Admin: `https://admin.company.com`

**Hostinger DNS:**
```
Type | Name | Value        | TTL
-----|------|--------------|-----
A    | app  | 203.0.113.50 | 3600
A    | api  | 203.0.113.50 | 3600
A    | ws   | 203.0.113.50 | 3600
A    | admin| 203.0.113.50 | 3600
```

**Nginx Routes:**
```
app.company.com → localhost:3000 (Frontend)
api.company.com → localhost:8000 (API)
ws.company.com → localhost:8001 (WebSocket Server)
admin.company.com → localhost:8002 (Admin Panel)
```

---

## Step-by-Step Configuration for Different Scenarios

### Scenario A: Brand New Hostinger Account

1. **Log in to Hostinger**
   - Go to Domains → Purchase Domain (if needed)
   - Select your domain

2. **Configure DNS**
   - Domains → Your Domain → DNS
   - Add A records for:
     - `@` (root) → Your Public IP
     - `www` → Your Public IP
     - `*` (wildcard) → Your Public IP

3. **Configure Router**
   - Log in to router (192.168.1.1)
   - Port Forwarding → Add rules:
     - External 80 → 192.168.x.x:80 (your local machine)
     - External 443 → 192.168.x.x:443 (your local machine)

4. **Generate SSL**
   ```bash
   ./scripts/setup-ssl.sh
   ```

5. **Start Services**
   ```bash
   docker-compose up -d
   ```

---

### Scenario B: Existing Hostinger Domain

If you already have a domain:

1. **Get your Hostinger domain details**
   ```bash
   # Find your domain name
   # Example: mydomain.com or mydomain.hostinger.com
   ```

2. **Update nginx.conf**
   ```bash
   sed -i '' 's/yourdomain\.com/mydomain.com/g' infrastructure/nginx.conf
   ```

3. **Update DNS records** (if not already set)
   - Go to Hostinger → Domains → Your Domain → DNS
   - Point to your public IP

4. **Continue as above**

---

### Scenario C: Subdomain Already Hosted Elsewhere

If your main domain is on another host but you want to use subdomains:

1. **In Hostinger DNS, create CNAME records:**
   ```
   Type  | Name   | Value          | TTL
   ------|--------|----------------|-----
   CNAME | app1   | yourdomain.com | 3600
   CNAME | app2   | yourdomain.com | 3600
   CNAME | api    | yourdomain.com | 3600
   ```

2. **Or use A records if you control root domain:**
   ```
   Type | Name | Value        | TTL
   -----|------|--------------|-----
   A    | @    | 203.0.113.50 | 3600
   A    | *    | 203.0.113.50 | 3600
   ```

---

## Nginx Configuration for Different Scenarios

### Config 1: Single Backend on Subdomain

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }
}
```

### Config 2: Multiple Backends - Subdomain Routing

```nginx
server {
    listen 443 ssl http2;
    server_name ~^(?<subdomain>.+)\.example\.com$;
    
    location / {
        proxy_pass http://backend:8000;
        proxy_set_header X-Subdomain $subdomain;
        # Your backend reads X-Subdomain to route requests
    }
}
```

### Config 3: Multiple Backends - Path Routing

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    location /app1/ {
        proxy_pass http://backend1:8000/;
    }
    
    location /app2/ {
        proxy_pass http://backend2:8001/;
    }
}
```

### Config 4: Frontend + Backend Split

```nginx
# Frontend
server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    location / {
        proxy_pass http://frontend:3000;
    }
}

# Backend API
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    location / {
        proxy_pass http://backend:8000;
    }
}
```

---

## Backend Code Examples

### FastAPI - Extract Subdomain from Header

```python
# In your FastAPI router
from fastapi import Header

@app.get("/health")
async def health(x_subdomain: str = Header(None)):
    """
    Nginx passes subdomain via X-Subdomain header
    Examples:
    - x_subdomain = "app1"
    - x_subdomain = "api"
    """
    return {
        "status": "healthy",
        "subdomain": x_subdomain
    }
```

### FastAPI - CORS Configuration

```python
# In backend/app/core/config.py

from fastapi.middleware.cors import CORSMiddleware

# Update these with your domains
ALLOWED_ORIGINS = [
    "https://example.com",
    "https://www.example.com",
    "https://api.example.com",
    "https://app1.example.com",
    "https://app2.example.com",
    "https://*.example.com",  # Wildcard (if needed)
]

# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Next.js - Environment Variables

```bash
# In frontend/.env.local

# Single backend
NEXT_PUBLIC_API_URL=https://api.example.com

# Or subdomain-based
NEXT_PUBLIC_API_URL=https://app1.example.com

# Or main domain with path
NEXT_PUBLIC_API_URL=https://example.com/api
```

---

## Docker Compose Examples

### Setup for Multiple Backends

```yaml
services:
  backend1:
    build: ./backend
    environment:
      - INSTANCE=app1
    ports:
      - "8001:8000"
    networks:
      - zyphron_network

  backend2:
    build: ./backend
    environment:
      - INSTANCE=app2
    ports:
      - "8002:8000"
    networks:
      - zyphron_network

  nginx:
    volumes:
      - ./infrastructure/nginx-multi.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend1
      - backend2
      - frontend
```

---

## SSL Certificate Management

### Generate Wildcard Certificate

```bash
# For *.example.com
certbot certonly \
    --standalone \
    -d example.com \
    -d "*.example.com" \
    -d www.example.com
```

### Renew Before Expiry

```bash
# Check expiration
certbot certificates

# Renew all
certbot renew

# Force renewal
certbot renew --force-renewal
```

### Automated Renewal

```bash
# Add to crontab (runs monthly)
0 3 1 * * /usr/bin/certbot renew --quiet

# Or
0 3 1 * * /path/to/scripts/setup-ssl.sh
```

---

## Testing Configurations

### Test DNS Resolution

```bash
# Check if domain resolves to your public IP
nslookup example.com

# Detailed DNS info
dig example.com

# Check specific subdomain
nslookup app1.example.com
```

### Test SSL Certificate

```bash
# Check certificate details
curl -v https://example.com 2>&1 | grep "subject=\|issuer=\|dates="

# Full certificate info
openssl s_client -connect example.com:443 < /dev/null

# Check certificate expiry
certbot certificates
```

### Test Nginx Configuration

```bash
# Validate syntax
docker exec zyphron_nginx nginx -t

# Check running config
docker exec zyphron_nginx nginx -T

# View logs
docker logs zyphron_nginx -f
```

### Test Connectivity

```bash
# From your local machine
curl https://example.com
curl https://api.example.com/health

# From external network (ask a friend or use mobile hotspot)
# This confirms your router port forwarding is correct
```

---

## Hostinger-Specific Notes

### Hostinger DNS Propagation

Hostinger uses these nameservers (usually pre-configured):
- `ns1.hostinger.com`
- `ns2.hostinger.com`

Changes typically propagate in 24 hours, but can take up to 48 hours.

### Hostinger Firewall (if enabled)

Make sure ports 80, 443 are allowed:
- Hostinger Control Panel → Advanced → Firewall
- Add rules to allow traffic on ports 80, 443

### Hostinger Email Configuration

If using Hostinger for email:
- Keep MX records (don't delete)
- Add your A records for domain
- Both can coexist

---

## Quick Command Reference

```bash
# Setup
./scripts/setup-domain.sh          # Interactive setup
./scripts/setup-ssl.sh             # Generate SSL certs

# Testing
nslookup yourdomain.com            # Check DNS
curl https://yourdomain.com        # Test frontend
curl https://app1.yourdomain.com   # Test backend

# Management
docker-compose up -d               # Start services
docker-compose down                # Stop services
docker logs zyphron_nginx -f       # View nginx logs

# Renewal
certbot renew                       # Renew SSL certificates
./scripts/setup-ssl.sh             # Alternative renewal method
```

---

Need help with a specific scenario? Check the troubleshooting section in `DOMAIN_SETUP.md`.
