# Quick Start Guide

## Overview

This guide provides a comprehensive quick start to get the University ERP running on your machine. This guide is designed for developers who want to get up and running quickly while still understanding the system architecture and components.

## Prerequisites

### System Requirements

**Hardware Requirements:**
- CPU: 4 cores or higher recommended
- RAM: 16GB minimum, 32GB recommended
- Storage: 50GB free space minimum
- Network: Stable internet connection for downloading dependencies

**Software Requirements:**
- **Operating System**: Linux (Ubuntu 20.04+ recommended), macOS (10.15+), or Windows 10+ with WSL2
- **Node.js**: Version 18.x or higher (LTS recommended)
- **npm**: Version 9.x or higher (comes with Node.js)
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.x or higher
- **Git**: Version 2.x or higher

### Verification

```bash
# Verify Node.js
node --version  # Should be v18.x.x or higher

# Verify npm
npm --version   # Should be 9.x.x or higher

# Verify Docker
docker --version  # Should be 20.x.x or higher

# Verify Docker Compose
docker-compose --version  # Should be 2.x.x or higher

# Verify Git
git --version  # Should be 2.x.x or higher
```

## Quick Start Steps

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/UniversityERP.git

# Navigate to the project directory
cd UniversityERP

# Verify the structure
ls -la
```

**Expected Structure:**
```
UniversityERP/
├── apps/
│   ├── core-api/
│   └── cbe-engine/
├── web/
│   ├── admin-portal/
│   └── student-portal/
├── docker/
├── libs/
├── docker-compose.yml
├── package.json
└── README.md
```

### Step 2: Install Dependencies

```bash
# Install root dependencies
npm install

# Install backend dependencies
cd apps/core-api
npm install

# Install frontend dependencies
cd ../../web/admin-portal
npm install

# Return to project root
cd ../..
```

### Step 3: Configure Environment

```bash
# Copy environment file for core-api
cp apps/core-api/.env.example apps/core-api/.env

# Copy environment file for admin-portal
cp web/admin-portal/.env.example web/admin-portal/.env

# Edit environment files as needed
# Default values work for local development
```

**Key Environment Variables:**

**core-api/.env:**
```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/university_erp?schema=public"
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
PORT=3000
NODE_ENV=development
```

**admin-portal/.env:**
```env
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000
VITE_APP_NAME=University ERP
```

### Step 4: Start Docker Services

```bash
# Start Docker services
docker-compose up -d

# Verify services are running
docker-compose ps
```

**Expected Output:**
```
NAME                    STATUS              PORTS
university-erp-db      running             0.0.0.0:5432->5432/tcp
university-erp-redis   running             0.0.0.0:6379->6379/tcp
university-erp-minio   running             0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp
```

### Step 5: Setup Database

```bash
# Navigate to core-api
cd apps/core-api

# Generate Prisma Client
npx prisma generate

# Run database migrations
npx prisma migrate dev --name init

# Seed database with initial data
npx prisma db seed

# Return to project root
cd ../..
```

### Step 6: Start Development Servers

**Terminal 1 - Start Core API:**
```bash
cd apps/core-api
npm run start:dev
```

**Terminal 2 - Start Admin Portal:**
```bash
cd web/admin-portal
npm run dev
```

### Step 7: Access Application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:3000
- **Health Check**: http://localhost:3000/health
- **MinIO Console**: http://localhost:9001
- **Prisma Studio**: http://localhost:5555 (run `npx prisma studio` in apps/core-api)

## Verification

### Verify Backend

```bash
# Test health endpoint
curl http://localhost:3000/health

# Expected response:
# {
#   "status": "ok",
#   "timestamp": "2024-01-01T10:00:00.000Z",
#   "uptime": 123.456
# }
```

### Verify Frontend

Open browser and navigate to http://localhost:5173

**You should see the University ERP login page.**

### Verify Database

```bash
# In apps/core-api directory
npx prisma studio

# This will open Prisma Studio in your browser
# Verify that tables exist and data is seeded
```

### Verify Redis

```bash
# Connect to Redis
redis-cli

# Test connection
ping
# Expected output: PONG

# Exit
exit
```

### Verify MinIO

Open MinIO Console in browser: http://localhost:9001

**Default credentials:**
- Username: `minioadmin`
- Password: `minioadmin`

## Default Credentials

### Database

- **User**: postgres
- **Password**: postgres
- **Database**: university_erp
- **Host**: localhost
- **Port**: 5432

### MinIO

- **Access Key**: minioadmin
- **Secret Key**: minioadmin
- **Console**: http://localhost:9001

### Default User (After Seed)

- **Email**: admin@university.edu
- **Password**: admin123
- **Role**: ADMIN

## Common Commands

### Start Everything

```bash
# Start Docker services
docker-compose up -d

# Start Core API (Terminal 1)
cd apps/core-api && npm run start:dev

# Start Admin Portal (Terminal 2)
cd web/admin-portal && npm run dev
```

### Stop Everything

```bash
# Stop Core API (Ctrl+C in Terminal 1)
# Stop Admin Portal (Ctrl+C in Terminal 2)

# Stop Docker services
docker-compose down
```

### Reset Database

```bash
# Reset database (WARNING: deletes all data)
cd apps/core-api
npx prisma migrate reset
npx prisma db seed
```

### View Logs

```bash
# Docker logs
docker-compose logs -f

# Core API logs (view in terminal where it's running)
# Admin Portal logs (view in terminal where it's running)
```

## Troubleshooting

### Issue: Docker Services Not Starting

**Fix:**
```bash
# Restart Docker
# Linux
sudo systemctl restart docker

# macOS/Windows
# Restart Docker Desktop

# Re-start services
docker-compose down
docker-compose up -d
```

### Issue: Database Connection Failed

**Fix:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check database logs
docker-compose logs postgres
```

### Issue: Port Already in Use

**Fix:**
```bash
# Find process using port
lsof -i :3000  # Core API
lsof -i :5173  # Admin Portal

# Kill process
kill -9 <PID>

# Or change port in .env
PORT=3001
```

### Issue: npm install Fails

**Fix:**
```bash
# Clear cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

## Next Steps

After successful quick start:

1. **Explore the Application**: Open http://localhost:5173
2. **Read Documentation**: Proceed to detailed documentation
3. **Understand Architecture**: Read System Architecture section
4. **Learn Modules**: Explore individual modules
5. **Start Developing**: Start building features

## Additional Resources

- [Installation Guide](./01-Installation.md) - Detailed installation instructions
- [Setup Guide](./02-Setup.md) - System configuration
- [Development Environment](./04-Development-Environment.md) - Development environment setup
- [Project Structure](./05-Project-Structure.md) - Project structure overview
