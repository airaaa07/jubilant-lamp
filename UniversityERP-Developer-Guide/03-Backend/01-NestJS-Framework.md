# NestJS Framework

## Purpose

This document explains the NestJS framework used in the University ERP backend. It details the framework concepts, architecture, and patterns used throughout the application.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend is built with NestJS 10.x. Understanding NestJS is critical for:
- Developing backend features
- Understanding the module system
- Implementing dependency injection
- Using NestJS features effectively
- Debugging NestJS issues

Without understanding NestJS, developers may struggle to work with the backend codebase.

## Where This Is Used

- **Onboarding**: New developers learn NestJS
- **Feature Development**: Implementing NestJS features
- **Code Reviews**: Understanding NestJS code
- **Debugging**: Debugging NestJS issues
- **Architecture Reviews**: Evaluating NestJS architecture

## Dependencies

### NestJS Dependencies

**Confirmed by Code**: NestJS depends on:

- **Node.js 18+**: JavaScript runtime
- **TypeScript 6.x**: Type-safe JavaScript
- **Reflect-metadata**: Metadata reflection for decorators
- **RxJS**: Reactive programming library
- **Class-validator**: Validation decorators
- **Class-transformer**: Data transformation

## Internal Architecture

### NestJS Architecture

**Confirmed by Code**: NestJS follows a modular architecture.

```
┌─────────────────────────────────────────────────────────┐
│                  NestJS Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Modules      │  │  Controllers   │  │  Providers      │
│  (Organization)│  │  (HTTP Layer)  │  │  (Services)     │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Guards       │  │  Pipes          │  │  Interceptors   │
│  (Authz)      │  │  (Validation)   │  │  (Transform)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Module System

**Confirmed by Code**: NestJS uses a module system for organization.

**Module Definition**:
```typescript
@Module({
  imports: [ConfigModule, PrismaModule],
  controllers: [MyController],
  providers: [MyService],
  exports: [MyService],
})
export class MyModule {}
```

**What This Does**:
- **imports**: Imports other modules to use their exported providers
- **controllers**: Controllers defined in this module
- **providers**: Services and other providers defined in this module
- **exports**: Providers exported for use in other modules

**Module Features**:
- Encapsulation: Modules encapsulate their providers
- Reusability: Modules can be imported by other modules
- Dependency Injection: Modules manage dependency injection
- Lazy Loading: Modules can be lazy loaded

### Controllers

**Confirmed by Code**: Controllers handle HTTP requests.

**Controller Definition**:
```typescript
@Controller('users')
@UseGuards(GlobalJwtAuthGuard)
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
    return this.usersService.update(id, dto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.usersService.remove(id);
  }
}
```

**What This Does**:
- **@Controller**: Defines route prefix
- **@Get**: Defines GET endpoint
- **@Post**: Defines POST endpoint
- **@Patch**: Defines PATCH endpoint
- **@Delete**: Defines DELETE endpoint
- **@Param**: Extracts route parameters
- **@Body**: Extracts request body
- **@UseGuards**: Applies guards to all routes

**Controller Features**:
- Route handling
- Request validation
- Response formatting
- Error handling
- Guard application

### Providers

**Confirmed by Code**: Providers handle business logic.

**Service Definition**:
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

  async findOne(id: string) {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async create(dto: CreateUserDto) {
    return this.prisma.user.create({ data: dto });
  }
}
```

**What This Does**:
- **@Injectable**: Marks class as provider
- **constructor**: Injects dependencies
- **methods**: Implements business logic

**Provider Features**:
- Dependency injection
- Business logic
- Data access
- Caching
- External service integration

### Dependency Injection

**Confirmed by Code**: NestJS uses dependency injection.

**Constructor Injection**:
```typescript
@Injectable()
export class MyService {
  constructor(
    private prisma: PrismaService,
    private redis: RedisService,
  ) {}
}
```

**What This Does**:
- Automatically injects dependencies
- Manages dependency lifecycle
- Enables testing with mocks

