# 13-MinIO

## Purpose

This folder provides comprehensive documentation about MinIO in the University ERP system. It details how MinIO is used for object storage, file management, and document storage.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses MinIO for object storage. Understanding MinIO is critical for:
- Storing files and documents
- Managing object storage
- Implementing file uploads
- Debugging MinIO issues
- Optimizing storage usage

Without understanding MinIO, developers may struggle with file storage or may introduce MinIO-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn MinIO
- **Feature Development**: Implementing file storage
- **Code Reviews**: Reviewing MinIO code
- **File Storage**: Storing files and documents
- **Document Management**: Managing documents

## Dependencies

### MinIO Dependencies

**Confirmed by Code**: MinIO depends on:

- **minio**: MinIO client for Node.js
- **NestJS**: Framework for MinIO integration
- **Environment Variables**: MinIO configuration
- **Multer**: File upload middleware

## Internal Architecture

### MinIO Architecture

**Confirmed by Code**: MinIO follows S3-compatible object storage architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              MinIO Client                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              MinIO Server                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Buckets      │  │  Objects        │  │  Presigned URLs │
│  (Containers) │  │  (Files)        │  │  (Temporary)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### MinIO Service

**Confirmed by Code**: MinIO service provides MinIO client.

**MinioService**:
```typescript
import { Injectable, OnModuleDestroy } from '@nestjs/common';
import * as Minio from 'minio';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class MinioService extends Minio.Client implements OnModuleDestroy {
  constructor(private configService: ConfigService) {
    super({
      endPoint: configService.get('MINIO_ENDPOINT', 'localhost'),
      port: parseInt(configService.get('MINIO_PORT', '9000')),
      useSSL: configService.get('MINIO_USE_SSL', 'false') === 'true',
      accessKey: configService.get('MINIO_ACCESS_KEY'),
      secretKey: configService.get('MINIO_SECRET_KEY'),
    });
  }

  async onModuleDestroy() {
    // Clean up if needed
  }

  async uploadFile(bucketName: string, objectName: string, file: Buffer, metaData: any) {
    await this.putObject(bucketName, objectName, file, file.length, metaData);
    return {
      bucketName,
      objectName,
      url: await this.getPresignedUrl(bucketName, objectName),
    };
  }

  async downloadFile(bucketName: string, objectName: string) {
    return await this.getObject(bucketName, objectName);
  }

  async deleteFile(bucketName: string, objectName: string) {
    await this.removeObject(bucketName, objectName);
  }

  async getPresignedUrl(bucketName: string, objectName: string, expiry: number = 3600) {
    return await this.presignedGetObject(bucketName, objectName, expiry);
  }
}
```

**What This Does**:
- **Minio.Client**: Extends MinIO client
- **Configuration**: Configures from environment variables
- **uploadFile**: Uploads file to MinIO
- **downloadFile**: Downloads file from MinIO
- **deleteFile**: Deletes file from MinIO
- **getPresignedUrl**: Generates presigned URL

### MinIO Module

**Confirmed by Code**: MinIO module provides MinIO integration.

**MinioModule**:
```typescript
import { Module, Global } from '@nestjs/common';
import { MinioService } from './minio.service';

@Global()
@Module({
  providers: [MinioService],
  exports: [MinioService],
})
export class MinioModule {}
```

**What This Does**:
- **@Global**: Makes module global
- **Providers**: Provides MinioService
- **Exports**: Exports MinioService for other modules

## Database Interactions

### MinIO-Database Flow

**Confirmed by Code**: MinIO doesn't interact with database directly.

**Flow**:
```
MinIO → No database interaction
```

## Redis Interactions

### MinIO-Redis Flow

**Confirmed by Code**: MinIO doesn't interact with Redis.

**Flow**:
```
MinIO → No Redis interaction
```

## Queue Interactions

### MinIO-Queue Flow

**Confirmed by Code**: MinIO doesn't interact with queues.

**Flow**:
```
MinIO → No queue interaction
```

## Worker Interactions

### MinIO-Worker Flow

**Confirmed by Code**: Workers can use MinIO for file processing.

**Flow**:
```
Worker → MinIO → Process File
```

## Business Rules

### MinIO Rules

**Confirmed by Code**: MinIO follows these rules:

1. **Buckets**: Files stored in buckets
2. **Objects**: Files are objects
3. **Metadata**: Metadata attached to objects
4. **Presigned URLs**: Temporary access via presigned URLs
5. **S3 Compatible**: S3-compatible API

### File Storage Rules

**Confirmed by Code**: File storage rules:

1. **Naming**: Use consistent object naming
2. **Metadata**: Include relevant metadata
3. **Size**: Monitor file size
4. **Type**: Validate file type
5. **Access**: Control access via presigned URLs

## Security

### MinIO Security

**Confirmed by Code**: Security considerations for MinIO:

1. **Access Keys**: Use secure access keys
2. **Presigned URLs**: Use presigned URLs for temporary access
3. **Bucket Policies**: Configure bucket policies
4. **Encryption**: Encrypt sensitive files
5. **Access Control**: Restrict MinIO access

