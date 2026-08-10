# University ERP - Backend Architecture

## Overview

The backend is built with **NestJS 10.x**, a progressive Node.js framework for building efficient, scalable server-side applications. It follows a modular architecture with 36 independent feature modules.

## Technology Stack

### Core Framework
- **NestJS 10.x**: Main framework with dependency injection
- **TypeScript 5.4.x**: Type-safe JavaScript
- **Express**: HTTP server (via @nestjs/platform-express)
- **RxJS 7.x**: Reactive programming

### Database
- **Prisma 5.x**: ORM and query builder
- **PostgreSQL 16**: Primary database
- **Prisma Client**: Type-safe database client

### Authentication & Security
- **Passport 0.6.x**: Authentication middleware
- **@nestjs/passport**: NestJS Passport integration
- **@nestjs/jwt**: JWT token handling
- **bcrypt 5.x**: Password hashing
- **helmet 8.x**: Security headers

### Validation
- **class-validator 0.14.x**: Decorator-based validation
- **class-transformer 0.5.x**: Object transformation
- **zod 3.22.x**: Schema validation

### Caching & Storage
- **ioredis 5.x**: Redis client
- **minio 7.x**: S3-compatible object storage
- **@azure/storage-blob**: Azure Blob storage (fallback)

### Background Jobs
- **@nestjs/bull 10.x**: Bull queue integration
- **bull 4.x**: Redis-based job queue

### Scheduling
- **@nestjs/schedule 4.x**: Cron job scheduling

### API Documentation
- **@nestjs/swagger 7.x**: OpenAPI/Swagger documentation

### Health Monitoring
- **@nestjs/terminus 10.x**: Health checks

### Rate Limiting
- **@nestjs/throttler 6.x**: Request rate limiting

### Email & SMS
- **nodemailer 9.x**: Email sending
- **svg-captcha 1.4.x**: CAPTCHA generation

### Payment Integration
- **razorpay 2.9.x**: Payment gateway

### Secret Management
- **@aws-sdk/client-secrets-manager**: AWS Secrets Manager
- **@azure/keyvault-secrets**: Azure Key Vault
- **@google-cloud/secret-manager**: Google Secret Manager

### QR Code & Barcode
- **qrcode 1.5.x**: QR code generation
- **bwip-js 4.x**: Barcode generation

## Application Bootstrap

### Entry Point: `apps/core-api/src/main.ts`

```typescript
1. Bootstrap vault secrets (if enabled)
2. Create NestJS app with custom body parser (20mb limit)
3. Set global prefix to 'api'
4. Apply Helmet security headers
5. Configure CORS
6. Strip null bytes (PostgreSQL compatibility)
7. Establish request context (async local storage)
8. Setup Swagger docs (non-production only)
9. Listen on configured port (default 3000)
```

### Root Module: `apps/core-api/src/app.module.ts`

The root module imports and configures:

1. **Global Modules**
   - ConfigModule (isGlobal: true)
   - ScheduleModule (for cron jobs)
   - ThrottlerModule (rate limiting: 300 req/min)

2. **Infrastructure Modules**
   - DatabaseModule
   - RedisModule
   - MinioModule
   - HealthModule

3. **Feature Modules** (36 modules)
   - AuthModule
   - MasterDataModule
   - AdmissionsModule
   - ... (33 more modules)

4. **Global Providers**
   - HttpExceptionFilter (APP_FILTER)
   - ThrottlerGuard (APP_GUARD)
   - GlobalJwtAuthGuard (APP_GUARD)

## Module Architecture

### Module Pattern

Each feature module follows this structure:

```
[module-name]/
├── [module-name].module.ts    # Module definition
├── [module-name].controller.ts # API endpoints
├── [module-name].service.ts    # Business logic
├── dto/                       # Data transfer objects
│   ├── [entity].dto.ts       # Request/response DTOs
│   └── [entity].schema.ts     # Zod validation schemas
└── (optional)
    ├── guards/               # Module-specific guards
    ├── decorators/           # Custom decorators
    └── interfaces/           # TypeScript interfaces
```

### Module List (36 Modules)

#### Core Modules
1. **AuthModule** - Authentication, registration, password management
2. **UsersModule** - User management and profiles
3. **RolesModule** - Role and permission management
4. **MasterDataModule** - University/institute/department management

