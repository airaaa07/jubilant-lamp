# Database Guide

## Overview

This document provides comprehensive information about the database architecture, schema, migrations, and best practices for the University ERP system.

## Database Technology

**Confirmed by Code**: The University ERP uses PostgreSQL as the primary database.

**Why PostgreSQL:**
- Open-source and reliable
- ACID compliance
- Advanced features (JSON, arrays, etc.)
- Excellent performance
- Strong community support
- Full-text search capabilities

**Version:**
- PostgreSQL 14+

## Database Architecture

**Confirmed by Code**: The database follows a normalized schema design.

**Database Schema Overview:**

```
┌─────────────────────────────────────────────────────────┐
│              Core Tables                                   │
├─────────────────────────────────────────────────────────┤
│ User, Role, UserRoleAssignment                           │
│ Student, Course, Subject, Enrollment                     │
│ Attendance, Exam, Result                                 │
│ Fee, Payment                                             │
│ LibraryBook, LibraryIssue                                │
│ Hostel, Room, RoomAllocation                             │
│ TransportRoute, TransportPass                             │
└─────────────────────────────────────────────────────────┘
```

 ORM

**Confirmed by Code**: The University ERP uses Prisma ORM for database access.

**Why Prisma:**
- Type-safe database access
- Auto-generated TypeScript types
- Excellent developer experience
- Migration management
- Query builder
- Database agnostic (mostly)

**Prisma Configuration:**

**File**: `apps/core-api/prisma/schema.prisma`

