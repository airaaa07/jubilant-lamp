# Setup Guide

## Overview

This guide provides comprehensive instructions for configuring the University ERP system after installation. It covers system configuration, user setup, module configuration, and initial data setup.

## System Configuration

### Database Configuration

**Configure Database Connection Pool**

**Confirmed by Code**: The system uses Prisma ORM with PostgreSQL. Configure connection pooling in `.env`:

```env
# Database Connection Pooling
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/university_erp?schema=public&connection_limit=10&pool_timeout=20"
```

**Connection Pool Parameters:**
- `connection_limit`: Maximum number of connections in the pool (default: 10)
- `pool_timeout`: Timeout in seconds for getting a connection from the pool (default: 20)
- `schema`: Database schema to use (default: public)

**Configure Prisma Client for Connection Pooling:**

**File**: `apps/core-api/src/prisma/prisma.service.ts`

```typescript
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor() {
    super({
      datasources: {
        db: {
          url: process.env.DATABASE_URL,
        },
      },
      log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
    });
  }

  async onModuleInit() {
    await this.$connect();
    console.log('Database connected successfully');
  }

  async onModuleDestroy() {
    await this.$disconnect();
    console.log('Database disconnected successfully');
  }

  async cleanDatabase() {
    if (process.env.NODE_ENV === 'production') return;
    
    const models = Reflect.ownKeys(this).filter(
      (key) => key[0] !== '_' && typeof this[key] === 'object',
    );

    return Promise.all(
      models.map((modelKey) => this[modelKey].deleteMany()),
    );
  }
}
```

**What This Does:**
- **Constructor**: Initializes PrismaClient with configuration
- **onModuleInit**: Connects to database when module initializes
- **onModuleDestroy**: Disconnects from database when module destroys
- **cleanDatabase**: Cleans database in development environment
- **Logging**: Logs queries in development, only errors in production

### Redis Configuration

**Configure Redis Connection**

**Confirmed by Code**: The system uses Redis for caching and queue management. Configure Redis in `.env`:

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_CLUSTER_MODE=false
REDIS_SENTINEL_HOST=
REDIS_SENTINEL_PORT=
REDIS_SENTINEL_MASTER=
```

**Redis Configuration Parameters:**
- `REDIS_HOST`: Redis server host
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_PASSWORD`: Redis password (if required)
- `REDIS_DB`: Redis database number (default: 0)
- `REDIS_CLUSTER_MODE`: Enable Redis cluster mode (default: false)
- `REDIS_SENTINEL_HOST`: Redis Sentinel host (if using Sentinel)
- `REDIS_SENTINEL_PORT`: Redis Sentinel port (if using Sentinel)
- `REDIS_SENTINEL_MASTER`: Redis Sentinel master name (if using Sentinel)

**Configure Redis Service:**

**File**: `apps/core-api/src/redis/redis.service.ts`

```typescript
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { createClient, RedisClientType } from 'redis';

@Injectable()
export class RedisService implements OnModuleInit, OnModuleDestroy {
  private client: RedisClientType;

  constructor() {
    this.client = createClient({
      socket: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT) || 6379,
        password: process.env.REDIS_PASSWORD || undefined,
      },
      database: parseInt(process.env.REDIS_DB) || 0,
    });

    this.client.on('error', (err) => console.error('Redis Client Error', err));
    this.client.on('connect', () => console.log('Redis Client Connected'));
    this.client.on('disconnect', () => console.log('Redis Client Disconnected'));
  }

  async onModuleInit() {
    await this.client.connect();
  }

  async onModuleDestroy() {
    await this.client.quit();
  }

  async get(key: string): Promise<string | null> {
    return this.client.get(key);
  }

  async set(key: string, value: string, ttl?: number): Promise<void> {
    if (ttl) {
      await this.client.setEx(key, ttl, value);
    } else {
      await this.client.set(key, value);
    }
  }

  async del(key: string): Promise<void> {
    await this.client.del(key);
  }

  async keys(pattern: string): Promise<string[]> {
    return this.client.keys(pattern);
  }

  async flushDb(): Promise<void> {
    await this.client.flushDb();
  }
}
```

**What This Does:**
- **Constructor**: Creates Redis client with configuration
- **onModuleInit**: Connects to Redis when module initializes
- **onModuleDestroy**: Disconnects from Redis when module destroys
- **get**: Gets value from Redis by key
- **set**: Sets value in Redis with optional TTL
- **del**: Deletes key from Redis
- **keys**: Gets keys matching pattern
- **flushDb**: Flushes Redis database (use with caution)

### MinIO Configuration

**Configure MinIO Connection**

**Confirmed by Code**: The system uses MinIO for object storage. Configure MinIO in `.env`:

```env
# MinIO Configuration
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USE_SSL=false
MINIO_BUCKET=university-erp
MINIO_REGION=us-east-1
```

