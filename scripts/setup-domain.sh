#!/bin/bash

# Quick Domain Setup Script for Hostinger
# This script guides you through the configuration process

echo "🚀 Zyphron Hostinger Domain Setup"
echo "=================================="
echo ""

# Step 1: Get domain name
read -p "Enter your Hostinger domain (e.g., example.com): " DOMAIN
read -p "Enter your email for SSL certificates: " EMAIL
read -p "Enter your public IP address (or leave blank to fetch): " PUBLIC_IP

if [ -z "$PUBLIC_IP" ]; then
    echo "🌐 Fetching your public IP..."
    PUBLIC_IP=$(curl -s ifconfig.me)
fi

echo ""
echo "📋 Your Configuration:"
echo "  Domain: $DOMAIN"
echo "  Email: $EMAIL"
echo "  Public IP: $PUBLIC_IP"
echo ""

# Step 2: Update nginx.conf
echo "📝 Updating nginx configuration..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/yourdomain\.com/$DOMAIN/g" infrastructure/nginx.conf
else
    sed -i "s/yourdomain\.com/$DOMAIN/g" infrastructure/nginx.conf
fi
echo "✅ nginx.conf updated"

# Step 3: Update SSL script
echo "🔐 Updating SSL certificate script..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/yourdomain\.com/$DOMAIN/g" scripts/setup-ssl.sh
    sed -i '' "s/your-email@example\.com/$EMAIL/g" scripts/setup-ssl.sh
else
    sed -i "s/yourdomain\.com/$DOMAIN/g" scripts/setup-ssl.sh
    sed -i "s/your-email@example\.com/$EMAIL/g" scripts/setup-ssl.sh
fi
echo "✅ SSL script updated"

# Step 4: Summary
echo ""
echo "🎯 Next Steps:"
echo ""
echo "1️⃣ Update Hostinger DNS Records:"
echo "   Go to: Domains → $DOMAIN → DNS"
echo "   Add these records:"
echo ""
echo "   Type | Name      | Value           | TTL"
echo "   -----|-----------|-----------------|-----"
echo "   A    | @         | $PUBLIC_IP      | 3600"
echo "   A    | www       | $PUBLIC_IP      | 3600"
echo "   A    | *         | $PUBLIC_IP      | 3600"
echo ""
echo "2️⃣ Configure Router Port Forwarding:"
echo "   Forward External 80, 443 → Local Machine Port 80, 443"
echo "   Get your local IP:"
echo ""
if [[ "$OSTYPE" == "darwin"* ]]; then
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
else
    LOCAL_IP=$(hostname -I | awk '{print $1}')
fi
echo "   Local IP: $LOCAL_IP"
echo ""
echo "3️⃣ Generate SSL Certificates:"
echo ""
echo "   chmod +x scripts/setup-ssl.sh"
echo "   ./scripts/setup-ssl.sh"
echo ""
echo "4️⃣ Start Docker Services:"
echo ""
echo "   docker-compose up -d"
echo ""
echo "5️⃣ Test Your Setup:"
echo ""
echo "   # Wait 24 hours for DNS to propagate, then:"
echo "   curl https://$DOMAIN"
echo "   curl https://app1.$DOMAIN/api/v1/health"
echo ""
echo "✨ Configuration complete!"
echo ""
echo "📊 Check DNS Propagation:"
echo "   https://www.whatsmydns.net/?d=$DOMAIN"
echo ""
