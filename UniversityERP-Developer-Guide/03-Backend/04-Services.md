# Services

## Purpose

This document explains the service pattern used in the University ERP backend. It details how services handle business logic, interact with databases and external services, and implement core functionality.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS services for business logic. Understanding services is critical for:
- Implementing business logic
- Interacting with databases
- Integrating with external services
- Implementing caching
- Testing business logic

Without understanding services, developers may struggle to implement business logic correctly.

## Where This Is Used

- **Onboarding**: New developers learn service pattern
- **Feature Development**: Implementing business logic
- **Code Reviews**: Reviewing service code
- **Debugging**: Debugging business logic issues
- **Testing**: Testing business logic

## Dependencies

### Service Dependencies

**Confirmed by Code**: Services depend on:

- **NestJS Injectable**: Dependency injection
- **PrismaService**: Database access
- **RedisService**: Caching
- **MinioService**: Object storage
- **Other Services**: Service-to-service communication

## Internal Architecture

### Service Architecture

**Confirmed by Code**: Services handle business logic.

```
┌─────────────────────────────────────────────────────────┐
│                  Service                                   │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Database     │  │  Cache          │  │  External      │
│  Operations   │  │  Operations     │  │  Services      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Service Definition

**Confirmed by Code**: Services defined with @Injectable decorator.

**Basic Service**:
```typescript
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private redis: RedisService,
  ) {}

  async findAll() {
    return this.prisma.user.findMany();
  }
}
```

**What This Does**:
- **@Injectable**: Marks class as provider
- **constructor**: Injects dependencies
- **findAll()**: Implements business logic

### Database Operations

**Confirmed by Code**: Services interact with database via Prisma.

**Find Operations**:
```typescript
async findAll(query: QueryUserDto) {
  const { page, limit, search } = query;
  
  const skip = (page - 1) * limit;
  
  const where = search ? {
    OR: [
      { email: { contains: search, mode: 'insensitive' } },
      { name: { contains: search, mode: 'insensitive' } },
    ],
  } : undefined;
  
  const [users, total] = await Promise.all([
    this.prisma.user.findMany({
      where,
      skip,
      take: limit,
    }),
    this.prisma.user.count({ where }),
  ]);
  
  return {
    data: users,
    meta: { total, page, limit },
  };
}

async findOne(id: string) {
  const user = await this.prisma.user.findUnique({
    where: { id },
  });
  
  if (!user) {
    throw new NotFoundException('User not found');
  }
  
  return user;
}
```

**Create Operations**:
```typescript
async create(dto: CreateUserDto) {
  const existingUser = await this.prisma.user.findUnique({
    where: { email: dto.email },
  });
  
  if (existingUser) {
    throw new ConflictException('Email already exists');
  }
  
  const hashedPassword = await bcrypt.hash(dto.password, 10);
  
  const user = await this.prisma.user.create({
    data: {
      ...dto,
      passwordHash: hashedPassword,
    },
  });
  
  return user;
}
```

**Update Operations**:
```typescript
async update(id: string, dto: UpdateUserDto) {
  const user = await this.findOne(id);
  
  if (dto.email && dto.email !== user.email) {
    const existingUser = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });
    
    if (existingUser) {
      throw new ConflictException('Email already exists');
    }
  }
  
  const updatedUser = await this.prisma.user.update({
    where: { id },
    data: dto,
  });
  
  return updatedUser;
}
```

**Delete Operations**:
```typescript
async remove(id: string) {
  const user = await this.findOne(id);
  
  await this.prisma.user.delete({
    where: { id },
  });
  
  return { success: true };
}
```

### Transaction Operations

**Confirmed by Code**: Services use transactions for atomic operations.

**Transaction Example**:
```typescript
async createUserWithProfile(dto: CreateUserWithProfileDto) {
  return this.prisma.$transaction(async (tx) => {
    const user = await tx.user.create({
      data: {
        email: dto.email,
        passwordHash: await bcrypt.hash(dto.password, 10),
      },
    });
    
    const profile = await tx.userProfile.create({
      data: {
        userId: user.id,
        ...dto.profile,
      },
    });
    
    return { user, profile };
  });
}
```

**What This Does**:
- **$transaction**: Wraps operations in transaction
- **tx**: Transaction client for all operations
- **Atomicity**: All operations succeed or all fail
- **Rollback**: Automatic rollback on failure

### Caching Operations

**Confirmed by Code**: Services use Redis for caching.

**Cache-Aside Pattern**:
```typescript
async getUniversity(id: string) {
  const cacheKey = `university:${id}`;
  const cached = await this.redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const university = await this.prisma.university.findUnique({
    where: { id },
    include: { institutes: true },
  });
  
  await this.redis.setex(cacheKey, 300, JSON.stringify(university));
  
  return university;
}

