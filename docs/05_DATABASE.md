# University ERP - Database

## Overview

The database is **PostgreSQL 16** managed through **Prisma 5.x** ORM. The schema contains **100+ models** covering all aspects of university operations, organized into logical domains with complex relationships.

## Technology Stack

- **Database**: PostgreSQL 16
- **ORM**: Prisma 5.x
- **Migration**: Prisma Migrate
- **Seeding**: Custom seed scripts
- **Connection**: Connection pooling via Prisma

## Database Configuration

### Connection String

```
DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
```

### Environment Variables

- **POSTGRES_USER**: Database user
- **POSTGRES_PASSWORD**: Database password
- **POSTGRES_DB**: Database name
- **DATABASE_URL**: Full connection string

### Prisma Configuration

```prisma
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}
```

## Schema Organization

The schema is organized into logical domains:

### 1. Core Domain (University, Institute, User)

#### University
- **Purpose**: Top-level university entity
- **Key Fields**: name, domain, config (Json), branding (Json)
- **Relations**: Institutes, Users, Departments, FeeHeads

#### Institute
- **Purpose**: Individual colleges under a university
- **Key Fields**: name, schemaName, config (Json), branding (Json)
- **Relations**: University, Departments, Users, Resources

#### User
- **Purpose**: System users (students, staff, admins)
- **Key Fields**: email, passwordHash, role, scope, socialLinks (Json)
- **Relations**: University, Institute, RefreshToken, Notification, UserRoleAssignment

#### Role
- **Purpose**: Role definitions
- **Key Fields**: name, roleType, scope, description
- **Relations**: University, UserRoleAssignment

#### UserRoleAssignment
- **Purpose**: Multi-role assignment to users
- **Key Fields**: userId, roleId, roleName, instituteId, isPrimary
- **Relations**: User, Role

### 2. Authentication Domain

#### RefreshToken
- **Purpose**: JWT refresh tokens
- **Key Fields**: userId, token, expiresAt
- **Relations**: User

#### MobileOtp
- **Purpose**: Mobile OTP for registration/password reset
- **Key Fields**: phone, purpose, codeHash, expiresAt, attempts

#### PasswordHistory
- **Purpose**: Password history for reuse policy
- **Key Fields**: userId, passwordHash, createdAt

### 3. Academic Domain

#### UniversityDepartment
- **Purpose**: University-level departments
- **Key Fields**: name, code, shortName, isAcademic
- **Relations**: University, UniversityCourse, Department

#### UniversityCourse
- **Purpose**: University-level courses
- **Key Fields**: name, code, shortName
- **Relations**: UniversityDepartment, UniversityStream, Programme

#### UniversityStream
- **Purpose**: Streams within courses
- **Key Fields**: name, code, shortName
- **Relations**: UniversityCourse, UniversitySubject, StreamLabel

#### UniversitySubject
- **Purpose**: Subjects within streams
- **Key Fields**: name, code, shortName, isElective
- **Relations**: UniversityStream, SubjectLabel, Question, StaffSubject

#### Department
- **Purpose**: Institute-level departments
- **Key Fields**: name, code, headUserId
- **Relations**: Institute, UniversityDepartment, Programme, Staff

#### Programme
- **Purpose**: Academic programs
- **Key Fields**: name, code, calendarType, durationYears, totalCredits
- **Relations**: Department, UniversityCourse, Course, FeeStructure

#### Course
- **Purpose**: Courses within programs
- **Key Fields**: name, code, credits, applicationFee, tuitionFee
- **Relations**: Programme, UniversityStream, Batch, StudentAttendance

#### Batch
- **Purpose**: Student batches
- **Key Fields**: academicYear, semester, batchName, batchSize, admissionMode
- **Relations**: Course, StreamLabel, Section, ExamPaper

#### Section
- **Purpose**: Sections within batches
- **Key Fields**: name, sectionSize, lunchStart, lunchEnd
- **Relations**: Batch, Student, TimetableEntry

#### Student
- **Purpose**: Enrolled students
- **Key Fields**: enrollmentNo, firstName, lastName, status
- **Relations**: Section, StudentAttendance, FeeLedger, IssuedDocument

### 4. Academic Configuration Layer (Versioned)

