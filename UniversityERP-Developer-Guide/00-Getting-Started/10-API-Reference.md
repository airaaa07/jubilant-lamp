# API Reference

## Overview

This document provides comprehensive API reference documentation for the University ERP system. It includes all available endpoints, request/response formats, authentication requirements, and usage examples.

## Base URL

**Development:**
```
http://localhost:3000/api
```

**Production:**
```
https://api.university.edu/api
```

## Authentication

### JWT Authentication

**Confirmed by Code**: The API uses JWT (JSON Web Token) for authentication.

**Authentication Flow:**

1. **Login to get access token:**
   ```bash
   POST /auth/login
   {
     "email": "admin@university.edu",
     "password": "admin123"
   }
   ```

2. **Response:**
   ```json
   {
     "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "user": {
       "id": "user-id",
       "email": "admin@university.edu",
       "name": "System Administrator",
       "role": "ADMIN"
     }
   }
   ```

3. **Use access token in subsequent requests:**
   ```bash
   GET /users/profile
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Token Refresh

**Refresh access token:**
```bash
POST /auth/refresh
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    // Response data
  },
  "message": "Success message"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": {
      // Additional error details
    }
  }
}
```

### Pagination Response

```json
{
  "success": true,
  "data": [
    // Array of items
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  }
}
```

## API Endpoints

### Authentication Endpoints

#### POST /auth/register

Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "role": "STUDENT"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "STUDENT",
    "createdAt": "2024-01-01T10:00:00.000Z"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email already exists"
  }
}
```

#### POST /auth/login

Login with email and password.

**Request Body:**
```json
{
  "email": "admin@university.edu",
  "password": "admin123"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user-id",
      "email": "admin@university.edu",
      "name": "System Administrator",
      "role": "ADMIN"
    }
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

#### POST /auth/logout

Logout current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### POST /auth/refresh

Refresh access token.

**Request Body:**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### User Endpoints

#### GET /users

Get all users (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `search` (optional): Search by name or email
- `role` (optional): Filter by role

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "user-1",
      "email": "user1@example.com",
      "name": "User 1",
      "role": "ADMIN",
      "isActive": true,
      "createdAt": "2024-01-01T10:00:00.000Z"
    },
    {
      "id": "user-2",
      "email": "user2@example.com",
      "name": "User 2",
      "role": "STAFF",
      "isActive": true,
      "createdAt": "2024-01-01T10:00:00.000Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 2,
    "totalPages": 1
  }
}
```

#### GET /users/:id

Get user by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "STUDENT",
    "isActive": true,
    "emailVerified": true,
    "createdAt": "2024-01-01T10:00:00.000Z",
    "updatedAt": "2024-01-01T10:00:00.000Z"
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found"
  }
}
```

#### POST /users

Create a new user (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "password123",
  "name": "New User",
  "role": "STAFF"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "new-user-id",
    "email": "newuser@example.com",
    "name": "New User",
    "role": "STAFF",
    "isActive": true,
    "createdAt": "2024-01-01T10:00:00.000Z"
  }
}
```

#### PUT /users/:id

Update user (requires ADMIN role or own user).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "updated@example.com"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "updated@example.com",
    "name": "Updated Name",
    "role": "STAFF",
    "isActive": true,
    "updatedAt": "2024-01-01T11:00:00.000Z"
  }
}
```

#### DELETE /users/:id

Delete user (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

### Student Endpoints

#### GET /students

Get all students.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `search` (optional): Search by name or roll number
- `batch` (optional): Filter by batch
- `course` (optional): Filter by course
- `section` (optional): Filter by section

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "student-1",
      "userId": "user-1",
      "rollNumber": "2024001",
      "batch": "2024",
      "course": "BTECH-CS",
      "section": "A",
      "semester": 1,
      "status": "ACTIVE",
      "user": {
        "id": "user-1",
        "email": "student1@example.com",
        "name": "Student 1"
      }
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### GET /students/:id

Get student by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "student-1",
    "userId": "user-1",
    "rollNumber": "2024001",
    "batch": "2024",
    "course": "BTECH-CS",
    "section": "A",
    "semester": 1,
    "status": "ACTIVE",
    "admissionDate": "2024-07-01",
    "user": {
      "id": "user-1",
      "email": "student1@example.com",
      "name": "Student 1"
    }
  }
}
```

#### POST /students

Create a new student (requires ADMIN or STAFF role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "userId": "user-id",
  "rollNumber": "2024001",
  "batch": "2024",
  "course": "BTECH-CS",
  "section": "A",
  "semester": 1,
  "admissionDate": "2024-07-01"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "student-1",
    "userId": "user-id",
    "rollNumber": "2024001",
    "batch": "2024",
    "course": "BTECH-CS",
    "section": "A",
    "semester": 1,
    "status": "ACTIVE",
    "admissionDate": "2024-07-01"
  }
}
```

#### PUT /students/:id

Update student (requires ADMIN or STAFF role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "section": "B",
  "semester": 2
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "student-1",
    "userId": "user-id",
    "rollNumber": "2024001",
    "batch": "2024",
    "course": "BTECH-CS",
    "section": "B",
    "semester": 2,
    "status": "ACTIVE",
    "updatedAt": "2024-01-01T11:00:00.000Z"
  }
}
```

