# Data Flow Patterns

## Purpose

This document explains the data flow patterns used in the University ERP system. It details how data moves through the system, from user input to database storage, and from database to user display.

## Why This Document Exists

**Confirmed by Code**: The University ERP has complex data flows involving multiple services, databases, and caches. Understanding data flow patterns is critical for:
- Debugging data-related issues
- Optimizing data access
- Understanding system behavior
- Implementing new features correctly
- Troubleshooting data inconsistencies

Without understanding data flow patterns, developers may introduce data inconsistencies or performance issues.

## Where This Is Used

- **Onboarding**: New developers learn data flows
- **Feature Development**: Implementing data operations
- **Debugging**: Tracing data issues
- **Performance Optimization**: Optimizing data access
- **Data Migration**: Understanding data movement

## Dependencies

### Data Flow Dependencies

**Confirmed by Code**: Data flows depend on:

- **API Layer**: Controllers receive HTTP requests
- **Service Layer**: Services process business logic
- **Repository Layer**: Prisma accesses database
- **Cache Layer**: Redis caches data
- **Queue Layer**: Bull queues process async operations
- **Storage Layer**: MinIO stores files

## Internal Architecture

### Request Data Flow

**Confirmed by Code**: HTTP requests flow through the system.

```
User → React Component → Axios → Nginx → NestJS → Controller → Service → Prisma → PostgreSQL
                                                              ↓
                                                         Redis (cache)
                                                              ↓
                                                         MinIO (storage)
```

### Response Data Flow

**Confirmed by Code**: HTTP responses flow back to the user.

```
PostgreSQL → Prisma → Service → Controller → NestJS → Nginx → Axios → React Component → User
```

### Background Job Data Flow

**Confirmed by Code**: Background jobs flow through queues.

```
Service → Bull Queue → Redis → Worker → Process → Database/MinIO → Result
```

## Code Walkthrough

### Create Operation Flow

**Confirmed by Code**: Create operations follow this flow.

**Example**: Create a new user

```typescript
// 1. User submits form
const formData = { email: 'test@example.com', password: 'password' };

// 2. React component sends request
await axios.post('/api/auth/register', formData);

// 3. Request reaches NestJS
@Controller('auth')
export class AuthController {
  @Post('register')
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }
}

// 4. Service processes business logic
@Injectable()
export class AuthService {
  async register(dto: RegisterDto) {
    // Validate email not exists
    const existing = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });
    if (existing) throw new ConflictException('Email already exists');

    // Hash password
    const hashedPassword = await bcrypt.hash(dto.password, 10);

    // Create user
    const user = await this.prisma.user.create({
      data: {
        email: dto.email,
        passwordHash: hashedPassword,
        role: 'STUDENT',
      },
    });

    // Invalidate cache
    await this.redis.del(`user:${user.id}`);

    return user;
  }
}

// 5. Prisma executes SQL
INSERT INTO "User" (email, passwordHash, role) VALUES ($1, $2, $3)

// 6. PostgreSQL stores data
// Data persisted in database

// 7. Response returns to user
return { success: true, data: user };
```

### Read Operation Flow

**Confirmed by Code**: Read operations follow this flow.

**Example**: Get user profile

```typescript
// 1. User requests data
const { data: user } = useQuery(['user', userId], () => fetchUser(userId));

// 2. React Query checks cache
// If cached, return cached data

// 3. If not cached, send request
await axios.get(`/api/users/${userId}`);

// 4. Request reaches NestJS
@Controller('users')
export class UserController {
  @Get(':id')
  async findOne(@Param('id') id: string, @CurrentUser() user: JwtPayload) {
    return this.userService.findOne(id, user);
  }
}

// 5. Service checks cache
@Injectable()
export class UserService {
  async findOne(id: string, currentUser: JwtPayload) {
    const cacheKey = `user:${id}`;
    const cached = await this.redis.get(cacheKey);

    if (cached) {
      return JSON.parse(cached);
    }

    // Cache miss, query database
    const user = await this.prisma.user.findUnique({
      where: { id },
      include: { institute: true },
    });

    // Cache result
    await this.redis.setex(cacheKey, 300, JSON.stringify(user));

    return user;
  }
}

// 6. Prisma executes SQL
SELECT * FROM "User" WHERE id = $1

// 7. PostgreSQL returns data
// Data retrieved from database

// 8. Service caches result
await this.redis.setex(cacheKey, 300, JSON.stringify(user));

// 9. Response returns to user
return { success: true, data: user };

// 10. React Query caches response
// Future requests use cached data
```

