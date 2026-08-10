# API Reference

## Purpose

This document provides a comprehensive reference for the University ERP API. It details the API structure, authentication, endpoints, request/response formats, and error handling.

## Why This Document Exists

**Confirmed by Code**: The University ERP has a RESTful API with many endpoints. Understanding the API reference is critical for:
- Integrating with the API
- Building frontend applications
- Testing the API
- Debugging API issues
- Documenting API contracts

Without understanding the API reference, developers may struggle to use the API correctly.

## Where This Is Used

- **Frontend Development**: Building React components
- **Integration**: Integrating with external systems
- **Testing**: Writing API tests
- **Debugging**: Debugging API issues
- **Documentation**: API documentation

## Dependencies

### API Dependencies

**Confirmed by Code**: The API depends on:

- **NestJS**: Backend framework
- **JWT**: Authentication
- **Zod**: Validation
- **Prisma**: Database access
- **Guards**: Authorization
- **Pipes**: Validation

## Internal Architecture

### API Architecture

**Confirmed by Code**: The API follows RESTful principles.

```
┌─────────────────────────────────────────────────────────┐
│                  API Architecture                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Controllers   │  │  Services       │  │  Repositories   │
│  (HTTP Layer)  │  │ (Business Logic)│  │  (Data Access)  │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Guards       │  │  Pipes          │  │  Interceptors   │
│  (Authz)      │  │  (Validation)   │  │  (Transform)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### API Structure

**Confirmed by Code**: The API is organized by modules.

**Base URL**: `http://localhost:3000/api`

**Module Structure**:
```
/api
├── /auth                    # Authentication
├── /master-data             # Master data
│   ├── /universities
│   ├── /institutes
│   └── /departments
├── /admissions              # Admissions
├── /academic                # Academic
├── /attendance              # Attendance
├── /examination             # Examination
├── /fee                     # Fee
├── /timetable               # Timetable
├── /library                 # Library
├── /hostel                  # Hostel
├── /transport               # Transport
├── /hr                      # Human Resources
├── /documents               # Documents
├── /workflow                # Workflow
├── /notifications           # Notifications
├── /notice-board            # Notice Board
├── /banners                 # Banners
├── /users                   # Users
├── /settings                # Settings
├── /forms                   # Forms
├── /analytics               # Analytics
├── /audit                   # Audit
└── /counselling             # Counselling
```

## Code Walkthrough

### Authentication API

**Confirmed by Code**: Authentication endpoints in AuthController.

**Endpoints**:

#### POST /auth/login

**Purpose**: Authenticate user and receive tokens.

**Request**:
```json
{
  "email": "admin@university.edu",
  "password": "password"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc...",
    "user": {
      "id": "user-id",
      "email": "admin@university.edu",
      "role": "SUPERADMIN",
      "universityId": "uni-1",
      "instituteId": "inst-1"
    }
  }
}
```

**Rate Limit**: 5 requests per minute

#### POST /auth/register

**Purpose**: Register a new user.

**Request**:
```json
{
  "email": "student@university.edu",
  "password": "password123",
  "role": "STUDENT",
  "universityId": "uni-1",
  "instituteId": "inst-1"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "student@university.edu",
    "role": "STUDENT"
  }
}
```

#### POST /auth/refresh

**Purpose**: Refresh access token.

**Request**:
```json
{
  "refreshToken": "eyJhbGc..."
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc..."
  }
}
```

#### POST /auth/logout

**Purpose**: Logout user and invalidate tokens.

**Request**:
```json
{
  "refreshToken": "eyJhbGc..."
}
```

**Response**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Master Data API

**Confirmed by Code**: Master data endpoints in master-data controllers.

#### GET /master-data/universities

