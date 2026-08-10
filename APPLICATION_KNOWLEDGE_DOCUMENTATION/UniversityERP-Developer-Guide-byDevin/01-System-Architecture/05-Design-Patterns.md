# Design Patterns

## Purpose

This document explains the design patterns used in the University ERP system. It details the architectural patterns, design patterns, and coding patterns that are consistently used throughout the codebase.

## Why This Document Exists

**Confirmed by Code**: The University ERP follows specific design patterns for consistency and maintainability. Understanding these patterns is critical for:
- Writing consistent code
- Understanding existing code
- Extending the system correctly
- Maintaining code quality
- Onboarding new developers

Without understanding the design patterns, developers may introduce inconsistencies or break established patterns.

## Where This Is Used

- **Onboarding**: New developers learn the patterns
- **Code Reviews**: Ensuring pattern consistency
- **Feature Development**: Following established patterns
- **Refactoring**: Applying patterns consistently
- **Architecture Reviews**: Evaluating pattern usage

## Dependencies

### Pattern Dependencies

**Confirmed by Code**: The design patterns depend on:

- **NestJS Architecture**: Module, Controller, Service pattern
- **TypeScript**: Type patterns, generic patterns
- **Prisma**: Repository pattern, active record pattern
- **React**: Component pattern, hook pattern
- **Bull**: Producer-consumer pattern

## Internal Architecture

### Architectural Patterns

**Confirmed by Code**: The system uses these architectural patterns:

1. **Modular Monolith**: Single application with modules
2. **Layered Architecture**: Controller → Service → Repository
3. **Dependency Injection**: NestJS DI container
4. **Repository Pattern**: Prisma as repository
5. **Producer-Consumer Pattern**: Bull queues
6. **Observer Pattern**: Audit middleware
7. **Strategy Pattern**: Multiple authentication strategies
8. **Decorator Pattern**: Guards, pipes, decorators

### Design Patterns

**Confirmed by Code**: The system uses these design patterns:

1. **Singleton Pattern**: Services are singletons
2. **Factory Pattern**: DTO validation pipes
3. **Builder Pattern**: Query builders
4. **Adapter Pattern**: MinIO adapter for Azure Blob
5. **Template Method Pattern**: Base controller/service
6. **Facade Pattern**: Service facades
7. **Proxy Pattern**: Prisma proxy for audit
8. **Command Pattern**: Workflow commands

## Code Walkthrough

### Module Pattern

**Confirmed by Code**: NestJS modules are the primary organizational pattern.

**Purpose**: Encapsulate related functionality.

**Implementation**:
```typescript
@Module({
  imports: [ConfigModule, PrismaModule],
  controllers: [AuthController],
  providers: [AuthService],
  exports: [AuthService],
})
export class AuthModule {}
```

**Why This Pattern**:
- Encapsulation
- Reusability
- Testability
- Clear boundaries

### Controller-Service Pattern

**Confirmed by Code**: Controllers handle HTTP, Services handle business logic.

**Purpose**: Separation of concerns.

**Implementation**:
```typescript
// Controller
@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('login')
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }
}

// Service
@Injectable()
export class AuthService {
  async login(dto: LoginDto) {
    // Business logic
  }
}
```

**Why This Pattern**:
- Separation of concerns
- Testability
- Reusability
- Clear responsibilities

### Repository Pattern

**Confirmed by Code**: Prisma acts as the repository.

**Purpose**: Abstract database access.

**Implementation**:
```typescript
@Injectable()
export class PrismaService extends PrismaClient {
  async onModuleInit() {
    await this.$connect();
  }
}

@Injectable()
export class UserRepository {
  constructor(private prisma: PrismaService) {}

  async findById(id: string) {
    return this.prisma.user.findUnique({ where: { id } });
  }
}
```

**Why This Pattern**:
- Abstraction
- Testability
- Flexibility
- Consistency

### Dependency Injection Pattern

**Confirmed by Code**: NestJS DI container manages dependencies.

**Purpose**: Manage dependencies and their lifecycles.

**Implementation**:
```typescript
@Injectable()
export class MyService {
  constructor(
    private prisma: PrismaService,
    private redis: RedisService,
    private minio: MinioService,
  ) {}
}
```

**Why This Pattern**:
- Loose coupling
- Testability
- Easy mocking
- Lifecycle management

### Guard Pattern

**Confirmed by Code**: Guards protect routes based on conditions.

**Purpose**: Protect routes with authentication/authorization.

**Implementation**:
```typescript
@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScope = this.reflector.get('scope', context.getHandler());
    if (!requiredScope) return true;

    const request = context.switchToHttp().getRequest();
    return request.user.scope === requiredScope;
  }
}
```

**Why This Pattern**:
- Reusable authorization logic
- Declarative access control
- Easy to test
- Consistent enforcement

### Pipe Pattern

