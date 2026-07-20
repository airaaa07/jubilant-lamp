# 05-Database

## Purpose

This folder provides comprehensive documentation about the database architecture of the University ERP system. It explains the PostgreSQL database, Prisma ORM, schema design, and database operations.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses PostgreSQL 16 with Prisma ORM. Understanding the database is critical for:
- Designing database schemas
- Writing efficient queries
- Understanding data relationships
- Implementing database migrations
- Debugging database issues

Without understanding the database, developers may struggle with data modeling or may introduce performance issues.

## Where This Is Used

- **Onboarding**: New developers learn database architecture
- **Feature Development**: Designing database schemas
- **Code Reviews**: Reviewing database code
- **Migrations**: Implementing database migrations
- **Debugging**: Debugging database issues

## Dependencies

### Database Dependencies

**Confirmed by Code**: The database depends on:

- **PostgreSQL 16**: Relational database
- **Prisma 5.x**: ORM for database access
- **Docker**: Container for database
- **Docker Compose**: Database orchestration

## Internal Architecture

### Database Architecture

**Confirmed by Code**: Database follows relational model.

```
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Schema       │  │  Tables         │  │  Relationships  │
│  (Structure)  │  │  (Entities)     │  │  (Foreign Keys) │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Indexes      │  │  Constraints    │  │  Migrations    │
│  (Performance)│  │  (Rules)        │  │  (Versioning)   │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Prisma Schema

**Confirmed by Code**: Schema defined in prisma/schema.prisma.

**Schema Definition**:
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  passwordHash  String?
  name          String?
  role          UserRole
  universityId  String
  instituteId   String?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  university    University @relation(fields: [universityId], references: [id])
  institute     Institute? @relation(fields: [instituteId], references: [id])
  
  @@index([email])
  @@index([universityId])
  @@index([instituteId])
}

enum UserRole {
  SUPERADMIN
  UNIVERSITY_ADMIN
  INSTITUTE_ADMIN
  DEPARTMENT_ADMIN
  STAFF
  STUDENT
}
```

**What This Does**:
- **generator**: Generates Prisma Client
- **datasource**: Configures database connection
- **model**: Defines database table
- **@id**: Primary key
- **@default(cuid())**: Default value
- **@unique**: Unique constraint
- **@relation**: Defines relationship
- **@@index**: Creates index
- **enum**: Defines enum type

### Database Operations

**Confirmed by Code**: Database operations via Prisma Client.

**PrismaService**:
```typescript
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

**What This Does**:
- **extends PrismaClient**: Extends Prisma Client
- **onModuleInit**: Connects on module init
- **onModuleDestroy**: Disconnects on module destroy

**Find Operations**:
```typescript
// Find one
const user = await prisma.user.findUnique({
  where: { id: userId },
});

// Find many
const users = await prisma.user.findMany({
  where: { universityId: universityId },
});

// Find with relations
const user = await prisma.user.findUnique({
  where: { id: userId },
  include: { university: true, institute: true },
});
```

**Create Operations**:
```typescript
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    passwordHash: hashedPassword,
    name: 'John Doe',
    role: 'STUDENT',
    universityId: universityId,
  },
});
```

**Update Operations**:
```typescript
const user = await prisma.user.update({
  where: { id: userId },
  data: {
    name: 'Jane Doe',
  },
});
```

**Delete Operations**:
```typescript
const user = await prisma.user.delete({
  where: { id: userId },
});
```

**Transaction Operations**:
```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

## Database Interactions

### Backend-Database Flow

**Confirmed by Code**: Backend interacts with database via Prisma.

**Flow**:
```
Backend Service → Prisma → PostgreSQL
```

## Redis Interactions

### Database-Redis Flow

**Confirmed by Code**: Database cached in Redis.

**Flow**:
```
Backend → Database → Redis Cache
```

## Queue Interactions

### Database-Queue Flow

**Confirmed by Code**: Queue operations interact with database.

**Flow**:
```
Worker → Database → Queue
```

## Worker Interactions

### Worker-Database Flow

**Confirmed by Code**: Workers interact with database via Prisma.

**Flow**:
```
Worker → Prisma → PostgreSQL
```

## Business Rules

### Database Rules

**Confirmed by Code**: Database follows these rules:

1. **Normalization**: Database normalized to 3NF
2. **Indexes**: Indexes for frequently queried columns
3. **Constraints**: Constraints for data integrity
4. **Relationships**: Foreign keys for relationships
5. **Migrations**: Versioned migrations

### Schema Design Rules

**Confirmed by Code**: Schema design follows these rules:

1. **CUID**: Use CUID for primary keys
2. **Timestamps**: Include createdAt and updatedAt
3. **Soft Deletes**: Use deletedAt for soft deletes (if needed)
4. **Enums**: Use enums for fixed values
5. **Indexes**: Index foreign keys and frequently queried columns

