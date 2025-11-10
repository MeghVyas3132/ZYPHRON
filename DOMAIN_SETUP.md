# Domain Configuration Guide for Hostinger

## 📋 Overview

This guide explains how to connect your Hostinger domain to your local Zyphron deployment with:
- **Main Domain**: yourdomain.com → Frontend (Next.js)
- **Subdomains**: app1.yourdomain.com, app2.yourdomain.com → Backend API

## 🔧 Configuration Steps

### 1. Update Nginx Configuration

**File**: `infrastructure/nginx.conf`

Replace all instances of `yourdomain.com` with your actual domain:

```bash
# Using sed on macOS
sed -i '' 's/yourdomain\.com/YOUR_ACTUAL_DOMAIN.com/g' infrastructure/nginx.conf
```

Or manually edit the file and replace `yourdomain.com` with your domain (e.g., `example.com`)

### 2. Update SSL Certificate Paths

Edit `scripts/setup-ssl.sh` and update:

```bash
DOMAIN="yourdomain.com"          # ← Change this
EMAIL="your-email@example.com"   # ← Change this
```

### 3. Generate SSL Certificates

```bash
# Make script executable
chmod +x scripts/setup-ssl.sh

# Run the SSL setup script
./scripts/setup-ssl.sh
```

This will:
- Generate certificates for `yourdomain.com`, `*.yourdomain.com`, `www.yourdomain.com`
- Store them in `infrastructure/certs/`
- Automatically renew them (validity: 3 months, just rerun before expiry)

### 4. Hostinger DNS Configuration

Log in to your Hostinger control panel:

1. Go to **Domains** → **Your Domain** → **DNS**
2. Add/Update these records:

```
Type    | Name (Subdomain) | Value              | TTL
--------|------------------|--------------------|-------
A       | @                | YOUR_PUBLIC_IP     | 3600
A       | www              | YOUR_PUBLIC_IP     | 3600
A       | *                | YOUR_PUBLIC_IP     | 3600
CNAME   | app1             | yourdomain.com     | 3600
CNAME   | app2             | yourdomain.com     | 3600
```

**Note**: If using CNAME, all subdomains will route to your main IP. The wildcard `*` record is simpler if supported.

### 5. Router Port Forwarding

Access your router admin panel (usually `192.168.1.1`):

1. Go to **Port Forwarding** or **Virtual Server**
2. Add these rules:

```
External Port | Protocol | Internal IP      | Internal Port
80            | TCP      | YOUR_LOCAL_IP    | 80
443           | TCP      | YOUR_LOCAL_IP    | 443
```

Replace `YOUR_LOCAL_IP` with your machine's local IP:
```bash
# Find your local IP
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### 6. Find Your Public IP

```bash
# Check your public IP
curl ifconfig.me
# Or visit: https://whatismyipaddress.com
```

Use this IP in Hostinger DNS settings.

### 7. Start Docker Containers

```bash
# Build and start all services
docker-compose up -d

# Verify nginx is running
docker ps | grep zyphron_nginx

# Check logs
docker logs zyphron_nginx -f
```

## 📞 Testing Your Setup

### Test from Local Machine

```bash
# Test frontend (via nginx)
curl https://yourdomain.com

# Test backend (via subdomain)
curl https://app1.yourdomain.com/api/v1/health

# Check certificate
curl -v https://yourdomain.com 2>&1 | grep "subject="
```

### From External Network (Mobile/Friend's Phone)

1. Ensure your domain is working: `https://yourdomain.com`
2. Check subdomains: `https://app1.yourdomain.com`
3. If it fails, verify:
   - DNS records are propagated (wait up to 24 hours)
   - Port forwarding is correct
   - Public IP is correct
   - Firewall allows ports 80, 443

### DNS Propagation Check

Visit: https://www.whatsmydns.net/?d=yourdomain.com

Wait for all DNS servers to show your public IP.

## 🔄 Architecture Flow

```
Internet
    ↓
Your Public IP:443 (Hostinger DNS points here)
    ↓
Router (Port 443 forwarded to Local IP:443)
    ↓
Your Machine (Docker Host)
    ↓
Nginx Container (0.0.0.0:443)
    ├─→ yourdomain.com → frontend:3000 (Next.js Frontend)
    └─→ *.yourdomain.com → backend:8000 (FastAPI Backend)
```

## 🚀 Deployment Examples

### Deploy Frontend on Main Domain

Accessible at: `https://yourdomain.com`

### Deploy Backend API on Subdomains

- `https://app1.yourdomain.com` → API Instance 1
- `https://api.yourdomain.com` → API Gateway
- `https://admin.yourdomain.com` → Admin Panel

### Dynamic Subdomain Routing

Nginx automatically routes any subdomain to your backend:

```bash
# All these work:
curl https://anything.yourdomain.com
curl https://myapp.yourdomain.com
curl https://api-v2.yourdomain.com
```

Your backend can identify the subdomain via the `X-Subdomain` header.

## ⚠️ Troubleshooting

### "Connection Refused" or "Cannot Reach Server"

1. **Check DNS**: `nslookup yourdomain.com` should show your public IP
2. **Check Port Forwarding**: Router should forward 80/443 to your machine
3. **Check Firewall**: Ensure macOS firewall allows nginx
4. **Check Nginx**: `docker logs zyphron_nginx` for errors

### SSL Certificate Errors

```bash
# Renew certificates
./scripts/setup-ssl.sh

# Or manually:
certbot renew
```

### Wildcard Certificate Not Working

If `*.yourdomain.com` doesn't work but `yourdomain.com` does:

1. Ensure you used `--standalone` or `--dns` method in certbot
2. Check Hostinger supports wildcard DNS
3. Try using explicit CNAME records instead:
   ```
   app1.yourdomain.com CNAME yourdomain.com
   app2.yourdomain.com CNAME yourdomain.com
   ```

### Nginx Not Starting

```bash
# Check nginx config syntax
docker exec zyphron_nginx nginx -t

# View full logs
docker logs zyphron_nginx

# Rebuild container
docker-compose down
docker-compose up -d --build nginx
```

## 📝 Nginx Configuration Locations

- **Main Config**: `infrastructure/nginx.conf`
- **SSL Certs**: `infrastructure/certs/live/yourdomain.com/`
- **Container Logs**: `docker logs zyphron_nginx -f`

## 🔐 Security Checklist

- [ ] SSL certificates valid (check expiry: `curl -v https://yourdomain.com 2>&1 | grep dates`)
- [ ] Nginx security headers enabled (check in `infrastructure/nginx.conf`)
- [ ] Firewall configured to only allow 80, 443
- [ ] Port forwarding not exposing backend directly (only via nginx)
- [ ] HTTPS enforced (HTTP redirects to HTTPS)

## 📅 Certificate Renewal

Let's Encrypt certificates are valid for 90 days. Renew them:

```bash
# Manual renewal (run monthly to be safe)
certbot renew

# Or run the setup script again
./scripts/setup-ssl.sh
```

## 🆘 Still Having Issues?

1. **Can't access domain from outside**: Wait 24 hours for DNS propagation
2. **Certificate errors**: Regenerate with `./scripts/setup-ssl.sh`
3. **Nginx not responding**: Check container logs and port forwarding
4. **Subdomains not working**: Verify wildcard DNS record or CNAME records

For more help, check Hostinger's documentation or your router's manual.

---

**Your deployment should now be live at: https://yourdomain.com** 🎉
