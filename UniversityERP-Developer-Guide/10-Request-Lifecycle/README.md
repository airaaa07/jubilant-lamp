# 10-Request Lifecycle

## Purpose

This folder provides comprehensive documentation about the request lifecycle in the University ERP system. It details how requests flow through the system, from the initial request to the final response.

## Why This Folder Exists

**Confirmed by Code**: Understanding the request lifecycle is critical for:
- Debugging request issues
- Understanding system architecture
- Implementing middleware and interceptors
- Optimizing request performance
- Adding cross-cutting concerns

Without understanding the request lifecycle, developers may struggle with debugging or may introduce bugs.

## Where This Is Used

- **Onboarding**: New developers learn request lifecycle
- **Feature Development**: Implementing request handling
- **Code Reviews**: Reviewing request handling code
- **Debugging**: Debugging request issues
- **Performance**: Optimizing request performance

## Dependencies

### Request Lifecycle Dependencies

**Confirmed by Code**: Request lifecycle depends on:

- **NestJS**: Framework for request handling
- **Express**: Underlying HTTP server
- **Middleware**: Request preprocessing
- **Guards**: Request authentication/authorization
- **Interceptors**: Request/response transformation
- **Pipes**: Request validation
- **Exception Filters**: Error handling

## Internal Architecture

### Request Lifecycle Architecture

**Confirmed by Code**: Request lifecycle follows NestJS middleware pipeline.

```
┌─────────────────────────────────────────────────────────┐
│              Request Lifecycle                             │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Middleware   │  │  Guards         │  │  Interceptors   │
│  (Pre-Process)│  │  (Auth/Authz)   │  │  (Transform)    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Pipes        │  │  Controller     │  │  Service        │
│  (Validation) │  │  (Route Handler) │  │  (Business Logic)│
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Exception    │  │  Interceptors   │  │  Response      │
│  Filters      │  │  (Post-Process) │  │  (Final)        │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Middleware Pipeline

**Confirmed by Code**: Middleware executes before guards.

**Global Middleware**:
```typescript
export function loggerMiddleware(req: Request, res: Response, next: NextFunction) {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
}

export function corsMiddleware(req: Request, res: Response, next: NextFunction) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  next();
}
```

**What This Does**:
- **loggerMiddleware**: Logs request method and URL
- **corsMiddleware**: Adds CORS headers
- **next()**: Passes control to next middleware

### Guards

**Confirmed by Code**: Guards execute after middleware.

**GlobalJwtAuthGuard**:
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
- **@Public Decorator**: Checks for public routes
- **Bypass**: Bypasses JWT validation for public routes
- **Default**: Validates JWT for all other routes

**ScopeGuard**:
```typescript
@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScope = this.reflector.get('scope', context.getHandler());
    
    if (!requiredScope) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (user.role === 'SUPERADMIN') {
      return true;
    }

    return user.scope === requiredScope;
  }
}
```

**What This Does**:
- **@Scope Decorator**: Checks for @Scope decorator
- **SUPERADMIN**: SUPERADMIN has access to all scopes
- **Scope Check**: Checks if user has required scope

### Interceptors

**Confirmed by Code**: Interceptors execute before and after controller.

**LoggingInterceptor**:
```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const now = Date.now();

    return next.handle().pipe(
      tap(() => {
        const response = context.switchToHttp().getResponse();
        console.log(`${request.method} ${request.url} - ${response.statusCode} - ${Date.now() - now}ms`);
      }),
    );
  }
}
```

**What This Does**:
- **Pre-Request**: Records start time
- **Post-Request**: Logs request duration
- **Response Status**: Logs response status code

**TransformInterceptor**:
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, ResponseDto<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<ResponseDto<T>> {
    return next.handle().pipe(
      map(data => ({
        success: true,
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}
```

**What This Does**:
- **Transform**: Wraps response in standard format
- **Success Flag**: Adds success flag
- **Timestamp**: Adds timestamp

### Pipes

**Confirmed by Code**: Pipes execute before controller.

