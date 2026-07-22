# Queue Storage

## Purpose

This document explains queue storage in the University ERP system. It details how Redis is used for queue storage by Bull, queue configuration, and best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Redis for queue storage. Understanding queue storage is critical for:
- Implementing async processing
- Managing queues
- Configuring Bull queues
- Debugging queue issues
- Optimizing queue performance

Without understanding queue storage, developers may struggle with queues or may introduce queue-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn queue storage
- **Feature Development**: Implementing queues
- **Code Reviews**: Reviewing queue code
- **Async Processing**: Implementing async processing
- **Workers**: Managing workers

## Dependencies

### Queue Storage Dependencies

**Confirmed by Code**: Queue storage depends on:

- **Bull**: Queue library
- **RedisService**: Redis client
- **NestJS**: Framework for queues
- **Environment Variables**: Queue configuration

## Internal Architecture

### Queue Storage Architecture

**Confirmed by Code**: Queue storage uses Redis lists.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Bull Queue                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Redis Server                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Wait Queue   │  │  Active Queue   │  │  Delayed Queue  │
│  (Pending)    │  │  (Processing)   │  │  (Delayed)      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Queue Configuration

**Confirmed by Code**: Queues configured in BullModule.

**QueueModule**:
```typescript
import { Module } from '@nestjs/common';
import { BullModule } from '@nestjs/bull';
import { ConfigService } from '@nestjs/config';

@Module({
  imports: [
    BullModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        redis: {
          host: configService.get('REDIS_HOST', 'localhost'),
          port: configService.get('REDIS_PORT', 6379),
          password: configService.get('REDIS_PASSWORD'),
          db: configService.get('REDIS_DB', 0),
        },
      }),
    }),
    BullModule.registerQueue({
      name: 'notifications',
      defaultJobOptions: {
        attempts: 3,
        backoff: {
          type: 'exponential',
          delay: 2000,
        },
        removeOnComplete: 100,
        removeOnFail: 50,
      },
    }),
    BullModule.registerQueue({
      name: 'workflow',
      defaultJobOptions: {
        attempts: 5,
        backoff: {
          type: 'exponential',
          delay: 3000,
        },
        removeOnComplete: 100,
        removeOnFail: 50,
      },
    }),
  ],
})
export class QueueModule {}
```

**What This Does**:
- **BullModule.forRootAsync**: Configures Bull globally
- **registerQueue**: Registers queues
- **defaultJobOptions**: Default job options
- **attempts**: Retry attempts
- **backoff**: Backoff strategy
- **removeOnComplete**: Remove completed jobs
- **removeOnFail**: Remove failed jobs

### Queue Producer

**Confirmed by Code**: Queue producer adds jobs to queue.

**QueueProducer**:
```typescript
import { Injectable, Inject } from '@nestjs/common';
import { Queue } from 'bull';
import { InjectQueue } from '@nestjs/bull';

@Injectable()
export class QueueProducer {
  constructor(
    @InjectQueue('notifications') private notificationQueue: Queue,
    @InjectQueue('workflow') private workflowQueue: Queue,
  ) {}

  async addEmailJob(data: any) {
    return this.notificationQueue.add('send-email', data, {
      attempts: 3,
      backoff: {
        type: 'exponential',
        delay: 2000,
      },
    });
  }

  async addWorkflowJob(data: any) {
    return this.workflowQueue.add('auto-transition', data, {
      attempts: 5,
      backoff: {
        type: 'exponential',
        delay: 3000,
      },
    });
  }

  async addDelayedJob(data: any, delay: number) {
    return this.notificationQueue.add('send-email', data, {
      delay,
    });
  }
}
```

**What This Does**:
- **addEmailJob**: Adds email job to queue
- **addWorkflowJob**: Adds workflow job to queue
- **addDelayedJob**: Adds delayed job to queue
- **Job Options**: Configures job options

## Database Interactions

### Queue Storage-Database Flow

**Confirmed by Code**: Queue storage doesn't interact with database directly.

**Flow**:
```
Queue Storage → No database interaction
```

## Redis Interactions

### Queue Storage-Redis Flow

**Confirmed by Code**: Queue storage uses Redis for storage.

**Flow**:
```
Bull Queue → Redis Server → Bull Worker
```

## Queue Interactions

### Queue Storage-Queue Flow

**Confirmed by Code**: Queue storage is used by Bull.

**Flow**:
```
Application → Bull Queue → Redis → Bull Worker
```

## Worker Interactions

### Queue Storage-Worker Flow

**Confirmed by Code**: Workers process jobs from queue storage.

**Flow**:
```
Worker → Redis Queue → Process Job
```

## Business Rules

### Queue Storage Rules

**Confirmed by Code**: Queue storage follows these rules:

1. **FIFO**: Jobs processed in FIFO order
2. **Priority**: Jobs can have priority
3. **Retry**: Failed jobs retried
4. **Backoff**: Exponential backoff for retries
5. **Cleanup**: Old jobs cleaned up

### Job Rules

**Confirmed by Code**: Job rules:

1. **Job Data**: Job data serialized
2. **Job Options**: Job options configured
3. **Job Status**: Job status tracked
4. **Job Progress**: Job progress tracked
5. **Job Result**: Job result stored