### Course Endpoints

#### GET /courses

Get all courses.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `department` (optional): Filter by department

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "course-1",
      "code": "BTECH-CS",
      "name": "Bachelor of Technology in Computer Science",
      "department": "Computer Science",
      "duration": 4,
      "credits": 160,
      "isActive": true
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### GET /courses/:id

Get course by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "course-1",
    "code": "BTECH-CS",
    "name": "Bachelor of Technology in Computer Science",
    "department": "Computer Science",
    "duration": 4,
    "credits": 160,
    "isActive": true,
    "subjects": [
      {
        "id": "subject-1",
        "code": "CS101",
        "name": "Introduction to Programming",
        "credits": 4,
        "semester": 1
      }
    ]
  }
}
```

#### POST /courses

Create a new course (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "code": "BTECH-CS",
  "name": "Bachelor of Technology in Computer Science",
  "department": "Computer Science",
  "duration": 4,
  "credits": 160
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "course-1",
    "code": "BTECH-CS",
    "name": "Bachelor of Technology in Computer Science",
    "department": "Computer Science",
    "duration": 4,
    "credits": 160,
    "isActive": true
  }
}
```

### Attendance Endpoints

#### GET /attendance

Get attendance records.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `studentId` (optional): Filter by student
- `subjectId` (optional): Filter by subject
- `date` (optional): Filter by date
- `status` (optional): Filter by status (PRESENT, ABSENT, LATE)

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "attendance-1",
      "studentId": "student-1",
      "subjectId": "subject-1",
      "date": "2024-01-01",
      "status": "PRESENT",
      "markedBy": "staff-1",
      "markedAt": "2024-01-01T09:00:00.000Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### POST /attendance/mark

Mark attendance (requires STAFF role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "studentId": "student-1",
  "subjectId": "subject-1",
  "date": "2024-01-01",
  "status": "PRESENT"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "attendance-1",
    "studentId": "student-1",
    "subjectId": "subject-1",
    "date": "2024-01-01",
    "status": "PRESENT",
    "markedBy": "staff-1",
    "markedAt": "2024-01-01T09:00:00.000Z"
  }
}
```

#### GET /attendance/report/:studentId

Get attendance report for a student.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "studentId": "student-1",
    "totalClasses": 100,
    "present": 85,
    "absent": 15,
    "percentage": 85,
    "subjectWise": [
      {
        "subjectId": "subject-1",
        "subjectName": "Introduction to Programming",
        "total": 20,
        "present": 18,
        "absent": 2,
        "percentage": 90
      }
    ]
  }
}
```

### Exam Endpoints

#### GET /exams

Get all exams.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `course` (optional): Filter by course
- `semester` (optional): Filter by semester
- `status` (optional): Filter by status

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "exam-1",
      "name": "Mid Semester Exam",
      "course": "BTECH-CS",
      "semester": 1,
      "startDate": "2024-02-01",
      "endDate": "2024-02-15",
      "status": "SCHEDULED"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### GET /exams/:id

Get exam by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "exam-1",
    "name": "Mid Semester Exam",
    "course": "BTECH-CS",
    "semester": 1,
    "startDate": "2024-02-01",
    "endDate": "2024-02-15",
    "status": "SCHEDULED",
    "subjects": [
      {
        "subjectId": "subject-1",
        "subjectName": "Introduction to Programming",
        "date": "2024-02-01",
        "time": "09:00",
        "duration": 3
      }
    ]
  }
}
```

#### POST /exams

Create a new exam (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Mid Semester Exam",
  "course": "BTECH-CS",
  "semester": 1,
  "startDate": "2024-02-01",
  "endDate": "2024-02-15"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "exam-1",
    "name": "Mid Semester Exam",
    "course": "BTECH-CS",
    "semester": 1,
    "startDate": "2024-02-01",
    "endDate": "2024-02-15",
    "status": "SCHEDULED"
  }
}
```

#### POST /exams/:id/results

Publish exam results (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "results": [
    {
      "studentId": "student-1",
      "subjectId": "subject-1",
      "marks": 85,
      "grade": "A"
    }
  ]
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Results published successfully"
}
```

### Fee Endpoints

#### GET /fees

Get fee records.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `studentId` (optional): Filter by student
- `status` (optional): Filter by status (PENDING, PAID, OVERDUE)

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "fee-1",
      "studentId": "student-1",
      "type": "TUITION",
      "amount": 50000,
      "dueDate": "2024-01-31",
      "status": "PENDING",
      "paidAmount": 0
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### POST /fees/pay

Pay fee (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "feeId": "fee-1",
  "amount": 50000,
  "paymentMethod": "ONLINE",
  "transactionId": "TXN123456"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "payment-1",
    "feeId": "fee-1",
    "amount": 50000,
    "paymentMethod": "ONLINE",
    "transactionId": "TXN123456",
    "paidAt": "2024-01-15T10:00:00.000Z"
  }
}
```