**MinIO Configuration Parameters:**
- `MINIO_ENDPOINT`: MinIO server endpoint
- `MINIO_PORT`: MinIO server port (default: 9000)
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key
- `MINIO_USE_SSL`: Use SSL for MinIO connection (default: false)
- `MINIO_BUCKET`: Default bucket name
- `MINIO_REGION`: MinIO region (default: us-east-1)

**Configure MinIO Service:**

**File**: `apps/core-api/src/minio/minio.service.ts`

```typescript
import { Injectable, OnModuleInit } from '@nestjs/common';
import * as Minio from 'minio';

@Injectable()
export class MinioService implements OnModuleInit {
  private client: Minio.Client;
  private bucketName: string;

  constructor() {
    this.client = new Minio.Client({
      endPoint: process.env.MINIO_ENDPOINT || 'localhost',
      port: parseInt(process.env.MINIO_PORT) || 9000,
      useSSL: process.env.MINIO_USE_SSL === 'true',
      accessKey: process.env.MINIO_ACCESS_KEY || 'minioadmin',
      secretKey: process.env.MINIO_SECRET_KEY || 'minioadmin',
    });
    this.bucketName = process.env.MINIO_BUCKET || 'university-erp';
  }

  async onModuleInit() {
    await this.ensureBucketExists();
    console.log('MinIO bucket initialized');
  }

  private async ensureBucketExists() {
    const bucketExists = await this.client.bucketExists(this.bucketName);
    if (!bucketExists) {
      await this.client.makeBucket(this.bucketName, process.env.MINIO_REGION || 'us-east-1');
      console.log(`Bucket ${this.bucketName} created`);
    }
  }

  async uploadFile(
    fileName: string,
    buffer: Buffer,
    contentType: string,
  ): Promise<string> {
    await this.client.putObject(
      this.bucketName,
      fileName,
      buffer,
      buffer.length,
      { 'Content-Type': contentType },
    );
    return this.getPresignedUrl(fileName);
  }

  async getFile(fileName: string): Promise<Buffer> {
    const stream = await this.client.getObject(this.bucketName, fileName);
    const chunks: Buffer[] = [];
    
    return new Promise((resolve, reject) => {
      stream.on('data', (chunk) => chunks.push(chunk));
      stream.on('end', () => resolve(Buffer.concat(chunks)));
      stream.on('error', reject);
    });
  }

  async deleteFile(fileName: string): Promise<void> {
    await this.client.removeObject(this.bucketName, fileName);
  }

  async getPresignedUrl(fileName: string, expiry: number = 3600): Promise<string> {
    return this.client.presignedGetObject(this.bucketName, fileName, expiry);
  }

  async listFiles(prefix: string = ''): Promise<string[]> {
    const objects = await this.client.listObjects(this.bucketName, prefix, true);
    return objects.map((obj) => obj.name);
  }
}
```

**What This Does:**
- **Constructor**: Creates MinIO client with configuration
- **onModuleInit**: Ensures bucket exists when module initializes
- **ensureBucketExists**: Creates bucket if it doesn't exist
- **uploadFile**: Uploads file to MinIO
- **getFile**: Gets file from MinIO
- **deleteFile**: Deletes file from MinIO
- **getPresignedUrl**: Gets presigned URL for file
- **listFiles**: Lists files in bucket with optional prefix

### JWT Configuration

**Configure JWT Settings**

**Confirmed by Code**: The system uses JWT for authentication. Configure JWT in `.env`:

```env
# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=7d
JWT_ISSUER=university-erp
JWT_AUDIENCE=university-erp-users
```

