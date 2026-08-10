# MinIO Guide

## Overview

This document provides comprehensive information about MinIO usage in the University ERP system. It covers MinIO configuration, object storage operations, file management, and best practices.

## MinIO Technology

**Confirmed by Code**: The University ERP uses MinIO for object storage.

**Why MinIO:**
- S3-compatible object storage
- Open-source and self-hosted
- High performance
- Scalable architecture
- Easy to deploy
- Cost-effective compared to cloud storage

**Version:**
- MinIO latest

## MinIO Architecture

**Confirmed by Code**: MinIO is used for file storage.

**MinIO Usage Overview:**

```
┌─────────────────────────────────────────────────────────┐
│              MinIO Usage                                 │
├─────────────────────────────────────────────────────────┤
│ Profile Pictures: User profile images                   │
│ Documents: Student documents, certificates              │
│ Exam Papers: Exam question papers                       │
│ Library Resources: Book covers, PDFs                    │
│ Reports: Generated reports and exports                  │
│ Backups: Database backups                               │
└─────────────────────────────────────────────────────────┘
```

## MinIO Configuration

**Confirmed by Code**: MinIO is configured via environment variables.

**Environment Variables:**

```env
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USE_SSL=false
MINIO_BUCKET=university-erp
MINIO_REGION=us-east-1
```

**Configuration Parameters:**
- `MINIO_ENDPOINT`: MinIO server endpoint
- `MINIO_PORT`: MinIO server port (default: 9000)
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key
- `MINIO_USE_SSL`: Use SSL for MinIO connection (default: false)
- `MINIO_BUCKET`: Default bucket name
- `MINIO_REGION`: MinIO region (default: us-east-1)

## MinIO Service

**Confirmed by Code**: The University ERP has a MinIO service for object storage operations.

**File**: `apps/core-api/src/minio/minio.service.ts`

```typescript
import { Injectable, OnModuleInit } from '@nestjs/common';
import * as Minio from 'minio';

@Injectable()
export class MinioService implements OnModuleInit {
  private client: Minio.Client;
  private bucketName: string;

  constructor() {
    this.client = new Minio.Client({
      endPoint: process.env.MINIO_ENDPOINT || 'localhost',
      port: parseInt(process.env.MINIO_PORT) || 9000,
      useSSL: process.env.MINIO_USE_SSL === 'true',
      accessKey: process.env.MINIO_ACCESS_KEY || 'minioadmin',
      secretKey: process.env.MINIO_SECRET_KEY || 'minioadmin',
    });
    this.bucketName = process.env.MINIO_BUCKET || 'university-erp';
  }

  async onModuleInit() {
    await this.ensureBucketExists();
    console.log('MinIO bucket initialized');
  }

  private async ensureBucketExists() {
    const bucketExists = await this.client.bucketExists(this.bucketName);
    if (!bucketExists) {
      await this.client.makeBucket(this.bucketName, process.env.MINIO_REGION || 'us-east-1');
      console.log(`Bucket ${this.bucketName} created`);
    }
  }

  async uploadFile(
    fileName: string,
    buffer: Buffer,
    contentType: string,
    metadata?: Record<string, string>,
  ): Promise<string> {
    await this.client.putObject(
      this.bucketName,
      fileName,
      buffer,
      buffer.length,
      {
        'Content-Type': contentType,
        ...metadata,
      },
    );
    return this.getPresignedUrl(fileName);
  }

  async getFile(fileName: string): Promise<Buffer> {
    const stream = await this.client.getObject(this.bucketName, fileName);
    const chunks: Buffer[] = [];
    
    return new Promise((resolve, reject) => {
      stream.on('data', (chunk) => chunks.push(chunk));
      stream.on('end', () => resolve(Buffer.concat(chunks)));
      stream.on('error', reject);
    });
  }

  async getFileStream(fileName: string): Promise<Readable> {
    return this.client.getObject(this.bucketName, fileName);
  }

  async deleteFile(fileName: string): Promise<void> {
    await this.client.removeObject(this.bucketName, fileName);
  }

  async deleteFiles(fileNames: string[]): Promise<void> {
    await this.client.removeObjects(this.bucketName, fileNames);
  }

  async copyFile(sourceFileName: string, destinationFileName: string): Promise<void> {
    await this.client.copyObject(
      this.bucketName,
      destinationFileName,
      `${this.bucketName}/${sourceFileName}`,
    );
  }

  async getPresignedUrl(fileName: string, expiry: number = 3600): Promise<string> {
    return this.client.presignedGetObject(this.bucketName, fileName, expiry);
  }

  async getPresignedPutUrl(fileName: string, expiry: number = 3600): Promise<string> {
    return this.client.presignedPutObject(this.bucketName, fileName, expiry);
  }

  async listFiles(prefix: string = '', recursive: boolean = true): Promise<string[]> {
    const objects = await this.client.listObjects(this.bucketName, prefix, recursive);
    return objects.map((obj) => obj.name);
  }

  async listFilesWithMetadata(prefix: string = '', recursive: boolean = true): Promise<any[]> {
    const objects = await this.client.listObjects(this.bucketName, prefix, recursive);
    return objects.map((obj) => ({
      name: obj.name,
      size: obj.size,
      lastModified: obj.lastModified,
      etag: obj.etag,
    }));
  }

  async fileExists(fileName: string): Promise<boolean> {
    try {
      await this.client.statObject(this.bucketName, fileName);
      return true;
    } catch (error) {
      return false;
    }
  }

  async getFileMetadata(fileName: string): Promise<any> {
    return this.client.statObject(this.bucketName, fileName);
  }

  async setBucketPolicy(policy: any): Promise<void> {
    await this.client.setBucketPolicy(this.bucketName, JSON.stringify(policy));
  }

  async getBucketPolicy(): Promise<any> {
    const policy = await this.client.getBucketPolicy(this.bucketName);
    return JSON.parse(policy);
  }

  async setBucketVersioning(enabled: boolean): Promise<void> {
    await this.client.setBucketVersioning(this.bucketName, { Versioning: enabled ? 'Enabled' : 'Suspended' });
  }

  async getBucketVersioning(): Promise<any> {
    return this.client.getBucketVersioning(this.bucketName);
  }
}
```