```prisma
// This is your Prisma schema file

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// User model
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  passwordHash  String
  name          String
  role          Role      @default(STUDENT)
  isActive      Boolean   @default(true)
  emailVerified Boolean   @default(false)
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  student       Student?
  staff         Staff?
  libraryIssues LibraryIssue[]
  transportPass TransportPass[]

  @@map("users")
}

// Role enum
enum Role {
  ADMIN
  STAFF
  STUDENT
}

// Student model
model Student {
  id           String    @id @default(cuid())
  userId       String    @unique
  rollNumber   String    @unique
  batch        String
  course       String
  section      String
  semester     Int
  status       StudentStatus @default(ACTIVE)
  admissionDate DateTime
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt

  user         User      @relation(fields: [userId], references: [id])
  enrollments  Enrollment[]
  attendance   Attendance[]
  results      Result[]
  fees         Fee[]
  roomAllocation RoomAllocation?

  @@map("students")
}

// Student status enum
enum StudentStatus {
  ACTIVE
  INACTIVE
  GRADUATED
  SUSPENDED
}

// Course model
model Course {
  id          String    @id @default(cuid())
  code        String    @unique
  name        String
  department  String
  duration    Int
  credits     Int
  isActive    Boolean   @default(true)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  enrollments Enrollment[]
  subjects    Subject[]

  @@map("courses")
}

// Subject model
model Subject {
  id          String    @id @default(cuid())
  code        String    @unique
  name        String
  courseId    String
  credits     Int
  semester    Int
  isActive    Boolean   @default(true)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  course      Course    @relation(fields: [courseId], references: [id])
  enrollments Enrollment[]
  attendance  Attendance[]
  results     Result[]

  @@map("subjects")
}

// Enrollment model
model Enrollment {
  id         String   @id @default(cuid())
  studentId  String
  subjectId  String
  semester   Int
  createdAt  DateTime @default(now())

  student    Student  @relation(fields: [studentId], references: [id])
  subject    Subject  @relation(fields: [subjectId], references: [id])

  @@unique([studentId, subjectId, semester])
  @@map("enrollments")
}

// Attendance model
model Attendance {
  id        String   @id @default(cuid())
  studentId String
  subjectId String
  date      DateTime
  status    AttendanceStatus
  markedBy  String
  markedAt  DateTime @default(now())
  createdAt DateTime @default(now())

  student   Student  @relation(fields: [studentId], references: [id])
  subject   Subject  @relation(fields: [subjectId], references: [id])

  @@unique([studentId, subjectId, date])
  @@map("attendance")
}

// Attendance status enum
enum AttendanceStatus {
  PRESENT
  ABSENT
  LATE
  EXCUSED
}

// Exam model
model Exam {
  id          String    @id @default(cuid())
  name        String
  course      String
  semester    Int
  startDate   DateTime
  endDate     DateTime
  status      ExamStatus @default(SCHEDULED)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  results     Result[]

  @@map("exams")
}

// Exam status enum
enum ExamStatus {
  SCHEDULED
  IN_PROGRESS
  COMPLETED
  CANCELLED
}

// Result model
model Result {
  id        String   @id @default(cuid())
  studentId String
  examId    String
  subjectId String
  marks     Float
  grade     String
  createdAt DateTime @default(now())

  student   Student  @relation(fields: [studentId], references: [id])
  subject   Subject  @relation(fields: [subjectId], references: [id])
  exam      Exam     @relation(fields: [examId], references: [id])

  @@unique([studentId, examId, subjectId])
  @@map("results")
}

// Fee model
model Fee {
  id          String    @id @default(cuid())
  studentId   String
  type        FeeType
  amount      Float
  dueDate     DateTime
  status      FeeStatus @default(PENDING)
  paidAmount  Float     @default(0)
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  student     Student   @relation(fields: [studentId], references: [id])
  payments    Payment[]

  @@map("fees")
}

// Fee type enum
enum FeeType {
  TUITION
  HOSTEL
  TRANSPORT
  LIBRARY
  OTHER
}

// Fee status enum
enum FeeStatus {
  PENDING
  PARTIALLY_PAID
  PAID
  OVERDUE
}

// Payment model
model Payment {
  id            String   @id @default(cuid())
  feeId         String
  amount        Float
  paymentMethod String
  transactionId String   @unique
  paidAt        DateTime @default(now())
  createdAt     DateTime @default(now())

  fee           Fee      @relation(fields: [feeId], references: [id])

  @@map("payments")
}

// Library book model
model LibraryBook {
  id              String   @id @default(cuid())
  isbn            String   @unique
  title           String
  author          String
  category        String
  publisher       String?
  publishedYear   Int?
  totalCopies     Int
  availableCopies Int
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  issues          LibraryIssue[]

  @@map("library_books")
}

// Library issue model
model LibraryIssue {
  id         String   @id @default(cuid())
  bookId     String
  userId     String
  issueDate  DateTime @default(now())
  dueDate    DateTime
  returnDate DateTime?
  fine       Float    @default(0)
  status     IssueStatus @default(ISSUED)
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  book       LibraryBook @relation(fields: [bookId], references: [id])
  user       User      @relation(fields: [userId], references: [id])

  @@map("library_issues")
}

// Issue status enum
enum IssueStatus {
  ISSUED
  RETURNED
  OVERDUE
}

// Hostel model
model Hostel {
  id          String   @id @default(cuid())
  name        String   @unique
  location    String
  capacity    Int
  warden      String?
  contact     String?
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  rooms       Room[]

  @@map("hostels")
}

// Room model
model Room {
  id         String   @id @default(cuid())
  hostelId   String
  roomNumber String
  capacity   Int
  occupied   Int      @default(0)
  floor      Int?
  isActive   Boolean  @default(true)
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  hostel     Hostel   @relation(fields: [hostelId], references: [id])
  allocations RoomAllocation[]

  @@unique([hostelId, roomNumber])
  @@map("rooms")
}

// Room allocation model
model RoomAllocation {
  id         String   @id @default(cuid())
  studentId  String
  roomId     String
  startDate  DateTime
  endDate    DateTime?
  status     AllocationStatus @default(ACTIVE)
  createdAt  DateTime @default(now())
  updatedAt  DateTime @updatedAt

  student    Student  @relation(fields: [studentId], references: [id])
  room       Room     @relation(fields: [roomId], references: [id])

  @@map("room_allocations")
}

// Allocation status enum
enum AllocationStatus {
  ACTIVE
  INACTIVE
  COMPLETED
}

// Transport route model
model TransportRoute {
  id          String   @id @default(cuid())
  name        String   @unique
  stops       String[]
  capacity    Int
  fare        Float
  isActive    Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  passes      TransportPass[]

  @@map("transport_routes")
}

// Transport pass model
model TransportPass {
  id          String   @id @default(cuid())
  userId      String
  routeId     String
  duration    PassDuration
  validFrom   DateTime
  validTo     DateTime
  status      PassStatus @default(ACTIVE)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  user        User          @relation(fields: [userId], references: [id])
  route       TransportRoute @relation(fields: [routeId], references: [id])

  @@map("transport_passes")
}

// Pass duration enum
enum PassDuration {
  MONTHLY
  SEMESTER
  YEARLY
}

// Pass status enum
enum PassStatus {
  ACTIVE
  EXPIRED
  CANCELLED
}
```

## Database Migrations

**Confirmed by Code**: The University ERP uses Prisma migrations for schema changes.

### Creating Migrations

**Create a new migration:**

```bash
cd apps/core-api

# Create migration
npx prisma migrate dev --name add_user_profile

# This will:
# 1. Update schema.prisma
# 2. Generate migration SQL
# 3. Apply migration to database
# 4. Regenerate Prisma Client
```

**Example Migration:**

**File**: `prisma/migrations/20240101100000_add_user_profile/migration.sql`

```sql
-- AlterTable
ALTER TABLE "users" ADD COLUMN "profile" JSONB;
```

