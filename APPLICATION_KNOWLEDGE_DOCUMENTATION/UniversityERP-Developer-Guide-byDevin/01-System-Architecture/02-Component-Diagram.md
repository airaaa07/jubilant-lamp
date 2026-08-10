# Component Diagram

## Overview

This document provides detailed component diagrams for the University ERP system. It illustrates the relationships between components, their interactions, and data flows.

## System Components

### Backend Components

**Confirmed by Code**: The backend is organized into modular components.

**Component Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│                      Core API (NestJS)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Auth Module                            │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Auth Guard   │  │ JWT Strategy │  │ Local Strat  │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Auth Ctrl    │  │ Auth Service │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    User Module                            │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ User Ctrl    │  │ User Service │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ User Repo     │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Student Module                           │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Student Ctrl │  │ Student Svc  │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Student Repo  │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Course Module                           │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Course Ctrl  │  │ Course Svc   │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Course Repo   │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 Attendance Module                         │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Attendance   │  │ Attendance   │                       │  │
│  │  │ Ctrl         │  │ Service      │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Attendance   │                                           │  │
│  │  │ Repo         │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Exam Module                           │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Exam Ctrl    │  │ Exam Service │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Exam Repo     │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      Fee Module                            │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Fee Ctrl     │  │ Fee Service  │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Fee Repo      │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Library Module                          │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Library Ctrl │  │ Library Svc  │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Library Repo  │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Hostel Module                          │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Hostel Ctrl  │  │ Hostel Svc   │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Hostel Repo   │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Transport Module                         │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Transport    │  │ Transport    │                       │  │
│  │  │ Ctrl         │  │ Service      │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Transport    │                                           │  │
│  │  │ Repo         │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Workflow Module                          │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Workflow     │  │ Workflow     │                       │  │
│  │  │ Ctrl         │  │ Service      │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Workflow     │                                           │  │
│  │  │ Repo         │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Common Services                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Prisma Svc   │  │ Redis Svc    │  │ MinIO Svc    │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Cache Svc    │  │ Logger Svc   │  │ Queue Svc    │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Frontend Components

**Confirmed by Code**: The frontend is organized into component-based architecture.

**Component Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│                  Admin Portal (React)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    App Component                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Router       │  │ Auth Context │  │ Theme Ctx    │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Layout Components                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Header       │  │ Sidebar      │  │ Footer       │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐                                           │  │
│  │  │ Layout       │                                           │  │
│  │  └──────────────┘                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Common Components                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Button       │  │ Input        │  │ Modal        │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Table        │  │ Card         │  │ Badge        │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Avatar       │  │ Spinner      │  │ Alert        │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Page Components                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Login Page   │  │ Dashboard    │  │ Profile Page │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Students     │  │ Courses      │  │ Attendance   │    │  │
│  │  │ Page         │  │ Page         │  │ Page         │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Exams Page   │  │ Fees Page    │  │ Library Page │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐                       │  │
│  │  │ Hostel Page  │  │ Transport    │                       │  │
│  │  │              │  │ Page         │                       │  │
│  │  └──────────────┘  └──────────────┘                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Form Components                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Login Form   │  │ User Form    │  │ Student Form │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Course Form  │  │ Exam Form    │  │ Fee Form     │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Services                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ API Service  │  │ Auth Service │  │ User Service │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ Student Svc  │  │ Course Svc   │  │ Attendance   │    │  │
│  │  │              │  │              │  │ Svc          │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Hooks                                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ useAuth      │  │ useUsers     │  │ useStudents  │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │ useCourses   │  │ useAttendance│  │ useExams     │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interactions

### Auth Module Interactions

**Confirmed by Code**: Auth module interacts with multiple components.

**Interaction Diagram:**

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │
       │ POST /auth/login
       │ { email, password }
       ▼
┌──────────────┐
│ Auth Guard   │
└──────┬───────┘
       │
       │ Validates JWT
       ▼
┌──────────────┐
│ Auth Ctrl    │
└──────┬───────┘
       │
       │ validateLogin(dto)
       ▼
┌──────────────┐
│ Auth Service │
└──────┬───────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────────┐ ┌──────────────┐
│ User Repo    │ │ Cache Svc    │
└──────┬───────┘ └──────┬───────┘
       │               │
       │ findByEmail   │ get(email)
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│ PostgreSQL   │ │ Redis        │
└──────────────┘ └──────────────┘
       │               │
       │ User data     │ Cache miss
       │               │
       └───────┬───────┘
               │
               │ compare password
               │ generate tokens
               ▼
┌──────────────┐
│ Auth Service │
└──────┬───────┘
       │
       │ set(email, user, 3600)
       ▼
┌──────────────┐
│ Cache Svc    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Redis        │
└──────┬───────┘
       │
       │ { accessToken, refreshToken, user }
       ▼