#### StreamLabel
- **Purpose**: Versioned academic program rules
- **Key Fields**: label, version, status, gradingScaleType, gradeBoundaries
- **Relations**: UniversityStream, Batch, SubjectPool

#### SubjectLabel
- **Purpose**: Versioned subject-specific rules
- **Key Fields**: label, version, status, totalCredits, internalTotalMarks, externalTotalMarks
- **Relations**: UniversitySubject, BatchTermSubject, StudentSubjectEnrollment

#### SubjectPool
- **Purpose**: Elective subject pools
- **Key Fields**: poolName, minSelection, maxSelection
- **Relations**: StreamLabel, SubjectPoolMember, BatchTermSubject

#### SubjectPoolMember
- **Purpose**: Subjects in pools
- **Key Fields**: poolId, subjectLabelId, sortOrder
- **Relations**: SubjectPool, SubjectLabel

### 5. Batch & Term Layer

#### BatchTerm
- **Purpose**: Terms within batches
- **Key Fields**: termNumber, termLabel, startDate, endDate, isFrozen
- **Relations**: Batch, BatchTermSubject, StudentTermResult

#### BatchTermSubject
- **Purpose**: Subjects in terms
- **Key Fields**: subjectLabelId, subjectPoolId, isFrozen
- **Relations**: BatchTerm, SubjectLabel, SubjectPool, StudentSubjectEnrollment

#### StudentSubjectEnrollment
- **Purpose**: Student subject enrollment
- **Key Fields**: subjectLabelId, status
- **Relations**: Student, BatchTermSubject, SubjectLabel, StudentMarks

### 6. Marks & Results Layer

#### StudentMarks
- **Purpose**: Student marks by component
- **Key Fields**: componentType, marksObtained, maxMarks, attemptNumber, isLocked
- **Relations**: StudentSubjectEnrollment, BatchTermSubject

#### StudentSubjectAttendance
- **Purpose**: Session-level attendance
- **Key Fields**: attendanceType, sessionDate, sessionNumber, status
- **Relations**: StudentSubjectEnrollment

#### SubjectAttendanceSummary
- **Purpose**: Aggregated attendance
- **Key Fields**: attendanceType, totalSessions, attended, condonated
- **Relations**: StudentSubjectEnrollment

#### StudentTermResult
- **Purpose**: Term-wise results
- **Key Fields**: sgpa, creditsEarned, backlogs, resultState
- **Relations**: Student, BatchTerm

#### StudentCumulativeResult
- **Purpose**: Cumulative CGPA
- **Key Fields**: cgpa, cgpaPercentage, degreeAwarded, degreeClass
- **Relations**: Student, BatchTerm

#### ResultHold
- **Purpose**: Result holds (attendance, fees, etc.)
- **Key Fields**: holdReasonType, description, status
- **Relations**: Student, BatchTerm

#### ReAssessmentRequest
- **Purpose**: Re-totalling, re-evaluation requests
- **Key Fields**: requestType, componentType, status, originalMark, outcomeMark
- **Relations**: Student, BatchTermSubject

### 7. Exam Domain

#### ExamConfig
- **Purpose**: University-wide exam configuration
- **Key Fields**: minInvigilatorsPerRoom, invigilatorBaseStudents, fnStart, anStart
- **Relations**: University

#### Question
- **Purpose**: Question bank
- **Key Fields**: questionText, questionType, options, correctAnswer, difficulty, marks
- **Relations**: Course, UniversitySubject, Institute, ExamPaperQuestion

#### ExamPaper
- **Purpose**: Exam papers
- **Key Fields**: title, examType, totalMarks, passingMarks, durationMins
- **Relations**: Course, Batch, ExamPaperQuestion, ExamAttempt

#### ExamPaperQuestion
- **Purpose**: Questions in papers
- **Key Fields**: marks, sortOrder
- **Relations**: ExamPaper, Question

#### ExamAttempt
- **Purpose**: Student exam attempts
- **Key Fields**: startedAt, submittedAt, totalMarks, obtainedMarks, status
- **Relations**: ExamPaper, Student, ExamResponse, ExamProctorEvent

#### ExamResponse
- **Purpose**: Student responses
- **Key Fields**: responseText (Json), isCorrect, marksAwarded
- **Relations**: ExamAttempt, Question

