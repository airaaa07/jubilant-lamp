# University ERP - Email and SMTP

## Overview

The system uses **Nodemailer** for sending emails. Email functionality is integrated into the authentication service for OTP verification, password reset, and general notifications.

## Technology Stack

- **Nodemailer 9.x**: Email sending library
- **SMTP**: Email protocol
- **Handlebars**: Email template rendering (potential)

## Architecture

```
┌─────────────────┐
│   Core API      │
│                 │
│  MailService    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   SMTP Server   │
│                 │
│  Email Gateway  │
└─────────────────┘
```

## Mail Service

### Location

- **Service**: `apps/core-api/src/modules/auth/auth.service.ts` (integrated)
- **Package**: `nodemailer` in core-api/package.json

### Implementation

The mail service is integrated into the AuthService. Based on the code structure, there would be a dedicated MailService for email operations.

### Expected Implementation

```typescript
// Expected mail service pattern
@Injectable()
export class MailService {
  private transporter: nodemailer.Transporter;

  constructor(private configService: ConfigService) {
    this.transporter = nodemailer.createTransport({
      host: this.configService.get('SMTP_HOST'),
      port: this.configService.get('SMTP_PORT', 587),
      secure: this.configService.get('SMTP_SECURE', false),
      auth: {
        user: this.configService.get('SMTP_USER'),
        pass: this.configService.get('SMTP_PASSWORD'),
      },
    });
  }

  async sendEmail(options: {
    to: string;
    subject: string;
    html: string;
    text?: string;
  }) {
    await this.transporter.sendMail({
      from: this.configService.get('SMTP_FROM'),
      to: options.to,
      subject: options.subject,
      html: options.html,
      text: options.text,
    });
  }

  async sendOtpEmail(email: string, otp: string) {
    await this.sendEmail({
      to: email,
      subject: 'Your OTP Code',
      html: `<p>Your OTP code is: <strong>${otp}</strong></p>`,
      text: `Your OTP code is: ${otp}`,
    });
  }

  async sendPasswordResetEmail(email: string, resetLink: string) {
    await this.sendEmail({
      to: email,
      subject: 'Password Reset',
      html: `<p>Click <a href="${resetLink}">here</a> to reset your password</p>`,
      text: `Click here to reset your password: ${resetLink}`,
    });
  }
}
```

## Email Types

### 1. OTP Emails

- **Purpose**: Send OTP for registration verification
- **Trigger**: User requests OTP during registration
- **Content**: 6-digit OTP code

### 2. Password Reset Emails

- **Purpose**: Send password reset link
- **Trigger**: User requests password reset
- **Content**: Reset link with token

### 3. Welcome Emails

- **Purpose**: Welcome new users
- **Trigger**: User registration completed
- **Content**: Welcome message + login details

### 4. Notification Emails

- **Purpose**: System notifications
- **Trigger**: Various system events
- **Content**: Event-specific information

### 5. Document Emails

- **Purpose**: Send generated documents
- **Trigger**: Document generation completed
- **Content**: Download link + document details

## Environment Variables

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu
```

## SMTP Configuration

### Gmail

```typescript
{
  host: 'smtp.gmail.com',
  port: 587,
  secure: false,
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-app-password',
  },
}
```

### SendGrid

```typescript
{
  host: 'smtp.sendgrid.net',
  port: 587,
  secure: false,
  auth: {
    user: 'apikey',
    pass: 'YOUR_SENDGRID_API_KEY',
  },
}
```

### AWS SES

```typescript
{
  host: 'email-smtp.us-east-1.amazonaws.com',
  port: 587,
  secure: true,
  auth: {
    user: 'YOUR_SES_SMTP_USERNAME',
    pass: 'YOUR_SES_SMTP_PASSWORD',
  },
}
```

## SMS Integration

### SMS Service

Based on the code structure, there is an SMS service for mobile OTP:

```typescript
// Expected SMS service pattern
@Injectable()
export class SmsService {
  async sendOtp(phone: string, otp: string) {
    // Integrate with SMS gateway (e.g., Twilio, MSG91)
    // Send SMS with OTP code
  }
}
```

### SMS Gateway Options

- **Twilio**: Popular SMS gateway
- **MSG91**: Indian SMS gateway
- **BulkSMS**: Bulk SMS service
- **Custom**: Custom SMS gateway integration

## Email Templates

### HTML Templates

Emails are sent as HTML for better formatting:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .button { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome to University ERP</h1>
    <p>Your account has been created successfully.</p>
    <a href="https://erp.university.edu/login" class="button">Login Now</a>
  </div>
</body>
</html>
```

