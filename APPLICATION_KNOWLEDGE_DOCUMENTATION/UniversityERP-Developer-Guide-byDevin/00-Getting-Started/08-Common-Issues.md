# Common Issues

## Purpose

This document provides solutions to common issues encountered during setup and development of the University ERP system. Use this as a first reference when encountering problems.

## Why This Document Exists

**Confirmed by Code**: The University ERP has multiple components that can fail. Common issues include:
- Docker service failures
- Database connection issues
- Dependency conflicts
- Port conflicts
- Environment variable issues

This document exists to provide quick solutions to these common problems.

## Where This Is Used

- **Troubleshooting**: First reference when issues occur
- **Onboarding**: New developers encounter common issues
- **Environment Reset**: Issues after environment reset
- **Production**: Production issues (with production-specific solutions)

## Issue Categories

### Docker Issues

### Issue 1: Docker Services Fail to Start

**Symptom**:
```bash
docker-compose up -d
# Services show "Exited" or "Restarting"
```

**Possible Causes**:
- Docker daemon not running
- Port conflicts
- Insufficient resources
- Permission issues
- Corrupted Docker images

**Investigation**:
```bash
# Check Docker status
docker ps

# Check Docker logs
docker-compose logs

# Check specific service logs
docker-compose logs postgres
docker-compose logs redis
docker-compose logs minio
docker-compose logs elasticsearch
```

**Solutions**:

**Solution 1: Restart Docker**
```bash
# Linux
sudo systemctl restart docker

# macOS/Windows
# Restart Docker Desktop application
```

**Solution 2: Check Port Conflicts**
```bash
# Find process using port
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :9000  # MinIO
lsof -i :9200  # Elasticsearch

# Kill process
kill -9 <PID>

# Or change port in .env
```

**Solution 3: Check Resources**
```bash
# Check Docker resources
docker stats

# Allocate more RAM to Docker
# Docker Desktop > Settings > Resources
```

**Solution 4: Fix Permissions**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in
```

**Solution 5: Remove and Recreate**
```bash
# Stop services
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Restart
docker-compose up -d
```

### Issue 2: Docker Image Pull Fails

**Symptom**:
```bash
docker-compose up -d
# Error: failed to pull image
```

**Possible Causes**:
- Network issues
- Docker registry down
- Authentication issues
- Insufficient disk space

**Investigation**:
```bash
# Check network
ping registry-1.docker.io

# Check disk space
df -h

# Check Docker disk usage
docker system df
```

**Solutions**:

**Solution 1: Retry**
```bash
docker-compose pull
docker-compose up -d
```

**Solution 2: Clear Docker Cache**
```bash
docker system prune -a
docker-compose up -d
```

**Solution 3: Use Different Registry**
```bash
# Edit docker-compose.yml
# Change image to use different registry
```

**Solution 4: Free Disk Space**
```bash
# Remove unused images
docker image prune -a

# Remove unused containers
docker container prune

# Remove unused volumes
docker volume prune
```

### Issue 3: Docker Volume Permission Denied

**Symptom**:
```bash
docker-compose up -d
# Error: permission denied
```

**Possible Causes**:
- Volume mounted with wrong permissions
- User not in docker group
- SELinux issues (Linux)

**Investigation**:
```bash
# Check volume permissions
ls -la docker-volumes/

# Check docker group
groups
```

**Solutions**:

**Solution 1: Fix Permissions**
```bash
# Fix volume permissions
sudo chown -R $USER:$USER docker-volumes/
```

**Solution 2: Disable SELinux**
```bash
# Temporary
sudo setenforce 0

# Permanent
# Edit /etc/selinux/config
# Set SELINUX=permissive
```

**Solution 3: Use Docker User**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
```

## Database Issues

### Issue 4: Database Connection Failed

**Symptom**:
```bash
# Application logs
Error: Can't reach database server
```

**Possible Causes**:
- PostgreSQL not running
- Invalid DATABASE_URL
- Network issues
- Firewall blocking

**Investigation**:
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Test connection
docker-compose exec postgres pg_isready

# Check DATABASE_URL
cat .env | grep DATABASE_URL
```

**Solutions**:

**Solution 1: Start PostgreSQL**
```bash
docker-compose up -d postgres

# Wait for it to be ready
docker-compose exec postgres pg_isready
```

**Solution 2: Fix DATABASE_URL**
```bash
# Edit .env
# Should be: postgresql://postgres:postgres@localhost:5432/university_erp
```

**Solution 3: Check Firewall**
```bash
# Allow PostgreSQL port
sudo ufw allow 5432
```

**Solution 4: Test Connection Manually**
```bash
docker-compose exec postgres psql -U postgres -d university_erp
```

### Issue 5: Migration Failed

**Symptom**:
```bash
npx prisma migrate dev
# Error: Migration failed
```

**Possible Causes**:
- Schema conflict
- Migration conflict
- Database lock
- Permission issues

**Investigation**:
```bash
# Check migration status
npx prisma migrate status

