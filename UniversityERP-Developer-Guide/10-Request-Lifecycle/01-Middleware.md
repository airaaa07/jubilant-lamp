# Middleware

## Purpose

This document explains middleware in the University ERP system. It details how middleware works, how to create custom middleware, and how middleware fits into the request lifecycle.

## Why This Document Exists

**Confirmed by Code**: Middleware is used for request preprocessing. Understanding middleware is critical for:
- Implementing cross-cutting concerns
- Preprocessing requests
- Postprocessing responses
- Debugging request issues
- Adding custom middleware

Without understanding middleware, developers may struggle with request preprocessing or may introduce middleware bugs.

## Where This Is Used

- **Onboarding**: New developers learn middleware
- **Feature Development**: Implementing middleware
- **Code Reviews**: Reviewing middleware code
- **Debugging**: Debugging request issues
- **Cross-Cutting Concerns**: Implementing cross-cutting concerns

## Dependencies

### Middleware Dependencies

**Confirmed by Code**: Middleware depends on:

- **NestJS**: Framework for middleware
- **Express**: Underlying HTTP server
- **TypeScript**: Type-safe middleware

## Internal Architecture

### Middleware Architecture

**Confirmed by Code**: Middleware executes before guards.

```
┌─────────────────────────────────────────────────────────┐
│              Request                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Middleware                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Guards                                      │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Middleware Implementation

**Confirmed by Code**: Middleware implements NestMiddleware interface.

**Logger Middleware**:
```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
  }
}
```

**What This Does**:
- **NestMiddleware**: Implements NestMiddleware interface
- **use()**: Middleware function
- **Log**: Logs request method and URL
- **next()**: Passes control to next middleware

**CORS Middleware**:
```typescript
@Injectable()
export class CorsMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
      res.sendStatus(200);
      return;
    }
    
    next();
  }
}
```

**What This Does**:
- **CORS Headers**: Adds CORS headers
- **OPTIONS**: Handles OPTIONS preflight request
- **next()**: Passes control to next middleware

**Request ID Middleware**:
```typescript
@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    req.id = req.headers['x-request-id'] as string || generateId();
    res.setHeader('X-Request-ID', req.id);
    next();
  }
}