### Applying Migrations

**Apply pending migrations:**

```bash
cd apps/core-api

# Apply all pending migrations
npx prisma migrate dev

# Apply specific migration
npx prisma migrate deploy
```

### Resetting Database

**Reset database (WARNING: deletes all data):**

```bash
cd apps/core-api

# Reset database
npx prisma migrate reset

# This will:
# 1. Drop all tables
# 2. Re-run all migrations
# 3. Re-seed database
```

### Migration Status

**Check migration status:**

```bash
cd apps/core-api

# Check migration status
npx prisma migrate status
```

**Output:**
```
Schema migrations from main database

Migration ID    Applied At              Migration Name
20240101100000  2024-01-01 10:00:00    init
20240101100001  2024-01-01 11:00:00    add_user_profile
```

## Database Seeding

**Confirmed by Code**: The University ERP uses Prisma seed for initial data.

### Seed Script

**File**: `apps/core-api/prisma/seed.ts`

```typescript
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('Starting seed...');

  // Create admin user
  const hashedPassword = await bcrypt.hash('admin123', 10);

  const admin = await prisma.user.upsert({
    where: { email: 'admin@university.edu' },
    update: {},
    create: {
      id: 'admin-user-id',
      email: 'admin@university.edu',
      passwordHash: hashedPassword,
      name: 'System Administrator',
      role: 'ADMIN',
      isActive: true,
      emailVerified: true,
    },
  });

  console.log({ admin });

  // Create course
  const course = await prisma.course.upsert({
    where: { code: 'BTECH-CS' },
    update: {},
    create: {
      id: 'course-btech-cs',
      code: 'BTECH-CS',
      name: 'Bachelor of Technology in Computer Science',
      department: 'Computer Science',
      duration: 4,
      credits: 160,
      isActive: true,
    },
  });

  console.log({ course });

  // Create subject
  const subject = await prisma.subject.upsert({
    where: { code: 'CS101' },
    update: {},
    create: {
      id: 'subject-cs101',
      code: 'CS101',
      name: 'Introduction to Programming',
      courseId: course.id,
      credits: 4,
      semester: 1,
      isActive: true,
    },
  });

  console.log({ subject });

  console.log('Seed completed successfully');
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
```

### Running Seed

**Run seed script:**

```bash
cd apps/core-api

# Run seed
npx prisma db seed
```

## Database Queries

**Confirmed by Code**: The University ERP uses Prisma for database queries.

### Basic Queries

**Find All:**

```typescript
// Find all users
const users = await prisma.user.findMany();

// Find all students with pagination
const students = await prisma.student.findMany({
  skip: 0,
  take: 10,
});

// Find with filtering
const activeStudents = await prisma.student.findMany({
  where: {
    status: 'ACTIVE',
  },
});
```

**Find One:**

```typescript
// Find by ID
const user = await prisma.user.findUnique({
  where: {
    id: 'user-id',
  },
});

// Find by unique field
const user = await prisma.user.findUnique({
  where: {
    email: 'user@example.com',
  },
});
```

**Create:**

```typescript
// Create user
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    passwordHash: 'hashed-password',
    name: 'John Doe',
    role: 'STUDENT',
  },
});
```

**Update:**

```typescript
// Update user
const user = await prisma.user.update({
  where: {
    id: 'user-id',
  },
  data: {
    name: 'Updated Name',
  },
});
```

**Delete:**

```typescript
// Delete user
const user = await prisma.user.delete({
  where: {
    id: 'user-id',
  },
});
```

### Advanced Queries

**Include Relations:**

```typescript
// Find student with user
const student = await prisma.student.findUnique({
  where: {
    id: 'student-id',
  },
  include: {
    user: true,
  },
});

// Find student with enrollments and subjects
const student = await prisma.student.findUnique({
  where: {
    id: 'student-id',
  },
  include: {
    enrollments: {
      include: {
        subject: true,
      },
    },
  },
});
```

**Select Specific Fields:**

```typescript
// Select specific fields
const user = await prisma.user.findUnique({
  where: {
    id: 'user-id',
  },
  select: {
    id: true,
    email: true,
    name: true,
  },
});
```

**Where Conditions:**

```typescript
// Complex where conditions
const students = await prisma.student.findMany({
  where: {
    AND: [
      { status: 'ACTIVE' },
      { batch: '2024' },
    ],
  },
});

// OR conditions
const students = await prisma.student.findMany({
  where: {
    OR: [
      { status: 'ACTIVE' },
      { status: 'INACTIVE' },
    ],
  },
});

// Nested conditions
const students = await prisma.student.findMany({
  where: {
    user: {
      email: {
        contains: '@university.edu',
      },
    },
  },
});
```

**Sorting:**

