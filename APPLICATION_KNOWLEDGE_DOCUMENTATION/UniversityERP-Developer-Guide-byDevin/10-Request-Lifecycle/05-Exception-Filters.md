# Exception Filters

## Purpose

This document explains exception filters in the University ERP system. It details how exception filters work, how to create custom exception filters, and how exception filters fit into the request lifecycle.

## Why This Document Exists

**Confirmed by Code**: Exception filters are used for error handling. Understanding exception filters is critical for:
- Handling errors gracefully
- Standardizing error responses
- Logging errors
- Debugging error issues
- Creating custom exception filters

Without understanding exception filters, developers may struggle with error handling or may introduce error handling bugs.

## Where This Is Used

- **Onboarding**: New developers learn exception filters
- **Feature Development**: Implementing exception filters
- **Code Reviews**: Reviewing exception filter code
- **Error Handling**: Handling errors gracefully
- **Debugging**: Debugging error issues

## Dependencies

### Exception Filter Dependencies

**Confirmed by Code**: Exception filters depend on:

- **NestJS**: Framework for exception filters
- **TypeScript**: Type-safe exception filters

## Internal Architecture

### Exception Filter Architecture

**Confirmed by Code**: Exception filters execute when exceptions occur.

```
┌─────────────────────────────────────────────────────────┐
│              Controller/Service                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Exception Thrown                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Exception Filter                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Error Response                                │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Exception Filter Implementation

**Confirmed by Code**: Exception filters implement ExceptionFilter interface.

**HttpExceptionFilter**:
```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    const errorResponse = {
      success: false,
      error: {
        code: status,
        message: exception.message,
        ...(typeof exceptionResponse === 'object' && exceptionResponse),
      },
      timestamp: new Date().toISOString(),
    };

    response.status(status).json(errorResponse);
  }
}
```

**What This Does**:
- **@Catch(HttpException)**: Catches HTTP exceptions
- **ExceptionFilter**: Implements ExceptionFilter interface
- **catch()**: Filter function
- **Transform**: Transforms error to standard format
- **Response**: Returns error response

**AllExceptionsFilter**:
```typescript
import { ExceptionFilter, Catch, ArgumentsHost } from '@nestjs/common';
import { HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    let status = 500;
    let message = 'Internal server error';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      message = exception.message;
    }

    const errorResponse = {
      success: false,
      error: {
        code: status,
        message,
      },
      timestamp: new Date().toISOString(),
    };

    response.status(status).json(errorResponse);
  }
}
```

**What This Does**:
- **@Catch()**: Catches all exceptions
- **HttpException Handling**: Handles HTTP exceptions
- **Default Handling**: Default error handling for other exceptions
- **Response**: Returns error response

### Exception Filter Registration

**Confirmed by Code**: Exception filters registered globally or locally.

**Global Registration**:
```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalFilters(new HttpExceptionFilter());
  
  await app.listen(3000);
}
```

**What This Does**:
- **useGlobalFilters**: Applies filter globally
- **HttpExceptionFilter**: Applies to all HTTP exceptions

**Local Registration**:
```typescript
@Controller('users')
@UseFilters(HttpExceptionFilter)
export class UsersController {
  @Get()
  @UseFilters(CustomExceptionFilter)
  findAll() {
    return this.usersService.findAll();
  }
}
```

**What This Does**:
- **@UseFilters**: Applies filter to controller/method
- **HttpExceptionFilter**: Applied at controller level
- **CustomExceptionFilter**: Applied at method level

## Database Interactions

### Exception Filter-Database Flow

**Confirmed by Code**: Exception filters don't interact with database.

**Flow**:
```
Exception Filter → No database interaction
```

## Redis Interactions

### Exception Filter-Redis Flow

**Confirmed by Code**: Exception filters can log to Redis.

**Flow**:
```
Exception Filter → Redis → Error Logs
```

## Queue Interactions

### Exception Filter-Queue Flow

**Confirmed by Code**: Exception filters don't interact with queues.

**Flow**:
```
Exception Filter → No queue interaction
```

## Worker Interactions

### Exception Filter-Worker Flow

**Confirmed by Code**: Workers don't use exception filters.

**Flow**:
```
Worker → No exception filters (internal service)
```

## Business Rules

### Exception Filter Rules

**Confirmed by Code**: Exception filters follow these rules:

1. **ExceptionFilter**: Implement ExceptionFilter interface
2. **@Catch()**: Specify exception type to catch
3. **catch()**: Filter function
4. **Response**: Return error response
5. **Order**: Most specific filter first

### Exception Filter Order Rules

**Confirmed by Code**: Exception filter order follows these rules:

1. **Method-Level**: Method-level filters first
2. **Controller-Level**: Controller-level filters second
3. **Global**: Global filters last
4. **Specificity**: More specific filters first
4. **First Match**: First matching filter handles exception

## Security

### Exception Filter Security

**Confirmed by Code**: Security considerations for exception filters:

1. **Error Messages**: Don't leak sensitive info in errors
2. **Stack Traces**: Don't expose stack traces in production
3. **Logging**: Log errors for debugging
4. **Sanitization**: Sanitize error messages
5. **Monitoring**: Monitor error rates

## Performance Considerations

### Exception Filter Performance

**Confirmed by Code**: Performance considerations:

1. **Fast Execution**: Keep filters fast
2. **Logging**: Use async logging
3. **Error Tracking**: Track errors efficiently
4. **Response**: Return error response quickly
5. **Skip**: Skip when possible

## Common Mistakes

### Mistake 1: Not Implementing ExceptionFilter

**Symptom**: Filter not working

**Cause**: Not implementing ExceptionFilter interface

**Fix**:
```typescript
// Implement ExceptionFilter
@Catch(HttpException)
export class MyFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    // filter logic
  }
}
```

### Mistake 2: Not Returning Response

**Symptom**: No error response

**Cause**: Not returning error response

**Fix**:
```typescript
// Return error response
response.status(status).json(errorResponse);
```

### Mistake 3: Leaking Sensitive Info

**Symptom**: Sensitive info in error messages

**Cause**: Not sanitizing error messages

**Fix**:
```typescript
// Sanitize error messages
const message = process.env.NODE_ENV === 'production' 
  ? 'An error occurred' 
  : exception.message;