#### ExamProctorEvent
- **Purpose**: Proctoring events
- **Key Fields**: type, detail (Json)
- **Relations**: ExamAttempt

#### ExamSnapshot
- **Purpose**: Webcam snapshots
- **Key Fields**: fileUrl, imageData, flagged, reason
- **Relations**: ExamAttempt

#### ExamDirective
- **Purpose**: Invigilator directives
- **Key Fields**: type, message, minutes
- **Relations**: ExamAttempt

#### ExamSchedule
- **Purpose**: Exam scheduling
- **Key Fields**: examType, scheduledDate, startTime, endTime, venueDetails (Json)
- **Relations**: BatchTerm, BatchTermSubject, ExamInvigilator

#### ExamInvigilator
- **Purpose**: Invigilator assignments
- **Key Fields**: roomName
- **Relations**: ExamSchedule, Staff

#### QuestionChallenge
- **Purpose**: Student question challenges
- **Key Fields**: category, description, status, awardedMarks
- **Relations**: ExamPaper, Question

#### SupplementaryExam
- **Purpose**: Supplementary/back-paper exams
- **Key Fields**: attemptNumber, status, marksObtained
- **Relations**: Student, BatchTermSubject

### 8. Attendance Domain

#### StudentAttendance
- **Purpose**: Course-level attendance
- **Key Fields**: date, session, status, remarks
- **Relations**: Student, Course, Staff

#### FacultyAttendance
- **Purpose**: Faculty attendance
- **Key Fields**: date, session, status, leaveType, substituteId
- **Relations**: Staff

#### NtStaffAttendance
- **Purpose**: Non-teaching staff attendance
- **Key Fields**: date, status, inTime, outTime, overtimeHrs
- **Relations**: Staff

#### AttendanceConfig
- **Purpose**: Attendance configuration
- **Key Fields**: alertThresholdPct, blockExamCardPct, shiftStartTime
- **Relations**: University

### 9. Fee Domain

#### FeeHead
- **Purpose**: Fee head catalog
- **Key Fields**: code, name, category, amountType, defaultAmount
- **Relations**: University, Institute, FeeDemand

#### FeeStructure
- **Purpose**: Fee structures
- **Key Fields**: academicYear, semester, feeHeads (Json)
- **Relations**: Institute, Programme

#### FeeLedger
- **Purpose**: Student fee ledger
- **Key Fields**: feeHead, amountDue, amountPaid, lateFee, dueDate, status
- **Relations**: Student, Payment, FeeWaiver

#### Payment
- **Purpose**: Payment records
- **Key Fields**: amount, paymentMode, gatewayRef, receiptNo
- **Relations**: FeeLedger

#### Scholarship
- **Purpose**: Scholarships
- **Key Fields**: name, amountType, amountValue, applicableFeeHeads (Json)
- **Relations**: Institute, FeeWaiver

#### FeeWaiver
- **Purpose**: Fee waivers
- **Key Fields**: waiverType, waiverAmount, status
- **Relations**: Student, Scholarship, FeeLedger

#### GovtReimbursement
- **Purpose**: Government reimbursements
- **Key Fields**: scheme, category, expectedAmt, receivedAmt
- **Relations**: Student, FeeLedger

#### StudentPayable
- **Purpose**: Exam module payables
- **Key Fields**: payableType, amount, referenceId, status
- **Relations**: Student

### 10. Staff & HR Domain

#### Staff
- **Purpose**: Staff records
- **Key Fields**: employeeId, staffType, designation, dateOfJoining
- **Relations**: Department, User, StaffSubject, LeaveApplication

#### StaffSubject
- **Purpose**: Staff-subject mapping
- **Key Fields**: universitySubjectId
- **Relations**: Staff, UniversitySubject

#### LeaveType
- **Purpose**: Leave types
- **Key Fields**: code, name, maxDays, carryForward
- **Relations**: Institute, LeaveApplication, LeaveBalance

#### LeaveApplication
- **Purpose**: Leave applications
- **Key Fields**: fromDate, toDate, days, status
- **Relations**: Staff, LeaveType

#### LeaveBalance
- **Purpose**: Leave balances
- **Key Fields**: year, allocated, used, pending
- **Relations**: Staff, LeaveType

