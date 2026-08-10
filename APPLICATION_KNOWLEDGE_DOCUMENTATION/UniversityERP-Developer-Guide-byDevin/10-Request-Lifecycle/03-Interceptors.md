# Interceptors

## Purpose

This document explains interceptors in the University ERP system. It details how interceptors work, how to create custom interceptors, and how interceptors fit into the request lifecycle.

## Why This Document Exists

**Confirmed by Code**: Interceptors are used for cross-cutting concerns. Understanding interceptors is critical for:
- Implementing logging
- Transforming requests/responses
- Caching
- Measuring performance
- Adding custom logic

Without understanding interceptors, developers may struggle with cross-cutting concerns or may introduce bugs.

## Where This Is Used

- **Onboarding**: New developers learn interceptors
- **Feature Development**: Implementing interceptors
- **Code Reviews**: Reviewing interceptor code
- **Debugging**: Debugging request issues
- **Cross-Cutting Concerns**: Implementing cross-cutting concerns

## Dependencies

### Interceptor Dependencies

**Confirmed by Code**: Interceptors depend on:

- **NestJS**: Framework for interceptors
- **RxJS**: Observable operators
- **TypeScript**: Type-safe interceptors

## Internal Architecture

### Interceptor Architecture

**Confirmed by Code**: Interceptors execute before/after controller.

```
┌─────────────────────────────────────────────────────────┐
│              Guards                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Interceptors (Pre)                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Controller                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Interceptors (Post)                          │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Interceptor Implementation

**Confirmed by Code**: Interceptors implement NestInterceptor interface.

**LoggingInterceptor**:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

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
- **NestInterceptor**: Implements NestInterceptor interface
- **intercept()**: Interceptor function
- **Pre-Request**: Records start time
- **Post-Request**: Logs request duration
- **tap()**: Side effect operator

**TransformInterceptor**:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

interface ResponseDto<T> {
  success: boolean;
  data: T;
  timestamp: string;
}

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
- **map()**: Transform operator

**CacheInterceptor**:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { of } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class CacheInterceptor implements NestInterceptor {
  constructor(private redis: RedisService) {}

  async intercept(context: ExecutionContext, next: CallHandler): Promise<Observable<any>> {
    const request = context.switchToHttp().getRequest();
    const cacheKey = `${request.method}:${request.url}`;

    // Check cache
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return of(JSON.parse(cached));
    }

    // Execute request
    return next.handle().pipe(
      tap(async (data) => {
        await this.redis.setex(cacheKey, 300, JSON.stringify(data));
      }),
    );
  }
}
```

**What This Does**:
- **Cache Check**: Checks Redis cache
- **Cache Hit**: Returns cached data
- **Cache Miss**: Executes request and caches result
- **TTL**: 5 minute TTL

**TimeoutInterceptor**:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { timeout, catchError } from 'rxjs/operators';
import { RequestTimeoutException } from '@nestjs/common';

@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      timeout(5000),
      catchError(err => {
        if (err.name === 'TimeoutError') {
          throw new RequestTimeoutException('Request timeout');
        }
        throw err;
      }),
    );
  }
}
```

**What This Does**:
- **timeout()**: 5 second timeout
- **catchError()**: Catches timeout error
- **RequestTimeoutException**: Throws timeout exception

### Interceptor Registration

**Confirmed by Code**: Interceptors registered globally or locally.

**Global Registration**:
```typescript
@Module({
  providers: [
    {
      provide: APP_INTERCEPTOR,
      useClass: LoggingInterceptor,
    },
    {
      provide: APP_INTERCEPTOR,
      useClass: TransformInterceptor,
    },
  ],
})
export class AppModule {}
```

**What This Does**:
- **APP_INTERCEPTOR**: Registers interceptor globally
- **useClass**: Uses interceptor class
- **Order**: Interceptors execute in registration order

**Local Registration**:
```typescript
@Controller('users')
@UseInterceptors(TransformInterceptor)
export class UsersController {
  @Get()
  @UseInterceptors(CacheInterceptor)
  findAll() {
    return this.usersService.findAll();
  }
}
```

**What This Does**:
- **@UseInterceptors**: Applies interceptor to controller/method
- **TransformInterceptor**: Applied at controller level
- **CacheInterceptor**: Applied at method level

## Database Interactions

### Interceptor-Database Flow

**Confirmed by Code**: Interceptors don't directly interact with database.

**Flow**:
```
Interceptor → No database interaction
```

## Redis Interactions

### Interceptor-Redis Flow

**Confirmed by Code**: Interceptors can use Redis for caching.

**Flow**:
```
Interceptor → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Interceptor-Queue Flow

**Confirmed by Code**: Interceptors don't interact with queues.

**Flow**:
```
Interceptor → No queue interaction
```

## Worker Interactions

### Interceptor-Worker Flow

**Confirmed by Code**: Workers don't use interceptors.

**Flow**:
```
Worker → No interceptors (internal service)
```

## Business Rules

### Interceptor Rules

**Confirmed by Code**: Interceptors follow these rules:

1. **NestInterceptor**: Implement NestInterceptor interface
2. **Observable**: Return Observable
3. **RxJS Operators**: Use RxJS operators
4. **Pre/Post**: Can execute before/after controller
5. **Chaining**: Can chain multiple interceptors

### Interceptor Order Rules

**Confirmed by Code**: Interceptor order follows these rules:

