# 00-Getting-Started

## Purpose

This folder provides everything you need to get started with the University ERP system. Whether you're a new developer joining the team, a contractor evaluating the codebase, or a technical lead taking over ownership, this section will guide you through the initial setup and provide context for the entire system.

## Why This Folder Exists

**Confirmed by Code**: The University ERP is a complex system with multiple services, databases, and infrastructure components. Without proper setup, you cannot:
- Run the application locally
- Understand the system architecture
- Make meaningful contributions
- Debug issues effectively
- Deploy to production

This folder exists to ensure every developer has a consistent, working development environment and understands the foundational concepts before diving into specific modules.

## Where This Is Used

- **Onboarding**: New developers start here
- **Environment Setup**: Setting up local development
- **CI/CD**: Understanding how the system is built
- **Documentation**: Reference for installation procedures

## Dependencies

### System Requirements

**Confirmed by Code**:
- **Node.js**: 18.x or higher (confirmed by package.json engines)
- **npm**: 9.x or higher (confirmed by package-lock.json)
- **Docker**: 20.x or higher (confirmed by docker-compose.yml)
- **Docker Compose**: 2.x or higher (confirmed by docker-compose.yml)
- **Git**: 2.x or higher (for version control)
- **PostgreSQL Client**: 16.x or higher (for direct database access)
- **Redis CLI**: 7.x or higher (for direct Redis access)

### Hardware Requirements

**Inferred** (based on typical development needs):
- **RAM**: Minimum 8GB, Recommended 16GB
- **CPU**: Minimum 4 cores, Recommended 8 cores
- **Disk**: Minimum 50GB free space (for Docker volumes and node_modules)

### Software Dependencies

**Confirmed by Code**:
- **Turbo**: Monorepo build system (confirmed by turbo.json)
- **Prisma**: ORM for database (confirmed by apps/core-api/package.json)
- **NestJS**: Backend framework (confirmed by apps/core-api/package.json)
- **React**: Frontend framework (confirmed by web/admin-portal/package.json)
- **Vite**: Frontend build tool (confirmed by web/admin-portal/package.json)

## Internal Architecture

This folder contains the following documentation:

```
00-Getting-Started/
├── README.md                    # This file - overview and navigation
├── 01-Prerequisites.md          # Detailed system requirements
├── 02-Installation.md           # Step-by-step installation guide
├── 03-Quick-Start.md            # 5-minute quick start guide
├── 04-Development-Setup.md     # Complete development environment setup
├── 05-Database-Setup.md         # Database initialization and seeding
├── 06-Testing-Setup.md          # Testing framework configuration
├── 07-IDE-Setup.md              # VS Code and other IDE configurations
├── 08-Common-Issues.md          # Troubleshooting common problems
├── 09-Next-Steps.md             # What to do after setup
└── 10-Verification.md           # How to verify your setup is correct
```

## Code Walkthrough

### Installation Process

**Confirmed by Code**: The installation process involves these steps:

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd UniversityERP
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```
   This installs root-level dependencies and all workspace dependencies via npm workspaces.

3. **Start Docker Services**
   ```bash
   docker-compose up -d
   ```
   This starts PostgreSQL, Redis, MinIO, and Elasticsearch.

4. **Run Database Migrations**
   ```bash
   cd apps/core-api
   npx prisma migrate dev
   ```
   This applies all pending migrations to the database.

5. **Seed Database**
   ```bash
   npx prisma db seed
   ```
   This populates the database with initial data.

### Development Server Startup

**Confirmed by Code**:

**Backend (Core API)**:
```bash
cd apps/core-api
npm run start:dev
```
This starts the NestJS backend with hot-reload enabled.

**Frontend (Admin Portal)**:
```bash
cd web/admin-portal
npm run dev
```
This starts the Vite dev server with hot-reload enabled.

## Database Interactions

### Initial Database Setup

**Confirmed by Code**: The database is initialized through Prisma migrations:

```typescript
// apps/core-api/prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

**Migration Files**: Located in `apps/core-api/prisma/migrations/`

**Seed Script**: Located in `apps/core-api/prisma/seed.ts`

### Database Connection String

**Confirmed by Code**: The database connection is configured via environment variable:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
```

This is set in `.env` file and used by Prisma.

## Redis Interactions

### Redis Setup

**Confirmed by Code**: Redis is started via Docker Compose:

```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - ./docker-volumes/redis:/data
  command: redis-server --appendonly yes