**Purpose**: Get all universities.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "uni-1",
      "name": "University A",
      "shortName": "UA",
      "domain": "university-a.edu",
      "logoUrl": "https://...",
      "config": {},
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "total": 1,
    "page": 1,
    "limit": 10
  }
}
```

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `search`: Search term

#### GET /master-data/universities/:id

**Purpose**: Get university by ID.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uni-1",
    "name": "University A",
    "shortName": "UA",
    "domain": "university-a.edu",
    "logoUrl": "https://...",
    "config": {},
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

#### POST /master-data/universities

**Purpose**: Create a new university.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request**:
```json
{
  "name": "University B",
  "shortName": "UB",
  "domain": "university-b.edu"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uni-2",
    "name": "University B",
    "shortName": "UB",
    "domain": "university-b.edu",
    "config": {},
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

**Scope**: `university`

#### PATCH /master-data/universities/:id

**Purpose**: Update university.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request**:
```json
{
  "name": "University B Updated"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "uni-2",
    "name": "University B Updated",
    "shortName": "UB",
    "domain": "university-b.edu",
    "config": {},
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T01:00:00Z"
  }
}
```

**Scope**: `university`

#### DELETE /master-data/universities/:id

**Purpose**: Delete university.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "success": true,
  "message": "University deleted successfully"
}
```

**Scope**: `university`

## Database Interactions

### API Database Operations

**Confirmed by Code**: API operations go through Prisma.

**Pattern**:
```typescript
// Controller
@Get()
async findAll(@Query() query: QueryDto) {
  return this.service.findAll(query);
}

// Service
async findAll(query: QueryDto) {
  return this.prisma.university.findMany({
    skip: (query.page - 1) * query.limit,
    take: query.limit,
    where: query.search ? {
      name: { contains: query.search, mode: 'insensitive' }
    } : undefined,
  });
}
```

## Redis Interactions

### API Caching

**Confirmed by Code**: API responses are cached.

**Pattern**:
```typescript
async findAll(query: QueryDto) {
  const cacheKey = `universities:${JSON.stringify(query)}`;
  const cached = await this.redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const universities = await this.prisma.university.findMany();
  await this.redis.setex(cacheKey, 300, JSON.stringify(universities));
  
  return universities;
}
```

## Queue Interactions

### API Background Jobs

**Confirmed by Code**: API can trigger background jobs.

**Pattern**:
```typescript
async sendNotification(dto: NotificationDto) {
  await this.notificationQueue.add('email', dto);
  return { success: true, message: 'Notification queued' };
}
```

## Worker Interactions

### API Worker Integration

**Confirmed by Code**: Workers process API-triggered jobs.

**Pattern**:
```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { to, subject, body } = job.data;
    await this.mailService.sendEmail({ to, subject, body });
  }
}
```

## Business Rules

### API Rules

**Confirmed by Code**: API follows these rules:

1. **RESTful**: Follow RESTful conventions
2. **JSON**: Use JSON for request/response
3. **Authentication**: All endpoints require authentication (except public)
4. **Authorization**: Scope-based access control
5. **Validation**: All inputs validated
6. **Pagination**: List endpoints support pagination
7. **Filtering**: List endpoints support filtering
8. **Sorting**: List endpoints support sorting

### Response Format

**Confirmed by Code**: Standard response format.

**Success Response**:
```json
{
  "success": true,
  "data": { ... },
  "meta": { ... }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": { ... }
  }
}
```

## Security

### API Security

**Confirmed by Code**: API security measures:

1. **JWT Authentication**: All endpoints require JWT token
2. **HTTPS**: Use HTTPS in production
3. **Rate Limiting**: Rate limiting on sensitive endpoints
4. **Input Validation**: All inputs validated
5. **Output Sanitization**: All outputs sanitized
6. **CORS**: CORS configured for allowed origins

## Performance Considerations

### API Performance

**Confirmed by Code**: Performance optimizations:

1. **Caching**: Frequently accessed data cached
2. **Pagination**: Large datasets paginated
3. **Select Fields**: Select only needed fields
4. **Connection Pooling**: Database connections pooled
5. **Compression**: Response compression enabled

## Common Mistakes

### Mistake 1: Not Including Authorization Header

**Symptom**: 401 Unauthorized error

**Cause**: Not including Authorization header

**Fix**:
```javascript
// Wrong
axios.get('/api/universities');