async updateUniversity(id: string, dto: UpdateUniversityDto) {
  const university = await this.prisma.university.update({
    where: { id },
    data: dto,
  });
  
  await this.redis.del(`university:${id}`);
  
  return university;
}
```

**What This Does**:
- **Cache Check**: Check cache before database
- **Cache Hit**: Return cached data if available
- **Cache Miss**: Query database
- **Cache Set**: Store result in cache with TTL
- **Cache Invalidation**: Delete cache on update

### External Service Integration

**Confirmed by Code**: Services integrate with external services.

**Email Service**:
```typescript
@Injectable()
export class NotificationService {
  constructor(
    @InjectQueue('notifications') private notificationsQueue: Queue,
  ) {}

  async sendEmail(dto: EmailDto) {
    await this.notificationsQueue.add('email', dto);
    return { success: true, message: 'Email queued' };
  }
}
```

**MinIO Service**:
```typescript
@Injectable()
export class DocumentsService {
  constructor(
    private prisma: PrismaService,
    private minio: MinioService,
  ) {}

  async uploadDocument(file: Express.Multer.File, metadata: DocumentMetadata) {
    const fileName = `${metadata.type}/${Date.now()}-${file.originalname}`;
    
    await this.minio.upload(fileName, file.buffer, file.mimetype);
    
    const document = await this.prisma.document.create({
      data: {
        name: file.originalname,
        fileName,
        mimeType: file.mimetype,
        size: file.size,
        ...metadata,
      },
    });
    
    return document;
  }

  async downloadDocument(id: string) {
    const document = await this.prisma.document.findUnique({
      where: { id },
    });
    
    if (!document) {
      throw new NotFoundException('Document not found');
    }
    
    const url = await this.minio.getPresignedUrl(document.fileName);
    
    return url;
  }
}
```

## Database Interactions

### Prisma Service Integration

**Confirmed by Code**: Services use PrismaService for database access.

**PrismaService Usage**:
```typescript
@Injectable()
export class MyService {
  constructor(private prisma: PrismaService) {}

  async myMethod() {
    return this.prisma.model.findMany();
  }
}
```

**What This Does**:
- Injects PrismaService
- Uses Prisma Client methods
- Type-safe database access

## Redis Interactions

### Redis Service Integration

**Confirmed by Code**: Services use RedisService for caching.

**RedisService Usage**:
```typescript
@Injectable()
export class MyService {
  constructor(private redis: RedisService) {}

  async myMethod() {
    const cached = await this.redis.get('key');
    if (cached) return JSON.parse(cached);
    
    const data = await this.prisma.model.findMany();
    await this.redis.setex('key', 300, JSON.stringify(data));
    return data;
  }
}
```

**What This Does**:
- Injects RedisService
- Checks cache before database
- Stores result in cache

## Queue Interactions

### Bull Queue Integration

**Confirmed by Code**: Services submit jobs to Bull queues.

**Queue Usage**:
```typescript
@Injectable()
export class MyService {
  constructor(
    @InjectQueue('notifications') private notificationsQueue: Queue,
  ) {}

  async myMethod() {
    await this.notificationsQueue.add('email', data);
  }
}
```

**What This Does**:
- Injects Bull queue
- Adds job to queue
- Job processed asynchronously

## Worker Interactions

### Service-Worker Communication

**Confirmed by Code**: Services communicate with workers via queues.

**Flow**:
```
Service → Queue → Worker → Process → Result
```

**Example**:
```typescript
// Service
async sendEmail(dto: EmailDto) {
  await this.notificationsQueue.add('email', dto);
}

// Worker (separate service)
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    await this.mailService.sendEmail(job.data);
  }
}
```

## Business Rules

### Service Rules

**Confirmed by Code**: Services follow these rules:

1. **Business Logic**: Services contain business logic
2. **Validation**: Validate data before database operations
3. **Error Handling**: Handle errors appropriately
4. **Caching**: Cache frequently accessed data
5. **Transactions**: Use transactions for related operations

### Error Handling Rules

**Confirmed by Code**: Error handling follows these rules:

1. **Validation Errors**: Throw BadRequestException
2. **Not Found**: Throw NotFoundException
3. **Conflict**: Throw ConflictException
4. **Unauthorized**: Throw UnauthorizedException
5. **Forbidden**: Throw ForbiddenException

## Security

### Service Security

**Confirmed by Code**: Security measures in services:

1. **Data Scoping**: Scope data by tenant
2. **Input Validation**: Validate all inputs
3. **Output Sanitization**: Sanitize outputs
4. **Password Hashing**: Hash passwords before storage
5. **Audit Logging**: Log all writes

## Performance Considerations

### Service Performance

**Confirmed by Code**: Performance considerations for services:

1. **Caching**: Cache frequently accessed data
2. **Pagination**: Paginate large datasets
3. **Select Fields**: Select only needed fields
4. **Connection Pooling**: Reuse database connections
5. **Async Operations**: Use async/await

## Common Mistakes

### Mistake 1: Not Validating Data

**Symptom**: Invalid data in database

**Cause**: Not validating data

**Fix**:
```typescript
// Add validation
async create(dto: CreateUserDto) {
  const existingUser = await this.prisma.user.findUnique({
    where: { email: dto.email },
  });
  
  if (existingUser) {
    throw new ConflictException('Email already exists');
  }
  
  return this.prisma.user.create({ data: dto });
}
```

### Mistake 2: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Not using transactions for related operations

**Fix**:
```typescript
// Use transaction
await this.prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

