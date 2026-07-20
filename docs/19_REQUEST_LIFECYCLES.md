# University ERP - Request Lifecycles

## Overview

This document describes the complete lifecycle of requests as they flow through the University ERP system, from the initial user action to the final response.

## HTTP Request Lifecycle

### 1. User Action

```
User clicks button / submits form / navigates
    ↓
React Component
    ↓
Event Handler
```

### 2. Frontend Processing

```
Event Handler
    ↓
Form Validation (Zod)
    ↓
API Call (axios)
    ↓
Add Authorization Header (if token exists)
```

### 3. HTTP Request

```
axios.request({
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE',
  url: '/api/endpoint',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  data: requestBody,
})
    ↓
Network Request
```

### 4. Nginx (Production)

```
HTTP Request → Nginx
    ↓
Reverse Proxy
    ↓
Route to appropriate service
    ↓
Forward to Core API
```

### 5. Core API Entry

```
HTTP Request → NestJS Application
    ↓
Express Middleware Chain
    ↓
1. Body Parser (20mb limit)
    ↓
2. Helmet (Security Headers)
    ↓
3. CORS
    ↓
4. Strip Null Bytes
    ↓
5. Request Context (Async Local Storage)
```

### 6. Global Guards

```
Request Context
    ↓
GlobalJwtAuthGuard
    ↓
Check @Public decorator
    ↓
If public: Skip auth
    ↓
If not public: Validate JWT
    ↓
Attach user to request
```

### 7. Route Matching

```
NestJS Router
    ↓
Match route pattern
    ↓
Select Controller
    ↓
Select Method
```

### 8. Controller Guards

```
Controller Method
    ↓
@UseGuards decorators
    ↓
JwtAuthGuard (if present)
    ↓
ScopeGuard (if present)
    ↓
Check permissions
```

### 9. DTO Validation

```
Controller Method
    ↓
@Body(new ZodValidationPipe(Schema))
    ↓
Zod Schema Validation
    ↓
If invalid: Throw BadRequestException
    ↓
If valid: Continue
```

### 10. Controller Execution

```
Controller Method
    ↓
Extract parameters (@Param, @Query, @Body, @CurrentUser)
    ↓
Call Service method
    ↓
await service.method(data, user)
```

### 11. Service Processing

```
Service Method
    ↓
Business Logic
    ↓
1. Input validation
    ↓
2. Authorization check
    ↓
3. Business rules
    ↓
4. Database operations (Prisma)
    ↓
5. Cache operations (Redis)
    ↓
6. External service calls (MinIO, Email, SMS)
    ↓
7. Queue jobs (Bull)
    ↓
8. Notifications
```

### 12. Database Operations

```
PrismaService
    ↓
Prisma Client
    ↓
Query Builder
    ↓
SQL Generation
    ↓
PostgreSQL Execution
    ↓
Result Parsing
    ↓
Type Conversion
    ↓
Return to Service
```

### 13. Audit Logging

```
Prisma Middleware
    ↓
Intercept write operations
    ↓
Extract actor from request context
    ↓
Compute field changes
    ↓
Redact sensitive fields
    ↓
Create AuditLog record
    ↓
Best-effort (don't block)
```

### 14. Cache Operations

```
RedisService
    ↓
Check cache
    ↓
If cache hit: Return cached data
    ↓
If cache miss: Fetch from database
    ↓
Set cache
    ↓
Return data
```

### 15. External Service Calls

```
MinioService
    ↓
Upload/Download/Delete
    ↓
MinIO/Azure Blob
    ↓
Return URL/Buffer

MailService
    ↓
Send email
    ↓
SMTP Server
    ↓
Return success/failure

SmsService
    ↓
Send SMS
    ↓
SMS Gateway
    ↓
Return success/failure
```

### 16. Queue Jobs

```
Service
    ↓
Add job to queue
    ↓
Bull Queue
    ↓
Redis Storage
    ↓
Worker Polling
    ↓
Worker Processing
    ↓
Async Execution
```

### 17. Response Construction

```
Service
    ↓
Return data
    ↓
Controller
    ↓
Wrap in response object
    ↓
{
  success: true,
  data: result,
  meta: { page, limit, total }
}
```

### 18. Exception Handling

```
If error occurs:
    ↓
Service throws exception
    ↓
HttpExceptionFilter catches
    ↓
Normalize error
    ↓
Map Prisma errors to HTTP status
    ↓
Return error response
    ↓
{
  success: false,
  message: error message,
  statusCode: 400,
  error: 'Bad Request'
}
```

