# Migrations

## Purpose

This document explains the migration strategy used in the University ERP system. It details how to create, apply, and manage database migrations using Prisma.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Prisma migrations for database schema changes. Understanding migrations is critical for:
- Managing schema changes
- Versioning database schema
- Rolling back changes
- Collaborating on schema changes
- Deploying schema changes

Without understanding migrations, developers may struggle with schema management or may introduce breaking changes.

## Where This Is Used

- **Onboarding**: New developers learn migration workflow
- **Feature Development**: Creating migrations for schema changes
- **Code Reviews**: Reviewing migration changes
- **Deployment**: Deploying migrations to production
- **Rollback**: Rolling back schema changes

## Dependencies

### Migration Dependencies

**Confirmed by Code**: Migrations depend on:

- **Prisma 5.x**: ORM for database access
- **PostgreSQL 16**: Relational database
- **Prisma CLI**: Migration CLI tool
- **Docker**: Database container

## Internal Architecture

### Migration Architecture

**Confirmed by Code**: Migrations follow a versioned structure.

```
┌─────────────────────────────────────────────────────────┐
│              Migration History                             │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Pending      │  │  Applied        │  │  Rolled Back   │
│  Migrations  │  │  Migrations     │  │  Migrations    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Creating Migrations

**Confirmed by Code**: Migrations created with Prisma CLI.

**Generate Migration**:
```bash
npx prisma migrate dev --name add_user_profile
```

**What This Does**:
- **migrate dev**: Creates migration in development
- **--name**: Names the migration
- **Generates**: Creates migration file
- **Applies**: Applies migration to database

**Migration File**:
```sql
-- CreateIndex
CREATE INDEX "User.email_idx" ON "User"("email");

-- CreateIndex
CREATE INDEX "User.universityId_idx" ON "User"("universityId");

-- CreateIndex
CREATE INDEX "User.instituteId_idx" ON "User"("instituteId");
```

**What This Does**:
- **CREATE INDEX**: Creates index on column
- **idx**: Index naming convention
- **ON**: Specifies table and column

### Applying Migrations

**Confirmed by Code**: Migrations applied with Prisma CLI.

**Apply Migrations**:
```bash
npx prisma migrate deploy
```

**What This Does**:
- **migrate deploy**: Applies pending migrations
- **Production**: Used in production
- **Safe**: Only applies new migrations
- **Idempotent**: Safe to run multiple times

### Rolling Back Migrations

**Confirmed by Code**: Migrations can be rolled back.

**Rollback Migration**:
```bash
npx prisma migrate resolve --rolled-back "20240101000000_add_user_profile"
```

**What This Does**:
- **migrate resolve**: Resolves migration status
- **--rolled-back**: Marks migration as rolled back
- **Manual**: Requires manual rollback SQL
- **Tracking**: Updates migration tracking

### Migration Status

**Confirmed by Code**: Migration status checked with Prisma CLI.

**Check Status**:
```bash
npx prisma migrate status
```

**Output**:
```
schema.prisma is up to date with the database.
```

**What This Does**:
- **migrate status**: Checks migration status
- **Comparison**: Compares schema to database
- **Status**: Shows migration status
- **Sync**: Indicates if schema is synced

### Resetting Database

**Confirmed by Code**: Database can be reset for development.

**Reset Database**:
```bash
npx prisma migrate reset
```

**What This Does**:
- **migrate reset**: Resets database
- **Drop**: Drops all tables
- **Recreate**: Recreates all tables
- **Seed**: Runs seed script
- **Warning**: Deletes all data

## Database Interactions

### Migration-Database Flow

**Confirmed by Code**: Migrations applied directly to database.

**Flow**:
```
Migration File → Prisma → PostgreSQL
```

## Redis Interactions

### Migration-Redis Flow

**Confirmed by Code**: Migrations don't interact with Redis.

**Flow**:
```
Migration → Database → Redis Cache (invalidated)
```

## Queue Interactions

### Migration-Queue Flow

**Confirmed by Code**: Migrations don't interact with queues.

**Flow**:
```
Migration → Database (no queue interaction)
```

## Worker Interactions

### Migration-Worker Flow

**Confirmed by Code**: Workers don't interact with migrations.

**Flow**:
```
Migration → Database (no worker interaction)
```

## Business Rules

### Migration Rules

**Confirmed by Code**: Migrations follow these rules:

1. **Version Control**: Migrations in version control
2. **Review**: Review migrations before applying
3. **Test**: Test migrations in staging
4. **Backup**: Backup database before migration
5. **Rollback**: Have rollback plan ready

### Migration Naming Rules

**Confirmed by Code**: Migration naming follows these rules:

1. **Descriptive**: Use descriptive names
2. **Snake Case**: Use snake_case
3. **Prefix**: Use verb prefix (add_, remove_, update_)
4. **Timestamp**: Auto-generated timestamp
5. **Unique**: Each migration must be unique

## Security

### Migration Security

**Confirmed by Code**: Security considerations for migrations:

1. **Access Control**: Restrict migration access
2. **Audit Logging**: Log all migrations
3. **Backup**: Backup before migration
4. **Review**: Review migration SQL
5. **Test**: Test in staging

## Performance Considerations

### Migration Performance

**Confirmed by Code**: Performance considerations for migrations:

1. **Large Tables**: Migrate large tables in batches
2. **Indexes**: Create indexes after data migration
3. **Downtime**: Plan for downtime if needed
4. **Testing**: Test migration performance
5. **Monitoring**: Monitor migration performance

## Common Mistakes

### Mistake 1: Not Reviewing Migration SQL

**Symptom**: Unexpected migration changes

**Cause**: Not reviewing migration SQL

**Fix**:
```bash
# Review migration SQL before applying
npx prisma migrate dev --name my_migration
# Review generated SQL
# Apply if correct
```

### Mistake 2: Not Testing in Staging

**Symptom**: Migration fails in production

**Cause**: Not testing in staging

**Fix**:
```bash
# Test in staging first
npx prisma migrate deploy
# Verify changes
# Then apply to production
```

### Mistake 3: Not Having Rollback Plan

**Symptom**: Can't rollback failed migration

**Cause**: Not having rollback plan

**Fix**:
```bash
# Have rollback SQL ready
# Test rollback in staging
# Document rollback procedure
```

## Debugging Guide

### Migration Debugging

**Issue**: Migration failing

**Investigation**:
1. Check migration SQL
2. Check database state
3. Check for conflicts
4. Review error message
5. Fix migration

**Tools**:
- Prisma CLI
- Database logs
- Migration files
- Schema diff

## Future Enhancements

### Automatic Rollback

**Status**: Not implemented

**Proposal**: Implement automatic rollback:
- Auto-generate rollback SQL
- One-command rollback
- Safer migrations
- Better recovery
- Easier deployment

### Migration Testing

**Status**: Not implemented

**Proposal**: Implement migration testing:
- Test migrations in CI/CD
- Validate migration SQL
- Test rollback
- Performance testing
- Data integrity testing

## Production Considerations

### Production Migrations

**Production Deployment**:
- Review migrations in staging
- Backup database before migration
- Apply during maintenance window
- Monitor migration performance
- Have rollback plan ready
- Document migration

### Migration Monitoring

**Monitoring Metrics**:
- Migration success rate
- Migration duration
- Database size changes
- Index creation time
- Data migration time

## Example Requests

### Migration Example

**Request**: Create migration

```bash
npx prisma migrate dev --name add_user_profile
```

## Example Responses

### Migration Response

**Response**: Migration created and applied

```
The following migration(s) have been created and applied from new schema changes:

migrations/
  └─ 20240101000000_add_user_profile/
    └─ migration.sql
```

## Sequence Diagrams

### Migration Flow

```
Schema Change → Generate Migration → Review Migration → Apply Migration → Database Updated
```

## Architecture Diagrams

### Migration Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Prisma Schema                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Migration Generator                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Migration File                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Database                                     │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you manage database schema changes?

**Answer**: Schema changes via:
- Prisma migrations
- Version control for migrations
- Review before applying
- Test in staging
- Apply to production with backup

### Q2: How do you rollback a migration?

**Answer**: Rollback via:
- Manual rollback SQL
- Mark migration as rolled back
- Test rollback in staging
- Document rollback procedure
- Have rollback plan ready

### Q3: How do you handle breaking changes in migrations?

**Answer**: Breaking changes via:
- Plan breaking changes carefully
- Test in staging
- Backup database before migration
- Apply during maintenance window
- Have rollback plan ready

## Exercises

### Exercise 1: Create a Migration

**Task**: Create a new migration.

**Steps**:
1. Update Prisma schema
2. Generate migration
3. Review migration SQL
4. Apply migration
5. Verify changes

**Verification**:
- Migration created
- SQL correct
- Migration applied
- Database updated
- Tests pass

### Exercise 2: Rollback a Migration

**Task**: Rollback a migration.

**Steps**:
1. Create rollback SQL
2. Test rollback in staging
3. Apply rollback
4. Mark migration as rolled back
5. Verify rollback

**Verification**:
- Rollback SQL correct
- Rollback tested
- Rollback applied
- Database reverted
- Tests pass

## Real Production Scenarios

### Scenario 1: Migration Failure

**Situation**: Migration failing in production

**Response**:
1. Check error message
2. Review migration SQL
3. Fix migration
4. Apply fixed migration
5. Monitor database

### Scenario 2: Data Loss After Migration

**Situation**: Data lost after migration

**Response**:
1. Stop migration
2. Restore from backup
3. Review migration SQL
4. Fix migration
5. Reapply migration

## Navigation

**Next Section**: [03-Query-Optimization](./03-Query-Optimization.md)

**Previous Section**: [01-Prisma-Schema](./01-Prisma-Schema.md)

**Related Documentation**:
- [01-Prisma-Schema](./01-Prisma-Schema.md) - Prisma schema
- [03-Backend/04-Services](../03-Backend/04-Services.md) - Services
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
