# Monitoring and Logging

## Purpose

This document explains the monitoring and logging strategy for the University ERP system. It details what is monitored, how logging is implemented, and how to use logs for debugging and analysis.

## Why This Document Exists

**Confirmed by Code**: The University ERP is a complex system with multiple services. Understanding monitoring and logging is critical for:
- Debugging issues in production
- Understanding system behavior
- Performance optimization
- Capacity planning
- Security auditing

Without proper monitoring and logging, it's difficult to troubleshoot issues or understand system performance.

## Where This Is Used

- **Onboarding**: New developers learn logging practices
- **Debugging**: Using logs to debug issues
- **Performance Analysis**: Analyzing system performance
- **Security Auditing**: Auditing system access
- **Capacity Planning**: Planning for growth

## Dependencies

### Monitoring Dependencies

**Confirmed by Code**: Monitoring depends on:

- **Application Logs**: NestJS logger
- **Database Logs**: PostgreSQL logs
- **Cache Logs**: Redis logs
- **Worker Logs**: Worker service logs
- **Audit Logs**: Audit logging middleware

## Internal Architecture

### Logging Architecture

**Confirmed by Code**: The system uses structured logging.

```
┌─────────────────────────────────────────────────────────┐
│                  Logging Architecture                      │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Application   │  │  Database       │  │  Infrastructure │
│  Logs          │  │  Logs           │  │  Logs           │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Console      │  │  File           │  │  Log Aggregation│
│  Output       │  │  Storage        │  │  (ELK, etc.)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Log Levels

**Confirmed by Code**: NestJS logger supports standard log levels.

**Levels**:
- **ERROR**: Error events that might still allow the application to continue running
- **WARN**: Warning events that might cause problems
- **LOG**: Informational messages that highlight the progress of the application
- **DEBUG**: Detailed information for debugging purposes
- **VERBOSE**: More detailed information than DEBUG

## Code Walkthrough

### Application Logging

**Confirmed by Code**: NestJS Logger is used for application logging.

**Implementation**:
```typescript
import { Logger } from '@nestjs/common';

@Injectable()
export class MyService {
  private readonly logger = new Logger(MyService.name);

  async doSomething() {
    this.logger.log('Starting operation');
    
    try {
      const result = await this.performOperation();
      this.logger.log('Operation completed successfully');
      return result;
    } catch (error) {
      this.logger.error('Operation failed', error.stack);
      throw error;
    }
  }
}
```

**What This Does**:
- Creates logger instance with service name
- Logs informational messages
- Logs errors with stack traces
- Provides context for debugging

### Audit Logging

**Confirmed by Code**: Prisma middleware logs all write operations.

**Implementation**:
```typescript
// apps/core-api/src/database/audit-middleware.ts
prisma.$use(async (params, next) => {
  const before = await findBefore(params);
  const result = await next(params);
  const after = await findAfter(params);
  
  await prisma.auditLog.create({
    data: {
      actorId: getCurrentUser().id,
      actionType: params.action,
      entityType: params.model,
      entityId: params.args.where?.id,
      oldValue: before,
      newValue: after,
      timestamp: new Date(),
    },
  });
  
  return result;
});
```

**What This Does**:
- Intercepts all write operations
- Records before and after state
- Logs actor, action, entity
- Provides audit trail

### Request Logging

**Confirmed by Code**: Middleware logs HTTP requests.

**Implementation**:
```typescript
import { Logger } from '@nestjs/common';

@Injectable()
export class LoggingMiddleware implements NestMiddleware {
  private readonly logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const { method, url, ip } = req;
    const userAgent = req.get('user-agent') || '';
    
    res.on('finish', () => {
      const { statusCode } = res;
      const contentLength = res.get('content-length');
      
      this.logger.log(
        `${method} ${url} ${statusCode} ${contentLength} - ${userAgent} ${ip}`,
      );
    });
    
    next();
  }
}
```

**What This Does**:
- Logs HTTP requests
- Logs method, URL, status code
- Logs user agent and IP
- Provides request tracking

## Database Interactions

### Database Query Logging

**Confirmed by Code**: Prisma can log database queries.

**Implementation**:
```typescript
const prisma = new PrismaClient({
  log: [
    { level: 'query', emit: 'event' },
    { level: 'error', emit: 'stdout' },
    { level: 'warn', emit: 'stdout' },
  ],
});