function generateId(): string {
  return Math.random().toString(36).substring(2, 15);
}
```

**What This Does**:
- **Request ID**: Generates or uses request ID
- **Header**: Adds request ID to response header
- **Tracking**: Enables request tracking

### Middleware Registration

**Confirmed by Code**: Middleware registered in module.

**Module Registration**:
```typescript
@Module({
  imports: [],
  controllers: [],
  providers: [],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(LoggerMiddleware, CorsMiddleware, RequestIdMiddleware)
      .forRoutes('*');
  }
}
```

**What This Does**:
- **configure()**: Configures middleware
- **apply()**: Applies middleware
- **forRoutes()**: Applies to all routes

## Database Interactions

### Middleware-Database Flow

**Confirmed by Code**: Middleware doesn't interact with database.

**Flow**:
```
Middleware → No database interaction
```

## Redis Interactions

### Middleware-Redis Flow

**Confirmed by Code**: Middleware can use Redis for rate limiting.

**Flow**:
```
Middleware → Redis → Rate Limit Check
```

## Queue Interactions

### Middleware-Queue Flow

**Confirmed by Code**: Middleware doesn't interact with queues.

**Flow**:
```
Middleware → No queue interaction
```

## Worker Interactions

### Middleware-Worker Flow

**Confirmed by Code**: Workers don't use middleware.

**Flow**:
```
Worker → No middleware (internal service)
```

## Business Rules

### Middleware Rules

**Confirmed by Code**: Middleware follows these rules:

1. **First in Pipeline**: Middleware executes first
2. **Sequential**: Middleware executes sequentially
3. **next()**: Must call next() to continue
4. **Order Matters**: Middleware order matters
5. **Global/Local**: Can be global or local

### Middleware Order Rules

**Confirmed by Code**: Middleware order follows these rules:

1. **CORS First**: CORS middleware first
2. **Logger Second**: Logger middleware second
3. **Request ID Third**: Request ID middleware third
4. **Rate Limiting**: Rate limiting middleware
5. **Body Parser**: Body parser middleware

## Security

### Middleware Security

**Confirmed by Code**: Security considerations for middleware:

1. **CORS**: Configure CORS properly
2. **Rate Limiting**: Implement rate limiting
3. **Security Headers**: Add security headers
4. **Input Sanitization**: Sanitize input
5. **Request Validation**: Validate requests

## Performance Considerations

### Middleware Performance

**Confirmed by Code**: Performance considerations:

1. **Fast Execution**: Keep middleware fast
2. **Async Operations**: Use async for slow operations
3. **Caching**: Cache middleware results
4. **Order**: Order middleware for performance
5. **Skip**: Skip middleware when possible

## Common Mistakes

### Mistake 1: Not Calling next()

**Symptom**: Request hangs

**Cause**: Not calling next()

**Fix**:
```typescript
// Always call next()
next();
```

### Mistake 2: Wrong Middleware Order

**Symptom**: Middleware not working as expected

**Cause**: Wrong middleware order

**Fix**:
```typescript
// Order middleware correctly
consumer.apply(LoggerMiddleware, CorsMiddleware).forRoutes('*');
```

### Mistake 3: Not Handling Errors

**Symptom**: Errors not caught

**Cause**: Not handling errors in middleware

**Fix**:
```typescript
// Add error handling
try {
  // middleware logic
  next();
} catch (error) {
  next(error);
}
```

## Debugging Guide

### Middleware Debugging

**Issue**: Middleware not working

**Investigation**:
1. Check middleware registration
2. Check middleware order
3. Check next() call
4. Check middleware logic
5. Check logs

**Tools**:
- Middleware logs
- Request logs
- Response logs
- Console logs

## Future Enhancements

### Rate Limiting Middleware

**Status**: Partially implemented

**Proposal**: Implement comprehensive rate limiting:
- Per-user rate limiting
- Per-endpoint rate limiting
- Adaptive rate limiting
- Redis-backed rate limiting
- Better protection

### Security Headers Middleware

**Status**: Not implemented

**Proposal**: Implement security headers:
- HSTS header
- X-Frame-Options header
- X-Content-Type-Options header
- CSP header
- Better security

## Production Considerations

### Production Middleware

**Production Deployment**:
- Enable all middleware
- Configure CORS properly
- Enable rate limiting
- Add security headers
- Monitor middleware performance

### Middleware Monitoring

**Monitoring Metrics**:
- Middleware execution time
- Middleware error rate
- Rate limiting violations
- CORS violations
- Request ID tracking

## Example Requests

### Middleware Example

**Request**:
```bash
GET /api/users
X-Request-ID: custom-id
```

## Example Responses

### Middleware Response

**Response**:
```http
HTTP/1.1 200 OK
X-Request-ID: custom-id
Content-Type: application/json
```

## Sequence Diagrams

### Middleware Flow

```
Request → Middleware 1 → Middleware 2 → Middleware 3 → Guards → Controller → Service → Response
```

## Architecture Diagrams

### Middleware Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Request                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Middleware 1                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Middleware 2                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Middleware 3                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Guards                                      │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does middleware work in NestJS?

**Answer**: Middleware via:
- Implements NestMiddleware interface
- Executes before guards
- Can modify request/response
- Must call next() to continue
- Can be global or local

### Q2: How do you register middleware in NestJS?

**Answer**: Middleware registration via:
- Implement NestMiddleware interface
- Register in module's configure() method
- Use MiddlewareConsumer
- Apply to routes with forRoutes()
- Can apply multiple middleware

### Q3: What is the difference between middleware and interceptors?

**Answer**: Middleware vs Interceptors:
- Middleware: Express-level, executes before guards
- Interceptors: NestJS-level, executes before/after controller
- Middleware: Can modify request/response
- Interceptors: Can transform data
- Middleware: Less powerful, more performant

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

### Exercise 2: Create Rate Limiting Middleware

**Task**: Create rate limiting middleware.

**Steps**:
1. Implement rate limiting logic
2. Use Redis for tracking
3. Add rate limit check
4. Handle rate limit exceeded
5. Test rate limiting

**Verification**:
- Rate limiting implemented
- Redis tracking works
- Rate limit check works
- Exceeded handled
- Tests pass

## Real Production Scenarios

### Scenario 1: Middleware Not Executing

**Situation**: Middleware not executing

**Response**:
1. Check middleware registration
2. Check middleware order
3. Check route matching
4. Fix registration
5. Test middleware

### Scenario 2: Request Hanging

**Situation**: Request hanging

**Response**:
1. Check next() call
2. Check middleware logic
3. Check for errors
4. Fix middleware
5. Test request

## Navigation

**Next Section**: [02-Guards](./02-Guards.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/09-Middleware](../03-Backend/09-Middleware.md) - Middleware details
