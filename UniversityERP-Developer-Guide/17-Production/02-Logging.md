# Logging

## Purpose

This document explains logging in the University ERP system. It details how logging is implemented, log levels, log aggregation, and best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP requires effective logging. Understanding logging is critical for:
- Debugging issues
- Auditing actions
- Monitoring system health
- Troubleshooting problems
- Compliance requirements

Without understanding logging, developers may struggle with debugging or may not have adequate visibility into system behavior.

## Where This Is Used

- **Onboarding**: New developers learn logging
- **Feature Development**: Adding logging to features
- **Code Reviews**: Reviewing logging approaches
- **Production**: Monitoring production logs
- **Troubleshooting**: Troubleshooting issues

## Dependencies

### Logging Dependencies

**Confirmed by Code**: Logging depends on:

- **Winston**: Logging library
- **ELK Stack**: Log aggregation
- **Log Levels**: Appropriate log levels
- **Structured Logging**: Structured log format
- **Log Rotation**: Log rotation policies

## Internal Architecture

### Logging Architecture

**Confirmed by Code**: Logging follows centralized architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Winston Logger                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Log Transport                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Log Aggregation (ELK)                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Log Analysis                                   │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Winston Logger

**Confirmed by Code**: Winston logger for logging.

**Logger Service**:
```typescript
import { Injectable, LoggerService as NestLoggerService } from '@nestjs/common';
import * as winston from 'winston';

@Injectable()
export class LoggerService implements NestLoggerService {
  private logger: winston.Logger;

  constructor() {
    this.logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json(),
      ),
      transports: [
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple(),
          ),
        }),
        new winston.transports.File({
          filename: 'logs/error.log',
          level: 'error',
        }),
        new winston.transports.File({
          filename: 'logs/combined.log',
        }),
      ],
    });
  }

  log(message: any, context?: string) {
    this.logger.info(message, { context });
  }

  error(message: any, trace?: string, context?: string) {
    this.logger.error(message, { context, trace });
  }

  warn(message: any, context?: string) {
    this.logger.warn(message, { context });
  }

  debug(message: any, context?: string) {
    this.logger.debug(message, { context });
  }

  verbose(message: any, context?: string) {
    this.logger.verbose(message, { context });
  }
}
```

**What This Does**:
- **winston.createLogger**: Create Winston logger
- **format**: JSON format for structured logging
- **transports**: Console and file transports
- **log**: Info level logging
- **error**: Error level logging

### Structured Logging

**Confirmed by Code**: Structured logging for better analysis.

**Structured Logging**:
```typescript
this.logger.info('User logged in', {
  userId: user.id,
  email: user.email,
  timestamp: new Date().toISOString(),
  ip: req.ip,
  userAgent: req.headers['user-agent'],
});
```

**What This Does**:
- **Structured Data**: Log structured data
- **Context**: Include relevant context
- **Timestamp**: Include timestamp
- **Metadata**: Include metadata

### Log Levels

**Confirmed by Code**: Log levels for different severity.

**Log Levels**:
```typescript
// Error: Critical errors
this.logger.error('Database connection failed', { error: error.message });

// Warn: Warning messages
this.logger.warn('Cache miss', { key: cacheKey });

// Info: Informational messages
this.logger.info('User created', { userId: user.id });

// Debug: Debug messages
this.logger.debug('Processing request', { requestId });

// Verbose: Verbose messages
this.logger.verbose('Cache hit', { key: cacheKey });
```

**What This Does**:
- **error**: Critical errors
- **warn**: Warning messages
- **info**: Informational messages
- **debug**: Debug messages
- **verbose**: Verbose messages

## Database Interactions

### Logging-Database Flow

**Confirmed by Code**: Database queries logged.

**Flow**:
```
Database Query → Logger → Log Aggregation
```

## Redis Interactions

### Logging-Redis Flow

**Confirmed by Code**: Redis operations logged.

**Flow**:
```
Redis Operation → Logger → Log Aggregation
```

## Queue Interactions

### Logging-Queue Flow

**Confirmed by Code**: Queue operations logged.

**Flow**:
```
Queue Operation → Logger → Log Aggregation
```

## Worker Interactions

### Logging-Worker Flow

**Confirmed by Code**: Worker operations logged.

**Flow**:
```
Worker Operation → Logger → Log Aggregation
```

## Business Rules

### Logging Rules

**Confirmed by Code**: Logging follows these rules:

1. **Structured**: Use structured logging
2. **Levels**: Use appropriate log levels
3. **Context**: Include relevant context
4. **Sensitive Data**: Don't log sensitive data
5. **Performance**: Consider performance impact

### Log Level Rules

**Confirmed by Code**: Log level rules:

1. **Error**: Critical errors only
2. **Warn**: Warnings for potential issues
3. **Info**: Important informational messages
4. **Debug**: Debug information
5. **Verbose**: Detailed information

## Security

### Logging Security