1. **Global First**: Global interceptors first
2. **Local Second**: Local interceptors second
3. **Registration Order**: Execute in registration order
4. **Controller Level**: Controller-level before method-level
5. **All Execute**: All interceptors execute

## Security

### Interceptor Security

**Confirmed by Code**: Security considerations for interceptors:

1. **Data Sanitization**: Sanitize sensitive data in logs
2. **Cache Security**: Secure cached data
3. **Error Handling**: Handle errors properly
4. **Input Validation**: Validate input in pre-interceptor
5. **Output Sanitization**: Sanitize output in post-interceptor

## Performance Considerations

### Interceptor Performance

**Confirmed by Code**: Performance considerations:

1. **Fast Execution**: Keep interceptors fast
2. **Caching**: Use caching for expensive operations
3. **Async Operations**: Use async for slow operations
4. **RxJS Operators**: Use efficient RxJS operators
5. **Skip**: Skip interceptor when possible

## Common Mistakes

### Mistake 1: Not Returning Observable

**Symptom**: Interceptor not working

**Cause**: Not returning Observable

**Fix**:
```typescript
// Return Observable
return next.handle();
```

### Mistake 2: Not Handling Errors

**Symptom**: Errors not caught

**Cause**: Not handling errors in interceptor

**Fix**:
```typescript
// Add error handling
return next.handle().pipe(
  catchError(err => {
    // handle error
    throw err;
  }),
);
```

### Mistake 3: Not Using RxJS Operators

**Symptom**: Interceptor not working as expected

**Cause**: Not using RxJS operators

**Fix**:
```typescript
// Use RxJS operators
return next.handle().pipe(
  map(data => transform(data)),
);
```

## Debugging Guide

### Interceptor Debugging

**Issue**: Interceptor not working

**Investigation**:
1. Check interceptor registration
2. Check interceptor logic
3. Check RxJS operators
4. Check Observable chain
5. Check logs

**Tools**:
- Interceptor logs
- Request logs
- Response logs
- Console logs

## Future Enhancements

### Caching Interceptor

**Status**: Partially implemented

**Proposal**: Implement comprehensive caching:
- Cache invalidation
- Cache tags
- Cache warming
- Better cache control
- More complex

### Metrics Interceptor

**Status**: Not implemented

**Proposal**: Implement metrics interceptor:
- Request metrics
- Response metrics
- Error metrics
- Performance metrics
- Better monitoring

## Production Considerations

### Production Interceptors

**Production Deployment**:
- Enable all interceptors
- Configure caching
- Configure timeout
- Monitor interceptor performance
- Monitor interceptor errors

### Interceptor Monitoring

**Monitoring Metrics**:
- Interceptor execution time
- Cache hit rate
- Timeout rate
- Error rate
- Transform rate

## Example Requests

### Interceptor Example

**Request**:
```bash
GET /api/users
```

## Example Responses

### Interceptor Response

**Response**:
```json
{
  "success": true,
  "data": [...],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Sequence Diagrams

### Interceptor Flow

```
Request → Guards → Interceptor (Pre) → Controller → Service → Interceptor (Post) → Response
```

## Architecture Diagrams

### Interceptor Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Guards                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptor 1 (Pre)                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptor 2 (Pre)                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptor 2 (Post)                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptor 1 (Post)                      │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do interceptors work in NestJS?

**Answer**: Interceptors via:
- Implement NestInterceptor interface
- Return Observable
- Execute before/after controller
- Use RxJS operators
- Can transform data

### Q2: How do you create a custom interceptor?

**Answer**: Custom interceptor via:
- Implement NestInterceptor interface
- Add interceptor logic
- Use RxJS operators
- Return Observable
- Register interceptor

### Q3: What is the difference between interceptors and middleware?

**Answer**: Interceptors vs Middleware:
- Interceptors: NestJS-level, executes after guards
- Middleware: Express-level, executes before guards
- Interceptors: Can transform data
- Middleware: Can modify request/response
- Interceptors: RxJS-based
- Middleware: Express-based

## Exercises

### Exercise 1: Create an Interceptor

**Task**: Create a custom interceptor.

**Steps**:
1. Implement NestInterceptor interface
2. Add interceptor logic
3. Use RxJS operators
4. Register interceptor
5. Test interceptor

**Verification**:
- Interceptor created
- Logic works
- RxJS operators work
- Interceptor registered
- Tests pass

### Exercise 2: Create a Caching Interceptor

**Task**: Create a caching interceptor.

**Steps**:
1. Implement NestInterceptor interface
2. Add cache check logic
3. Use Redis for caching
4. Add cache invalidation
5. Test caching

**Verification**:
- Interceptor created
- Cache check works
- Redis works
- Cache invalidation works
- Tests pass

## Real Production Scenarios

### Scenario 1: Interceptor Not Executing

**Situation**: Interceptor not executing

**Response**:
1. Check interceptor registration
2. Check interceptor order
3. Check interceptor logic
4. Fix registration
5. Test interceptor

### Scenario 2: Interceptor Causing Error

**Situation**: Interceptor causing error

**Response**:
1. Check interceptor logic
2. Check RxJS operators
3. Check error handling
4. Fix interceptor
5. Test interceptor

## Navigation

**Next Section**: [04-Pipes](./04-Pipes.md)

**Previous Section**: [02-Guards](./02-Guards.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/08-Interceptors](../03-Backend/08-Interceptors.md) - Interceptors details