# Check database logs
docker-compose logs postgres
```

**Solutions**:

**Solution 1: Resolve Conflict**
```bash
# Check migration files
ls prisma/migrations/

# Manually resolve conflict in migration SQL
```

**Solution 2: Reset Database**
```bash
# WARNING: Deletes all data
npx prisma migrate reset
```

**Solution 3: Create New Migration**
```bash
# Resolve schema conflict
# Create new migration
npx prisma migrate dev --name fix_conflict
```

**Solution 4: Bypass Lock**
```bash
# Kill connections
docker-compose exec postgres psql -U postgres -d university_erp -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'university_erp';"
```

### Issue 6: Seed Failed

**Symptom**:
```bash
npx prisma db seed
# Error: Seed failed
```

**Possible Causes**:
- Migrations not applied
- Invalid data in seed script
- Foreign key violations
- Unique constraint violations

**Investigation**:
```bash
# Check migration status
npx prisma migrate status

# Check seed script
cat prisma/seed.ts
```

**Solutions**:

**Solution 1: Apply Migrations**
```bash
npx prisma migrate dev
```

**Solution 2: Fix Seed Script**
```bash
# Edit prisma/seed.ts
# Fix invalid data
# Re-run seed
npx prisma db seed
```

**Solution 3: Reset and Reseed**
```bash
npx prisma migrate reset
npx prisma db seed
```

## Redis Issues

### Issue 7: Redis Connection Failed

**Symptom**:
```bash
# Application logs
Error: Redis connection failed
```

**Possible Causes**:
- Redis not running
- Invalid REDIS_HOST/PORT
- Network issues
- Firewall blocking

**Investigation**:
```bash
# Check Redis status
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# Check environment variables
cat .env | grep REDIS
```

**Solutions**:

**Solution 1: Start Redis**
```bash
docker-compose up -d redis
```

**Solution 2: Fix Environment Variables**
```bash
# Edit .env
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Solution 3: Test Connection**
```bash
docker-compose exec redis redis-cli ping
# Should return PONG
```

### Issue 8: Redis Memory Full

**Symptom**:
```bash
# Application logs
Error: OOM command not allowed
```

**Possible Causes**:
- Redis maxmemory reached
- No eviction policy set

**Investigation**:
```bash
# Check Redis memory
docker-compose exec redis redis-cli INFO memory
```

**Solutions**:

**Solution 1: Clear Redis**
```bash
# WARNING: Deletes all data
docker-compose exec redis redis-cli FLUSHALL
```

**Solution 2: Set Eviction Policy**
```bash
# Edit redis.conf
maxmemory 256mb
maxmemory-policy allkeys-lru

# Restart Redis
docker-compose restart redis
```

## MinIO Issues

### Issue 9: MinIO Connection Failed

**Symptom**:
```bash
# Application logs
Error: MinIO connection failed
```

**Possible Causes**:
- MinIO not running
- Invalid MINIO_ENDPOINT
- Invalid credentials
- Network issues

**Investigation**:
```bash
# Check MinIO status
docker-compose ps minio

# Test connection
curl http://localhost:9000/minio/health/live

# Check environment variables
cat .env | grep MINIO
```

**Solutions**:

**Solution 1: Start MinIO**
```bash
docker-compose up -d minio
```

**Solution 2: Fix Environment Variables**
```bash
# Edit .env
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

**Solution 3: Test Connection**
```bash
curl http://localhost:9000/minio/health/live
```

### Issue 10: MinIO Bucket Not Found

**Symptom**:
```bash
# Application logs
Error: Bucket not found
```

**Possible Causes**:
- Bucket not created
- Incorrect bucket name
- Permission issues

**Investigation**:
```bash
# List buckets
docker-compose exec minio mc ls local
```

**Solutions**:

**Solution 1: Create Bucket**
```bash
docker-compose exec minio mc mb local/university-erp-docs
docker-compose exec minio mc mb local/university-erp-exams
```

**Solution 2: Fix Bucket Name**
```bash
# Edit .env
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams
```

## Node.js/npm Issues

### Issue 11: npm install Fails

**Symptom**:
```bash
npm install
# Error: EACCES, ENOENT, etc.
```

**Possible Causes**:
- Node.js version too old
- npm version too old
- Permission issues
- Network issues
- Corrupted cache

**Investigation**:
```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# Check permissions
ls -la
```

**Solutions**:

**Solution 1: Clear Cache**
```bash
npm cache clean --force
```

**Solution 2: Remove node_modules**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Solution 3: Fix Permissions**
```bash
# Linux/macOS
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) node_modules
```

**Solution 4: Update Node.js**
```bash
# Use nvm
nvm install 18
nvm use 18
```

**Solution 5: Use Alternative Registry**
```bash
npm install --registry=https://registry.npmjs.org
```

### Issue 12: TypeScript Compilation Errors

**Symptom**:
```bash
npm run build
# TypeScript errors
```

**Possible Causes**:
- Type errors
- Missing dependencies
- Wrong TypeScript version
- tsconfig.json issues

**Investigation**:
```bash
# Check TypeScript version
npx tsc --version