**Confirmed by Code**: Security considerations for logging:

1. **Sensitive Data**: Don't log sensitive data
2. **PII**: Don't log PII
3. **Passwords**: Don't log passwords
3. **Tokens**: Don't log tokens
4. **Access Control**: Restrict log access

## Performance Considerations

### Logging Performance

**Confirmed by Code**: Performance considerations:

1. **Async Logging**: Use async logging
2. **Log Level**: Use appropriate log level
3. **Sampling**: Sample logs in high traffic
4. **Buffering**: Buffer logs
5. **Optimization**: Optimize logging code

## Common Mistakes

### Mistake 1: Logging Sensitive Data

**Symptom**: Security vulnerability

**Cause**: Logging sensitive data

**Fix**:
```typescript
// Don't log sensitive data
this.logger.info('User logged in', { userId: user.id }); // OK
this.logger.info('User logged in', { password: user.password }); // NOT OK
```

### Mistake 2: Using Wrong Log Level

**Symptom**: Too many logs

**Cause**: Using wrong log level

**Fix**:
```typescript
// Use appropriate log level
this.logger.error('Critical error'); // OK
this.logger.info('Debug info'); // NOT OK - use debug
```

### Mistake 3: Not Using Structured Logging

**Symptom**: Hard to analyze logs

**Cause**: Not using structured logging

**Fix**:
```typescript
// Use structured logging
this.logger.info('User logged in', { userId: user.id }); // OK
this.logger.info('User logged in'); // NOT OK - no context
```

## Debugging Guide

### Logging Debugging

**Issue**: Logs not appearing

**Investigation**:
1. Check log level
2. Check log transport
3. Check log file
4. Check log aggregation
5. Check permissions

**Tools**:
- Log files
- ELK Stack
- Log aggregation tools
- Console logs

## Future Enhancements

### Log Aggregation

**Status**: Not implemented

**Proposal**: Implement log aggregation:
- ELK Stack integration
- Centralized logging
- Better log analysis
- More complex
- Better for production

### Log Sampling

**Status**: Not implemented

**Proposal**: Implement log sampling:
- Sample logs in high traffic
- Reduce log volume
- Better performance
- More complex
- Better for production

## Production Considerations

### Production Logging

**Production Deployment**:
- Use structured logging
- Use appropriate log levels
- Don't log sensitive data
- Enable log aggregation
- Monitor log volume

### Logging Monitoring

**Monitoring Metrics**:
- Log volume
- Error log rate
- Log level distribution
- Log aggregation lag
- Log storage usage

## Example Requests

### Logging Example

**Log Info**:
```typescript
this.logger.info('User created', { userId: user.id });
```

**Log Error**:
```typescript
this.logger.error('Database error', { error: error.message });
```

## Example Responses

### Logging Response

**Response**: Log output

```json
{
  "level": "info",
  "message": "User created",
  "context": "UsersService",
  "userId": "user-id",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Sequence Diagrams

### Logging Flow

```
Application → Logger → Log Transport → Log Aggregation → Analysis
```

## Architecture Diagrams

### Logging Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Winston Logger                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Log Transport                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Log Aggregation (ELK)                          │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is logging implemented?

**Answer**: Logging via:
- Winston for logging
- Structured logging
- Multiple log levels
- Multiple transports
- Log aggregation

### Q2: What log levels do you use?

**Answer**: Log levels via:
- Error: Critical errors
- Warn: Warnings
- Info: Important information
- Debug: Debug information
- Verbose: Detailed information

### Q3: How do you handle sensitive data in logs?

**Answer**: Sensitive data handling via:
- Don't log sensitive data
- Sanitize data before logging
- Use log masking
- Configure log filters
- Audit log access

## Exercises

### Exercise 1: Add Logging

**Task**: Add logging to a service.

**Steps**:
1. Inject LoggerService
2. Add log statements
3. Use appropriate log levels
4. Add context to logs
5. Test logging

**Verification**:
- Logging added
- Log levels correct
- Context added
- Logs visible
- Tests pass

### Exercise 2: Implement Structured Logging

**Task**: Implement structured logging.

**Steps**:
1. Use structured logging format
2. Add relevant context
3. Add metadata
4. Test structured logs
5. Verify log analysis

**Verification**:
- Structured logging used
- Context added
- Metadata added
- Logs analyzable
- Tests pass

## Real Production Scenarios

### Scenario 1: High Log Volume

**Situation**: High log volume

**Response**:
1. Check log level
2. Implement log sampling
3. Optimize logging
4. Monitor log volume
5. Adjust log level

### Scenario 2: Sensitive Data in Logs

**Situation**: Sensitive data in logs

**Response**:
1. Identify sensitive data
2. Implement log masking
3. Sanitize logs
4. Audit logs
5. Fix logging

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [01-Monitoring](./01-Monitoring.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [16-Debugging](../16-Debugging/README.md) - Debugging details
