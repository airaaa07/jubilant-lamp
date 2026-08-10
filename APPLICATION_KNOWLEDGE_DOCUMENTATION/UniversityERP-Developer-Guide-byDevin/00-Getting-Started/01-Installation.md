# Installation Guide

## Overview

This guide provides comprehensive instructions for installing and setting up the University ERP system on your local development machine. This guide assumes you have basic knowledge of command-line operations and software development.

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
- **PostgreSQL**: Version 14 or higher (if not using Docker)
- **Redis**: Version 6 or higher (if not using Docker)

### Development Tools

**Required Development Tools:**
- **VS Code**: Recommended IDE with extensions
  - ESLint extension
  - Prettier extension
  - Prisma extension
  - Docker extension
  - GitLens extension
- **Postman** or **Insomnia**: For API testing
- **DBeaver** or **pgAdmin**: For database management
- **Redis Commander**: For Redis management (optional)

## Installation Steps

### Step 1: Clone the Repository

**Clone the repository from Git:**

```bash
# Clone the repository
git clone https://github.com/airaaa07/UniversityERP.git

# Navigate to the project directory
cd UniversityERP

# Verify the structure
ls -la
```

**Expected Output:**
```
total 48
drwxr-xr-x  12 user  staff   384 Jan  1 10:00 .
drwxr-xr-x   3 user  staff    96 Jan  1 10:00 ..
drwxr-xr-x   5 user  staff   160 Jan  1 10:00 apps
drwxr-xr-x   3 user  staff    96 Jan  1 10:00 docker
drwxr-xr-x   3 user  staff    96 Jan  1 10:00 web
-rw-r--r--   1 user  staff  2345 Jan  1 10:00 docker-compose.yml
-rw-r--r--   1 user  staff  1234 Jan  1 10:00 package.json
-rw-r--r--   1 user  staff   567 Jan  1 10:00 README.md
```

### Step 2: Install Dependencies

**Install root dependencies:**

```bash
# Install root dependencies
npm install

# Verify installation
npm list --depth=0
```

**Install backend dependencies:**

```bash
# Navigate to core-api
cd apps/core-api

# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

**Install frontend dependencies:**

```bash
# Navigate to admin-portal
cd ../../web/admin-portal

# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

### Step 3: Set Up Environment Variables

**Create environment file for core-api:**

```bash
# Navigate to core-api
cd ../../apps/core-api

# Create .env file
cp .env.example .env

# Edit .env file
nano .env
```

**Environment Variables for core-api:**

```env
# Database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/university_erp?schema=public"

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=7d

# MinIO
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USE_SSL=false
MINIO_BUCKET=university-erp

# App
PORT=3000
NODE_ENV=development

# CORS
CORS_ORIGIN=http://localhost:5173

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu
```

**Create environment file for admin-portal:**

```bash
# Navigate to admin-portal
cd ../../web/admin-portal

# Create .env file
cp .env.example .env

# Edit .env file
nano .env
```

**Environment Variables for admin-portal:**

```env
# API
VITE_API_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000

# App
VITE_APP_NAME=University ERP
VITE_APP_VERSION=1.0.0
```

### Step 4: Set Up Docker Services

**Start Docker services:**

```bash
# Navigate to project root
cd ../../

# Start Docker services
docker-compose up -d

# Verify services are running
docker-compose ps
```

**Expected Output:**
```
NAME                    COMMAND                  SERVICE             STATUS              PORTS
university-erp-db      "docker-entrypoint.s…"   postgres            running             0.0.0.0:5432->5432/tcp
university-erp-redis   "docker-entrypoint.s…"   redis               running             0.0.0.0:6379->6379/tcp
university-erp-minio   "/usr/bin/docker-ent…"   minio               running             0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp
```

### Step 5: Run Database Migrations

**Generate Prisma Client:**

```bash
# Navigate to core-api
cd apps/core-api

# Generate Prisma Client
npx prisma generate

# Verify generation
ls node_modules/.prisma/client
```

**Run database migrations:**

```bash
# Run migrations
npx prisma migrate dev --name init

# Verify migration
npx prisma migrate status
```

**Expected Output:**
```
Environment variables loaded from .env
Datasource "db": PostgreSQL database "university_erp" at "localhost:5432"

The following migration(s) have been applied:

migrations/
  └─ 20240101100000_init/
    └─ migration.sql
```

### Step 6: Seed Database (Optional)

**Seed database with initial data:**

```bash
# Seed database
npx prisma db seed

# Verify seed data
npx prisma studio
```

**This will open Prisma Studio in your browser where you can verify the seeded data.**

### Step 7: Start Development Servers

**Start backend server:**

```bash
# In apps/core-api directory
npm run start:dev
```

**Expected Output:**
```
[Nest] 12345  - [NestFactory] Starting Nest application...
[Nest] 12345  - [InstanceLoader] AppModule dependencies initialized...
[Nest] 12345  - [RoutesResolver] AppController {/}: +4ms
[Nest] 12345  - [RouterExplorer] Mapped {/, GET} route +4ms
[Nest] 12345  - [NestApplication] Nest application successfully started
```

**Start frontend server (in new terminal):**

```bash
# In web/admin-portal directory
npm run dev
```

**Expected Output:**
```
  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

## Verification

### Verify Backend

**Test backend health endpoint:**

```bash
curl http://localhost:3000/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T10:00:00.000Z",
  "uptime": 123.456
}
```

**Test backend API:**

```bash
curl http://localhost:3000/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@university.edu","password":"admin123"}'
```

### Verify Frontend

**Open browser and navigate to:**
```
http://localhost:5173
```

**You should see the University ERP login page.**

### Verify Database

**Check database connection:**

```bash
# In apps/core-api directory
npx prisma db push --accept-data-loss
```

**Open Prisma Studio:**

```bash
npx prisma studio
```

**This will open Prisma Studio in your browser at http://localhost:5555**

### Verify Redis

**Check Redis connection:**

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

**Open MinIO Console in browser:**
```
http://localhost:9001
```

**Default credentials:**
- Username: `minioadmin`
- Password: `minioadmin`

## Troubleshooting

### Common Issues

**Issue: Port already in use**

**Solution:**
```bash
# Find process using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or change the port in .env file
PORT=3001
```

**Issue: Database connection failed**

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check database logs
docker-compose logs postgres
```

**Issue: Redis connection failed**

**Solution:**
```bash
# Check if Redis is running
docker-compose ps redis

# Restart Redis
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

**Issue: npm install fails**

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules

# Reinstall
npm install
```

**Issue: Prisma migration fails**

**Solution:**
```bash
# Reset database (WARNING: This will delete all data)
npx prisma migrate reset

# Or resolve the migration conflict manually
npx prisma migrate resolve --applied 20240101100000_init
```

## Next Steps

After successful installation, proceed to:
- [Setup Guide](./02-Setup.md) - Configure the system
- [Quick Start](./03-Quick-Start.md) - Get started quickly
- [Development Environment](./04-Development-Environment.md) - Set up your development environment

## Additional Resources

- [Project README](../../README.md)
- [Docker Documentation](https://docs.docker.com/)
- [Node.js Documentation](https://nodejs.org/docs/)
- [Prisma Documentation](https://www.prisma.io/docs)
- [NestJS Documentation](https://docs.nestjs.com/)
- [React Documentation](https://react.dev/)
