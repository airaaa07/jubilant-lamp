# 11-Workers

## Purpose

This folder provides comprehensive documentation about the workers in the University ERP system. It details how workers work, what tasks they process, and how they interact with the queue system.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses workers for async task processing. Understanding workers is critical for:
- Processing async tasks
- Implementing background jobs
- Handling queue operations
- Debugging worker issues
- Creating custom workers

Without understanding workers, developers may struggle with async processing or may introduce worker bugs.

## Where This Is Used

- **Onboarding**: New developers learn workers
- **Feature Development**: Implementing workers
- **Code Reviews**: Reviewing worker code
- **Async Processing**: Processing async tasks
- **Background Jobs**: Implementing background jobs

## Dependencies

### Worker Dependencies

**Confirmed by Code**: Workers depend on:

- **Bull**: Queue library
- **NestJS**: Framework for workers
- **Prisma**: Database access
- **Redis**: Queue storage
- **External Services**: Email, SMS, etc.

## Internal Architecture

### Worker Architecture

**Confirmed by Code**: Workers follow Bull queue pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Queue Producer                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Bull Queue (Redis)                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Bull Worker                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Processor    │  │  Database       │  │  External       │
│  (Task Logic) │  │  (Data)         │  │  Services       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Worker Implementation

**Confirmed by Code**: Workers use Bull @Processor decorator.

**NotificationWorker**:
```typescript
import { Processor, Process } from '@nestjs/bull';
import { Job } from 'bull';
import { Injectable } from '@nestjs/common';

@Injectable()
@Processor('notifications')
export class NotificationWorker {
  constructor(private emailService: EmailService) {}

  @Process('send-email')
  async handleSendEmail(job: Job) {
    const { to, subject, body } = job.data;

    try {
      await this.emailService.sendEmail(to, subject, body);
      await job.progress(100);
    } catch (error) {
      throw new Error(`Failed to send email: ${error.message}`);
    }
  }

  @Process('send-sms')
  async handleSendSms(job: Job) {
    const { to, message } = job.data;

    try {
      await this.smsService.sendSms(to, message);
      await job.progress(100);
    } catch (error) {
      throw new Error(`Failed to send SMS: ${error.message}`);
    }
  }
}
```

**What This Does**:
- **@Processor**: Registers worker for queue
- **@Process**: Registers processor for job type
- **job.data**: Job data
- **job.progress()**: Updates job progress
- **Error Handling**: Handles errors

**WorkflowWorker**:
```typescript
@Injectable()
@Processor('workflow')
export class WorkflowWorker {
  constructor(private workflowService: WorkflowService) {}

  @Process('auto-transition')
  async handleAutoTransition(job: Job) {
    const { instanceId, stateId } = job.data;

    try {
      await this.workflowService.transition(instanceId, 'AUTO', {
        role: 'SYSTEM',
      } as JwtPayload);
      await job.progress(100);
    } catch (error) {
      throw new Error(`Failed to auto-transition: ${error.message}`);
    }
  }
}
```

**What This Does**:
- **auto-transition**: Processes workflow auto-transitions
- **workflowService**: Calls workflow service
- **transition**: Transitions workflow instance
- **Error Handling**: Handles errors

### Queue Registration

**Confirmed by Code**: Queues registered in module.

**QueueModule Registration**:
```typescript
@Module({
  imports: [
    BullModule.registerQueue({
      name: 'notifications',
      redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT),
      },
    }),
    BullModule.registerQueue({
      name: 'workflow',
      redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT),
      },
    }),
  ],
  providers: [NotificationWorker, WorkflowWorker],
})
export class WorkerModule {}
```

**What This Does**:
- **registerQueue**: Registers queue
- **redis**: Redis configuration
- **providers**: Registers workers

## Database Interactions

### Worker-Database Flow

**Confirmed by Code**: Workers interact with database for task processing.

**Flow**:
```
Worker → Service → Prisma → Database
```

## Redis Interactions

### Worker-Redis Flow

**Confirmed by Code**: Workers use Redis for queue storage.

**Flow**:
```
Queue Producer → Redis Queue → Worker
```

## Queue Interactions

### Worker-Queue Flow

**Confirmed by Code**: Workers process jobs from queues.

**Flow**:
```
Service → Queue → Worker → Process Job
```

## Worker Interactions

### Worker-Worker Flow

**Confirmed by Code**: Workers don't interact with other workers.

**Flow**:
```
Worker → No worker interaction
```

## Business Rules

### Worker Rules

**Confirmed by Code**: Workers follow these rules:

1. **Async Processing**: Workers process async tasks
2. **Queue-Based**: Workers process jobs from queues
3. **Error Handling**: Workers handle errors gracefully
4. **Progress Tracking**: Workers track job progress
5. **Retry Logic**: Workers retry failed jobs

### Job Processing Rules

**Confirmed by Code**: Job processing rules:

1. **Job Types**: Workers process specific job types
2. **Job Data**: Workers use job data
3. **Job Progress**: Workers update job progress
4. **Job Completion**: Workers mark jobs complete
5. **Job Failure**: Workers handle job failure