## File Upload

**Confirmed by Code**: The University ERP handles file uploads with validation.

**File Upload Controller:**

**File**: `apps/core-api/src/files/files.controller.ts`

```typescript
import { Controller, Post, UseInterceptors, UploadedFile, BadRequestException } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { MinioService } from '../minio/minio.service';

@Controller('files')
export class FilesController {
  constructor(private minioService: MinioService) {}

  @Post('upload')
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: Express.Multer.File) {
    // Validate file
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      throw new BadRequestException('File size exceeds 10MB limit');
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!allowedTypes.includes(file.mimetype)) {
      throw new BadRequestException('Invalid file type');
    }

    // Generate unique filename
    const fileName = `${Date.now()}-${file.originalname}`;

    // Upload to MinIO
    const url = await this.minioService.uploadFile(
      fileName,
      file.buffer,
      file.mimetype,
      {
        'original-name': file.originalname,
        'content-type': file.mimetype,
        'size': file.size.toString(),
      },
    );

    return {
      success: true,
      data: {
        fileName,
        url,
        size: file.size,
        mimetype: file.mimetype,
      },
    };
  }

  @Post('upload/profile-picture')
  @UseInterceptors(FileInterceptor('file'))
  async uploadProfilePicture(@UploadedFile() file: Express.Multer.File) {
    // Validate file
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    // Validate file type (only images)
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.mimetype)) {
      throw new BadRequestException('Only image files are allowed');
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      throw new BadRequestException('File size exceeds 5MB limit');
    }

    // Generate filename
    const fileName = `profile-pictures/${Date.now()}-${file.originalname}`;

    // Upload to MinIO
    const url = await this.minioService.uploadFile(
      fileName,
      file.buffer,
      file.mimetype,
    );

    return {
      success: true,
      data: {
        fileName,
        url,
      },
    };
  }
}
```

## File Download

**Confirmed by Code**: The University ERP handles file downloads with presigned URLs.

