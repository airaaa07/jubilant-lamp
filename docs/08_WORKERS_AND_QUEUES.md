# University ERP - Workers and Queues

## Overview

The system uses **Bull** (Redis-based queue) for background job processing. There are two main worker services that process jobs asynchronously:

1. **notification-worker**: Processes email and SMS notifications
2. **cert-generator**: Processes certificate generation jobs

## Technology Stack

- **Bull 4.x**: Redis-based job queue
- **Redis 7**: Queue backend
- **@nestjs/bull 10.x**: NestJS Bull integration
- **Nodemailer 9.x**: Email sending (notification-worker)
- **Puppeteer**: PDF generation (cert-generator)
- **Handlebars**: Template rendering (cert-generator)

## Queue Architecture

```
┌─────────────────┐
│   Core API      │
│                 │
│  Job Producer   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│     Redis       │
│                 │
│  Queue Storage  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Worker Process  │
│                 │
│  Job Consumer   │
└─────────────────┘
```

## Notification Worker

### Purpose

Processes email and SMS notifications asynchronously to avoid blocking the main API.

### Location

- **Service**: `apps/notification-worker/`
- **Port**: 3002
- **Docker**: `notification-worker` service in docker-compose.yml

### Package.json Dependencies

```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/config": "^3.0.0",
    "@nestjs/bull": "^10.0.0",
    "bull": "^4.11.0",
    "nodemailer": "^9.0.0",
    "@university-erp/types": "workspace:*"
  }
}
```

### App Module

```typescript
// apps/notification-worker/src/app.module.ts
@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true })],
})
export class AppModule {}
```

**Note**: The notification-worker has a minimal app module. The actual queue processing logic would be implemented in queue processors (not visible in current discovery).

### Main Entry Point

```typescript
// apps/notification-worker/src/main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT || 3002);
}
bootstrap();
```

### Expected Queue Processors

Based on the system architecture, the notification-worker would process:

1. **Email Queue**
   - Job type: email
   - Data: recipient, subject, template, variables
   - Process: Render template, send via Nodemailer

2. **SMS Queue**
   - Job type: sms
   - Data: phone, message
   - Process: Send via SMS gateway

3. **Bulk Email Queue**
   - Job type: bulk_email
   - Data: recipients[], subject, template
   - Process: Send to all recipients

### Job Flow

```
Core API Service
    ↓
Add job to queue (Bull)
    ↓
Redis stores job
    ↓
Notification Worker polls
    ↓
Worker processes job
    ↓
Send email/SMS
    ↓
Update job status
    ↓
Remove from queue
```

## Certificate Generator

### Purpose

Generates PDF certificates asynchronously using Puppeteer and Handlebars templates.

### Location

- **Service**: `apps/cert-generator/`
- **Port**: 3003
- **Docker**: `cert-generator` service in docker-compose.yml

### Package.json Dependencies

```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "@nestjs/config": "^3.0.0",
    "@nestjs/bull": "^10.0.0",
    "bull": "^4.11.0",
    "puppeteer": "^21.0.0",
    "handlebars": "^4.7.0",
    "minio": "^7.0.0",
    "@university-erp/types": "workspace:*"
  }
}
```

### App Module

```typescript
// apps/cert-generator/src/app.module.ts
@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true })],
})
export class AppModule {}
```

**Note**: Similar to notification-worker, the cert-generator has a minimal app module. The actual queue processing logic would be implemented in queue processors.

### Main Entry Point

```typescript
// apps/cert-generator/src/main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT || 3003);
}
bootstrap();
```

### Expected Queue Processors

Based on the system architecture, the cert-generator would process:

1. **Certificate Queue**
   - Job type: certificate
   - Data: templateId, subjectId, subjectType, variables
   - Process:
     - Load template
     - Bind data
     - Render HTML
     - Convert to PDF (Puppeteer)
     - Upload to MinIO
     - Return URL

2. **Bulk Certificate Queue**
   - Job type: bulk_certificate
   - Data: templateId, subjects[]
   - Process: Generate certificates for all subjects

### Job Flow

```
Core API Service
    ↓
Add job to queue (Bull)
    ↓
Redis stores job
    ↓
Certificate Generator polls
    ↓
Worker processes job
    ↓
Load template (Handlebars)
    ↓
Bind data
    ↓
Render HTML
    ↓
Convert to PDF (Puppeteer)
    ↓
Upload to MinIO
    ↓
Return URL
    ↓
Update job status
    ↓
Remove from queue
```

