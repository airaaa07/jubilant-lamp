# University ERP - Storage and MinIO

## Overview

The system uses **MinIO** as the primary object storage solution, with **Azure Blob Storage** as a fallback for cloud deployments. Storage is used for:

- Document uploads (photos, ID proofs, certificates)
- Exam artefacts (proctoring snapshots, exam papers)
- Generated PDFs (certificates, receipts, marksheets)
- User avatars
- Form attachments

## Technology Stack

- **MinIO 7.x**: S3-compatible object storage
- **Azure Blob Storage**: Cloud storage fallback (via @azure/storage-blob)
- **MinIO Client (minio)**: MinIO SDK
- **Azure SDK**: @azure/storage-blob

## Architecture

```
┌─────────────────┐
│   Core API      │
│                 │
│  MinioService   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Backend Switch │
│                 │
│  Azure? MinIO?  │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌────────┐
│ Azure  │ │ MinIO  │
│ Blob   │ │ S3     │
└────────┘ └────────┘
```

## MinIO Service

### Location

- **Module**: `apps/core-api/src/infrastructure/minio/`
- **Service**: `MinioService`
- **Module**: `MinioModule` (global)

### Service Implementation

```typescript
// apps/core-api/src/infrastructure/minio/minio.service.ts
@Injectable()
export class MinioService implements OnModuleInit {
  private readonly useBlob = !!process.env.AZURE_STORAGE_CONNECTION_STRING;
  private client!: Minio.Client;
  private blob?: BlobServiceClient;
  private readonly bucket = process.env.MINIO_BUCKET ?? 'university-erp-docs';
  private readonly examBucket = process.env.MINIO_EXAM_BUCKET ?? 'university-erp-exams';
  private readonly ensured = new Set<string>();
  private readonly storeClients = new Map<string, Minio.Client>();
}
```

### Backend Selection

The service automatically selects the backend based on environment:

```typescript
async onModuleInit() {
  if (this.useBlob) {
    // Azure Blob Storage
    this.blob = BlobServiceClient.fromConnectionString(
      process.env.AZURE_STORAGE_CONNECTION_STRING!
    );
    this.logger.log('Object storage backend: Azure Blob');
  } else {
    // MinIO / S3
    const endpoint = process.env.MINIO_ENDPOINT ?? 'http://minio:9000';
    this.client = new Minio.Client({
      endPoint: url.hostname,
      port: parseInt(url.port || '9000', 10),
      useSSL: url.protocol === 'https:',
      accessKey: process.env.MINIO_ACCESS_KEY ?? '',
      secretKey: process.env.MINIO_SECRET_KEY ?? '',
    });
    this.logger.log('Object storage backend: MinIO/S3');
  }
  await this.ensureBucket(this.bucket);
  await this.ensureBucket(this.examBucket);
}
```

### Buckets

Two logical buckets are used:

1. **Documents Bucket** (`university-erp-docs`)
   - User documents
   - Form attachments
   - Certificates
   - Receipts
   - Marksheets

2. **Exam Bucket** (`university-erp-exams`)
   - Proctoring snapshots
   - Exam papers
   - Exam responses
   - Exam artefacts

### Environment Variables

#### MinIO Configuration

```bash
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams
```

#### Azure Blob Configuration

```bash
AZURE_STORAGE_CONNECTION_STRING=<connection-string>
```

When `AZURE_STORAGE_CONNECTION_STRING` is set, Azure Blob is used instead of MinIO.

## API Methods

### upload()

Upload a file to storage:

```typescript
async upload(
  objectName: string,
  buffer: Buffer,
  mimeType: string,
  bucket: string = this.bucket,
): Promise<string>
```

**Parameters**:
- `objectName`: Path/key for the object
- `buffer`: File content as buffer
- `mimeType`: Content type (e.g., 'image/jpeg')
- `bucket`: Bucket name (default: documents bucket)

**Returns**: Public URL of the uploaded file

**Example**:
```typescript
const url = await minioService.upload(
  'students/photo123.jpg',
  photoBuffer,
  'image/jpeg'
);
```

### download()

Download a file from storage:

```typescript
async download(
  objectName: string,
  bucket: string = this.bucket,
): Promise<Buffer>
```