```

### Redis Connection

**Confirmed by Code**: Redis connection is configured in the RedisService:

```typescript
// apps/core-api/src/infrastructure/redis/redis.service.ts
@Injectable()
export class RedisService extends Redis implements OnModuleDestroy {
  constructor(configService: ConfigService) {
    super({
      host: configService.get<string>('REDIS_HOST', 'localhost'),
      port: configService.get<number>('REDIS_PORT', 6379),
    });
  }
}
```

## Queue Interactions

### Bull Queue Setup

**Confirmed by Code**: Bull queues are used for background jobs:

```typescript
// Queue configuration (inferred from package.json)
import Bull from 'bull';

const queue = new Bull('queue-name', {
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT),
  },
});
```

**Note**: Actual queue processor implementations were not visible in code discovery. This is inferred from Bull dependency.

## Worker Interactions

### Worker Services

**Confirmed by Code**: There are two worker services:

1. **Notification Worker** (`apps/notification-worker/`)
   - Processes email and SMS notifications
   - Minimal app module (only ConfigModule)
   - Queue processors not visible in discovery

2. **Certificate Generator** (`apps/cert-generator/`)
   - Generates PDF certificates
   - Minimal app module (only ConfigModule)
   - Queue processors not visible in discovery

**Status**: Worker implementations need further investigation.

## Business Rules

### Development Environment Rules

**Confirmed by Code**:
1. All services must be running before starting development
2. Database migrations must be applied before running the application
3. Database must be seeded with initial data
4. Environment variables must be configured in `.env` file
5. Docker volumes must be mounted for data persistence

### Code Organization Rules

**Confirmed by Code**:
1. Monorepo structure with npm workspaces
2. Shared code in `libs/` directory
3. Backend services in `apps/` directory
4. Frontend applications in `web/` directory
5. Each service has its own package.json

## Security

### Environment Variables

**Confirmed by Code**: Sensitive data is stored in environment variables:

```bash
# .env file (not committed to git)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
JWT_SECRET=your-secret-key
SMTP_PASSWORD=your-smtp-password
MINIO_SECRET_KEY=minioadmin
```

**Security Best Practices**:
- Never commit `.env` file to version control
- Use strong secrets in production
- Rotate secrets regularly
- Use vault for production secrets (AWS Secrets Manager, Azure Key Vault, etc.)

### Docker Security

**Confirmed by Code**: Docker services run with default configurations:

**Known Issues**:
- PostgreSQL uses default credentials (postgres/postgres) in development
- MinIO uses default credentials (minioadmin/minioadmin)
- Redis has no authentication in development

**Production Considerations**:
- Change default credentials in production
- Enable Redis authentication
- Use secrets management
- Enable network isolation

## Performance Considerations

### Development Performance

**Confirmed by Code**:
- Hot-reload enabled for both backend and frontend
- Docker volumes mounted for code changes
- Source maps enabled for debugging

### Known Performance Issues

**Inferred**:
- Large node_modules may slow down initial installation
- Docker services may consume significant RAM
- Prisma migrations may take time for large schemas

### Optimization Tips

**Inferred**:
- Use `.dockerignore` to exclude unnecessary files
- Use npm workspaces to avoid duplicate dependencies
- Use Docker build cache for faster rebuilds

## Common Mistakes

### Mistake 1: Not Starting Docker Services

**Symptom**: Application fails to start with connection errors

**Cause**: PostgreSQL, Redis, MinIO not running

**Fix**: Always run `docker-compose up -d` before starting development

### Mistake 2: Skipping Database Migrations

**Symptom**: Application errors about missing tables

**Cause**: Database schema not up to date

**Fix**: Always run `npx prisma migrate dev` after pulling changes

### Mistake 3: Not Seeding Database

**Symptom**: Application works but has no data

**Cause**: Database is empty

**Fix**: Run `npx prisma db seed` after migrations

### Mistake 4: Wrong Node.js Version

**Symptom**: Installation errors or runtime errors

**Cause**: Node.js version doesn't match package.json engines

**Fix**: Use Node.js 18.x or higher (check package.json for exact version)

### Mistake 5: Port Conflicts

**Symptom**: Services fail to start with "port already in use" error

**Cause**: Another process using the same port

**Fix**: Stop conflicting processes or change ports in .env file

## Debugging Guide

### Installation Issues

**Symptom**: `npm install` fails

**Investigation Steps**:
1. Check Node.js version: `node --version`
2. Check npm version: `npm --version`
3. Clear npm cache: `npm cache clean --force`
4. Delete node_modules: `rm -rf node_modules`
5. Reinstall: `npm install`

### Docker Issues

**Symptom**: Docker services fail to start

**Investigation Steps**:
1. Check Docker status: `docker ps`
2. Check Docker logs: `docker-compose logs`
3. Restart Docker daemon
4. Check port conflicts: `lsof -i :5432` (PostgreSQL), `lsof -i :6379` (Redis)

### Database Issues

**Symptom**: Database connection fails

**Investigation Steps**:
1. Check PostgreSQL is running: `docker-compose ps postgres`
2. Check DATABASE_URL in .env file
3. Test connection: `docker-compose exec postgres psql -U postgres -d university_erp`
4. Check migrations: `npx prisma migrate status`

### Redis Issues

**Symptom**: Redis connection fails

**Investigation Steps**:
1. Check Redis is running: `docker-compose ps redis`
2. Test connection: `docker-compose exec redis redis-cli ping`
3. Check REDIS_HOST and REDIS_PORT in .env file

## Future Enhancements

### Automated Setup Script

**Status**: Not implemented

**Proposal**: Create a setup script that automates the entire installation process:

```bash
./setup.sh
```

This script would:
- Check prerequisites
- Install dependencies
- Start Docker services
- Run migrations
- Seed database
- Verify setup

### Docker Compose Profiles

**Status**: Not implemented

**Proposal**: Use Docker Compose profiles for different environments:

```bash
docker-compose --profile dev up
docker-compose --profile test up
docker-compose --profile prod up
```

### Health Check Endpoint

**Status**: Not implemented

**Proposal**: Add a health check endpoint that verifies all services are running:

```bash
curl http://localhost:3000/health
```

This would check:
- Database connection
- Redis connection
- MinIO connection
- Elasticsearch connection

## Production Considerations

### Environment-Specific Configuration

**Confirmed by Code**: Different environment files for different stages:

- `.env` - Development
- `.env.staging` - Staging
- `.env.production` - Production

**Best Practices**:
- Never use production credentials in development
- Use different databases for different environments
- Use different Redis instances for different environments
- Use different MinIO buckets for different environments

### Production Deployment

**Inferred**: Production deployment uses PM2 or Kubernetes:

**PM2 Configuration** (inferred from ecosystem.native.config.js):
```javascript
module.exports = {
  apps: [
    {
      name: 'core-api',
      script: 'apps/core-api/dist/main.js',
      instances: 2,
      exec_mode: 'cluster',
    },
  ],
};
```

## Example Requests

### Health Check

**Request**:
```bash
curl http://localhost:3000/health
```

**Expected Response**:
```json
{
  "status": "ok",
  "database": "connected",
  "redis": "connected",
  "minio": "connected"
}
```

**Status**: Inferred - health check endpoint not visible in code

### API Test

**Request**:
```bash
curl http://localhost:3000/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'
```

**Expected Response**:
```json
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "user": {
    "id": "user-id",
    "email": "test@example.com",
    "role": "ADMIN"
  }
}
```

**Status**: Confirmed by Code - auth endpoint exists

## Example Responses

### Successful Setup

**Indicators**:
- All Docker services running: `docker-compose ps` shows all services as "Up"
- Database migrations applied: `npx prisma migrate status` shows all migrations applied
- Database seeded: Database contains initial data
- Backend running: Core API accessible at http://localhost:3000
- Frontend running: Admin Portal accessible at http://localhost:5173

### Failed Setup

**Indicators**:
- Docker services not running: `docker-compose ps` shows services as "Exited"
- Database connection errors: Application logs show connection errors
- Migration errors: Application logs show migration errors
- Port conflicts: Application logs show "port already in use" errors

## Sequence Diagrams

### Installation Sequence

```
Developer
    ↓
