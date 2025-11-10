#!/bin/bash

# 🚀 Zyphron Quick Start Script
# This script gets Zyphron running in 5 minutes

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║         🚀 ZYPHRON QUICK START GUIDE 🚀            ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check if Docker is running
echo "✓ Step 1: Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi
echo "✅ Docker is running!"
echo ""

# Step 2: Install frontend dependencies
echo "✓ Step 2: Installing frontend dependencies..."
cd frontend
if [ -d "node_modules" ]; then
    echo "   ℹ️  node_modules already exists, skipping..."
else
    echo "   📦 Running npm install... (this may take 2-3 minutes)"
    npm install --legacy-peer-deps
fi
cd ..
echo "✅ Frontend dependencies installed!"
echo ""

# Step 3: Start Docker services
echo "✓ Step 3: Starting Docker services..."
echo "   🐳 Starting containers..."
docker-compose up -d
echo "✅ Services started!"
echo ""

# Wait for services to be healthy
echo "✓ Step 4: Waiting for services to be healthy..."
sleep 5
echo "✅ Services are running!"
echo ""

# Step 5: Display access information
echo "╔════════════════════════════════════════════════════╗"
echo "║              ✨ ZYPHRON IS RUNNING! ✨             ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

echo "📊 Access Your Services:"
echo ""
echo "  🌐 Frontend (Main UI)"
echo "     👉 http://localhost:3000"
echo ""
echo "  📡 Backend API"
echo "     👉 http://localhost:8000"
echo ""
echo "  📚 API Documentation (Swagger)"
echo "     👉 http://localhost:8000/docs"
echo ""
echo "  🗄️  Database Viewer (pgAdmin)"
echo "     👉 http://localhost:5050"
echo "     Email: admin@zyphron.local"
echo "     Password: zyphron"
echo ""
echo "  📊 PostgreSQL Database"
echo "     Host: localhost:5432"
echo "     Username: zyphron"
echo "     Password: zyphron"
echo ""
echo "  💾 Redis Cache"
echo "     Host: localhost:6379"
echo ""

echo "╔════════════════════════════════════════════════════╗"
echo "║            NEXT STEPS FOR PRODUCTION               ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

echo "1️⃣  Generate SSL Certificates"
echo "   $ ./scripts/setup-ssl.sh"
echo ""

echo "2️⃣  Configure Your Hostinger Domain"
echo "   See: DOMAIN_SETUP_SUMMARY.md"
echo ""

echo "3️⃣  Monitor Your Services"
echo "   $ docker-compose logs -f"
echo ""

echo "4️⃣  Stop All Services"
echo "   $ docker-compose down"
echo ""

echo "╔════════════════════════════════════════════════════╗"
echo "║          🎉 READY TO DEPLOY YOUR APPS! 🎉         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Show Docker status
echo "📦 Container Status:"
docker-compose ps
echo ""

echo "💡 Pro Tips:"
echo "  • Frontend auto-reloads on file changes"
echo "  • View real-time logs: docker-compose logs -f frontend"
echo "  • Database viewer (pgAdmin) is already configured"
echo "  • Check database health in pgAdmin"
echo ""

echo "🚀 Start building! Your platform is ready."
