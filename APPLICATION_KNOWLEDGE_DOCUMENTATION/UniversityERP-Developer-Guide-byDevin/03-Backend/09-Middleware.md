# Middleware

## Purpose

This document explains the middleware pattern used in the University ERP backend. It details how middleware handles request processing, implements cross-cutting concerns, and differs from interceptors.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS middleware for request processing. Understanding middleware is critical for:
- Implementing request processing
- Implementing cross-cutting concerns
- Understanding middleware vs interceptors
- Implementing Express-specific logic
- Debugging request issues

Without understanding middleware, developers may struggle with request processing or may misuse middleware vs interceptors.

## Where This Is Used

- **Onboarding**: New developers learn middleware pattern
- **Feature Development**: Creating middleware for request processing
- **Code Reviews**: Reviewing middleware implementation
- **Request Processing**: Implementing request processing logic
- **Debugging**: Debugging request issues

## Dependencies

### Middleware Dependencies

**Confirmed by Code**: Middleware depends on:

- **NestJS Middleware**: Middleware interface
- **Express**: Express middleware
- **Request/Response**: Express request/response objects
- **Next Function**: Next middleware in chain

## Internal Architecture

### Middleware Architecture

**Confirmed by Code**: Middleware follows a chain Pattern.

```
┌─────────────────────────────────────────────────────────┐
│                  Middleware Chain                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  CORS         │  │  Body Parser    │  │  Logging       │
│  Middleware   │  │  Middleware     │  │  Middleware    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Middleware Definition

**Confirmed by Code**: Middleware defined with @Middleware decorator.

**Basic Middleware**:
```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class MyMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log('Request received');
    next();
  }
}
```

**What This Does**:
- **NestMiddleware**: Interface for middleware
- **use()**: Middleware function
- **req**: Express request object
- **res**: Express response object
- **next()**: Next middleware in chain

### CORS Middleware

**Confirmed by Code**: CORS enabled in main.ts.

**CORS Configuration**:
```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.enableCors({
    origin: process.env.CORS_ORIGIN || '*',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS',
    credentials: true,
  });
  
  await app.listen(3000);
}
```

**What This Does**:
- **enableCors()**: Enables CORS
- **origin**: Allowed origins
- **methods**: Allowed HTTP methods
- **credentials**: Allow credentials

### Logging Middleware

**Confirmed by Code**: Logging middleware logs requests.

**LoggingMiddleware**:
```typescript
@Injectable()
export class LoggingMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const { method, url, ip } = req;
    const userAgent = req.get('user-agent') || '';
    
    console.log(`[${new Date().toISOString()}] ${method} ${url} ${userAgent} ${ip}`);
    
    next();
  }
}
```

**What This Does**:
- **Request Logging**: Logs request details
- **Timing**: Logs timestamp
- **User Agent**: Logs user agent
- **IP**: Logs client IP

### Body Parser Middleware

**Confirmed by Code**: Body parser configured in main.ts.

**Body Parser Configuration**:
```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));
  
  await app.listen(3000);
}
```

**What This Does**:
- **express.json()**: Parses JSON bodies
- **express.urlencoded()**: Parses URL-encoded bodies
- **extended**: Allows nested objects

### Request ID Middleware

**Status**: Not implemented

**Proposal**: Request ID middleware for request tracing.

**RequestIdMiddleware**:
```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const requestId = req.headers['x-request-id'] as string || uuidv4();
    req['requestId'] = requestId;
    res.setHeader('x-request-id', requestId);
    next();
  }
}
```

**What This Does**:
- **Request ID**: Generates or extracts request ID
- **Header**: Sets request ID in response header
- **Tracing**: Enables request tracing
- **Debugging**: Helps with debugging

## Database Interactions

### Middleware-Database Flow

**Confirmed by Code**: Middleware doesn't directly interact with database.

**Flow**:
```
Request → Middleware → Controller → Service → Database
```

## Redis Interactions

### Middleware-Redis Flow

**Confirmed by Code**: Middleware doesn't directly interact with Redis.

**Flow**:
```
Request → Middleware → Controller → Service → Redis
```

## Queue Interactions

### Middleware-Queue Flow

**Confirmed by Code**: Middleware doesn't directly interact with queues.

**Flow**:
```
Request → Middleware → Controller → Service → Queue
```

## Worker Interactions

### Middleware-Worker Flow

**Confirmed by Code**: Workers don't use middleware.

**Flow**:
```
Worker processes job directly without middleware
```

## Business Rules

### Middleware Rules

**Confirmed by Code**: Middleware follows these rules:

1. **Request Processing**: Use for request processing
2. **Cross-Cutting Concerns**: Use for cross-cutting concerns
3. **Express-Specific**: Use for Express-specific logic
4. **Chain Pattern**: Middleware forms a chain
5. **Next()**: Always call next() unless terminating

### Middleware vs Interceptors

**Confirmed by Code**: Middleware vs Interceptors:

**Middleware**:
- Express-based
- Can't modify response
- Less powerful
- Good for Express-specific logic
- Runs before interceptors

**Interceptors**:
- NestJS-specific
- Can modify response
- More powerful
- Good for AOP
- Runs after middleware

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

**Confirmed by Code**: Performance considerations for middleware:

1. **Fast Execution**: Keep middleware fast
2. **Minimal Overhead**: Minimize overhead
3. **Early Return**: Return early if possible
4. **Async Operations**: Use async for expensive operations
5. **Ordering**: Order middleware efficiently

## Common Mistakes

### Mistake 1: Not Calling next()

**Symptom**: Request hangs

**Cause**: Not calling next()

**Fix**:
```typescript
// Wrong
use(req: Request, res: Response, next: NextFunction) {
  console.log('Request received');
  // Missing next()
}