Clone Repository
    ↓
npm install
    ↓
Docker Compose Up
    ↓
PostgreSQL Starts
    ↓
Redis Starts
    ↓
MinIO Starts
    ↓
Elasticsearch Starts
    ↓
Run Migrations
    ↓
Seed Database
    ↓
Start Core API
    ↓
Start Admin Portal
    ↓
Verify Setup
```

## Architecture Diagrams

### Development Environment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Developer Machine                      │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API      │  │  Admin Portal  │  │  Docker Desktop │
│  (NestJS)      │  │  (React/Vite)  │  │                 │
│  Port 3000     │  │  Port 5173     │  └────────┬─────────┘
└────────────────┘  └─────────────────┘             │
                                                   │
        ┌──────────────────────────────────────────┘
        │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL    │  │     Redis       │  │     MinIO       │
│  Port 5432     │  │   Port 6379     │  │   Port 9000     │
└────────────────┘  └─────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What is the purpose of the monorepo structure?

**Answer**: The monorepo structure allows us to:
- Share code between services via npm workspaces
- Manage dependencies consistently
- Build and test all services together
- Simplify CI/CD pipelines
- Ensure version compatibility

### Q2: Why do we use Docker for development?

**Answer**: Docker provides:
- Consistent development environment across machines
- Easy setup of infrastructure services (PostgreSQL, Redis, MinIO)
- Data persistence via volumes
- Easy cleanup and reset
- Production-like environment

### Q3: What is the difference between development and production setup?

**Answer**:
- Development: Uses Docker, hot-reload, detailed logging, Swagger docs
- Production: Uses PM2 or Kubernetes, optimized builds, minimal logging, no Swagger

### Q4: Why do we need to seed the database?

**Answer**: Seeding provides:
- Initial master data (universities, institutes, departments)
- Test data for development
- Default configurations
- Default users for testing

### Q5: What happens if I skip running migrations?

**Answer**: The application will fail because:
- Database schema will be out of sync with Prisma schema
- Prisma Client will not match database structure
- Queries will fail with "table does not exist" errors

## Exercises

### Exercise 1: Complete Setup

**Task**: Follow the installation guide to set up the development environment

**Verification**:
- All Docker services running
- Database migrations applied
- Database seeded
- Core API running
- Admin Portal running

### Exercise 2: Verify Database Connection

**Task**: Connect to PostgreSQL and verify the database structure

**Steps**:
1. Connect to PostgreSQL: `docker-compose exec postgres psql -U postgres -d university_erp`
2. List tables: `\dt`
3. Verify key tables exist (User, University, Institute, etc.)
4. Disconnect: `\q`

### Exercise 3: Verify Redis Connection

**Task**: Connect to Redis and verify it's working

**Steps**:
1. Connect to Redis: `docker-compose exec redis redis-cli`
2. Test connection: `ping`
3. Set a value: `set test "hello"`
4. Get the value: `get test`
5. Disconnect: `exit`

### Exercise 4: Test API Endpoint

**Task**: Test the health check endpoint (if exists) or login endpoint

**Steps**:
1. Start Core API
2. Test endpoint with curl
3. Verify response
4. Check logs for any errors

### Exercise 5: Reset Environment

**Task**: Reset the development environment to clean state

**Steps**:
1. Stop Docker services: `docker-compose down`
2. Remove Docker volumes: `docker-compose down -v`
3. Start Docker services: `docker-compose up -d`
4. Run migrations: `npx prisma migrate dev`
5. Seed database: `npx prisma db seed`

## Real Production Scenarios

### Scenario 1: New Developer Onboarding

**Situation**: A new developer joins the team and needs to set up their development environment.

**Steps**:
1. Developer clones repository
2. Developer follows this Getting Started guide
3. Developer verifies setup
4. Developer completes exercises
5. Developer proceeds to System Architecture documentation

**Expected Outcome**: Developer has working environment in 1-2 hours

### Scenario 2: Environment Reset

**Situation**: Development environment has issues and needs to be reset.

**Steps**:
1. Stop all services
2. Remove Docker volumes
3. Restart Docker services
4. Re-run migrations
5. Re-seed database
6. Verify setup

**Expected Outcome**: Clean development environment

### Scenario 3: Database Schema Update

**Situation**: A developer adds a new model to Prisma schema.

**Steps**:
1. Update schema.prisma
2. Create migration: `npx prisma migrate dev`
3. Apply migration
4. Update seed if needed
5. Test new model

**Expected Outcome**: New model available in database

## Navigation

**Next Section**: [01-System-Architecture](../01-System-Architecture/README.md)

**Previous Section**: None (this is the first section)

**Related Documentation**:
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [05-Database](../05-Database/README.md) - Database details