# Check tsconfig.json
cat tsconfig.json
```

**Solutions**:

**Solution 1: Fix Type Errors**
```bash
# Read error messages
# Fix type errors in code
```

**Solution 2: Install Missing Dependencies**
```bash
npm install
```

**Solution 3: Regenerate Prisma Client**
```bash
cd apps/core-api
npx prisma generate
```

**Solution 4: Check TypeScript Version**
```bash
# Ensure workspace TypeScript is used
# VS Code: Use workspace TypeScript
# WebStorm: Use workspace TypeScript
```

## Port Conflicts

### Issue 13: Port Already in Use

**Symptom**:
```bash
# Application logs
Error: Port 3000 already in use
```

**Possible Causes**:
- Another process using the port
- Previous instance not stopped
- Port conflict with another service

**Investigation**:
```bash
# Find process using port
lsof -i :3000
lsof -i :5173
lsof -i :5432
lsof -i :6379
```

**Solutions**:

**Solution 1: Kill Process**
```bash
# Kill process
kill -9 <PID>
```

**Solution 2: Change Port**
```bash
# Edit .env
PORT=3001
```

**Solution 3: Stop Previous Instance**
```bash
# Stop application
# Ctrl+C in terminal

# Or find and kill
ps aux | grep node
kill -9 <PID>
```

## Environment Variable Issues

### Issue 14: Environment Variable Not Found

**Symptom**:
```bash
# Application logs
Error: DATABASE_URL is not defined
```

**Possible Causes**:
- .env file not created
- Variable not in .env
- Variable misspelled
- .env file not loaded

**Investigation**:
```bash
# Check .env exists
ls .env

# Check variable
cat .env | grep DATABASE_URL
```

**Solutions**:

**Solution 1: Create .env**
```bash
cp .env.example .env
```

**Solution 2: Add Variable**
```bash
# Edit .env
# Add missing variable
```

**Solution 3: Check Spelling**
```bash
# Ensure variable name matches
# DATABASE_URL (not DATABASEURL)
```

**Solution 4: Restart Application**
```bash
# .env is loaded on startup
# Restart application after changes
```

## Frontend Issues

### Issue 15: Frontend Build Fails

**Symptom**:
```bash
cd web/admin-portal
npm run build
# Build failed
```

**Possible Causes**:
- TypeScript errors
- Missing dependencies
- Vite configuration issues
- Environment variable issues

**Investigation**:
```bash
# Check build logs
npm run build

# Check dependencies
npm install
```

**Solutions**:

**Solution 1: Fix TypeScript Errors**
```bash
# Read error messages
# Fix type errors
```

**Solution 2: Install Dependencies**
```bash
npm install
```

**Solution 3: Check Environment Variables**
```bash
# Check VITE_API_URL
cat .env | grep VITE_API_URL
```

**Solution 4: Clear Cache**
```bash
rm -rf node_modules .vite dist
npm install
npm run build
```

### Issue 16: Frontend Hot Reload Not Working

**Symptom**:
```bash
# Changes not reflected without manual refresh
```

**Possible Causes**:
- File watcher limits
- Vite configuration issues
- Browser cache

**Investigation**:
```bash
# Check Vite logs
npm run dev
```

**Solutions**:

**Solution 1: Increase File Watcher Limits**
```bash
# Linux
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

**Solution 2: Clear Browser Cache**
```bash
# Hard refresh in browser
# Ctrl+Shift+R (Windows/Linux)
# Cmd+Shift+R (macOS)
```

**Solution 3: Restart Dev Server**
```bash
# Stop and restart
Ctrl+C
npm run dev
```

## Backend Issues

### Issue 17: Backend Fails to Start

**Symptom**:
```bash
cd apps/core-api
npm run start:dev
# Application fails to start
```

**Possible Causes**:
- Database connection failed
- Redis connection failed
- Environment variable issues
- Port conflicts
- Code errors

**Investigation**:
```bash
# Check logs
npm run start:dev

# Check database connection
docker-compose ps postgres

# Check Redis connection
docker-compose ps redis
```

**Solutions**:

**Solution 1: Start Infrastructure Services**
```bash
docker-compose up -d postgres redis minio
```

**Solution 2: Fix Environment Variables**
```bash
# Check .env
cat .env
```

