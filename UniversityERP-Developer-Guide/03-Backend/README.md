# 03-Backend

## Purpose

This folder provides comprehensive documentation about the backend architecture of the University ERP system. It explains the NestJS framework, module structure, services, controllers, and backend patterns.

## Why This Folder Exists

**Confirmed by Code**: The University ERP backend is built with NestJS and has 36 modules. Understanding the backend architecture is critical for:
- Developing backend features
- Understanding the module system
- Implementing business logic
- Integrating with databases and external services
- Debugging backend issues

Without understanding the backend architecture, developers may struggle to implement features correctly or may introduce bugs.

## Where This Is Used

- **Onboarding**: New developers learn backend architecture
- **Feature Development**: Implementing backend features
- **Code Reviews**: Understanding backend code
- **Debugging**: Debugging backend issues
- **Architecture Reviews**: Evaluating backend architecture

## Dependencies

### Backend Dependencies

**Confirmed by Code**: The backend depends on:

- **NestJS 10.x**: Backend framework
- **TypeScript 6.x**: Type-safe JavaScript
- **Prisma 5.x**: ORM for database access
- **PostgreSQL 16.x**: Relational database
- **Redis 7.x**: In-memory data store
- **Bull 4.x**: Queue for background jobs
- **MinIO SDK**: Object storage client
- **Passport.js**: Authentication
- **JWT**: JSON Web Tokens

## Internal Architecture

### Backend Architecture

**Confirmed by Code**: The backend follows NestJS architecture.

```
┌─────────────────────────────────────────────────────────┐
│                  NestJS Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Controllers   │  │  Services       │  │  Repositories   │
│  (HTTP Layer)  │  │ (Business Logic)│  │  (Data Access)  │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Guards       │  │  Pipes          │  │  Interceptors   │
│  (Authz)      │  │  (Validation)   │  │  (Transform)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Module Structure

**Confirmed by Code**: The backend has 36 modules organized by domain.

```
apps/core-api/src/modules/
├── auth/                  # Authentication
├── master-data/           # Master data management
├── admissions/            # Admissions management
├── academic/              # Academic management
├── attendance/            # Attendance tracking
├── examination/           # Examination system
├── fee/                   # Fee management
├── timetable/             # Timetable management
├── library/               # Library management
├── hostel/                # Hostel management
├── transport/             # Transport management
├── hr/                    # Human resources
├── documents/             # Document management
├── workflow/              # Workflow engine
├── notifications/         # Notifications
├── notice-board/          # Notice board
├── banners/               # Banner management
├── users/                 # User management
├── settings/              # Settings management
├── forms/                 # Dynamic forms
├── analytics/             # Analytics
├── audit/                 # Audit logging
├── counselling/           # Counselling
├── social-monitoring/     # Social media monitoring
├── resource-reservation/  # Resource reservation
└── infrastructure/        # Infrastructure services
```

## Code Walkthrough

### Application Bootstrap

**Confirmed by Code**: The application bootstraps through main.ts.

```typescript
// apps/core-api/src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Enable CORS
  app.enableCors();
  
  // Use global pipes
  app.useGlobalPipes(new ValidationPipe());
  
  // Use global filters
  app.useGlobalFilters(new HttpExceptionFilter());
  
  // Use global guards
  app.useGlobalGuards(new GlobalJwtAuthGuard());
  
  await app.listen(process.env.PORT || 3000);
}
bootstrap();
```

**What This Does**:
- Creates NestJS application
- Enables CORS for cross-origin requests
- Sets up global validation pipe
- Sets up global exception filter
- Sets up global JWT guard
- Starts HTTP server on port 3000

### Module Pattern

**Confirmed by Code**: Modules follow NestJS module pattern.

```typescript
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    RedisModule,
    MinioModule,
  ],
  controllers: [MyController],
  providers: [MyService],
  exports: [MyService],
})
export class MyModule {}
```

**What This Does**:
- Imports required modules
- Defines controllers
- Defines providers
- Exports services for other modules

### Controller Pattern

**Confirmed by Code**: Controllers handle HTTP requests.

```typescript
@Controller('users')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  @Scope('users')
  async findAll(@CurrentUser() user: JwtPayload) {
    return this.usersService.findAll(user);
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }
}
```

**What This Does**:
- Defines route prefix
- Applies guards
- Defines HTTP methods
- Defines route parameters
- Delegates to service

### Service Pattern

**Confirmed by Code**: Services handle business logic.

```typescript
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private redis: RedisService,
  ) {}

  async findAll(user: JwtPayload) {
    // Business logic here
    const cacheKey = `users:${user.universityId}`;
    const cached = await this.redis.get(cacheKey);
    
    if (cached) {
      return JSON.parse(cached);
    }
    
    const users = await this.prisma.user.findMany({
      where: { universityId: user.universityId },
    });
    
    await this.redis.setex(cacheKey, 300, JSON.stringify(users));
    
    return users;
  }
}
```

**What This Does**:
- Injects dependencies
- Implements business logic
- Handles caching
- Interacts with database

## Database Interactions

### Prisma Service

**Confirmed by Code**: PrismaService wraps Prisma Client.

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
- Extends Prisma Client
- Connects on module init
- Disconnects on module destroy

### Database Operations

**Confirmed by Code**: All database operations go through Prisma.

```typescript
// Find one
const user = await prisma.user.findUnique({
  where: { id: userId },
});