**Parameters**:
- `objectName`: Path/key for the object
- `bucket`: Bucket name (default: documents bucket)

**Returns**: File content as buffer

**Example**:
```typescript
const buffer = await minioService.download('students/photo123.jpg');
```

### delete()

Delete a file from storage:

```typescript
async delete(
  objectName: string,
  bucket: string = this.bucket,
): Promise<void>
```

**Parameters**:
- `objectName`: Path/key for the object
- `bucket`: Bucket name (default: documents bucket)

**Example**:
```typescript
await minioService.delete('students/photo123.jpg');
```

### getPresignedUrl()

Generate a presigned URL for temporary access:

```typescript
async getPresignedUrl(
  objectName: string,
  expirySeconds = 3600,
  bucket: string = this.bucket,
): Promise<string>
```

**Parameters**:
- `objectName`: Path/key for the object
- `expirySeconds`: URL expiry time in seconds (default: 1 hour)
- `bucket`: Bucket name (default: documents bucket)

**Returns**: Presigned URL

**Example**:
```typescript
const url = await minioService.getPresignedUrl(
  'students/photo123.jpg',
  3600 // 1 hour
);
```

### healthCheck()

Check storage connectivity:

```typescript
async healthCheck(): Promise<boolean>
```

**Returns**: true if storage is accessible

**Usage**: Used by system status page

## External Store Configuration

The service supports configurable S3-compatible external stores:

### ObjectStoreConfig Interface

```typescript
export interface ObjectStoreConfig {
  provider: string;              // minio | s3 | other | gcs | azure
  bucket: string;
  endpoint?: string;
  region?: string;
  accessKeyId?: string;
  secretAccessKey?: string;
}
```

### putToStore()

Upload to any S3-compatible store:

```typescript
async putToStore(
  cfg: ObjectStoreConfig,
  objectName: string,
  buffer: Buffer,
  mimeType: string,
): Promise<void>
```

**Behavior**:
- If `provider: 'minio'` and no endpoint: Uses built-in store (MinIO or Azure)
- Otherwise: Uses configured S3-compatible endpoint

### getFromStore()

Download from any S3-compatible store:

```typescript
async getFromStore(
  cfg: ObjectStoreConfig,
  objectName: string,
): Promise<Buffer>
```

## Usage Patterns

### User Photo Upload

```typescript
// In service
const photoBuffer = Buffer.from(base64Photo, 'base64');
const photoUrl = await minioService.upload(
  `users/${userId}/photo.jpg`,
  photoBuffer,
  'image/jpeg'
);

// Update user record
await prisma.user.update({
  where: { id: userId },
  data: { photoPath: photoUrl },
});
```

### Document Upload

```typescript
// In service
const docBuffer = Buffer.from(base64Doc, 'base64');
const docUrl = await minioService.upload(
  `documents/${studentId}/${documentType}_${Date.now()}.pdf`,
  docBuffer,
  'application/pdf'
);

// Create document record
await prisma.staffDocument.create({
  data: {
    staffId,
    docType,
    name: fileName,
    fileUrl: docUrl,
  },
});
```

### Certificate Generation

```typescript
// In cert-generator worker
const pdfBuffer = await generateCertificate(data);
const certUrl = await minioService.upload(
  `certificates/${serialNo}.pdf`,
  pdfBuffer,
  'application/pdf',
  minioService.documentsBucket
);

// Update issued document
await prisma.issuedDocument.update({
  where: { id: documentId },
  data: { fileUrl: certUrl },
});
```

### Exam Snapshot Upload

```typescript
// In CBE engine
const snapshotBuffer = Buffer.from(base64Image, 'base64');
const snapshotUrl = await minioService.upload(
  `exams/${attemptId}/snapshot_${timestamp}.jpg`,
  snapshotBuffer,
  'image/jpeg',
  minioService.examsBucket
);

// Create exam snapshot record
await prisma.examSnapshot.create({
  data: {
    attemptId,
    fileUrl: snapshotUrl,
    flagged,
    reason,
  },
});
```

### Presigned URL for Download