┌──────────────┐
│   Client     │
└──────────────┘
```

### Student Module Interactions

**Confirmed by Code**: Student module interacts with course and user modules.

**Interaction Diagram:**

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │
       │ GET /students/:id
       ▼
┌──────────────┐
│ Auth Guard   │
└──────┬───────┘
       │
       │ Validates JWT
       ▼
┌──────────────┐
│ Student Ctrl │
└──────┬───────┘
       │
       │ findOne(id)
       ▼
┌──────────────┐
│ Student Svc  │
└──────┬───────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────────┐ ┌──────────────┐
│ Student Repo │ │ Cache Svc    │
└──────┬───────┘ └──────┬───────┘
       │               │
       │ findById     │ get(student:id)
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│ PostgreSQL   │ │ Redis        │
└──────┬───────┘ └──────┬───────┘
       │               │
       │ Student data  │ Cache miss
       │               │
       └───────┬───────┘
               │
               │ include: { user, enrollments }
               ├─────────────┐
               │             │
               ▼             ▼
        ┌──────────────┐ ┌──────────────┐
        │ User Repo    │ │ Course Repo  │
        └──────┬───────┘ └──────┬───────┘
               │               │
               │ findById     │ findMany
               ▼               ▼
        ┌──────────────┐ ┌──────────────┐
        │ PostgreSQL   │ │ PostgreSQL   │
        └──────────────┘ └──────────────┘
               │               │
               └───────┬───────┘
                       │
                       │ set(student:id, data, 3600)
                       ▼
                ┌──────────────┐
                │ Cache Svc    │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Redis        │
                └──────┬───────┘
                       │
                       │ Student with relations
                       ▼
                ┌──────────────┐
                │   Client     │
                └──────────────┘
```

## Data Flow Components

### Request Processing Flow

**Confirmed by Code**: Request processing follows a clear component flow.

**Flow Diagram:**

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │
       │ HTTP Request
       ▼
┌──────────────┐
│ API Gateway  │
└──────┬───────┘
       │
       │ Route request
       ▼
┌──────────────┐
│ Middleware   │
└──────┬───────┘
       │
       │ CORS, Logger, etc.
       ▼
┌──────────────┐
│ Auth Guard   │
└──────┬───────┘
       │
       │ Validate JWT
       ▼
┌──────────────┐
│ Roles Guard  │
└──────┬───────┘
       │
       │ Check permissions
       ▼
┌──────────────┐
│ Validation   │
│ Pipe         │
└──────┬───────┘
       │
       │ Validate DTO
       ▼
┌──────────────┐
│ Controller   │
└──────┬───────┘
       │
       │ Call service
       ▼
┌──────────────┐
│ Service      │
└──────┬───────┘
       │
       ├─────────────┐
       │             │
       ▼             ▼
┌──────────────┐ ┌──────────────┐
│ Cache Svc    │ │ Repository   │
└──────┬───────┘ └──────┬───────┘
       │               │
       │ Check cache   │ Query DB
       ▼               ▼
┌──────────────┐ ┌──────────────┐
│ Redis        │ │ PostgreSQL   │
└──────┬───────┘ └──────┬───────┘
       │               │
       └───────┬───────┘
               │
               │ Return data
               ▼
┌──────────────┐
│ Service      │
└──────┬───────┘
       │
       │ Set cache
       ▼
┌──────────────┐
│ Cache Svc    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Redis        │
└──────┬───────┘
       │
       │ Return to controller
       ▼
┌──────────────┐
│ Controller   │
└──────┬───────┘
       │
       │ Transform response
       ▼
┌──────────────┐
│ Response     │
└──────┬───────┘
       │
       │ HTTP Response
       ▼
┌──────────────┐
│   Client     │
└──────────────┘
```

### Background Job Processing

**Confirmed by Code**: Background jobs use queue-based processing.

**Flow Diagram:**

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │
       │ Request (e.g., send email)
       ▼
┌──────────────┐
│ Controller   │
└──────┬───────┘
       │
       │ Add job to queue
       ▼
┌──────────────┐
│ Queue Svc    │
└──────┬───────┘
       │
       │ add('email', data)
       ▼
┌──────────────┐
│ Bull Queue   │
└──────┬───────┘
       │
       │ Store in Redis
       ▼
┌──────────────┐
│ Redis        │
└──────┬───────┘
       │
       │ Job queued
       ▼
┌──────────────┐
│ Worker       │
└──────┬───────┘
       │
       │ Process job
       ▼
┌──────────────┐
│ Processor    │
└──────┬───────┘
       │
       │ Execute job logic
       ▼
┌──────────────┐
│ External Svc │
└──────┬───────┘
       │
       │ Send email
       ▼
┌──────────────┐
│ Email Svc    │
└──────┬───────┘
       │
       │ Email sent
       ▼
┌──────────────┐
│ Processor    │
└──────┬───────┘
       │
       │ Mark job complete
       ▼
┌──────────────┐
│ Bull Queue   │
└──────┬───────┘
       │
       │ Update job status
       ▼
┌──────────────┐
│ Redis        │
└──────────────┘
```