// Find many
const users = await prisma.user.findMany({
  where: { role: 'STUDENT' },
});

// Create
const user = await prisma.user.create({
  data: userData,
});

// Update
const user = await prisma.user.update({
  where: { id: userId },
  data: updateData,
});

// Delete
const user = await prisma.user.delete({
  where: { id: userId },
});

// Transaction
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

## Redis Interactions

### Redis Service

**Confirmed by Code**: RedisService wraps ioredis client.

```typescript
@Injectable()
export class RedisService extends Redis implements OnModuleDestroy {
  constructor(configService: ConfigService) {
    super({
      host: configService.get<string>('REDIS_HOST', 'localhost'),
      port: configService.get<number>('REDIS_PORT', 6379),
    });
  }

  async onModuleDestroy() {
    await this.quit();
  }
}
```

**What This Does**:
- Extends ioredis Redis client
- Configures connection from environment variables
- Quits connection on module destroy

### Caching Pattern

**Confirmed by Code**: Services use Redis for caching.

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

## Queue Interactions

### Bull Queue Configuration

**Confirmed by Code**: Bull queues use Redis as backend.

```typescript
import Bull from 'bull';

const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT),
  },
});
```

**What This Does**:
- Creates Bull queue
- Configures Redis as backend
- Enables job processing

### Job Submission

**Confirmed by Code**: Services submit jobs to queues.

```typescript
async sendEmail(data: EmailDto) {
  await this.notificationQueue.add('email', data);
}
```

## Worker Interactions

### Worker Processing

**Confirmed by Code**: Workers process jobs asynchronously.

```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { to, subject, body } = job.data;
    await this.mailService.sendEmail({ to, subject, body });
  }
}
```

## Business Rules

### Backend Rules

**Confirmed by Code**: Backend follows these rules:

1. **Modular Architecture**: Each domain in its own module
2. **Controller-Service Pattern**: Controllers handle HTTP, Services handle logic
3. **Dependency Injection**: All dependencies injected
4. **Type Safety**: All code is TypeScript
5. **Validation**: All inputs validated

### Code Organization Rules

**Confirmed by Code**: Code organization follows these rules:

1. **Module Structure**: Each module has controllers, services, DTOs
2. **Naming Conventions**: kebab-case for files, PascalCase for classes
3. **Export Services**: Services exported for use in other modules
4. **Shared Code**: Shared code in infrastructure folder

## Security

### Backend Security

**Confirmed by Code**: Security measures in backend:

1. **Authentication**: JWT-based authentication
2. **Authorization**: Role-based and scope-based access control
3. **Input Validation**: All inputs validated with Zod
4. **Output Sanitization**: All outputs sanitized
5. **Audit Logging**: All writes audited

## Performance Considerations