#### Academic Modules
5. **AcademicModule** - Academic operations (attendance, marks, results)
6. **AttendanceModule** - Attendance tracking
7. **ExaminationModule** - Examination management
8. **TimetableModule** - Timetable scheduling
9. **QuestionBankModule** - Question bank management
10. **StudentProfileModule** - Student profile management

#### Administrative Modules
11. **AdmissionsModule** - Admissions management
12. **OnboardingModule** - Student onboarding
13. **FormsModule** - Dynamic form builder
14. **WorkflowModule** - Generic workflow engine
15. **SettingsModule** - System settings
16. **AuditModule** - Audit log viewer

#### Financial Modules
17. **FeeModule** - Fee management
18. **IdFormatModule** - ID format configuration

#### Infrastructure Modules
19. **HostelModule** - Hostel management
20. **TransportModule** - Transport management
21. **LibraryModule** - Library management
22. **ResourceReservationModule** - Resource booking
23. **ResourceOptimisationModule** - Resource optimization

#### HR Modules
24. **HrModule** - HR management
25. **StaffSubjectModule** - Staff-subject mapping
26. **LeaveModule** (part of HR) - Leave management

#### Communication Modules
27. **NotificationsModule** - Notification management
28. **NoticeBoardModule** - Notice board
29. **BannersModule** - Login banners
30. **DirectoryModule** - Staff/student directory
31. **SocialMonitoringModule** - Social media monitoring
32. **CounsellingModule** - Student counselling

#### Document Modules
33. **DocumentsModule** - Document generation
34. **UploadModule** - File upload handling

#### Other Modules
35. **AnalyticsModule** - Analytics and reporting
36. **ParentPortalModule** - Parent portal features
37. **BrandingModule** - University branding

## Controller Architecture

### Controller Responsibilities

Controllers handle HTTP requests and delegate business logic to services:

```typescript
@Controller('api/[module-path]')
@ApiTags('[Module Name]')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, ScopeGuard)
export class [Module]Controller {
  constructor(private readonly [module]Service: [Module]Service) {}

  @Get()
  async findAll(@Query() query: QueryDto, @CurrentUser() user: JwtPayload) {
    return this.[module]Service.findAll(query, user);
  }

  @Get(':id')
  async findOne(@Param('id') id: string, @CurrentUser() user: JwtPayload) {
    return this.[module]Service.findOne(id, user);
  }

  @Post()
  async create(@Body() dto: CreateDto, @CurrentUser() user: JwtPayload) {
    return this.[module]Service.create(dto, user);
  }

  @Patch(':id')
  async update(@Param('id') id: string, @Body() dto: UpdateDto, @CurrentUser() user: JwtPayload) {
    return this.[module]Service.update(id, dto, user);
  }

  @Delete(':id')
  async remove(@Param('id') id: string, @CurrentUser() user: JwtPayload) {
    return this.[module]Service.remove(id, user);
  }
}
```

### Controller Decorators

- **@Controller()**: Defines controller and route prefix
- **@ApiTags()**: Swagger documentation grouping
- **@ApiBearerAuth()**: Requires JWT in Swagger
- **@UseGuards()**: Apply guards (auth, scope, etc.)
- **@Scope()**: Module-level scope requirement
- **@Public()**: Exempt from global auth guard
- **@Throttle()**: Rate limiting override
- **@Get/@Post/@Patch/@Put/@Delete**: HTTP method decorators
- **@Param/@Query/@Body**: Parameter extraction
- **@CurrentUser()**: Custom decorator for authenticated user

## Service Architecture

### Service Responsibilities

Services contain business logic and interact with repositories/external services:

```typescript
@Injectable()
export class [Module]Service {
  constructor(
    private readonly prisma: PrismaService,
    private readonly redis: RedisService,
    private readonly minio: MinioService,
    // Other dependencies
  ) {}

  async findAll(query: QueryDto, user: JwtPayload) {
    // Business logic
    // Database queries via Prisma
    // Caching via Redis
    // External service calls
    return result;
  }

  async create(dto: CreateDto, user: JwtPayload) {
    // Validation
    // Business rules
    // Database transaction
    // Audit logging (automatic via Prisma middleware)
    // Notifications
    return result;
  }
}
```

### Service Patterns

