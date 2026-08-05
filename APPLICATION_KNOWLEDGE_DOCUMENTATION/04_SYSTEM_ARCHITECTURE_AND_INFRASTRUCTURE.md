# System Architecture & Infrastructure Documentation

## Table of Contents
1. [Monorepo Architecture](#monorepo-architecture)
2. [Backend Microservices & Core API](#backend-microservices--core-api)
3. [Database & Persistence Layer](#database--persistence-layer)
4. [Caching & Background Processing](#caching--background-processing)
5. [Storage & External Integrations](#storage--external-integrations)
6. [Security & Protection Infrastructure](#security--protection-infrastructure)
7. [Audit & Maintenance System](#audit--maintenance-system)
8. [Scheduled Jobs & Cron Operations](#scheduled-jobs--cron-operations)
9. [Multi-Tenancy & Data Isolation](#multi-tenancy--data-isolation)

---

## Monorepo Architecture

UniversityERP is structured as an enterprise-grade monorepo managed via **Turborepo**. The codebase decouples backend services, frontend portals, and shared packages to support scalable development.

### Directory Structure Overview
```
UniversityERP/
├── apps/
│   ├── core-api/               # Main NestJS API Server (38 Modules)
│   ├── cbe-engine/             # Computer-Based Exam Engine (Scaffolding Stub)
│   ├── cert-generator/         # PDF & Certificate Generator (Scaffolding Stub)
│   └── notification-worker/    # Background Notification Processor (Scaffolding Stub)
├── web/
│   ├── admin-portal/           # Primary React 19 Frontend (Admin, Staff & Student UI)
│   └── student-portal/         # Dedicated Student Portal (Package Structure/Placeholder)
├── libs/                       # Shared internal libraries (reserved for shared utilities)
├── docs/                       # Architectural diagrams, SQL dumps, and API reports
├── APPLICATION_KNOWLEDGE_DOCUMENTATION/ # Full-stack single source of truth docs
├── docker-compose.yml          # Local infrastructure deployment
└── ecosystem.native.config.js  # PM2 process management for production
```

---

## Backend Microservices & Core API

### 1. Monolithic Core API (`apps/core-api`)
The core of UniversityERP is a high-performance **NestJS** application (`core-api`) running on Node.js with TypeScript. It centralizes authentication, domain logic, database operations, background scheduling, and API delivery.

- **Framework**: NestJS v10+ with Express adapter
- **Entrypoint**: `apps/core-api/src/main.ts`
- **Root Module**: `apps/core-api/src/app.module.ts`
- **Port**: Default `3000` (configurable via `PORT` environment variable)
- **API Prefix**: `/api/v1`
- **Swagger Documentation**: Accessible at `/api/docs` in non-production environments

### 2. Standalone Service Analysis & Implementation Reality
While the codebase contains separate subdirectories under `apps/` for dedicated microservices, a code-level audit reveals their current production deployment state:

| Service Name | Path | Declared Purpose | Actual Codebase Implementation State |
| :--- | :--- | :--- | :--- |
| **`core-api`** | `apps/core-api` | Main API & Domain Services | **Fully Implemented**. Serves all 38 business domains, handles database operations, authentication, background jobs, document generation, and exam logic. |
| **`cbe-engine`** | `apps/cbe-engine` | Online Exam & Proctoring Service | **Scaffolding Stub**. Contains basic NestJS boilerplate (`AppModule` importing `ConfigModule` only). All active CBE logic, proctoring endpoints, and question paper generation are executed directly inside `core-api` under `ExaminationModule`. |
| **`cert-generator`** | `apps/cert-generator` | PDF Certificate & Document Service | **Scaffolding Stub**. Basic NestJS bootstrap only. Active certificate and document rendering is handled inside `core-api` under `DocumentsModule` using Handlebars/PDFKit templates. |
| **`notification-worker`** | `apps/notification-worker` | Asynchronous Email/SMS Queue Processor | **Scaffolding Stub**. Basic NestJS bootstrap only. Active notification dispatching is handled within `core-api` under `NotificationsModule` with Redis/Bull queues. |

> [!NOTE]
> **Architectural Recommendation**: The project architecture is currently a **modular monolith** contained inside `core-api`. The separate `apps/` subdirectories represent an architectural strategy for future microservice extraction once traffic scale demands horizontal isolation.

---

## Database & Persistence Layer

### PostgreSQL + Prisma ORM
The application utilizes **PostgreSQL** as its primary relational database management system, accessed via **Prisma ORM**.

- **Prisma Schema Path**: `apps/core-api/prisma/schema.prisma`
- **Total Data Models**: 100+ entities spanning organizational, academic, financial, and operational domains.
- **Connection Management**: Managed via NestJS `DatabaseModule` (`PrismaService`).
- **Migrations**: Database state is versioned using Prisma Migrate.

```
┌─────────────────────────────────────────────────────────────┐
│                       PostgreSQL Database                   │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐  │
│  │ Organization &   │  │ Academic Rules & │  │ Financial │  │
│  │ Multi-Tenancy    │  │ Versioned Labels │  │ Ledger    │  │
│  └──────────────────┘  └──────────────────┘  └───────────┘  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐  │
│  │ Examinations &   │  │ Infrastructure & │  │ Workflow  │  │
│  │ AI Proctoring    │  │ Facilities       │  │ Engine    │  │
│  └──────────────────┘  └──────────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Caching & Background Processing

### 1. Redis Cache & Storage
**Redis** powers in-memory caching, session tracking, OTP rate limiting, and Bull queue backend operations.
- **Module**: `apps/core-api/src/infrastructure/redis/redis.module.ts`
- **Use Cases**:
  - Caching academic catalogs and stream label definitions
  - Holding temporary OTP tokens during registration (`MobileOtp`)
  - Distributed lock management during timetable generation and resource allocation

### 2. Bull Queue System
Background tasks requiring asynchronous processing are delegated to **Bull queues** backed by Redis.
- **Async Workflows**:
  - Batch Email & SMS notifications
  - PDF document compile and upload tasks
  - Large-scale timetable conflict solving calculations
  - Exam paper auto-grading and SGPA/CGPA result generation

---

## Storage & External Integrations

### 1. Object Storage (MinIO / S3 Compatible)
All physical files, student documents, photo uploads, generated certificates, and exam proctoring webcam snapshots are stored in object storage.
- **Module**: `apps/core-api/src/infrastructure/minio/minio.module.ts`
- **Provider**: MinIO (local Docker container) or AWS S3 in cloud deployments.
- **Buckets**:
  - `student-documents`: Passports, marksheets, certificates
  - `generated-docs`: Compiled PDFs, hall tickets, fee receipts
  - `proctoring-captures`: Webcam snapshots captured during CBE exams
  - `system-backups`: Encrypted PostgreSQL database backup archives

### 2. HashiCorp Vault / Secret Management
System configurations, payment gateway keys, and encryption secrets are resolved securely via Vault or `vault.env.json`.

### 3. Razorpay Payment Gateway Integration
- Integrates directly with `FeeModule` and `WorkflowModule`.
- Supports webhooks and synchronous payment verification callbacks.
- Triggers automatic ledger updates and receipt generation upon payment confirmation.

---

## Security & Protection Infrastructure

### 1. Multi-Layer Guard Pipeline
Every HTTP request to `core-api` passes through a strict order of NestJS guards configured in `app.module.ts`:

```
Incoming Request
      │
      ▼
┌──────────────────────────┐
│  ThrottlerGuard          │  (Rate limits request floods: 300/min default, 5/min on login)
└────────────┬─────────────┘
             │ Pass
             ▼
┌──────────────────────────┐
│  GlobalJwtAuthGuard      │  (Fail-Closed: Requires JWT unless decorated with @Public())
└────────────┬─────────────┘
             │ Pass
             ▼
┌──────────────────────────┐
│  MaintenanceGuard        │  (Blocks non-SuperAdmins during database backup/restore)
└────────────┬─────────────┘
             │ Pass
             ▼
┌──────────────────────────┐
│  RolesGuard / Scoping    │  (Verifies application role and institute/dept boundaries)
└────────────┬─────────────┘
             │ Pass
             ▼
      Route Handler
```

### 2. Password & Auth Security Policies
- **Bcrypt Hashing**: Password hashes are generated with high salt rounds.
- **JWT Tokens**: Short-lived access tokens paired with secure refresh tokens.
- **Account Lockout Policy**: Tracks consecutive failed login attempts; locks account temporarily upon threshold breach.
- **Password History**: Prevents users from reusing their last $N$ passwords during reset or initial setup.

---

## Audit & Maintenance System

### 1. Database Level Audit Logging
Audit logging is enforced automatically at the data persistence layer using custom **Prisma Middleware** in `PrismaService`.
- **Interactions Monitored**: `create`, `update`, `delete`, `upsert`, `updateMany`, `deleteMany`.
- **Field-Level Diffing**: Compares entity state before and after modification and records exact JSON field changes.
- **Persistence**: Writes directly to `audit_logs` table with `userId`, `action`, `entityName`, `entityId`, `oldValues`, `newValues`, `ipAddress`, and `timestamp`.

### 2. Maintenance Gate (`MaintenanceGuard`)
During critical system maintenance or automated database backups:
- Admins can set `MAINTENANCE_MODE=true` or initiate a backup restore.
- `MaintenanceGuard` intercepts non-system requests and returns **HTTP 503 Service Unavailable** with a custom user message.
- SuperAdmin accounts and health check endpoints (`/api/v1/health`) bypass maintenance locks.

---

## Scheduled Jobs & Cron Operations

UniversityERP runs automated background tasks using NestJS `@Cron` schedulers.

| Schedule | Component / Service | Task Name | Description |
| :--- | :--- | :--- | :--- |
| **`0 0 * * *`** (Daily Midnight) | `LibraryService` | `cleanupExpiredReservations` | Releases held library books that were not picked up within the reservation window; updates status to `EXPIRED`. |
| **`0 0 * * *`** (Daily Midnight) | `NoticeBoardService` | `checkExpiredNotices` | Scans published notices, marks expired notices inactive, and sends notifications to authors. |
| **`0 0 * * *`** (Daily Midnight) | `WorkflowSchedulerService` | `expirePaymentDemands` | Expires unpaid workflow payment demands, cancels associated pending workflow instances, and releases resource holds. |
| **`0 2 * * *`** (Daily 2:00 AM) | `RecurringBillingService` | `processDailyBilling` | Scans all active student enrollments, checks per-term fee rules, and auto-generates `FeeDemand` records for upcoming terms. |
| **Custom / Configurable** | `BackupService` | `runAutomatedBackup` | Executes PostgreSQL `pg_dump`, compresses the output, uploads to MinIO `system-backups`, and verifies archive integrity. |
| **On Demand** | `ExamSchedulerService` | `generateExamSchedule` | Executes constraint-solving algorithm to auto-schedule exam dates, rooms, and invigilator duties. |
| **On Demand** | `TimetableService` | `generateTimetable` | Runs timetabling algorithm to assign staff, courses, and classrooms without resource conflicts. |

---

## Multi-Tenancy & Data Isolation

UniversityERP implements a multi-tenant hierarchy designed for educational groups managing multiple colleges or institutes:

```
                      University (Top Level Entity)
                     /             |             \
         Institute 1          Institute 2          Institute 3
        (Engineering)           (Medical)           (Management)
         /         \            /       \           /         \
    Dept 1        Dept 2     Dept 1    Dept 2    Dept 1      Dept 2
   (CS/IT)        (Mech)    (Anatomy) (Pharma)   (Finance)   (Marketing)
```

### Data Isolation Rules
1. **University Level**: Cross-institute policies, master academic catalog, global fee heads, global roles, and system configuration.
2. **Institute Level**: Each record in `Institute` contains a unique `schemaName` and `headUserId`. Core tables enforce `instituteId` foreign keys.
3. **Department Level**: Program offerings, section allocations, and staff-subject assignments are scoped to specific `departmentId` references.
4. **User Level**: Scoping guards inspect `user.universityId`, `user.instituteId`, and `user.departmentId` on every API request to enforce boundary isolation.