#### StaffDocument
- **Purpose**: Staff documents
- **Key Fields**: docType, name, fileUrl, expiresAt
- **Relations**: Staff

### 11. Infrastructure Domain

#### InstituteResourceType
- **Purpose**: Resource types
- **Key Fields**: name, category
- **Relations**: Institute, InstituteResource

#### InstituteResource
- **Purpose**: Institute resources
- **Key Fields**: name, capacity, facilities (Json)
- **Relations**: Institute, InstituteResourceType, ResourceReservation

#### ResourceReservation
- **Purpose**: Resource bookings
- **Key Fields**: startAt, endAt, status, seriesId
- **Relations**: Institute, InstituteResource, Section, Staff, BatchTermSubject

#### BatchTermSubjectResource
- **Purpose**: Per-subject eligible resources
- **Key Fields**: component
- **Relations**: BatchTermSubject, InstituteResource

#### ScheduleRun
- **Purpose**: Scheduler run tracking
- **Key Fields**: status, params (Json), generatedCount
- **Relations**: Institute, BatchTerm

#### Hostel
- **Purpose**: Hostels
- **Key Fields**: name, category, totalRooms, wardenId
- **Relations**: Institute, HostelRoom, User

#### HostelRoom
- **Purpose**: Hostel rooms
- **Key Fields**: roomNumber, capacity, occupied, amenity, monthlyFee
- **Relations**: Hostel, HostelAllocation

#### HostelAllocation
- **Purpose**: Hostel allocations
- **Key Fields**: fromDate, toDate, status
- **Relations**: HostelRoom, Student

#### HostelConfig
- **Purpose**: Hostel configuration
- **Key Fields**: blockingWindowDays, messFeeMonthly
- **Relations**: Institute

#### TransportRoute
- **Purpose**: Transport routes
- **Key Fields**: routeNo, name, startPoint, endPoint, monthlyFee
- **Relations**: Institute, TransportVehicle, TransportPass

#### TransportVehicle
- **Purpose**: Transport vehicles
- **Key Fields**: regNumber, vehicleType, capacity, driverId
- **Relations**: TransportRoute

#### TransportPass
- **Purpose**: Transport passes
- **Key Fields**: boardingStop, validFrom, validTo, status
- **Relations**: Student, TransportRoute

#### TransportConfig
- **Purpose**: Transport configuration
- **Key Fields**: blockingWindowDays, lateCancelFee
- **Relations**: Institute

#### LibraryConfig
- **Purpose**: Library configuration
- **Key Fields**: maxBooksPerStudent, issuePeriodDays, finePerDay
- **Relations**: Institute

#### Book
- **Purpose**: Library books
- **Key Fields**: title, authors (Json), isbn, totalCopies, availableCopies
- **Relations**: Institute, BookCopy, BookIssue, BookReservation

#### BookCopy
- **Purpose**: Book copies
- **Key Fields**: barcode, condition, isAvailable
- **Relations**: Book, BookIssue, BookReservation

#### BookIssue
- **Purpose**: Book issues
- **Key Fields**: issuedAt, dueDate, fineAmount, status
- **Relations**: Book, BookCopy

#### BookReservation
- **Purpose**: Book reservations
- **Key Fields**: status, holdExpiresAt
- **Relations**: Book, BookCopy

### 12. Library Domain

#### HolidayCalendar
- **Purpose**: Holiday calendar
- **Key Fields**: scope, date, name, type, halfDay
- **Relations**: University, Institute

### 13. Document Domain

#### DocumentTemplate
- **Purpose**: Document templates
- **Key Fields**: name, documentCode, templateHtml, variables (Json)
- **Relations**: University, IssuedDocument

#### IssuedDocument
- **Purpose**: Issued documents
- **Key Fields**: serialNo, documentData (Json), fileUrl, qrCode, status
- **Relations**: DocumentTemplate, Student

### 14. Form Domain

#### FormTemplate
- **Purpose**: Dynamic form templates
- **Key Fields**: title, fields (Json), groups (Json), visibleToRoles (Json)
- **Relations**: FormSubmission

#### FormSubmission
- **Purpose**: Form submissions
- **Key Fields**: data (Json), status
- **Relations**: FormTemplate, Student