**DI Features**:
- Automatic resolution
- Singleton by default
- Custom scopes (REQUEST, TRANSIENT)
- Circular dependency handling

### Guards

**Confirmed by Code**: Guards protect routes.

**Guard Definition**:
```typescript
@Injectable()
export class GlobalJwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(
      'isPublic',
      [context.getHandler(), context.getClass()],
    );

    if (isPublic) {
      return true;
    }

    return super.canActivate(context);
  }
}
```

**What This Does**:
- Extends Passport JWT guard
- Checks for @Public decorator
- Returns true if public route
- Otherwise validates JWT

**Guard Features**:
- Route protection
- Authentication
- Authorization
- Custom logic
- Metadata access

### Pipes

**Confirmed by Code**: Pipes transform and validate data.

**Validation Pipe**:
```typescript
@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodSchema) {}

  transform(value: any) {
    return this.schema.parse(value);
  }
}
```

**What This Does**:
- Validates data against Zod schema
- Throws error if validation fails
- Returns validated data

**Pipe Features**:
- Input validation
- Data transformation
- Type conversion
- Custom validation logic

### Interceptors

**Confirmed by Code**: Interceptors transform requests and responses.

**Logging Interceptor**:
```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const now = Date.now();

    return next.handle().pipe(
      tap(() => {
        const response = context.switchToHttp().getResponse();
        const delay = Date.now() - now;
        console.log(`${request.method} ${request.url} ${response.statusCode} ${delay}ms`);
      }),
    );
  }
}
```

**What This Does**:
- Logs request method and URL
- Logs response status code
- Logs request duration

**Interceptor Features**:
- Request transformation
- Response transformation
- Logging
- Caching
- Error handling

### Decorators

**Confirmed by Code**: Decorators add metadata.

**Custom Decorators**:
```typescript
export const Public = () => SetMetadata('isPublic', true);

export const Scope = (scope: string) => SetMetadata('scope', scope);

export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return data ? request.user?.[data] : request.user;
  },
);
```

**What This Does**:
- **@Public**: Marks route as public (no auth required)
- **@Scope**: Sets required scope for route
- **@CurrentUser**: Extracts current user from request

**Decorator Features**:
- Metadata setting
- Parameter extraction
- Custom logic
- Reusable functionality

## Database Interactions

### Prisma Integration

**Confirmed by Code**: Prisma integrated via PrismaModule.

**PrismaModule**:
```typescript
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

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

## Redis Interactions

### Redis Integration

**Confirmed by Code**: Redis integrated via RedisModule.

**RedisModule**:
```typescript
@Module({
  providers: [RedisService],
  exports: [RedisService],
})
export class RedisModule {}
```

**RedisService**:
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

## Queue Interactions

### Bull Integration

**Confirmed by Code**: Bull queues integrated via BullModule.

**BullModule**:
```typescript
@Module({
  imports: [
    BullModule.forRoot({
      redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT),
      },
    }),
    BullModule.registerQueue({
      name: 'notifications',
    }),
  ],
  controllers: [NotificationController],
  providers: [NotificationService],
})
export class NotificationModule {}
```

## Worker Interactions

### Worker Processing

**Confirmed by Code**: Workers process Bull jobs.

**Processor**:
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

### NestJS Rules

**Confirmed by Code**: NestJS follows these rules:

1. **Modular Architecture**: Each domain in its own module
2. **Dependency Injection**: All dependencies injected
3. **Controller-Service Pattern**: Controllers handle HTTP, Services handle logic
4. **Type Safety**: All code is TypeScript
5. **Validation**: All inputs validated

### Code Organization Rules

**Confirmed by Code**: Code organization follows these rules:

1. **Module Structure**: Each module has controllers, services, DTOs
2. **Naming Conventions**: kebab-case for files, PascalCase for classes
3. **Export Services**: Services exported for use in other modules
4. **Shared Code**: Shared code in infrastructure folder

## Security

### NestJS Security

**Confirmed by Code**: Security measures in NestJS:

1. **Guards**: Route protection
2. **Pipes**: Input validation
3. **Interceptors**: Request/response transformation
4. **Decorators**: Metadata for security
5. **Helmet**: Security headers (if configured)

## Performance Considerations

### NestJS Performance

**Confirmed by Code**: Performance considerations:

1. **Lazy Loading**: Modules can be lazy loaded
2. **Caching**: Interceptors for caching
3. **Async Operations**: All I/O operations async
4. **Connection Pooling**: Database connection pooling
5. **Compression**: Response compression (if configured)

## Common Mistakes

### Mistake 1: Not Exporting Services

**Symptom**: Service not available in other modules

**Cause**: Not exporting service from module

**Fix**:
```typescript
// Wrong
@Module({
  providers: [MyService],
})
export class MyModule {}