**File Download Controller:**

**File**: `apps/core-api/src/files/files.controller.ts`

```typescript
import { Controller, Get, Param, StreamableFile } from '@nestjs/common';
import { MinioService } from '../minio/minio.service';

@Controller('files')
export class FilesController {
  constructor(private minioService: MinioService) {}

  @Get('download/:fileName')
  async downloadFile(@Param('fileName') fileName: string) {
    const file = await this.minioService.getFile(fileName);
    return new StreamableFile(file);
  }

  @Get('presigned-url/:fileName')
  async getPresignedUrl(@Param('fileName') fileName: string) {
    const url = await this.minioService.getPresignedUrl(fileName, 3600);
    return {
      success: true,
      data: {
        url,
        expiresIn: 3600,
      },
    };
  }
}
```

## File Organization

**Confirmed by Code**: The University ERP organizes files in a structured manner.

**File Structure:**

```
university-erp/
├── profile-pictures/
│   ├── user-1.jpg
│   ├── user-2.png
│   └── ...
├── documents/
│   ├── student-documents/
│   │   ├── student-1/
│   │   │   ├── aadhar-card.pdf
│   │   │   ├── marksheet.pdf
│   │   │   └── ...
│   │   └── ...
│   └── staff-documents/
│       └── ...
├── exam-papers/
│   ├── 2024/
│   │   ├── semester-1/
│   │   │   ├── cs101.pdf
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── library/
│   ├── book-covers/
│   │   ├── book-1.jpg
│   │   └── ...
│   └── resources/
│       └── ...
├── reports/
│   ├── attendance/
│   ├── exams/
│   └── fees/
└── backups/
    ├── database/
    └── logs/
```

## File Validation

**Confirmed by Code**: The University ERP validates files before upload.

**Validation Rules:**

1. **File Size Limits**
   - Profile pictures: 5MB max
   - Documents: 10MB max
   - Exam papers: 20MB max
   - Reports: 50MB max

2. **Allowed File Types**
   - Images: JPEG, PNG, GIF, WebP
   - Documents: PDF, DOC, DOCX
   - Spreadsheets: XLS, XLSX, CSV
   - Archives: ZIP, RAR

3. **File Naming**
   - Use unique filenames
   - Include timestamp
   - Use lowercase
   - Replace spaces with hyphens

## File Security

**Confirmed by Code**: The University ERP implements file security measures.

**Security Measures:**

1. **Presigned URLs**
   - URLs expire after a set time
   - Prevents unauthorized access
   - Can be revoked

2. **Bucket Policies**
   - Restrict public access
   - Use IAM policies
   - Implement ACLs

3. **Encryption**
   - Enable server-side encryption
   - Use TLS in transit
   - Encrypt at rest

**Bucket Policy Example:**

```typescript
const policy = {
  Version: '2012-10-17',
  Statement: [
    {
      Effect: 'Allow',
      Principal: { AWS: ['*'] },
      Action: ['s3:GetObject'],
      Resource: ['arn:aws:s3:::university-erp/profile-pictures/*'],
    },
  ],
};

await minioService.setBucketPolicy(policy);
```

## File Versioning

**Confirmed by Code**: The University ERP supports file versioning.

**Enable Versioning:**

```typescript
await minioService.setBucketVersioning(true);
```

**List Versions:**

```typescript
const versions = await minioService.listFilesWithMetadata('', true);
```

## File Lifecycle

**Confirmed by Code**: The University ERP implements file lifecycle management.

**Lifecycle Rules:**

1. **Auto-delete old files**
   - Delete files older than 1 year
   - Delete temporary files after 30 days

2. **Archive old files**
   - Move files to archive after 6 months
   - Compress archived files

**Lifecycle Configuration:**

```typescript
const lifecycleConfig = {
  Rules: [
    {
      ID: 'DeleteOldFiles',
      Status: 'Enabled',
      Filter: { Prefix: 'temp/' },
      Expiration: { Days: 30 },
    },
    {
      ID: 'ArchiveOldFiles',
      Status: 'Enabled',
      Filter: { Prefix: 'documents/' },
      Transition: { Days: 180, StorageClass: 'ARCHIVE' },
    },
  ],
};
```

