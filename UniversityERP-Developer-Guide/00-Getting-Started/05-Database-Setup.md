# Database Setup

## Purpose

This document provides detailed instructions for setting up and managing the PostgreSQL database for the University ERP system. This includes initialization, migrations, seeding, and common database operations.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses PostgreSQL with Prisma ORM. Database setup is critical for:
- Storing all application data
- Supporting complex relationships between entities
- Ensuring data consistency
- Supporting transactions

Without proper database setup, the application cannot function.

## Where This Is Used

- **Initial Setup**: First-time database initialization
- **Development**: Managing database during development
- **Testing**: Setting up test databases
- **Production**: Database deployment and maintenance
- **Troubleshooting**: Database-related issues

## Prerequisites

**Required**:
- Docker running with PostgreSQL service
- Environment variables configured (DATABASE_URL)
- Prisma CLI installed

**Verification**:
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check DATABASE_URL
cat .env | grep DATABASE_URL
```

## Database Architecture

### PostgreSQL Version

**Confirmed by Code**: PostgreSQL 16.x (from docker-compose.yml)

```yaml
postgres:
  image: postgres:16-alpine
```

### Database Name

**Confirmed by Code**: `university_erp` (from .env.example)

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
```

### Database Schema

**Confirmed by Code**: Prisma schema defines 100+ models

**Location**: `apps/core-api/prisma/schema.prisma`

**Key Domains**:
- Authentication (User, Role, Permission)
- Master Data (University, Institute, Department)
- Academic (Course, Batch, Section, Student)
- Examination (Question, ExamPaper, ExamAttempt)
- Fee (FeeStructure, FeeLedger, Payment)
- Workflow (WorkflowDefinition, WorkflowInstance)
- Documents (DocumentTemplate, IssuedDocument)
- And many more...

## Database Initialization

### Step 1: Start PostgreSQL

**Confirmed by Code**: PostgreSQL runs in Docker.

**Action**:
```bash
# Start PostgreSQL service
docker-compose up -d postgres

# Verify it's running
docker-compose ps postgres
```

**What This Does**:
- Starts PostgreSQL container
- Creates database if not exists
- Mounts volume for data persistence

### Step 2: Create Database

**Confirmed by Code**: Database is created automatically by PostgreSQL.

**Action**:
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres

# Create database (if not exists)
CREATE DATABASE university_erp;

# Verify database exists
\l

# Disconnect
\q
```

**Note**: Database is usually created automatically by PostgreSQL when first connected.

### Step 3: Run Migrations

**Confirmed by Code**: Prisma manages migrations.

**Action**:
```bash
cd apps/core-api

# Run pending migrations
npx prisma migrate dev

# Verify migrations
npx prisma migrate status
```

**What This Does**:
- Applies all pending migrations
- Creates tables
- Creates indexes
- Creates foreign keys
- Creates constraints

**Migration Files Location**: `apps/core-api/prisma/migrations/`

### Step 4: Generate Prisma Client

**Confirmed by Code**: Prisma Client is generated from schema.

**Action**:
```bash
cd apps/core-api

# Generate Prisma Client
npx prisma generate
```

**What This Does**:
- Generates TypeScript types
- Generates Prisma Client
- Enables type-safe database queries

### Step 5: Seed Database

**Confirmed by Code**: Seed script populates initial data.

**Action**:
```bash
cd apps/core-api

# Run seed script
npx prisma db seed
```

**What This Does**:
- Populates master data
- Creates default users
- Creates default configurations
- Creates sample data for development

**Seed Script Location**: `apps/core-api/prisma/seed.ts`

## Database Migrations

### Creating a Migration

**Confirmed by Code**: Prisma migrate dev creates migrations.

**Action**:
```bash
cd apps/core-api

# Modify schema.prisma
# Add/modify models

# Create migration
npx prisma migrate dev --name migration_name
```

**What This Does**:
- Detects schema changes
- Generates migration SQL
- Applies migration to database
- Updates Prisma Client

**Migration File Structure**:
```
prisma/migrations/
└── 20240101000000_migration_name/
    └── migration.sql
```

### Migration SQL

**Example Migration**:
```sql
-- CreateIndex
CREATE INDEX "User_email_idx" ON "User"("email");

-- AlterTable
ALTER TABLE "User" ADD COLUMN "phone" TEXT;
```

### Applying Migrations

**Development**:
```bash
cd apps/core-api
npx prisma migrate dev
```

**Production**:
```bash
cd apps/core-api
npx prisma migrate deploy
```

**Difference**:
- `migrate dev`: Creates and applies migrations (development)
- `migrate deploy`: Applies existing migrations (production)

### Rolling Back Migrations

**Confirmed by Code**: Prisma supports migration rollback.

**Action**:
```bash
cd apps/core-api

