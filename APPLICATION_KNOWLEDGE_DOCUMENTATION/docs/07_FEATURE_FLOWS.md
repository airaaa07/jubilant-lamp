# University ERP - Feature Flows

## Overview

This document describes the execution flows for major features in the University ERP system, including sequence diagrams and step-by-step process descriptions.

## 1. User Registration Flow

### Flow Diagram

```
User → React Form → API → Service → Prisma → Database
                         ↓
                    OTP Service → SMS/Email
```

### Step-by-Step

1. **User fills registration form**
   - Enters personal details
   - Enters email and phone
   - Solves CAPTCHA
   - Submits form

2. **Frontend validation**
   - Zod schema validation
   - CAPTCHA verification
   - Password policy check

3. **API call**: `POST /api/auth/register`
   - Controller receives request
   - DTO validation via ZodValidationPipe

4. **Service processing**
   - Check if email/phone already exists
   - Hash password with bcrypt
   - Create RegistrationRequest record
   - Determine OTP requirements (email/SMS based on university config)

5. **OTP sending**
   - If SMS required: Send mobile OTP
   - If email required: Send email OTP
   - Store OTP hash in MobileOtp table

6. **Response**
   - Return success message
   - Indicate which OTPs are required

7. **User verification**
   - User enters OTP(s)
   - Frontend calls verify endpoints
   - Service validates OTP hash
   - On success: Create User record
   - On success: Assign default role
   - On success: Send welcome email

### Key Files

- **Frontend**: `web/admin-portal/src/pages/RegisterPage.tsx`
- **Controller**: `apps/core-api/src/modules/auth/auth.controller.ts`
- **Service**: `apps/core-api/src/modules/auth/auth.service.ts`
- **DTO**: `apps/core-api/src/modules/auth/dto/register.dto.ts`

## 2. Login Flow

### Flow Diagram

```
User → Login Form → API → LocalAuthGuard → AuthService → Prisma → Database
                                        ↓
                                   JWT Generation
                                        ↓
                                   Token Response
```

### Step-by-Step

1. **User enters credentials**
   - Email
   - Password
   - CAPTCHA (if enabled)

2. **Frontend validation**
   - Required fields
   - Email format

3. **API call**: `POST /api/auth/login`
   - Controller receives request
   - LocalAuthGuard intercepts

4. **Passport authentication**
   - PassportLocalStrategy validates credentials
   - Finds user by email
   - Compares password hash with bcrypt
   - On success: Attaches user to request

5. **Service processing**
   - Generate access token (15 min expiry)
   - Generate refresh token (7 days expiry)
   - Store refresh token in database
   - Update lastLoginAt timestamp
   - Check profile completeness

6. **Response**
   - Return accessToken
   - Return refreshToken
   - Return user profile
   - Return profile completeness status

7. **Frontend storage**
   - Store accessToken in localStorage
   - Store refreshToken in localStorage
   - Update AuthContext
   - Redirect to dashboard

### Key Files

- **Frontend**: `web/admin-portal/src/pages/LoginPage.tsx`
- **Controller**: `apps/core-api/src/modules/auth/auth.controller.ts`
- **Service**: `apps/core-api/src/modules/auth/auth.service.ts`
- **Guard**: `apps/core-api/src/modules/auth/guards/local.guard.ts`
- **Strategy**: `apps/core-api/src/modules/auth/strategies/local.strategy.ts`

## 3. Admission Application Flow

### Flow Diagram

```
User → Form → Workflow → Payment → Approval → Enrollment
         ↓
    Dynamic Form Builder
         ↓
    Workflow Engine
         ↓
    Fee Module
         ↓
    Admission Module
```

### Step-by-Step

1. **User starts application**
   - Navigate to admissions page
   - Select program/course
   - Click "Apply"

2. **Form rendering**
   - Load FormTemplate for registration
   - Render dynamic form fields
   - User fills form data

3. **Form submission**
   - Validate form data
   - Create FormSubmission record
   - Start WorkflowInstance

4. **Workflow execution**
   - Initial state: "Application Submitted"
   - Create WorkflowTask for reviewer
   - Send notification to reviewer

5. **Document upload**
   - User uploads documents (photo, ID proof, etc.)
   - Files uploaded to MinIO
   - URLs stored in FormSubmission data

6. **Payment gate (if configured)**
   - Create FeeDemand for application fee
   - Redirect to payment gateway (Razorpay)
   - On success: Update FeeDemand status
   - On success: Advance workflow state

7. **Review process**
   - Reviewer sees task in My Tasks
   - Reviewer reviews application
   - Reviewer approves/rejects with notes