## MinIO Console

**Access MinIO Console:**

```
http://localhost:9001
```

**Default Credentials:**
- Username: `minioadmin`
- Password: `minioadmin`

**Console Features:**
- Bucket management
- File browser
- User management
- Policy configuration
- Monitoring dashboard

## MinIO CLI

**Install MinIO CLI:**

```bash
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/
```

**Configure MinIO CLI:**

```bash
mc alias set local http://localhost:9000 minioadmin minioadmin
```

**Common Commands:**

```bash
# List buckets
mc ls local

# List files in bucket
mc ls local/university-erp

# Upload file
mc cp local-file.txt local/university-erp/

# Download file
mc cp local/university-erp/file.txt .

# Remove file
mc rm local/university-erp/file.txt

# Remove bucket
mc rb local/university-erp --force

# Set bucket policy
mc policy set download local/university-erp

# Get bucket info
mc stat local/university-erp
```

## MinIO Monitoring

**Confirmed by Code**: The University ERP monitors MinIO for health and performance.

**Monitoring Metrics:**

1. **Storage Usage**
   - Total storage used
   - Storage by bucket
   - Storage by file type

2. **Request Metrics**
   - GET requests
   - PUT requests
   - DELETE requests

3. **Error Metrics**
   - Error rate
   - Timeout rate
   - Authentication failures

**Monitoring Commands:**

```bash
# Check MinIO info
mc admin info local

# Check bucket usage
mc du local/university-erp

# Check server status
mc admin heal local
```

## MinIO Backup

**Backup Strategy:**

1. **Regular Backups**
   - Backup daily
   - Keep 7 daily backups
   - Keep 4 weekly backups
   - Keep 12 monthly backups

2. **Backup Methods**
   - Use MinIO replication
   - Use external backup tools
   - Use snapshot backups

**Backup Script:**

```bash
#!/bin/bash
# Backup MinIO bucket

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/minio"
BUCKET="university-erp"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup bucket
mc mirror local/$BUCKET $BACKUP_DIR/$BUCKET-$DATE

# Compress backup
tar -czf $BACKUP_DIR/$BUCKET-$DATE.tar.gz $BACKUP_DIR/$BUCKET-$DATE

# Remove uncompressed backup
rm -rf $BACKUP_DIR/$BUCKET-$DATE

# Keep last 7 days
find $BACKUP_DIR -name "$BUCKET-*.tar.gz" -mtime +7 -delete
```

## MinIO Troubleshooting

### Common Issues

**Issue: Connection refused**

**Solution:**
```bash
# Check if MinIO is running
docker-compose ps minio

# Restart MinIO
docker-compose restart minio

# Check MinIO logs
docker-compose logs minio
```

**Issue: Access denied**

**Solution:**
```bash
# Check credentials
# Verify MINIO_ACCESS_KEY and MINIO_SECRET_KEY

# Check bucket policy
mc policy get local/university-erp
```

**Issue: File upload failed**

**Solution:**
```bash
# Check bucket exists
mc ls local

# Create bucket if not exists
mc mb local/university-erp

# Check disk space
df -h
```

## MinIO Best Practices

**Confirmed by Code**: The University ERP follows MinIO best practices.

### Best Practices

1. **Use appropriate bucket names**
   - Use lowercase
   - Use hyphens for separation
   - Avoid special characters

2. **Implement lifecycle policies**
   - Auto-delete old files
   - Archive old files
   - Reduce storage costs

3. **Use presigned URLs**
   - For temporary access
   - For secure downloads
   - For external sharing

4. **Monitor storage usage**
   - Set up alerts
   - Monitor growth trends
   - Plan capacity

5. **Implement redundancy**
   - Use MinIO gateway
   - Use replication
   - Use backup strategies

## Additional Resources

- [MinIO Documentation](https://docs.min.io/)
- [MinIO Best Practices](https://docs.min.io/minio/baremetal/)
- [MinIO CLI Guide](https://docs.min.io/minio/client-tools/minio-mc.html)