## Bull Queue Configuration

### Redis Connection

```typescript
import Bull from 'bull';

const queue = new Bull('queue-name', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});
```

### Queue Options

```typescript
{
  redis: {
    host: 'localhost',
    port: 6379,
  },
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 10,
    removeOnFailed: 50,
  },
}
```

### Job Options

- **attempts**: Number of retry attempts (default: 3)
- **backoff**: Retry strategy (exponential backoff)
- **removeOnComplete**: Keep last N completed jobs
- **removeOnFailed**: Keep last N failed jobs
- **delay**: Delay before processing
- **priority**: Job priority (1-10)

## Queue Management

### Adding Jobs

```typescript
// In Core API
import { InjectQueue } from '@nestjs/bull';
import { Queue } from 'bull';

@Injectable()
export class NotificationService {
  constructor(
    @InjectQueue('notifications') private notificationQueue: Queue,
  ) {}

  async sendEmail(data: EmailDto) {
    await this.notificationQueue.add('email', data);
  }
}
```

### Processing Jobs

```typescript
// In Worker
import { Processor, Process } from '@nestjs/bull';
import { Job } from 'bull';

@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { recipient, subject, body } = job.data;
    // Send email logic
  }
}
```

### Job Status

- **waiting**: Job waiting to be processed
- **active**: Job currently being processed
- **completed**: Job completed successfully
- **failed**: Job failed after all retries
- **delayed**: Job delayed until specific time
- **paused**: Queue is paused
- **stopped**: Queue is stopped

## Queue Monitoring

### Bull Board

Bull Board is a UI for monitoring Bull queues. It can be configured to view:

- Queue statistics
- Job lists
- Job details
- Retry attempts
- Failed jobs

### Configuration

```typescript
import { BullAdapter } from '@bull-board/api/bullAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

const queue = new Bull('notifications');
serverAdapter.add(new BullAdapter(queue));

app.use('/admin/queues', serverAdapter.getRouter());
```

## Error Handling

### Retry Strategy

```typescript
{
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 2000, // 2s, 4s, 8s
  },
}
```

### Error Logging

```typescript
@Process('email')
async handleEmail(job: Job) {
  try {
    await this.sendEmail(job.data);
  } catch (error) {
    job.moveToFailed(error);
    this.logger.error('Email failed', error);
  }
}
```

### Dead Letter Queue

Failed jobs can be moved to a dead letter queue for manual inspection:

```typescript
queue.on('failed', (job, error) => {
  // Log error
  // Optionally move to dead letter queue
});
```

## Performance Considerations

### Concurrency

```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  @Concurrency(5) // Process 5 jobs concurrently
  async handleEmail(job: Job) {
    // Process job
  }
}
```

### Rate Limiting

For external services (email/SMS gateways), implement rate limiting:

```typescript
private rateLimiter = new RateLimiter({
  tokensPerInterval: 10,
  interval: 'minute',
});

async sendEmail(data: EmailDto) {
  await this.rateLimiter.removeTokens(1);
  // Send email
}
```

## Scaling Workers

### Horizontal Scaling

Multiple worker instances can process the same queue:

```bash
# Start multiple worker instances
npm run start -- --port 3002
npm run start -- --port 3002
npm run start -- --port 3002
```

Bull handles job distribution across workers automatically.

### Vertical Scaling

Increase worker resources:
- More CPU for Puppeteer (cert-generator)
- More memory for large PDF generation

## Known Limitations

1. **Minimal Implementation**: Current worker app modules are minimal (only ConfigModule)
2. **No Queue Processors Visible**: Actual queue processors not visible in discovery
3. **No Bull Board**: Queue monitoring UI not configured
4. **No Dead Letter Queue**: Failed job handling not visible
5. **No Rate Limiting**: External service rate limiting not visible

## Future Enhancements

1. **Implement Queue Processors**: Add actual job processing logic
2. **Add Bull Board**: Configure queue monitoring UI
3. **Implement Dead Letter Queue**: Handle failed jobs
4. **Add Rate Limiting**: Protect external services
5. **Add Job Priorities**: Prioritize urgent notifications
6. **Add Job Scheduling**: Schedule delayed jobs
7. **Add Job Chaining**: Chain dependent jobs
8. **Add Job Batching**: Batch similar jobs for efficiency
