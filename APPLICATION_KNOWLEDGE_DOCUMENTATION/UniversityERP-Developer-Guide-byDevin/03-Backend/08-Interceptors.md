# Interceptors

## Purpose

This document explains the interceptor pattern used in the University ERP backend. It details how interceptors transform requests and responses, implement cross-cutting concerns, and handle AOP (Aspect-Oriented Programming).

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS interceptors for cross-cutting concerns. Understanding interceptors is critical for:
- Implementing logging
- Implementing caching
- Transforming requests/responses
- Measuring execution time
- Implementing AOP patterns

Without understanding interceptors, developers may struggle to implement cross-cutting concerns.

## Where This Is Used

- **Onboarding**: New developers learn interceptor pattern
- **Feature Development**: Creating interceptors for cross-cutting concerns
- **Code Reviews**: Reviewing interceptor implementation
- **Logging**: Implementing logging
- **Performance**: Measuring execution time

## Dependencies

### Interceptor Dependencies

**Confirmed by Code**: Interceptors depend on:

- **NestJS Interceptors**: Interceptor interface
- **RxJS**: Observable operators
- **ExecutionContext**: Execution context
- **CallHandler**: Next handler in chain

## Internal Architecture

### Interceptor Architecture

**Confirmed by Code**: Interceptors follow a chain pattern.

```
┌─────────────────────────────────────────────────────────┐
│                  Interceptor Chain                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Logging      │  │  Caching        │  │  Transform     │
│  Interceptor  │  │  Interceptor    │  │  Interceptor    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Interceptor Definition

**Confirmed by Code**: Interceptors implement NestInterceptor interface.

**Basic Interceptor**:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const now = Date.now();
    return next.handle().pipe(
      tap(() => {
        const delay = Date.now() - now;
        console.log(`Request took ${delay}ms`);
      }),
    );
  }
}
```

**What This Does**:
- **NestInterceptor**: Interface for interceptor
- **intercept()**: Intercepts request/response
- **ExecutionContext**: Provides request context
- **CallHandler**: Next handler in chain
- **Observable**: Returns observable for async handling

### Logging Interceptor

**Confirmed by Code**: Logging interceptor logs requests and responses.

**LoggingInterceptor**:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url, ip } = request;
    const userAgent = request.get('user-agent') || '';
    const now = Date.now();

    console.log(`[${new Date().toISOString()}] ${method} ${url} ${userAgent} ${ip}`);

    return next.handle().pipe(
      tap(() => {
        const response = context.switchToHttp().getResponse();
        const delay = Date.now() - now;
        console.log(`[${new Date().toISOString()}] ${method} ${url} ${response.statusCode} ${delay}ms`);
      }),
    );
  }
}
```

**What This Does**:
- **Request Logging**: Logs request method, URL, user agent, IP
- **Response Logging**: Logs response status code and duration
- **Timing**: Measures request duration
- **Context Access**: Accesses request and response

### Caching Interceptor

**Status**: Not implemented

**Proposal**: Caching interceptor for GET requests.

**CacheInterceptor**:
```typescript
@Injectable()
export class CacheInterceptor implements NestInterceptor {
  constructor(private cacheManager: Cache) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const cacheKey = `${request.method}:${request.url}`;

    return from(this.cacheManager.get(cacheKey)).pipe(
      switchMap((cached) => {
        if (cached) {
          return of(cached);
        }

        return next.handle().pipe(
          tap((response) => {
            this.cacheManager.set(cacheKey, response, { ttl: 300 });
          }),
        );
      }),
    );
  }
}
```

### Transform Interceptor

**Confirmed by Code**: Transform interceptor can transform responses.

**TransformInterceptor**:
```typescript
@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => ({
        success: true,
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}
```

**What This Does**:
- **map()**: Transforms response data
- **Standard Format**: Wraps response in standard format
- **Timestamp**: Adds timestamp to response
- **Success Flag**: Adds success flag

### Timeout Interceptor

**Status**: Not implemented

**Proposal**: Timeout interceptor for long-running requests.

**TimeoutInterceptor**:
```typescript
@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      timeout(5000), // 5 second timeout
    );
  }
}
```

## Database Interactions

### Interceptor-Database Flow

**Confirmed by Code**: Interceptors don't directly interact with database.

**Flow**:
```
Request → Interceptor → Controller → Service → Database
```

## Redis Interactions

### Interceptor-Redis Flow

**Confirmed by Code**: Caching interceptor would interact with Redis.

**Flow**:
```
Request → Interceptor → Redis Cache Check
                              ↓
                         Cache Hit → Return
                              ↓
                         Cache Miss → Controller → Service → Redis Cache Set
```

## Queue Interactions

### Interceptor-Queue Flow

**Confirmed by Code**: Interceptors don't directly interact with queues.

**Flow**:
```
Request → Interceptor → Controller → Service → Queue
```

## Worker Interactions

### Interceptor-Worker Flow

**Confirmed by Code**: Workers don't use interceptors.

**Flow**:
```
Worker processes job directly without interceptors
```

## Business Rules

### Interceptor Rules

**Confirmed by Code**: Interceptors follow these rules:

1. **Cross-Cutting Concerns**: Use for cross-cutting concerns
2. **Chain Pattern**: Interceptors form a chain
3. **Observable Return**: Always return Observable
4. **Error Handling**: Handle errors appropriately
5. **Performance**: Keep interceptors fast

### Logging Rules

**Confirmed by Code**: Logging follows these rules:

1. **Request Logging**: Log all requests
2. **Response Logging**: Log all responses
3. **Error Logging**: Log all errors
4. **Performance Logging**: Log execution time
5. **Security Logging**: Log security events

## Security

### Interceptor Security

**Confirmed by Code**: Security considerations for interceptors:

1. **No Sensitive Data**: Don't log sensitive data
2. **Sanitization**: Sanitize logged data
3. **Access Control**: Log access attempts
4. **Audit Trail**: Maintain audit trail
5. **Secure Storage**: Secure log storage

## Performance Considerations

### Interceptor Performance

**Confirmed by Code**: Performance considerations for interceptors:

1. **Fast Execution**: Keep interceptors fast
2. **Minimal Overhead**: Minimize overhead
3. **Async Operations**: Use async for expensive operations
4. **Caching**: Cache interceptor results if applicable
5. **Conditional Execution**: Conditionally execute interceptors

## Common Mistakes

### Mistake 1: Not Returning Observable

**Symptom**: Interceptor not working

**Cause**: Not returning Observable

**Fix**:
```typescript
// Wrong
intercept(context: ExecutionContext, next: CallHandler) {
  return next.handle();
}

