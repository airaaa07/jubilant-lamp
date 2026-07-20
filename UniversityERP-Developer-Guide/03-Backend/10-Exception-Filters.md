# Exception Filters

## Purpose

This document explains the exception filter pattern used in the University ERP backend. It details how exception filters handle errors, implement error handling, and provide consistent error responses.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS exception filters for error handling. Understanding exception filters is critical for:
- Implementing consistent error handling
- Providing meaningful error messages
- Handling different error types
- Implementing error logging
- Debugging errors

Without understanding exception filters, developers may struggle with error handling or may provide inconsistent error responses.

## Where This Is Used

- **Onboarding**: New developers learn exception filter pattern
- **Feature Development**: Creating exception filters for error handling
- **Code Reviews**: Reviewing exception filter implementation
- **Error Handling**: Implementing error handling
- **Debugging**: Debugging errors

## Dependencies

### Exception Filter Dependencies

**Confirmed by Code**: Exception filters depend on:

- **NestJS Exception Filters**: Exception filter interface
- **HttpException**: HTTP exception class
- **Logger**: Logging service
- **ExecutionContext**: Execution context

## Internal Architecture

### Exception Filter Architecture

**Confirmed by Code**: Exception filters follow a hierarchical pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Exception Filter Chain                        │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  HTTP         │  │  Validation    │  │  Database      │
│  Exception    │  │  Exception     │  │  Exception     │
│  Filter       │  │  Filter        │  │  Filter        │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Exception Filter Definition

**Confirmed by Code**: Exception filters implement ExceptionFilter interface.

**Basic Exception Filter**:
```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const message = exception.message;

    response.status(status).json({
      success: false,
      error: {
        code: exception.name,
        message,
      },
    });
  }
}
```

**What This Does**:
- **@Catch**: Catches specific exception types
- **ExceptionFilter**: Interface for exception filter
- **catch()**: Handles exception
- **ArgumentsHost**: Provides execution context
- **Response**: Express response object

### Global Exception Filter

**Confirmed by Code**: Global exception filter handles all exceptions.

**HttpExceptionFilter**:
```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Response } from 'express';

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Internal server error';
    let code = 'INTERNAL_SERVER_ERROR';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exceptionResponse = exception.getResponse();
      
      if (typeof exceptionResponse === 'string') {
        message = exceptionResponse;
      } else if (typeof exceptionResponse === 'object') {
        message = (exceptionResponse as any).message || message;
        code = (exceptionResponse as any).code || code;
      }
    }

    response.status(status).json({
      success: false,
      error: {
        code,
        message,
        timestamp: new Date().toISOString(),
        path: request.url,
      },
    });
  }
}
```

**What This Does**:
- **@Catch()**: Catches all exceptions
- **HttpException Handling**: Handles HTTP exceptions
- **Default Error**: Handles unknown exceptions
- **Standard Format**: Returns standard error format
- **Timestamp**: Adds timestamp to error

**Usage in main.ts**:
```typescript
app.useGlobalFilters(new HttpExceptionFilter());
```

### Validation Exception Filter

**Status**: Not implemented

**Proposal**: Validation exception filter for validation errors.

**ValidationExceptionFilter**:
```typescript
@Catch(BadRequestException)
export class ValidationExceptionFilter implements ExceptionFilter {
  catch(exception: BadRequestException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const exceptionResponse = exception.getResponse();

    if (typeof exceptionResponse === 'object' && 'message' in exceptionResponse) {
      const message = (exceptionResponse as any).message;
      
      if (Array.isArray(message)) {
        return response.status(exception.getStatus()).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Validation failed',
            details: message,
          },
        });
      }
    }

    response.status(exception.getStatus()).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: exception.message,
      },
    });
  }
}
```

### Database Exception Filter

**Status**: Not implemented

**Proposal**: Database exception filter for database errors.

**DatabaseExceptionFilter**:
```typescript
@Catch(Prisma.PrismaClientKnownRequestError)
export class DatabaseExceptionFilter implements ExceptionFilter {
  catch(exception: Prisma.PrismaClientKnownRequestError, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    let message = 'Database error';
    let code = 'DATABASE_ERROR';

    switch (exception.code) {
      case 'P2002':
        message = 'Unique constraint violation';
        code = 'DUPLICATE_ENTRY';
        break;
      case 'P2025':
        message = 'Record not found';
        code = 'NOT_FOUND';
        break;
      default:
        message = exception.message;
    }

    response.status(HttpStatus.BAD_REQUEST).json({
      success: false,
      error: {
        code,
        message,
      },
    });
  }
}
```

## Database Interactions

### Exception Filter-Database Flow

**Confirmed by Code**: Exception filters handle database errors.

**Flow**:
```
Database Error → Exception Filter → Error Response
```

## Redis Interactions

### Exception Filter-Redis Flow

**Confirmed by Code**: Exception filters handle Redis errors.

**Flow**:
```
Redis Error → Exception Filter → Error Response
```

## Queue Interactions

### Exception Filter-Queue Flow

**Confirmed by Code**: Exception filters handle queue errors.

**Flow**:
```
Queue Error → Exception Filter → Error Response
```

## Worker Interactions

### Exception Filter-Worker Flow

**Confirmed by Code**: Workers may have their own exception handling.

**Flow**:
```
Worker Error → Worker Exception Handler → Error Response
```

## Business Rules

### Exception Filter Rules

**Confirmed by Code**: Exception filters follow these rules:

1. **Consistent Format**: Return consistent error format
2. **Meaningful Messages**: Provide meaningful error messages
3. **Error Codes**: Use error codes for programmatic handling
4. **Logging**: Log all errors
5. **Security**: Don't expose sensitive information