1. **Transaction Management**: Use Prisma transactions for multi-step operations
2. **Error Handling**: Throw NestJS exceptions (BadRequest, NotFound, etc.)
3. **Validation**: Validate inputs before database operations
4. **Authorization**: Check user permissions in service layer
5. **Caching**: Cache frequently accessed data in Redis
6. **Audit**: Automatic via Prisma middleware
7. **Notifications**: Emit events for background processing

## Common Layer Architecture

### Guards (`src/common/guards/`)

#### GlobalJwtAuthGuard
- **Purpose**: Fail-closed JWT authentication
- **Behavior**: Requires valid JWT unless route marked @Public
- **File**: `global-jwt.guard.ts`

#### JwtAuthGuard
- **Purpose**: Always-enforce JWT (ignores @Public)
- **Usage**: For routes that must be authenticated even in @Public controllers
- **File**: `auth/jwt.guard.ts`

#### ScopeGuard
- **Purpose**: Module-level authorization
- **Behavior**: Checks user has required scope
- **File**: `auth/scope.guard.ts`

### Decorators (`src/common/decorators/`)

#### @Public()
- **Purpose**: Exempt route from global JWT guard
- **Usage**: On controller methods that should be publicly accessible
- **File**: `public.decorator.ts`

#### @Scope(scope: string)
- **Purpose**: Require specific module scope
- **Usage**: On controllers or methods
- **File**: `scope.decorator.ts`

#### @CurrentUser()
- **Purpose**: Inject authenticated user payload
- **Usage**: In controller methods
- **File**: `current-user.decorator.ts`

### Pipes (`src/common/pipes/`)

#### ZodValidationPipe
- **Purpose**: Validate request bodies with Zod schemas
- **Usage**: `@Body(new ZodValidationPipe(Schema))`
- **File**: `zod-validation.pipe.ts`

### Filters (`src/common/filters/`)

#### HttpExceptionFilter
- **Purpose**: Global exception handling
- **Behavior**: Normalizes errors, maps Prisma errors to HTTP status
- **File**: `http-exception.filter.ts`

### Middleware (`src/common/middleware/`)

#### Strip Null Bytes
- **Purpose**: Remove NUL bytes from requests
- **Reason**: PostgreSQL rejects NUL bytes
- **File**: `strip-null-bytes.ts`

### Context (`src/common/context/`)

#### Request Context
- **Purpose**: Async local storage for request-scoped data
- **Usage**: Audit middleware uses this to attribute writes to actors
- **File**: `request-context.ts`

## Database Layer Architecture

### PrismaService (`src/database/prisma.service.ts`)

```typescript
@Injectable()
export class PrismaService extends PrismaClient {
  constructor() {
    super({
      datasources: {
        db: {
          url: process.env.DATABASE_URL,
        },
      },
    });
  }

  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

### Audit Middleware (`src/database/audit-middleware.ts`)

- **Purpose**: Automatic field-level audit logging
- **Behavior**: 
  - Records create/update/delete operations
  - Tracks actor (user) who made changes
  - Redacts sensitive fields (passwords, tokens)
  - Ignores noise fields (updatedAt, lastLoginAt)
- **Denylist**: AuditLog, RefreshToken, MobileOtp, etc.
- **Sensitive Fields**: passwordhash, token, secretkey, etc.

### Database Module (`src/database/database.module.ts`)

```typescript
@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class DatabaseModule {}
```

## Infrastructure Layer Architecture

### Redis Module (`src/infrastructure/redis/`)

#### RedisService
- **Purpose**: Redis client wrapper
- **Implementation**: Extends ioredis Redis
- **Configuration**: REDIS_HOST, REDIS_PORT
- **Usage**: Caching, session storage, queue backend

### MinIO Module (`src/infrastructure/minio/`)

#### MinioService
- **Purpose**: Object storage (S3-compatible)
- **Backends**: 
  - MinIO (default for local/docker)
  - Azure Blob (when AZURE_STORAGE_CONNECTION_STRING set)
- **Buckets**: 
  - `university-erp-docs` (documents)
  - `university-erp-exams` (exam artefacts)
- **Methods**: upload, download, delete, getPresignedUrl
- **External Stores**: Configurable S3-compatible endpoints

### Vault Module (`src/infrastructure/vault/`)

#### Vault Bootstrap
- **Purpose**: Fetch secrets from cloud vaults
- **Providers**: 
  - AWS Secrets Manager
  - Azure Key Vault
  - Google Secret Manager
- **Behavior**: No-op when vault disabled

## DTO Architecture

### DTO Pattern

```typescript
// dto/[entity].dto.ts
export class Create[Entity]Dto {
  field1: string;
  field2: number;
  // ...
}

