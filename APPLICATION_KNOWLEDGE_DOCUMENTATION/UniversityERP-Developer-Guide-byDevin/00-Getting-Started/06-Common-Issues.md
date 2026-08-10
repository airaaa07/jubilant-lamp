# Common Issues and Solutions

## Overview

This document provides comprehensive solutions to common issues encountered during development, deployment, and operation of the University ERP system. Each issue includes symptoms, causes, and step-by-step solutions.

## Installation Issues

### Issue: Node.js Version Incompatible

**Symptom:**
```bash
npm ERR! engine Unsupported engine
npm ERR! node Unsupported engine
```

**Cause:** Node.js version doesn't meet the minimum requirement (18+).

**Solution:**
```bash
# Check current Node.js version
node --version

# Install nvm (Node Version Manager)
# macOS/Linux
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Windows
# Download from https://github.com/coreybutler/nvm-windows/releases

# Reload shell
source ~/.bashrc
# or
source ~/.zshrc

# Install Node.js 18
nvm install 18
nvm use 18

# Verify
node --version
```

### Issue: Docker Not Starting

**Symptom:**
```bash
docker: command not found
```

**Cause:** Docker is not installed or not in PATH.

**Solution:**
```bash
# Check if Docker is installed
which docker

# Install Docker
# macOS
brew install --cask docker

# Linux (Ubuntu)
sudo apt update
sudo apt install docker.io docker-compose

# Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop

# Start Docker
# macOS/Windows
# Open Docker Desktop application

# Linux
sudo systemctl start docker
sudo systemctl enable docker

# Verify
docker --version
docker-compose --version
```

### Issue: Port Already in Use

**Symptom:**
```bash
Error: listen EADDRINUSE: address already in use :::3000
```

**Cause:** Port is already being used by another process.

**Solution:**
```bash
# Find process using the port
lsof -i :3000

# Output example:
# COMMAND   PID   USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
# node     12345  user   22u  IPv6  0t0    TCP    *:3000 (LISTEN)

# Kill the process
kill -9 12345

# Or use fuser (Linux)
fuser -k 3000/tcp

# Or change the port in .env file
PORT=3001
```

### Issue: npm install Fails

**Symptom:**
```bash
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Cause:** Dependency conflicts or npm cache issues.

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, use legacy peer deps
npm install --legacy-peer-deps

# Or use --force flag
npm install --force
```

## Database Issues

### Issue: Database Connection Failed

**Symptom:**
```bash
Error: Can't reach database server at `localhost:5432`
```

**Cause:** PostgreSQL is not running or connection details are incorrect.

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# If not running, start it
docker-compose up -d postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Verify connection details in .env
cat apps/core-api/.env | grep DATABASE_URL

# Should be: postgresql://postgres:postgres@localhost:5432/university_erp?schema=public

# Test connection
docker-compose exec postgres pg_isready

# Restart PostgreSQL
docker-compose restart postgres
```

### Issue: Migration Failed

**Symptom:**
```bash
Error: P3006
Migration `20240101100000_init` failed to apply cleanly to the shadow database.
```

**Cause:** Migration conflict or database schema mismatch.

**Solution:**
```bash
# Check migration status
cd apps/core-api
npx prisma migrate status

# Resolve migration conflict
npx prisma migrate resolve --applied 20240101100000_init

# Or reset database (WARNING: deletes all data)
npx prisma migrate reset

# Re-run migrations
npx prisma migrate dev

# If still failing, check migration file
cat prisma/migrations/20240101100000_init/migration.sql
```

### Issue: Seed Failed

**Symptom:**
```bash
Error: Unique constraint failed on the fields: (`email`)
```

**Cause:** Duplicate data in database or seed script error.

**Solution:**
```bash
# Reset database
cd apps/core-api
npx prisma migrate reset

# Re-seed database
npx prisma db seed

# Check seed script
cat prisma/seed.ts

# Check for duplicate data in seed script
# Ensure unique constraints are respected
```

### Issue: Prisma Client Not Generated

**Symptom:**
```bash
Error: @prisma/client did not initialize yet
```

**Cause:** Prisma Client not generated after schema changes.

**Solution:**
```bash
# Generate Prisma Client
cd apps/core-api
npx prisma generate

# Verify generation
ls node_modules/.prisma/client

# If still failing, reinstall Prisma
npm uninstall @prisma/client prisma
npm install @prisma/client prisma

# Regenerate
npx prisma generate
```

## Redis Issues

### Issue: Redis Connection Failed

**Symptom:**
```bash
Error: connect ECONNREFUSED 127.0.0.1:6379
```

**Cause:** Redis is not running or connection details are incorrect.

**Solution:**
```bash
# Check if Redis is running
docker-compose ps redis

# If not running, start it
docker-compose up -d redis

# Check Redis logs
docker-compose logs redis

# Verify connection details in .env
cat apps/core-api/.env | grep REDIS

# Should be:
# REDIS_HOST=localhost
# REDIS_PORT=6379

# Test connection
redis-cli ping

# Expected output: PONG