### Backend Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Redis caching for frequently accessed data
2. **Connection Pooling**: Prisma connection pooling
3. **Async Operations**: All I/O operations async
4. **Lazy Loading**: Data loaded on demand
5. **Pagination**: Large datasets paginated

## Common Mistakes

### Mistake 1: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Not using Prisma transactions

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

### Mistake 2: Not Caching

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

### Mistake 3: Not Validating Input

**Symptom**: Invalid data in database

**Cause**: Not validating input

**Fix**:
```typescript
// Add validation pipe
@Post()
@UsePipes(new ZodValidationPipe(CreateUserSchema))
async create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

## Debugging Guide

### Backend Debugging

**Issue**: Backend not working as expected

**Investigation**:
1. Check service logs
2. Check database connection
3. Check Redis connection
4. Check environment variables
5. Use debugger

**Tools**:
- NestJS debugger
- VS Code debugger
- Service logs
- Database logs

## Future Enhancements

### GraphQL API

**Status**: Not implemented

**Proposal**: Add GraphQL API:
- Flexible queries
- Reduced over-fetching
- Better for frontend
- Schema-first approach

### Event-Driven Architecture

**Status**: Not implemented

**Proposal**: Implement event-driven architecture:
- Event emitter for domain events
- Event listeners for side effects
- Better decoupling
- Better scalability

## Production Considerations

### Production Backend

**Production Deployment**:
- Use production build
- Use process manager (PM2, systemd)
- Enable clustering
- Configure logging
- Configure monitoring
- Configure alerting

### Backend Monitoring

**Monitoring Metrics**:
- Request rate
- Response time
- Error rate
- Database query time
- Cache hit rate
- Queue backlog

## Example Requests

### API Request Example

**Request**:
```bash
GET /api/users
Authorization: Bearer <token>
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "user-id",
      "email": "user@example.com",
      "role": "STUDENT"
    }
  ]
}
```

## Example Responses

### Service Response

**Response**: Service response

```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com"
  }
}
```

## Sequence Diagrams

### Request Flow

```
Client → HTTP Request → Controller → Service → Prisma → Database
                                          ↓
                                      Redis (cache)
```

## Architecture Diagrams

### Backend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  NestJS Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Controllers   │  │  Services       │  │  Infrastructure │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL   │  │   Redis         │  │   MinIO        │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: Why did you choose NestJS for the backend?

**Answer**: NestJS provides:
- Built-in dependency injection
- Modular architecture
- TypeScript support out of the box
- Easy testing
- Scalable structure
- Large ecosystem

### Q2: How does the module system work in NestJS?

**Answer**: NestJS modules:
- Encapsulate related functionality
- Define controllers, providers, and imports
- Can export providers for other modules
- Enable code organization and reusability

### Q3: How do you handle database operations?

**Answer**: Database operations via:
- Prisma ORM for type-safe database access
- Service layer for business logic
- Transactions for atomic operations
- Connection pooling for performance

## Exercises

### Exercise 1: Create a New Module

**Task**: Create a new NestJS module.

**Steps**:
1. Create module directory
2. Create module file
3. Create controller
4. Create service
5. Create DTOs
6. Register module in AppModule

**Verification**:
- Module created
- Controller works
- Service works
- Module registered

### Exercise 2: Add Caching to Service

**Task**: Add Redis caching to a service.

**Steps**:
1. Inject RedisService
2. Check cache before query
3. Set cache after query
4. Invalidate cache on update
5. Test caching

**Verification**:
- Cache works
- Cache invalidation works
- Performance improved

## Real Production Scenarios

### Scenario 1: Service Not Responding

**Situation**: Service not responding to requests

**Response**:
1. Check service logs
2. Check service status
3. Check database connection
4. Check Redis connection
5. Restart service if needed

### Scenario 2: Database Query Slow

**Situation**: Database query slow

**Response**:
1. Identify slow query
2. Add index if needed
3. Optimize query
4. Add caching
5. Monitor performance

## Navigation

**Next Section**: [01-NestJS-Framework](./01-NestJS-Framework.md)

**Previous Section**: [02-Infrastructure](../02-Infrastructure/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [05-Database](../05-Database/README.md) - Database details
