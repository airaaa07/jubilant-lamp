# Installation

## Purpose

This document provides a step-by-step guide to install the University ERP system on your local machine. Follow these instructions carefully to ensure a successful installation.

## Why This Document Exists

**Confirmed by Code**: The University ERP has multiple components that must be installed in a specific order:
- Monorepo with npm workspaces
- Docker infrastructure services
- Database migrations
- Database seeding

Skipping steps or performing them out of order will result in a non-functional system.

## Where This Is Used

- **Initial Setup**: First-time installation
- **Fresh Install**: Setting up on a new machine
- **Environment Reset**: Reinstalling after corruption
- **CI/CD**: Automated installation in pipelines

## Prerequisites

**Required**: Complete [01-Prerequisites.md](./01-Prerequisites.md) before proceeding.

**Verification Checklist**:
- [ ] Node.js 18.x or higher
- [ ] npm 9.x or higher
- [ ] Docker 20.x or higher
- [ ] Docker Compose 2.x or higher
- [ ] Git 2.x or higher
- [ ] Stable internet connection

## Installation Steps

### Step 1: Clone the Repository

**Confirmed by Code**: Repository is hosted on Git.

**Action**:
```bash
# Clone the repository
git clone <repository-url>
cd UniversityERP
```

**What This Does**:
- Downloads all source code
- Creates local copy of repository
- Sets up git tracking

**Verification**:
```bash
# Verify repository structure
ls -la
# Should show: apps/, web/, libs/, docker-compose.yml, package.json, etc.
```

**Troubleshooting**:
- **Git not installed**: Install Git (see Prerequisites)
- **Permission denied**: Check directory permissions
- **Repository not found**: Verify repository URL

### Step 2: Install Dependencies

**Confirmed by Code**: Monorepo uses npm workspaces.

**Action**:
```bash
# Install all dependencies
npm install
```