```typescript
// Generate temporary download link
const downloadUrl = await minioService.getPresignedUrl(
  `documents/${studentId}/marksheet.pdf`,
  86400 // 24 hours
);

// Send to user via email
await mailService.sendEmail({
  to: student.email,
  subject: 'Your Marksheet',
  body: `Download your marksheet: ${downloadUrl}`,
});
```

## Docker Configuration

### MinIO Service

```yaml
# docker-compose.yml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  ports:
    - "9000:9000"
    - "9001:9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  volumes:
    - ./docker-volumes/minio:/data
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    interval: 30s
    timeout: 20s
    retries: 3
```

### Access

- **API**: http://localhost:9000
- **Console**: http://localhost:9001
- **Default Credentials**: minioadmin / minioadmin

## File Naming Conventions

### User Files

```
users/{userId}/photo.jpg
users/{userId}/documents/{docType}_{timestamp}.pdf
```

### Student Files

```
students/{studentId}/photo.jpg
students/{studentId}/documents/{docType}_{timestamp}.pdf
students/{studentId}/marksheets/{termId}.pdf
```

### Staff Files

```
staff/{staffId}/photo.jpg
staff/{staffId}/documents/{docType}_{timestamp}.pdf
```

### Certificate Files

```
certificates/{serialNo}.pdf
certificates/{documentCode}/{serialNo}.pdf
```

### Exam Files

```
exams/{attemptId}/snapshot_{timestamp}.jpg
exams/{examPaperId}/paper.pdf
exams/{batchId}/response_{studentId}.pdf
```

## Security Considerations

### Access Control

- **MinIO**: Uses access key/secret key authentication
- **Azure Blob**: Uses connection string with shared key
- **Presigned URLs**: Temporary access with expiry

### Bucket Policies

MinIO bucket policies should restrict access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "AWS": "*" },
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::university-erp-docs/*"]
    }
  ]
}
```

### Sensitive Data

- **Never store**: Passwords, tokens, secrets in object storage
- **Encrypt**: Encrypt sensitive documents before upload
- **Access Logs**: Enable MinIO access logging

## Performance Considerations

### Upload Optimization

- **Buffer size**: Chunk large files
- **Compression**: Compress before upload
- **Parallel uploads**: Upload multiple files in parallel

### Download Optimization

- **Streaming**: Stream large files instead of loading into memory
- **Caching**: Use CDN or cache frequently accessed files
- **Presigned URLs**: Use presigned URLs instead of proxying

### Storage Optimization

- **Lifecycle policies**: Auto-delete old files
- **Compression**: Enable MinIO compression
- **Tiering**: Move old files to cold storage

## Backup Strategy

### MinIO Backup

```bash
# Backup MinIO data
mc mirror minio/university-erp-docs /backup/university-erp-docs

# Restore MinIO data
mc mirror /backup/university-erp-docs minio/university-erp-docs
```

### Docker Volume Backup

```bash
# Backup Docker volume
docker run --rm -v docker-volumes_minio:/data -v $(pwd):/backup \
  alpine tar czf /backup/minio-backup.tar.gz /data
```

## Monitoring

### Health Check

```typescript
async healthCheck(): Promise<boolean> {
  if (this.useBlob) {
    return this.blob!.getContainerClient(this.bucket).exists();
  }
  return this.client.bucketExists(this.bucket);
}
```

### Metrics

- **Upload count**: Track upload operations
- **Download count**: Track download operations
- **Storage usage**: Monitor bucket size
- **Error rate**: Track failed operations

## Known Limitations

1. **No CDN Integration**: No CDN configured for static assets
2. **No Lifecycle Policies**: No automatic file deletion
3. **No Encryption at Rest**: Files stored unencrypted
4. **No Versioning**: No file versioning enabled
5. **No Multi-Region**: Single region deployment

## Future Enhancements

1. **CDN Integration**: Add CloudFront/Cloudflare CDN
2. **Lifecycle Policies**: Auto-delete old files
3. **Encryption**: Enable server-side encryption
4. **Versioning**: Enable file versioning
5. **Multi-Region**: Multi-region replication
6. **Compression**: Automatic compression
7. **Thumbnail Generation**: Auto-generate thumbnails
8. **Virus Scanning**: Scan uploaded files
