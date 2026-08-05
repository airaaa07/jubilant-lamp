# UniversityERP - Application Overview

## What is UniversityERP?

UniversityERP is a comprehensive enterprise resource planning system designed for universities and educational institutions. It manages the complete academic and administrative lifecycle of students, staff, and institutional operations.

## System Purpose

This application serves as a centralized platform for:
- **Academic Management**: Programs, courses, batches, sections, and academic planning
- **Student Lifecycle**: From registration and admission to graduation and alumni status
- **Examination System**: Traditional exams and Computer-Based Examinations (CBE) with AI proctoring
- **Fee Management**: Complex fee structures, payments, scholarships, and refunds
- **Infrastructure**: Hostel, transport, library, and resource management
- **Human Resources**: Staff management, leave systems, and attendance
- **Workflow Automation**: Generic approval workflows for various processes
- **Communication**: Notifications, notice boards, and counselling systems

## Architecture Overview

### Technology Stack

**Backend (NestJS):**
- Framework: NestJS with TypeScript
- Database: PostgreSQL with Prisma ORM
- Authentication: JWT with refresh tokens
- File Storage: MinIO/S3 compatible
- Cache: Redis
- Payment: Razorpay integration
- Background Jobs: Bull queues with Redis

**Frontend (React):**
- Framework: React 19 with TypeScript
- Build Tool: Vite
- UI: Tailwind CSS with Headless UI
- State Management: TanStack Query
- Routing: React Router v7
- Rich Text: Tiptap editor
- Charts: Recharts

**Additional Services:**
- **Notification Worker**: Dedicated service for email/SMS notifications
- **CBE Engine**: Computer-Based Examination engine
- **Certificate Generator**: Document generation service

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Multi-Tenant Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  University (Top Level)                                       │
│    ├── Institute 1 (College/School)                          │
│    │    ├── Department 1                                     │
│    │    │    ├── Programme A → Batch → Section → Students   │
│    │    │    └── Programme B → Batch → Section → Students   │
│    │    └── Department 2                                     │
│    ├── Institute 2                                           │
│    └── Institute 3                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Application Structure

**Backend Services:**
- `core-api`: Main NestJS API server (35 modules)
- `notification-worker`: Background notification processing
- `cbe-engine`: Computer-Based Examination engine
- `cert-generator`: Document and certificate generation

**Frontend Applications:**
- `admin-portal`: Main administrative interface for all users
- `student-portal`: Dedicated student interface (planned)

## Key Business Domains

### 1. Academic Management
- University and institute hierarchy
- Program catalog and course offerings
- Batch and section management
- Stream labels with versioned academic rules
- Subject pools and elective management
- Term-based academic structure

### 2. Student Lifecycle
- Registration with OTP verification
- Admission workflows and merit lists
- Student onboarding and profile management
- Subject enrollment and elections
- Attendance tracking
- Examination and results
- Document generation
- Alumni management

### 3. Examination System
- Question bank management
- Exam paper creation
- Computer-Based Examinations (CBE)
- AI proctoring with webcam monitoring
- Question challenge system
- Result processing and grading
- SGPA/CGPA calculation

### 4. Fee Management
- Fee structures and heads
- Recurring billing (daily at 2 AM)
- Payment processing (Razorpay)
- Scholarships and concessions
- Government reimbursements
- Deposit refunds
- Receipt generation

### 5. Infrastructure
- **Hostel**: Room allocation, mess fees, security deposits
- **Transport**: Route planning, vehicle management, passes
- **Library**: Book catalog, circulation, reservations, fines
- **Resources**: Generic resource booking (classrooms, labs, auditoriums)

### 6. Human Resources
- Staff management and profiles
- Leave application and approval
- Leave balance tracking
- Staff-subject assignments
- Attendance tracking

### 7. Workflow Engine
- Generic approval workflows
- Visual workflow designer
- Multi-step approvals
- Conditional routing
- Payment gate integration
- Resource reservation holds

### 8. Communication
- In-app notifications
- Email notifications
- SMS notifications
- Notice board with expiry
- Login banners
- Social media monitoring

## User Types and Roles

### Application Roles (System Access)
- **SuperAdmin**: Full system access, university-level configuration
- **UnivAdmin**: University-level administration
- **InstAdmin**: Institute-level administration
- **Student**: Self-service access to academic data
- **Applicant**: Public registration and application access
- **Alumni**: Graduate access to services

### Staff Roles (Functional Roles)
**University-Level:**
- General Staff, Lecturer, Professor, Dean/HOD
- Finance Head, Accounts Officer, Section Officer
- Registrar, Dy Registrar, Controller of Examinations
- Pro President, President, Chairperson

**Institute-Level:**
- General Staff, Non Teaching Staff, Lecturer, Professor
- TeachingFaculty, Accountant, AdminStaff
- HOD, Director/Principal, Librarian

## Key Features

### Multi-Tenancy
- Support for multiple universities
- Each university can have multiple institutes
- Shared infrastructure with data isolation