### Update Operation Flow

**Confirmed by Code**: Update operations follow this flow.

**Example**: Update user profile

```typescript
// 1. User submits form
const formData = { name: 'John Doe' };

// 2. React component sends request
await axios.patch(`/api/users/${userId}`, formData);

// 3. Request reaches NestJS
@Controller('users')
export class UserController {
  @Patch(':id')
  async update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
    return this.userService.update(id, dto);
  }
}

// 4. Service processes update
@Injectable()
export class UserService {
  async update(id: string, dto: UpdateUserDto) {
    // Update in database
    const user = await this.prisma.user.update({
      where: { id },
      data: dto,
    });

    // Invalidate cache
    await this.redis.del(`user:${id}`);

    // Send notification (async)
    await this.notificationQueue.add('profile-update', {
      userId: id,
      changes: dto,
    });

    return user;
  }
}

// 5. Prisma executes SQL
UPDATE "User" SET name = $1 WHERE id = $2

// 6. PostgreSQL updates data
// Data updated in database

// 7. Audit middleware logs change
// AuditLog record created

// 8. Cache invalidated
// Cache key deleted

// 9. Job added to queue
// Background job scheduled

// 10. Response returns to user
return { success: true, data: user };
```

### Delete Operation Flow

**Confirmed by Code**: Delete operations follow this flow.

**Example**: Delete user

```typescript
// 1. User confirms delete
await axios.delete(`/api/users/${userId}`);

// 2. Request reaches NestJS
@Controller('users')
export class UserController {
  @Delete(':id')
  async remove(@Param('id') id: string) {
    return this.userService.remove(id);
  }
}

// 3. Service processes delete
@Injectable()
export class UserService {
  async remove(id: string) {
    // Check if user can be deleted
    const user = await this.prisma.user.findUnique({
      where: { id },
      include: { student: true, staff: true },
    });

    if (user.student || user.staff) {
      throw new BadRequestException('Cannot delete user with associated data');
    }

    // Delete user
    await this.prisma.user.delete({
      where: { id },
    });

    // Invalidate cache
    await this.redis.del(`user:${id}`);

    // Delete files from MinIO
    if (user.profilePictureUrl) {
      await this.minioService.delete(user.profilePictureUrl);
    }

    return { success: true };
  }
}

// 4. Prisma executes SQL
DELETE FROM "User" WHERE id = $1

// 5. PostgreSQL deletes data
// Data deleted from database

// 6. Audit middleware logs deletion
// AuditLog record created

// 7. Cache invalidated
// Cache key deleted

// 8. Files deleted from MinIO
// Object storage cleaned up

// 9. Response returns to user
return { success: true };
```

## Database Interactions

### Query Flow

**Confirmed by Code**: Database queries flow through Prisma.

**Flow**:
1. Service calls Prisma method
2. Prisma generates SQL
3. Prisma sends SQL to PostgreSQL
4. PostgreSQL executes SQL
5. PostgreSQL returns results
6. Prisma parses results
7. Prisma returns typed results

### Transaction Flow

**Confirmed by Code**: Transactions ensure atomicity.

**Flow**:
1. Service starts transaction
2. Prisma begins transaction
3. Service executes operations within transaction
4. If all succeed: commit
5. If any fail: rollback
6. Transaction ends

## Redis Interactions

### Cache Flow

**Confirmed by Code**: Cache follows cache-aside pattern.

**Flow**:
1. Service checks Redis cache
2. If cache hit: return cached data
3. If cache miss: query database
4. Store result in Redis with TTL
5. Return data

### Cache Invalidation Flow

