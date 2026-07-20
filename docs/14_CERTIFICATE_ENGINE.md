# University ERP - Certificate Engine

## Overview

The **Certificate Generator** is a separate NestJS service responsible for generating PDF certificates using **Puppeteer** and **Handlebars** templates. It processes jobs from a Bull queue and stores generated certificates in MinIO.

## Technology Stack

- **NestJS 10.x**: Framework
- **Bull 4.x**: Queue processing
- **Puppeteer 21.x**: PDF generation from HTML
- **Handlebars 4.x**: Template rendering
- **MinIO 7.x**: Object storage for PDFs
- **Redis 7.x**: Queue backend

## Architecture

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
│ Cert Generator  │
│                 │
│  Job Consumer   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Puppeteer      │
│                 │
│  HTML → PDF     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│     MinIO       │
│                 │
│  PDF Storage    │
└─────────────────┘
```

## Service Configuration

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

**Note**: The cert-generator has a minimal app module. The actual queue processing logic would be implemented in queue processors (not visible in current discovery).

### Main Entry Point

```typescript
// apps/cert-generator/src/main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT || 3003);
}
bootstrap();
```

## Expected Queue Processors

Based on the system architecture, the cert-generator would process:

### 1. Certificate Queue

**Job Type**: `certificate`

**Job Data**:
```typescript
{
  templateId: string;
  subjectId: string;
  subjectType: 'student' | 'staff';
  variables: Record<string, any>;
}
```

**Processing Steps**:
1. Load DocumentTemplate from database
2. Fetch subject data (student/staff)
3. Bind variables to Handlebars template
4. Render HTML
5. Convert HTML to PDF using Puppeteer
6. Generate serial number
7. Generate QR code
8. Add QR code to PDF
9. Upload PDF to MinIO
10. Update IssuedDocument record
11. Return URL

### 2. Bulk Certificate Queue

**Job Type**: `bulk_certificate`

**Job Data**:
```typescript
{
  templateId: string;
  subjects: Array<{
    subjectId: string;
    subjectType: 'student' | 'staff';
    variables: Record<string, any>;
  }>;
}
```

**Processing Steps**:
1. Load DocumentTemplate
2. Process each subject
3. Generate individual certificates
4. Upload all certificates
5. Update all IssuedDocument records
6. Return URLs

## Puppeteer Configuration

### Browser Launch

```typescript
const browser = await puppeteer.launch({
  headless: 'new',
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
  ],
});
```

### PDF Generation

```typescript
const page = await browser.newPage();
await page.setContent(html, { waitUntil: 'networkidle0' });
const pdfBuffer = await page.pdf({
  format: 'A4',
  printBackground: true,
  margin: {
    top: '20px',
    right: '20px',
    bottom: '20px',
    left: '20px',
  },
});
await page.close();
await browser.close();
```

## Handlebars Templates

### Template Structure

```handlebars
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .header { text-align: center; }
    .content { margin: 20px; }
    .signature { margin-top: 50px; }
  </style>
</head>
<body>
  <div class="header">
    <h1>{{universityName}}</h1>
    <h2>Certificate of Completion</h2>
  </div>
  <div class="content">
    <p>This is to certify that</p>
    <h3>{{studentName}}</h3>
    <p>Enrollment No: {{enrollmentNo}}</p>
    <p>has successfully completed the</p>
    <h3>{{programName}}</h3>
    <p>with {{grade}} grade</p>
    <p>Date: {{date}}</p>
  </div>
  <div class="signature">
    <p>_____________________</p>
    <p>Principal</p>
  </div>
</body>
</html>
```

### Variable Binding

```typescript
const template = Handlebars.compile(templateHtml);
const html = template(variables);
```

## QR Code Generation

### QR Code Library

The system uses `qrcode` package for QR code generation:

```typescript
import QRCode from 'qrcode';

