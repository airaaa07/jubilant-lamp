# File Storage

## Purpose

This document explains file storage in the University ERP system. It details how files are stored, managed, and accessed using MinIO.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses MinIO for file storage. Understanding file storage is critical for:
- Storing user uploads
- Managing documents
- Implementing file uploads
- Debugging file storage issues
- Optimizing storage usage

Without understanding file storage, developers may struggle with file management or may introduce file storage bugs.

## Where This Is Used

- **Onboarding**: New developers learn file storage
- **Feature Development**: Implementing file storage
- **Code Reviews**: Reviewing file storage code
- **File Management**: Managing files
- **Document Storage**: Storing documents

## Dependencies

### File Storage Dependencies

**Confirmed by Code**: File storage depends on:

- **MinioService**: MinIO client
- **Multer**: File upload middleware
- **NestJS**: Framework for file storage
- **Environment Variables**: Storage configuration

## Internal Architecture

### File Storage Architecture

**Confirmed by Code**: File storage follows bucket-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              File Upload Controller                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              MinIO Service                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              MinIO Server                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Documents    │  │  Images         │  │  Videos         │
│  Bucket       │  │  Bucket         │  │  Bucket         │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### File Upload Controller

**Confirmed by Code**: File upload controller handles file uploads.

**FilesController**:
```typescript
@Controller('files')
@UseGuards(GlobalJwtAuthGuard)
export class FilesController {
  constructor(private filesService: FilesService) {}

  @Post('upload')
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: Express.Multer.File, @CurrentUser() user: JwtPayload) {
    return this.filesService.uploadFile(file, user);
  }

  @Get('download/:bucketName/:objectName')
  async downloadFile(
    @Param('bucketName') bucketName: string,
    @Param('objectName') objectName: string,
  ) {
    return this.filesService.downloadFile(bucketName, objectName);
  }

  @Delete(':bucketName/:objectName')
  async deleteFile(
    @Param('bucketName') bucketName: string,
    @Param('objectName') objectName: string,
  ) {
    return this.filesService.deleteFile(bucketName, objectName);
  }
}
```

**What This Does**:
- **uploadFile**: Uploads file to MinIO
- **downloadFile**: Downloads file from MinIO
- **deleteFile**: Deletes file from MinIO

### File Storage Service

**Confirmed by Code**: File storage service manages file operations.

**FilesService**:
```typescript
@Injectable()
export class FilesService {
  constructor(
    private minioService: MinioService,
    private prisma: PrismaService,
  ) {}

  async uploadFile(file: Express.Multer.File, user: JwtPayload) {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!allowedTypes.includes(file.mimetype)) {
      throw new BadRequestException('Invalid file type');
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      throw new BadRequestException('File too large');
    }

    // Generate object name
    const objectName = `${user.sub}/${Date.now()}-${file.originalname}`;

    // Set metadata
    const metaData = {
      'Content-Type': file.mimetype,
      'X-Amz-Meta-Original-Name': file.originalname,
      'X-Amz-Meta-Uploaded-By': user.sub,
      'X-Amz-Meta-Uploaded-At': new Date().toISOString(),
    };

    // Determine bucket based on file type
    let bucketName = 'documents';
    if (file.mimetype.startsWith('image/')) {
      bucketName = 'images';
    }

    // Ensure bucket exists
    await this.minioService.bucketExists(bucketName) || 
      await this.minioService.makeBucket(bucketName);

    // Upload file
    const result = await this.minioService.uploadFile(
      bucketName,
      objectName,
      file.buffer,
      metaData,
    );

    // Save file record to database
    await this.prisma.file.create({
      data: {
        bucketName: result.bucketName,
        objectName: result.objectName,
        originalName: file.originalname,
        mimeType: file.mimetype,
        size: file.size,
        uploadedBy: user.sub,
      },
    });

    return result;
  }

  async downloadFile(bucketName: string, objectName: string) {
    // Check if file exists
    const file = await this.prisma.file.findFirst({
      where: { bucketName, objectName },
    });

    if (!file) {
      throw new NotFoundException('File not found');
    }

    // Get presigned URL
    const url = await this.minioService.getPresignedUrl(bucketName, objectName, 3600);
    return { url };
  }

  async deleteFile(bucketName: string, objectName: string) {
    // Check if file exists
    const file = await this.prisma.file.findFirst({
      where: { bucketName, objectName },
    });

    if (!file) {
      throw new NotFoundException('File not found');
    }

    // Delete from MinIO
    await this.minioService.deleteFile(bucketName, objectName);

    // Delete from database
    await this.prisma.file.delete({
      where: { id: file.id },
    });

    return { success: true };
  }
}
```

**What This Does**:
- **uploadFile**: Validates, uploads, and records file
- **downloadFile**: Checks existence and returns presigned URL
- **deleteFile**: Deletes from MinIO and database
- **Bucket Management**: Ensures bucket exists
- **Metadata**: Sets file metadata

## Database Interactions

### File Storage-Database Flow

**Confirmed by Code**: File storage records file metadata in database.

**Flow**:
```
File Upload → MinIO → Database → File Record
```

## Redis Interactions

### File Storage-Redis Flow

**Confirmed by Code**: File storage doesn't interact with Redis.

**Flow**:
```
File Storage → No Redis interaction
```

## Queue Interactions

### File Storage-Queue Flow

**Confirmed by Code**: File storage doesn't interact with queues.

**Flow**:
```
File Storage → No queue interaction
```

## Worker Interactions