# Rollback last migration
npx prisma migrate resolve --rolled-back <migration_name>

# Or reset database (WARNING: deletes all data)
npx prisma migrate reset
```

**Warning**: Rolling back migrations can cause data loss. Use with caution.

### Migration Status

**Action**:
```bash
cd apps/core-api

# Check migration status
npx prisma migrate status
```

**Output**:
```
Migration Name          Applied?          Migration Time
--------------------------------------------------------
20240101000000_init     Yes               2024-01-01 00:00:00
20240102000000_add_phone Yes              2024-01-02 00:00:00
```

## Database Seeding

### Seed Script

**Confirmed by Code**: Seed script is in `apps/core-api/prisma/seed.ts`.

**Purpose**:
- Populate master data
- Create default users
- Create default configurations
- Create sample data

**Running Seed**:
```bash
cd apps/core-api
npx prisma db seed
```

**Seed Data Includes**:
- Universities
- Institutes
- Departments
- Courses
- Batches
- Sections
- Users (admin, staff, students)
- Configurations

### Custom Seed Data

**Action**:
```bash
cd apps/core-api

# Edit seed.ts
# Add custom seed data

# Run seed
npx prisma db seed
```

### Resetting Database

**Action**:
```bash
cd apps/core-api

# Reset database (WARNING: deletes all data)
npx prisma migrate reset

# Re-seed
npx prisma db seed
```

**Warning**: This deletes all data. Use with caution.

## Database Operations

### Connecting to Database

**Using Docker exec**:
```bash
docker-compose exec postgres psql -U postgres -d university_erp
```

**Using local client**:
```bash
psql -h localhost -U postgres -d university_erp
```

**Using Prisma Studio**:
```bash
cd apps/core-api
npx prisma studio
```

Opens Prisma Studio at http://localhost:5555

### Common SQL Queries

**List Tables**:
```sql
\dt
```

**Describe Table**:
```sql
\d "User"
```

**Select Data**:
```sql
SELECT * FROM "User" LIMIT 10;
```

**Count Records**:
```sql
SELECT COUNT(*) FROM "User";
```

**Join Tables**:
```sql
SELECT u.*, i.name as institute_name
FROM "User" u
JOIN "Institute" i ON u."instituteId" = i.id;
```

**Update Data**:
```sql
UPDATE "User" SET email = 'new@example.com' WHERE id = 'user-id';
```

**Delete Data**:
```sql
DELETE FROM "User" WHERE id = 'user-id';
```

**Exit**:
```sql
\q
```

### Prisma Queries

**Confirmed by Code**: Prisma is used for database operations.

**Select**:
```typescript
// Find one
const user = await prisma.user.findUnique({
  where: { id: userId },
});

// Find many
const users = await prisma.user.findMany({
  where: { role: 'STUDENT' },
});

// With relations
const user = await prisma.user.findUnique({
  where: { id: userId },
  include: { institute: true, department: true },
});
```

**Create**:
```typescript
const user = await prisma.user.create({
  data: {
    email: 'test@example.com',
    passwordHash: hashedPassword,
    role: 'STUDENT',
  },
});
```

**Update**:
```typescript
const user = await prisma.user.update({
  where: { id: userId },
  data: { email: 'new@example.com' },
});
```

**Delete**:
```typescript
const user = await prisma.user.delete({
  where: { id: userId },
});
```

**Transaction**:
```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  const profile = await tx.userProfile.create({ data: profileData });
  return { user, profile };
});
```

## Database Backup and Restore

### Backup

**Using pg_dump**:
```bash
# Backup to file
docker-compose exec postgres pg_dump -U postgres university_erp > backup.sql

# Backup with custom format
docker-compose exec postgres pg_dump -U postgres -Fc university_erp > backup.dump
```

**Using Docker volume**:
```bash
# Backup Docker volume
docker run --rm \
  -v docker-volumes_postgres:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz /data
```

### Restore

**Using psql**:
```bash
# Restore from file
docker-compose exec -T postgres psql -U postgres university_erp < backup.sql

# Restore from custom format
docker-compose exec postgres pg_restore -U postgres -d university_erp backup.dump
```

**Using Docker volume**:
```bash
# Restore Docker volume
docker run --rm \
  -v docker-volumes_postgres:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup-20240101.tar.gz -C /
```

## Database Performance

### Indexes

**Confirmed by Code**: Prisma schema defines indexes.

**View Indexes**:
```sql
-- List indexes on table
\d "User"