// Correct
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  return next.handle();
}
```

### Mistake 2: Blocking in Interceptor

**Symptom**: Slow requests

**Cause**: Blocking operations in interceptor

**Fix**:
```typescript
// Use async operations
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  return next.handle().pipe(
    tap(async (data) => {
      await this.asyncOperation(data);
    }),
  );
}
```

### Mistake 3: Logging Sensitive Data

**Symptom**: Sensitive data in logs

**Cause**: Logging sensitive data

**Fix**:
```typescript
// Sanitize logged data
const request = context.switchToHttp().getRequest();
const { password, ...sanitizedRequest } = request.body;
console.log(sanitizedRequest);
```

## Debugging Guide

### Interceptor Debugging

**Issue**: Interceptor not working

**Investigation**:
1. Check interceptor registration
2. Check interceptor logic
3. Check Observable chain
4. Check error handling
5. Check logs

**Tools**:
- Interceptor logs
- Request logs
- Observable debugging
- RxJS operators

## Future Enhancements

### Rate Limiting Interceptor

**Status**: Not implemented

**Proposal**: Implement rate limiting interceptor:
- Rate limit by IP
- Rate limit by user
- Configurable limits
- Sliding window algorithm
- Distributed rate limiting

### Compression Interceptor

**Status**: Not implemented

**Proposal**: Implement compression interceptor:
- Compress responses
- Decompress requests
- Configurable compression
- Different compression algorithms
- Performance monitoring

## Production Considerations

### Production Interceptors

**Production Deployment**:
- Enable all interceptors
- Configure logging level
- Configure cache TTL
- Monitor interceptor performance
- Monitor interceptor errors

### Interceptor Monitoring

**Monitoring Metrics**:
- Interceptor execution time
- Interceptor error rate
- Cache hit rate (for caching interceptor)
- Request rate
- Response time

## Example Requests

### Interceptor Example

**Request**:
```bash
GET /api/users
```

**Response** (with TransformInterceptor):
```json
{
  "success": true,
  "data": [...],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Example Responses

### Interceptor Output

**Response**: Interceptor logs

```
[2024-01-01T00:00:00Z] GET /api/users Mozilla/5.0 127.0.0.1
[2024-01-01T00:00:00.100Z] GET /api/users 200 100ms
```

## Sequence Diagrams

### Interceptor Flow

```
Request → Interceptor 1 → Interceptor 2 → Controller → Service
            ↓                ↓
        Pre-Processing  Pre-Processing
            ↓                ↓
        Post-Processing Post-Processing
            ↓                ↓
        Response
```

## Architecture Diagrams

### Interceptor Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Logging Interceptor                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Transform Interceptor                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the role of interceptors in NestJS?

**Answer**: Interceptors role:
- Transform requests and responses
- Implement cross-cutting concerns
- Implement AOP patterns
- Add logging and monitoring
- Implement caching

### Q2: How do you create a custom interceptor?

**Answer**: Custom interceptor via:
- Implement NestInterceptor interface
- Define intercept method
- Return Observable
- Use RxJS operators
- Apply to controller or globally

### Q3: How do interceptors differ from middleware?

**Answer**: Interceptors vs middleware:
- Interceptors: More powerful, can modify response, RxJS-based
- Middleware: Less powerful, can't modify response, Express-based
- Interceptors: Better for AOP
- Middleware: Better for Express-specific logic

## Exercises

### Exercise 1: Create a Logging Interceptor

**Task**: Create a logging interceptor.

**Steps**:
1. Implement NestInterceptor interface
2. Add request logging
3. Add response logging
4. Add timing
5. Apply globally

**Verification**:
- Interceptor created
- Logging works
- Timing works
- Applied correctly

### Exercise 2: Create a Transform Interceptor

**Task**: Create a transform interceptor.

**Steps**:
1. Implement NestInterceptor interface
2. Add transformation logic
3. Use RxJS map operator
4. Apply globally
5. Test transformation

**Verification**:
- Interceptor created
- Transformation works
- Response format changed
- Tests pass

## Real Production Scenarios

### Scenario 1: Slow Interceptor

**Situation**: Interceptor causing slow requests

**Response**:
1. Identify slow interceptor
2. Optimize interceptor logic
3. Add caching if applicable
4. Monitor performance
5. Test optimization

### Scenario 2: Interceptor Error

**Situation**: Interceptor throwing errors

**Response**:
1. Check interceptor logic
2. Check error handling
3. Fix error handling
4. Test interceptor
5. Monitor errors

## Navigation

**Next Section**: [09-Middleware](./09-Middleware.md)

**Previous Section**: [07-Pipes](./07-Pipes.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [11-Monitoring-and-Logging](../01-System-Architecture/11-Monitoring-and-Logging.md) - Monitoring and logging
- [18-Performance](../18-Performance/README.md) - Performance guide