**Confirmed by Code**: Cache is invalidated on updates.

**Flow**:
1. Service updates database
2. Service deletes cache key
3. Next request queries database
4. Result cached again

## Queue Interactions

### Job Submission Flow

**Confirmed by Code**: Jobs are submitted to Bull queues.

**Flow**:
1. Service adds job to queue
2. Bull stores job in Redis
3. Job status: waiting
4. Worker polls queue
5. Worker fetches job
6. Job status: active
7. Worker processes job
8. Job status: completed or failed

## Worker Interactions

### Job Processing Flow

**Confirmed by Code**: Workers process jobs asynchronously.

**Flow**:
1. Worker polls queue
2. Worker fetches next job
3. Worker processes job
4. Worker updates job status
5. Worker returns result
6. Worker fetches next job

## Business Rules

### Data Consistency Rules

**Confirmed by Code**: Data consistency is enforced:

1. **Transactions**: Related operations are atomic
2. **Foreign Keys**: Referential integrity enforced
3. **Validation**: Data validated before storage
4. **Audit**: All writes are logged
5. **Cache Invalidation**: Cache invalidated on updates

### Data Isolation Rules

**Confirmed by Code**: Data is isolated by tenant:

1. **Queries**: Filtered by tenant
2. **Cache**: Tenant-specific cache keys
3. **Jobs**: Tenant context included
4. **Audit**: Tenant information logged

## Security

### Data Security

**Confirmed by Code**: Data security is enforced:

1. **Encryption**: Passwords hashed before storage
2. **Validation**: All inputs validated
3. **Sanitization**: Outputs sanitized
4. **Access Control**: Data access controlled
5. **Audit**: All access logged

## Performance Considerations

### Data Flow Performance

**Confirmed by Code**: Performance is optimized:

1. **Caching**: Frequently accessed data cached
2. **Lazy Loading**: Data loaded on demand
3. **Pagination**: Large datasets paginated
4. **Async Processing**: Heavy tasks processed asynchronously
5. **Connection Pooling**: Database connections pooled

## Common Mistakes

### Mistake 1: Not Invalidating Cache

**Symptom**: Stale data returned

**Cause**: Cache not invalidated on update

**Fix**:
```typescript
// Wrong
await prisma.user.update({ where: { id }, data });

// Correct
await prisma.user.update({ where: { id }, data });
await redis.del(`user:${id}`);
```

### Mistake 2: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Related operations not atomic

**Fix**:
```typescript
// Wrong
const user = await prisma.user.create({ data });
const profile = await prisma.userProfile.create({ data });

// Correct
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

### Mistake 3: Not Scoping Data by Tenant

**Symptom**: Cross-tenant data access

**Cause**: Not filtering by tenant

**Fix**:
```typescript
// Wrong
const users = await prisma.user.findMany();

// Correct
const users = await prisma.user.findMany({
  where: { universityId: user.universityId },
});
```

## Debugging Guide

### Data Flow Debugging

**Issue**: Data not flowing correctly

**Investigation**:
1. Check request payload
2. Check controller logs
3. Check service logs
4. Check database query
5. Check cache
6. Check response

**Tools**:
- Request logs
- Service logs
- Database query logs
- Redis logs
- Network logs

## Future Enhancements

### Event-Driven Architecture

**Status**: Not implemented

**Proposal**: Implement event-driven architecture:
- Events for data changes
- Event listeners for side effects
- Better decoupling
- Better scalability

### CQRS Pattern

**Status**: Not implemented

**Proposal**: Implement CQRS pattern:
- Separate read and write models
- Optimized read models
- Better performance
- Clear separation

## Production Considerations

### Data Flow Monitoring

**Production Monitoring**:
- Monitor request latency
- Monitor database query performance
- Monitor cache hit rate
- Monitor queue processing time
- Monitor error rates

### Data Flow Optimization

**Optimization Strategies**:
- Add caching for slow queries
- Optimize database indexes
- Scale workers independently
- Use read replicas for reads
- Implement connection pooling

## Example Requests

### Data Flow Example

**Request**: Create a new student

**Flow**:
1. User submits form
2. Frontend validates form
3. Frontend sends request
4. Backend validates request
5. Backend processes business logic
6. Backend stores in database
7. Backend invalidates cache
8. Backend sends notification
9. Backend returns response
10. Frontend updates UI

## Example Responses

### Data Flow Response

**Response**: Student created successfully

**Data Flow**:
- Database: Student record created
- Cache: Student cache invalidated
- Queue: Notification job added
- Audit: Audit log created
- Response: Success response returned

## Sequence Diagrams

### Create Data Flow

```
User → Form → Validation → API Request → Controller → Service → Prisma → Database
                                                              ↓
                                                         Audit Log
                                                              ↓
                                                         Cache Invalidation
                                                              ↓
                                                         Queue Job
                                                              ↓
                                                         Response
