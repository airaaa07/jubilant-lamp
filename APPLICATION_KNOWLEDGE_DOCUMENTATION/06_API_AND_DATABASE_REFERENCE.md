# API and Database Reference

## Table of Contents
1. [Database Schema Overview](#database-schema-overview)
2. [Domain Model Clusters](#domain-model-clusters)
3. [Core Enums Reference](#core-enums-reference)
4. [API Architecture & Conventions](#api-architecture--conventions)
5. [Authentication & Request Context](#authentication--request-context)
6. [Standardized Response & Error Contracts](#standardized-response--error-contracts)

---

## Database Schema Overview

The database is built on **PostgreSQL** and managed using **Prisma ORM** (`apps/core-api/prisma/schema.prisma`). It comprises over **100 relational tables** designed with strict foreign key constraints, composite indexes for high-throughput queries, and cascading updates.

---

## Domain Model Clusters

### 1. Organizational & Multi-Tenant Cluster
- `University`: Top-level tenant (domain, logo, admin contact, JSON config).
- `Institute`: College/school entity within a university (`schemaName`, `headUserId`).
- `Department`: Academic or administrative department within an institute.
- `UniversityDepartment`: Central university-level department mapping.

### 2. User, Authentication & Security Cluster
- `User`: Central user account (`email`, `passwordHash`, `role`, `isActive`, `mustChangePassword`, `universityId`, `instituteId`, `departmentId`).
- `Role`: Custom role definitions (`code`, `name`, `scopeLevel`).
- `Permission`: Fine-grained permission actions (`action`, `resource`).
- `UserRole`: Many-to-many junction connecting users to roles within a tenant scope.
- `MobileOtp`: Stores temporary 6-digit OTPs with expiration and retry counts.
- `PasswordHistory`: Hash history preventing reuse of the last $N$ passwords.
- `RegistrationRequest`: Tracks pending self-registration requests.
- `AuditLog`: System-wide audit log storing JSON field-level diffs (`oldValues`, `newValues`).

### 3. Academic Structure & Versioned Rules Cluster
- `Program`: Degree/Diploma offerings (e.g., B.Tech CS, MBA).
- `Batch`: Year-based cohort (e.g., Batch of 2024–2028).
- `Section`: Division of a batch (e.g., Section A, Section B).
- `Term`: Semester/Trimester division within a batch.
- `Subject`: Course unit offered by a department.
- `StreamLabel`: **Immutable rule snapshot** governing graduation requirements for a batch.
- `SubjectLabel`: Immutable rule snapshot governing course curriculum requirements.
- `SubjectPool`: Grouping of elective subjects for student choice.
- `StudentElectiveChoice`: Student choices submitted for subject pools.

### 4. Student & Admissions Cluster
- `StudentProfile`: Extended profile data (enrollment number, roll number, stream label reference, guardian contact, address).
- `ApplicationForm`: Configured admission form definition.
- `FormSubmission`: Submitted student admission application.
- `MeritList`: Generated ranking list for admission approval.
- `MeritListCandidate`: Individual candidate position and score on a merit list.

### 5. Examination & Grading Cluster
- `ExamSchedule`: Exam timetable slot, duration, total marks, and room assignment.
- `ExamPaper`: Question paper composition for offline/online exams.
- `Question`: Question bank item (`type`, `difficulty`, `marks`, `content`).
- `QuestionOption`: Multiple-choice option for a question.
- `ExamAttempt`: Student submission session for a CBE exam (`startTime`, `submitTime`, `score`, `status`).
- `ExamProctorLog`: Suspicious activity event logged during CBE (`tabSwitches`, `webcamSnapshots`, `deviceFingerprint`).
- `QuestionChallenge`: Student challenge against exam question accuracy post-exam.
- `ExamResult`: Published term results, SGPA, CGPA, and letter grades.

### 6. Fee & Financial Ledger Cluster
- `FeeHead`: Categorized fee item (Tuition, Library Deposit, Hostel Fee, Exam Fee).
- `FeeStructure`: Grouping of fee heads for a program/batch/term.
- `FeeDemand`: Invoice issued to a student (`amount`, `dueDate`, `status`).
- `FeeLedger`: Double-entry transaction record tracking all debits and credits per student account.
- `Payment`: Razorpay payment record (`transactionId`, `amount`, `paymentDate`, `status`).
- `DepositRefund`: Security deposit refund request and approval record.

### 7. Workflow Engine Cluster
- `WorkflowDefinition`: Configured workflow graph (name, entityType, triggerCondition).
- `WorkflowState`: State node within a workflow (e.g., "UNDER_REVIEW", "APPROVED").
- `WorkflowTransition`: Valid transition arrow between states.
- `WorkflowInstance`: Active execution instance of a workflow for a target entity.
- `WorkflowStepInstance`: History log of step executions, comments, and actor decisions.
- `WorkflowHold`: Soft reservation hold on resources/payments during workflow progress (Saga pattern).

---

## Core Enums Reference

```typescript
// Roles
enum ApplicationRole {
  SuperAdmin,
  UnivAdmin,
  InstAdmin,
  Student,
  Applicant,
  Alumni
}

// Workflow Engine
enum WorkflowStatus {
  DRAFT,
  ACTIVE,
  IN_PROGRESS,
  APPROVED,
  REJECTED,
  CANCELLED,
  EXPIRED
}

// Fee Management
enum FeeDemandStatus {
  PENDING,
  PARTIALLY_PAID,
  PAID,
  OVERDUE,
  CANCELLED
}

// Examinations
enum ExamType {
  TRADITIONAL_OFFLINE,
  CBE_ONLINE,
  HYBRID
}

enum AttemptStatus {
  NOT_STARTED,
  IN_PROGRESS,
  PAUSED,
  SUBMITTED,
  TERMINATED_PROCTOR
}
```

---

## API Architecture & Conventions

### URL Naming Conventions
All endpoints follow standard RESTful conventions prefixed with `/api/v1/`:

- `GET /api/v1/academic/programs` - List academic programs
- `POST /api/v1/admissions/applications` - Submit an application
- `GET /api/v1/fee/demands/my-demands` - Fetch student fee demands
- `POST /api/v1/examination/cbe/start-attempt` - Start online exam attempt
- `POST /api/v1/workflow/instances/:id/action` - Submit workflow step decision

---

## Authentication & Request Context

### Header Standards
For all protected routes, clients must pass the JWT token in the `Authorization` header:

```http
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
```

### Context Resolution (`req.user`)
The `GlobalJwtAuthGuard` extracts token payload and populates `req.user` with:
- `userId`: Sub ID of authenticated user
- `email`: User email
- `roles`: Assigned application and staff roles
- `universityId`: Bound university tenant ID
- `instituteId`: Bound institute ID (if scoped)
- `departmentId`: Bound department ID (if scoped)

---

## Standardized Response & Error Contracts

### 1. Successful API Response
```json
{
  "statusCode": 200,
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}
```

### 2. Standardized Error Response (`HttpExceptionFilter`)
```json
{
  "statusCode": 400,
  "success": false,
  "error": "Bad Request",
  "message": "Invalid input parameters: amount must be greater than 0",
  "timestamp": "2026-08-05T17:15:00.000Z",
  "path": "/api/v1/fee/demands"
}
```
