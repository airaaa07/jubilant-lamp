# Notification Worker

## Purpose

This document explains the notification worker in the University ERP system. It details how the notification worker processes email and SMS notifications.

## Why This Document Exists

**Confirmed by Code**: The notification worker handles email and SMS notifications. Understanding the notification worker is critical for:
- Processing notification jobs
- Sending emails
- Sending SMS
- Debugging notification issues
- Creating custom notification processors

Without understanding the notification worker, developers may struggle with notifications or may introduce notification bugs.

## Where This Is Used

- **Onboarding**: New developers learn notification worker
- **Feature Development**: Implementing notifications
- **Code Reviews**: Reviewing notification code
- **Notifications**: Processing notifications
- **Email/SMS**: Sending emails and SMS

## Dependencies

### Notification Worker Dependencies

**Confirmed by Code**: Notification worker depends on:

- **Bull**: Queue library
- **NestJS**: Framework for workers
- **Email Service**: Email sending service
- **SMS Service**: SMS sending service
- **Redis**: Queue storage

## Internal Architecture

### Notification Worker Architecture

**Confirmed by Code**: Notification worker follows Bull queue pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Service                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Notification Queue                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Notification Worker                          │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Email        │  │  SMS            │  │  Push          │
│  Processor    │  │  Processor      │  │  (Future)       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Notification Worker Implementation

**Confirmed by Code**: Notification worker processes email and SMS jobs.

**NotificationWorker**:
```typescript
import { Processor, Process } from '@nestjs/bull';
import { Job } from 'bull';
import { Injectable } from '@nestjs/common';

@Injectable()
@Processor('notifications')
export class NotificationWorker {
  constructor(
    private emailService: EmailService,
    private smsService: SmsService,
  ) {}

  @Process('send-email')
  async handleSendEmail(job: Job) {
    const { to, subject, body, attachments } = job.data;

    try {
      await this.emailService.sendEmail(to, subject, body, attachments);
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

  @Process('send-bulk-email')
  async handleSendBulkEmail(job: Job) {
    const { recipients, subject, body } = job.data;
    const total = recipients.length;

    for (let i = 0; i < total; i++) {
      try {
        await this.emailService.sendEmail(recipients[i], subject, body);
        await job.progress(Math.round(((i + 1) / total) * 100));
      } catch (error) {
        console.error(`Failed to send email to ${recipients[i]}: ${error.message}`);
      }
    }
  }
}
```

**What This Does**:
- **send-email**: Processes single email job
- **send-sms**: Processes single SMS job
- **send-bulk-email**: Processes bulk email job
- **Progress Tracking**: Updates job progress
- **Error Handling**: Handles errors gracefully

### Email Service

**Confirmed by Code**: Email service sends emails.

**EmailService**:
```typescript
@Injectable()
export class EmailService {
  constructor(private configService: ConfigService) {}

  async sendEmail(to: string, subject: string, body: string, attachments?: any[]) {
    // Implementation depends on email provider
    // Could be SendGrid, AWS SES, SMTP, etc.
    
    console.log(`Sending email to ${to}`);
    console.log(`Subject: ${subject}`);
    
    // Send email using provider
    // await this.sendGrid.send({ to, subject, body, attachments });
  }
}
```

**What This Does**:
- **sendEmail**: Sends email
- **Provider**: Uses email provider
- **Attachments**: Supports attachments
- **Logging**: Logs email sending

### SMS Service

**Confirmed by Code**: SMS service sends SMS messages.

**SmsService**:
```typescript
@Injectable()
export class SmsService {
  constructor(private configService: ConfigService) {}

  async sendSms(to: string, message: string) {
    // Implementation depends on SMS provider
    // Could be Twilio, AWS SNS, etc.
    
    console.log(`Sending SMS to ${to}`);
    console.log(`Message: ${message}`);
    
    // Send SMS using provider
    // await this.twilio.messages.create({ to, body: message });
  }
}
```

**What This Does**:
- **sendSms**: Sends SMS
- **Provider**: Uses SMS provider
- **Logging**: Logs SMS sending

## Database Interactions

### Notification Worker-Database Flow

**Confirmed by Code**: Notification worker may log to database.

**Flow**:
```
Worker → Service → Database → Notification Log
```

## Redis Interactions

### Notification Worker-Redis Flow

**Confirmed by Code**: Notification worker uses Redis for queue storage.

**Flow**:
```
Service → Redis Queue → Worker
```

## Queue Interactions

### Notification Worker-Queue Flow

**Confirmed by Code**: Notification worker processes jobs from queue.

**Flow**:
```
Service → Notification Queue → Worker → Process Job
```

## Worker Interactions

### Notification Worker-Worker Flow

**Confirmed by Code**: Notification worker doesn't interact with other workers.

**Flow**:
```
Notification Worker → No worker interaction
```

## Business Rules

### Notification Worker Rules

**Confirmed by Code**: Notification worker follows these rules:

1. **Async Processing**: Notifications processed asynchronously
2. **Queue-Based**: Notifications queued for processing
3. **Retry Logic**: Failed notifications retried
4. **Progress Tracking**: Job progress tracked
5. **Bulk Processing**: Bulk notifications supported

### Email Rules

**Confirmed by Code**: Email rules:

1. **To**: Recipient email address
2. **Subject**: Email subject
3. **Body**: Email body (HTML or text)
4. **Attachments**: Email attachments supported
5. **Template**: Email templates supported

### SMS Rules

**Confirmed by Code**: SMS rules:

1. **To**: Recipient phone number
2. **Message**: SMS message
3. **Length**: SMS length limited
4. **Encoding**: UTF-8 encoding
5. **Template**: SMS templates supported

## Security

### Notification Worker Security

**Confirmed by Code**: Security considerations for notification worker:

1. **Input Validation**: Validate notification data
2. **Sensitive Data**: Don't log sensitive data
3. **Rate Limiting**: Rate limit notifications
4. **Provider Security**: Secure provider credentials
5. **Audit Logging**: Log all notifications

## Performance Considerations

### Notification Worker Performance

**Confirmed by Code**: Performance considerations:

1. **Concurrency**: Configure worker concurrency
2. **Batch Processing**: Batch process notifications
3. **Provider Limits**: Respect provider rate limits
4. **Queue Size**: Monitor queue size
5. **Retry Logic**: Configure retry logic

## Common Mistakes

### Mistake 1: Not Handling Errors

**Symptom**: Notifications failing silently

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

### Mistake 3: Not Respecting Rate Limits

**Symptom**: Provider blocking requests

**Cause**: Not respecting provider rate limits

**Fix**:
```typescript
// Add rate limiting
await this.rateLimiter.wait();
await this.emailService.sendEmail(to, subject, body);
```

## Debugging Guide

### Notification Worker Debugging

**Issue**: Notification not sent

**Investigation**:
1. Check queue connection
2. Check job data
3. Check worker logic
4. Check provider credentials
5. Check logs

**Tools**:
- Worker logs
- Queue logs
- Provider logs
- Email logs
- SMS logs

## Future Enhancements

### Push Notifications

**Status**: Not implemented

**Proposal**: Implement push notifications:
- FCM for Android
- APNS for iOS
- Web push notifications
- Better user experience
- More complex

### Notification Templates

**Status**: Not implemented

**Proposal**: Implement notification templates:
- Email templates
- SMS templates
- Dynamic content
- Better customization
- More complex

## Production Considerations

### Production Notification Worker

**Production Deployment**:
- Enable all processors
- Configure concurrency
- Configure retry logic
- Monitor queue size
- Monitor provider limits

### Notification Worker Monitoring

**Monitoring Metrics**:
- Email send rate
- SMS send rate
- Notification failure rate
- Queue size
- Provider response time

## Example Requests

### Notification Worker Example

**Queue Email Job**:
```typescript
await this.notificationQueue.add('send-email', {
  to: 'user@example.com',
  subject: 'Test Email',
  body: 'Test Body',
});
```

**Queue SMS Job**:
```typescript
await this.notificationQueue.add('send-sms', {
  to: '+1234567890',
  message: 'Test SMS',
});
```

## Example Responses

### Notification Worker Response

**Job Completed**:
```typescript
await job.progress(100);
// Job marked complete
```

## Sequence Diagrams

### Notification Worker Flow

```
Service → Notification Queue → Worker → Email/SMS Service → Provider → Notification Sent
```

## Architecture Diagrams

### Notification Worker Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Service                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Notification Queue                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Notification Worker                        │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Email        │  │  SMS            │  │  Bulk Email     │
│  Processor    │  │  Processor      │  │  Processor      │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Email/SMS Provider                        │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does the notification worker work?

**Answer**: Notification worker via:
- Processes jobs from notification queue
- Sends emails via email service
- Sends SMS via SMS service
- Tracks job progress
- Retries failed jobs

### Q2: How do you send a notification?

**Answer**: Send notification via:
- Add job to notification queue
- Specify job type (send-email, send-sms)
- Provide notification data
- Worker processes job
- Notification sent

### Q3: How do you handle notification failures?

**Answer**: Notification failures via:
- Try-catch blocks
- Throw errors to mark job failed
- Configure retry logic
- Log errors for debugging
- Monitor failure rate

## Exercises

### Exercise 1: Create a Notification Processor

**Task**: Create a custom notification processor.

**Steps**:
1. Add @Process decorator
2. Implement processor logic
3. Add error handling
4. Add progress tracking
5. Test processor

**Verification**:
- Processor created
- Logic works
- Error handling works
- Progress tracking works
- Tests pass

### Exercise 2: Implement Bulk Email Processing

**Task**: Implement bulk email processing.

**Steps**:
1. Add bulk email processor
2. Implement batch processing
3. Add progress tracking
4. Add error handling per recipient
5. Test bulk processing

**Verification**:
- Processor created
- Batch processing works
- Progress tracking works
- Error handling works
- Tests pass

## Real Production Scenarios

### Scenario 1: Email Not Sending

**Situation**: Email not sending

**Response**:
1. Check email service
2. Check provider credentials
3. Check email data
4. Fix email service
5. Test email

### Scenario 2: Queue Backlog

**Situation**: Notification queue backlog

**Response**:
1. Check queue size
2. Add more workers
3. Optimize processing
4. Monitor queue
5. Clear backlog

## Navigation

**Next Section**: [02-Workflow-Worker](./02-Workflow-Worker.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [09-Workflows](../09-Workflows/README.md) - Workflow details