### Error Response Rules

**Confirmed by Code**: Error responses follow these rules:

1. **success**: Always false for errors
2. **error**: Error object with code and message
3. **timestamp**: Timestamp of error
4. **path**: Path where error occurred
5. **details**: Additional error details if applicable

## Security

### Exception Filter Security

**Confirmed by Code**: Security considerations for exception filters:

1. **No Sensitive Data**: Don't expose sensitive data in errors
2. **Sanitization**: Sanitize error messages
3. **Stack Traces**: Don't expose stack traces in production
4. **Database Errors**: Don't expose database structure
5. **Internal Errors**: Use generic messages for internal errors

## Performance Considerations

### Exception Filter Performance

**Confirmed by Code**: Performance considerations for exception filters:

1. **Fast Execution**: Keep exception filters fast
2. **Minimal Overhead**: Minimize overhead
3. **Logging**: Use async logging
4. **Error Tracking**: Track error metrics
5. **Monitoring**: Monitor error rates

## Common Mistakes

### Mistake 1: Not Handling All Exceptions

**Symptom**: Unhandled exceptions cause 500 errors

**Cause**: Not catching all exception types

**Fix**:
```typescript
// Catch all exceptions
@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // Handle all exceptions
  }
}
```

### Mistake 2: Exposing Sensitive Data

**Symptom**: Sensitive data in error responses

**Cause**: Exposing sensitive data in errors

**Fix**:
```typescript
// Sanitize error messages
const message = process.env.NODE_ENV === 'production' 
  ? 'Internal server error' 
  : exception.message;
```

### Mistake 3: Not Logging Errors

**Symptom**: No error logs

**Cause**: Not logging errors

**Fix**:
```typescript
// Add logging
this.logger.error(
  `${request.method} ${request.url} - ${status} - ${message}`,
  exception.stack,
);
```

## Debugging Guide

### Exception Filter Debugging

**Issue**: Exception filter not working

**Investigation**:
1. Check exception filter registration
2. Check exception type
3. Check error handling logic
4. Check response format
5. Check logs

**Tools**:
- Exception filter logs
- Application logs
- Error tracking
- Stack traces

## Future Enhancements

### Error Tracking

**Status**: Not implemented

**Proposal**: Implement error tracking:
- Sentry integration
- Error aggregation
- Error alerting
- Error analytics
- Error reporting

### Custom Error Classes

**Status**: Not implemented

**Proposal**: Implement custom error classes:
- Custom exception classes
- Business-specific errors
- Better error categorization
- Easier error handling
- Better error messages

## Production Considerations

### Production Exception Filters

**Production Deployment**:
- Enable all exception filters
- Use generic error messages
- Enable error logging
- Enable error tracking
- Monitor error rates

### Exception Filter Monitoring

**Monitoring Metrics**:
- Error rate
- Error types
- Error frequency
- Error response time
- Error trends

## Example Requests

### Exception Filter Example

**Request**:
```bash
GET /api/users/invalid-id
```

**Response**:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "timestamp": "2024-01-01T00:00:00Z",
    "path": "/api/users/invalid-id"
  }
}
```

## Example Responses

### Error Response

**Response**: Error response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

## Sequence Diagrams

### Exception Flow

```
Request → Controller → Service → Error
                              ↓
                        Exception Thrown
                              ↓
                        Exception Filter
                              ↓
                        Error Response
```

## Architecture Diagrams

### Exception Filter Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Error Occurred                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Exception Filter                              │
│              (Catch Exception)                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Error Logging                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Error Response                                │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the role of exception filters in NestJS?

**Answer**: Exception filters role:
- Catch and handle exceptions
- Provide consistent error responses
- Log errors
- Transform exceptions to HTTP responses
- Implement error handling logic

### Q2: How do you create a custom exception filter?

**Answer**: Custom exception filter via:
- Implement ExceptionFilter interface
- Use @Catch decorator to specify exception types
- Define catch method
- Access execution context
- Return error response

### Q3: How do you handle different exception types?

**Answer**: Different exception types via:
- Multiple exception filters for different types
- @Catch decorator with multiple exception types
- Type checking in catch method
- Switch statement for different error codes
- Specific error handling per type

## Exercises

### Exercise 1: Create a Global Exception Filter

**Task**: Create a global exception filter.

**Steps**:
1. Implement ExceptionFilter interface
2. Handle all exception types
3. Return standard error format
4. Add error logging
5. Apply globally

**Verification**:
- Exception filter created
- All exceptions handled
- Error format consistent
- Logging works
- Tests pass

### Exercise 2: Create a Validation Exception Filter

**Task**: Create a validation exception filter.

**Steps**:
1. Implement ExceptionFilter interface
2. Catch BadRequestException
3. Parse validation errors
4. Return detailed error response
5. Test filter

**Verification**:
- Exception filter created
- Validation errors handled
- Error details returned
- Tests pass

## Real Production Scenarios

### Scenario 1: Error Not Caught

**Situation**: Exception not caught by filter

**Response**:
1. Check exception type
2. Check @Catch decorator
3. Add exception type to filter
4. Test exception handling
5. Monitor errors

### Scenario 2: Sensitive Data Exposed

**Situation**: Sensitive data in error response

**Response**:
1. Identify sensitive data
2. Sanitize error messages
3. Use generic messages in production
4. Test error responses
5. Monitor error logs

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [09-Middleware](./09-Middleware.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
- [19-Security](../19-Security/README.md) - Security guide
