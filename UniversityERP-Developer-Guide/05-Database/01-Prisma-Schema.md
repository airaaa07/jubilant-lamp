# Prisma Schema

## Purpose

This document explains the Prisma schema used in the University ERP system. It details the schema structure, models, relationships, and schema design patterns.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Prisma 5.x for database access. Understanding the Prisma schema is critical for:
- Designing database models
- Understanding data relationships
- Implementing migrations
- Type-safe database access
- Debugging schema issues

Without understanding the Prisma schema, developers may struggle with data modeling or may introduce schema errors.

## Where This Is Used

- **Onboarding**: New developers learn Prisma schema
- **Feature Development**: Designing new models
- **Code Reviews**: Reviewing schema changes
- **Migrations**: Implementing schema migrations
- **Database Design**: Designing database structure

## Dependencies

### Prisma Schema Dependencies

**Confirmed by Code**: Prisma schema depends on:

- **Prisma 5.x**: ORM for database access
- **PostgreSQL 16**: Relational database
- **TypeScript**: Type-safe schema

## Internal Architecture

### Schema Architecture

**Confirmed by Code**: Schema organized by domain.

```
┌─────────────────────────────────────────────────────────┐
│              Prisma Schema                                │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core Models  │  │  Academic Models│  │  Admin Models  │
│  (User, Auth) │  │  (Course, Batch)│  │  (Fee, Exam)   │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Enums        │  │  Relations     │  │  Indexes       │
│  (Fixed Values)│  │  (Foreign Keys) │  │  (Performance) │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Schema Structure

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
```

**What This Does**:
- **generator**: Generates Prisma Client
- **provider**: Uses prisma-client-js
- **datasource**: Configures database
- **provider**: Uses PostgreSQL
- **url**: Gets DATABASE_URL from environment

### Core Models

**Confirmed by Code**: Core models for authentication and users.

**User Model**:
```prisma
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
```

**What This Does**:
- **@id**: Primary key
- **@default(cuid())**: Default CUID value
- **@unique**: Unique constraint on email
- **@relation**: Defines relationship with University
- **@@index**: Creates indexes for performance
- **@updatedAt**: Auto-updates timestamp

**UserRole Enum**:
```prisma
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
- **enum**: Defines fixed set of values
- **Type Safety**: Type-safe role values
- **Validation**: Validates role values

### Academic Models

**Confirmed by Code**: Academic models for courses and students.

**Course Model**:
```prisma
model Course {
  id            String    @id @default(cuid())
  code          String
  name          String
  credits       Int
  universityId  String
  departmentId  String
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  university    University @relation(fields: [universityId], references: [id])
  department    Department @relation(fields: [departmentId], references: [id])
  batches       Batch[]
  
  @@unique([universityId, code])
  @@index([universityId])
  @@index([departmentId])
}
```

**What This Does**:
- **@unique**: Unique constraint on universityId + code
- **credits**: Course credits
- **batches**: One-to-many relationship with Batch

**Student Model**:
```prisma
model Student {
  id            String    @id @default(cuid())
  userId        String    @unique
  rollNumber    String
  batchId       String
  sectionId     String
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
  
  user          User      @relation(fields: [userId], references: [id])
  batch         Batch     @relation(fields: [batchId], references: [id])
  section       Section   @relation(fields: [sectionId], references: [id])
  attendances   StudentAttendance[]
  marks         StudentMarks[]
  
  @@unique([batchId, rollNumber])
  @@index([userId])
  @@index([batchId])
  @@index([sectionId])
}
```

**What This Does**:
- **@unique**: Unique constraint on batchId + rollNumber
- **rollNumber**: Student roll number
- **attendances**: One-to-many relationship with StudentAttendance
- **marks**: One-to-many relationship with StudentMarks

### Relationships

**Confirmed by Code**: Models have various relationships.

**One-to-One**:
```prisma
model User {
  id        String      @id @default(cuid())
  profile   UserProfile?
}

model UserProfile {
  id     String @id @default(cuid())
  userId String @unique
  user   User   @relation(fields: [userId], references: [id])
}
```

**One-to-Many**:
```prisma
model University {
  id      String      @id @default(cuid())
  users   User[]
  courses Course[]
}

model User {
  id           String      @id @default(cuid())
  universityId String
  university   University  @relation(fields: [universityId], references: [id])
}
```

**Many-to-Many**:
```prisma
model Student {
  id           String             @id @default(cuid())
  enrollments  StudentSubjectEnrollment[]
}

model Subject {
  id          String             @id @default(cuid())
  enrollments StudentSubjectEnrollment[]
}