# Restart Redis
docker-compose restart redis
```

### Issue: Redis Memory Full

**Symptom:**
```bash
Error: OOM command not allowed when used memory > 'maxmemory'
```

**Cause:** Redis memory limit reached.

**Solution:**
```bash
# Connect to Redis
redis-cli

# Check memory usage
INFO memory

# Flush all data (WARNING: deletes all data)
FLUSHALL

# Or flush specific database
SELECT 0
FLUSHDB

# Exit
exit

# Configure Redis with maxmemory in docker-compose.yml
# Add to redis service:
# command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

## MinIO Issues

### Issue: MinIO Connection Failed

**Symptom:**
```bash
Error: Unable to connect to MinIO server
```

**Cause:** MinIO is not running or connection details are incorrect.

**Solution:**
```bash
# Check if MinIO is running
docker-compose ps minio

# If not running, start it
docker-compose up -d minio

# Check MinIO logs
docker-compose logs minio

# Verify connection details in .env
cat apps/core-api/.env | grep MINIO

# Should be:
# MINIO_ENDPOINT=localhost
# MINIO_PORT=9000
# MINIO_ACCESS_KEY=minioadmin
# MINIO_SECRET_KEY=minioadmin

# Test connection
curl http://localhost:9000/minio/health/live

# Expected output: OK

# Restart MinIO
docker-compose restart minio
```

### Issue: Bucket Not Found

**Symptom:**
```bash
Error: The specified bucket does not exist
```

**Cause:** Bucket not created in MinIO.

**Solution:**
```bash
# Open MinIO Console
# http://localhost:9001

# Login with credentials:
# Username: minioadmin
# Password: minioadmin

# Create bucket named "university-erp"

# Or create bucket using mc CLI
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/university-erp

# Verify bucket exists
mc ls local/university-erp
```

## Backend Issues

### Issue: NestJS Application Not Starting

**Symptom:**
```bash
Error: Nest can't resolve dependencies of the AuthService
```

**Cause:** Missing dependencies or incorrect module imports.

**Solution:**
```bash
# Check for missing dependencies
cd apps/core-api
npm install

# Check module imports
cat src/app.module.ts

# Ensure all modules are imported
# Ensure all providers are declared

# Check for circular dependencies
# Use circular-dependency-plugin
npm install --save-dev circular-dependency-plugin

# Add to nest-cli.json
{
  "plugins": [
    {
      "name": "circular-dependency-plugin",
      "options": {
        "cwd": process.cwd(),
        "exclude": /(node_modules|test)/,
        "failOnError": true
      }
    }
  ]
}

# Rebuild
npm run build
```

### Issue: JWT Token Invalid

**Symptom:**
```bash
Error: 401 Unauthorized
Invalid token
```

**Cause:** JWT token expired or invalid secret.

**Solution:**
```bash
# Check JWT secret in .env
cat apps/core-api/.env | grep JWT_SECRET

# Ensure JWT_SECRET is set
# Generate new secret if needed
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Update .env with new secret
JWT_SECRET=<new-secret>

# Restart application
# Login again to get new token
```

### Issue: CORS Error

**Symptom:**
```bash
Error: CORS policy: No 'Access-Control-Allow-Origin' header
```

**Cause:** CORS not configured or origin not allowed.

**Solution:**
```bash
# Check CORS configuration in .env
cat apps/core-api/.env | grep CORS_ORIGIN

# Ensure CORS_ORIGIN is set
CORS_ORIGIN=http://localhost:5173

# Or configure in main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.enableCors({
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
    credentials: true,
  });
  
  await app.listen(3000);
}
bootstrap();

# Restart application
```

## Frontend Issues

### Issue: Vite Dev Server Not Starting

**Symptom:**
```bash
Error: Failed to start dev server
```

**Cause:** Port already in use or dependency issues.

**Solution:**
```bash
# Check if port is in use
lsof -i :5173

# Kill process if needed
kill -9 <PID>

# Clear cache
cd web/admin-portal
rm -rf node_modules .vite

# Reinstall dependencies
npm install

# Start dev server
npm run dev
```

### Issue: API Request Failed

**Symptom:**
```bash
Error: Network Error
```

**Cause:** Backend not running or incorrect API URL.

**Solution:**
```bash
# Check if backend is running
curl http://localhost:3000/health

# Check API URL in .env
cat web/admin-portal/.env | grep VITE_API_URL

# Ensure VITE_API_URL is correct
VITE_API_URL=http://localhost:3000/api

# Restart frontend
npm run dev
```

### Issue: Build Failed

**Symptom:**
```bash
Error: Build failed with errors
```

**Cause:** TypeScript errors or missing dependencies.

**Solution:**
```bash
# Check TypeScript errors
cd web/admin-portal
npm run type-check

# Fix TypeScript errors

# Clear cache
rm -rf node_modules .vite dist

# Reinstall dependencies
npm install

# Rebuild
npm run build
```

## Docker Issues

### Issue: Docker Container Exits Immediately