export class Update[Entity]Dto {
  field1?: string;
  field2?: number;
  // ...
}

export class Query[Entity]Dto {
  page?: number;
  limit?: number;
  search?: string;
  // ...
}
```

### Schema Pattern (Zod)

```typescript
// dto/[entity].schema.ts
import { z } from 'zod';

export const Create[Entity]Schema = z.object({
  field1: z.string().min(1),
  field2: z.number().positive(),
  // ...
});

export const Update[Entity]Schema = Create[Entity]Schema.partial();

export const Query[Entity]Schema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(10),
  search: z.string().optional(),
  // ...
});
```

### Validation Usage

```typescript
@Post()
async create(
  @Body(new ZodValidationPipe(CreateEntitySchema)) dto: CreateEntityDto,
  @CurrentUser() user: JwtPayload
) {
  return this.service.create(dto, user);
}
```

## Authentication Flow

### Login Flow

```
1. POST /api/auth/login
   ↓
2. LocalAuthGuard validates credentials
   ↓
3. AuthService.login() generates JWT tokens
   ↓
4. Returns access token (15 min) + refresh token (7 days)
   ↓
5. Client stores tokens
```

### Token Refresh Flow

```
1. POST /api/auth/refresh
   ↓
2. AuthService.refreshToken() validates refresh token
   ↓
3. Generates new access token
   ↓
4. Returns new access token
```

### Protected Request Flow

```
1. Client sends request with Authorization: Bearer <token>
   ↓
2. GlobalJwtAuthGuard validates JWT
   ↓
3. ScopeGuard checks module scope
   ↓
4. @CurrentUser() injects user payload
   ↓
5. Controller processes request
   ↓
6. Service executes business logic
   ↓
7. Prisma middleware logs audit
   ↓
8. Response returned
```

## Error Handling

### Global Exception Filter

The `HttpExceptionFilter` handles:

1. **Prisma Errors**: Maps to appropriate HTTP status codes
   - P2002 (unique constraint) → 409 Conflict
   - P2025 (record not found) → 404 Not Found
   - P2003 (foreign key) → 400 Bad Request

2. **Validation Errors**: 400 Bad Request with details

3. **Authorization Errors**: 401/403 Forbidden

4. **Generic Errors**: 500 Internal Server Error

### Custom Exceptions

Services throw NestJS exceptions:

- `BadRequestException`: Invalid input
- `UnauthorizedException`: Not authenticated
- `ForbiddenException`: Not authorized
- `NotFoundException`: Resource not found
- `ConflictException`: Resource conflict
- `InternalServerErrorException`: Server error

## Rate Limiting

### Global Configuration

- **Default**: 300 requests per minute per IP
- **Sensitive Routes**: Tighter limits via @Throttle
  - Login: 5 per minute
  - OTP send: 3 per minute
  - OTP verify: 10 per minute

### Implementation

```typescript
ThrottlerModule.forRoot([{ ttl: 60000, limit: 300 }])
```

### Per-Route Override

```typescript
@Throttle({ default: { limit: 5, ttl: 60000 } })
@Post('login')
login(@Body() dto: LoginDto) {
  // ...
}
```

## CORS Configuration

```typescript
app.enableCors({
  origin: process.env.APP_URL || 'http://localhost:5173',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
});
```

## Security Headers

### Helmet Configuration

```typescript
app.use(helmet());