## Security

### Database Security

**Confirmed by Code**: Security considerations for database:

1. **Connection Security**: Use SSL in production
2. **Password Hashing**: Hash passwords with bcrypt
3. **Data Encryption**: Encrypt sensitive data
4. **Access Control**: Restrict database access
5. **Audit Logging**: Log all database writes

## Performance Considerations

### Database Performance

**Confirmed by Code**: Performance considerations:

1. **Indexes**: Add indexes for frequently queried columns
2. **Query Optimization**: Optimize queries with EXPLAIN ANALYZE
3. **Connection Pooling**: Use connection pooling
4. **Caching**: Cache frequently accessed data in Redis
5. **Pagination**: Paginate large datasets

## Common Mistakes

### Mistake 1: Not Using Indexes

**Symptom**: Slow queries

**Cause**: Not using indexes

**Fix**:
```prisma
// Add index
@@index([email])
@@index([universityId])
```

### Mistake 2: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Not using transactions for related operations

**Fix**:
```typescript
// Use transaction
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

### Mistake 3: N+1 Query Problem

**Symptom**: Too many database queries

**Cause**: Not using include for relations

**Fix**:
```typescript
// Use include
const users = await prisma.user.findMany({
  include: { university: true, institute: true },
});
```

## Debugging Guide

### Database Debugging

**Issue**: Database query slow

**Investigation**:
1. Check query with EXPLAIN ANALYZE
2. Check indexes
3. Check query plan
4. Optimize query
5. Add indexes if needed

**Tools**:
- Prisma Studio
- pgAdmin
- EXPLAIN ANALYZE
- Database logs

## Future Enhancements

### Read Replicas

**Status**: Not implemented

**Proposal**: Add read replicas:
- Better read performance
- Scalability
- Load balancing
- Better availability
- Reduced load on primary

### Partitioning

**Status**: Not implemented

**Proposal**: Add table partitioning:
- Better performance for large tables
- Easier maintenance
- Better query performance
- Parallel queries
- Better data management

## Production Considerations

### Production Database

**Production Deployment**:
- Use managed PostgreSQL (AWS RDS, Azure Database)
- Enable SSL
- Configure backups
- Configure monitoring
- Configure alerts

### Database Monitoring

**Monitoring Metrics**:
- Query performance
- Connection pool usage
- Database size
- Index usage
- Slow queries

## Example Requests

### Database Query Example

**Request**: Query database

```typescript
const users = await prisma.user.findMany({
  where: { universityId: universityId },
});
```

## Example Responses

### Database Response

**Response**: Query results

```typescript
[
  {
    id: 'user-id',
    email: 'user@example.com',
    name: 'John Doe'
  }
]
```

## Sequence Diagrams

### Query Flow

```
Service → Prisma → PostgreSQL → Data → Service
```

## Architecture Diagrams

### Database Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Backend Service                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Prisma ORM                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                          │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: Why did you choose PostgreSQL?

**Answer**: PostgreSQL chosen because:
- ACID compliance
- Advanced features (JSON, arrays, etc.)
- Strong community support
- Excellent performance
- Open source
- Mature and stable

### Q2: How does Prisma work?

**Answer**: Prisma:
- Type-safe database access
- Auto-generated types
- Migration system
- Query builder
- Database client
- Schema-first approach

### Q3: How do you optimize database queries?

**Answer**: Optimize via:
- Add indexes for frequently queried columns
- Use EXPLAIN ANALYZE to analyze queries
- Optimize query plans
- Use connection pooling
- Cache frequently accessed data

## Exercises

### Exercise 1: Create a Migration

**Task**: Create a database migration.

**Steps**:
1. Update Prisma schema
2. Generate migration
3. Review migration SQL
4. Apply migration
5. Test migration

**Verification**:
- Migration created
- SQL correct
- Migration applied
- Database updated
- Tests pass

### Exercise 2: Optimize a Query

**Task**: Optimize a slow query.

**Steps**:
1. Identify slow query
2. Run EXPLAIN ANALYZE
3. Add indexes
4. Optimize query
5. Test performance

**Verification**:
- Query optimized
- Indexes added
- Performance improved
- Tests pass

## Real Production Scenarios

### Scenario 1: Slow Query

**Situation**: Database query slow

**Response**:
1. Identify slow query
2. Run EXPLAIN ANALYZE
3. Add indexes
4. Optimize query
5. Monitor performance

### Scenario 2: Migration Failure

**Situation**: Migration failing

**Response**:
1. Check migration SQL
2. Check database state
3. Fix migration
4. Revert if needed
5. Apply migration

## Navigation

**Next Section**: [01-Prisma-Schema](./01-Prisma-Schema.md)

**Previous Section**: [04-Frontend](../04-Frontend/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