```

## Debugging Guide

### Exception Filter Debugging

**Issue**: Exception filter not working

**Investigation**:
1. Check filter registration
2. Check filter logic
3. Check exception type
4. Check response
5. Check logs

**Tools**:
- Error logs
- Filter logs
- Response logs
- Console logs

## Future Enhancements

### Logging Integration

**Status**: Partially implemented

**Proposal**: Implement logging integration:
- Log all exceptions
- Log to external service
- Error tracking
- Better debugging
- More complex

### Error Monitoring

**Status**: Not implemented

**Proposal**: Implement error monitoring:
- Sentry integration
- Error tracking
- Error alerts
- Better monitoring
- More complex

## Production Considerations

### Production Exception Filters

**Production Deployment**:
- Enable all filters
- Configure error logging
- Configure error monitoring
- Monitor error rates
- Monitor error patterns

### Exception Filter Monitoring

**Monitoring Metrics**:
- Error rate
- Error types
- Error frequency
- Error patterns
- Error impact

## Example Requests

### Exception Filter Example

**Request**:
```bash
GET /api/users/invalid
```

## Example Responses

### Exception Filter Response

**Response**:
```json
{
  "success": false,
  "error": {
    "code": 404,
    "message": "User not found"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Sequence Diagrams

### Exception Filter Flow

```
Request → Controller → Service → Exception Thrown → Exception Filter → Error Response
```

## Architecture Diagrams

### Exception Filter Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Controller/Service                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Exception Thrown                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Exception Filter                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Error Response                             │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do exception filters work in NestJS?

**Answer**: Exception filters via:
- Implement ExceptionFilter interface
- Catch specific exception types
- Transform error to standard format
- Return error response
- Can be global or local

### Q2: How do you create a custom exception filter?

**Answer**: Custom exception filter via:
- Implement ExceptionFilter interface
- Add @Catch() decorator
- Implement catch() method
- Transform error response
- Register filter

### Q3: What is the difference between exception filters and try-catch?

**Answer**: Exception filters vs try-catch:
- Exception filters: Global error handling
- try-catch: Local error handling
- Exception filters: Standardized error responses
- try-catch: Custom error handling
- Exception filters: Better for cross-cutting concerns
- try-catch: Better for specific error handling

## Exercises

### Exercise 1: Create an Exception Filter

**Task**: Create a custom exception filter.

**Steps**:
1. Implement ExceptionFilter interface
2. Add @Catch() decorator
3. Add filter logic
4. Register filter
5. Test filter

**Verification**:
- Filter created
- Logic works
- Decorator works
- Filter registered
- Tests pass

### Exercise 2: Create a Logging Exception Filter

**Task**: Create a logging exception filter.

**Steps**:
1. Implement ExceptionFilter interface
2. Add logging logic
3. Log to external service
4. Add error tracking
5. Test logging

**Verification**:
- Filter created
- Logging works
- External service works
- Error tracking works
- Tests pass

## Real Production Scenarios

### Scenario 1: Exception Filter Not Catching

**Situation**: Exception filter not catching exception

**Response**:
1. Check filter registration
2. Check exception type
3. Check filter logic
4. Fix filter
5. Test filter

### Scenario 2: Error Response Not Standard

**Situation**: Error response not standard

**Response**:
1. Check filter logic
2. Check error transformation
3. Check response format
4. Fix filter
5. Test filter

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [04-Pipes](./04-Pipes.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/10-Exception-Filters](../03-Backend/10-Exception-Filters.md) - Exception filters details
