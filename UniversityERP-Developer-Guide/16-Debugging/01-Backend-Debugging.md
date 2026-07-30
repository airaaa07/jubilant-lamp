# Backend Debugging

## Purpose

This document explains backend debugging in the University ERP system. It details how to debug NestJS applications, common backend issues, and debugging techniques.

## Why This Document Exists

**Confirmed by Code**: Backend debugging is essential for troubleshooting. Understanding backend debugging is critical for:
- Debugging NestJS applications
- Troubleshooting API issues
- Debugging database queries
- Debugging authentication/authorization
- Debugging workflow issues

Without understanding backend debugging, developers may struggle with backend issues or may take longer to fix them.

## Where This Is Used

- **Onboarding**: New developers learn backend debugging
- **Feature Development**: Debugging backend features
- **Code Reviews**: Reviewing debugging approaches
- **Troubleshooting**: Troubleshooting backend issues
- **Bug Fixes**: Fixing backend bugs

## Dependencies

### Backend Debugging Dependencies

**Confirmed by Code**: Backend debugging depends on:

- **VS Code Debugger**: IDE debugger
- **NestJS Debugger**: NestJS debug mode
- **Prisma Studio**: Database debugger
- **Postman**: API testing
- **Console Logs**: Logging

## Internal Architecture

### Backend Debugging Architecture

**Confirmed by Code**: Backend debugging follows systematic approach.

```
┌─────────────────────────────────────────────────────────┐
│              Issue Identified                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Check Logs                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Use Debugger                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Identify Root Cause                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Fix Issue                                      │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### NestJS Debugger Configuration

**Confirmed by Code**: NestJS debugger configuration.

**launch.json**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch NestJS",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start:debug"],
      "console": "integratedTerminal",
      "restart": true,
      "protocol": "inspector",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to NestJS",
      "port": 9229,
      "restart": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

**What This Does**:
- **launch**: Launch NestJS in debug mode
- **attach**: Attach to running NestJS
- **port**: Debug port (9229)
- **skipFiles**: Skip internal Node.js files

### Debugging Controllers

**Confirmed by Code**: Debugging controllers using breakpoints.

**Controller Debugging**:
```typescript
@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    debugger; // Breakpoint
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    console.log('Finding user:', id); // Log
    return this.usersService.findOne(id);
  }
}
```

**What This Does**:
- **debugger**: Breakpoint for debugger
- **console.log**: Log for debugging

### Debugging Services

**Confirmed by Code**: Debugging services using breakpoints.

**Service Debugging**:
```typescript
@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    console.log('Fetching all users'); // Log
    const users = await this.prisma.user.findMany();
    console.log('Found users:', users.length); // Log
    return users;
  }

  async findOne(id: string) {
    debugger; // Breakpoint
    const user = await this.prisma.user.findUnique({
      where: { id },
    });
    return user;
  }
}
```

**What This Does**:
- **console.log**: Log for debugging
- **debugger**: Breakpoint for debugger

## Database Interactions

### Backend Debugging-Database Flow

**Confirmed by Code**: Debugging database queries.

**Flow**:
```
Debugging → Prisma Studio → Database → Query Results
```

## Redis Interactions

### Backend Debugging-Redis Flow

**Confirmed by Code**: Debugging Redis using logs.

**Redis Debugging**:
```typescript
async get(key: string) {
  console.log('Getting key:', key); // Log
  const value = await this.redis.get(key);
  console.log('Value:', value); // Log
  return value;
}
```

**What This Does**:
- **console.log**: Log Redis operations

## Queue Interactions

### Backend Debugging-Queue Flow

**Confirmed by Code**: Debugging queues using Bull Board.

**Bull Board**:
```typescript
import { BullAdapter } from '@bull-board/api/bullAdapter';
import { BullBoard } from '@bull-board/nestjs';