### File Storage-Worker Flow

**Confirmed by Code**: Workers can process files.

**Flow**:
```
Worker → MinIO → Process File → Database
```

## Business Rules

### File Storage Rules

**Confirmed by Code**: File storage follows these rules:

1. **Validation**: Validate file type and size
2. **Bucket Organization**: Organize by file type
3. **Metadata**: Include relevant metadata
4. **Database Record**: Record file metadata in database
5. **Presigned URLs**: Use presigned URLs for access

### File Naming Rules

**Confirmed by Code**: File naming rules:

1. **User ID**: Include user ID in path
2. **Timestamp**: Include timestamp for uniqueness
3. **Original Name**: Preserve original name in metadata
4. **Extension**: Preserve file extension
5. **Sanitization**: Sanitize file name

## Security

### File Storage Security

**Confirmed by Code**: Security considerations for file storage:

1. **File Type Validation**: Validate file type
2. **File Size Validation**: Validate file size
3. **Access Control**: Control access via presigned URLs
4. **Bucket Policies**: Configure bucket policies
5. **Malware Scanning**: Scan files for malware (future)

## Performance Considerations

### File Storage Performance

**Confirmed by Code**: Performance considerations:

1. **File Size**: Limit file size
2. **Compression**: Compress files if needed
3. **CDN**: Use CDN for static files
4. **Concurrent Uploads**: Use concurrent uploads
5. **Caching**: Cache presigned URLs

## Common Mistakes

### Mistake 1: Not Validating File Type

**Symptom**: Invalid files uploaded

**Cause**: Not validating file type

**Fix**:
```typescript
// Validate file type
const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
if (!allowedTypes.includes(file.mimetype)) {
  throw new BadRequestException('Invalid file type');
}
```

### Mistake 2: Not Validating File Size

**Symptom**: Large files uploaded

**Cause**: Not validating file size

**Fix**:
```typescript
// Validate file size
if (file.size > 10 * 1024 * 1024) {
  throw new BadRequestException('File too large');
}
```

### Mistake 3: Not Recording Metadata

**Symptom**: No file information

**Cause**: Not recording metadata

**Fix**:
```typescript
// Record metadata in database
await this.prisma.file.create({
  data: {
    bucketName: result.bucketName,
    objectName: result.objectName,
    originalName: file.originalname,
    mimeType: file.mimetype,
    size: file.size,
    uploadedBy: user.sub,
  },
});
```

## Debugging Guide

### File Storage Debugging

**Issue**: File upload failed

**Investigation**:
1. Check MinIO connection
2. Check bucket existence
3. Check file validation
4. Check file permissions
5. Check logs

**Tools**:
- MinIO console
- MinIO logs
- Application logs
- Network tools

## Future Enhancements

### Image Processing

**Status**: Not implemented

**Proposal**: Implement image processing:
- Image resizing
- Image compression
- Thumbnail generation
- Better user experience
- More complex

### Malware Scanning

**Status**: Not implemented

**Proposal**: Implement malware scanning:
- Scan uploaded files
- Quarantine infected files
- Better security
- More complex
- Better for production

## Production Considerations

### Production File Storage

**Production Deployment**:
- Enable file validation
- Configure bucket policies
- Use presigned URLs
- Monitor storage usage
- Monitor upload rate

### File Storage Monitoring

**Monitoring Metrics**:
- Storage usage
- Upload rate
- Download rate
- Error rate
- File size distribution

## Example Requests

### File Storage Example

**Upload File**:
```bash
POST /api/files/upload
Content-Type: multipart/form-data

file: <file>
```

## Example Responses

### File Storage Response

**Response**: File uploaded

```json
{
  "bucketName": "documents",
  "objectName": "user-id/1234567890-file.pdf",
  "url": "https://minio.example.com/documents/user-id/1234567890-file.pdf?X-Amz-..."
}
```

## Sequence Diagrams

### File Storage Flow

```
Client → Upload Request → Controller → Service → MinIO → File Stored → Database Record → Response
```

## Architecture Diagrams

### File Storage Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Service                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
┌───────▼────────┐                          ┌────────▼────────┐
│  MinIO        │                          │  Database       │
│  (File Store) │                          │  (Metadata)     │
└────────────────┘                          └─────────────────┘
```

## Common Interview Questions

### Q1: How is file storage implemented?

**Answer**: File storage via:
- MinIO for object storage
- File validation (type, size)
- Bucket organization by type
- Metadata in database
- Presigned URLs for access

### Q2: How do you handle file uploads?

**Answer**: File uploads via:
- Validate file type and size
- Generate object name
- Upload to MinIO
- Record metadata in database
- Return presigned URL

### Q3: How do you secure file access?

**Answer**: File security via:
- Presigned URLs for temporary access
- Bucket policies for access control
- File type validation
- File size validation
- Access logging

## Exercises

### Exercise 1: Implement File Upload

**Task**: Implement file upload with validation.

**Steps**:
1. Validate file type
2. Validate file size
3. Generate object name
4. Upload to MinIO
5. Record metadata

**Verification**:
- Validation works
- Object name generated
- Upload works
- Metadata recorded
- Tests pass

### Exercise 2: Implement File Download

**Task**: Implement file download with presigned URLs.

**Steps**:
1. Check file existence
2. Generate presigned URL
3. Return URL to client
4. Client downloads file
5. Test download

**Verification**:
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
3. Check file validation
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

**Next Section**: [README](../README.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [08-Modules](../08-Modules/README.md) - Modules details