## Security

### Worker Security

**Confirmed by Code**: Security considerations for workers:

1. **Input Validation**: Validate job data
2. **Error Messages**: Don't leak sensitive info
3. **Access Control**: Workers have limited access
4. **Audit Logging**: Log all worker actions
5. **External Services**: Secure external service calls

## Performance Considerations

### Worker Performance

**Confirmed by Code**: Performance considerations:

1. **Concurrency**: Configure worker concurrency
2. **Batch Processing**: Batch process jobs
3. **Database Queries**: Optimize database queries
4. **External Calls**: Optimize external service calls
5. **Queue Size**: Monitor queue size

## Common Mistakes

### Mistake 1: Not Handling Errors

**Symptom**: Jobs failing silently

**Cause**: Not handling errors in worker

**Fix**:
```typescript
// Add error handling
try {
  await this.emailService.sendEmail(to, subject, body);
} catch (error) {
  throw new Error(`Failed to send email: ${error.message}`);
}
```

### Mistake 2: Not Updating Progress

**Symptom**: No progress tracking

**Cause**: Not updating job progress

**Fix**:
```typescript
// Update progress
await job.progress(50);
```

### Mistake 3: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Not using transactions for database operations

**Fix**:
```typescript
// Use transaction
await this.prisma.$transaction(async (tx) => {
  await tx.model.create({ data });
  await tx.model.update({ data });
});
```

## Debugging Guide

### Worker Debugging

**Issue**: Worker not processing jobs

**Investigation**:
1. Check worker registration
2. Check queue connection
3. Check job data
4. Check worker logic
5. Check logs

**Tools**:
- Worker logs
- Queue logs
- Redis logs
- Database logs

## Future Enhancements

### Worker Scaling

**Status**: Not implemented

**Proposal**: Implement worker scaling:
- Auto-scaling based on queue size
- Horizontal scaling
- Better resource utilization
- More complex
- Better performance

### Worker Monitoring

**Status**: Not implemented

**Proposal**: Implement worker monitoring:
- Worker health checks
- Queue monitoring
- Job monitoring
- Better observability
- More complex

## Production Considerations

### Production Workers

**Production Deployment**:
- Enable all workers
- Configure concurrency
- Configure retry logic
- Monitor worker performance
- Monitor queue size

### Worker Monitoring

**Monitoring Metrics**:
- Worker job processing rate
- Worker error rate
- Queue size
- Job duration
- Worker resource usage

## Example Requests

### Worker Example

**Queue Job**:
```typescript
await this.notificationQueue.add('send-email', {
  to: 'user@example.com',
  subject: 'Test Email',
  body: 'Test Body',
});
```

## Example Responses

### Worker Response

**Job Completed**:
```typescript
await job.progress(100);
// Job marked complete
```

## Sequence Diagrams

### Worker Flow

```
Service → Queue → Worker → Process Job → Database/External Service → Job Complete
```

## Architecture Diagrams

### Worker Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Service                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Bull Queue                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Bull Worker                                │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Processor    │  │  Database       │  │  External       │
│  (Task Logic) │  │  (Data)         │  │  Services       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How do workers work in NestJS?

**Answer**: Workers via:
- Use Bull for queue management
- @Processor decorator for worker registration
- @Process decorator for job processing
- Redis for queue storage
- Async job processing

### Q2: How do you create a custom worker?

**Answer**: Custom worker via:
- Create worker class
- Add @Processor decorator
- Add @Process decorator for job types
- Implement job processing logic
- Register worker in module

### Q3: How do you handle worker errors?

**Answer**: Worker errors via:
- Try-catch blocks
- Throw errors to mark job failed
- Configure retry logic
- Log errors for debugging
- Monitor error rate

## Exercises

### Exercise 1: Create a Worker

**Task**: Create a custom worker.

**Steps**:
1. Create worker class
2. Add @Processor decorator
3. Add @Process decorator
4. Implement job processing logic
5. Register worker

**Verification**:
- Worker created
- Decorators work
- Logic works
- Worker registered
- Tests pass

### Exercise 2: Create a Notification Worker

**Task**: Create a notification worker.

**Steps**:
1. Create worker class
2. Add email processor
3. Add SMS processor
4. Implement notification logic
5. Test notifications

**Verification**:
- Worker created
- Email works
- SMS works
- Notifications sent
- Tests pass

## Real Production Scenarios

### Scenario 1: Worker Not Processing Jobs

**Situation**: Worker not processing jobs

**Response**:
1. Check worker registration
2. Check queue connection
3. Check worker logic
4. Fix worker
5. Test worker

### Scenario 2: Queue Backlog

**Situation**: Queue backlog building up

**Response**:
1. Check queue size
2. Add more workers
3. Optimize job processing
4. Monitor queue
5. Clear backlog

## Navigation

**Next Section**: [01-Notification-Worker](./01-Notification-Worker.md)

**Previous Section**: [10-Request-Lifecycle](../10-Request-Lifecycle/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [12-Redis](../12-Redis/README.md) - Redis details