### 15. Workflow Domain

#### WorkflowDefinition
- **Purpose**: Workflow definitions
- **Key Fields**: name, entityType, initiatorRoles (Json), config (Json)
- **Relations**: WorkflowState, WorkflowTransition, WorkflowInstance

#### WorkflowState
- **Purpose**: Workflow states
- **Key Fields**: key, name, type, actorType, actorRole, isPaymentGate
- **Relations**: WorkflowDefinition, WorkflowTransition

#### WorkflowTransition
- **Purpose**: Workflow transitions
- **Key Fields**: fromStateId, toStateId, decision, isParallel
- **Relations**: WorkflowDefinition, WorkflowState

#### WorkflowInstance
- **Purpose**: Workflow instances
- **Key Fields**: status, outcome, data (Json), joinState (Json)
- **Relations**: WorkflowDefinition, WorkflowTask, WorkflowReservation

#### WorkflowTask
- **Purpose**: Workflow tasks
- **Key Fields**: stateKey, actorRole, status, decision
- **Relations**: WorkflowInstance

#### WorkflowInstanceEvent
- **Purpose**: Workflow events
- **Key Fields**: type, stateKey, decision, message
- **Relations**: WorkflowInstance

#### WorkflowReservation
- **Purpose**: Resource holds
- **Key Fields**: resourceType, resourceId, qty, status
- **Relations**: WorkflowInstance

### 16. ID Format Domain

#### IdFormat
- **Purpose**: ID format configuration
- **Key Fields**: name, purpose, pattern, resetScope
- **Relations**: IdSequenceCounter

#### IdSequenceCounter
- **Purpose**: ID sequence counters
- **Key Fields**: scopeKey, value
- **Relations**: IdFormat

#### IdCustomToken
- **Purpose**: Custom ID tokens
- **Key Fields**: key, label, options (Json)
- **Relations**: University

### 17. Communication Domain

#### Notification
- **Purpose**: User notifications
- **Key Fields**: title, body, type, isRead
- **Relations**: User

#### SocialHandle
- **Purpose**: Social media handles
- **Key Fields**: platform, handle, profileUrl
- **Relations**: University, SocialPost

#### SocialPost
- **Purpose**: Social media posts
- **Key Fields**: platformId, content, mediaUrls (Json), sentiment
- **Relations**: SocialHandle

#### Banner
- **Purpose**: Login banners
- **Key Fields**: title, message, severity, targetRoles (Json)
- **Relations**: University, BannerReceipt

#### BannerReceipt
- **Purpose**: Banner receipts
- **Key Fields**: firstSeenAt, lastShownAt, showCount
- **Relations**: Banner, User

#### Notice
- **Purpose**: Notice board
- **Key Fields**: tab, body (markdown), isVisible, pinned
- **Relations**: University, Institute

#### NoticeTag
- **Purpose**: Notice tags
- **Key Fields**: name, slug
- **Relations**: Institute

### 18. Counselling Domain

#### Counsellor
- **Purpose**: Empanelled counsellors
- **Key Fields**: city, experienceYears, active
- **Relations**: User, CounsellorContract, CounsellingRequest

#### CounsellorContract
- **Purpose**: Counsellor contracts
- **Key Fields**: startDate, endDate, compensation (Json)
- **Relations**: Counsellor

#### CounsellingRequest
- **Purpose**: Counselling requests
- **Key Fields**: courseType, connectMode, status, feedbackRating
- **Relations**: Counsellor, CounsellingComment

#### CounsellingComment
- **Purpose**: Counselling comments
- **Key Fields**: body
- **Relations**: CounsellingRequest

#### CounsellorEnrollmentCredit
- **Purpose**: Counsellor credits
- **Key Fields**: enrollmentNo, enrolledAt
- **Relations**: Counsellor

### 19. Registration Domain

#### RegistrationRequest
- **Purpose**: Registration requests
- **Key Fields**: userType, status, registrationData (Json), applicationNo
- **Relations**: University, FeeDemand

#### StudentProfile
- **Purpose**: Student profiles
- **Key Fields**: enrollmentNo, status
- **Relations**: User, University

### 20. Audit Domain