**What This Does**:
- Installs root-level dependencies
- Installs all workspace dependencies (apps/*, web/*, libs/*)
- Creates node_modules directories
- Generates package-lock.json files

**Estimated Time**: 5-15 minutes (depending on internet speed)

**Verification**:
```bash
# Check node_modules exists
ls node_modules

# Check workspace dependencies
ls apps/core-api/node_modules
ls web/admin-portal/node_modules
```

**Troubleshooting**:
- **npm install fails**: Clear npm cache and retry
  ```bash
  npm cache clean --force
  rm -rf node_modules package-lock.json
  npm install
  ```
- **Permission denied**: Check directory permissions
- **Network error**: Check internet connection
- **EACCES error**: May need to fix npm permissions (Linux/macOS)
  ```bash
  sudo chown -R $(whoami) ~/.npm
  ```

### Step 3: Configure Environment Variables

**Confirmed by Code**: Environment variables are stored in `.env` file.

**Action**:
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your preferred editor
nano .env  # or vim .env, or code .env
```

**Required Variables**:
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=university_erp

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MinIO
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams

# JWT
JWT_SECRET=dev-secret-key-change-in-production
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# SMTP (optional, for email functionality)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu

# Elasticsearch
ELASTICSEARCH_NODE=http://localhost:9200

# Application
APP_URL=http://localhost:5173
API_URL=http://localhost:3000
NODE_ENV=development
PORT=3000
```

**What This Does**:
- Configures database connection
- Configures Redis connection
- Configures MinIO connection
- Configures JWT secrets
- Configures SMTP for emails
- Configures application URLs

**Security Note**:
- Never commit `.env` file to version control
- Use strong secrets in production
- Rotate secrets regularly

**Verification**:
```bash
# Verify .env file exists
ls .env

# Verify variables are set
cat .env
```

**Troubleshooting**:
- **Missing .env.example**: Create manually from documentation
- **Invalid DATABASE_URL**: Verify PostgreSQL is running
- **Invalid JWT_SECRET**: Must be non-empty string

### Step 4: Start Docker Services

**Confirmed by Code**: Infrastructure services run in Docker.

**Action**:
```bash
# Start all Docker services in background
docker-compose up -d

# View service status
docker-compose ps
```

**What This Does**:
- Starts PostgreSQL database
- Starts Redis cache
- Starts MinIO object storage
- Starts Elasticsearch search engine
- Creates Docker volumes for data persistence

**Estimated Time**: 2-5 minutes (first run downloads images)

**Expected Output**:
```
NAME                    STATUS              PORTS
postgres                Up                  0.0.0.0:5432->5432/tcp
redis                   Up                  0.0.0.0:6379->6379/tcp
minio                   Up                  0.0.0.0:9000->9000/tcp, 0.0.0.0:9001->9001/tcp
elasticsearch           Up                  0.0.0.0:9200->9200/tcp
```

**Verification**:
```bash
# Check all services are running
docker-compose ps

# Check service logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs minio
docker-compose logs elasticsearch
```

**Troubleshooting**:
- **Docker not running**: Start Docker Desktop or Docker daemon
- **Port conflicts**: Stop conflicting processes or change ports
- **Image pull failed**: Check internet connection, retry
- **Permission denied**: Check Docker permissions (add user to docker group)

### Step 5: Wait for Services to Be Healthy

**Confirmed by Code**: Docker services have health checks.

**Action**:
```bash
# Wait for services to be healthy (30-60 seconds)
# Check health status
docker-compose ps
# All services should show "Up" (not "Exited" or "Restarting")
```

**What This Does**:
- Ensures services are fully initialized
- Prevents connection errors during migration

**Verification**:
```bash
# Test PostgreSQL connection
docker-compose exec postgres pg_isready

# Test Redis connection
docker-compose exec redis redis-cli ping

# Test MinIO connection
curl http://localhost:9000/minio/health/live

# Test Elasticsearch connection
curl http://localhost:9200/_cluster/health
```

**Expected Output**:
```
# PostgreSQL
postgres:5432 - accepting connections

# Redis
PONG

# MinIO
# (HTTP 200 response)

# Elasticsearch
# (JSON response with cluster health)
```

**Troubleshooting**:
- **PostgreSQL not ready**: Wait longer, check logs
- **Redis not ready**: Wait longer, check logs
- **MinIO not ready**: Wait longer, check logs
- **Elasticsearch not ready**: Wait longer, check logs

### Step 6: Run Database Migrations

**Confirmed by Code**: Prisma manages database migrations.

**Action**:
```bash
cd apps/core-api

# Run pending migrations
npx prisma migrate dev

# Return to root directory
cd ../..
```

**What This Does**:
- Applies all pending database migrations
- Creates database tables
- Creates indexes
- Creates foreign keys
- Updates Prisma Client

**Estimated Time**: 1-3 minutes

**Expected Output**:
```
Environment variables loaded from .env
Prisma schema loaded from prisma/schema.prisma

Datasource "db" - PostgreSQL
Database URL: "postgresql://postgres:postgres@localhost:5432/university_erp"

The following migration(s) have been applied:

migrations/
  └─ 20240101000000_init/
    └─ migration.sql

Applying migration `20240101000000_init`
The migration `20240101000000_init` has been applied.
```

**Verification**:
```bash
# Check migration status
cd apps/core-api
npx prisma migrate status

# Should show all migrations as "Applied"
```

**Troubleshooting**:
- **DATABASE_URL invalid**: Check .env file
- **PostgreSQL not running**: Check Docker status
- **Migration conflict**: May need to resolve migration conflict
- **Permission denied**: Check database permissions

### Step 7: Seed Database

**Confirmed by Code**: Prisma seed script populates initial data.

**Action**:
```bash
cd apps/core-api

# Run seed script
npx prisma db seed

# Return to root directory
cd ../..
```

**What This Does**:
- Populates database with initial data
- Creates default universities
- Creates default institutes
- Creates default departments
- Creates default users
- Creates default configurations

**Estimated Time**: 1-2 minutes

**Expected Output**:
```
Environment variables loaded from .env
Seeding database...
✓ Seeded universities
✓ Seeded institutes
✓ Seeded departments
✓ Seeded users
✓ Seeded configurations
Seed completed successfully.
```

**Verification**:
```bash
# Connect to database
docker-compose exec postgres psql -U postgres -d university_erp

# Count tables
\dt
# Should show 100+ tables

# Count universities
SELECT COUNT(*) FROM "University";

# Count users
SELECT COUNT(*) FROM "User";

# Disconnect
\q
```

**Troubleshooting**:
- **Seed script fails**: Check seed script for errors
- **Data already exists**: Seed script should be idempotent
- **Foreign key errors**: Ensure migrations ran成功

### Step 8: Verify Installation

**Confirmed by Code**: Verification steps ensure system is working.

**Action**:
```bash
# Start Core API
cd apps/core-api
npm run start:dev

# In another terminal, start Admin Portal
cd web/admin-portal
npm run dev
```

**What This Does**:
- Starts backend API server
- Starts frontend development server
- Verifies both can connect to database and Redis

**Expected Output**:

**Core API**:
```
[Nest] 12345  - [Date]     LOG [NestFactory] Starting Nest application...
[Nest] 12345  - [Date]     LOG [InstanceLoader] AppModule dependencies initialized
...
[Nest] 12345  - [Date]     LOG [NestApplication] Nest application successfully started
```

**Admin Portal**:
```
  VITE v5.x.x  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Verification**:
```bash
# Test Core API health
curl http://localhost:3000/health

# Test Admin Portal
# Open browser to http://localhost:5173
```

**Troubleshooting**:
- **Core API fails to start**: Check logs, verify database connection
- **Admin Portal fails to start**: Check logs, verify API URL
- **Connection refused**: Check if services are running

### Step 9: Stop Services (Optional)

**Action**:
```bash
# Stop Core API (Ctrl+C in terminal)
# Stop Admin Portal (Ctrl+C in terminal)

# Stop Docker services
docker-compose down
```

**What This Does**:
- Stops all running services
- Keeps Docker volumes for data persistence

**Note**: Use `docker-compose down -v` to remove volumes (deletes all data)

## Post-Installation Steps

### Generate Prisma Client

**Action**:
```bash
cd apps/core-api
npx prisma generate
```

**What This Does**:
- Generates Prisma Client based on schema
- Required for TypeScript type safety

### Build Project

**Action**:
```bash
# Build all packages
npm run build
```

**What This Does**:
- Compiles TypeScript to JavaScript
- Creates dist/ directories
- Prepares for production deployment

## Installation Verification

### Complete Verification Checklist

- [ ] Repository cloned successfully
- [ ] Dependencies installed (npm install)
- [ ] Environment variables configured (.env file)
- [ ] Docker services running (docker-compose up -d)
- [ ] All services healthy (docker-compose ps)
- [ ] Database migrations applied (npx prisma migrate dev)
- [ ] Database seeded (npx prisma db seed)
- [ ] Core API starts successfully (npm run start:dev)
- [ ] Admin Portal starts successfully (npm run dev)
- [ ] Can access API at http://localhost:3000
- [ ] Can access frontend at http://localhost:5173

### Automated Verification Script

**Status**: Not implemented

**Proposal**: Create automated verification script:

```bash
./verify-installation.sh
```

This script would:
- Check all services are running
- Test database connection
- Test Redis connection
- Test MinIO connection
- Test Elasticsearch connection
- Test API health endpoint
- Report overall status

## Uninstallation

### Complete Uninstallation

**Action**:
```bash
# Stop Docker services
docker-compose down

# Remove Docker volumes (deletes all data)
docker-compose down -v

# Remove Docker images
docker-compose down --rmi all

# Remove node_modules
rm -rf node_modules
rm -rf apps/*/node_modules
rm -rf web/*/node_modules
rm -rf libs/*/node_modules

# Remove package-lock files
rm -rf package-lock.json
rm -rf apps/*/package-lock.json
rm -rf web/*/package-lock.json
rm -rf libs/*/package-lock.json

# Remove dist directories
rm -rf apps/*/dist
rm -rf web/*/dist
rm -rf libs/*/dist

# Remove .env file
rm .env
```

**Warning**: This deletes all data. Use with caution.

### Partial Uninstallation

**Action**:
```bash
# Stop Docker services only
docker-compose down

# Remove node_modules only
rm -rf node_modules apps/*/node_modules web/*/node_modules libs/*/node_modules
```

## Common Issues

### Issue 1: npm install Fails

**Symptom**: `npm install` fails with errors

**Possible Causes**:
- Node.js version too old
- npm version too old
- Network issues
- Permission issues
- Corrupted cache

**Investigation**:
```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# Check network
ping registry.npmjs.org

# Check permissions
ls -la
```

**Fix**:
```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue 2: Docker Services Fail to Start

**Symptom**: `docker-compose up -d` fails

**Possible Causes**:
- Docker not running
- Port conflicts
- Insufficient resources
- Permission issues

**Investigation**:
```bash
# Check Docker status
docker ps

# Check Docker logs
docker-compose logs

# Check port conflicts
lsof -i :5432
lsof -i :6379
lsof -i :9000
lsof -i :9200
```

**Fix**:
```bash
# Start Docker
# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop

# Stop conflicting processes
kill -9 <PID>

# Restart Docker services
docker-compose down
docker-compose up -d
```

### Issue 3: Database Migration Fails

**Symptom**: `npx prisma migrate dev` fails

**Possible Causes**:
- PostgreSQL not running
- Invalid DATABASE_URL
- Migration conflict
- Permission issues

**Investigation**:
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Check DATABASE_URL
cat .env | grep DATABASE_URL

# Test connection
docker-compose exec postgres psql -U postgres -d university_erp
```

**Fix**:
```bash
# Ensure PostgreSQL is running
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
docker-compose exec postgres pg_isready

# Verify DATABASE_URL
# Should match: postgresql://postgres:postgres@localhost:5432/university_erp

# Reset database (WARNING: deletes all data)
docker-compose exec postgres psql -U postgres -d university_erp -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
npx prisma migrate dev
```

### Issue 4: Seed Script Fails

**Symptom**: `npx prisma db seed` fails

**Possible Causes**:
- Migrations not applied
- Invalid data in seed script
- Foreign key violations
- Permission issues

**Investigation**:
```bash
# Check migration status
npx prisma migrate status

# Check seed script
cat prisma/seed.ts
```

**Fix**:
```bash
# Ensure migrations are applied
npx prisma migrate dev

# Reset and reseed
npx prisma migrate reset
npx prisma db seed
```

### Issue 5: Core API Fails to Start

**Symptom**: `npm run start:dev` fails

**Possible Causes**:
- Database not running
- Redis not running
- Invalid environment variables
- Port conflicts

**Investigation**:
```bash
# Check database
docker-compose ps postgres

# Check Redis
docker-compose ps redis

# Check environment variables
cat .env

# Check port
lsof -i :3000
```

**Fix**:
```bash
# Ensure services are running
docker-compose up -d postgres redis

# Verify environment variables
# Ensure DATABASE_URL, REDIS_HOST, etc. are correct

# Stop conflicting process
kill -9 <PID>

# Restart Core API
npm run start:dev
```

## Performance Considerations

### Installation Performance

**Optimization Tips**:
- Use SSD for faster Docker operations
- Use wired network for faster downloads
- Use npm cache to avoid re-downloading
- Use Docker build cache for faster rebuilds

### Resource Usage

**Expected Resource Usage**:
- **RAM**: 4-8GB (Docker services + Node.js)
- **Disk**: 10-20GB (Docker images + node_modules + database)
- **CPU**: Moderate during installation, low during idle

## Security Considerations

### Installation Security

- **Verify repository**: Ensure repository is from trusted source
- **Review .env.example**: Understand what variables are needed
- **Use strong secrets**: Generate strong JWT_SECRET
- **Don't commit .env**: Add .env to .gitignore
- **Scan for vulnerabilities**: Run `npm audit` after installation

### Post-Installation Security

- **Change default passwords**: Change PostgreSQL, Redis, MinIO passwords
- **Enable authentication**: Enable Redis authentication
- **Use HTTPS**: Use HTTPS in production
- **Rotate secrets**: Rotate secrets regularly
- **Update dependencies**: Keep dependencies updated

## Future Enhancements

### Automated Installation Script

**Status**: Not implemented

**Proposal**: Create automated installation script:

```bash
./install.sh
```

This script would:
- Check prerequisites
- Install dependencies
- Configure environment
- Start Docker services
- Run migrations
- Seed database
- Verify installation
- Report status

### Docker Compose Profiles

**Status**: Not implemented

**Proposal**: Use Docker Compose profiles for different setups:

```bash
# Minimal setup (PostgreSQL + Redis only)
docker-compose --profile minimal up

# Full setup (all services)
docker-compose --profile full up

# Development setup (with dev tools)
docker-compose --profile dev up
```

## Production Considerations

### Production Installation

Production installation differs from development:

1. **Use production build**: `npm run build` instead of `npm run start:dev`
2. **Use process manager**: Use PM2 or systemd instead of running directly
3. **Use production database**: Use managed PostgreSQL (AWS RDS, Azure Database)
4. **Use production Redis**: Use managed Redis (ElastiCache, Azure Cache)
5. **Use production secrets**: Use secrets manager (AWS Secrets Manager, Azure Key Vault)
6. **Use HTTPS**: Configure SSL/TLS certificates
7. **Use load balancer**: Use Nginx or cloud load balancer
8. **Use monitoring**: Set up monitoring and alerting

### Production Environment Variables

Production environment variables should:
- Use strong secrets
- Use production database URLs
- Use production Redis URLs
- Use production MinIO URLs
- Use production SMTP credentials
- Be stored in secrets manager
- Not be committed to version control

## Next Steps

After successful installation:

1. Proceed to [03-Quick-Start.md](./03-Quick-Start.md) for quick start guide
2. Or proceed to [04-Development-Setup.md](./04-Development-Setup.md) for detailed development setup
3. Then proceed to System Architecture documentation

## Related Documentation

- [01-Prerequisites.md](./01-Prerequisites.md) - Prerequisites
- [03-Quick-Start.md](./03-Quick-Start.md) - Quick start guide
- [04-Development-Setup.md](./04-Development-Setup.md) - Development setup
- [05-Database-Setup.md](./05-Database-Setup.md) - Database setup
- [08-Common-Issues.md](./08-Common-Issues.md) - Common issues
