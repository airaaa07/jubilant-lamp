# 01-System-Architecture

## Purpose

This folder provides comprehensive documentation about the University ERP system architecture. It explains the high-level design, technology choices, architectural patterns, and the reasoning behind key decisions.

## Why This Folder Exists

**Confirmed by Code**: The University ERP is a complex monorepo with multiple services, databases, and infrastructure components. Understanding the architecture is critical for:
- Making informed technical decisions
- Debugging system-wide issues
- Extending the system correctly
- Optimizing performance
- Planning for scalability

Without understanding the architecture, developers may make decisions that conflict with the system design.

## Where This Is Used

- **Onboarding**: New developers learn the system architecture
- **Architecture Reviews**: Evaluating proposed changes
- **Technical Planning**: Planning new features
- **Debugging**: Understanding system-wide issues
- **Performance Optimization**: Identifying bottlenecks
- **Scaling Planning**: Planning for growth

## Dependencies

### System Dependencies

**Confirmed by Code**:
- **Monorepo Structure**: npm workspaces
- **Backend Framework**: NestJS 10.x
- **Frontend Framework**: React 19 + Vite
- **Database**: PostgreSQL 16 + Prisma 5.x
- **Cache**: Redis 7.x
- **Object Storage**: MinIO 7.x / Azure Blob
- **Search**: Elasticsearch 8.13.0 (configured but not deeply integrated)
- **Queue**: Bull 4.x
- **Containerization**: Docker + Docker Compose

### Architecture Dependencies

**Confirmed by Code**:
- **Multi-Tenancy**: University → Institute → Department hierarchy
- **Modular Architecture**: 36 NestJS modules
- **Microservices**: 4 services (Core API, CBE Engine, Notification Worker, Certificate Generator)
- **Event-Driven**: Background jobs via queues
- **REST API**: RESTful API design
- **WebSocket**: Real-time communication (CBE Engine)

## Internal Architecture

### High-Level Architecture

**Confirmed by Code**: The system follows a monolithic modular architecture with separate worker services.

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                  │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Admin Portal  │  │    Core API     │  │   CBE Engine    │
│  (React/Vite)  │  │   (NestJS)      │  │  (NestJS/WS)    │
│   Port 5173    │  │    Port 3000    │  │    Port 3001    │
└────────────────┘  └────────┬────────┘  └────────┬────────┘
                           │                     │
        ┌───────────────────┼───────────────────┐ │
        │                   │                   │ │
┌───────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│ Notification   │ │ Cert Gen    │ │                 │
│   Worker       │ │              │ │                 │
│   Port 3002    │ │ Port 3003   │ │                 │
└────────────────┘ └──────────────┘ │                 │
                                     │                 │
        ┌────────────────────────────┼─────────────────┘
        │
        ↓
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Services                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │PostgreSQL│ │  Redis   │ │  MinIO   │ │Elasticsearch│ │
│  │ Port 5432│ │ Port 6379│ │ Port 9000│ │ Port 9200│  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Monorepo Structure

**Confirmed by Code**: The project uses npm workspaces for monorepo management.

```
UniversityERP/
├── apps/
│   ├── core-api/           # Main NestJS backend
│   ├── cbe-engine/         # Computer-Based Exam engine
│   ├── notification-worker/ # Background notification worker
│   └── cert-generator/     # Certificate generation worker
├── web/
│   └── admin-portal/      # React admin portal
├── libs/                  # Shared libraries (empty currently)
├── docker-compose.yml     # Docker services
├── package.json           # Root package.json
└── turbo.json             # Turborepo configuration
```

### Module Architecture

**Confirmed by Code**: The Core API has 36 modules organized by domain.

```
apps/core-api/src/modules/
├── auth/                  # Authentication
├── master-data/           # Master data management
│   ├── controllers/
│   │   ├── university.controller.ts
│   │   ├── institute.controller.ts
│   │   └── department.controller.ts
│   └── services/
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
    ├── redis/
    ├── minio/
    └── elasticsearch/
```

## Code Walkthrough

### Application Bootstrap

**Confirmed by Code**: The NestJS application bootstraps through `main.ts`.