**Symptom:**
```bash
docker-compose ps
# Shows container status as "Exited"
```

**Cause:** Container crash or configuration error.

**Solution:**
```bash
# Check container logs
docker-compose logs <service-name>

# Check for errors in logs

# Restart container
docker-compose restart <service-name>

# If still failing, rebuild container
docker-compose up -d --build <service-name>

# Check docker-compose.yml for errors
cat docker-compose.yml
```

### Issue: Docker Volume Permission Error

**Symptom:**
```bash
Error: Permission denied
```

**Cause:** Docker volume permission issue.

**Solution:**
```bash
# Check volume permissions
ls -la docker/volumes

# Fix permissions
sudo chown -R $USER:$USER docker/volumes

# Or run Docker with user namespace
# Add to docker-compose.yml:
# user: "${UID}:${GID}"

# Set environment variables
export UID=$(id -u)
export GID=$(id -g)

# Restart Docker
docker-compose down
docker-compose up -d
```

## Performance Issues

### Issue: Slow API Response

**Symptom:** API requests taking too long to respond.

**Cause:** Database query performance, lack of caching, or inefficient code.

**Solution:**
```bash
# Check database query performance
cd apps/core-api
npx prisma studio

# Enable query logging in development
# Update .env
LOG_LEVEL=debug

# Check logs for slow queries
# Add indexes to slow queries
# Example:
# npx prisma migrate dev --name add-index

# Add caching
# Implement Redis caching for frequently accessed data

# Optimize N+1 queries
# Use Prisma include/select
```

### Issue: Memory Leak

**Symptom:** Application memory usage keeps increasing.

**Cause:** Memory leak in code or unclosed connections.

**Solution:**
```bash
# Check memory usage
docker stats

# Check for memory leaks
# Use Node.js memory profiling
node --inspect apps/core-api/dist/main.js

# Open Chrome DevTools
# Go to chrome://inspect
# Connect to Node.js process
# Take memory snapshot

# Check for unclosed connections
# Ensure database connections are closed
# Ensure Redis connections are closed
# Ensure MinIO connections are closed

# Fix memory leaks
# Close connections properly
# Use connection pooling
```

## Security Issues

### Issue: Unauthorized Access

**Symptom:** Users can access resources they shouldn't.

**Cause:** Missing or incorrect authorization guards.

**Solution:**
```bash
# Check authorization guards
cat apps/core-api/src/auth/guards/roles.guard.ts

# Ensure guards are applied to routes
# Example:
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('ADMIN')
@Get('admin-only')
adminOnly() {
  return 'Admin only data';
}

# Check role assignments
npx prisma studio
# Navigate to UserRoleAssignment model

# Ensure users have correct roles
```

### Issue: SQL Injection Vulnerability

**Symptom:** Potential SQL injection vulnerability.

**Cause:** Using raw SQL without parameterization.

**Solution:**
```bash
# Check for raw SQL usage
grep -r "queryRaw\|executeRaw" apps/core-api/src

# Ensure raw SQL uses parameterization
# Bad:
await prisma.$queryRaw`SELECT * FROM users WHERE email = '${email}'`;

# Good:
await prisma.$queryRaw`SELECT * FROM users WHERE email = ${email}`;

# Use Prisma ORM instead of raw SQL when possible
```

## Deployment Issues

### Issue: Deployment Failed

**Symptom:** Deployment process fails.

**Cause:** Build errors, configuration errors, or environment issues.

**Solution:**
```bash
# Check build logs
# Review deployment logs for errors

# Check environment variables
# Ensure all required environment variables are set

# Check database connection
# Ensure database is accessible from deployment environment

# Check dependencies
# Ensure all dependencies are installed

# Test locally first
# Build and test locally before deploying
npm run build
npm run test
```

### Issue: Database Migration Failed in Production

**Symptom:** Migration fails during deployment.

**Cause:** Schema conflict or data inconsistency.

**Solution:**
```bash
# Backup production database
pg_dump production_db > backup.sql

# Check migration status
npx prisma migrate status

# Resolve migration conflict
npx prisma migrate resolve --applied <migration-name>

# Or create new migration to fix schema
npx prisma migrate dev --name fix-schema

# Test migration in staging
# Apply to production after testing
```

## Getting Help

If you encounter an issue not covered here:

1. **Check Logs**: Always check logs for error messages
2. **Search Issues**: Search existing GitHub issues
3. **Check Documentation**: Check relevant documentation
4. **Ask Team**: Ask team members for help
5. **Create Issue**: Create a new GitHub issue with details

## Reporting Issues

When reporting an issue, include:

1. **Environment**: OS, Node.js version, Docker version
2. **Error Message**: Full error message
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Logs**: Relevant logs

## Additional Resources

- [NestJS Troubleshooting](https://docs.nestjs.com/faq/troubleshooting)
- [Prisma Troubleshooting](https://www.prisma.io/docs/guides/troubleshooting)
- [React Troubleshooting](https://react.dev/learn/troubleshooting)
- [Docker Troubleshooting](https://docs.docker.com/config/troubleshooting/)