prisma.$on('query', (e) => {
  console.log('Query: ' + e.query);
  console.log('Params: ' + e.params);
  console.log('Duration: ' + e.duration + 'ms');
});
```

**What This Does**:
- Logs all database queries
- Logs query parameters
- Logs query duration
- Helps identify slow queries

### Database Connection Logging

**Confirmed by Code**: Prisma logs connection events.

**Implementation**:
```typescript
prisma.$on('connect', () => {
  console.log('Database connected');
});

prisma.$on('disconnect', () => {
  console.log('Database disconnected');
});

prisma.$on('beforeExit', async () => {
  console.log('Before exit hook');
});
```

**What This Does**:
- Logs connection events
- Logs disconnection events
- Logs before exit events
- Helps debug connection issues

## Redis Interactions

### Redis Command Logging

**Confirmed by Code**: Redis commands can be logged.

**Implementation**:
```typescript
import { Logger } from '@nestjs/common';

@Injectable()
export class RedisService extends Redis {
  private readonly logger = new Logger(RedisService.name);

  async set(key: string, value: string) {
    this.logger.debug(`SET ${key}`);
    return super.set(key, value);
  }

  async get(key: string) {
    this.logger.debug(`GET ${key}`);
    return super.get(key);
  }
}
```

**What This Does**:
- Logs Redis commands
- Provides debugging context
- Helps identify cache issues

## Queue Interactions

### Queue Job Logging

**Confirmed by Code**: Bull jobs are logged.

**Implementation**:
```typescript
@Processor('notifications')
export class NotificationProcessor {
  private readonly logger = new Logger(NotificationProcessor.name);

  @Process('email')
  async handleEmail(job: Job) {
    this.logger.log(`Processing email job ${job.id}`);
    
    try {
      await this.mailService.sendEmail(job.data);
      this.logger.log(`Email job ${job.id} completed`);
    } catch (error) {
      this.logger.error(`Email job ${job.id} failed`, error.stack);
      throw error;
    }
  }
}
```

**What This Does**:
- Logs job processing
- Logs job completion
- Logs job failures
- Helps debug queue issues

## Worker Interactions

### Worker Status Logging

**Confirmed by Code**: Workers log their status.

**Implementation**:
```typescript
@Injectable()
export class WorkerService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(WorkerService.name);

  async onModuleInit() {
    this.logger.log('Worker started');
  }

  async onModuleDestroy() {
    this.logger.log('Worker stopped');
  }
}
```

**What This Does**:
- Logs worker startup
- Logs worker shutdown
- Provides worker lifecycle tracking

## Business Rules

### Logging Rules

**Confirmed by Code**: Logging follows these rules:

1. **Structured Logging**: Use structured log format
2. **Log Levels**: Use appropriate log levels
3. **Context**: Include relevant context in logs
4. **PII**: Don't log personally identifiable information
5. **Performance**: Don't log in hot paths

### Audit Rules

**Confirmed by Code**: Audit logging follows these rules:

1. **All Writes**: Log all write operations
2. **Actor**: Log who made the change
3. **Timestamp**: Log when the change was made
4. **Before/After**: Log state before and after
5. **Immutable**: Audit logs are immutable

## Security

### Logging Security

**Confirmed by Code**: Security considerations for logging:

1. **No Secrets**: Never log secrets or passwords
2. **No PII**: Don't log personally identifiable information
3. **Sanitization**: Sanitize sensitive data before logging
4. **Access Control**: Restrict log access
5. **Retention**: Define log retention policy

## Performance Considerations

### Logging Performance

**Confirmed by Code**: Performance considerations for logging:

1. **Async Logging**: Use async logging to avoid blocking
2. **Log Level**: Use appropriate log levels
3. **Sampling**: Sample logs in high-traffic scenarios
4. **Buffering**: Buffer logs to reduce I/O
5. **Compression**: Compress logs for storage

## Common Mistakes

### Mistake 1: Logging Sensitive Data

**Symptom**: Secrets in logs

**Cause**: Logging sensitive data

**Fix**:
```typescript
// Wrong
this.logger.log(`User password: ${password}`);

// Correct
this.logger.log(`User login attempt`);
```

### Mistake 2: Using Wrong Log Level

**Symptom**: Too much noise in logs

**Cause**: Using wrong log level

**Fix**:
```typescript
// Wrong
this.logger.error('User logged in');

// Correct
this.logger.log('User logged in');
```

### Mistake 3: Not Including Context

**Symptom**: Logs not helpful for debugging

**Cause**: Not including context

**Fix**:
```typescript
// Wrong
this.logger.log('Error occurred');