8. **Approval flow**
   - If approved: Advance to next state
   - If rejected: End workflow
   - If send back: Return to applicant

9. **Final approval**
   - Generate application number
   - Create User record (if not exists)
   - Create Student record
   - Assign enrollment number
   - Send confirmation email

### Key Files

- **Frontend**: `web/admin-portal/src/pages/RegisterPage.tsx`
- **Workflow**: `apps/core-api/src/modules/workflow/`
- **Forms**: `apps/core-api/src/modules/forms/`
- **Admissions**: `apps/core-api/src/modules/admissions/`
- **Fees**: `apps/core-api/src/modules/fee/`

## 4. Computer-Based Examination (CBE) Flow

### Flow Diagram

```
Student → Exam Interface → CBE Engine (WebSocket) → Core API → Database
                              ↓
                         Real-time Events
                              ↓
                         Proctoring
                              ↓
                         Auto-grading
```

### Step-by-Step

1. **Exam start**
   - Student navigates to exam page
   - Frontend checks ExamPaper status
   - If published: Show exam interface
   - If not published: Show "not available" message

2. **WebSocket connection**
   - Connect to CBE Engine (ws://localhost:3001)
   - Send exam attempt ID
   - Receive exam configuration

3. **Exam activation**
   - Check activationLeadMins
   - If within window: Unlock exam
   - If before window: Show countdown

4. **Question rendering**
   - Fetch questions from ExamPaper
   - Shuffle questions (if configured)
   - Render questions one by one or all at once

5. **Answer submission**
   - Student selects answers
   - Send answers via WebSocket
   - Server stores in ExamResponse table
   - Update lastSeenAt timestamp

6. **Proctoring**
   - Request camera permission (if required)
   - Capture periodic snapshots
   - Upload snapshots to MinIO
   - Detect violations:
     - Tab switch
     - Fullscreen exit
     - No face detected
     - Multiple faces
     - Audio high

7. **Violation handling**
   - Log ExamProctorEvent
   - Increment warningCount
   - If warnings > maxWarnings: Auto-submit
   - Send ExamDirective to student

8. **Invigilator monitoring**
   - Invigilator views ExamMonitorPage
   - See live snapshots
   - See proctoring events
   - Send directives:
     - Message
     - Extend time
     - Terminate

9. **Exam submission**
   - Student clicks submit
   - Or auto-submit on time up
   - Or auto-submit on max warnings
   - Close WebSocket connection

10. **Auto-grading**
    - Process ExamResponse records
    - Compare with correctAnswer
    - Calculate marks per question
    - Calculate total marks
    - Calculate percentage
    - Determine result (pass/fail)
    - Update ExamAttempt record

11. **Result publication**
    - Exam owner reviews results
    - Owner publishes results
    - Update isResultReleased flag
    - Calculate challengeWindowExpiry
    - Send result notifications

### Key Files

- **Frontend**: `web/admin-portal/src/pages/ExamTakePage.tsx`
- **CBE Engine**: `apps/cbe-engine/src/`
- **Exam Module**: `apps/core-api/src/modules/examination/`
- **WebSocket**: Socket.IO integration

## 5. Fee Payment Flow

### Flow Diagram

```
Student → Fee Ledger → Payment Gateway → Razorpay → Core API → Database
                                           ↓
                                      Payment Confirmation
                                           ↓
                                      Update Ledger
                                           ↓
                                      Receipt Generation
```

### Step-by-Step

1. **View fee ledger**
   - Student navigates to fees page
   - Fetch FeeLedger records
   - Show pending dues
   - Show payment history

2. **Initiate payment**
   - Student selects fee to pay
   - Click "Pay Now"
   - Frontend calls payment initiation API

3. **Payment initiation**
   - API: `POST /api/fees/ledger/:studentId/pay`
   - Create Payment record (status: pending)
   - Call Razorpay API to create order
   - Return Razorpay order ID

4. **Razorpay checkout**
   - Frontend opens Razorpay checkout
   - Student completes payment
   - Razorpay returns payment ID

5. **Payment verification**
   - Frontend sends payment ID to API
   - API verifies with Razorpay
   - On success: Update Payment record
   - On success: Update FeeLedger (amountPaid)
   - On success: Generate receipt number
   - On success: Send email receipt

6. **Receipt generation**
   - Generate PDF receipt
   - Upload to MinIO
   - Store URL in Payment record
   - Send download link to student

### Key Files

- **Frontend**: `web/admin-portal/src/pages/FeesPage.tsx`
- **Fee Module**: `apps/core-api/src/modules/fee/`
- **Razorpay**: Razorpay SDK integration

## 6. Attendance Marking Flow

### Flow Diagram

```
Faculty → Attendance Form → API → Service → Prisma → Database
                                        ↓
                                   Attendance Summary
                                        ↓
                                   Alert Generation
```

### Step-by-Step

1. **Faculty opens attendance page**
   - Select course
   - Select date
   - Select session
   - Load student list

2. **Mark attendance**
   - Faculty marks each student (present/absent/condonated)
   - Add remarks if needed
   - Submit form

3. **API call**: `POST /api/attendance/students`
   - Controller receives attendance array
   - DTO validation

4. **Service processing**
   - Create StudentAttendance records
   - Update SubjectAttendanceSummary
   - Check attendance percentage
   - If below threshold: Generate alert
   - If below exam card threshold: Block exam card

5. **Notification**
   - Send notification to student
   - Send notification to parent (if linked)
   - Update student status if needed

6. **Response**
   - Return success message
   - Return updated attendance summary

### Key Files

- **Frontend**: `web/admin-portal/src/pages/AttendancePage.tsx`
- **Attendance Module**: `apps/core-api/src/modules/attendance/`
- **Notification Module**: `apps/core-api/src/modules/notifications/`

## 7. Timetable Scheduling Flow

### Flow Diagram

```
Admin → Timetable Form → API → Service → Prisma → Database
                                      ↓
                                 Resource Check
                                      ↓
                                 Conflict Detection
                                      ↓
                                 Reservation Creation
```

### Step-by-Step

1. **Admin opens timetable page**
   - Select batch/term
   - Select subject
   - Load available time slots
   - Load available resources

2. **Create timetable entry**
   - Select time slot
   - Select staff
   - Select room/resource
   - Set effective dates
   - Submit form

3. **API call**: `POST /api/timetable/entries`
   - Controller receives request
   - DTO validation

4. **Service processing**
   - Check staff availability
   - Check resource availability
   - Detect conflicts:
     - Staff double-booking
     - Resource double-booking
     - Section double-booking
   - If conflicts: Return error
   - If no conflicts: Create TimetableEntry
   - Create ResourceReservation

5. **Series generation**
   - If recurring: Generate series
   - Create multiple entries
   - Link with seriesId
   - Create multiple reservations

6. **Response**
   - Return created entries
   - Return any conflicts found

### Key Files

- **Frontend**: `web/admin-portal/src/pages/TimetablePage.tsx`
- **Timetable Module**: `apps/core-api/src/modules/timetable/`
- **Resource Module**: `apps/core-api/src/modules/resource-reservation/`

## 8. Document Generation Flow

### Flow Diagram

```
User → Document Request → API → Service → Template Engine → PDF → MinIO
                                            ↓
                                       Data Binding
                                            ↓
                                       PDF Generation
                                            ↓
                                       QR Code Generation
```

### Step-by-Step

1. **User requests document**
   - Navigate to documents page
   - Select document type
   - Select subject (student/staff)
   - Click "Generate"

2. **API call**: `POST /api/documents/issued`
   - Controller receives request
   - DTO validation

3. **Service processing**
   - Load DocumentTemplate
   - Fetch subject data (student/staff)
   - Bind data to template variables
   - Render HTML from template

4. **PDF generation**
   - Use Puppeteer (cert-generator service)
   - Convert HTML to PDF
   - Generate serial number
   - Generate QR code
   - Add QR code to PDF

5. **Storage**
   - Upload PDF to MinIO
   - Get presigned URL
   - Store URL in IssuedDocument record

6. **Response**
   - Return document details
   - Return download URL

7. **Delivery**
   - If softcopy: Student can download
   - If hardcopy: Mark as "Ready for collection"
   - Send notification to student

### Key Files

- **Frontend**: `web/admin-portal/src/pages/DocumentsPage.tsx`
- **Documents Module**: `apps/core-api/src/modules/documents/`
- **Certificate Generator**: `apps/cert-generator/src/`

## 9. Workflow Execution Flow

### Flow Diagram

```
User → Start Workflow → Workflow Engine → Task Creation → Assignment → Action → State Transition
                                              ↓
                                         Resource Reservation
                                              ↓
                                         Payment Gate (if configured)
                                              ↓
                                         Notification
```

### Step-by-Step

1. **User initiates workflow**
   - Select workflow definition
   - Fill initial form (if configured)
   - Submit to start workflow

2. **API call**: `POST /api/workflow/instances`
   - Controller receives request
   - DTO validation

3. **Service processing**
   - Load WorkflowDefinition
   - Create WorkflowInstance
   - Set initial state
   - Create initial task(s)

4. **Task assignment**
   - Determine actor for initial state
   - If role: Create tasks for all users with role
   - If resolver: Resolve to specific user
   - Send notifications

5. **Actor action**
   - Actor sees task in My Tasks
   - Actor opens task
   - Actor fills form (if configured)
   - Actor selects decision (approve/reject/send back)
   - Actor adds comment
   - Actor submits

6. **State transition**
   - Service validates decision
   - Find matching transition
   - Execute entry actions
   - Create next task(s)
   - Update WorkflowInstance state

7. **Resource reservation**
   - If state has resource holds:
     - Create WorkflowReservation
     - Adjust resource counters
     - Set expiry time

8. **Payment gate**
   - If state is payment gate:
     - Create FeeDemand
     - Wait for payment
     - On payment: Advance state

9. **Parallel execution**
   - If transition is parallel:
     - Create multiple tasks
     - Wait for all to complete
     - Join and advance

10. **Terminal state**
    - If state is terminal:
      - Set WorkflowInstance status
      - Set outcome (approved/rejected)
      - Release all reservations
      - Send final notification

### Key Files

- **Frontend**: `web/admin-portal/src/pages/WorkflowDesignerPage.tsx`
- **Workflow Module**: `apps/core-api/src/modules/workflow/`
- **Resource Module**: `apps/core-api/src/modules/resource-reservation/`

## 10. Result Processing Flow

### Flow Diagram

```
Faculty → Marks Entry → API → Service → Prisma → Result Calculation → CGPA Update
                                              ↓
                                         Grade Assignment
                                              ↓
                                         Result Hold Check
                                              ↓
                                         Publication
```

### Step-by-Step

1. **Faculty enters marks**
   - Select batch/term
   - Select subject
   - Load student list
   - Enter marks by component
   - Submit

2. **API call**: `POST /api/academic/marks`
   - Controller receives marks array
   - DTO validation

3. **Service processing**
   - Create StudentMarks records
   - Lock marks (isLocked = true)
   - Trigger result calculation

4. **Result calculation**
   - Aggregate marks by student
   - Calculate internal marks
   - Calculate external marks
   - Calculate total marks
   - Calculate percentage
   - Assign grade based on grade boundaries
   - Calculate SGPA
   - Calculate CGPA
   - Update StudentTermResult

5. **Result hold check**
   - Check for ResultHold records
   - If holds exist: Block publication
   - If no holds: Allow publication

6. **Approval**
   - HOD reviews results
   - HOD approves results
   - Set resultState to "approved"

7. **Publication**
   - Controller publishes results
   - Set resultState to "published"
   - Set publishedAt timestamp
   - Calculate challengeWindowExpiry
   - Send notifications to students

8. **Marksheet generation**
   - Wait for challenge window to expire
   - Check for pending ReAssessmentRequests
   - If none: Generate marksheet
   - Upload to MinIO
   - Send download link

### Key Files

- **Frontend**: `web/admin-portal/src/pages/ExaminationsPage.tsx`
- **Academic Module**: `apps/core-api/src/modules/academic/`
- **Examination Module**: `apps/core-api/src/modules/examination/`

## 11. Library Book Issue Flow

### Flow Diagram

```
Student → Book Search → Reservation → Collection → Issue → Return → Fine Calculation
```

### Step-by-Step

1. **Student searches books**
   - Navigate to library page
   - Search by title, author, ISBN
   - View book details
   - Check availability

2. **Reservation**
   - Student clicks "Reserve"
   - Create BookReservation record
   - Decrement availableCopies
   - Set holdExpiresAt (1 day)
   - Send notification

3. **Collection**
   - Student visits library
   - Librarian scans book barcode
   - Librarian scans student ID
   - Create BookIssue record
   - Set dueDate
   - Update BookReservation status
   - Send confirmation

4. **Return**
   - Student returns book
   - Librarian scans book barcode
   - Calculate days overdue
   - Calculate fine (if overdue)
   - Update BookIssue record
   - Increment availableCopies
   - If fine: Create FeeDemand

5. **Renewal**
   - Student requests renewal
   - Check renewal limit
   - Check if not reserved by others
   - Extend dueDate
   - Increment renewalCount

### Key Files

- **Frontend**: `web/admin-portal/src/pages/LibraryPage.tsx`
- **Library Module**: `apps/core-api/src/modules/library/`

## 12. Hostel Allocation Flow

### Flow Diagram

```
Student → Hostel Application → Workflow → Approval → Allocation → Room Assignment → Fee Generation
```

### Step-by-Step

1. **Student applies for hostel**
   - Navigate to hostel page
   - Select hostel preference
   - Select room type preference
   - Submit application

2. **Workflow execution**
   - Start hostel allocation workflow
   - Create WorkflowInstance
   - Create task for warden

3. **Warden review**
   - Warden reviews application
   - Check room availability
   - Approve or reject

4. **Allocation**
   - On approval: Find available room
   - Create HostelAllocation record
   - Update HostelRoom occupied count
   - Generate monthly fee demand

5. **Room assignment**
   - Assign student to specific room
   - Send room details to student
   - Send allocation notification

6. **Vacating**
   - Student requests vacating
   - Warden approves
   - Update HostelAllocation status
   - Update HostelRoom occupied count
   - Calculate final charges

### Key Files

- **Frontend**: `web/admin-portal/src/pages/HostelPage.tsx`
- **Hostel Module**: `apps/core-api/src/modules/hostel/`
- **Workflow Module**: `apps/core-api/src/modules/workflow/`

## 13. Notification Sending Flow

### Flow Diagram

```
Service → Queue Job → Redis Queue → Notification Worker → Email/SMS Gateway → Delivery
```

### Step-by-Step

1. **Service creates notification**
   - Create Notification record in database
   - Determine delivery channels (email/SMS)
   - Add job to queue

2. **Queue processing**
   - Bull queue stores job in Redis
   - Notification worker polls queue
   - Worker processes job

3. **Email sending**
   - Load email template
   - Bind data to template
   - Send via Nodemailer
   - Update Notification status

4. **SMS sending**
   - Format SMS message
   - Send via SMS gateway
   - Update Notification status

5. **Failure handling**
   - On failure: Retry with backoff
   - After max retries: Mark as failed
   - Log error

### Key Files

- **Notification Module**: `apps/core-api/src/modules/notifications/`
- **Notification Worker**: `apps/notification-worker/src/`
- **Queue**: Bull queue integration

## 14. Certificate Generation Flow

### Flow Diagram

```
Service → Queue Job → Cert Generator → Puppeteer → PDF → MinIO → URL Return
```

### Step-by-Step

1. **Service requests certificate**
   - Determine certificate type
   - Fetch student/staff data
   - Load certificate template
   - Add job to queue

2. **Queue processing**
   - Bull queue stores job in Redis
   - Cert generator polls queue
   - Worker processes job

3. **PDF generation**
   - Load Handlebars template
   - Bind data to template
   - Render HTML
   - Use Puppeteer to convert to PDF
   - Add watermark/signature if configured

4. **Storage**
   - Upload PDF to MinIO
   - Get presigned URL
   - Return URL to service

5. **Completion**
   - Update IssuedDocument record
   - Send notification to user
   - Mark job as complete

### Key Files

- **Certificate Generator**: `apps/cert-generator/src/`
- **Documents Module**: `apps/core-api/src/modules/documents/`
- **Queue**: Bull queue integration

## 15. Audit Logging Flow

### Flow Diagram

```
Service → Prisma Operation → Middleware → Audit Log → Database
```

### Step-by-Step

1. **Service performs database operation**
   - Create, update, or delete
   - Via Prisma client

2. **Prisma middleware intercepts**
   - AuditMiddleware.$use() intercepts
   - Check model in denylist
   - If in denylist: Skip audit

3. **Audit processing**
   - Extract action type (create/update/delete)
   - Extract actor from request context
   - Extract before/after state
   - Compute field changes (diff)
   - Redact sensitive fields
   - Ignore noise fields

4. **Audit log creation**
   - Create AuditLog record
   - Set actorId, actorRole
   - Set actionType, module, entityType
   - Set oldValue, newValue (JSON)
   - Set timestamp

5. **Best-effort**
   - If audit logging fails: Continue operation
   - Don't block primary operation
   - Log error separately

### Key Files

- **Audit Middleware**: `apps/core-api/src/database/audit-middleware.ts`
- **Request Context**: `apps/core-api/src/common/context/request-context.ts`

## Summary

These flows represent the major feature execution paths in the University ERP system. Each flow involves multiple components working together:

- **Frontend**: React components for user interaction
- **API**: NestJS controllers and services
- **Database**: PostgreSQL via Prisma
- **Infrastructure**: Redis, MinIO, Elasticsearch
- **Background Workers**: Bull queues for async processing
- **External Services**: Email, SMS, payment gateways

The system is designed with:
- **Separation of concerns**: Each layer has distinct responsibilities
- **Async processing**: Background jobs for heavy operations
- **Audit trail**: All writes are logged
- **Error handling**: Graceful degradation
- **Scalability**: Queue-based processing for horizontal scaling
