# 16-Debugging

## Purpose

This folder provides comprehensive documentation about debugging in the University ERP system. It details debugging techniques, tools, common issues, and solutions.

## Why This Folder Exists

**Confirmed by Code**: The University ERP requires effective debugging. Understanding debugging is critical for:
- Identifying and fixing bugs
- Troubleshooting issues
- Using debugging tools
- Debugging different components
- Optimizing debugging process

Without understanding debugging, developers may struggle with troubleshooting or may take longer to fix issues.

## Where This Is Used

- **Onboarding**: New developers learn debugging
- **Feature Development**: Debugging new features
- **Code Reviews**: Reviewing debugging approaches
- **Troubleshooting**: Troubleshooting issues
- **Bug Fixes**: Fixing bugs

## Dependencies

### Debugging Dependencies

**Confirmed by Code**: Debugging depends on:

- **VS Code Debugger**: IDE debugger
- **Chrome DevTools**: Browser debugger
- **Prisma Studio**: Database debugger
- **Redis CLI**: Redis debugger
- **kubectl Logs**: Kubernetes logs

## Internal Architecture

### Debugging Architecture

**Confirmed by Code**: Debugging follows systematic approach.

```
┌─────────────────────────────────────────────────────────┐
│              Issue Identified                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Reproduce Issue                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Identify Root Cause                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Fix Issue                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Test Fix                                       │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Backend Debugging

**Confirmed by Code**: Backend debugging using NestJS debugger.

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
      "protocol": "inspector"
    }
  ]
}
```

**What This Does**:
- **type**: Node.js debugger
- **request**: Launch configuration
- **runtimeExecutable**: Use npm
- **runtimeArgs**: Run start:debug
- **protocol**: Inspector protocol

### Frontend Debugging

**Confirmed by Code**: Frontend debugging using Chrome DevTools.

**Debugging Steps**:
1. Open Chrome DevTools (F12)
2. Use Sources tab for debugging
3. Use Console for logging
4. Use Network tab for API calls
5. Use React DevTools for React debugging

**What This Does**:
- **Sources**: Debug JavaScript
- **Console**: View logs
- **Network**: Monitor API calls
- **React DevTools**: Debug React components

### Database Debugging

**Confirmed by Code**: Database debugging using Prisma Studio.

**Prisma Studio**:
```bash
npx prisma studio
```

**What This Does**:
- **GUI**: Graphical interface for database
- **Query**: Query database visually
- **Edit**: Edit data directly
- **Debug**: Debug database issues

## Database Interactions

### Debugging-Database Flow

**Confirmed by Code**: Debugging database queries.

**Flow**:
```
Debugging → Prisma Studio → Database → Query Results
```

## Redis Interactions

### Debugging-Redis Flow

**Confirmed by Code**: Debugging Redis using Redis CLI.

**Redis CLI**:
```bash
redis-cli
> KEYS *
> GET key
> DEL key
```

**What This Does**:
- **KEYS**: List all keys
- **GET**: Get value
- **DEL**: Delete key

## Queue Interactions

### Debugging-Queue Flow

**Confirmed by Code**: Debugging queues using Bull Board.

**Bull Board**:
```typescript
import { BullAdapter } from '@bull-board/api/bullAdapter';
import { BullBoard } from '@bull-board/nestjs';

@Module({
  imports: [
    BullModule.forRoot({ redis: { host: 'localhost', port: 6379 } }),
    BullBoardModule.forFeature({
      name: 'notifications',
      adapter: BullAdapter,
    }),
  ],
})
export class AppModule {}
```

**What This Does**:
- **Bull Board**: UI for queue management
- **Adapter**: Bull adapter
- **Feature**: Register queue

## Worker Interactions

### Debugging-Worker Flow

**Confirmed by Code**: Debugging workers using logs.

**Worker Logs**:
```typescript
@Process('send-email')
async handleSendEmail(job: Job) {
  console.log(`Processing job ${job.id}`);
  console.log(`Job data:`, job.data);
  // ... processing
  console.log(`Job ${job.id} completed`);
}
```

