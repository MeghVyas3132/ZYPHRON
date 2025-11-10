#!/bin/bash

# Setup SSL Certificates for your Hostinger domain
# Run this script to generate and manage Let's Encrypt certificates

set -e

DOMAIN="yourdomain.com"
EMAIL="your-email@example.com"
CERT_DIR="./infrastructure/certs"

echo "🔐 Setting up SSL certificates for $DOMAIN"

# Create cert directory
mkdir -p "$CERT_DIR/live/$DOMAIN"
mkdir -p "$CERT_DIR/archive/$DOMAIN"

# Install Certbot if not already installed
if ! command -v certbot &> /dev/null; then
    echo "📦 Installing Certbot..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install certbot
    else
        # Linux
        sudo apt-get update
        sudo apt-get install -y certbot python3-certbot-nginx
    fi
fi

# Generate certificate
echo "📝 Generating Let's Encrypt certificate..."
certbot certonly \
    --standalone \
    --non-interactive \
    --agree-tos \
    -m "$EMAIL" \
    -d "$DOMAIN" \
    -d "*.$DOMAIN" \
    -d "www.$DOMAIN"

# Copy certificates to infrastructure folder
echo "📋 Copying certificates..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    CERT_SOURCE="/opt/homebrew/etc/letsencrypt"
else
    CERT_SOURCE="/etc/letsencrypt"
fi

cp -r "$CERT_SOURCE/live/$DOMAIN/" "$CERT_DIR/live/" || true
cp -r "$CERT_SOURCE/archive/$DOMAIN/" "$CERT_DIR/archive/" || true

echo "✅ SSL setup complete!"
echo ""
echo "Next steps:"
echo "1. Update infrastructure/nginx.conf - Replace 'yourdomain.com' with your actual domain"
echo "2. Update docker-compose.yml if needed"
echo "3. Run: docker-compose up -d"
echo ""
echo "🔄 To renew certificates (run monthly):"
echo "   certbot renew"