### 19. HTTP Response

```
NestJS Response
    ↓
Express Response
    ↓
HTTP Headers
    ↓
Body
    ↓
Status Code
```

### 20. Frontend Response Handling

```
axios response
    ↓
Response interceptor
    ↓
Check status code
    ↓
If 401: Attempt token refresh
    ↓
If refresh success: Retry original request
    ↓
If refresh fail: Logout and redirect
    ↓
Return data to component
```

### 21. Component Update

```
React Component
    ↓
React Query cache update
    ↓
State update
    ↓
Re-render
    ↓
UI Update
```

## WebSocket Request Lifecycle (CBE Engine)

### 1. Connection Establishment

```
React Component
    ↓
Socket.IO Client
    ↓
WebSocket Connection
    ↓
ws://localhost:3001
```

### 2. Authentication

```
WebSocket Connection
    ↓
Send authentication event
    ↓
{ type: 'auth', token: accessToken }
    ↓
CBE Engine validates token
    ↓
Attach user to socket
    ↓
Join exam room
```

### 3. Event Flow

```
React Component
    ↓
Send event via WebSocket
    ↓
socket.emit('exam:answer', { answer })
    ↓
CBE Engine receives event
    ↓
Validate user
    ↓
Process answer
    ↓
Store in database
    ↓
Emit response
    ↓
socket.emit('exam:answer:ack', { success: true })
    ↓
React Component receives ack
    ↓
Update UI
```

### 4. Proctoring Events

```
React Component
    ↓
Capture webcam snapshot
    ↓
Upload to MinIO
    ↓
Send event via WebSocket
    ↓
socket.emit('exam:snapshot', { url })
    ↓
CBE Engine stores snapshot
    ↓
Detect violations
    ↓
If violation: Send directive
    ↓
socket.emit('exam:directive', { type: 'warning' })
    ↓
React Component shows warning
```

### 5. Exam Submission

```
React Component
    ↓
Submit exam
    ↓
socket.emit('exam:submit', { answers })
    ↓
CBE Engine processes submission
    ↓
Close WebSocket connection
    ↓
Trigger auto-grading
    ↓
Return results
```

## Background Job Lifecycle

### 1. Job Creation

```
Service
    ↓
Add job to queue
    ↓
queue.add('job-type', data, options)
    ↓
Bull stores job in Redis
    ↓
Job status: waiting
```

### 2. Job Processing

```
Worker polls queue
    ↓
Fetch next job
    ↓
Job status: active
    ↓
Process job
    ↓
Execute business logic
    ↓
If success:
    - Job status: completed
    - Remove from queue (after N jobs)
    ↓
If failure:
    - Job status: failed
    - Retry with backoff
    - After max retries: Move to dead letter queue
```

### 3. Job Completion

```
Worker completes job
    ↓
Update job status
    ↓
Notify queue
    ↓
Queue removes job (after N completed jobs)
    ↓
Worker fetches next job
```

## Authentication Token Lifecycle

### 1. Token Generation

```
User logs in
    ↓
AuthService.login()
    ↓
Generate access token (15 min)
    ↓
Generate refresh token (7 days)
    ↓
Store refresh token in database
    ↓
Store refresh token in Redis
    ↓
Return tokens to client
```

### 2. Token Storage

```
Client receives tokens
    ↓
Store in localStorage
    ↓
accessToken: "eyJhbGc..."
    ↓
refreshToken: "eyJhbGc..."
```

### 3. Token Usage

```
Client makes request
    ↓
Add Authorization header
    ↓
Bearer eyJhbGc...
    ↓
Server validates token
    ↓
Extract user payload
    ↓
Attach user to request
```

### 4. Token Refresh

```
Access token expires
    ↓
Client sends refresh request
    ↓
POST /api/auth/refresh
    ↓
AuthService.refreshToken()
    ↓
Validate refresh token
    ↓
Generate new access token
    ↓
Return new access token
    ↓
Client updates localStorage
```

### 5. Token Revocation

```
User logs out
    ↓
AuthService.logout()
    ↓
Delete refresh token from database
    ↓
Delete refresh token from Redis
    ↓
Client clears localStorage
    ↓
Redirect to login
```

## Database Transaction Lifecycle

### 1. Transaction Start

```
Service
    ↓
prisma.$transaction(async (tx) => {
    ↓
Transaction context created
    ↓
All operations use tx instead of prisma
```

### 2. Transaction Operations

```
tx.create()
    ↓
tx.update()
    ↓
tx.delete()
    ↓
All operations are atomic
```

### 3. Transaction Commit