**ZodValidationPipe**:
```typescript
@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: z.ZodSchema) {}

  transform(value: any) {
    try {
      return this.schema.parse(value);
    } catch (error) {
      throw new BadRequestException('Validation failed');
    }
  }
}
```

**What This Does**:
- **Validate**: Validates input against Zod schema
- **Error**: Throws BadRequestException on validation failure
- **Transform**: Returns validated data

### Controller

**Confirmed by Code**: Controller executes after pipes.

**Controller Example**:
```typescript
@Controller('users')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  @Scope('users')
  findAll() {
    return this.usersService.findAll();
  }

  @Post()
  @Scope('users')
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}
```

**What This Does**:
- **findAll**: Returns all users
- **create**: Creates new user
- **Guards**: Applied at controller level
- **Scope**: Applied at method level

### Service

**Confirmed by Code**: Service executes after controller.

**Service Example**:
```typescript
@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.user.findMany();
  }

  async create(dto: CreateUserDto) {
    return this.prisma.user.create({ data: dto });
  }
}
```

**What This Does**:
- **findAll**: Queries database for all users
- **create**: Creates user in database
- **Prisma**: Uses Prisma for database operations

### Exception Filters

**Confirmed by Code**: Exception filters handle errors.

**HttpExceptionFilter**:
```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();

    response.status(status).json({
      success: false,
      error: {
        code: status,
        message: exception.message,
      },
      timestamp: new Date().toISOString(),
    });
  }
}
```

**What This Does**:
- **Catch**: Catches HTTP exceptions
- **Transform**: Transforms error to standard format
- **Response**: Returns error response

## Database Interactions

### Request-Database Flow

**Confirmed by Code**: Database interactions happen in service layer.

**Flow**:
```
Request → Controller → Service → Prisma → Database
```

## Redis Interactions

### Request-Redis Flow

**Confirmed by Code**: Redis can be used for caching.