```

### Read Data Flow

```
User → Component → React Query → Cache Check
                                          ↓
                                    Cache Hit → Return
                                          ↓
                                    Cache Miss → API Request → Controller → Service
                                                                              ↓
                                                                        Cache Check
                                                                              ↓
                                                                    Cache Hit → Return
                                                                              ↓
                                                                    Cache Miss → Database
                                                                              ↓
                                                                        Cache Set
                                                                              ↓
                                                                        Response
```

## Architecture Diagrams

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ React Query  │  │   Axios      │  │  Components  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                    Backend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Controllers  │  │   Services   │  │   Guards     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Prisma     │  │   Redis      │  │   Bull       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Storage Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ PostgreSQL   │  │   MinIO      │  │ Elasticsearch │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does data flow from user input to database storage?

**Answer**: Data flows through:
1. User submits form
2. Frontend validates
3. Frontend sends API request
4. Backend validates
5. Controller receives request
6. Service processes business logic
7. Prisma executes SQL
8. PostgreSQL stores data
9. Audit log created
10. Response returned

### Q2: How does caching work in the data flow?

**Answer**: Caching follows cache-aside pattern:
1. Service checks Redis cache
2. If cache hit: return cached data
3. If cache miss: query database
4. Store result in Redis with TTL
5. Return data
6. Invalidate cache on updates

### Q3: How do background jobs fit into the data flow?

**Answer**: Background jobs use producer-consumer pattern:
1. Service adds job to Bull queue
2. Bull stores job in Redis
3. Worker polls queue
4. Worker processes job
5. Worker updates database/storage
6. Worker returns result

## Exercises

### Exercise 1: Trace Data Flow

**Task**: Trace the data flow for a specific operation.

**Steps**:
1. Choose an operation (e.g., create student)
2. Trace from user input to database
3. Document each step
4. Identify cache interactions
5. Identify queue interactions

**Verification**:
- All steps documented
- Cache interactions identified
- Queue interactions identified

### Exercise 2: Optimize Data Flow

**Task**: Optimize data flow for a slow operation.

**Steps**:
1. Identify slow operation
2. Analyze data flow
3. Add caching
4. Optimize queries
5. Test performance

**Verification**:
- Performance improved
- Data flow optimized
- Tests pass

## Real Production Scenarios

### Scenario 1: Data Inconsistency

**Situation**: Data inconsistency between cache and database

**Investigation**:
1. Check cache invalidation logic
2. Check transaction logic
3. Check concurrent updates
4. Check cache TTL

**Resolution**:
- Fix cache invalidation
- Add transactions
- Add optimistic locking

### Scenario 2: Slow Data Access

**Situation**: Slow data access for frequently accessed data

**Investigation**:
1. Check cache hit rate
2. Check query performance
3. Check network latency
4. Check database performance

**Resolution**:
- Add caching
- Optimize queries
- Add indexes
- Use read replicas

## Navigation

**Next Section**: [07-Security-Model](./07-Security-Model.md)

**Previous Section**: [05-Design-Patterns](./05-Design-Patterns.md)

**Related Documentation**:
- [10-Request-Lifecycle](../10-Request-Lifecycle/README.md) - Request lifecycle
- [05-Database](../05-Database/README.md) - Database details
- [12-Redis](../12-Redis/README.md) - Redis details