### Mistake 3: Not Caching

**Symptom**: Slow API responses

**Cause**: Not caching frequently accessed data

**Fix**:
```typescript
// Add caching
const cached = await this.redis.get(cacheKey);
if (cached) return JSON.parse(cached);

const data = await this.prisma.model.findMany();
await this.redis.setex(cacheKey, 300, JSON.stringify(data));
return data;
```

## Debugging Guide

### Service Debugging

**Issue**: Service not working

**Investigation**:
1. Check service logic
2. Check database query
3. Check cache
4. Check error handling
5. Check logs

**Tools**:
- NestJS debugger
- Service logs
- Database logs
- Redis logs

## Future Enhancements

### Event Emitter

**Status**: Not implemented

**Proposal**: Add event emitter:
- Emit events on data changes
- Listen to events for side effects
- Better decoupling
- Event-driven architecture

### CQRS Pattern

**Status**: Not implemented

**Proposal**: Implement CQRS:
- Separate command and query handlers
- Better performance
- Clear separation of concerns
- Better scalability

## Production Considerations

### Production Services

**Production Deployment**:
- Optimize database queries
- Implement caching
- Use connection pooling
- Monitor service performance
- Monitor error rates

### Service Monitoring

**Monitoring Metrics**:
- Service execution time
- Database query time
- Cache hit rate
- Error rate
- Queue backlog

## Example Requests

### Service Example

**Request**: Call service method

```typescript
const users = await usersService.findAll({ page: 1, limit: 10 });
```

## Example Responses

### Service Response

**Response**: Service response

```json
{
  "data": [
    {
      "id": "user-id",
      "email": "user@example.com"
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 10
  }
}
```

## Sequence Diagrams

### Service Flow

```
Controller → Service → Database
                  ↓
              Cache Check
                  ↓
              Cache Set (if miss)
```

## Architecture Diagrams

### Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Service                                  │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Prisma       │  │   Redis         │  │   Queue        │
│  (Database)   │  │   (Cache)       │  │   (Async)      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What is the role of a service in NestJS?

**Answer**: Service role:
- Implement business logic
- Interact with database
- Interact with external services
- Implement caching
- Handle errors

### Q2: How do you handle database transactions in services?

**Answer**: Transactions via:
- Prisma $transaction method
- Wrap related operations
- Automatic rollback on failure
- Atomicity guaranteed

### Q3: How do you implement caching in services?

**Answer**: Caching via:
- Cache-aside pattern
- Check cache before database
- Set cache after database query
- Invalidate cache on update
- Use Redis for caching

## Exercises

### Exercise 1: Create a Service

**Task**: Create a new service.

**Steps**:
1. Generate service with NestJS CLI
2. Inject dependencies
3. Implement business logic
4. Add error handling
5. Test service

**Verification**:
- Service created
- Dependencies injected
- Logic works
- Testing passes

### Exercise 2: Add Caching to Service

**Task**: Add caching to a service.

**Steps**:
1. Inject RedisService
2. Add cache check
3. Add cache set
4. Add cache invalidation
5. Test caching

**Verification**:
- Caching works
- Cache hit rate improved
- Performance improved

## Real Production Scenarios

### Scenario 1: Slow Service

**Situation**: Service method slow

**Response**:
1. Identify slow operation
2. Add caching
3. Optimize query
4. Add index
5. Monitor performance

### Scenario 2: Data Inconsistency

**Situation**: Data inconsistent after operation

**Response**:
1. Identify operation
2. Add transaction
3. Test transaction
4. Monitor consistency
5. Fix issues

## Navigation

**Next Section**: [05-DTOs](./05-DTOs.md)

**Previous Section**: [03-Controllers](./03-Controllers.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [03-Controllers](./03-Controllers.md) - Controllers
- [05-Database](../05-Database/README.md) - Database details