// Custom Permissions-Policy
app.use((_req, res, next) => {
  res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=()');
  next();
});
```

## Request Body Size

### Configuration

```typescript
app.use(express.json({ limit: '20mb' }));
app.use(express.urlencoded({ limit: '20mb', extended: true }));
```

### Reason

20mb limit accommodates base64-embedded form documents (marksheets, ID proofs).

## Swagger Documentation

### Configuration

- **Enabled**: Non-production only
- **Route**: `/api/docs`
- **Title**: University ERP API
- **Version**: 1.0
- **Auth**: Bearer token

### Usage

```typescript
if (process.env.NODE_ENV !== 'production') {
  const config = new DocumentBuilder()
    .setTitle('University ERP API')
    .setDescription('Core API for the University ERP System')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);
}
```

## Health Checks

### Health Module

- **Route**: `/health`
- **Checks**: Database, Redis, MinIO
- **Implementation**: @nestjs/terminus

### Custom Health Indicators

```typescript
@Injectable()
export class HealthService {
  async checkDatabase() {
    // Check PostgreSQL connection
  }

  async checkRedis() {
    // Check Redis connection
  }

  async checkMinio() {
    // Check MinIO/Azure Blob connection
  }
}
```

## Scheduled Tasks

### Schedule Module

Uses @nestjs/schedule for cron jobs:

- **Notice Board**: Auto-expire notices
- **Library**: Expire book reservations
- **Cleanup**: Remove stale data

### Implementation

```typescript
@Cron('0 0 * * *') // Daily at midnight
async handleDailyCleanup() {
  // Cleanup logic
}
```

## Background Jobs

### Bull Queues

- **Notification Queue**: Email/SMS sending
- **Certificate Queue**: PDF generation
- **Exam Queue**: Exam processing

### Worker Services

- **notification-worker**: Processes notification jobs
- **cert-generator**: Processes certificate jobs

## Dependency Injection

### Constructor Injection

```typescript
@Injectable()
export class UserService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly redis: RedisService,
    private readonly mailService: MailService,
  ) {}
}
```

### Module Providers

```typescript
@Module({
  providers: [UserService],
  exports: [UserService],
})
```

## Module Communication

### Direct Service Injection

```typescript
@Injectable()
export class AdmissionsService {
  constructor(
    private readonly userService: UserService,
    private readonly feeService: FeeService,
  ) {}
}
```

### Event Emitters

For async communication between modules:

```typescript
@Injectable()
export class NotificationService {
  constructor(private readonly eventEmitter: EventEmitter2) {}

  async sendNotification(data: NotificationDto) {
    this.eventEmitter.emit('notification.send', data);
  }
}
```

## Testing Strategy

### Unit Tests

- **Framework**: Jest
- **Location**: `src/**/__tests__/`
- **Coverage**: Services, guards, pipes

### Integration Tests

- **Framework**: Jest with Supertest
- **Location**: `test/`
- **Coverage**: API endpoints

### Test Configuration

```typescript
// jest.config.js
module.exports = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  rootDir: 'src',
  testRegex: '.*\\.spec\\.ts$',
  transform: {
    '^.+\\.(t|j)s$': 'ts-jest',
  },
};
```

## Performance Optimizations

### Database

1. **Connection Pooling**: Prisma connection limits
2. **Query Optimization**: Select only necessary fields
3. **Indexes**: Strategic indexes on foreign keys
4. **Batch Operations**: Bulk inserts/updates

### Caching

1. **Redis**: Cache frequently accessed data
2. **Query Caching**: Cache expensive queries
3. **Session Caching**: Store session data in Redis

### Code

1. **Lazy Loading**: Load modules on demand
2. **Tree Shaking**: Remove unused code
3. **Minification**: Production builds

## Deployment Considerations

### Environment Variables

Critical variables:
- DATABASE_URL
- REDIS_HOST, REDIS_PORT
- MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
- JWT_SECRET
- UNIVERSITY_ID

### Process Management

- **Development**: NestJS watch mode
- **Production**: PM2 (ecosystem.native.config.js)
- **Docker**: Containerized deployment

### Scaling

- **Horizontal**: Multiple API instances
- **Vertical**: Increase resources
- **Database**: Read replicas (not implemented)
- **Cache**: Redis cluster (not implemented)

## Monitoring

### Logs

- **Application**: NestJS logger
- **Audit**: Database audit trail
- **Errors**: Global exception filter

### Metrics

- **Response Times**: Custom middleware
- **Queue Metrics**: Bull dashboard
- **Database Metrics**: Prisma logs

## Known Limitations

1. **No API Versioning**: Single API version
2. **Limited E2E Tests**: Manual testing required
3. **No GraphQL**: REST API only
4. **No gRPC**: REST API only
5. **Limited Circuit Breaker**: No resilience patterns