```typescript
// apps/core-api/src/main.ts
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
1. Creates NestJS application
2. Enables CORS for cross-origin requests
3. Sets up global validation pipe
4. Sets up global exception filter
5. Sets up global JWT guard
6. Starts HTTP server

### Module Import Pattern

**Confirmed by Code**: Modules follow a consistent import pattern.

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

**Pattern**:
- Import ConfigModule globally
- Import infrastructure modules
- Define controllers
- Define services
- Export services for other modules

## Database Interactions

### Prisma Service

**Confirmed by Code**: All database operations go through PrismaService.

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

**Usage**:
```typescript
@Injectable()
export class MyService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.user.findMany();
  }
}
```

### Audit Middleware

**Confirmed by Code**: Prisma middleware intercepts write operations for audit logging.

```typescript
// apps/core-api/src/database/audit-middleware.ts
prisma.$use(async (params, next) => {
  const before = await findBefore(params);
  const result = await next(params);
  const after = await findAfter(params);
  
  await createAuditLog(params, before, after);
  
  return result;
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

### Caching Pattern

**Confirmed by Code**: Services use Redis for caching frequently accessed data.

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

### Job Submission

**Confirmed by Code**: Services submit jobs to queues.

```typescript
async sendEmail(data: EmailDto) {
  await this.notificationQueue.add('email', data);
}
```

## Worker Interactions

### Notification Worker

**Confirmed by Code**: Notification worker processes email and SMS jobs.

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

### Certificate Generator

**Confirmed by Code**: Certificate generator processes PDF generation jobs.

```typescript
@Processor('certificates')
export class CertificateProcessor {
  @Process('certificate')
  async handleCertificate(job: Job) {
    const { templateId, studentId } = job.data;
    const pdf = await this.generateCertificate(templateId, studentId);
    await this.minioService.upload(`certificates/${studentId}.pdf`, pdf);
  }
}
```

## Business Rules

### Multi-Tenancy

**Confirmed by Code**: The system supports multi-tenancy with hierarchy.

**Hierarchy**: University → Institute → Department

**Rule**: All data is scoped to the user's university and institute.

**Implementation**:
```typescript
@Scope('university')
@Controller('universities')
export class UniversityController {
  @Get()
  async findAll(@CurrentUser() user: JwtPayload) {
    // Only return universities user has access to
    return this.universityService.findAll(user.universityId);
  }
}
```

### Fail-Closed Authentication

**Confirmed by Code**: All routes are protected by default.

**Rule**: All routes require authentication unless explicitly marked as public.

**Implementation**:
```typescript
@Injectable()
export class GlobalJwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(
      'isPublic',
      [context.getHandler(), context.getClass()]
    );

    if (isPublic) {
      return true;
    }

    return super.canActivate(context);
  }
}
```

### Audit Logging

**Confirmed by Code**: All write operations are audited.

**Rule**: Every create, update, delete operation is logged with actor, timestamp, and changes.

**Implementation**:
```typescript
prisma.$use(async (params, next) => {
  const result = await next(params);
  
  await prisma.auditLog.create({
    data: {
      actorId: getCurrentUser().id,
      actionType: params.action,
      entityType: params.model,
      oldValue: before,
      newValue: after,
    },
  });
  
  return result;
});
```

## Security

### Authentication

**Confirmed by Code**: JWT-based authentication with refresh tokens.

**Flow**:
1. User logs in with email/password
2. Server validates credentials
3. Server generates access token (15 min) and refresh token (7 days)
4. Client stores tokens
5. Client sends access token in Authorization header
6. Server validates token on each request
7. Client uses refresh token to get new access token

### Authorization

**Confirmed by Code**: Role-based and scope-based authorization.

**Roles**: SUPERADMIN, ADMIN, STAFF, STUDENT

**Scopes**: Module-level access (e.g., 'university', 'admissions')

**Implementation**:
```typescript
@Scope('university')
@Controller('universities')
export class UniversityController {
  // Only users with 'university' scope or SUPERADMIN role can access
}
```

### Rate Limiting

**Confirmed by Code**: NestJS throttler for rate limiting.

**Limits**:
- Login: 5 attempts per minute
- OTP Send: 3 attempts per minute
- OTP Verify: 10 attempts per minute

**Implementation**:
```typescript
@Throttle({ default: { limit: 5, ttl: 60000 } })
@Post('login')
login(@Request() req) {
  return this.authService.login(req.user);
}
```

## Performance Considerations

### Database Performance

**Confirmed by Code**: Prisma with connection pooling.

**Optimizations**:
- Connection pooling (automatic)
- Indexes on frequently queried columns
- Select only needed fields
- Use pagination

### Caching Strategy

**Confirmed by Code**: Redis caching for frequently accessed data.

**Cache Keys**:
- `university:{id}` - University data
- `institute:{id}` - Institute data
- `user:{id}` - User profile
- `refresh:{userId}` - Refresh tokens

**TTL**: 5 minutes for most data, 7 days for refresh tokens

### Frontend Performance

**Confirmed by Code**: React lazy loading and code splitting.

**Optimizations**:
- Lazy loading of pages
- Code splitting by route
- Image optimization
- Bundle size optimization

## Common Mistakes

### Mistake 1: Not Scoping Data by Tenant

**Symptom**: Users see data from other universities

**Cause**: Not filtering by universityId/instituteId

**Fix**:
```typescript
// Wrong
const users = await prisma.user.findMany();

// Correct
const users = await prisma.user.findMany({
  where: { universityId: user.universityId },
});
```

### Mistake 2: Not Caching Frequently Accessed Data

**Symptom**: Slow API responses

**Cause**: Querying database for every request

**Fix**:
```typescript
// Add caching
const cached = await this.redis.get(cacheKey);
if (cached) return JSON.parse(cached);

const data = await this.prisma.model.findMany();
await this.redis.setex(cacheKey, 300, JSON.stringify(data));
```

### Mistake 3: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Related operations not atomic

**Fix**:
```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

## Debugging Guide

### Architecture-Level Debugging

**Issue**: System-wide performance degradation

**Investigation**:
1. Check Docker resource usage: `docker stats`
2. Check database performance: `docker-compose exec postgres pg_isready`
3. Check Redis performance: `docker-compose exec redis redis-cli ping`
4. Check application logs
5. Check API response times

**Tools**:
- Docker stats
- PostgreSQL EXPLAIN ANALYZE
- Redis INFO command
- Application logs
- APM tools (if configured)

### Module-Level Debugging

**Issue**: Specific module not working

**Investigation**:
1. Check module imports
2. Check service dependencies
3. Check database connections
4. Check Redis connections
5. Check module logs

**Tools**:
- NestJS debugger
- Module-specific logs
- Service tests

## Future Enhancements

### Microservices Migration

**Status**: Not implemented

**Proposal**: Migrate to full microservices architecture:
- Separate services for each domain
- API Gateway for routing
- Service mesh for communication
- Event-driven architecture

### GraphQL API

**Status**: Not implemented

**Proposal**: Add GraphQL API alongside REST:
- Flexible queries
- Reduced over-fetching
- Better for frontend

### Event Sourcing

**Status**: Not implemented

**Proposal**: Implement event sourcing:
- Event log for all changes
- Event replay for debugging
- Better audit trail

## Production Considerations

### High Availability

**Recommendations**:
- Load balancer for API servers
- Database replication
- Redis clustering
- MinIO gateway configuration
- Multiple worker instances

### Disaster Recovery

**Recommendations**:
- Automated backups
- Point-in-time recovery
- Multi-region deployment
- Failover procedures
- Regular recovery testing

### Monitoring

**Recommendations**:
- APM monitoring (New Relic, Datadog)
- Log aggregation (ELK stack)
- Metrics collection (Prometheus)
- Alerting (PagerDuty)
- Uptime monitoring

## Example Requests

### System Health Check

**Request**:
```bash
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "database": "connected",
  "redis": "connected",
  "minio": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Status**: Inferred - health check endpoint not visible in code

## Example Responses

### System Information

**Request**:
```bash
GET /api/system/info
```

**Response**:
```json
{
  "version": "1.0.0",
  "environment": "development",
  "modules": [
    "auth",
    "master-data",
    "admissions",
    "academic",
    "attendance",
    "examination",
    "fee",
    "timetable",
    "library",
    "hostel",
    "transport",
    "hr",
    "documents",
    "workflow",
    "notifications",
    "notice-board",
    "banners",
    "users",
    "settings",
    "forms",
    "analytics",
    "audit",
    "counselling",
    "social-monitoring",
    "resource-reservation"
  ],
  "services": [
    "core-api",
    "cbe-engine",
    "notification-worker",
    "cert-generator"
  ]
}
```

**Status**: Inferred - system info endpoint not visible in code

## Sequence Diagrams

### Request Flow

```
User → React Component → Axios → Nginx → NestJS → Controller → Service → Prisma → PostgreSQL
                                                              ↓
                                                         Redis (cache)
                                                              ↓
                                                         MinIO (storage)
```

### Authentication Flow

```
User → Login Form → API → LocalAuthGuard → AuthService → Prisma → PostgreSQL
                                          ↓
                                     JWT Generation
                                          ↓
                                     Token Response
```

## Architecture Diagrams

### Multi-Tenancy Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   University ERP System                    │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  University A   │  │  University B   │  │  University C   │
└────────────────┘  └────────────────┘  └────────────────┘
         │                     │                     │
    ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
    ↓         ↓           ↓         ↓           ↓         ↓
┌──────┐ ┌──────┐     ┌──────┐ ┌──────┐     ┌──────┐ ┌──────┐
│Inst 1│ │Inst 2│     │Inst 1│ │Inst 2│     │Inst 1│ │Inst 2│
└──────┘ └──────┘     └──────┘ └──────┘     └──────┘ └──────┘
```

## Common Interview Questions

### Q1: Why did you choose NestJS for the backend?

**Answer**: NestJS provides:
- Built-in dependency injection
- Modular architecture
- TypeScript support out of the box
- Excellent documentation
- Easy testing
- Scalable architecture
- Large ecosystem

### Q2: Why did you choose a monolithic modular architecture instead of microservices?

**Answer**: Monolithic modular architecture provides:
- Simpler development and deployment
- Easier debugging and testing
- Lower operational overhead
- Better performance for small to medium scale
- Can be split into microservices later if needed

### Q3: How does the multi-tenancy model work?

**Answer**: The system uses a hierarchical multi-tenancy model:
- University is the top-level tenant
- Institute belongs to University
- Department belongs to Institute
- All data is scoped to user's university and institute
- Scope guards enforce access control

### Q4: How do you handle background jobs?

**Answer**: Background jobs are handled via:
- Bull queues with Redis backend
- Separate worker services
- Job prioritization
- Retry logic with exponential backoff
- Dead letter queue for failed jobs

### Q5: How do you ensure data consistency?

**Answer**: Data consistency is ensured via:
- Prisma transactions for related operations
- Audit logging for all write operations
- Foreign key constraints in database
- Validation at DTO level
- Business rules in services

## Exercises

### Exercise 1: Draw System Architecture

**Task**: Draw the complete system architecture diagram including all services, databases, and their relationships.

**Verification**:
- Include all 4 services
- Include all infrastructure services
- Show data flow
- Show communication patterns

### Exercise 2: Explain Multi-Tenancy

**Task**: Explain how the multi-tenancy model works and how it's enforced.

**Verification**:
- Explain the hierarchy
- Explain data scoping
- Explain enforcement mechanism
- Provide examples

### Exercise 3: Design a New Module

**Task**: Design a new module for a feature (e.g., alumni management).

**Verification**:
- Define module structure
- Define database schema
- Define API endpoints
- Define business rules
- Consider multi-tenancy

## Real Production Scenarios

### Scenario 1: System Outage

**Situation**: Core API service goes down

**Impact**:
- Admin portal inaccessible
- All API requests fail
- Background jobs continue (separate services)

**Recovery**:
1. Check service logs
2. Restart service
3. Verify database connection
4. Verify Redis connection
5. Monitor for recurrence

### Scenario 2: Database Performance Degradation

**Situation**: Database queries become slow

**Impact**:
- API response times increase
- User experience degrades
- Timeouts may occur

**Recovery**:
1. Identify slow queries
2. Add indexes
3. Optimize queries
4. Add caching
5. Scale database

### Scenario 3: Redis Failure

**Situation**: Redis service goes down

**Impact**:
- Caching fails
- Session management fails
- Queue processing stops

**Recovery**:
1. Restart Redis
2. Restore from backup
3. Rebuild cache
4. Restart workers

## Navigation

**Next Section**: [02-Repository-Structure](./02-Repository-Structure.md)

**Previous Section**: [00-Getting-Started](../00-Getting-Started/README.md)

**Related Documentation**:
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [05-Database](../05-Database/README.md) - Database details