const qrCodeDataUrl = await QRCode.toDataURL(serialNo, {
  width: 200,
  margin: 2,
});
```

### QR Code in PDF

QR code is embedded in the PDF:

```html
<img src="{{qrCode}}" alt="QR Code" />
```

## Serial Number Generation

### ID Format Service

The system uses the IdFormat service for generating serial numbers:

```typescript
const serialNo = await idFormatService.generate('certificate', {
  studentId,
  programmeId,
  batchId,
});
```

### Pattern Example

```
{instShortName}/{courseCode}/{YY}/{SEQ:4}
```

Example: `UNIV/CSC01/24/0001`

## Storage

### MinIO Upload

```typescript
const url = await minioService.upload(
  `certificates/${serialNo}.pdf`,
  pdfBuffer,
  'application/pdf'
);
```

### Document Record Update

```typescript
await prisma.issuedDocument.update({
  where: { id: documentId },
  data: {
    serialNo,
    fileUrl: url,
    qrCode: qrCodeDataUrl,
    status: 'active',
  },
});
```

## Job Flow

### Certificate Generation Flow

```
1. Core API Service
   ↓
2. Add job to queue (Bull)
   ↓
3. Redis stores job
   ↓
4. Cert Generator polls
   ↓
5. Worker processes job
   ↓
6. Load template (Handlebars)
   ↓
7. Bind data
   ↓
8. Render HTML
   ↓
9. Convert to PDF (Puppeteer)
   ↓
10. Generate QR code
   ↓
11. Add QR to PDF
   ↓
12. Upload to MinIO
   ↓
13. Update database
   ↓
14. Return URL
   ↓
15. Mark job complete
```

## Error Handling

### Retry Strategy

```typescript
{
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 5000, // 5s, 10s, 20s
  },
}
```

### Error Logging

```typescript
try {
  await this.generateCertificate(job.data);
} catch (error) {
  this.logger.error('Certificate generation failed', error);
  throw error;
}
```

### Failure Handling

- On failure: Update IssuedDocument status to 'failed'
- On failure: Log error details
- On failure: Notify admin

## Performance Considerations

### Concurrency

```typescript
@Processor('certificates')
export class CertificateProcessor {
  @Process('certificate')
  @Concurrency(2) // Process 2 jobs concurrently (Puppeteer is resource-heavy)
  async handleCertificate(job: Job) {
    await this.generateCertificate(job.data);
  }
}
```

### Resource Management

- **Browser Pool**: Reuse browser instances
- **Memory Limits**: Limit concurrent PDF generation
- **Timeout**: Set timeout for Puppeteer operations

### Optimization

- **Template Caching**: Cache compiled Handlebars templates
- **Font Optimization**: Use system fonts
- **Image Optimization**: Optimize images before embedding

## Docker Configuration

### Service Definition

```yaml
# docker-compose.yml
cert-generator:
  build:
    context: ./apps/cert-generator
    dockerfile: Dockerfile
  ports:
    - "3003:3003"
  depends_on:
    - postgres
    - minio
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
    - MINIO_ENDPOINT=http://minio:9000
    - MINIO_ACCESS_KEY=minioadmin
    - MINIO_SECRET_KEY=minioadmin
    - REDIS_HOST=redis
    - REDIS_PORT=6379
```

### Puppeteer Dependencies

Dockerfile should include Chrome dependencies:

```dockerfile
FROM node:18-alpine

# Install Chrome dependencies
RUN apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont

# Set Puppeteer to use installed Chrome
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
```

## Monitoring

### Health Check

```typescript
async healthCheck(): Promise<boolean> {
  try {
    await this.redis.ping();
    return true;
  } catch (error) {
    return false;
  }
}
```

### Job Metrics

- **Queue size**: Number of pending jobs
- **Processing time**: Average time per certificate
- **Success rate**: Percentage of successful generations
- **Failure rate**: Percentage of failed generations

## Known Limitations

1. **Minimal Implementation**: Current app module is minimal (only ConfigModule)
2. **No Queue Processors Visible**: Actual queue processors not visible in discovery
3. **No Template Engine**: Handlebars integration not visible
4. **No QR Code Integration**: QR code generation not visible
5. **No Serial Number Logic**: ID format integration not visible

## Future Enhancements

1. **Implement Queue Processors**: Add actual job processing logic
2. **Add Template Engine**: Integrate Handlebars for templates
3. **Add QR Code**: Integrate QR code generation
4. **Add Serial Numbers**: Integrate ID format service
5. **Add Watermarks**: Add university watermark to certificates
6. **Add Digital Signatures**: Add digital signature support
7. **Add Batch Processing**: Optimize bulk certificate generation
8. **Add Certificate Verification**: Add certificate verification endpoint