model StudentSubjectEnrollment {
  id        String   @id @default(cuid())
  studentId String
  subjectId String
  student   Student @relation(fields: [studentId], references: [id])
  subject   Subject @relation(fields: [subjectId], references: [id])
  
  @@unique([studentId, subjectId])
}
```

## Database Interactions

### Schema-Database Flow

**Confirmed by Code**: Schema synced to database via migrations.

**Flow**:
```
Schema → Migration → Database
```

## Redis Interactions

### Schema-Redis Flow

**Confirmed by Code**: Schema doesn't directly interact with Redis.

**Flow**:
```
Schema → Database → Redis Cache
```

## Queue Interactions

### Schema-Queue Flow

**Confirmed by Code**: Schema doesn't directly interact with queues.

**Flow**:
```
Schema → Database → Queue
```

## Worker Interactions

### Schema-Worker Flow

**Confirmed by Code**: Workers use Prisma Client based on schema.

**Flow**:
```
Worker → Prisma Client → Database
```

## Business Rules

### Schema Rules

**Confirmed by Code**: Schema follows these rules:

1. **CUID**: Use CUID for primary keys
2. **Timestamps**: Include createdAt and updatedAt
3. **Indexes**: Index foreign keys and frequently queried columns
4. **Constraints**: Use constraints for data integrity
5. **Relations**: Define all relationships

### Naming Conventions

**Confirmed by Code**: Naming conventions follow these rules:

1. **Model Names**: PascalCase (User, UserProfile)
2. **Field Names**: camelCase (email, passwordHash)
3. **Enum Names**: PascalCase (UserRole)
4. **Relation Names**: camelCase (university, users)
5. **Index Names**: Auto-generated by Prisma

## Security

### Schema Security

**Confirmed by Code**: Security considerations for schema:

1. **Password Hashing**: Store password hash, not plain password
2. **Sensitive Data**: Encrypt sensitive fields if needed
3. **Access Control**: Implement row-level security
4. **Audit Logging**: Log all writes
5. **Data Validation**: Validate data at application level

## Performance Considerations

### Schema Performance

**Confirmed by Code**: Performance considerations:

1. **Indexes**: Index foreign keys and frequently queried columns
2. **Unique Constraints**: Use unique constraints sparingly
3. **Relation Loading**: Use include for eager loading
4. **Query Optimization**: Optimize queries with indexes
5. **Connection Pooling**: Use connection pooling

## Common Mistakes

### Mistake 1: Not Adding Indexes

**Symptom**: Slow queries

**Cause**: Not adding indexes

**Fix**:
```prisma
// Add index
@@index([email])
@@index([universityId])
```

### Mistake 2: Not Defining Relations

**Symptom**: Manual joins required

**Cause**: Not defining relations in schema

**Fix**:
```prisma
// Define relation
university University @relation(fields: [universityId], references: [id])
```

### Mistake 3: Not Using Constraints

**Symptom**: Invalid data in database

**Cause**: Not using constraints

**Fix**:
```prisma
// Add constraints
@@unique([email])
@@index([universityId])
```

## Debugging Guide

### Schema Debugging

**Issue**: Schema not syncing

**Investigation**:
1. Check schema syntax
2. Check migration status
3. Check database connection
4. Review migration SQL
5. Apply migration manually

**Tools**:
- Prisma Studio
- Prisma CLI
- Database logs
- Migration files

## Future Enhancements

### Soft Deletes

**Status**: Not implemented

**Proposal**: Add soft deletes:
- Add deletedAt field
- Filter deleted records
- Restore deleted records
- Better data recovery
- Audit trail

### Full Text Search

**Status**: Not implemented

**Proposal**: Add full text search:
- PostgreSQL full text search
- Better search performance
- Advanced search features
- Search indexes
- Better UX

## Production Considerations

### Production Schema

**Production Deployment**:
- Review migrations before applying
- Test migrations in staging
- Backup database before migration
- Monitor migration performance
- Rollback plan ready

### Schema Monitoring

**Monitoring Metrics**:
- Table sizes
- Index usage
- Query performance
- Constraint violations
- Migration success rate

## Example Requests

### Schema Query Example

**Request**: Query with relations

```typescript
const users = await prisma.user.findMany({
  include: { university: true, institute: true },
});
```

## Example Responses

### Schema Response

**Response**: Query results with relations

```typescript
[
  {
    id: 'user-id',
    email: 'user@example.com',
    university: { id: 'uni-id', name: 'University' },
    institute: { id: 'inst-id', name: 'Institute' }
  }
]
```

## Sequence Diagrams

### Schema Sync Flow

```
Schema Change → Generate Migration → Review Migration → Apply Migration → Database Updated
```

## Architecture Diagrams

### Schema Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Prisma Schema                                │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Models       │  │  Enums          │  │  Relations     │
│  (Tables)     │  │  (Fixed Values) │  │  (Foreign Keys) │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What is Prisma and why did you choose it?

**Answer**: Prisma chosen because:
- Type-safe database access
- Auto-generated TypeScript types
- Migration system
- Query builder
- Excellent developer experience
- Strong community support

### Q2: How do you define relationships in Prisma?

**Answer**: Relationships via:
- @relation decorator
- Foreign key fields
- Relation fields
- One-to-one, one-to-many, many-to-many
- Cascade delete options

### Q3: How do you optimize Prisma schema for performance?

**Answer**: Optimize via:
- Add indexes for frequently queried columns
- Use include for eager loading
- Optimize query plans
- Use connection pooling
- Cache frequently accessed data

## Exercises

### Exercise 1: Create a New Model

**Task**: Create a new Prisma model.

**Steps**:
1. Define model in schema
2. Add fields and types
3. Add relations
4. Add indexes
5. Generate migration

**Verification**:
- Model created
- Fields correct
- Relations defined
- Indexes added
- Migration generated

### Exercise 2: Add a Relation

**Task**: Add a relation between models.

**Steps**:
1. Add foreign key field
2. Add relation field
3. Add @relation decorator
4. Generate migration
5. Test relation

**Verification**:
- Foreign key added
- Relation defined
- Migration generated
- Relation works
- Tests pass

## Real Production Scenarios

### Scenario 1: Migration Conflict

**Situation**: Migration conflict in production

**Response**:
1. Review migration conflict
2. Resolve conflict manually
3. Test resolved migration
4. Apply migration
5. Monitor database

### Scenario 2: Schema Performance Issue

**Situation**: Query performance degraded

**Response**:
1. Identify slow queries
2. Check indexes
3. Add missing indexes
4. Optimize queries
5. Monitor performance

## Navigation

**Next Section**: [02-Migrations](./02-Migrations.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/04-Services](../03-Backend/04-Services.md) - Services