### Versioned Academic Rules
- StreamLabel and SubjectLabel are immutable snapshots
- Students governed by rules active at enrollment
- Supports rule changes without affecting ongoing batches

### Workflow-Driven Approvals
- Generic workflow engine for all approval processes
- Visual workflow designer
- Conditional routing based on data
- Payment gate integration
- Resource reservation with saga pattern

### Computer-Based Examinations
- Proctored online exams
- Webcam and microphone monitoring
- Device fingerprinting
- Tab switch detection
- Real-time invigilator intervention
- Question challenge system

### Automated Scheduling
- Timetable auto-scheduler
- Resource conflict detection
- Staff load balancing
- Elective pooling support
- Clubbing support (lecture/tutorial)

### Comprehensive Fee Management
- Complex fee structures
- Recurring billing automation
- Scholarship and concession support
- Government reimbursement tracking
- Deposit refund workflows

### Robust Security
- JWT-based authentication
- Password policy enforcement
- Account lockout protection
- Comprehensive audit logging
- Multi-role assignment with scoping

## Integration Points

### External Integrations
- **Razorpay**: Payment gateway
- **Email Service**: SMTP configuration
- **SMS Gateway**: SMS notifications
- **MinIO/S3**: Object storage
- **Vault**: Secure secret storage

### Internal Integrations
- Document generation (PDF certificates)
- Analytics dashboards
- Parent portal access
- Directory services
- Social media monitoring

## Scheduled Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| Database Backup | Per-university (nightly/hourly/custom) | Backup to MinIO with verification |
| Library Reservation Cleanup | Daily midnight | Release expired book reservations |
| Notice Expiry Check | Daily midnight | Notify authors of expired notices |
| Workflow Payment Expiry | Daily midnight | Expire payment windows, release reservations |
| Recurring Billing | Daily 2 AM | Generate per-term fee demands |
| Exam Scheduling | On-demand | Generate exam schedules and invigilation assignments |
| Timetable Auto-Scheduler | On-demand | Generate institute timetables |

## Data Models Summary

The system has 100+ database models organized into:
- Organizational structure (4 models)
- User & authentication (7 models)
- Academic program structure (12 models)
- Student management (8 models)
- Staff management (5 models)
- Term & subject management (4 models)
- Results & assessment (6 models)
- Examination system (11 models)
- Fee & payment (9 models)
- Hostel management (7 models)
- Transport management (4 models)
- Library management (5 models)
- Timetable & scheduling (4 models)
- Institute resources (3 models)
- Leave management (3 models)
- Document management (3 models)
- Workflow engine (7 models)
- Forms & submissions (2 models)
- Notifications (4 models)
- Counselling (4 models)
- Configuration (8 models)
- Refund management (2 models)

## Access and Navigation

The admin portal provides 40+ pages organized into:
- Authentication & User Management
- Academic Management
- Examinations
- Student Services
- Workflow & Automation
- Infrastructure & Resources
- Analytics & Reporting
- Settings & Configuration

Navigation is role-based with module access control configurable per role.

## Development and Deployment

- **Monorepo Structure**: Turborepo for workspace management
- **Containerization**: Docker support with docker-compose
- **Database Migrations**: Prisma migrate with seed scripts
- **API Documentation**: Swagger/OpenAPI (non-production)
- **Build System**: Turbo for optimized builds
- **Code Quality**: ESLint, TypeScript strict mode

## Default Credentials

After fresh installation:
- **University**: SlashCurate University (slashcurate.edu)
- **SuperAdmin Email**: erpsupport@slashcurate.com
- **Default Password**: Admin@1234 (must change on first login)

## Documentation Structure

This single source of truth knowledge repository is organized into 8 core documents plus a master navigation hub:
- [`README.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/README.md) - Master Navigation & Repository Map
- [`00_APPLICATION_OVERVIEW.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/00_APPLICATION_OVERVIEW.md) - High-Level Product Purpose, Architecture & Key Business Domains
- [`01_BUSINESS_PROCESSES.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/01_BUSINESS_PROCESSES.md) - Step-by-Step Real-World End-to-End Processes (12 Major Workflows)
- [`02_USER_JOURNEYS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/02_USER_JOURNEYS.md) - Day-in-the-Life & Screen-by-Screen User Experiences (12 User Roles)
- [`03_DATA_FLOW_AND_LIFECYCLE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/03_DATA_FLOW_AND_LIFECYCLE.md) - Complete End-to-End Data Lifecycles & State Transformations
- [`04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md) - Technical Infrastructure, Guards, Crons & Microservices
- [`05_MODULE_BY_MODULE_DIRECTORY.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/05_MODULE_BY_MODULE_DIRECTORY.md) - Detailed Breakdown for all 38 NestJS Modules in Core API
- [`06_API_AND_DATABASE_REFERENCE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/06_API_AND_DATABASE_REFERENCE.md) - 100+ Database Tables, Schema Models, Enums & REST API Rules
- [`07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md) - Transparent Audit of Incomplete Flows, Stubs & System Limitations

---

**Document Version**: 1.4.0  
**Last Updated**: 2026-08-05  
**Application Version**: 1.4.0