#### AuditLog
- **Purpose**: Audit log
- **Key Fields**: actorId, actionType, module, entityType, oldValue (Json), newValue (Json)
- **Relations**: None

### 21. Access Control Domain

#### ModuleAccess
- **Purpose**: Module access configuration
- **Key Fields**: moduleKey, readRoles (Json), writeRoles (Json)
- **Relations**: University

### 22. Other Domain

#### Room
- **Purpose**: Rooms
- **Key Fields**: name, building, capacity, roomType
- **Relations**: Institute, RoomBooking

#### RoomBooking
- **Purpose**: Room bookings
- **Key Fields**: purpose, fromTime, toTime, status
- **Relations**: Room

#### Equipment
- **Purpose**: Equipment
- **Key Fields**: name, assetTag, category, status
- **Relations**: Institute

#### ParentLink
- **Purpose**: Parent-student links
- **Key Fields**: relation, isPrimary, verifiedAt
- **Relations**: Student

## Key Relationships

### University → Institute → Department Hierarchy

```
University (1) ──< (N) Institute (1) ──< (N) Department
```

### Academic Hierarchy

```
UniversityDepartment ──< UniversityCourse ──< UniversityStream ──< UniversitySubject
                                    │
                                    └─< StreamLabel ──< SubjectLabel
```

### Institute Academic Hierarchy

```
Department ──< Programme ──< Course ──< Batch ──< Section ──< Student
```

### Batch/Term Structure

```
Batch ──< BatchTerm ──< BatchTermSubject ──< StudentSubjectEnrollment
```

### User Multi-Role

```
User ──< UserRoleAssignment ──> Role
```

## Indexes

### Strategic Indexes

- **Foreign keys**: All foreign key fields indexed
- **Unique constraints**: Composite unique indexes
- **Query optimization**: Indexes on frequently queried fields

### Examples

```prisma
@@index([userId])
@@index([roleId])
@@unique([userId, roleName, instituteId])
@@index([universityId])
```

## Audit Middleware

### Purpose

Automatic field-level audit logging for all database operations.

### Behavior

- **Logs**: create, update, upsert, delete
- **Tracks**: actor (user), action, entity, field changes
- **Redacts**: Sensitive fields (passwords, tokens)
- **Ignores**: Noise fields (updatedAt, lastLoginAt)
- **Denylist**: AuditLog, RefreshToken, MobileOtp, etc.

### Implementation

```typescript
// src/database/audit-middleware.ts
prisma.$use(async (params, next) => {
  // Audit logic
  const result = await next(params)
  // Log changes
  return result
})
```

## Migrations

### Migration Strategy

- **Tool**: Prisma Migrate
- **Location**: `prisma/migrations/`
- **Naming**: Timestamped migration files
- **Baseline**: Pre-baseline migrations archived

### Running Migrations

```bash
# Development
npx prisma migrate dev

# Production
npx prisma migrate deploy
```

### Seeding

- **Location**: `prisma/seed.ts`
- **Scripts**: `prisma/seed-*.js/ts`
- **Categories**: 
  - Seed defaults
  - Seed roles
  - Seed master data
  - Seed forms
  - Seed workflows
  - Seed question banks

## Database Size

### Estimated Size

- **Tables**: 100+
- **Indexes**: 200+
- **Relations**: 300+
- **Schema Lines**: 2999

## Performance Considerations

### Connection Pooling

Prisma manages connection pooling automatically.

### Query Optimization

- **Select only needed fields**: Prisma select
- **Use indexes**: Strategic indexes on foreign keys
- **Batch operations**: createMany, updateMany
- **Transactions**: Prisma transactions for multi-step operations

### Caching

- **Redis**: Cache frequently accessed data
- **Query caching**: React Query on frontend
- **Denormalization**: Cached computed fields

## Backup Strategy

### Docker Volumes

```
docker-volumes/postgres/
```

### Backup Commands

```bash
# Backup
pg_dump -U postgres university_erp > backup.sql

# Restore
psql -U postgres university_erp < backup.sql
```

## Known Limitations

1. **No Read Replicas**: Single database instance
2. **No Sharding**: Single database for all tenants
3. **No Partitioning**: All tables in default schema
4. **No Materialized Views**: Not using materialized views
5. **Limited Stored Procedures**: Using application logic instead