**Flow**:
```
Request → Service → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Request-Queue Flow

**Confirmed by Code**: Queues used for async operations.

**Flow**:
```
Request → Service → Queue → Worker
```

## Worker Interactions

### Request-Worker Flow

**Confirmed by Code**: Workers process queued tasks.

**Flow**:
```
Worker → Process Task → Database → External Service
```

## Business Rules

### Request Lifecycle Rules

**Confirmed by Code**: Request lifecycle follows these rules:

1. **Middleware First**: Middleware executes first
2. **Guards Second**: Guards execute after middleware
3. **Interceptors Third**: Interceptors execute before/after controller
4. **Pipes Fourth**: Pipes execute before controller
5. **Controller Fifth**: Controller executes after pipes
6. **Service Sixth**: Service executes after controller
7. **Exception Filters**: Exception filters handle errors

### Error Handling Rules

**Confirmed by Code**: Error handling follows these rules:

1. **Validation Errors**: BadRequestException
2. **Authentication Errors**: UnauthorizedException
3. **Authorization Errors**: ForbiddenException
4. **Not Found Errors**: NotFoundException
5. **Server Errors**: InternalServerErrorException

## Security

### Request Lifecycle Security

**Confirmed by Code**: Security considerations for request lifecycle:

1. **Middleware**: CORS, rate limiting
2. **Guards**: Authentication, authorization
3. **Pipes**: Input validation
4. **Interceptors**: Logging, transformation
5. **Exception Filters**: Error handling

## Performance Considerations

### Request Lifecycle Performance

**Confirmed by Code**: Performance considerations:

1. **Middleware**: Keep middleware fast
2. **Guards**: Optimize guard logic
3. **Interceptors**: Minimize interceptor overhead
4. **Pipes**: Optimize validation
5. **Caching**: Cache frequently accessed data

## Common Mistakes

### Mistake 1: Not Using Guards

**Symptom**: Unprotected routes

**Cause**: Not using guards

**Fix**:
```typescript
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
```

### Mistake 2: Not Validating Input

**Symptom**: Invalid data in database

**Cause**: Not using validation pipes

**Fix**:
```typescript
@Body(new ZodValidationPipe(CreateUserDto))
```

### Mistake 3: Not Handling Errors

**Symptom**: Unhandled errors

**Cause**: Not using exception filters

**Fix**:
```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {}
```

## Debugging Guide

### Request Lifecycle Debugging

**Issue**: Request not working

**Investigation**:
1. Check middleware
2. Check guards
3. Check interceptors
4. Check pipes
5. Check controller

**Tools**:
- Request logs
- Middleware logs
- Guard logs
- Service logs

## Future Enhancements

### Request Tracing

**Status**: Not implemented

**Proposal**: Implement request tracing:
- Distributed tracing
- Request ID propagation
- Performance monitoring
- Better debugging
- More complex

### Rate Limiting

**Status**: Partially implemented

**Proposal**: Implement comprehensive rate limiting:
- Per-user rate limiting
- Per-endpoint rate limiting
- Adaptive rate limiting
- Better protection
- More complex

## Production Considerations

### Production Request Lifecycle

**Production Deployment**:
- Enable all middleware
- Enable all guards
- Enable all interceptors
- Enable all pipes
- Enable all exception filters

### Request Lifecycle Monitoring

**Monitoring Metrics**:
- Request rate
- Response time
- Error rate
- Request size
- Response size

## Example Requests

### Request Lifecycle Example

**Request**:
```bash
GET /api/users
Authorization: Bearer <token>
```

## Example Responses

### Request Lifecycle Response

**Response**:
```json
{
  "success": true,
  "data": [...],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Sequence Diagrams

### Request Lifecycle Flow

```
Request → Middleware → Guards → Interceptors → Pipes → Controller → Service → Database → Response → Interceptors → Response
```

## Architecture Diagrams

### Request Lifecycle Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Request                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Middleware                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Guards                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptors (Pre)                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Pipes                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Service                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptors (Post)                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Response                                   │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the NestJS request lifecycle?

**Answer**: NestJS request lifecycle via:
- Middleware (pre-processing)
- Guards (authentication/authorization)
- Interceptors (pre-processing)
- Pipes (validation)
- Controller (route handler)
- Service (business logic)
- Interceptors (post-processing)
- Exception filters (error handling)

### Q2: How do you add middleware in NestJS?

**Answer**: Middleware via:
- Apply at module level
- Apply at global level
- Implement NestMiddleware interface
- Use @Injectable() decorator
- Register in module

### Q3: How do you handle errors in NestJS?

**Answer**: Error handling via:
- Exception filters
- Built-in HTTP exceptions
- Custom exception filters
- Global exception filter
- Error logging

## Exercises

### Exercise 1: Create a Middleware

**Task**: Create a custom middleware.

**Steps**:
1. Implement NestMiddleware interface
2. Add middleware logic
3. Register middleware in module
4. Test middleware
5. Test request flow

**Verification**:
- Middleware created
- Logic works
- Middleware registered
- Request flow correct
- Tests pass

### Exercise 2: Create an Interceptor

**Task**: Create a custom interceptor.

**Steps**:
1. Implement NestInterceptor interface
2. Add interceptor logic
3. Register interceptor globally
4. Test interceptor
5. Test request flow

**Verification**:
- Interceptor created
- Logic works
- Interceptor registered
- Request flow correct
- Tests pass

## Real Production Scenarios

### Scenario 1: Slow Request

**Situation**: Request taking too long

**Response**:
1. Check middleware
2. Check guards
3. Check service
4. Check database queries
5. Optimize slow operation

### Scenario 2: Request Failing

**Situation**: Request failing with error

**Response**:
1. Check error logs
2. Check exception filter
3. Check validation
4. Check service logic
5. Fix error

## Navigation

**Next Section**: [01-Middleware](./01-Middleware.md)

**Previous Section**: [09-Workflows](../09-Workflows/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/09-Middleware](../03-Backend/09-Middleware.md) - Middleware details