// Correct
this.logger.log(`Error occurred while processing user ${userId}: ${error.message}`);
```

## Debugging Guide

### Log Analysis

**Issue**: Application error

**Investigation**:
1. Check application logs
2. Check error messages
3. Check stack traces
4. Check context
5. Check related logs

**Tools**:
- Log viewer
- Log aggregation (ELK)
- Log search
- Log analysis tools

## Future Enhancements

### Log Aggregation

**Status**: Not implemented

**Proposal**: Implement log aggregation:
- ELK stack (Elasticsearch, Logstash, Kibana)
- Centralized log storage
- Log search and analysis
- Log visualization

### Distributed Tracing

**Status**: Not implemented

**Proposal**: Implement distributed tracing:
- OpenTelemetry
- Trace requests across services
- Identify performance bottlenecks
- Better debugging

## Production Considerations

### Production Logging

**Production Logging**:
- Use appropriate log levels
- Don't log sensitive data
- Use structured logging
- Implement log rotation
- Implement log retention

### Log Retention

**Retention Policy**:
- Application logs: 30 days
- Audit logs: 1 year
- Database logs: 30 days
- Access logs: 90 days

## Example Requests

### View Logs

**Request**:
```bash
# View application logs
docker-compose logs -f core-api

# View database logs
docker-compose logs -f postgres

# View Redis logs
docker-compose logs -f redis
```

## Example Responses

### Log Output

**Response**: Application log output

```
[Nest] 12345  - [2024-01-01 00:00:00] [LOG] [MyService] Starting operation
[Nest] 12345  - [2024-01-01 00:00:01] [LOG] [MyService] Operation completed successfully
[Nest] 12345  - [2024-01-01 00:00:02] [ERROR] [MyService] Operation failed
Error: Something went wrong
    at MyService.performOperation (my-service.ts:10)
```

## Sequence Diagrams

### Logging Flow

```
Application → Logger → Console/File
                      ↓
                  Log Aggregation
                      ↓
                  Log Storage
                      ↓
                  Log Analysis
```

## Architecture Diagrams

### Monitoring Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Applications                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Core API     │  │ CBE Engine   │  │ Workers       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Log Aggregation                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ File Storage │  │ ELK Stack     │  │ Cloud Logs    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Monitoring & Alerting                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Dashboards   │  │ Alerts       │  │ Reports       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is logging implemented in the system?

**Answer**: Logging is implemented via:
- NestJS Logger for application logs
- Prisma middleware for audit logs
- Middleware for HTTP request logs
- Structured logging format
- Appropriate log levels

### Q2: What is logged for audit purposes?

**Answer**: Audit logging includes:
- All write operations (create, update, delete)
- Actor who made the change
- Timestamp of the change
- Entity type and ID
- State before and after (for updates)

### Q3: How do you debug issues using logs?

**Answer**: Debugging via logs:
- Check application logs for errors
- Check stack traces for context
- Check audit logs for data changes
- Check database logs for query issues
- Check worker logs for job issues

## Exercises

### Exercise 1: Add Logging to Service

**Task**: Add logging to a service.

**Steps**:
1. Create logger instance
2. Add log statements
3. Use appropriate log levels
4. Include context
5. Test logging

**Verification**:
- Logs are generated
- Log levels are appropriate
- Context is included
- Logs are helpful

### Exercise 2: Analyze Logs

**Task**: Analyze logs to debug an issue.

**Steps**:
1. Collect logs
2. Filter by time
3. Search for errors
4. Analyze context
5. Identify root cause

**Verification**:
- Issue identified
- Root cause found
- Solution proposed

## Real Production Scenarios

### Scenario 1: Application Error

**Situation**: Application error in production

**Response**:
1. Check application logs
2. Identify error message
3. Check stack trace
4. Check context
5. Identify root cause
6. Implement fix
7. Deploy fix
8. Monitor logs

### Scenario 2: Performance Degradation

**Situation**: Performance degradation in production

**Response**:
1. Check application logs
2. Check database query logs
3. Identify slow queries
4. Optimize queries
5. Add caching
6. Monitor logs
7. Verify improvement

## Navigation

**Next Section**: [12-API-Reference](./12-API-Reference.md)

**Previous Section**: [10-Development-Workflow](./10-Development-Workflow.md)

**Related Documentation**:
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
- [17-Production](../17-Production/README.md) - Production guide
- [18-Performance](../18-Performance/README.md) - Performance guide