**Solution 3: Fix Port Conflict**
```bash
# Change port in .env
PORT=3001
```

**Solution 4: Check Code Errors**
```bash
# Read error messages
# Fix code errors
```

### Issue 18: API Returns 500 Error

**Symptom**:
```bash
curl http://localhost:3000/api/test
# Returns 500 Internal Server Error
```

**Possible Causes**:
- Unhandled exception
- Database error
- Validation error
- Logic error

**Investigation**:
```bash
# Check application logs
# Look for error stack traces
```

**Solutions**:

**Solution 1: Check Logs**
```bash
# Read error logs
# Identify error
# Fix error
```

**Solution 2: Check Database**
```bash
# Ensure database is running
# Ensure migrations are applied
```

**Solution 3: Check Validation**
```bash
# Ensure request data is valid
# Check DTO validation
```

## Git Issues

### Issue 19: Git Merge Conflict

**Symptom**:
```bash
git pull origin main
# CONFLICT (content): Merge conflict in file.ts
```

**Possible Causes**:
- Same file modified in both branches
- Conflicting changes

**Investigation**:
```bash
# Check conflict
git status
```

**Solutions**:

**Solution 1: Resolve Conflict**
```bash
# Edit conflicted file
# Look for <<<<<<<, =======, >>>>>>
# Choose correct version
# Remove conflict markers
git add file.ts
git commit
```

**Solution 2: Use Merge Tool**
```bash
git mergetool
```

**Solution 3: Abort Merge**
```bash
git merge --abort
```

### Issue 20: Git Push Rejected

**Symptom**:
```bash
git push origin feature
# Error: rejected
```

**Possible Causes**:
- Remote has new commits
- Force push required
- Branch protection

**Investigation**:
```bash
# Check remote status
git fetch origin
git status
```

**Solutions**:

**Solution 1: Pull First**
```bash
git pull origin main
git push origin feature
```

**Solution 2: Rebase**
```bash
git pull --rebase origin main
git push origin feature
```

**Solution 3: Force Push (Caution)**
```bash
git push --force origin feature
# Only if you know what you're doing
```

## Performance Issues

### Issue 21: Application Slow

**Symptom**:
```bash
# Application responds slowly
```

**Possible Causes**:
- Database queries slow
- No caching
- Large payload
- Network issues

**Investigation**:
```bash
# Check database queries
# Check response times
# Check network
```

**Solutions**:

**Solution 1: Optimize Database**
```bash
# Add indexes
# Optimize queries
# Use connection pooling
```

**Solution 2: Add Caching**
```bash
# Use Redis caching
# Cache frequently accessed data
```

**Solution 3: Optimize Payload**
```bash
# Use pagination
# Select only needed fields
# Compress response
```

### Issue 22: High Memory Usage

**Symptom**:
```bash
# Application uses too much memory
```

**Possible Causes**:
- Memory leak
- Large data sets
- No pagination
- Caching issues

**Investigation**:
```bash
# Check memory usage
docker stats
```

**Solutions**:

**Solution 1: Add Pagination**
```bash
# Use pagination for large datasets
```

**Solution 2: Fix Memory Leak**
```bash
# Find memory leak
# Fix it
```

**Solution 3: Clear Cache**
```bash
# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

## Getting Help

### When to Ask for Help

If you encounter an issue not covered here:

1. **Check Logs**: Always check logs first
2. **Search Online**: Search error messages
3. **Check Documentation**: Read relevant documentation
4. **Ask Team**: Ask team members for help
5. **Create Issue**: Create GitHub issue if it's a bug

### Information to Provide

When asking for help, provide:

1. **Error Message**: Full error message
2. **Steps to Reproduce**: What you did
3. **Expected Behavior**: What you expected
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Node.js version, etc.
6. **Logs**: Relevant log output

## Prevention

### Best Practices to Prevent Issues

1. **Keep Dependencies Updated**: Regularly update dependencies
2. **Use Version Control**: Commit frequently
3. **Test Changes**: Test before committing
4. **Read Error Messages**: Don't ignore errors
5. **Check Logs**: Always check logs
6. **Follow Documentation**: Follow setup instructions carefully
7. **Use Correct Versions**: Use specified versions
8. **Monitor Resources**: Monitor CPU, RAM, disk

### Regular Maintenance

1. **Update Dependencies**: Weekly
2. **Clean Docker**: Monthly
3. **Backup Database**: Daily
4. **Check Logs**: Daily
5. **Monitor Performance**: Weekly

## Related Documentation

- [02-Installation.md](./02-Installation.md) - Installation guide
- [04-Development-Setup.md](./04-Development-Setup.md) - Development setup
- [05-Database-Setup.md](./05-Database-Setup.md) - Database setup
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
- [17-Production](../17-Production/README.md) - Production guide