-- Or
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'User';
```

**Create Index**:
```sql
CREATE INDEX "User_email_idx" ON "User"("email");
```

**Drop Index**:
```sql
DROP INDEX "User_email_idx";
```

### Query Performance

**Slow Query Log**:
```sql
-- Enable slow query log
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();
```

**Explain Query**:
```sql
EXPLAIN ANALYZE SELECT * FROM "User" WHERE email = 'test@example.com';
```

**Optimization Tips**:
- Use indexes on frequently queried columns
- Avoid SELECT * (select only needed columns)
- Use JOIN instead of subqueries when possible
- Use LIMIT for pagination
- Use connection pooling

### Connection Pooling

**Confirmed by Code**: Prisma uses connection pooling.

**Configuration**:
```typescript
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pooling is automatic
}
```

**Connection String with Pooling**:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp?connection_limit=10
```

## Database Security

### User Management

**Create User**:
```sql
CREATE USER app_user WITH PASSWORD 'strong_password';
```

**Grant Permissions**:
```sql
GRANT ALL PRIVILEGES ON DATABASE university_erp TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
```

**Revoke Permissions**:
```sql
REVOKE ALL PRIVILEGES ON DATABASE university_erp FROM app_user;
```

### Encryption

**Password Hashing**:
```typescript
import bcrypt from 'bcrypt';

const hash = await bcrypt.hash(password, 10);
```

**Data Encryption**:
- Use pgcrypto extension for column-level encryption
- Encrypt sensitive data before storage
- Use TLS for database connections

### Backup Security

- Encrypt backup files
- Store backups securely
- Limit backup access
- Regular backup rotation

## Database Monitoring

### Connection Monitoring

**Active Connections**:
```sql
SELECT count(*) FROM pg_stat_activity;
```

**Kill Connection**:
```sql
SELECT pg_terminate_backend(pid);
```

### Size Monitoring

**Database Size**:
```sql
SELECT pg_size_pretty(pg_database_size('university_erp'));
```

**Table Size**:
```sql
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Performance Monitoring

**Query Statistics**:
```sql
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

## Common Issues

### Issue 1: Database Connection Failed

**Symptom**: Application fails to connect to database

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

**Fix**:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Verify DATABASE_URL
# Should be: postgresql://postgres:postgres@localhost:5432/university_erp
```

### Issue 2: Migration Failed

**Symptom**: `npx prisma migrate dev` fails

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

**Fix**:
```bash
# Resolve conflict manually
# Or reset database (WARNING: deletes all data)
npx prisma migrate reset
```

### Issue 3: Seed Failed

**Symptom**: `npx prisma db seed` fails

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

**Fix**:
```bash
# Ensure migrations are applied
npx prisma migrate dev

# Fix seed script
# Re-run seed
npx prisma db seed
```

### Issue 4: Slow Queries

**Symptom**: Database queries are slow

**Possible Causes**:
- Missing indexes
- Large tables
- Complex queries
- Connection issues

**Investigation**:
```sql
-- Explain query
EXPLAIN ANALYZE SELECT * FROM "User" WHERE email = 'test@example.com';

-- Check indexes
\d "User"
```

**Fix**:
```sql
-- Add index
CREATE INDEX "User_email_idx" ON "User"("email");

-- Optimize query
-- Select only needed columns
-- Use LIMIT
-- Use JOIN instead of subqueries
```

## Future Enhancements

### Automated Backups

**Status**: Not implemented

**Proposal**: Automated daily backups with retention policy:

```bash
# Cron job
0 2 * * * /path/to/backup-script.sh
```

### Database Replication

**Status**: Not implemented

**Proposal**: Set up read replicas for scaling:

- Primary for writes
- Replicas for reads
- Load balancing

### Connection Pooling

**Status**: Prisma uses connection pooling

**Enhancement**: Use PgBouncer for better connection pooling:

```bash
# Install PgBouncer
docker-compose up -d pgbouncer
```

## Production Considerations

### Production Database

**Recommendations**:
- Use managed PostgreSQL (AWS RDS, Azure Database)
- Enable automated backups
- Enable point-in-time recovery
- Enable read replicas
- Use connection pooling
- Monitor performance
- Set up alerts

### Production Migrations

**Best Practices**:
- Test migrations in staging first
- Use `migrate deploy` instead of `migrate dev`
- Have rollback plan
- Run migrations during low traffic
- Monitor migration execution
- Verify migration success

### Production Backups

**Best Practices**:
- Automated daily backups
- Weekly full backups
- Point-in-time recovery
- Backup encryption
- Off-site backup storage
- Regular backup restoration testing

## Related Documentation

- [05-Database](../05-Database/README.md) - Detailed database documentation
- [02-Installation.md](./02-Installation.md) - Installation guide
- [08-Common-Issues.md](./08-Common-Issues.md) - Common issues
- [17-Production](../17-Production/README.md) - Production guide