## Component Dependencies

### Backend Dependencies

**Confirmed by Code**: Backend modules have specific dependencies.

**Dependency Graph:**

```
app.module.ts
├── auth.module
│   ├── users.module
│   └── common.module
├── users.module
│   ├── common.module
│   └── prisma.module
├── students.module
│   ├── users.module
│   ├── courses.module
│   ├── common.module
│   └── prisma.module
├── courses.module
│   ├── common.module
│   └── prisma.module
├── attendance.module
│   ├── students.module
│   ├── courses.module
│   ├── common.module
│   └── prisma.module
├── exams.module
│   ├── students.module
│   ├── courses.module
│   ├── common.module
│   └── prisma.module
├── fees.module
│   ├── students.module
│   ├── common.module
│   └── prisma.module
├── library.module
│   ├── users.module
│   ├── common.module
│   └── prisma.module
├── hostel.module
│   ├── students.module
│   ├── common.module
│   └── prisma.module
├── transport.module
│   ├── students.module
│   ├── common.module
│   └── prisma.module
└── workflow.module
    ├── users.module
    ├── students.module
    ├── courses.module
    ├── attendance.module
    ├── exams.module
    ├── fees.module
    ├── common.module
    └── prisma.module
```

### Frontend Dependencies

**Confirmed by Code**: Frontend components have specific dependencies.

**Dependency Graph:**

```
App.tsx
├── Router
├── AuthContext
├── ThemeContext
└── Layout
    ├── Header
    ├── Sidebar
    └── Footer
├── Pages
    ├── LoginPage
    │   ├── LoginForm
    │   └── Common Components
    ├── DashboardPage
    │   ├── Common Components
    │   └── Charts
    ├── StudentsPage
    │   ├── StudentTable
    │   ├── StudentForm
    │   └── Common Components
    ├── CoursesPage
    │   ├── CourseTable
    │   ├── CourseForm
    │   └── Common Components
    ├── AttendancePage
    │   ├── AttendanceTable
    │   ├── AttendanceForm
    │   └── Common Components
    ├── ExamsPage
    │   ├── ExamTable
    │   ├── ExamForm
    │   └── Common Components
    ├── FeesPage
    │   ├── FeeTable
    │   ├── FeeForm
    │   └── Common Components
    ├── LibraryPage
    │   ├── BookTable
    │   ├── BookForm
    │   └── Common Components
    ├── HostelPage
    │   ├── RoomTable
    │   ├── RoomForm
    │   └── Common Components
    └── TransportPage
        ├── RouteTable
        ├── RouteForm
        └── Common Components
└── Services
    ├── API Service
    ├── Auth Service
    ├── User Service
    ├── Student Service
    ├── Course Service
    ├── Attendance Service
    ├── Exam Service
    ├── Fee Service
    ├── Library Service
    ├── Hostel Service
    └── Transport Service
```

## Component Communication

### Synchronous Communication

**Confirmed by Code**: Most communication is synchronous via HTTP.

**Communication Pattern:**
```
Client → HTTP Request → API → Service → Repository → Database
                                                    ↓
Client ← HTTP Response ← API ← Service ← Cache ← Redis
```

### Asynchronous Communication

**Confirmed by Code**: Some communication is asynchronous via queues.

**Communication Pattern:**
```
Client → HTTP Request → API → Queue → Worker → External Service
                                                    ↓
Client ← HTTP Response ← API ← Queue ← Worker ← Result
```

### Event-Driven Communication

**Confirmed by Code**: Events are used for decoupled communication.

**Communication Pattern:**
```
Service A → Emit Event → Event Bus → Service B → Handle Event
                                    ↓
                              Service C → Handle Event
```

## Component Scaling

### Horizontal Scaling

**Confirmed by Code**: Components can be scaled horizontally.

**Scaling Strategy:**
```
Load Balancer
    │
    ├─→ API Instance 1
    ├─→ API Instance 2
    ├─→ API Instance 3
    └─→ API Instance N
```

### Database Scaling

**Confirmed by Code**: Database can be scaled with read replicas.

**Scaling Strategy:**
```
Primary Database (Write)
    │
    ├─→ Replica 1 (Read)
    ├─→ Replica 2 (Read)
    └─→ Replica N (Read)
```

### Cache Scaling

**Confirmed by Code**: Redis can be scaled with clustering.

**Scaling Strategy:**
```
Redis Cluster
    │
    ├─→ Node 1
    ├─→ Node 2
    ├─→ Node 3
    └─→ Node N
```

## Next Steps

After understanding component diagrams:

1. **Read Module Documentation**: Understand specific modules
2. **Read API Documentation**: Understand API design
3. **Read Database Guide**: Understand data model
4. **Read Deployment Guide**: Understand deployment

## Additional Resources

- [NestJS Modules](https://docs.nestjs.com/modules)
- [React Components](https://react.dev/learn/thinking-in-react)
- [Component Diagrams](https://www.uml-diagrams.org/component-diagrams.html)