### Library Endpoints

#### GET /library/books

Get all books.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `search` (optional): Search by title or author
- `category` (optional): Filter by category

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "book-1",
      "isbn": "978-3-16-148410-0",
      "title": "Introduction to Algorithms",
      "author": "Thomas H. Cormen",
      "category": "Computer Science",
      "availableCopies": 5,
      "totalCopies": 10
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### POST /library/issue

Issue a book (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "bookId": "book-1"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "issue-1",
    "bookId": "book-1",
    "userId": "user-1",
    "issueDate": "2024-01-01",
    "dueDate": "2024-01-15",
    "status": "ISSUED"
  }
}
```

#### POST /library/return

Return a book (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "issueId": "issue-1"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "issue-1",
    "returnDate": "2024-01-10",
    "status": "RETURNED",
    "fine": 0
  }
}
```

### Hostel Endpoints

#### GET /hostel/rooms

Get all hostel rooms.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)
- `hostel` (optional): Filter by hostel
- `availability` (optional): Filter by availability

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "room-1",
      "hostel": "Hostel A",
      "roomNumber": "101",
      "capacity": 3,
      "occupied": 2,
      "available": 1
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "totalPages": 1
  }
}
```

#### POST /hostel/allocate

Allocate room to student (requires ADMIN role).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "studentId": "student-1",
  "roomId": "room-1",
  "startDate": "2024-07-01"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "allocation-1",
    "studentId": "student-1",
    "roomId": "room-1",
    "startDate": "2024-07-01",
    "status": "ACTIVE"
  }
}
```

### Transport Endpoints

#### GET /transport/routes

Get all transport routes.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": "route-1",
      "name": "Route A",
      "stops": ["Stop 1", "Stop 2", "Stop 3"],
      "capacity": 50,
      "fare": 1000
    }
  ]
}
```

#### POST /transport/pass

Issue transport pass (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "routeId": "route-1",
  "duration": "SEMESTER"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "pass-1",
    "userId": "user-1",
    "routeId": "route-1",
    "duration": "SEMESTER",
    "validFrom": "2024-07-01",
    "validTo": "2024-12-31",
    "status": "ACTIVE"
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| VALIDATION_ERROR | Request validation failed |
| INVALID_CREDENTIALS | Invalid email or password |
| USER_NOT_FOUND | User not found |
| STUDENT_NOT_FOUND | Student not found |
| COURSE_NOT_FOUND | Course not found |
| ATTENDANCE_ALREADY_MARKED | Attendance already marked |
| EXAM_NOT_FOUND | Exam not found |
| FEE_NOT_FOUND | Fee not found |
| BOOK_NOT_AVAILABLE | Book not available |
| ROOM_NOT_AVAILABLE | Room not available |
| ROUTE_NOT_FOUND | Route not found |
| UNAUTHORIZED | Unauthorized access |
| FORBIDDEN | Access forbidden |
| INTERNAL_SERVER_ERROR | Internal server error |

## Rate Limiting

**Confirmed by Code**: The API implements rate limiting to prevent abuse.

**Rate Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

**Rate Limit Exceeded Response (429):**
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later."
  }
}
```

## WebSocket API

### Connection

**WebSocket URL:**
```
ws://localhost:3000
```

**Authentication:**
```javascript
const ws = new WebSocket('ws://localhost:3000?token=<access_token>');
```

### Events

#### Notification Event

**Server to Client:**
```json
{
  "type": "notification",
  "data": {
    "id": "notif-1",
    "title": "Attendance Marked",
    "message": "Your attendance has been marked for Introduction to Programming",
    "createdAt": "2024-01-01T10:00:00.000Z"
  }
}
```

#### Real-time Attendance Update

**Server to Client:**
```json
{
  "type": "attendance_update",
  "data": {
    "studentId": "student-1",
    "subjectId": "subject-1",
    "status": "PRESENT",
    "timestamp": "2024-01-01T09:00:00.000Z"
  }
}
```

## SDK Examples

### JavaScript/TypeScript

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login
const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password });
  localStorage.setItem('accessToken', response.data.data.accessToken);
  return response.data;
};

// Get students
const getStudents = async (page = 1, limit = 10) => {
  const response = await api.get('/students', { params: { page, limit } });
  return response.data;
};
```

### cURL

```bash
# Login
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@university.edu","password":"admin123"}'

# Get students
curl -X GET http://localhost:3000/api/students \
  -H "Authorization: Bearer <access_token>"

# Create student
curl -X POST http://localhost:3000/api/students \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"userId":"user-id","rollNumber":"2024001","batch":"2024","course":"BTECH-CS","section":"A","semester":1}'
```

## Additional Resources

- [Postman Collection](./postman-collection.json)
- [OpenAPI Specification](./openapi.yaml)
- [SDK Documentation](./sdk-documentation.md)