// Correct
@Module({
  providers: [MyService],
  exports: [MyService],
})
export class MyModule {}
```

### Mistake 2: Not Using Dependency Injection

**Symptom**: Hard to test code

**Cause**: Not using dependency injection

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

### Mistake 3: Not Using Pipes

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

### NestJS Debugging

**Issue**: NestJS application not working

**Investigation**:
1. Check module imports
2. Check provider registration
3. Check dependency injection
4. Check route registration
5. Check logs

**Tools**:
- NestJS debugger
- VS Code debugger
- Application logs
- NestJS CLI

## Future Enhancements

### GraphQL Integration

**Status**: Not implemented

**Proposal**: Add GraphQL support:
- @nestjs/graphql module
- Schema-first approach
- Type generation
- Better for frontend

### Microservices

**Status**: Not implemented

**Proposal**: Add microservices support:
- @nestjs/microservices
- Event-driven architecture
- Better scalability
- Service discovery

## Production Considerations

### Production NestJS

**Production Deployment**:
- Use production build
- Use process manager (PM2, systemd)
- Enable clustering
- Configure logging
- Configure monitoring
- Configure compression

### NestJS Monitoring

**Monitoring Metrics**:
- Request rate
- Response time
- Error rate
- Module performance
- Dependency health

## Example Requests

### Module Registration

**Request**: Register a new module

**Implementation**:
```typescript
// app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    MyModule, // New module
  ],
})
export class AppModule {}
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
Request → Guard → Pipe → Controller → Service → Database
```

## Architecture Diagrams

### NestJS Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  NestJS Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Modules      │  │  Controllers   │  │  Providers      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What is NestJS and why did you choose it?

**Answer**: NestJS is:
- A progressive Node.js framework
- Built with TypeScript
- Uses dependency injection
- Modular architecture
- Similar to Angular (familiarity)
- Large ecosystem and community

### Q2: How does dependency injection work in NestJS?

**Answer**: DI in NestJS:
- Providers are registered in modules
- Dependencies injected via constructor
- DI container manages lifecycle
- Singleton by default
- Can use custom scopes

### Q3: What are the main building blocks of NestJS?

**Answer**: Main building blocks:
- Modules: Organize application
- Controllers: Handle HTTP requests
- Providers: Business logic
- Guards: Route protection
- Pipes: Validation and transformation
- Interceptors: Request/response transformation

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

### Exercise 2: Create a Custom Guard

**Task**: Create a custom guard.

**Steps**:
1. Create guard class
2. Implement CanActivate interface
3. Add guard logic
4. Apply guard to controller
5. Test guard

**Verification**:
- Guard created
- Guard logic works
- Guard applied correctly
- Access control works

## Real Production Scenarios

### Scenario 1: Circular Dependency

**Situation**: Circular dependency between modules

**Response**:
1. Identify circular dependency
2. Refactor to remove circular dependency
3. Use forwardRef if necessary
4. Test refactored code

### Scenario 2: Slow Module Loading

**Situation**: Application slow to start

**Response**:
1. Identify slow modules
2. Implement lazy loading
3. Optimize module imports
4. Test performance

## Navigation

**Next Section**: [02-Module-System](./02-Module-System.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [05-Database](../05-Database/README.md) - Database details