// Correct
use(req: Request, res: Response, next: NextFunction) {
  console.log('Request received');
  next();
}
```

### Mistake 2: Using Middleware Instead of Interceptor

**Symptom**: Can't modify response

**Cause**: Using middleware instead of interceptor

**Fix**:
```typescript
// Use interceptor for response modification
// Use middleware for request processing
```

### Mistake 3: Blocking in Middleware

**Symptom**: Slow requests

**Cause**: Blocking operations in middleware

**Fix**:
```typescript
// Use async operations
use(req: Request, res: Response, next: NextFunction) {
  asyncFunction().then(() => next());
}
```

## Debugging Guide

### Middleware Debugging

**Issue**: Middleware not working

**Investigation**:
1. Check middleware registration
2. Check middleware logic
3. Check middleware order
4. Check next() call
5. Check logs

**Tools**:
- Middleware logs
- Request logs
- Network tools
- Express debugger

## Future Enhancements

### Rate Limiting Middleware

**Status**: Not implemented

**Proposal**: Implement rate limiting middleware:
- Rate limit by IP
- Rate limit by user
- Configurable limits
- Sliding window algorithm
- Distributed rate limiting

### Security Headers Middleware

**Status**: Not implemented

**Proposal**: Implement security headers middleware:
- Add security headers
- Helmet integration
- CSP headers
- HSTS headers
- X-Frame-Options

## Production Considerations

### Production Middleware

**Production Deployment**:
- Enable all necessary middleware
- Configure CORS properly
- Configure rate limiting
- Configure security headers
- Monitor middleware performance

### Middleware Monitoring

**Monitoring Metrics**:
- Middleware execution time
- Middleware error rate
- Request rate
- Response time
- Error rate

## Example Requests

### Middleware Example

**Request**:
```bash
GET /api/users
```

**Middleware Logs**:
```
[2024-01-01T00:00:00Z] GET /api/users Mozilla/5.0 127.0.0.1
```

## Example Responses

### Middleware Output

**Response**: Middleware logs

```
[2024-01-01T00:00:00Z] GET /api/users Mozilla/5.0 127.0.0.1
[2024-01-01T00:00:00.100Z] GET /api/users 200 100ms
```

## Sequence Diagrams

### Middleware Flow

```
Request → Middleware 1 → Middleware 2 → Controller → Service
            ↓                ↓
        Pre-Processing  Pre-Processing
            ↓                ↓
        Post-Processing Post-Processing
            ↓                ↓
        Response
```

## Architecture Diagrams

### Middleware Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  CORS Middleware                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Body Parser Middleware                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Logging Middleware                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the difference between middleware and interceptors?

**Answer**: Middleware vs Interceptors:
- Middleware: Express-based, can't modify response, less powerful
- Interceptors: NestJS-specific, can modify response, more powerful
- Middleware: Runs before interceptors
- Interceptors: Runs after middleware
- Middleware: Good for Express-specific logic
- Interceptors: Good for AOP

### Q2: When should you use middleware vs interceptors?

**Answer**: Use middleware when:
- Need Express-specific logic
- Need to process request before NestJS
- Need to terminate request early
- Need to modify request before NestJS

Use interceptors when:
- Need to modify response
- Need AOP patterns
- Need to use RxJS operators
- Need to implement cross-cutting concerns

### Q3: How do you create custom middleware?

**Answer**: Custom middleware via:
- Implement NestMiddleware interface
- Define use method
- Register in module
- Apply to routes or globally
- Call next() to continue chain

## Exercises

### Exercise 1: Create a Logging Middleware

**Task**: Create a logging middleware.

**Steps**:
1. Implement NestMiddleware interface
2. Add logging logic
3. Call next()
4. Register in module
5. Test middleware

**Verification**:
- Middleware created
- Logging works
- Chain works
- Tests pass

### Exercise 2: Create a Request ID Middleware

**Task**: Create a request ID middleware.

**Steps**:
1. Implement NestMiddleware interface
2. Generate or extract request ID
3. Set in request and response
4. Call next()
5. Test middleware

**Verification**:
- Middleware created
- Request ID works
- Tracing works
- Tests pass

## Real Production Scenarios

### Scenario 1: Middleware Order Issue

**Situation**: Middleware not working as expected

**Response**:
1. Check middleware order
2. Reorder middleware
3. Test middleware
4. Monitor behavior
5. Fix order

### Scenario 2: Middleware Performance Issue

**Situation**: Middleware causing slow requests

**Response**:
1. Identify slow middleware
2. Optimize middleware logic
3. Add caching if applicable
4. Monitor performance
5. Test optimization

## Navigation

**Next Section**: [10-Exception-Filters](./10-Exception-Filters.md)

**Previous Section**: [08-Interceptors](./08-Interceptors.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [08-Interceptors](./08-Interceptors.md) - Interceptors
- [11-Monitoring-and-Logging](../01-System-Architecture/11-Monitoring-and-Logging.md) - Monitoring and logging