### Text Fallback

Always include plain text version for email clients that don't support HTML.

## Queue-Based Email Sending

### Background Processing

Emails should be sent via queues to avoid blocking the API:

```typescript
// Add email job to queue
await this.notificationQueue.add('email', {
  to: user.email,
  subject: 'Welcome',
  template: 'welcome',
  variables: { name: user.firstName },
});
```

### Notification Worker

The notification-worker processes email jobs:

```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { to, subject, template, variables } = job.data;
    await this.mailService.sendTemplateEmail(to, subject, template, variables);
  }
}
```

## Error Handling

### Retry Logic

Email sending should retry on failure:

```typescript
try {
  await this.transporter.sendMail(options);
} catch (error) {
  // Retry with exponential backoff
  await this.retrySendEmail(options, 3);
}
```

### Bounce Handling

Handle bounced emails:

```typescript
transporter.on('bounce', (email, address, response) => {
  // Log bounce
  // Update user email status
});
```

### Complaint Handling

Handle spam complaints:

```typescript
transporter.on('complaint', (email, address, response) => {
  // Log complaint
  // Disable user email
});
```

## Security Considerations

### SMTP Credentials

- **Never commit**: SMTP credentials in code
- **Environment variables**: Store in environment
- **Secret management**: Use vault for production

### Email Content

- **Sanitize**: Sanitize user input in emails
- **No sensitive data**: Don't include passwords in emails
- **Rate limiting**: Limit email sending rate

### SPF/DKIM/DMARC

Configure email authentication:

- **SPF**: Specify authorized senders
- **DKIM**: Sign emails with DKIM
- **DMARC**: Policy for email authentication

## Monitoring

### Email Metrics

Track:
- **Send rate**: Emails per minute/hour
- **Bounce rate**: Percentage of bounced emails
- **Delivery rate**: Percentage of delivered emails
- **Open rate**: Percentage of opened emails
- **Click rate**: Percentage of clicked links

### Logging

Log all email operations:

```typescript
this.logger.log(`Email sent to ${to} with subject ${subject}`);
```

## Testing

### Development

Use email testing services during development:

- **Mailtrap**: Email testing service
- **MailHog**: Local email testing
- **Ethereal**: Email testing by Nodemailer

### Ethereal Example

```typescript
const testAccount = await nodemailer.createTestAccount();
const transporter = nodemailer.createTransport({
  host: 'smtp.ethereal.email',
  port: 587,
  auth: testAccount,
});
```

## Known Limitations

1. **No Dedicated MailService**: Email sending integrated in AuthService
2. **No Template Engine**: No Handlebars/Mustache integration visible
3. **No Email Queue**: Email sending not queued
4. **No Bounce Handling**: No bounce handling visible
5. **No Email Analytics**: No tracking of email metrics

## Future Enhancements

1. **Dedicated MailService**: Extract email logic to dedicated service
2. **Template Engine**: Add Handlebars for email templates
3. **Email Queue**: Queue email sending via notification-worker
4. **Bounce Handling**: Handle bounced emails
5. **Email Analytics**: Track email metrics
6. **Email Scheduling**: Schedule emails for later delivery
7. **Bulk Email**: Support bulk email sending
8. **Email Attachments**: Support file attachments