```
All operations succeed
    ↓
Transaction commits
    ↓
Changes persisted
    ↓
Return result
```

### 4. Transaction Rollback

```
Any operation fails
    ↓
Transaction rolls back
    ↓
All changes discarded
    ↓
Error thrown
```

## File Upload Lifecycle

### 1. File Selection

```
User selects file
    ↓
React Component
    ↓
File input change event
    ↓
Get file object
```

### 2. File Processing

```
File object
    ↓
Read as base64 or ArrayBuffer
    ↓
Validate file type
    ↓
Validate file size
    ↓
Convert to Buffer
```

### 3. Upload Request

```
axios.post('/api/upload', {
  file: base64String,
  fileName: 'photo.jpg',
  mimeType: 'image/jpeg',
})
```

### 4. Server Processing

```
Controller receives request
    ↓
Service processes upload
    ↓
MinioService.upload()
    ↓
Upload to MinIO
    ↓
Get public URL
    ↓
Return URL to client
```

### 5. URL Storage

```
Client receives URL
    ↓
Store URL in form data
    ↓
Submit form with URL
    ↓
Server stores URL in database
```

## Error Lifecycle

### 1. Error Occurrence

```
Error occurs in service
    ↓
throw new BadRequestException('Invalid input')
```

### 2. Error Propagation

```
Service throws error
    ↓
Controller receives error
    ↓
HttpExceptionFilter catches error
```

### 3. Error Normalization

```
HttpExceptionFilter
    ↓
Check error type
    ↓
Map to HTTP status code
    ↓
Format error response
```

### 4. Error Response

```
{
  success: false,
  message: 'Invalid input',
  statusCode: 400,
  error: 'Bad Request'
}
```

### 5. Frontend Error Handling

```
axios error interceptor
    ↓
Check error response
    ↓
Show error message to user
    ↓
Log error
```

## Cache Lifecycle

### 1. Cache Miss

```
Service requests data
    ↓
Check Redis cache
    ↓
Cache miss
    ↓
Fetch from database
    ↓
Store in Redis (with TTL)
    ↓
Return data
```

### 2. Cache Hit

```
Service requests data
    ↓
Check Redis cache
    ↓
Cache hit
    ↓
Return cached data
    ↓
Skip database query
```

### 3. Cache Invalidation

```
Data updated
    ↓
Delete cache key
    ↓
Next request will fetch fresh data
```

## Notification Lifecycle

### 1. Notification Creation

```
Service creates notification
    ↓
PrismaService.create()
    ↓
Create Notification record
    ↓
Add job to queue
```

### 2. Queue Processing

```
Notification Worker polls queue
    ↓
Fetch notification job
    ↓
Process job
    ↓
Send email/SMS
    ↓
Update notification status
```

### 3. Delivery

```
Email sent via SMTP
    ↓
SMS sent via gateway
    ↓
Update notification status to 'delivered'
```

## Workflow Lifecycle

### 1. Workflow Start

```
User initiates workflow
    ↓
Create WorkflowInstance
    ↓
Set initial state
    ↓
Create initial task(s)
    ↓
Send notifications
```

### 2. Task Assignment

```
Workflow state requires action
    ↓
Create WorkflowTask
    ↓
Assign to actor (role or user)
    ↓
Send notification
```

### 3. Task Action

```
Actor views task
    ↓
Actor fills form
    ↓
Actor selects decision
    ↓
Submit task
```

### 4. State Transition

```
Service validates decision
    ↓
Find matching transition
    ↓
Execute entry actions
    ↓
Create next task(s)
    ↓
Update WorkflowInstance state
```

### 5. Workflow Completion

```
Terminal state reached
    ↓
Set WorkflowInstance status
    ↓
Set outcome
    ↓
Release all reservations
    ↓
Send final notification
```

## Known Limitations

1. **No Request Tracing**: No distributed tracing
2. **No Request Logging**: No detailed request logging
3. **No Performance Monitoring**: No request performance tracking
4. **No Error Tracking**: No centralized error tracking
5. **No Request Replay**: No request replay capability

## Future Enhancements

1. **Add Request Tracing**: Add OpenTelemetry for distributed tracing
2. **Add Request Logging**: Add detailed request logging
3. **Add Performance Monitoring**: Add APM monitoring
4. **Add Error Tracking**: Add Sentry or similar
5. **Add Request Replay**: Add request replay for debugging
6. **Add Request Metrics**: Add request metrics dashboard
7. **Add Request Profiling**: Add request profiling
8. **Add Request Validation**: Add stricter request validation
