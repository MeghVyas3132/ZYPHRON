# 🌐 Hostinger Domain Setup - Quick Reference

## What You'll Have After Setup

```
Your Hostinger Domain: yourdomain.com
        ↓
    [Hostinger DNS]
        ↓
    Your Public IP (from Router)
        ↓
    [Your Router: Port 80, 443 Forwarded]
        ↓
    Your Local Machine
        ↓
    [Nginx Container]
        ├─→ yourdomain.com ──→ Frontend (Next.js on port 3000)
        ├─→ app1.yourdomain.com ──→ Backend API (FastAPI on port 8000)
        ├─→ app2.yourdomain.com ──→ Backend API (FastAPI on port 8000)
        └─→ any.yourdomain.com ──→ Backend API (Wildcard)
```

## 5-Minute Quick Start

### 1. Run Setup Script

```bash
chmod +x scripts/setup-domain.sh
./scripts/setup-domain.sh
```

This will ask for:
- Your Hostinger domain name
- Your email for SSL
- Your public IP (auto-fetches if you leave blank)

### 2. Update Hostinger DNS

Log in → Domains → Your Domain → DNS Records

Add these 3 records (using your public IP):

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | YOUR_PUBLIC_IP | 3600 |
| A | www | YOUR_PUBLIC_IP | 3600 |
| A | * | YOUR_PUBLIC_IP | 3600 |

### 3. Configure Router

1. Access router (192.168.1.1 or 192.168.0.1)
2. Port Forwarding → Add:
   - External: 80 → Internal: 80
   - External: 443 → Internal: 443

### 4. Generate SSL Certificates

```bash
chmod +x scripts/setup-ssl.sh
./scripts/setup-ssl.sh
```

Enter when prompted:
- Domain: yourdomain.com
- Email: your-email@example.com

### 5. Start Services

```bash
docker-compose up -d
```

### 6. Wait & Test

Wait 24 hours for DNS propagation, then:

```bash
# Test frontend
curl https://yourdomain.com

# Test backend
curl https://app1.yourdomain.com/api/v1/health
```

---

## Find Your IPs

### Get Public IP (for Hostinger)

```bash
curl ifconfig.me
```

Or visit: https://whatismyipaddress.com

### Get Local IP (for Router Port Forwarding)

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Linux:**
```bash
hostname -I
```

Or check your router's DHCP client list.

---

## File Locations

| File | Purpose |
|------|---------|
| `infrastructure/nginx.conf` | Main nginx config (routes frontend/backend) |
| `scripts/setup-ssl.sh` | Generate SSL certificates |
| `scripts/setup-domain.sh` | Interactive setup wizard |
| `infrastructure/certs/` | SSL certificates stored here |
| `DOMAIN_SETUP.md` | Detailed configuration guide |

---

## Architecture Flow

```
Step 1: DNS Resolution
   yourdomain.com → Hostinger DNS → Your Public IP

Step 2: Router Forwarding
   External IP:443 → Router → Your Local Machine:443

Step 3: Nginx Routing (in your container)
   yourdomain.com:443 → Frontend Container (3000)
   app1.yourdomain.com:443 → Backend Container (8000)
   app2.yourdomain.com:443 → Backend Container (8000)
   *.yourdomain.com:443 → Backend Container (8000)
```

---

## Common DNS Records Explained

### A Record
Maps domain name to IP address
```
@ (root)           → YOUR_PUBLIC_IP  (yourdomain.com)
www                → YOUR_PUBLIC_IP  (www.yourdomain.com)
*  (wildcard)      → YOUR_PUBLIC_IP  (*.yourdomain.com)
```

### CNAME Record (Alternative)
Maps subdomain to another domain
```
app1.yourdomain.com CNAME → yourdomain.com
app2.yourdomain.com CNAME → yourdomain.com
```

Use either A records with wildcard OR CNAME records for subdomains.

---

## Environment Variables to Update

### In `docker-compose.yml`:

**Frontend** - Already correct for nginx routing:
```yaml
NEXT_PUBLIC_API_URL=http://yourdomain.com/api/v1
# or
NEXT_PUBLIC_API_URL=https://app1.yourdomain.com/api/v1
```

**Backend** - CORS settings:
```python
# In backend/app/core/config.py
ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "https://*.yourdomain.com",
]
```

---

## Troubleshooting Quick Fixes

### Can't reach domain externally?

```bash
# 1. Check DNS propagation
nslookup yourdomain.com

# 2. Verify port forwarding
# Access router and confirm 80, 443 forwarding

# 3. Check firewall
# macOS: System Preferences → Security & Privacy → Firewall

# 4. Test locally first
curl http://localhost:80
curl http://localhost:3000
```

### SSL Certificate Error?

```bash
# Regenerate certificates
./scripts/setup-ssl.sh

# Or check if certs exist
ls -la infrastructure/certs/live/
```

### Nginx not responding?

```bash
# Check container status
docker ps | grep zyphron_nginx

# View logs
docker logs zyphron_nginx -f

# Verify config syntax
docker exec zyphron_nginx nginx -t
```

---

## Timeline

| When | Action |
|------|--------|
| **Day 0** | Set up DNS records, port forwarding, SSL certs |
| **Day 0-1** | DNS propagates (up to 24 hours) |
| **Day 1+** | Domain should be fully accessible |
| **Monthly** | Renew SSL certificates: `./scripts/setup-ssl.sh` |

---

## Support Resources

- **DNS Check**: https://www.whatsmydns.net
- **SSL Test**: https://www.ssllabs.com/ssltest
- **Hostinger Help**: https://support.hostinger.com
- **Let's Encrypt**: https://letsencrypt.org
- **Nginx Docs**: https://nginx.org/en/docs/

---

## Security Checklist

- [ ] Ports 80, 443 only open to internet (firewall)
- [ ] SSL certificates auto-renew (check cron job)
- [ ] HTTPS redirects HTTP (nginx configured)
- [ ] Backend not directly exposed (only via nginx)
- [ ] Environment variables not in code
- [ ] Rate limiting enabled on APIs
- [ ] CORS properly configured

---

**Status**: Ready to deploy! Follow the 5-minute quick start above. 🚀
