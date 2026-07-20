# Quick Start

## Purpose

This document provides a 5-minute quick start guide to get the University ERP running on your machine. This is for experienced developers who want to get up and running quickly without reading detailed documentation.

## Why This Document Exists

**Confirmed by Code**: The installation process has multiple steps that can be overwhelming. This document condenses the essential steps into a quick reference for experienced developers.

## Where This Is Used

- **Experienced Developers**: Quick reference for installation
- **Environment Reset**: Quick re-setup after reset
- **CI/CD**: Reference for automated installation
- **Troubleshooting**: Quick verification of setup

## Prerequisites

**Required**:
- Node.js 18+
- npm 9+
- Docker 20+
- Docker Compose 2+
- Git 2+

**Verification**:
```bash
node --version  # v18.x.x
npm --version   # 9.x.x
docker --version  # 20.x.x
docker-compose --version  # 2.x.x
git --version  # 2.x.x
```

## 5-Minute Quick Start

### Step 1: Clone and Install (2 minutes)

```bash
# Clone repository
git clone <repository-url>
cd UniversityERP

# Install dependencies
npm install
```

### Step 2: Configure Environment (30 seconds)

```bash
# Copy environment file
cp .env.example .env

# Edit .env (minimal changes required for development)
# Default values work for local development
```

### Step 3: Start Docker Services (1 minute)

```bash
# Start infrastructure services
docker-compose up -d

# Verify services are running
docker-compose ps
```

### Step 4: Setup Database (1 minute)

```bash
cd apps/core-api

# Run migrations
npx prisma migrate dev

# Seed database
npx prisma db seed

cd ../..
```

### Step 5: Start Application (30 seconds)

```bash
# Terminal 1: Start Core API
cd apps/core-api
npm run start:dev

# Terminal 2: Start Admin Portal
cd web/admin-portal
npm run dev
```

### Step 6: Access Application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:3000
- **Swagger Docs**: http://localhost:3000/api (if enabled)
- **MinIO Console**: http://localhost:9001

## Verification

### Quick Health Check

```bash
# Test API health
curl http://localhost:3000/health

# Test database connection
docker-compose exec postgres pg_isready

# Test Redis connection
docker-compose exec redis redis-cli ping
```

### Expected Results

- All Docker services: "Up" status
- Core API: Running on port 3000
- Admin Portal: Running on port 5173
- Database: Migrations applied, data seeded
- API health: Returns 200 OK

## Common Commands

### Start Everything

```bash
# Start Docker services
docker-compose up -d

# Start Core API
cd apps/core-api && npm run start:dev

# Start Admin Portal (new terminal)
cd web/admin-portal && npm run dev
```

### Stop Everything

```bash
# Stop Core API (Ctrl+C)
# Stop Admin Portal (Ctrl+C)

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

# Core API logs (if running)
# View in terminal where it's running

# Admin Portal logs (if running)
# View in terminal where it's running
```

## Default Credentials

### Database

**Confirmed by Code**:
- **User**: postgres
- **Password**: postgres
- **Database**: university_erp
- **Host**: localhost
- **Port**: 5432

### MinIO

**Confirmed by Code**:
- **Access Key**: minioadmin
- **Secret Key**: minioadmin
- **Console**: http://localhost:9001

### Default User (After Seed)

**Inferred** (from seed script):
- **Email**: admin@university.edu
- **Password**: admin123
- **Role**: SUPERADMIN

**Note**: Verify actual credentials in seed script.

## Troubleshooting

### Issue: Docker Services Not Starting

**Fix**:
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

**Fix**:
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Verify DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Should be: postgresql://postgres:postgres@localhost:5432/university_erp
```

### Issue: Port Already in Use

**Fix**:
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

**Fix**:
```bash
# Clear cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

## Next Steps

After quick start:

1. **Explore the Application**: Open http://localhost:5173
2. **Read Documentation**: Proceed to detailed documentation
3. **Understand Architecture**: Read System Architecture section
4. **Learn Modules**: Explore individual modules

## Detailed Documentation

For detailed information, see:

- [01-Prerequisites.md](./01-Prerequisites.md) - Detailed prerequisites
- [02-Installation.md](./02-Installation.md) - Detailed installation
- [04-Development-Setup.md](./04-Development-Setup.md) - Development setup
- [05-Database-Setup.md](./05-Database-Setup.md) - Database setup

## Tips

### Development Tips

- **Hot Reload**: Both backend and frontend have hot-reload enabled
- **Source Maps**: Source maps are enabled for debugging
- **Docker Volumes**: Data persists across Docker restarts
- **Environment Variables**: Edit .env to change configuration

### Productivity Tips

- **Use Multiple Terminals**: One for backend, one for frontend
- **Use VS Code**: Recommended IDE with extensions
- **Use Git Branches**: Create feature branches for work
- **Commit Often**: Commit frequently to save progress

### Performance Tips

- **Use SSD**: Faster Docker operations
- **Allocate RAM**: Give Docker at least 4GB RAM
- **Close Unused Apps**: Free up resources for Docker

## Common Mistakes

### Mistake 1: Not Starting Docker Services

**Symptom**: Application fails with connection errors

**Fix**: Always run `docker-compose up -d` before starting application

### Mistake 2: Skipping Migrations

**Symptom**: Application errors about missing tables

**Fix**: Always run `npx prisma migrate dev` after pulling changes

### Mistake 3: Wrong Directory

**Symptom**: Commands fail with "command not found"

**Fix**: Ensure you're in correct directory:
- Core API: `apps/core-api`
- Admin Portal: `web/admin-portal`

## Quick Reference

### Essential Commands

```bash
# Install
npm install

# Docker
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose ps             # Check status
docker-compose logs -f        # View logs

# Database
npx prisma migrate dev        # Run migrations
npx prisma db seed            # Seed database
npx prisma migrate reset      # Reset database

# Start
npm run start:dev             # Start backend (in apps/core-api)
npm run dev                   # Start frontend (in web/admin-portal)

# Build
npm run build                 # Build all packages
```

### Essential URLs

```
Frontend:      http://localhost:5173
API:           http://localhost:3000
MinIO Console: http://localhost:9001
Swagger:       http://localhost:3000/api (if enabled)
```

### Essential Ports

```
3000: Core API
3001: CBE Engine
3002: Notification Worker
3003: Certificate Generator
5173: Admin Portal
5432: PostgreSQL
6379: Redis
9000: MinIO API
9001: MinIO Console
9200: Elasticsearch
```

## Getting Help

If you encounter issues not covered here:

1. Check [08-Common-Issues.md](./08-Common-Issues.md)
2. Check [02-Installation.md](./02-Installation.md) for detailed troubleshooting
3. Check logs for error messages
4. Ask team members for help

## Security Notes

### Development Security

- **Default Credentials**: Change default passwords before production
- **Environment Variables**: Never commit .env file
- **Secrets**: Use strong secrets in production
- **HTTPS**: Use HTTPS in production

### Quick Security Check

```bash
# Check .env is not committed
git status
# Should show .env in untracked files (not in .gitignore)

# Check for secrets in code
grep -r "password" apps/ web/ libs/
# Should not find hardcoded passwords
```

## Production Quick Start

For production deployment, see:

- [15-Deployment](../15-Deployment/README.md)
- [17-Production](../17-Production/README.md)

Production deployment requires:
- Production build
- Process manager (PM2, systemd)
- Managed database (AWS RDS, Azure Database)
- Managed Redis (ElastiCache, Azure Cache)
- Secrets manager (AWS Secrets Manager, Azure Key Vault)
- Load balancer (Nginx, cloud load balancer)
- Monitoring and logging

## Summary

This quick start guide should get you running in 5 minutes if you have all prerequisites installed. For detailed information, refer to the other documentation files in this folder.

**Status Check**:
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] Docker services running
- [ ] Database migrated
- [ ] Database seeded
- [ ] Core API running
- [ ] Admin Portal running
- [ ] Can access frontend
- [ ] Can access API

If all checks pass, you're ready to start developing!