```typescript
// Sort by name
const users = await prisma.user.findMany({
  orderBy: {
    name: 'asc',
  },
});

// Sort by multiple fields
const students = await prisma.student.findMany({
  orderBy: [
    {
      batch: 'desc',
    },
    {
      rollNumber: 'asc',
    },
  ],
});
```

**Aggregation:**

```typescript
// Count
const count = await prisma.user.count();

// Count with filtering
const count = await prisma.student.count({
  where: {
    status: 'ACTIVE',
  },
});

// Sum
const total = await prisma.fee.aggregate({
  _sum: {
    amount: true,
  },
});

// Average
const average = await prisma.result.aggregate({
  _avg: {
    marks: true,
  },
});
```

**Transactions:**

```typescript
// Transaction
await prisma.$transaction(async (tx) => {
  // Create user
  const user = await tx.user.create({
    data: {
      email: 'user@example.com',
      passwordHash: 'hashed-password',
      name: 'John Doe',
      role: 'STUDENT',
    },
  });

  // Create student
  const student = await tx.student.create({
    data: {
      userId: user.id,
      rollNumber: '2024001',
      batch: '2024',
      course: 'BTECH-CS',
      section: 'A',
      semester: 1,
      admissionDate: new Date(),
    },
  });

  return { user, student };
});
```

## Database Optimization

**Confirmed by Code**: The University ERP uses various optimization techniques.

### Indexes

**Add indexes to schema:**

```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String
  
  @@index([name])
  @@map("users")
}
```

**Add composite index:**

```prisma
model Attendance {
  id        String   @id @default(cuid())
  studentId String
  subjectId String
  date      DateTime
  
  @@index([studentId, date])
  @@index([subjectId, date])
  @@map("attendance")
}
```

### Query Optimization

**Avoid N+1 queries:**

```typescript
// Bad - N+1 queries
const students = await prisma.student.findMany();
for (const student of students) {
  const user = await prisma.user.findUnique({
    where: { id: student.userId },
  });
}

// Good - Single query with include
const students = await prisma.student.findMany({
  include: {
    user: true,
  },
});
```

**Use select instead of include:**

```typescript
// Good - Select only needed fields
const students = await prisma.student.findMany({
  select: {
    id: true,
    rollNumber: true,
    user: {
      select: {
        name: true,
        email: true,
      },
    },
  },
});
```

### Connection Pooling

**Configure connection pooling in DATABASE_URL:**

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/university_erp?schema=public&connection_limit=10&pool_timeout=20"
```

## Database Backup and Restore

### Backup

**Backup database:**

```bash
# Backup to file
pg_dump -h localhost -U postgres -d university_erp > backup.sql

# Backup with custom format
pg_dump -h localhost -U postgres -d university_erp -F c -f backup.dump
```

### Restore

**Restore database:**

```bash
# Restore from file
psql -h localhost -U postgres -d university_erp < backup.sql

# Restore from custom format
pg_restore -h localhost -U postgres -d university_erp backup.dump
```

## Database Monitoring

**Confirmed by Code**: The University ERP uses Prisma for database monitoring.

### Query Logging

**Enable query logging in development:**

```typescript
// In prisma.service.ts
constructor() {
  super({
    log: process.env.NODE_ENV === 'development' 
      ? ['query', 'error', 'warn'] 
      : ['error'],
  });
}
```

### Slow Query Logging

**Use PostgreSQL slow query logging:**

```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Reload configuration
SELECT pg_reload_conf();
```

## Database Security

**Confirmed by Code**: The University ERP follows database security best practices.

### Security Best Practices

1. **Never commit sensitive data**
   - Never commit database credentials
   - Use environment variables
   - Use .env files (gitignored)

2. **Use parameterized queries**
   - Prisma automatically parameterizes queries
   - Never use raw SQL with user input

3. **Principle of least privilege**
   - Use separate database users for different purposes
   - Grant minimum required permissions

4. **Regular backups**
   - Schedule regular database backups
   - Test restore procedures

5. **Encryption at rest**
   - Enable disk encryption
   - Use SSL for database connections

## Troubleshooting

### Common Issues

**Issue: Migration conflict**

**Solution:**
```bash
# Resolve migration conflict
npx prisma migrate resolve --applied <migration-name>
```

**Issue: Connection pool exhausted**

**Solution:**
```bash
# Increase connection pool size
# Update DATABASE_URL
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/university_erp?schema=public&connection_limit=20"
```

**Issue: Slow queries**

**Solution:**
```bash
# Analyze slow queries
# Use EXPLAIN ANALYZE
npx prisma.$queryRaw`EXPLAIN ANALYZE SELECT * FROM users WHERE email = ${email}`
```

## Additional Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database Best Practices](https://www.prisma.io/docs/guides/performance-and-optimization)