**What This Does**:
- **console.log**: Log job progress
- **job.id**: Job identifier
- **job.data**: Job data

## Business Rules

### Debugging Rules

**Confirmed by Code**: Debugging follows these rules:

1. **Reproduce**: Reproduce the issue
2. **Isolate**: Isolate the problem
3. **Identify**: Identify root cause
4. **Fix**: Fix the issue
5. **Test**: Test the fix

### Logging Rules

**Confirmed by Code**: Logging rules:

1. **Structured Logging**: Use structured logging
2. **Log Levels**: Use appropriate log levels
3. **Context**: Include context in logs
4. **Sensitive Data**: Don't log sensitive data
5. **Performance**: Consider performance impact

## Security

### Debugging Security

**Confirmed by Code**: Security considerations for debugging:

1. **Sensitive Data**: Don't log sensitive data
2. **Debug Mode**: Disable debug mode in production
3. **Access Control**: Restrict debugging access
4. **Logs**: Secure log storage
5. **Tools**: Use secure debugging tools

## Performance Considerations

### Debugging Performance

**Confirmed by Code**: Performance considerations:

1. **Logging**: Minimize logging overhead
2. **Debug Mode**: Disable in production
3. **Profiling**: Use profiling tools
4. **Monitoring**: Monitor debugging impact
5. **Optimization**: Optimize debugging code

## Common Mistakes

### Mistake 1: Not Reproducing Issue

**Symptom**: Fix doesn't work

**Cause**: Not reproducing issue

**Fix**:
```typescript
// Reproduce issue before fixing
// Write test case
// Verify fix works
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

### Mistake 3: Not Using Debugger

**Symptom**: Slow debugging

**Cause**: Not using debugger

**Fix**:
```typescript
// Use debugger instead of console.log
debugger;
// or use breakpoints in IDE
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

### Frontend Debugging

**Issue**: Frontend not working

**Investigation**:
1. Check browser console
2. Check network tab
3. Check React DevTools
4. Check API calls
5. Check state

**Tools**:
- Chrome DevTools
- React DevTools
- Redux DevTools
- Network tab

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

### Production Debugging

**Production Deployment**:
- Disable debug mode
- Use structured logging
- Use error tracking
- Monitor logs
- Secure debugging access

### Debugging Monitoring

**Monitoring Metrics**:
- Error rate
- Log volume
- Debug mode usage
- Tool usage
- Issue resolution time

## Example Requests

### Debugging Example

**Debug Backend**:
```bash
npm run start:debug
```

**Debug Database**:
```bash
npx prisma studio
```

## Example Responses

### Debugging Response

**Response**: Debugger attached

```bash
Debugger listening on ws://127.0.0.1:9229
```

## Sequence Diagrams

### Debugging Flow

```
Issue → Reproduce → Identify Root Cause → Fix → Test → Deploy
```

## Architecture Diagrams

### Debugging Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Issue Identified                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Reproduce Issue                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Identify Root Cause                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Fix Issue                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Test Fix                                       │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you debug backend issues?

**Answer**: Backend debugging via:
- VS Code debugger
- Console logs
- Prisma Studio
- Postman for API testing
- Check logs and errors

### Q2: How do you debug frontend issues?

**Answer**: Frontend debugging via:
- Chrome DevTools
- React DevTools
- Network tab for API calls
- Console for errors
- State inspection

### Q3: How do you debug database issues?

**Answer**: Database debugging via:
- Prisma Studio
- Database logs
- Query analyzer
- Check connection
- Check constraints

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

### Exercise 2: Debug Frontend Issue

**Task**: Debug a frontend issue.

**Steps**:
1. Reproduce issue
2. Open DevTools
3. Check console
4. Check network
5. Fix issue

**Verification**:
- Issue reproduced
- Console checked
- Network checked
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

### Scenario 2: Frontend Error

**Situation**: Frontend error

**Response**:
1. Check console
2. Check network
3. Check state
4. Fix issue
5. Test fix

## Navigation

**Next Section**: [01-Backend-Debugging](./01-Backend-Debugging.md)

**Previous Section**: [15-Deployment](../15-Deployment/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