## Security

### Queue Storage Security

**Confirmed by Code**: Security considerations for queue storage:

1. **Input Validation**: Validate job data
2. **Sensitive Data**: Don't store sensitive data
3. **Access Control**: Restrict queue access
4. **Encryption**: Encrypt job data if needed
5. **Audit Logging**: Log queue operations

## Performance Considerations

### Queue Storage Performance

**Confirmed by Code**: Performance considerations:

1. **Queue Size**: Monitor queue size
2. **Job Size**: Keep job data small
3. **Cleanup**: Clean up old jobs
4. **Concurrency**: Configure worker concurrency
5. **Backpressure**: Handle backpressure

## Common Mistakes

### Mistake 1: Not Configuring Retry

**Symptom**: Jobs fail permanently

**Cause**: Not configuring retry

**Fix**:
```typescript
// Configure retry
await this.queue.add('job-type', data, {
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 2000,
  },
});
```

### Mistake 2: Not Cleaning Up Jobs

**Symptom**: Redis memory leak

**Cause**: Not cleaning up old jobs

**Fix**:
```typescript
// Configure cleanup
await this.queue.add('job-type', data, {
  removeOnComplete: 100,
  removeOnFail: 50,
});
```

### Mistake 3: Large Job Data

**Symptom**: Slow performance

**Cause**: Storing large job data

**Fix**:
```typescript
// Store only necessary data
const jobData = {
  id: data.id,
  // Don't store large nested objects
};
```

## Debugging Guide

### Queue Storage Debugging

**Issue**: Queue not working

**Investigation**:
1. Check Redis connection
2. Check queue configuration
3. Check job data
4. Check worker status
5. Check logs

**Tools**:
- Redis CLI
- Queue logs
- Worker logs
- Bull Board (UI)

## Future Enhancements

### Queue Dashboard

**Status**: Not implemented

**Proposal**: Implement queue dashboard:
- Bull Board integration
- Queue monitoring
- Job inspection
- Better observability
- More complex

### Queue Prioritization Advanced

**Status**: Partially implemented

**Proposal**: Implement advanced queue prioritization:
- Dynamic priority
- Priority escalation
- Better job scheduling
- More complex
- Better for complex workflows

## Production Considerations

### Production Queue Storage

**Production Deployment**:
- Configure retry logic
- Configure cleanup
- Monitor queue size
- Monitor job duration
- Monitor worker performance

### Queue Storage Monitoring

**Monitoring Metrics**:
- Queue size
- Job processing rate
- Job failure rate
- Job duration
- Worker resource usage

## Example Requests

### Queue Storage Example

**Add Job**:
```typescript
await this.notificationQueue.add('send-email', {
  to: 'user@example.com',
  subject: 'Test Email',
  body: 'Test Body',
});
```

## Example Responses

### Queue Storage Response

**Response**: Job added to queue

```typescript
const job = await this.notificationQueue.add('send-email', data);
// job.id = 'job-id'
```

## Sequence Diagrams

### Queue Storage Flow

```
Application → Bull Queue → Redis → Bull Worker → Process Job
```

## Architecture Diagrams

### Queue Storage Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Application                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Bull Queue                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Redis Server                               │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Wait Queue   │  │  Active Queue   │  │  Delayed Queue  │
│  (Pending)    │  │  (Processing)   │  │  (Delayed)      │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Bull Worker                                │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is Redis used for queue storage?

**Answer**: Queue storage via:
- Bull uses Redis lists for queue storage
- Jobs stored as serialized data
- Redis provides persistence
- Redis provides replication
- Redis provides clustering

### Q2: How do you configure retry logic?

**Answer**: Retry logic via:
- Configure attempts in job options
- Configure backoff strategy
- Exponential backoff for retries
- Linear backoff for retries
- Custom backoff function

### Q3: How do you monitor queue performance?

**Answer**: Queue monitoring via:
- Monitor queue size
- Monitor job processing rate
- Monitor job failure rate
- Monitor job duration
- Monitor worker resource usage

## Exercises

### Exercise 1: Create a Queue

**Task**: Create a custom queue.

**Steps**:
1. Register queue in BullModule
2. Configure default job options
3. Add job to queue
4. Create worker
5. Test queue

**Verification**:
- Queue created
- Job options configured
- Job added
- Worker processes job
- Tests pass

### Exercise 2: Implement Retry Logic

**Task**: Implement retry logic for jobs.

**Steps**:
1. Configure retry attempts
2. Configure backoff strategy
3. Test retry logic
4. Test failure handling
5. Test success after retry

**Verification**:
- Retry configured
- Backoff configured
- Retry works
- Failure handled
- Tests pass

## Real Production Scenarios

### Scenario 1: Queue Backlog

**Situation**: Queue backlog building up

**Response**:
1. Check queue size
2. Add more workers
3. Optimize job processing
4. Monitor queue
5. Clear backlog

### Scenario 2: Jobs Failing

**Situation**: Jobs failing repeatedly

**Response**:
1. Check job data
2. Check worker logic
3. Check retry configuration
4. Fix issue
5. Monitor queue

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [01-Caching](./01-Caching.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [11-Workers](../11-Workers/README.md) - Workers details