// Correct
axios.get('/api/universities', {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

### Mistake 2: Not Handling Pagination

**Symptom**: Missing data in list endpoints

**Cause**: Not handling pagination

** FIX**:
```javascript
// Wrong
const universities = await axios.get('/api/universities');

// Correct
const universities = await axios.get('/api/universities', {
  params: { page: 1, limit: 10 },
});
```

### Mistake 3: Not Validating Input

**Symptom**: 400 Bad Request error

**Cause**: Invalid input data

**Fix**:
```javascript
// Wrong
axios.post('/api/universities', { name: 123 });

// Correct
axios.post('/api/universities', { name: 'University Name' });
```

## Debugging Guide

### API Debugging

**Issue**: API request failing

**Investigation**:
1. Check request headers
2. Check request body
3. Check authentication token
4. Check response status
5. Check response body
6. Check API logs

**Tools**:
- Postman
- curl
- Browser DevTools
- API logs

## Future Enhancements

### GraphQL API

**Status**: Not implemented

**Proposal**: Add GraphQL API:
- Flexible queries
- Reduced over-fetching
- Better for frontend
- Schema-first approach

### API Versioning

**Status**: Not implemented

**Proposal**: Add API versioning:
- `/api/v1/`
- `/api/v2/`
- Backward compatibility
- Deprecation strategy

## Production Considerations

### API Production

**Production API**:
- Use HTTPS
- Enable rate limiting
- Enable CORS for allowed origins
- Enable compression
- Enable caching
- Monitor API performance
- Monitor error rates

### API Documentation

**Production Documentation**:
- Swagger/OpenAPI
- Interactive API explorer
- Code examples
- Error codes reference

## Example Requests

### Complete API Request Example

**Request**: Create a new university

```bash
curl -X POST http://localhost:3000/api/master-data/universities \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "University C",
    "shortName": "UC",
    "domain": "university-c.edu"
  }'
```

## Example Responses

### Error Response Example

**Response**: Validation error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

## Sequence Diagrams

### API Request Flow

```
Client → API Request
            ↓
        JWT Guard
            ↓
        Scope Guard
            ↓
        Validation Pipe
            ↓
        Controller
            ↓
        Service
            ↓
        Prisma
            ↓
        Database
            ↓
        Response
```

## Architecture Diagrams

### API Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ React App    │  │ Mobile App   │  │ 3rd Party    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  API Gateway                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Nginx        │  │ Load Balancer │  │ Rate Limiter  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  API Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Controllers  │  │ Guards        │  │ Pipes         │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is authentication handled in the API?

**Answer**: Authentication via JWT:
- Client sends credentials to /auth/login
- Server validates credentials
- Server returns access token and refresh token
- Client includes access token in Authorization header
- Server validates token on each request
- Client uses refresh token to get new access token

### Q2: How is authorization handled in the API?

**Answer**: Authorization via role-based and scope-based access:
- Users have roles (SUPERADMIN, ADMIN, STAFF, STUDENT)
- Users have scopes for module access
- Guards enforce access control
- Scope decorator on controller methods
- SUPERADMIN has access to all scopes

### Q3: How is pagination implemented in the API?

**Answer**: Pagination via query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- Response includes `meta` with pagination info
- Response includes `total` count

## Exercises

### Exercise 1: Call API Endpoint

**Task**: Call an API endpoint.

**Steps**:
1. Get access token
2. Call API endpoint with token
3. Handle response
4. Handle errors

**Verification**:
- API call successful
- Response parsed
- Errors handled

### Exercise 2: Create API Client

**Task**: Create an API client library.

**Steps**:
1. Create axios instance
2. Add interceptor for token
3. Add interceptor for errors
4. Create methods for endpoints
5. Test client

**Verification**:
- Client created
- Token handling works
- Error handling works
- Methods work correctly

## Real Production Scenarios

### Scenario 1: API Rate Limiting

**Situation**: API rate limiting triggered

**Response**:
1. Check rate limit headers
2. Implement exponential backoff
3. Cache responses
4. Optimize API calls

### Scenario 2: API Version Deprecation

**Situation**: API version deprecated

**Response**:
1. Check deprecation headers
2. Update to new version
3. Test new version
4. Update documentation

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [11-Monitoring-and-Logging](./11-Monitoring-and-Logging.md)

**Related Documentation**:
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [07-Authorization](../07-Authorization/README.md) - Authorization details