**JWT Configuration Parameters:**
- `JWT_SECRET`: Secret key for signing JWT tokens (MUST be changed in production)
- `JWT_EXPIRES_IN**: Access token expiry time (default: 1h)
- `REFRESH_TOKEN_EXPIRES_IN`: Refresh token expiry time (default: 7d)
- `JWT_ISSUER`: JWT issuer (default: university-erp)
- `JWT_AUDIENCE`: JWT audience (default: university-erp-users)

**Configure JWT Service:**

**File**: `apps/core-api/src/auth/jwt.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtAuthService {
  constructor(private jwtService: JwtService) {}

  async generateAccessToken(payload: any): Promise<string> {
    return this.jwtService.sign(payload, {
      expiresIn: process.env.JWT_EXPIRES_IN || '1h',
      issuer: process.env.JWT_ISSUER || 'university-erp',
      audience: process.env.JWT_AUDIENCE || 'university-erp-users',
    });
  }

  async generateRefreshToken(payload: any): Promise<string> {
    return this.jwtService.sign(payload, {
      expiresIn: process.env.REFRESH_TOKEN_EXPIRES_IN || '7d',
      issuer: process.env.JWT_ISSUER || 'university-erp',
      audience: process.env.JWT_AUDIENCE || 'university-erp-users',
    });
  }

  async verifyToken(token: string): Promise<any> {
    return this.jwtService.verify(token, {
      issuer: process.env.JWT_ISSUER || 'university-erp',
      audience: process.env.JWT_AUDIENCE || 'university-erp-users',
    });
  }

  async decodeToken(token: string): Promise<any> {
    return this.jwtService.decode(token);
  }
}
```

**What This Does:**
- **generateAccessToken**: Generates access token with expiry
- **generateRefreshToken**: Generates refresh token with expiry
- **verifyToken**: Verifies token signature and claims
- **decodeToken**: Decodes token without verification

## User Setup

### Create Admin User

**Create initial admin user using Prisma Studio:**

```bash
# Open Prisma Studio
npx prisma studio
```

**Navigate to User model and create:**

```json
{
  "id": "admin-user-id",
  "email": "admin@university.edu",
  "passwordHash": "$2b$10$abcdefghijklmnopqrstuvwxyz", // Hashed password
  "name": "System Administrator",
  "role": "ADMIN",
  "isActive": true,
  "emailVerified": true,
  "createdAt": "2024-01-01T10:00:00.000Z",
  "updatedAt": "2024-01-01T10:00:00.000Z"
}
```

**Or create admin user using seed script:**

**File**: `apps/core-api/prisma/seed.ts`

```typescript
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
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

**Run seed script:**

```bash
cd apps/core-api
npx prisma db seed
```

### Create Role Assignments

**Create role assignments for admin user:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create role assignment for admin
await prisma.userRoleAssignment.upsert({
  where: {
    userId_roleId: {
      userId: admin.id,
      roleId: 'admin-role-id',
    },
  },
  update: {},
  create: {
    userId: admin.id,
    roleId: 'admin-role-id',
    assignedAt: new Date(),
    assignedBy: admin.id,
  },
});
```

### Create Initial Roles

**Create initial roles in the system:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create admin role
const adminRole = await prisma.role.upsert({
  where: { name: 'ADMIN' },
  update: {},
  create: {
    id: 'admin-role-id',
    name: 'ADMIN',
    description: 'System administrator with full access',
    permissions: ['*'], // Full access
    isActive: true,
  },
});

// Create staff role
const staffRole = await prisma.role.upsert({
  where: { name: 'STAFF' },
  update: {},
  create: {
    id: 'staff-role-id',
    name: 'STAFF',
    description: 'Staff member with limited access',
    permissions: [
      'users.read',
      'students.read',
      'courses.read',
      'attendance.read',
      'attendance.write',
    ],
    isActive: true,
  },
});

// Create student role
const studentRole = await prisma.role.upsert({
  where: { name: 'STUDENT' },
  update: {},
  create: {
    id: 'student-role-id',
    name: 'STUDENT',
    description: 'Student with self-service access',
    permissions: [
      'profile.read',
      'profile.write',
      'courses.read',
      'attendance.read',
      'results.read',
    ],
    isActive: true,
  },
});
```

## Module Configuration

### Configure Module Access

**Configure which modules are accessible to which roles:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Configure module access for admin
await prisma.moduleAccess.create({
  data: {
    roleId: adminRole.id,
    module: 'ALL',
    accessLevel: 'FULL',
  },
});

// Configure module access for staff
await prisma.moduleAccess.createMany({
  data: [
    {
      roleId: staffRole.id,
      module: 'USERS',
      accessLevel: 'READ',
    },
    {
      roleId: staffRole.id,
      module: 'STUDENTS',
      accessLevel: 'READ_WRITE',
    },
    {
      roleId: staffRole.id,
      module: 'COURSES',
      accessLevel: 'READ',
    },
    {
      roleId: staffRole.id,
      module: 'ATTENDANCE',
      accessLevel: 'READ_WRITE',
    },
  ],
});

// Configure module access for students
await prisma.moduleAccess.createMany({
  data: [
    {
      roleId: studentRole.id,
      module: 'PROFILE',
      accessLevel: 'READ_WRITE',
    },
    {
      roleId: studentRole.id,
      module: 'COURSES',
      accessLevel: 'READ',
    },
    {
      roleId: studentRole.id,
      module: 'ATTENDANCE',
      accessLevel: 'READ',
    },
    {
      roleId: studentRole.id,
      module: 'RESULTS',
      accessLevel: 'READ',
    },
  ],
});
```

### Configure Academic Year

**Configure the current academic year:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create academic year
const academicYear = await prisma.academicYear.upsert({
  where: { year: '2024-2025' },
  update: {},
  create: {
    id: 'academic-year-2024-2025',
    year: '2024-2025',
    startDate: new Date('2024-07-01'),
    endDate: new Date('2025-06-30'),
    isActive: true,
  },
});
```

