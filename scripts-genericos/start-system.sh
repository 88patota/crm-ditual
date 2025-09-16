#!/bin/bash

# CRM System Startup Script
echo "🚀 Starting CRM System..."

# Stop any existing containers
echo "📦 Stopping existing containers..."
docker compose down

# Build and start all services
echo "🔨 Building and starting all services..."
docker compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Show status
echo "📊 Container status:"
docker compose ps

echo ""
echo "✅ CRM System started successfully!"
echo ""
echo "🌐 Access points:"
echo "   Frontend:     http://localhost:3000"
echo "   API Gateway:  http://localhost:8000"
echo "   User Service: http://localhost:8001"
echo "   Budget Service: http://localhost:8002"
echo "   PostgreSQL:   localhost:5432"
echo "   Redis:        localhost:6379"
echo ""
echo "📋 To view logs:"
echo "   docker compose logs -f [service_name]"
echo ""
echo "🛑 To stop the system:"
echo "   docker compose down"