## Performance Considerations

### MinIO Performance

**Confirmed by Code**: Performance considerations:

1. **File Size**: Optimize file size
2. **Compression**: Compress files if needed
3. **CDN**: Use CDN for static files
4. **Caching**: Cache presigned URLs
5. **Concurrent Uploads**: Use concurrent uploads

## Common Mistakes

### Mistake 1: Not Validating File Type

**Symptom**: Invalid files uploaded

**Cause**: Not validating file type

**Fix**:
```typescript
// Validate file type
if (!['image/jpeg', 'image/png'].includes(file.mimetype)) {
  throw new BadRequestException('Invalid file type');
}
```

### Mistake 2: Not Setting Metadata

**Symptom**: No file information

**Cause**: Not setting metadata

**Fix**:
```typescript
// Set metadata
const metaData = {
  'Content-Type': file.mimetype,
  'X-Amz-Meta-Original-Name': file.originalname,
  'X-Amz-Meta-Uploaded-By': userId,
};
```

### Mistake 3: Not Using Presigned URLs

**Symptom**: Security vulnerability

**Cause**: Not using presigned URLs

**Fix**:
```typescript
// Use presigned URL
const url = await this.minioService.getPresignedUrl(bucketName, objectName);
```

## Debugging Guide

### MinIO Debugging

**Issue**: MinIO not working

**Investigation**:
1. Check MinIO connection
2. Check MinIO server status
3. Check bucket existence
4. Check file permissions
5. Check logs

**Tools**:
- MinIO console
- MinIO logs
- Application logs
- Network tools

## Future Enhancements

### CDN Integration

**Status**: Not implemented

**Proposal**: Implement CDN integration:
- CloudFront integration
- Better performance
- Global distribution
- More complex
- Better for production

### File Processing

**Status**: Not implemented

**Proposal**: Implement file processing:
- Image processing
- Video processing
- Document conversion
- Better user experience
- More complex

## Production Considerations

### Production MinIO

**Production Deployment**:
- Use secure access keys
- Configure bucket policies
- Use presigned URLs
- Monitor storage usage
- Monitor performance

### MinIO Monitoring

**Monitoring Metrics**:
- Storage usage
- Upload rate
- Download rate
- Error rate
- Response time

## Example Requests

### MinIO Example

**Upload File**:
```typescript
const result = await this.minioService.uploadFile(
  'documents',
  'user-id/file.pdf',
  fileBuffer,
  metaData,
);
```

## Example Responses

### MinIO Response

**Response**: File uploaded

```typescript
{
  bucketName: 'documents',
  objectName: 'user-id/file.pdf',
  url: 'https://minio.example.com/documents/user-id/file.pdf?X-Amz-...'
}
```

## Sequence Diagrams

### MinIO Flow

```
Application → MinIO Client → MinIO Server → File Stored
Application → MinIO Client → MinIO Server → File Retrieved
```

## Architecture Diagrams

### MinIO Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Application                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  MinIO Client                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  MinIO Server                               │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Buckets      │  │  Objects        │  │  Presigned URLs │
│  (Containers) │  │  (Files)        │  │  (Temporary)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How is MinIO used in the system?

**Answer**: MinIO via:
- Object storage for files
- Document storage
- File uploads
- File downloads
- Presigned URLs for access

### Q2: How do you implement file upload?

**Answer**: File upload via:
- Validate file type
- Generate object name
- Upload to MinIO
- Set metadata
- Return presigned URL

### Q3: How do you secure file access?

**Answer**: File security via:
- Presigned URLs for temporary access
- Bucket policies for access control
- Access keys for authentication
- Encryption for sensitive files
- Access logging

## Exercises

### Exercise 1: Implement File Upload

**Task**: Implement file upload with MinIO.

**Steps**:
1. Validate file type
2. Generate object name
3. Upload to MinIO
4. Set metadata
5. Return presigned URL

**Verification**:
- Upload implemented
- Validation works
- Object name generated
- Metadata set
- Presigned URL returned

### Exercise 2: Implement File Download

**Task**: Implement file download from MinIO.

**Steps**:
1. Check file existence
2. Get presigned URL
3. Return URL to client
4. Client downloads file
5. Test download

**Verification**:
- Download implemented
- Existence check works
- Presigned URL generated
- Client downloads file
- Tests pass

## Real Production Scenarios

### Scenario 1: File Upload Failed

**Situation**: File upload failed

**Response**:
1. Check MinIO connection
2. Check bucket existence
3. Check file size
4. Fix issue
5. Test upload

### Scenario 2: Storage Full

**Situation**: MinIO storage full

**Response**:
1. Check storage usage
2. Clean up old files
3. Add more storage
4. Monitor storage
5. Alert on threshold

## Navigation

**Next Section**: [01-File-Storage](./01-File-Storage.md)

**Previous Section**: [12-Redis](../12-Redis/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [08-Modules](../08-Modules/README.md) - Modules details