### Configure University Structure

**Configure university departments, courses, and streams:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create university department
const department = await prisma.universityDepartment.upsert({
  where: { code: 'CS' },
  update: {},
  create: {
    id: 'department-cs',
    code: 'CS',
    name: 'Computer Science',
    description: 'Computer Science Department',
    isActive: true,
  },
});

// Create university course
const course = await prisma.universityCourse.upsert({
  where: { code: 'BTECH-CS' },
  update: {},
  create: {
    id: 'course-btech-cs',
    code: 'BTECH-CS',
    name: 'Bachelor of Technology in Computer Science',
    departmentId: department.id,
    duration: 4,
    description: 'B.Tech in Computer Science',
    isActive: true,
  },
});

// Create university stream
const stream = await prisma.universityStream.upsert({
  where: { code: 'CS-REGULAR' },
  update: {},
  create: {
    id: 'stream-cs-regular',
    code: 'CS-REGULAR',
    name: 'Computer Science Regular',
    courseId: course.id,
    description: 'Regular stream for Computer Science',
    isActive: true,
  },
});
```

## Initial Data Setup

### Configure System Settings

**Configure system-wide settings:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create system settings
await prisma.systemSettings.createMany({
  data: [
    {
      key: 'SYSTEM_NAME',
      value: 'University ERP',
      description: 'System name',
    },
    {
      key: 'SYSTEM_EMAIL',
      value: 'noreply@university.edu',
      description: 'System email',
    },
    {
      key: 'DEFAULT_LANGUAGE',
      value: 'en',
      description: 'Default language',
    },
    {
      key: 'TIMEZONE',
      value: 'Asia/Kolkata',
      description: 'System timezone',
    },
    {
      key: 'DATE_FORMAT',
      value: 'DD/MM/YYYY',
      description: 'Date format',
    },
  ],
  skipDuplicates: true,
});
```

### Configure Attendance Settings

**Configure attendance settings:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create attendance config
await prisma.attendanceConfig.create({
  data: {
    id: 'attendance-config',
    requiredAttendancePercentage: 75,
    gracePeriodMinutes: 15,
    allowLateMarking: true,
    autoMarkAbsent: true,
    autoMarkAbsentAfterMinutes: 30,
  },
});
```

### Configure Exam Settings

**Configure exam settings:**

**File**: `apps/core-api/prisma/seed.ts` (add to existing seed)

```typescript
// Create exam config
await prisma.examConfig.create({
  data: {
    id: 'exam-config',
    passingPercentage: 40,
    allowReassessment: true,
    reassessmentFee: 500,
    reassessmentDeadlineDays: 7,
    allowSupplementary: true,
    supplementaryFee: 1000,
  },
});
```

## Verification

### Verify Configuration

**Verify database connection:**

```bash
cd apps/core-api
npx prisma db push
```

**Verify Redis connection:**

```bash
redis-cli ping
# Expected output: PONG
```

**Verify MinIO connection:**

```bash
# Open MinIO Console in browser
http://localhost:9001
```

**Verify admin user creation:**

```bash
# Open Prisma Studio
npx prisma studio
# Navigate to User model and verify admin user
```

### Test Login

**Test admin login:**

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@university.edu","password":"admin123"}'
```

**Expected Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "admin-user-id",
    "email": "admin@university.edu",
    "name": "System Administrator",
    "role": "ADMIN"
  }
}
```

## Next Steps

After successful setup, proceed to:
- [Quick Start](./03-Quick-Start.md) - Get started quickly
- [Development Environment](./04-Development-Environment.md) - Set up your development environment
- [Project Structure](./05-Project-Structure.md) - Understand the project structure

## Troubleshooting

### Common Issues

**Issue: Database connection failed**

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# Check database logs
docker-compose logs postgres
```

**Issue: Redis connection failed**

**Solution:**
```bash
# Check if Redis is running
docker-compose ps redis

# Restart Redis
docker-compose restart redis redis

# Check Redis logs
docker-compose logs redis
```

**Issue: MinIO connection failed**

**Solution:**
```bash
# Check if MinIO is running
docker-compose ps minio

# Restart MinIO
docker-compose restart minio

# Check MinIO logs
docker-compose logs minio
```

**Issue: Admin user creation failed**

**Solution:**
```bash
# Check Prisma logs
npx prisma db seed

# Verify database connection
npx prisma db push

# Check user data in Prisma Studio
npx prisma studio
```

## Additional Resources

- [Installation Guide](./01-Installation.md) - Installation instructions
- [Quick Start](./03-Quick-Start.md) - Quick start guide
- [Development Environment](./04-Development-Environment.md) - Development environment setup
- [Prisma Documentation](https://www.prisma.io/docs)
- [Redis Documentation](https://redis.io/docs)
- [MinIO Documentation](https://docs.min.io/)