**Confirmed by Code**: Pipes transform or validate data.

**Purpose**: Transform or validate request data.

**Implementation**:
```typescript
@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodSchema) {}

  transform(value: any) {
    return this.schema.parse(value);
  }
}
```

**Why This Pattern**:
- Reusable validation
- Data transformation
- Clean controllers
- Type safety

### Decorator Pattern

**Confirmed by Code**: Decorators add metadata to classes/methods.

**Purpose**: Add metadata for guards, pipes, etc.

**Implementation**:
```typescript
export const Public = () => SetMetadata('isPublic', true);

export const Scope = (scope: string) => SetMetadata('scope', scope);
```

**Why This Pattern**:
- Declarative programming
- Metadata-driven behavior
- Clean code
- Reusable

## Database Interactions

### Active Record Pattern

**Confirmed by Code**: Prisma models act like active records.

**Purpose**: Database models with CRUD methods.

**Implementation**:
```typescript
const user = await prisma.user.create({ data: userData });
user.email = 'new@example.com';
await user.save();
```

**Why This Pattern**:
- Simple CRUD operations
- Type-safe
- Easy to use
- Built-in relationships

### Transaction Pattern

**Confirmed by Code**: Prisma transactions for atomic operations.

**Purpose**: Ensure atomicity of related operations.

**Implementation**:
```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

**Why This Pattern**:
- Data consistency
- Atomicity
- Rollback on failure
- Complex operations

## Redis Interactions

### Cache-Aside Pattern

**Confirmed by Code**: Services use cache-aside pattern.

**Purpose**: Cache frequently accessed data.

**Implementation**:
```typescript
async getUniversity(id: string) {
  const cacheKey = `university:${id}`;
  const cached = await this.redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const university = await this.prisma.university.findUnique({
    where: { id },
  });
  
  await this.redis.setex(cacheKey, 300, JSON.stringify(university));
  
  return university;
}
```

**Why This Pattern**:
- Performance
- Reduced database load
- Consistent caching
- TTL-based expiration

## Queue Interactions

### Producer-Consumer Pattern

**Confirmed by Code**: Bull queues implement producer-consumer.

**Purpose**: Decouple task submission from execution.

**Implementation**:
```typescript
// Producer
await queue.add('email', { to, subject, body });

// Consumer
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { to, subject, body } = job.data;
    await this.mailService.sendEmail({ to, subject, body });
  }
}
```

**Why This Pattern**:
- Decoupling
- Asynchronous processing
- Scalability
- Retry logic

## Worker Interactions

### Worker Pattern

**Confirmed by Code**: Separate worker services process background jobs.

**Purpose**: Offload background processing from main API.

**Implementation**:
```typescript
// Notification Worker
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    // Process email
  }
}

// Certificate Generator
@Processor('certificates')
export class CertificateProcessor {
  @Process('certificate')
  async handleCertificate(job: Job) {
    // Generate certificate
  }
}
```

**Why This Pattern**:
- Performance
- Scalability
- Reliability
- Separation of concerns

## Business Rules

### Pattern Application Rules

**Confirmed by Code**: Patterns are applied consistently:

1. **All modules follow Module pattern**
2. **All controllers follow Controller-Service pattern**
3. **All database access goes through Prisma**
4. **All background jobs use queues**
5. **All validation uses pipes**
6. **All authorization uses guards**

### Pattern Consistency Rules

**Confirmed by Code**: Patterns are consistent across the codebase:

1. **Naming conventions**: Consistent across all files
2. **File structure**: Consistent across all modules
3. **Code organization**: Consistent across all services
4. **Error handling**: Consistent across all modules

## Security

### Security Patterns

**Confirmed by Code**: Security patterns are applied:

1. **Fail-Closed Authentication**: All routes protected by default
2. **Least Privilege**: Users have minimum required access
3. **Input Validation**: All inputs validated
4. **Output Encoding**: All outputs encoded
5. **Audit Logging**: All writes are logged

## Performance Considerations

### Performance Patterns

**Confirmed by Code**: Performance patterns are applied:

1. **Caching**: Frequently accessed data cached
2. **Lazy Loading**: Data loaded on demand
3. **Pagination**: Large datasets paginated
4. **Connection Pooling**: Database connections pooled
5. **Async Processing**: Heavy tasks processed asynchronously

## Common Mistakes

### Mistake 1: Not Following Controller-Service Pattern

**Symptom**: Business logic in controller

**Cause**: Not following established pattern

**Fix**:
```typescript
// Wrong
@Controller('users')
export class UserController {
  @Get()
  async getUsers() {
    // Business logic in controller
    const users = await this.prisma.user.findMany();
    return users.filter(u => u.active);
  }
}

// Correct
@Controller('users')
export class UserController {
  constructor(private userService: UserService) {}