@Module({
  imports: [
    BullBoardModule.forFeature({
      name: 'notifications',
      adapter: BullAdapter,
    }),
  ],
})
export class AppModule {}
```

**What This Does**:
- **Bull Board**: Register queue for debugging

## Worker Interactions

### Backend Debugging-Worker Flow

**Confirmed by Code**: Debugging workers using logs.

**Worker Debugging**:
```typescript
@Process('send-email')
async handleSendEmail(job: Job) {
  console.log(`Processing job ${job.id}`); // Log
  console.log(`Job data:`, job.data); // Log
  // ... processing
  console.log(`Job ${job.id} completed`); // Log
}
```

**What This Does**:
- **console.log**: Log job progress

## Business Rules

### Backend Debugging Rules

**Confirmed by Code**: Backend debugging follows these rules:

1. **Logs**: Use logs for debugging
2. **Debugger**: Use debugger for complex issues
3. **Breakpoints**: Use breakpoints for step-through
4. **Prisma Studio**: Use for database debugging
5. **Postman**: Use for API testing

### Logging Rules

**Confirmed by Code**: Logging rules:

1. **Structured Logging**: Use structured logging
2. **Log Levels**: Use appropriate log levels
3. **Context**: Include context in logs
4. **Sensitive Data**: Don't log sensitive data
5. **Performance**: Consider performance impact

## Security

### Backend Debugging Security

**Confirmed by Code**: Security considerations for backend debugging:

1. **Sensitive Data**: Don't log sensitive data
2. **Debug Mode**: Disable debug mode in production
3. **Access Control**: Restrict debugging access
4. **Logs**: Secure log storage
5. **Tools**: Use secure debugging tools

## Performance Considerations

### Backend Debugging Performance

**Confirmed by Code**: Performance considerations:

1. **Logging**: Minimize logging overhead
2. **Debug Mode**: Disable in production
3. **Profiling**: Use profiling tools
4. **Monitoring**: Monitor debugging impact
5. **Optimization**: Optimize debugging code

## Common Mistakes

### Mistake 1: Not Using Debugger

**Symptom**: Slow debugging

**Cause**: Not using debugger

**Fix**:
```typescript
// Use debugger instead of console.log
debugger;
// or use breakpoints in IDE
```

### Mistake 2: Logging Sensitive Data

**Symptom**: Security vulnerability

**Cause**: Logging sensitive data

**Fix**:
```typescript
// Don't log sensitive data
console.log('User:', user.id); // OK
console.log('Password:', user.password); // NOT OK
```

### Mistake 3: Not Checking Logs

**Symptom**: Issue not identified

**Cause**: Not checking logs

**Fix**:
```typescript
// Check logs first
console.log('Debug info:', data);
```

## Debugging Guide

### Backend Debugging

**Issue**: Backend not working

**Investigation**:
1. Check logs
2. Use debugger
3. Check database connection
4. Check environment variables
5. Check dependencies

**Tools**:
- VS Code debugger
- Console logs
- Prisma Studio
- Postman

### API Debugging

**Issue**: API not working

**Investigation**:
1. Check logs
2. Use Postman
3. Check request/response
4. Check authentication
5. Check authorization

**Tools**:
- Postman
- Console logs
- Network tab
- VS Code debugger

### Database Debugging

**Issue**: Database not working

**Investigation**:
1. Check connection
2. Check queries
3. Check schema
4. Check data
5. Check constraints

**Tools**:
- Prisma Studio
- psql
- Database logs
- Query analyzer

## Future Enhancements

### Distributed Tracing

**Status**: Not implemented

**Proposal**: Implement distributed tracing:
- OpenTelemetry integration
- Trace requests across services
- Better debugging
- More complex
- Better for production

### Error Tracking

**Status**: Not implemented

**Proposal**: Implement error tracking:
- Sentry integration
- Error aggregation
- Better error visibility
- More complex
- Better for production

## Production Considerations

### Production Backend Debugging

**Production Deployment**:
- Disable debug mode
- Use structured logging
- Use error tracking
- Monitor logs
- Secure debugging access

### Backend Debugging Monitoring

**Monitoring Metrics**:
- Error rate
- Log volume
- Debug mode usage
- Tool usage
- Issue resolution time

## Example Requests

### Backend Debugging Example

**Debug Backend**:
```bash
npm run start:debug
```

**Debug Database**:
```bash
npx prisma studio
```

## Example Responses

### Backend Debugging Response

**Response**: Debugger attached

```bash
Debugger listening on ws://127.0.0.1:9229
```

## Sequence Diagrams

### Backend Debugging Flow

```
Issue → Check Logs → Use Debugger → Identify Root Cause → Fix → Test
```

## Architecture Diagrams

### Backend Debugging Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Issue Identified                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Check Logs                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Use Debugger                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Identify Root Cause                           │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you debug NestJS applications?

**Answer**: NestJS debugging via:
- VS Code debugger
- NestJS debug mode
- Console logs
- Breakpoints
- Prisma Studio

### Q2: How do you debug API issues?

**Answer**: API debugging via:
- Postman for testing
- Console logs
- Network tab
- Request/response inspection
- Authentication/authorization checks

### Q3: How do you debug database issues?

**Answer**: Database debugging via:
- Prisma Studio
- Database logs
- Query analyzer
- Connection checks
- Schema validation

## Exercises

### Exercise 1: Debug Backend Issue

**Task**: Debug a backend issue.

**Steps**:
1. Reproduce issue
2. Add breakpoints
3. Use debugger
4. Identify root cause
5. Fix issue

**Verification**:
- Issue reproduced
- Root cause identified
- Fix implemented
- Fix tested
- Issue resolved

### Exercise 2: Debug API Issue

**Task**: Debug an API issue.

**Steps**:
1. Use Postman
2. Check logs
3. Check request/response
4. Identify root cause
5. Fix issue

**Verification**:
- Issue reproduced
- Request/response checked
- Root cause identified
- Fix implemented
- Issue resolved

## Real Production Scenarios

### Scenario 1: API Not Working

**Situation**: API not working

**Response**:
1. Check logs
2. Use debugger
3. Check database
4. Fix issue
5. Test fix

### Scenario 2: Database Query Failed

**Situation**: Database query failed

**Response**:
1. Check connection
2. Check query
3. Check schema
4. Fix issue
5. Test fix

## Navigation

**Next Section**: [02-Frontend-Debugging](./02-Frontend-Debugging.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