  @Get()
  async getUsers() {
    return this.userService.findAll();
  }
}
```

### Mistake 2: Not Using Dependency Injection

**Symptom**: Hardcoded dependencies

**Cause**: Not using DI pattern

**Fix**:
```typescript
// Wrong
@Injectable()
export class MyService {
  private prisma = new PrismaService();
}

// Correct
@Injectable()
export class MyService {
  constructor(private prisma: PrismaService) {}
}
```

### Mistake 3: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Not using transaction pattern

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

## Debugging Guide

### Pattern-Related Debugging

**Issue**: Pattern not working as expected

**Investigation**:
1. Check pattern implementation
2. Check pattern usage
3. Check dependencies
4. Check configuration

**Tools**:
- NestJS debugger
- Pattern logs
- Service logs

## Future Enhancements

### CQRS Pattern

**Status**: Not implemented

**Proposal**: Implement CQRS pattern:
- Separate command and query handlers
- Better performance for complex operations
- Clear separation of concerns

### Event Sourcing Pattern

**Status**: Not implemented

**Proposal**: Implement event sourcing:
- Event log for all changes
- Event replay for debugging
- Better audit trail

## Production Considerations

### Pattern Performance

**Production Considerations**:
- Monitor pattern performance
- Optimize slow patterns
- Scale based on pattern usage
- Monitor pattern-specific metrics

### Pattern Scalability

**Scalability Considerations**:
- Worker pattern: Scale horizontally
- Cache pattern: Use distributed cache
- Queue pattern: Scale workers independently

## Example Requests

### Pattern Usage Example

**Request**: Create a new module following patterns

**Implementation**:
```typescript
@Module({
  imports: [ConfigModule, PrismaModule],
  controllers: [MyController],
  providers: [MyService],
  exports: [MyService],
})
export class MyModule {}
```

## Example Responses

### Pattern Consistency

**Request**: Check if code follows patterns

**Verification**:
- Module pattern used
- Controller-Service pattern used
- Dependency injection used
- Guards used for authorization
- Pipes used for validation

## Sequence Diagrams

### Request Flow Pattern

```
Request → Guard → Pipe → Controller → Service → Repository → Database
```

### Background Job Pattern

```
Service → Queue → Redis → Worker → Process → Result
```

## Architecture Diagrams

### Pattern Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Layered Architecture                     │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Controllers  │  │    Services     │  │  Repositories   │
│  (HTTP Layer)  │  │ (Business Logic)│  │  (Data Access)  │
└────────────────┘  └────────────────┘  └────────────────┘
```

## Common Interview Questions

### Q1: What design patterns does the system use?

**Answer**: The system uses:
- Module pattern (NestJS)
- Controller-Service pattern
- Repository pattern (Prisma)
- Dependency injection pattern
- Guard pattern (authorization)
- Pipe pattern (validation)
- Decorator pattern (metadata)
- Producer-consumer pattern (queues)

### Q2: Why did you choose the Controller-Service pattern?

**Answer**: Controller-Service pattern provides:
- Separation of concerns
- Testability (mock services)
- Reusability (services used by multiple controllers)
- Clear responsibilities
- Easy to maintain

### Q3: How do you handle background jobs?

**Answer**: Background jobs use the producer-consumer pattern:
- Services add jobs to Bull queues
- Workers consume jobs from queues
- Redis acts as queue backend
- Retry logic built-in
- Dead letter queue for failed jobs

## Exercises

### Exercise 1: Implement a New Pattern

**Task**: Implement a new service following established patterns.

**Steps**:
1. Create module
2. Create controller
3. Create service
4. Add guards/pipes
5. Test pattern

**Verification**:
- Pattern followed correctly
- Code is consistent
- Tests pass

### Exercise 2: Refactor to Use Pattern

**Task**: Refactor code to use established pattern.

**Steps**:
1. Identify code not following pattern
2. Refactor to follow pattern
3. Test refactored code
4. Verify consistency

**Verification**:
- Pattern applied correctly
- Code is consistent
- Tests pass

## Real Production Scenarios

### Scenario 1: Adding New Module

**Situation**: Need to add a new module

**Steps**:
1. Create module following Module pattern
2. Create controller following Controller-Service pattern
3. Create service following Service pattern
4. Add guards/pipes following Guard/Pipe pattern
5. Test module
6. Deploy module

### Scenario 2: Refactoring for Performance

**Situation**: Need to refactor for performance

**Steps**:
1. Identify performance bottleneck
2. Apply caching pattern
3. Apply lazy loading pattern
4. Test refactored code
5. Measure performance improvement
6. Deploy refactored code

## Navigation

**Next Section**: [06-Data-Flow-Patterns](./06-Data-Flow-Patterns.md)

**Previous Section**: [04-Multi-Tenancy-Model](./04-Multi-Tenancy-Model.md)

**Related Documentation**:
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [10-Request-Lifecycle](../10-Request-Lifecycle/README.md) - Request lifecycle
