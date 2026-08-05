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



---


# Business Processes - Complete Workflow Documentation

## Table of Contents
1. [User Registration and Authentication](#user-registration-and-authentication)
2. [Student Admission Process](#student-admission-process)
3. [Academic Enrollment Process](#academic-enrollment-process)
4. [Fee Management Process](#fee-management-process)
5. [Examination Process](#examination-process)
6. [Hostel Allocation Process](#hostel-allocation-process)
7. [Leave Application Process](#leave-application-process)
8. [Document Generation Process](#document-generation-process)
9. [Library Circulation Process](#library-circulation-process)
10. [Timetable Scheduling Process](#timetable-scheduling-process)
11. [Counselling Process](#counselling-process)
12. [Resource Reservation Process](#resource-reservation-process)

---

## User Registration and Authentication

### Purpose
Allow new users (students, staff, applicants) to register for the system and authenticate securely.

### Who Uses It
- **Applicants**: New students applying for admission
- **Staff**: New faculty and staff members
- **Admin**: User creation and management

### Process Flow

#### Step 1: Registration Initiation
**User Action**: User navigates to registration page
**Screen**: RegisterPage.tsx
**Data Entered**:
- Email address
- Password (with complexity validation)
- Personal information (name, phone, date of birth)
- Role selection (student/staff)
- Institute/department selection

**Frontend Processing**:
- Validates email format and password complexity
- Checks for existing email
- Collects personal details
- Sends registration request to backend

**Backend Processing** (AuthService.register):
- Validates input data
- Hashes password using bcrypt
- Creates User record with `isActive: false`
- Creates RegistrationRequest record
- Triggers OTP verification based on university config

**Database Changes**:
- INSERT into `users` table
- INSERT into `registration_requests` table

**Status Change**: User created but inactive, awaiting verification

#### Step 2: OTP Verification
**User Action**: User enters OTP received via email/SMS
**Screen**: RegisterPage.tsx (OTP step)
**Data Entered**: 6-digit OTP

**Frontend Processing**:
- Validates OTP format
- Sends verification request

**Backend Processing** (AuthService.verifyOtp):
- Validates OTP against stored value
- Checks OTP expiration
- On success: activates user account
- On failure: returns error with remaining attempts

**Database Changes**:
- UPDATE `users` set `isActive: true`
- UPDATE `registration_requests` set status

**Status Change**: User account activated

#### Step 3: Account Setup
**User Action**: User logs in for first time
**Screen**: SetupAccountPage.tsx
**Data Entered**: New password (if forced change)

**Frontend Processing**:
- Enforces password change if `mustChangePassword: true`
- Validates new password against policy

**Backend Processing** (AuthService.setupAccount):
- Validates password composition
- Checks password history (no reuse of last N)
- Updates password hash
- Clears `mustChangePassword` flag
- Records password change timestamp

**Database Changes**:
- UPDATE `users` password fields
- INSERT into `password_history`

**Status Change**: User fully activated and can access system

#### Step 4: Login
**User Action**: User enters credentials
**Screen**: LoginPage.tsx
**Data Entered**: Email and password

**Frontend Processing**:
- Validates input format
- Sends login request

**Backend Processing** (AuthService.login):
- Validates credentials
- Checks account lockout status
- Verifies password
- Generates JWT access token (15 min expiry)
- Generates refresh token (7 day expiry)
- Records last login timestamp
- Resets failed login count

**Database Changes**:
- UPDATE `users` last_login_at
- INSERT into `refresh_tokens`

**Status Change**: User authenticated with valid tokens

**Next User Involved**: User proceeds to dashboard based on role

---

## Student Admission Process

### Purpose
Manage the complete admission workflow from application to enrollment.

### Who Uses It
- **Applicants**: Submit admission applications
- **Admission Coordinators**: Review and process applications
- **Approvers**: Approve or reject applications
- **Finance Officers**: Verify fee payments
- **Admin**: Manage seat allocation and merit lists

### Process Flow

#### Step 1: Application Form Submission
**User Action**: Applicant fills admission form
**Screen**: StudentApplicationsPage.tsx or public form
**Data Entered**:
- Personal details (name, address, contact)
- Academic history (previous qualifications)
- Program and course preferences
- Document uploads (marksheets, ID proofs)
- Photo upload

**Frontend Processing**:
- Multi-step form with validation
- File upload with size limits
- Draft saving capability
- Razorpay payment integration for application fee

**Backend Processing** (FormsService.submit):
- Validates form data
- Processes file uploads to MinIO
- Creates FormSubmission record
- Triggers workflow instance if configured
- Generates application number

**Database Changes**:
- INSERT into `form_submissions`
- INSERT into `workflow_instances` (if workflow configured)
- INSERT into `fee_demands` (application fee)

**Status Change**: Application submitted, pending review

#### Step 2: Application Fee Payment
**User Action**: Applicant pays application fee
**Screen**: Payment gateway (Razorpay)
**Data Entered**: Payment details

**Frontend Processing**:
- Redirects to Razorpay
- Handles payment success/failure

**Backend Processing** (WorkflowPaymentService):
- Creates payment gate in workflow
- Processes Razorpay callback
- Records payment in FeeLedger
- Advances workflow to next state

**Database Changes**:
- INSERT into `payments`
- UPDATE `fee_demands` status
- UPDATE `workflow_instances` state

**Status Change**: Payment verified, awaiting coordinator review

#### Step 3: Coordinator Review
**User Action**: Admission coordinator reviews application
**Screen**: AdmissionsPage.tsx
**Data Entered**: Review comments, decision (approve/reject/send back)

**Frontend Processing**:
- Displays application details
- Shows document uploads
- Provides review interface

**Backend Processing** (AdmissionsService.review):
- Validates coordinator permissions
- Updates application status
- Triggers notification to applicant
- If approved: routes to approver
- If rejected: closes workflow
- If sent back: returns to applicant for corrections

**Database Changes**:
- UPDATE `form_submissions` status
- UPDATE `workflow_instances` state
- INSERT into `workflow_tasks` (for approver)

**Status Change**: Pending approver decision

#### Step 4: Approver Decision
**User Action**: Designated approver reviews and decides
**Screen**: MyTasksPage.tsx
**Data Entered**: Approval decision, comments

**Frontend Processing**:
- Shows task in inbox
- Displays application details
- Provides approve/reject buttons

**Backend Processing** (WorkflowEngineService.completeTask):
- Validates approver permissions
- Executes workflow transition
- Triggers notifications
- If approved: triggers seat allocation
- If rejected: notifies applicant

**Database Changes**:
- UPDATE `workflow_instances` state
- UPDATE `workflow_tasks` status
- INSERT into `workflow_instance_events`

**Status Change**: Approved, pending seat allocation

#### Step 5: Seat Allocation
**User Action**: System or admin allocates seat
**Screen**: AdmissionsPage.tsx (Seat Master)
**Data Entered**: Batch and section assignment

**Frontend Processing**:
- Shows available seats by program
- Displays seat utilization
- Allows manual allocation

**Backend Processing** (AdmissionsService.allocateSeat):
- Checks seat availability in batch
- Updates ProgramSeatApproval
- Creates Student record
- Links Student to User
- Assigns section
- Triggers enrollment workflow

**Database Changes**:
- INSERT into `students`
- UPDATE `program_seat_approvals`
- INSERT into `student_subject_enrollment` (auto-enroll based on batch)

**Status Change**: Seat allocated, student enrolled

#### Step 6: Fee Payment and Finalization
**User Action**: Student pays admission fee
**Screen**: FeesPage.tsx
**Data Entered**: Payment details

**Frontend Processing**:
- Shows fee breakdown
- Integrates with Razorpay
- Displays payment history

**Backend Processing** (FeeService.recordPayment):
- Processes payment
- Updates FeeLedger
- Generates receipt
- Triggers document generation (ID card)

**Database Changes**:
- INSERT into `payments`
- UPDATE `fee_ledger`
- INSERT into `fee_receipts`

**Status Change**: Admission complete, student active

**Final Outcome**: Student can now access academic services, timetable, attendance, etc.

---

## Academic Enrollment Process

### Purpose
Manage student subject enrollment and elective selection.

### Who Uses It
- **Students**: View and select subjects
- **Academic Admin**: Configure enrollment rules
- **HOD**: Approve elective selections

### Process Flow

#### Step 1: Auto-Enrollment Configuration
**User Action**: Admin configures batch enrollment rules
**Screen**: MasterDataPage.tsx (Batch configuration)
**Data Entered**:
- Batch-term subjects
- Enrollment type (auto/manual)
- Elective pools

**Frontend Processing**:
- Shows batch structure
- Allows subject configuration
- Validates subject prerequisites

**Backend Processing** (MasterDataService.configureBatch):
- Creates BatchTerm records
- Creates BatchTermSubject records
- Links subjects to streams
- Sets enrollment flags

**Database Changes**:
- INSERT into `batch_terms`
- INSERT into `batch_term_subjects`

**Status Change**: Enrollment rules configured

#### Step 2: Auto-Enrollment Execution
**User Action**: System auto-enrolls students (scheduled or manual)
**Screen**: AcademicModule controller
**Data Entered**: None (automated)

**Backend Processing** (EnrollmentService.autoEnroll):
- Queries students in batch
- For each student:
  - Identifies mandatory subjects
  - Creates StudentSubjectEnrollment records
  - Applies stream-based rules
- Triggers notifications

**Database Changes**:
- INSERT into `student_subject_enrollment` (bulk)

**Status Change**: Students enrolled in mandatory subjects

#### Step 3: Subject Election (Electives)
**User Action**: Student selects elective subjects
**Screen**: ElectivesPage.tsx
**Data Entered**:
- Selected subjects from pools
- Preferences (if applicable)

**Frontend Processing**:
- Shows available elective pools
- Displays subject details
- Validates credit limits
- Shows selection conflicts

**Backend Processing** (AcademicService.submitElection):
- Validates election window (open/closed)
- Checks seat availability in electives
- Validates prerequisites
- Creates StudentTermElection records
- Applies selection algorithm (if over-subscribed)

**Database Changes**:
- INSERT into `student_term_elections`
- UPDATE `student_subject_enrollment` (for elected subjects)

**Status Change**: Elective selection submitted

#### Step 4: Election Approval (if required)
**User Action**: HOD approves elective selections
**Screen**: ValidationPage.tsx
**Data Entered**: Approval/rejection decisions

**Backend Processing** (AcademicService.approveElection):
- Reviews election requests
- Approves or rejects selections
- Notifies students
- Finalizes enrollments

**Database Changes**:
- UPDATE `student_term_elections` status

**Status Change**: Elective enrollment finalized

**Final Outcome**: Students have complete subject enrollment for the term

---

## Fee Management Process

### Purpose
Manage fee structures, demands, payments, and refunds.

### Who Uses It
- **Students**: View and pay fees
- **Finance Officers**: Manage fee structures and payments
- **Admin**: Configure fee heads and recurring billing

### Process Flow

#### Step 1: Fee Structure Configuration
**User Action**: Admin configures fee structure
**Screen**: ProgramFeeManager.tsx
**Data Entered**:
- Fee components (tuition, lab, library, etc.)
- Amounts per term/year
- Applicable batches
- Concession rules

**Frontend Processing**:
- Shows program hierarchy
- Allows component configuration
- Validates amounts

**Backend Processing** (FeeService.createStructure):
- Creates FeeStructure records
- Links to programmes/batches
- Creates FeeHead components
- Sets effective dates

**Database Changes**:
- INSERT into `fee_structures`
- INSERT into `fee_heads`

**Status Change**: Fee structure configured

#### Step 2: Recurring Billing (Automated)
**User Action**: System runs daily at 2 AM
**Screen**: Scheduled job (RecurringBillingService)
**Data Entered**: None (automated)

**Backend Processing** (RecurringBillingService.run):
- For each university with billing enabled:
  - Identifies active students
  - For each student:
    - Calculates fee based on structure
    - Applies concessions (StudentConcession)
    - Creates FeeDemand records
    - Sets due dates
    - Uses sourceRef to prevent duplicates

**Database Changes**:
- INSERT into `fee_demands` (bulk, idempotent)

**Status Change**: Fee demands generated for term

#### Step 3: Student Views Fees
**User Action**: Student views fee dashboard
**Screen**: FeesPage.tsx
**Data Entered**: None (view only)

**Frontend Processing**:
- Shows fee breakdown
- Displays payment history
- Shows due dates and late fees
- Integrates with Razorpay for payment

**Backend Processing** (FeeService.getStudentFees):
- Queries FeeDemand by student
- Applies concessions
- Calculates outstanding
- Retrieves payment history

**Database Changes**: None (read operation)

**Status Change**: Student sees fee obligations

#### Step 4: Payment Processing
**User Action**: Student pays fee
**Screen**: Razorpay payment gateway
**Data Entered**: Payment details

**Frontend Processing**:
- Redirects to Razorpay
- Handles success/failure callbacks

**Backend Processing** (FeeService.processPayment):
- Validates payment amount
- Records payment in FeeLedger
- Updates FeeDemand status
- Generates receipt
- Triggers notifications

**Database Changes**:
- INSERT into `payments`
- UPDATE `fee_ledger`
- UPDATE `fee_demands`

**Status Change**: Fee paid, receipt generated

#### Step 5: Concession Application
**User Action**: Student applies for fee concession
**Screen**: FormsPage.tsx (concession form)
**Data Entered**:
- Concession type
- Supporting documents
- Reason

**Backend Processing** (WorkflowEngineService.startInstance):
- Creates workflow instance
- Routes to approver
- Holds on decision

**Database Changes**:
- INSERT into `workflow_instances`
- INSERT into `form_submissions`

**Status Change**: Concession request pending approval

#### Step 6: Concession Approval
**User Action**: Approver reviews concession
**Screen**: MyTasksPage.tsx
**Data Entered**: Approval decision, concession percentage

**Backend Processing** (WorkflowEngineService.completeTask):
- Approves concession
- Creates StudentConcession record
- Recalculates fee demands
- Applies to future billing

**Database Changes**:
- INSERT into `student_concessions`
- UPDATE `fee_demands` (recalculated)

**Status Change**: Concession applied, fees reduced

#### Step 7: Refund Processing
**User Action**: Student requests deposit refund
**Screen**: FeesPage.tsx (refund request)
**Data Entered**:
- Bank account details
- Refund amount
- Reason

**Backend Processing** (FeeService.initiateRefund):
- Creates ProgramDepositRefundRequest or HostelRefundRequest
- Triggers workflow approval
- Validates eligibility

**Database Changes**:
- INSERT into `program_deposit_refund_request` or `hostel_refund_request`
- INSERT into `workflow_instances`

**Status Change**: Refund request pending approval

#### Step 8: Refund Approval and Processing
**User Action**: Finance officer approves and processes refund
**Screen**: MyTasksPage.tsx
**Data Entered**: Approval decision, transaction details

**Backend Processing** (WorkflowEngineService.completeTask):
- Approves refund
- Updates refund request status
- Processes bank transfer
- Records in FeeLedger

**Database Changes**:
- UPDATE refund request status
- INSERT into `payments` (refund)
- UPDATE `fee_ledger`

**Status Change**: Refund processed

**Final Outcome**: Fee account settled, student financial obligations cleared

---

## Examination Process

### Purpose
Manage examination creation, scheduling, execution, and results.

### Who Uses It
- **Exam Controllers**: Create exams and papers
- **Faculty**: Set question papers and invigilate
- **Students**: Take exams and view results
- **Admin**: Schedule exams and manage logistics

### Process Flow

#### Step 1: Question Bank Management
**User Action**: Faculty adds questions to bank
**Screen**: ExaminationsPage.tsx (Question Bank tab)
**Data Entered**:
- Question text
- Question type (MCQ, descriptive, etc.)
- Difficulty level
- Subject association
- Answer key

**Frontend Processing**:
- Rich text editor for questions
- Math formula support (KaTeX)
- Bulk import from Excel

**Backend Processing** (QuestionBankService.addQuestion):
- Validates question format
- Stores in Question table
- Tags with subject and difficulty
- Supports bulk import

**Database Changes**:
- INSERT into `questions`

**Status Change**: Question added to bank

#### Step 2: Exam Paper Creation
**User Action**: Exam controller creates exam paper
**Screen**: ExaminationsPage.tsx (Paper Creation)
**Data Entered**:
- Paper name and code
- Subject and batch
- Exam duration
- Question selection from bank
- Marking scheme

**Frontend Processing**:
- Question picker from bank
- Mark allocation interface
- Paper preview

**Backend Processing** (ExaminationService.createPaper):
- Creates ExamPaper record
- Links questions (ExamPaperQuestion)
- Sets exam configuration
- Generates paper code

**Database Changes**:
- INSERT into `exam_papers`
- INSERT into `exam_paper_questions`

**Status Change**: Exam paper created

#### Step 3: Exam Scheduling
**User Action**: Admin schedules exam
**Screen**: ExaminationsPage.tsx (Scheduling)
**Data Entered**:
- Exam date and time
- Venue/room allocation
- Invigilator assignment
- Student eligibility

**Backend Processing** (ExamSchedulerService.schedule):
- Creates ExamSchedule record
- Assigns invigilators (ExamInvigilator)
- Generates hall tickets
- Checks resource conflicts
- Sends notifications

**Database Changes**:
- INSERT into `exam_schedules`
- INSERT into `exam_invigilators`

**Status Change**: Exam scheduled, hall tickets generated

#### Step 4: Student Exam Execution (CBE)
**User Action**: Student takes online exam
**Screen**: ExamTakePage.tsx
**Data Entered**:
- Answers to questions
- Navigation through questions

**Frontend Processing**:
- Full-screen mode enforcement
- Camera/mic access for proctoring
- Periodic snapshots
- Tab switch detection
- Auto-save answers

**Backend Processing** (ExaminationService.startExam):
- Creates ExamAttempt record
- Validates eligibility
- Tracks device fingerprint
- Monitors integrity events

**Frontend Processing** (during exam):
- Sends answers periodically
- Uploads snapshots
- Reports proctoring events

**Backend Processing** (ExaminationService.recordEvent):
- Records ExamProctorEvent (tab switch, etc.)
- Stores ExamSnapshot (webcam images)
- Saves ExamResponse (answers)

**Database Changes**:
- INSERT into `exam_attempts`
- INSERT into `exam_proctor_events`
- INSERT into `exam_snapshots`
- INSERT into `exam_responses`

**Status Change**: Exam in progress

#### Step 5: Exam Submission
**User Action**: Student submits exam or auto-submit on timeout
**Screen**: ExamTakePage.tsx
**Data Entered**: Final confirmation

**Backend Processing** (ExaminationService.submitExam):
- Finalizes ExamAttempt
- Closes proctoring session
- Triggers auto-grading (for MCQs)
- Notifies invigilators

**Database Changes**:
- UPDATE `exam_attempts` status

**Status Change**: Exam submitted, pending grading

#### Step 6: Grading and Evaluation
**User Action**: Faculty grades descriptive answers
**Screen**: ExaminationsPage.tsx (Grading)
**Data Entered**:
- Marks for each answer
- Feedback comments

**Backend Processing** (ExaminationService.gradePaper):
- Retrieves student responses
- Allows mark entry
- Calculates total
- Applies grading rules
- Updates StudentMarks

**Database Changes**:
- INSERT into `student_marks`
- UPDATE `exam_attempts` status

**Status Change**: Exam graded

#### Step 7: Question Challenge
**User Action**: Student challenges a question
**Screen**: ExaminationsPage.tsx (Challenge tab)
**Data Entered**:
- Question reference
- Challenge reason
- Supporting argument

**Backend Processing** (ExaminationService.challengeQuestion):
- Creates QuestionChallenge record
- Routes to examiner
- Holds on review

**Database Changes**:
- INSERT into `question_challenges`

**Status Change**: Challenge pending review

#### Step 8: Challenge Resolution
**User Action**: Examiner reviews challenge
**Screen**: MyTasksPage.tsx
**Data Entered**: Decision (accept/reject), mark adjustment

**Backend Processing** (ExaminationService.resolveChallenge):
- Updates challenge status
- If accepted: adjusts marks for all students
- Recalculates results
- Notifies affected students

**Database Changes**:
- UPDATE `question_challenges`
- UPDATE `student_marks` (bulk)
- UPDATE `exam_attempts`

**Status Change**: Challenge resolved

#### Step 9: Result Processing
**User Action**: System computes term results
**Screen**: AcademicModule controller
**Data Entered**: None (automated)

**Backend Processing** (AcademicService.computeResult):
- For each student in batch:
  - Aggregates subject marks
  - Calculates SGPA using StreamLabel rules
  - Determines pass/fail
  - Creates StudentTermResult
- Updates StudentCumulativeResult (CGPA)

**Database Changes**:
- INSERT into `student_term_results`
- UPDATE `student_cumulative_results`

**Status Change**: Results computed

#### Step 10: Result Publication
**User Action**: Admin publishes results
**Screen**: ExaminationsPage.tsx (Results tab)
**Data Entered**: Publication decision

**Backend Processing** (AcademicService.publishResult):
- Updates result status to published
- Triggers notifications
- Makes visible to students
- Generates mark sheets

**Database Changes**:
- UPDATE `student_term_results` status

**Status Change**: Results published, students can view

**Final Outcome**: Students access results, apply for revaluation if needed

---

## Hostel Allocation Process

### Purpose
Manage hostel room allocation and fee management.

### Who Uses It
- **Students**: Apply for hostel accommodation
- **Wardens**: Manage allocations and complaints
- **Admin**: Configure hostel infrastructure

### Process Flow

#### Step 1: Hostel Configuration
**User Action**: Admin configures hostel infrastructure
**Screen**: HostelPage.tsx
**Data Entered**:
- Hostel details (name, capacity)
- Room details (number, capacity, amenities)
- Fee components (mess, security deposit)
- Warden assignment

**Frontend Processing**:
- Hostel hierarchy display
- Room configuration interface
- Fee component setup

**Backend Processing** (HostelService.configure):
- Creates Hostel records
- Creates HostelRoom records
- Creates HostelFeeComponent records
- Assigns warden

**Database Changes**:
- INSERT into `hostels`
- INSERT into `hostel_rooms`
- INSERT into `hostel_fee_components`

**Status Change**: Hostel infrastructure configured

#### Step 2: Student Hostel Application
**User Action**: Student applies for hostel
**Screen**: FormsPage.tsx (hostel request form)
**Data Entered**:
- Hostel preferences
- Room type preference
- Personal details
- Document uploads

**Backend Processing** (WorkflowEngineService.startInstance):
- Creates HostelRequest record
- Starts workflow instance
- Routes to warden for review
- Creates fee demand for security deposit

**Database Changes**:
- INSERT into `hostel_requests`
- INSERT into `workflow_instances`
- INSERT into `fee_demands` (security deposit)

**Status Change**: Hostel request submitted, pending warden review

#### Step 3: Warden Review and Allocation
**User Action**: Warden reviews and allocates room
**Screen**: MyTasksPage.tsx
**Data Entered**:
- Allocation decision
- Room assignment
- Allocation comments

**Backend Processing** (WorkflowEngineService.completeTask):
- Approves hostel request
- Creates HostelAllocation record
- Links student to room
- Updates room occupancy
- Triggers fee billing

**Database Changes**:
- INSERT into `hostel_allocations`
- UPDATE `hostel_rooms` (occupancy)
- UPDATE `hostel_requests` status

**Status Change**: Room allocated, student moves in

#### Step 4: Hostel Fee Billing
**User Action**: System bills hostel fees (recurring)
**Screen**: Scheduled job (RecurringBillingService)
**Data Entered**: None (automated)

**Backend Processing** (RecurringBillingService.run):
- For each allocated student:
  - Calculates mess fee (monthly)
  - Applies pro-rating if mid-term joining
  - Creates FeeDemand records
  - Links to HostelFeeComponent

**Database Changes**:
- INSERT into `fee_demands` (hostel fees)

**Status Change**: Hostel fees billed

#### Step 5: Security Deposit Refund
**User Action**: Student requests deposit refund on vacating
**Screen**: HostelPage.tsx (refund request)
**Data Entered**:
- Bank account details
- Vacating date
- Refund amount

**Backend Processing** (HostelService.requestRefund):
- Creates HostelRefundRequest record
- Triggers workflow approval
- Validates room condition
- Calculates deductions (if any)

**Database Changes**:
- INSERT into `hostel_refund_requests`
- INSERT into `workflow_instances`

**Status Change**: Refund request pending approval

#### Step 6: Refund Approval and Processing
**User Action**: Warden approves refund
**Screen**: MyTasksPage.tsx
**Data Entered**: Approval decision, deduction details

**Backend Processing** (WorkflowEngineService.completeTask):
- Approves refund
- Updates room vacancy
- Processes refund transaction
- Records in FeeLedger

**Database Changes**:
- UPDATE `hostel_allocations` (end date)
- UPDATE `hostel_rooms` (occupancy)
- INSERT into `payments` (refund)

**Status Change**: Refund processed, room vacated

**Final Outcome**: Hostel allocation cycle complete

---

## Leave Application Process

### Purpose
Manage staff leave applications and approvals.

### Who Uses It
- **Staff**: Apply for leave
- **HOD**: Approve leave requests
- **Academic Admin**: Reschedule classes if needed

### Process Flow

#### Step 1: Leave Type Configuration
**User Action**: Admin configures leave types
**Screen**: HRPage.tsx (Leave Types)
**Data Entered**:
- Leave type name
- Carry forward rules
- Max accumulation
- Documentation requirements

**Backend Processing** (HRService.createLeaveType):
- Creates LeaveType record
- Sets leave policies
- Links to staff roles

**Database Changes**:
- INSERT into `leave_types`

**Status Change**: Leave types configured

#### Step 2: Leave Balance Initialization
**User Action**: System initializes leave balances (annual)
**Screen**: Scheduled job
**Data Entered**: None (automated)

**Backend Processing** (HRService.initializeBalances):
- For each staff member:
  - Creates LeaveBalance record
  - Sets annual quota
  - Carries forward unused balance

**Database Changes**:
- INSERT into `leave_balances`

**Status Change**: Leave balances initialized

#### Step 3: Leave Application
**User Action**: Staff applies for leave
**Screen**: LeaveRequestsPage.tsx
**Data Entered**:
- Leave type
- Start and end dates
- Reason
- Supporting documents (if required)

**Frontend Processing**:
- Date picker for leave period
- Leave balance display
- Document upload

**Backend Processing** (HRService.applyLeave):
- Validates leave balance
- Checks for overlapping requests
- Creates LeaveApplication record
- For faculty: checks class schedule
- Triggers workflow approval

**Database Changes**:
- INSERT into `leave_applications`
- INSERT into `workflow_instances`

**Status Change**: Leave application submitted, pending approval

#### Step 4: Class Impact Check (Faculty Only)
**User Action**: System checks for scheduled classes
**Screen**: Automatic (后台处理)
**Data Entered**: None (automated)

**Backend Processing** (LeaveRescheduleService.checkImpact):
- Queries timetable for faculty
- Identifies affected classes
- Creates rescheduling tasks
- Notifies academic admin

**Database Changes**:
- Creates rescheduling tasks (in workflow data)

**Status Change**: Class impact identified, rescheduling needed

#### Step 5: HOD Approval
**User Action**: HOD reviews leave request
**Screen**: MyTasksPage.tsx
**Data Entered**: Approval decision, comments

**Backend Processing** (WorkflowEngineService.completeTask):
- Approves/rejects leave
- Updates LeaveApplication status
- Deducts from LeaveBalance
- Notifies staff

**Database Changes**:
- UPDATE `leave_applications` status
- UPDATE `leave_balances`

**Status Change**: Leave approved/rejected

#### Step 6: Class Rescheduling (if applicable)
**User Action**: Academic admin reschedules affected classes
**Screen**: TimetablePage.tsx
**Data Entered**:
- New date/time for affected classes
- Substitute faculty (if needed)

**Backend Processing** (TimetableService.rescheduleClass):
- Updates TimetableEntry
- Creates SpecialLecture if needed
- Notifies students

**Database Changes**:
- UPDATE `timetable_entries`
- INSERT into `special_lectures`

**Status Change**: Classes rescheduled

**Final Outcome**: Leave processed, classes rescheduled if needed

---

## Document Generation Process

### Purpose
Generate official documents (ID cards, mark sheets, certificates).

### Who Uses It
- **Students**: Request documents
- **Admin**: Configure templates and issue documents
- **Staff**: Verify and approve document requests

### Process Flow

#### Step 1: Document Template Configuration
**User Action**: Admin configures document templates
**Screen**: DocumentsPage.tsx (Template Designer)
**Data Entered**:
- Template name and type
- Layout design
- Field placeholders
- Signature configuration
- Logo and branding

**Frontend Processing**:
- Visual template designer
- Drag-and-drop fields
- Preview functionality

**Backend Processing** (DocumentsService.createTemplate):
- Creates DocumentTemplate record
- Stores layout configuration (JSON)
- Links to university/institute
- Sets approval requirements

**Database Changes**:
- INSERT into `document_templates`

**Status Change**: Document template configured

#### Step 2: Document Request
**User Action**: Student requests document
**Screen**: FormsPage.tsx (document request form)
**Data Entered**:
- Document type
- Purpose
- Required details
- Supporting documents

**Backend Processing** (WorkflowEngineService.startInstance):
- Creates document request workflow
- Routes to verifier
- Checks document fee (if applicable)

**Database Changes**:
- INSERT into `form_submissions`
- INSERT into `workflow_instances`
- INSERT into `fee_demands` (if fee applicable)

**Status Change**: Document request submitted, pending verification

#### Step 3: Document Fee Payment (if applicable)
**User Action**: Student pays document fee
**Screen**: Razorpay payment
**Data Entered**: Payment details

**Backend Processing** (WorkflowPaymentService):
- Processes payment
- Advances workflow
- Records in FeeLedger

**Database Changes**:
- INSERT into `payments`
- UPDATE `fee_demands`

**Status Change**: Fee paid, pending generation

#### Step 4: Document Generation
**User Action**: System generates document
**Screen**: DocumentsPage.tsx
**Data Entered**: None (automated after approval)

**Backend Processing** (DocumentsService.generate):
- Retrieves template
- Fetches student data
- Replaces placeholders
- Generates PDF
- Stores in MinIO
- Creates IssuedDocument record

**Database Changes**:
- INSERT into `issued_documents`

**Status Change**: Document generated

#### Step 5: Document Verification and Issuance
**User Action**: Admin verifies and issues document
**Screen**: DocumentsPage.tsx
**Data Entered**: Verification decision, digital signature

**Backend Processing** (DocumentsService.issue):
- Applies digital signature
- Updates IssuedDocument status
- Notifies student
- Enables download

**Database Changes**:
- UPDATE `issued_documents` status

**Status Change**: Document issued, available for download

**Final Outcome**: Student downloads official document

---

## Library Circulation Process

### Purpose
Manage library book circulation, reservations, and fines.

### Who Uses It
- **Students**: Borrow and reserve books
- **Librarian**: Manage circulation and catalog
- **Admin**: Configure library policies

### Process Flow

#### Step 1: Library Configuration
**User Action**: Admin configures library policies
**Screen**: LibraryPage.tsx (Settings)
**Data Entered**:
- Loan period (days)
- Fine per day
- Max books per student
- Reservation rules

**Backend Processing** (LibraryService.configure):
- Creates LibraryConfig record
- Sets circulation policies

**Database Changes**:
- INSERT into `library_config`

**Status Change**: Library policies configured

#### Step 2: Book Catalog Management
**User Action**: Librarian adds books to catalog
**Screen**: LibraryPage.tsx (Catalog)
**Data Entered**:
- Book details (ISBN, title, author)
- Category
- Number of copies
- Location

**Frontend Processing**:
- Book entry form
- Bulk import support
- Barcode generation

**Backend Processing** (LibraryService.addBook):
- Creates Book record
- Creates BookCopy records for each copy
- Generates barcodes
- Assigns location

**Database Changes**:
- INSERT into `books`
- INSERT into `book_copies`

**Status Change**: Books added to catalog

#### Step 3: Book Issue
**User Action**: Student borrows book
**Screen**: LibraryPage.tsx (Circulation)
**Data Entered**: Student ID, book barcode

**Backend Processing** (LibraryService.issueBook):
- Validates student eligibility
- Checks book availability
- Creates BookIssue record
- Sets due date
- Updates BookCopy status

**Database Changes**:
- INSERT into `book_issues`
- UPDATE `book_copies` status

**Status Change**: Book issued to student

#### Step 4: Book Return
**User Action**: Student returns book
**Screen**: LibraryPage.tsx (Circulation)
**Data Entered**: Book barcode

**Backend Processing** (LibraryService.returnBook):
- Calculates overdue days
- Computes fine (if any)
- Creates FeeDemand for fine
- Updates BookIssue record
- Updates BookCopy status

**Database Changes**:
- UPDATE `book_issues` (return date)
- UPDATE `book_copies` status
- INSERT into `fee_demands` (fine)

**Status Change**: Book returned, fine charged if overdue

#### Step 5: Fine Payment
**User Action**: Student pays library fine
**Screen**: FeesPage.tsx
**Data Entered**: Payment details

**Backend Processing** (FeeService.recordPayment):
- Processes payment
- Updates FeeLedger
- Clears fine demand

**Database Changes**:
- INSERT into `payments`
- UPDATE `fee_demands`

**Status Change**: Fine paid

#### Step 6: Book Reservation
**User Action**: Student reserves unavailable book
**Screen**: LibraryPage.tsx (Catalog)
**Data Entered**: Book ID, reservation period

**Backend Processing** (LibraryService.reserveBook):
- Creates BookReservation record
- Adds to queue
- Sets expiration (if configured)
- Notifies when available

**Database Changes**:
- INSERT into `book_reservations`

**Status Change**: Book reserved

#### Step 7: Reservation Fulfillment (Automated)
**User Action**: System processes reservations (daily midnight)
**Screen**: LibrarySchedulerService
**Data Entered**: None (automated)

**Backend Processing** (LibrarySchedulerService.cleanup):
- Checks returned books
- Matches with reservations
- Notifies next in queue
- Expires old reservations

**Database Changes**:
- UPDATE `book_reservations` status
- DELETE expired reservations

**Status Change**: Reservations processed

**Final Outcome**: Library circulation managed, fines collected

---

## Timetable Scheduling Process

### Purpose
Generate and manage institutional timetables.

### Who Uses It
- **Academic Admin**: Configure scheduling rules
- **Faculty**: View assigned classes
- **Students**: View class schedule

### Process Flow

#### Step 1: Scheduling Configuration
**User Action**: Admin configures scheduling parameters
**Screen**: TimetablePage.tsx (Configuration)
**Data Entered**:
- Working days and hours
- Time slot definitions
- Resource availability
- Staff load limits
- Elective pooling rules

**Backend Processing** (TimetableService.configure):
- Creates TimeSlot records
- Sets scheduling constraints
- Configures resources

**Database Changes**:
- INSERT into `time_slots`

**Status Change**: Scheduling configured

#### Step 2: Manual Resource Booking
**User Action**: Admin manually books resources
**Screen**: TimetablePage.tsx (Manual Booking)
**Data Entered**:
- Resource (room, lab)
- Date and time
- Associated subject/section
- Faculty

**Backend Processing** (ResourceReservationService.book):
- Validates resource availability
- Checks conflicts
- Creates ResourceReservation record
- Links to academic entities

**Database Changes**:
- INSERT into `resource_reservations`

**Status Change**: Resource booked manually

#### Step 3: Auto-Scheduler Execution
**User Action**: Admin runs auto-scheduler
**Screen**: TimetablePage.tsx (Auto-Schedule)
**Data Entered**:
- Batch/Section to schedule
- Scheduling options (clubbing, half-day clustering)

**Backend Processing** (SchedulerService.generateTimetable):
- Queries subjects to schedule
- Applies constraints:
  - Staff availability
  - Resource capacity
  - Elective pooling
  - No conflicts
- Generates TimetableEntry records
- Creates ScheduleRun record
- Handles clubbing (lecture + tutorial)

**Database Changes**:
- INSERT into `timetable_entries` (bulk)
- INSERT into `schedule_run`

**Status Change**: Timetable generated

#### Step 4: Timetable Review and Adjustment
**User Action**: Admin reviews generated timetable
**Screen**: TimetablePage.tsx (Review)
**Data Entered**: Manual adjustments if needed

**Frontend Processing**:
- Shows timetable grid
- Highlights conflicts
- Allows drag-and-drop adjustments

**Backend Processing** (TimetableService.adjust):
- Updates TimetableEntry records
- Re-validates constraints
- Handles conflicts

**Database Changes**:
- UPDATE `timetable_entries`

**Status Change**: Timetable finalized

#### Step 5: Special Lecture Scheduling
**User Action**: Admin schedules special/guest lecture
**Screen**: TimetablePage.tsx (Special Lectures)
**Data Entered**:
- Topic and speaker
- Date and time
- Venue
- Target audience

**Backend Processing** (TimetableService.scheduleSpecial):
- Creates SpecialLecture record
- Books resource
- Notifies target audience

**Database Changes**:
- INSERT into `special_lectures`
- INSERT into `resource_reservations`

**Status Change**: Special lecture scheduled

#### Step 6: Timetable Publication
**User Action**: Admin publishes timetable
**Screen**: TimetablePage.tsx
**Data Entered**: Publication decision

**Backend Processing** (TimetableService.publish):
- Updates timetable status
- Notifies students and faculty
- Makes visible in portals

**Database Changes**:
- UPDATE timetable status flags

**Status Change**: Timetable published, visible to all

**Final Outcome**: Timetable available to students and faculty

---

## Counselling Process

### Purpose
Manage admission counselling services and counsellor attribution.

### Who Uses It
- **Applicants**: Request counselling guidance
- **Counsellors**: Provide guidance and track enrollments
- **Admin**: Empanel counsellors and manage contracts

### Process Flow

#### Step 1: Counsellor Empanelment
**User Action**: Admin empanels counsellors
**Screen**: CounsellingAdminPage.tsx
**Data Entered**:
- Counsellor details
- Expertise areas
- Contract terms
- Compensation structure

**Backend Processing** (CounsellingService.empanel):
- Creates Counsellor record
- Creates CounsellorContract record
- Sets compensation rules
- Makes available for allocation

**Database Changes**:
- INSERT into `counsellors`
- INSERT into `counsellor_contracts`

**Status Change**: Counsellor empanelled

#### Step 2: Allocation Rule Configuration
**User Action**: Admin sets allocation rules
**Screen**: CounsellingAdminPage.tsx
**Data Entered**:
- Counsellor capacity
- Program/Stream assignment
- Auto-allocation rules

**Backend Processing** (CounsellingService.configureRules):
- Stores allocation rules in university config
- Links counsellors to programs

**Database Changes**:
- UPDATE `universities` config

**Status Change**: Allocation rules configured

#### Step 3: Counselling Request
**User Action**: Applicant requests counselling
**Screen**: CounsellingDeskPage.tsx
**Data Entered**:
- Preferred programs
- Questions/concerns
- Contact preferences

**Backend Processing** (CounsellingService.createRequest):
- Creates CounsellingRequest record
- Auto-assigns counsellor (based on rules)
- Notifies counsellor
- Creates initial comment

**Database Changes**:
- INSERT into `counselling_requests`
- INSERT into `counselling_comments`

**Status Change**: Counselling request created, counsellor assigned

#### Step 4: Counselling Session (Async Chat)
**User Action**: Counsellor and applicant exchange messages
**Screen**: CounsellingDeskPage.tsx
**Data Entered**:
- Messages
- Documents shared
- Recommendations

**Backend Processing** (CounsellingService.addComment):
- Creates CounsellingComment record
- Notifies other party
- Tracks conversation history

**Database Changes**:
- INSERT into `counselling_comments`

**Status Change**: Counselling conversation active

#### Step 5: Application Guidance
**User Action**: Counsellor guides applicant to apply
**Screen**: CounsellingDeskPage.tsx
**Data Entered**: Program recommendations, application tips

**Backend Processing** (CounsellingService.recommend):
- Counsellor provides guidance
- Links request to application (when submitted)

**Database Changes**:
- UPDATE `counselling_requests` with application link

**Status Change**: Guidance provided

#### Step 6: Enrollment Attribution
**User Action**: System attributes enrollment to counsellor
**Screen**: Automatic (when student enrolls)
**Data Entered**: None (automated)

**Backend Processing** (CounsellingService.attributeEnrollment):
- Links student enrollment to counselling request
- Creates CounsellorEnrollmentCredit record
- Triggers compensation calculation

**Database Changes**:
- INSERT into `counsellor_enrollment_credits`

**Status Change**: Enrollment attributed

#### Step 7: Rating and Feedback
**User Action**: Applicant rates counselling service
**Screen**: CounsellingDeskPage.tsx
**Data Entered**:
- Rating (1-5 stars)
- Feedback comments

**Backend Processing** (CounsellingService.rate):
- Stores rating on CounsellingRequest
- Updates counsellor performance metrics

**Database Changes**:
- UPDATE `counselling_requests` rating

**Status Change**: Counselling complete with feedback

#### Step 8: Compensation Processing
**User Action**: System calculates counsellor compensation
**Screen**: Scheduled job
**Data Entered**: None (automated)

**Backend Processing** (CounsellingService.calculateCompensation):
- Queries enrollment credits
- Applies contract compensation rules
- Generates payment reports
- Creates fee demands for payment

**Database Changes**:
- INSERT into `fee_demands` (counsellor payment)

**Status Change**: Compensation calculated, payable

**Final Outcome**: Counselling service delivered, compensation processed

---

## Resource Reservation Process

### Purpose
Manage generic resource booking (classrooms, labs, auditoriums).

### Who Uses It
- **Staff**: Request resources for events
- **Admin**: Approve requests and manage availability
- **System**: Auto-scheduler integration

### Process Flow

#### Step 1: Resource Type Configuration
**User Action**: Admin configures resource types
**Screen**: MasterDataPage.tsx (Resource Types)
**Data Entered**:
- Resource type name (classroom, lab, auditorium)
- Custom attributes (capacity, equipment)
- Booking rules

**Backend Processing** (MasterDataService.createResourceType):
- Creates InstituteResourceType record
- Sets custom attribute schema (JSON)
- Links to institute

**Database Changes**:
- INSERT into `institute_resource_types`

**Status Change**: Resource type configured

#### Step 2: Resource Creation
**User Action**: Admin adds individual resources
**Screen**: MasterDataPage.tsx (Resources)
**Data Entered**:
- Resource name and code
- Type assignment
- Capacity
- Location
- Equipment details

**Backend Processing** (MasterDataService.createResource):
- Creates InstituteResource record
- Links to resource type
- Sets custom attributes
- Configures scheduling rules

**Database Changes**:
- INSERT into `institute_resources`

**Status Change**: Resource added

#### Step 3: Resource Booking Request
**User Action**: Staff requests resource booking
**Screen**: FormsPage.tsx (resource request form)
**Data Entered**:
- Resource type/preferences
- Date and time
- Purpose
- Attendee count

**Backend Processing** (WorkflowEngineService.startInstance):
- Creates resource request workflow
- Checks availability (soft check)
- Routes to approver
- Creates WorkflowReservation (hold)

**Database Changes**:
- INSERT into `workflow_instances`
- INSERT into `workflow_reservations` (hold)

**Status Change**: Booking request submitted, pending approval

#### Step 4: Availability Check and Conflict Detection
**User Action**: System validates availability
**Screen**: Automatic (后台处理)
**Data Entered**: None (automated)

**Backend Processing** (ResourceReservationService.checkAvailability):
- Queries existing reservations
- Detects conflicts
- Calculates available capacity
- Returns alternatives if needed

**Database Changes**: None (read operation)

**Status Change**: Availability validated

#### Step 5: Approval and Confirmation
**User Action**: Approver reviews and approves
**Screen**: MyTasksPage.tsx
**Data Entered**: Approval decision, resource assignment

**Backend Processing** (WorkflowEngineService.completeTask):
- Approves request
- Converts WorkflowReservation hold to actual ResourceReservation
- Confirms booking
- Notifies requester

**Database Changes**:
- UPDATE `workflow_reservations` (confirm)
- INSERT into `resource_reservations`

**Status Change**: Resource booked and confirmed

#### Step 6: Booking Utilization
**User Action**: Staff uses resource
**Screen**: Physical event
**Data Entered**: None (real-world usage)

**Backend Processing**: None (physical event)

**Database Changes**: None

**Status Change**: Resource utilized

#### Step 7: Booking Release
**User Action**: Booking expires or is cancelled
**Screen**: WorkflowMonitorPage.tsx or automatic expiry
**Data Entered**: Cancellation or expiry

**Backend Processing** (ResourceReservationService.release):
- Releases ResourceReservation
- Makes resource available
- Notifies if cancellation

**Database Changes**:
- UPDATE `resource_reservations` status
- DELETE/UPDATE `workflow_reservations`

**Status Change**: Resource released, available for booking

**Final Outcome**: Resource booking cycle complete

---

## Summary

This UniversityERP system implements comprehensive business processes covering:

1. **User Management**: Registration, authentication, role assignment
2. **Academic Lifecycle**: Admission, enrollment, examination, results
3. **Financial Operations**: Fee structures, billing, payments, refunds
4. **Infrastructure**: Hostel, transport, library, resource management
5. **Human Resources**: Staff management, leave systems
6. **Workflow Automation**: Generic approval workflows for all processes
7. **Communication**: Notifications, notices, counselling
8. **Document Management**: Template-based document generation

All processes are:
- **Workflow-driven**: Most major processes use the workflow engine for approvals
- **Audit-tracked**: Every action is logged for accountability
- **Notification-enabled**: Stakeholders are notified at each step
- **Configurable**: Business rules can be configured per university/institute
- **Integrated**: Processes share data and trigger related operations

The system supports multi-tenancy (multiple universities with multiple institutes each) while maintaining data isolation and customized business rules per tenant.

---

**Document Version**: 1.0  
**Last Updated**: 2025-08-05


---


# User Journeys - Complete Role-Based Experiences

## Table of Contents
1. [SuperAdmin Journey](#superadmin-journey)
2. [University Admin Journey](#university-admin-journey)
3. [Institute Admin Journey](#institute-admin-journey)
4. [Student Journey](#student-journey)
5. [Teaching Faculty Journey](#teaching-faculty-journey)
6. [HOD Journey](#hod-journey)
7. [Librarian Journey](#librarian-journey)
8. [Accountant Journey](#accountant-journey)
9. [Warden Journey](#warden-journey)
10. [Applicant Journey](#applicant-journey)
11. [Parent Journey](#parent-journey)
12. [Counsellor Journey](#counsellor-journey)

---

## SuperAdmin Journey

### Who is SuperAdmin?
The SuperAdmin is the highest-level system administrator with complete access to all modules and university-level configuration. They are responsible for system setup, user management, and overall configuration.

### Typical Day in the Life

#### Morning: System Health and Configuration
**Login**: SuperAdmin logs in via LoginPage
- Enters email: erpsupport@slashcurate.com
- Enters password
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views system health indicators
- Checks recent user registrations
- Reviews pending approval tasks
- Monitors system metrics

**System Configuration**: SettingsPage.tsx
- Navigates to Settings
- Reviews university-level configurations
- Checks integration status (email, SMS, payment gateway)
- Verifies module access settings
- Reviews backup schedules

#### Mid-Day: User and Access Management
**User Management**: UserManagementPage.tsx
- Reviews new user registrations
- Approves/rejects registration requests
- Assigns roles to new users
- Reviews staff account creation requests
- Manages SuperAdmin accounts (create other super admins)

**Role Management**: SettingsPage.tsx (Roles tab)
- Reviews role definitions
- Creates new roles if needed
- Configures role permissions
- Manages role assignments

**Module Access**: SettingsPage.tsx (Module Access)
- Configures which roles can access which modules
- Enables/disables modules per institute
- Sets up navigation menu customization

#### Afternoon: Master Data and Setup
**University Management**: MasterDataPage.tsx
- Reviews university configuration
- Manages institute creation/editing
- Configures university departments
- Sets up university-wide academic catalog

**ID Format Configuration**: IdFormatsPage.tsx
- Configures enrollment number patterns
- Sets up receipt number formats
- Configures exam roll number patterns
- Tests format generation

**Backup Management**: SettingsPage.tsx (Backup)
- Reviews backup schedules
- Checks backup verification status
- Manually triggers backup if needed
- Reviews backup logs

#### Evening: Monitoring and Reports
**Audit Log Review**: AuditLogPage.tsx
- Reviews recent system activities
- Checks for suspicious activities
- Monitors user access patterns
- Reviews configuration changes

**Analytics Review**: AnalyticsPage.tsx
- Views system-wide analytics
- Reviews user adoption metrics
- Checks module usage statistics
- Reviews performance indicators

### Key Responsibilities

1. **System Setup**
   - Initial university configuration
   - Institute creation and setup
   - Role and permission configuration
   - Integration setup (email, SMS, payment)

2. **User Management**
   - SuperAdmin account management
   - University admin assignment
   - Role and permission management
   - User account issues resolution

3. **Configuration Management**
   - University-level settings
   - Module access control
   - Navigation customization
   - Branding configuration

4. **System Health**
   - Backup monitoring
   - Integration health checks
   - Performance monitoring
   - Security audits

### Screens Frequently Used
- DashboardPage.tsx
- SettingsPage.tsx
- UserManagementPage.tsx
- MasterDataPage.tsx
- AuditLogPage.tsx
- AnalyticsPage.tsx
- IdFormatsPage.tsx

### Decisions Made
- University-level policy configuration
- Role and permission assignments
- Module availability decisions
- Integration enablement decisions
- Backup strategy decisions

### Interactions with Other Users
- **University Admins**: Delegates day-to-day administration
- **Institute Admins**: Provides access and support
- **Technical Team**: Coordinates system changes
- **Users**: Resolves access issues

### Pain Points
- System-wide configuration changes require careful testing
- User access issues can be urgent
- Integration failures need immediate attention
- Backup failures require quick resolution

### Success Metrics
- System uptime and availability
- User satisfaction with access
- Integration reliability
- Backup success rate
- Configuration accuracy

---

## University Admin Journey

### Who is University Admin?
University Admin manages university-level operations including academic programs, university departments, and cross-institute coordination. They report to SuperAdmin and oversee Institute Admins.

### Typical Day in the Life

#### Morning: Academic Planning
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views university-wide metrics
- Checks pending approvals
- Reviews institute activities
- Monitors enrollment trends

**University Catalog Management**: MasterDataPage.tsx
- Manages university-level programs (Programme)
- Configures university streams
- Sets up university subjects
- Manages university departments

**Stream Label Configuration**: MasterDataPage.tsx
- Creates new stream labels
- Configures academic rules (grading, attendance)
- Sets fee schedules for streams
- Version control for rule changes

#### Mid-Day: Institute Coordination
**Institute Management**: MasterDataPage.tsx
- Reviews institute performance
- Manages institute creation/editing
- Configures institute-specific settings
- Coordinates cross-institute activities

**Department Management**: MasterDataPage.tsx
- Manages university departments
- Assigns HODs to departments
- Configures departmental permissions
- Reviews departmental performance

**Admission Oversight**: AdmissionsPage.tsx
- Reviews university-wide admission statistics
- Monitors seat allocation across institutes
- Reviews merit list generation
- Coordinates admission policies

#### Afternoon: Examination and Results
**Exam Configuration**: ExaminationsPage.tsx
- Sets university-wide exam policies
- Configures exam schedules
- Reviews question bank standards
- Monitors exam results

**Result Publishing**: ExaminationsPage.tsx
- Reviews term results before publication
- Approves university-wide result publication
- Monitors revaluation requests
- Reviews academic performance

**Fee Structure Oversight**: FeesPage.tsx
- Reviews fee structures across institutes
- Approves major fee changes
- Monitors fee collection trends
- Reviews scholarship programs

#### Evening: Reporting and Planning
**Analytics Review**: AnalyticsPage.tsx
- Views university-wide analytics
- Reviews enrollment trends
- Monitors academic performance
- Reviews financial metrics

**Workflow Monitoring**: WorkflowMonitorPage.tsx
- Reviews university-wide workflow instances
- Monitors approval bottlenecks
- Reviews process completion rates
- Identifies process improvements

### Key Responsibilities

1. **Academic Governance**
   - University program catalog
   - Stream and subject definitions
   - Academic rule configuration
   - Grading and attendance policies

2. **Institute Coordination**
   - Institute performance monitoring
   - Cross-institute resource allocation
   - Standardization across institutes
   - Institute admin support

3. **Admission Management**
   - University-wide admission policies
   - Seat allocation coordination
   - Merit list oversight
   - Counseling program management

4. **Examination Oversight**
   - University exam policies
   - Result publication approval
   - Revaluation process oversight
   - Academic performance monitoring

### Screens Frequently Used
- DashboardPage.tsx
- MasterDataPage.tsx
- AdmissionsPage.tsx
- ExaminationsPage.tsx
- FeesPage.tsx
- AnalyticsPage.tsx
- WorkflowMonitorPage.tsx

### Decisions Made
- Academic program creation/modification
- Stream rule configuration
- Institute-level policy decisions
- Admission policy decisions
- Examination policy decisions

### Interactions with Other Users
- **SuperAdmin**: Receives delegated authority
- **Institute Admins**: Provides guidance and oversight
- **HODs**: Coordinates academic activities
- **Exam Controllers**: Manages examination processes

### Pain Points
- Coordinating across multiple institutes
- Standardizing policies while allowing flexibility
- Managing cross-institute resource conflicts
- Ensuring data consistency across institutes

### Success Metrics
- Enrollment targets achievement
- Academic performance standards
- Institute satisfaction levels
- Process efficiency
- Policy compliance

---

## Institute Admin Journey

### Who is Institute Admin?
Institute Admin manages day-to-day operations of a specific institute/college. They handle local master data, staff management, student services, and institute-level configuration.

### Typical Day in the Life

#### Morning: Daily Operations
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views institute-specific metrics
- Checks pending tasks and approvals
- Reviews today's schedule
- Monitors staff and student activity

**Notice Board Management**: NoticeBoardPage.tsx
- Posts institute announcements
- Reviews notice expiry
- Manages notice categories
- Pins important notices

**Staff Attendance Review**: AttendancePage.tsx
- Reviews staff attendance for today
- Identifies absent staff
- Approves leave requests
- Addresses attendance issues

#### Mid-Day: Academic Management
**Course and Batch Management**: MasterDataPage.tsx
- Manages institute-specific courses
- Creates and configures batches
- Manages sections within batches
- Configures batch-term structure

**Subject Management**: MasterDataPage.tsx
- Configures subjects for courses
- Sets up subject pools for electives
- Manages subject labels
- Configures prerequisite rules

**Staff-Subject Assignment**: MasterDataPage.tsx
- Assigns subjects to faculty
- Manages teaching loads
- Reviews subject allocation
- Adjusts assignments as needed

**Timetable Management**: TimetablePage.tsx
- Reviews current timetable
- Handles timetable adjustments
- Schedules special lectures
- Manages resource bookings

#### Afternoon: Student Services
**Student Onboarding**: OnboardStudentsPage.tsx
- Reviews new student registrations
- Manages student profile creation
- Assigns students to batches/sections
- Coordinates enrollment process

**Fee Management**: FeesPage.tsx
- Reviews fee collection status
- Approves fee concessions
- Manages refund requests
- Addresses fee payment issues

**Hostel Management**: HostelPage.tsx
- Reviews hostel occupancy
- Manages room allocations
- Addresses hostel complaints
- Manages hostel fee billing

**Transport Management**: TransportPage.tsx
- Reviews transport utilization
- Manages route assignments
- Issues transport passes
- Addresses transport issues

#### Evening: Approvals and Monitoring
**My Tasks**: MyTasksPage.tsx
- Reviews pending approval tasks
- Approves/rejects requests
- Delegates tasks if needed
- Follows up on overdue tasks

**Workflow Monitoring**: WorkflowMonitorPage.tsx
- Reviews institute workflow instances
- Identifies bottlenecks
- Monitors process completion
- Generates workflow reports

**User Management**: UserManagementPage.tsx
- Reviews new staff account requests
- Manages role assignments
- Addresses user access issues
- Manages staff profile updates

### Key Responsibilities

1. **Institute Operations**
   - Daily operational oversight
   - Staff management and coordination
   - Student services delivery
   - Infrastructure management

2. **Academic Administration**
   - Course and batch management
   - Subject and faculty assignment
   - Timetable management
   - Academic scheduling

3. **Student Services**
   - Student onboarding
   - Fee management
   - Hostel and transport services
   - Document issuance

4. **Approvals and Workflows**
   - Request approvals
   - Workflow monitoring
   - Process optimization
   - Staff support

### Screens Frequently Used
- DashboardPage.tsx
- MasterDataPage.tsx
- TimetablePage.tsx
- FeesPage.tsx
- HostelPage.tsx
- TransportPage.tsx
- MyTasksPage.tsx
- UserManagementPage.tsx
- NoticeBoardPage.tsx

### Decisions Made
- Course and batch creation
- Staff-subject assignments
- Timetable adjustments
- Fee concession approvals
- Hostel allocation decisions
- Resource booking approvals

### Interactions with Other Users
- **University Admin**: Receives guidance and reports
- **HODs**: Coordinates academic activities
- **Staff**: Provides support and oversight
- **Students**: Addresses issues and requests

### Pain Points
- Managing daily operational issues
- Coordinating with multiple departments
- Handling urgent student requests
- Balancing administrative and academic priorities

### Success Metrics
- Operational efficiency
- Staff and student satisfaction
- Process completion rates
- Issue resolution time
- Service delivery quality

---

## Student Journey

### Who is Student?
Student is the primary user of the system for academic activities, from enrollment to graduation. They access the system for academics, fees, examinations, and various services.

### Typical Day in the Life

#### Morning: Academic Dashboard
**Login**: LoginPage.tsx
- Enters student email and password
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views today's class schedule
- Checks upcoming deadlines
- Views attendance summary
- Reviews pending fee payments
- Checks notice board updates

**Timetable View**: TimetablePage.tsx
- Reviews today's classes
- Checks room locations
- Views faculty assignments
- Notes any schedule changes

#### Mid-Day: Academic Activities
**Attendance Check**: AttendancePage.tsx
- Views attendance record
- Checks attendance percentage
- Identifies any deficit areas
- Views attendance defaulter warnings

**Subject Enrollment**: ElectivesPage.tsx (if applicable)
- Views available elective subjects
- Selects preferred electives
- Submits election form
- Views enrollment status

**Library Access**: LibraryPage.tsx
- Searches for books
- Views borrowed books
- Checks due dates
- Reserves unavailable books
- Pays library fines if any

#### Afternoon: Services and Requests
**Fee Payment**: FeesPage.tsx
- Views pending fee demands
- Reviews fee breakdown
- Pays fees via Razorpay
- Downloads payment receipts
- Views payment history

**Document Requests**: FormsPage.tsx
- Requests documents (bonafide, ID card)
- Fills document request form
- Pays document fee if applicable
- Tracks request status
- Downloads issued documents

**Leave Application**: LeaveRequestsPage.tsx (if applicable - for research scholars/assignments)
- Applies for leave
- Views leave balance
- Tracks application status
- Views leave history

**Hostel Services**: HostelPage.tsx (if residing)
- Views hostel allocation details
- Pays hostel fees
- Submits complaints/requests
- Requests hostel services

#### Evening: Examinations and Results
**Exam Preparation**: ExaminationsPage.tsx
- Views exam schedule
- Downloads hall tickets
- Accesses previous year papers
- Takes practice tests if available

**Online Exam**: ExamTakePage.tsx (for CBE)
- Enters exam interface
- Takes proctored exam
- Submits answers
- Views submission confirmation

**Results View**: StudentProfilePage.tsx
- Views term results
- Checks SGPA/CGPA
- Downloads mark sheets
- Applies for revaluation if needed

**Profile Management**: StudentProfilePage.tsx
- Updates personal information
- Changes password
- Manages profile photo
- Updates contact details

### Key Responsibilities

1. **Academic Engagement**
   - Attend classes regularly
   - Maintain attendance requirements
   - Complete subject enrollment
   - Participate in examinations

2. **Financial Compliance**
   - Pay fees on time
   - Manage fee payments
   - Apply for concessions if eligible
   - Handle refund requests

3. **Service Utilization**
   - Use library services
   - Request documents
   - Access hostel/transport services
   - Utilize counselling services

4. **Profile Management**
   - Keep profile updated
   - Manage account security
   - Access academic records
   - Communicate with administration

### Screens Frequently Used
- DashboardPage.tsx
- TimetablePage.tsx
- AttendancePage.tsx
- FeesPage.tsx
- ExaminationsPage.tsx
- StudentProfilePage.tsx
- LibraryPage.tsx
- FormsPage.tsx
- ElectivesPage.tsx

### Decisions Made
- Subject/election selections
- Document requests
- Fee payment timing
- Leave applications
- Revaluation requests
- Service utilization choices

### Interactions with Other Users
- **Faculty**: Attend classes, seek guidance
- **HOD**: Academic issues, approvals
- **Admin**: Services, fees, documents
- **Librarian**: Library services
- **Counsellor**: Academic guidance

### Pain Points
- Fee payment deadlines
- Attendance requirements
- Document request delays
- Exam stress and technical issues
- Service request processing time

### Success Metrics
- Academic performance (SGPA/CGPA)
- Attendance compliance
- Fee payment timeliness
- Service satisfaction
- Profile completeness

---

## Teaching Faculty Journey

### Who is Teaching Faculty?
Teaching Faculty are academic staff responsible for teaching, assessment, and student guidance. They use the system for class management, attendance, examinations, and academic coordination.

### Typical Day in the Life

#### Morning: Class Preparation
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views today's class schedule
- Checks pending tasks
- Reviews student requests
- Views department notices

**Timetable Review**: TimetablePage.tsx
- Confirms today's class schedule
- Checks room assignments
- Views class timings
- Notes any special lectures

#### Mid-Day: Teaching Activities
**Attendance Marking**: AttendancePage.tsx
- Selects class for attendance
- Marks student attendance
- Adds attendance notes
- Submits attendance record
- Views attendance summary

**Class Management**: During class (physical)
- Uses system for class resources
- Accesses digital materials
- Records class notes if needed

**Student Interaction**: During/after class
- Addresses student queries
- Provides academic guidance
- Notes student issues
- Recommends counselling if needed

#### Afternoon: Assessment and Evaluation
**Exam Paper Creation**: ExaminationsPage.tsx
- Accesses question bank
- Creates exam papers
- Selects questions
- Sets marking scheme
- Reviews paper configuration

**Student Evaluation**: ExaminationsPage.tsx
- Grades student papers
- Enters marks
- Provides feedback
- Submits grades
- Reviews grade statistics

**Question Bank Contribution**: ExaminationsPage.tsx
- Adds new questions to bank
- Categorizes by difficulty
- Provides answer keys
- Reviews existing questions

#### Evening: Academic Coordination
**Subject Management**: MasterDataPage.tsx
- Reviews subject syllabus
- Updates subject materials
- Manages subject resources
- Coordinates with HOD

**Leave Application**: LeaveRequestsPage.tsx
- Applies for leave
- Views leave balance
- Checks class impact
- Submits leave request

**Invigilation Duty**: MyInvigilationPage.tsx
- Views assigned invigilation duties
- Checks exam schedules
- Reviews invigilation guidelines
- Reports invigilation issues

**My Tasks**: MyTasksPage.tsx
- Reviews pending approvals
- Approves student requests
- Provides recommendations
- Completes assigned tasks

### Key Responsibilities

1. **Teaching and Learning**
   - Conduct classes as per timetable
   - Mark student attendance
   - Provide academic guidance
   - Maintain teaching quality

2. **Assessment and Evaluation**
   - Create exam papers
   - Evaluate student performance
   - Provide timely feedback
   - Contribute to question bank

3. **Academic Coordination**
   - Coordinate with HOD
   - Participate in department activities
   - Contribute to curriculum development
   - Mentor students

4. **Professional Development**
   - Manage leave and duties
   - Participate in training
   - Contribute to research
   - Engage in academic activities

### Screens Frequently Used
- DashboardPage.tsx
- TimetablePage.tsx
- AttendancePage.tsx
- ExaminationsPage.tsx
- LeaveRequestsPage.tsx
- MyTasksPage.tsx
- MyInvigilationPage.tsx
- MasterDataPage.tsx

### Decisions Made
- Attendance marking
- Exam paper creation
- Student grading
- Leave applications
- Student recommendations
- Academic guidance

### Interactions with Other Users
- **Students**: Teaching, guidance, evaluation
- **HOD**: Academic coordination, reporting
- **Peers**: Subject coordination, sharing
- **Admin**: Services, requests
- **Exam Cell**: Exam coordination

### Pain Points
- Time management for multiple classes
- Balancing teaching and evaluation
- Managing student expectations
- Coordinating exam duties
- Keeping up with administrative tasks

### Success Metrics
- Student performance
- Attendance compliance
- Exam paper quality
- Student feedback
- Professional development

---

## HOD Journey

### Who is HOD?
Head of Department manages departmental academic operations, faculty coordination, and curriculum implementation. They bridge between institute administration and teaching faculty.

### Typical Day in the Life

#### Morning: Department Overview
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views departmental metrics
- Checks faculty attendance
- Reviews pending approvals
- Monitors departmental notices

**Faculty Coordination**: HRPage.tsx
- Reviews faculty attendance
- Addresses faculty issues
- Approves leave requests
- Manages faculty workload

#### Mid-Day: Academic Management
**Subject and Curriculum**: MasterDataPage.tsx
- Reviews subject offerings
- Coordinates curriculum implementation
- Manages subject allocations
- Reviews syllabus coverage

**Faculty-Subject Assignment**: MasterDataPage.tsx
- Assigns subjects to faculty
- Balances teaching loads
- Addresses allocation conflicts
- Reviews faculty expertise

**Attendance Monitoring**: AttendancePage.tsx
- Reviews departmental attendance
- Identifies defaulters
- Addresses attendance issues
- Monitors faculty compliance

**Timetable Coordination**: TimetablePage.tsx
- Reviews department timetable
- Addresses scheduling conflicts
- Approves special lectures
- Coordinates resource allocation

#### Afternoon: Student and Examination Management
**Student Academic Performance**: AnalyticsPage.tsx
- Reviews student performance
- Identifies at-risk students
- Coordinates remedial actions
- Monitors result trends

**Examination Coordination**: ExaminationsPage.tsx
- Reviews exam schedules
- Coordinates paper setting
- Monitors exam conduct
- Reviews result processing

**Elective Management**: ElectivesPage.tsx
- Approves elective offerings
- Reviews student elections
- Addresses capacity issues
- Finalizes elective allocations

#### Evening: Approvals and Reporting
**My Tasks**: MyTasksPage.tsx
- Reviews departmental approvals
- Approves student requests
- Addresses faculty requests
- Completes administrative tasks

**Workflow Monitoring**: WorkflowMonitorPage.tsx
- Reviews departmental workflows
- Monitors approval timelines
- Identifies bottlenecks
- Optimizes processes

**Department Reporting**: AnalyticsPage.tsx
- Generates departmental reports
- Reviews performance metrics
- Identifies improvement areas
- Plans academic initiatives

### Key Responsibilities

1. **Department Leadership**
   - Faculty management and coordination
   - Academic planning and implementation
   - Departmental administration
   - Resource allocation

2. **Academic Quality**
   - Curriculum implementation
   - Teaching quality monitoring
   - Student performance oversight
   - Academic standards maintenance

3. **Faculty Development**
   - Workload management
   - Professional development support
   - Performance evaluation
   - Mentoring and guidance

4. **Student Success**
   - Academic performance monitoring
   - Student support coordination
   - Remedial action planning
   - Career guidance facilitation

### Screens Frequently Used
- DashboardPage.tsx
- MasterDataPage.tsx
- TimetablePage.tsx
- AttendancePage.tsx
- ExaminationsPage.tsx
- HRPage.tsx
- AnalyticsPage.tsx
- MyTasksPage.tsx
- ElectivesPage.tsx

### Decisions Made
- Faculty-subject assignments
- Leave approvals
- Academic policy implementation
- Student academic interventions
- Resource allocation
- Curriculum adjustments

### Interactions with Other Users
- **Institute Admin**: Reporting and coordination
- **Faculty**: Management and support
- **Students**: Academic guidance
- **Other HODs**: Coordination and collaboration
- **University Admin**: Policy implementation

### Pain Points
- Balancing administrative and academic roles
- Managing faculty conflicts
- Addressing student performance issues
- Coordinating with multiple stakeholders
- Resource constraints

### Success Metrics
- Departmental academic performance
- Faculty satisfaction
- Student success rates
- Process efficiency
- Administrative compliance

---

## Librarian Journey

### Who is Librarian?
Librarian manages library operations including book circulation, catalog management, and reader services. They ensure smooth library operations and support academic needs.

### Typical Day in the Life

#### Morning: Library Operations
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views library statistics
- Checks today's due items
- Reviews pending reservations
- Monitors library notices

**Library Configuration**: LibraryPage.tsx (Settings)
- Reviews library policies
- Configures loan periods
- Sets fine rates
- Updates library rules

#### Mid-Day: Circulation Services
**Book Issue**: LibraryPage.tsx (Circulation)
- Processes book issue requests
- Validates student eligibility
- Updates book status
- Sets due dates
- Issues receipts

**Book Return**: LibraryPage.tsx (Circulation)
- Processes book returns
- Calculates overdue fines
- Updates book availability
- Creates fine demands
- Notifies reserved students

**Reservation Management**: LibraryPage.tsx
- Processes book reservations
- Manages reservation queue
- Notifies available books
- Expires old reservations

**Catalog Management**: LibraryPage.tsx (Catalog)
- Adds new books to catalog
- Updates book information
- Manages book copies
- Assigns categories and locations

#### Afternoon: Library Services
**Fine Management**: FeesPage.tsx
- Reviews library fine payments
- Processes fine waivers if applicable
- Addresses fine disputes
- Updates fine records

**Library Analytics**: AnalyticsPage.tsx
- Reviews circulation statistics
- Identifies popular books
- Monitors collection utilization
- Generates library reports

**User Support**: During operations
- Assists students with book search
- Resolves circulation issues
- Provides library orientation
- Addresses user complaints

#### Evening: Closing Tasks
**Daily Reconciliation**: LibraryPage.tsx
- Reconciles daily circulation
- Identifies discrepancies
- Updates library statistics
- Prepares daily reports

**Inventory Management**: LibraryPage.tsx
- Reviews book availability
- Identifies missing/damaged books
- Plans acquisition requests
- Updates inventory records

**Notice Board**: NoticeBoardPage.tsx
- Posts library announcements
- Updates library hours
- Notifies new arrivals
- Manages library notices

### Key Responsibilities

1. **Library Operations**
   - Book circulation management
   - Catalog maintenance
   - User service delivery
   - Library policy enforcement

2. **Collection Management**
   - Book acquisition and processing
   - Inventory management
   - Collection development
   - Preservation and maintenance

3. **User Services**
   - Circulation services
   - Reference assistance
   - Library orientation
   - User support

4. **Library Administration**
   - Policy implementation
   - Statistics and reporting
   - Budget management
   - Staff coordination

### Screens Frequently Used
- DashboardPage.tsx
- LibraryPage.tsx
- FeesPage.tsx
- NoticeBoardPage.tsx
- AnalyticsPage.tsx
- UserManagementPage.tsx

### Decisions Made
- Book acquisition decisions
- Fine waiver decisions
- Library policy adjustments
- Reservation prioritization
- Service hours decisions

### Interactions with Other Users
- **Students**: Circulation services, assistance
- **Faculty**: Collection development support
- **Admin**: Library administration
- **Vendors**: Book acquisition

### Pain Points
- Managing high circulation volume
- Handling overdue items
- Reserving popular books
- Maintaining inventory accuracy
- Balancing budget and needs

### Success Metrics
- Circulation statistics
- User satisfaction
- Collection utilization
- Fine collection rate
- Inventory accuracy

---

## Accountant Journey

### Who is Accountant?
Accountant manages financial operations including fee collection, payment processing, and financial reporting. They ensure timely fee collection and accurate financial records.

### Typical Day in the Life

#### Morning: Financial Overview
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views today's payment targets
- Checks pending fee demands
- Reviews collection statistics
- Monitors refund requests

**Fee Collection**: FeesPage.tsx
- Processes fee payments
- Records manual payments
- Generates receipts
- Updates payment records
- Handles payment queries

#### Mid-Day: Fee Management
**Fee Structure Review**: ProgramFeeManager.tsx
- Reviews fee structures
- Updates fee components if needed
- Configures payment schedules
- Manages fee heads

**Concession Management**: FeesPage.tsx
- Reviews concession applications
- Verifies eligibility
- Approves/rejects concessions
- Updates fee records

**Scholarship Processing**: FeesPage.tsx
- Processes scholarship applications
- Verifies eligibility criteria
- Calculates scholarship amounts
- Updates student fee records

#### Afternoon: Refunds and Reimbursements
**Refund Processing**: FeesPage.tsx
- Reviews refund requests
- Verifies refund eligibility
- Processes refund transactions
- Updates financial records
- Generates refund receipts

**Government Reimbursements**: FeesPage.tsx
- Processes government scholarship claims
- Verifies student eligibility
- Submits reimbursement claims
- Tracks claim status
- Records reimbursement receipts

**Financial Reporting**: AnalyticsPage.tsx
- Generates daily collection reports
- Reviews fee collection trends
- Identifies defaulters
- Prepares financial summaries

#### Evening: Reconciliation and Follow-up
**Payment Reconciliation**: FeesPage.tsx
- Reconciles daily payments
- Identifies discrepancies
- Updates financial records
- Prepares bank deposits

**Defaulter Management**: FeesPage.tsx
- Identifies fee defaulters
- Generates defaulter lists
- Sends payment reminders
- Initiates recovery actions

**My Tasks**: MyTasksPage.tsx
- Reviews financial approval tasks
- Approves financial requests
- Processes payment-related workflows
- Completes assigned tasks

### Key Responsibilities

1. **Fee Collection**
   - Process fee payments
   - Generate receipts
   - Manage payment records
   - Handle payment queries

2. **Financial Management**
   - Manage fee structures
   - Process concessions
   - Handle scholarships
   - Manage reimbursements

3. **Refund Processing**
   - Process refund requests
   - Verify eligibility
   - Execute refund transactions
   - Maintain refund records

4. **Financial Reporting**
   - Generate financial reports
   - Monitor collection trends
   - Identify defaulters
   - Prepare financial summaries

### Screens Frequently Used
- DashboardPage.tsx
- FeesPage.tsx
- ProgramFeeManager.tsx
- AnalyticsPage.tsx
- MyTasksPage.tsx
- UserManagementPage.tsx

### Decisions Made
- Concession approvals
- Refund processing
- Payment dispute resolution
- Defaulter classification
- Financial reporting decisions

### Interactions with Other Users
- **Students**: Fee collection, queries
- **Admin**: Financial reporting
- **Finance Head**: Policy guidance
- **Banks**: Payment processing

### Pain Points
- High payment volume management
- Handling payment disputes
- Processing refund requests
- Managing defaulters
- Maintaining accurate records

### Success Metrics
- Fee collection rate
- Payment processing accuracy
- Refund processing time
- Defaulter recovery rate
- Financial reporting accuracy

---

## Warden Journey

### Who is Warden?
Warden manages hostel operations including room allocation, student welfare, and hostel facility management. They ensure safe and comfortable hostel living for students.

### Typical Day in the Life

#### Morning: Hostel Operations
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views hostel occupancy
- Checks pending requests
- Reviews hostel notices
- Monitors hostel activities

**Room Allocation**: HostelPage.tsx
- Reviews allocation requests
- Allocates rooms to students
- Updates room occupancy
- Manages room changes
- Handles vacating requests

#### Mid-Day: Student Welfare
**Student Issues**: HostelPage.tsx
- Addresses student complaints
- Handles maintenance requests
- Resolves student conflicts
- Provides student support

**Hostel Facilities**: HostelPage.tsx
- Monitors facility conditions
- Coordinates maintenance
- Manages common areas
- Ensures safety standards

**Attendance and Discipline**: HostelPage.tsx
- Monitors student attendance
- Enforces hostel rules
- Addresses disciplinary issues
- Maintains discipline records

#### Afternoon: Fee and Administration
**Hostel Fee Management**: FeesPage.tsx
- Reviews hostel fee payments
- Processes fee concessions
- Manages mess fee billing
- Handles fee queries

**Refund Processing**: HostelPage.tsx
- Reviews security deposit refund requests
- Verifies room condition
- Processes refund approvals
- Updates refund records

**Hostel Configuration**: HostelPage.tsx
- Reviews hostel policies
- Configures fee components
- Manages hostel rules
- Updates hostel information

#### Evening: Safety and Reporting
**Safety Checks**: Physical rounds
- Conducts safety rounds
- Checks facility security
- Monitors student activities
- Addresses safety concerns

**Daily Reporting**: HostelPage.tsx
- Generates daily reports
- Documents incidents
- Updates hostel records
- Reports to administration

**Notice Board**: NoticeBoardPage.tsx
- Posts hostel notices
- Updates hostel rules
- Communicates with students
- Manages hostel announcements

### Key Responsibilities

1. **Hostel Management**
   - Room allocation and management
   - Student welfare and support
   - Facility maintenance
   - Safety and security

2. **Student Discipline**
   - Rule enforcement
   - Attendance monitoring
   - Disciplinary action
   - Conflict resolution

3. **Financial Management**
   - Hostel fee collection
   - Refund processing
   - Mess fee management
   - Financial record keeping

4. **Administration**
   - Policy implementation
   - Report generation
   - Staff coordination
   - Parent communication

### Screens Frequently Used
- DashboardPage.tsx
- HostelPage.tsx
- FeesPage.tsx
- NoticeBoardPage.tsx
- MyTasksPage.tsx
- UserManagementPage.tsx

### Decisions Made
- Room allocation decisions
- Disciplinary actions
- Refund approvals
- Maintenance prioritization
- Policy enforcement decisions

### Interactions with Other Users
- **Students**: Daily interaction and support
- **Admin**: Reporting and coordination
- **Maintenance staff**: Facility management
- **Parents**: Communication and updates

### Pain Points
- Managing student behavior
- Handling maintenance issues
- Balancing enforcement and welfare
- Processing refund requests
- Ensuring safety standards

### Success Metrics
- Student satisfaction
- Facility maintenance quality
- Fee collection rate
- Disciplinary incident rate
- Safety compliance

---

## Applicant Journey

### Who is Applicant?
Applicant is a prospective student who is applying for admission to the university. They interact with the system for registration, application submission, fee payment, and admission tracking.

### Application Journey

#### Step 1: Discovery and Information
**Access**: Public website or landing page
- Learns about programs offered
- Reviews admission requirements
- Understands application process
- Prepares necessary documents

#### Step 2: Registration
**Registration Page**: RegisterPage.tsx
- Enters personal information
- Provides contact details
- Selects applicant role
- Creates password
- Submits registration

**OTP Verification**: RegisterPage.tsx
- Receives OTP via email/SMS
- Enters OTP for verification
- Account activated on success

#### Step 3: Application Form
**Application Form**: StudentApplicationsPage.tsx or public form
- Fills personal details
- Provides academic history
- Uploads documents (marksheets, ID proofs)
- Selects program preferences
- Uploads photograph
- Saves draft as needed

#### Step 4: Application Fee Payment
**Payment Gateway**: Razorpay integration
- Views application fee amount
- Proceeds to payment
- Completes payment via Razorpay
- Receives payment confirmation

#### Step 5: Application Tracking
**Application Status**: StudentApplicationsPage.tsx
- Tracks application status
- Views coordinator review status
- Monitors approver decision
- Receives status notifications

#### Step 6: Counselling (Optional)
**Counselling Desk**: CounsellingDeskPage.tsx
- Requests counselling guidance
- Interacts with counsellor
- Receives program recommendations
- Gets application assistance

#### Step 7: Admission and Seat Allocation
**Admission Status**: StudentApplicationsPage.tsx
- Receives admission offer
- Views seat allocation details
- Accepts admission offer
- Proceeds to fee payment

#### Step 8: Admission Fee Payment
**Fee Payment**: FeesPage.tsx
- Views admission fee breakdown
- Pays admission fee via Razorpay
- Receives payment confirmation
- Downloads fee receipt

#### Step 9: Onboarding
**Onboarding**: OnboardStudentsPage.tsx (admin side)
- Completes profile setup
- Provides additional information
- Gets student ID assigned
- Receives login credentials

#### Step 10: Enrollment
**Student Portal**: Student journey begins
- Logs in as student
- Accesses academic services
- Begins academic journey

### Key Interactions

1. **Registration Process**
   - Create account
   - Verify identity
   - Complete profile

2. **Application Submission**
   - Fill application form
   - Upload documents
   - Pay application fee

3. **Application Tracking**
   - Monitor status
   - Respond to queries
   - Provide additional information

4. **Admission Process**
   - Receive offer
   - Accept admission
   - Pay admission fee

5. **Onboarding**
   - Complete enrollment
   - Get student ID
   - Access student services

### Screens Used
- RegisterPage.tsx
- StudentApplicationsPage.tsx
- CounsellingDeskPage.tsx
- FeesPage.tsx
- LoginPage.tsx (after enrollment)

### Decisions Made
- Program selection
- Document preparation
- Payment timing
- Admission acceptance
- Counselling utilization

### Interactions with Other Users
- **Admission Coordinators**: Application review
- **Approvers**: Admission decision
- **Counsellors**: Guidance and support
- **Finance Officers**: Fee processing

### Pain Points
- Document preparation and upload
- Application fee payment
- Waiting for admission decision
- Understanding process requirements
- Onboarding complexity

### Success Metrics
- Application completion rate
- Document accuracy
- Fee payment timeliness
- Admission conversion rate
- Onboarding success

---

## Parent Journey

### Who is Parent?
Parent is a guardian who wants to monitor their child's academic progress, fee payments, and overall performance. They access the system through the parent portal or linked accounts.

### Typical Monitoring Journey

#### Step 1: Account Setup
**Parent Linking**: StudentProfilePage.tsx (student initiates)
- Student links parent account
- Parent receives invitation
- Creates parent account
- Verifies relationship

#### Step 2: Dashboard Access
**Parent Dashboard**: Parent portal (accessed via login)
- Views child's academic summary
- Checks attendance status
- Reviews fee payment status
- Monitors overall performance

#### Step 3: Academic Monitoring
**Academic Performance**: StudentProfilePage.tsx (parent view)
- Views term results
- Checks SGPA/CGPA
- Reviews subject-wise performance
- Downloads mark sheets

**Attendance Monitoring**: AttendancePage.tsx (parent view)
- Views attendance record
- Checks attendance percentage
- Identifies attendance issues
- Reviews attendance trends

#### Step 4: Fee Management
**Fee Status**: FeesPage.tsx (parent view)
- Views pending fee demands
- Reviews payment history
- Checks fee payment status
- Pays fees on behalf of child

#### Step 5: Communication
**Notice Board**: NoticeBoardPage.tsx
- Views institute notices
- Checks examination schedules
- Reviews holiday announcements
- Monitors event notifications

**Direct Communication**: Through system
- Communicates with teachers
- Contacts administration
- Receives important alerts
- Responds to queries

#### Step 6: Reports and Analytics
**Performance Reports**: AnalyticsPage.tsx (parent view)
- Views academic performance trends
- Reviews attendance patterns
- Monitors fee payment history
- Generates progress reports

### Key Monitoring Activities

1. **Academic Performance**
   - Track grades and results
   - Monitor subject performance
   - Identify areas of concern
   - Review teacher feedback

2. **Attendance Monitoring**
   - Check daily attendance
   - Monitor attendance trends
   - Address attendance issues
   - Ensure compliance

3. **Fee Management**
   - View fee obligations
   - Make timely payments
   - Track payment history
   - Manage concessions

4. **Communication**
   - Receive school communications
   - Contact teachers/administration
   - Respond to queries
   - Provide feedback

### Screens Used
- Parent Dashboard (if separate portal)
- StudentProfilePage.tsx (parent view)
- AttendancePage.tsx (parent view)
- FeesPage.tsx (parent view)
- NoticeBoardPage.tsx

### Decisions Made
- Fee payment timing
- Communication preferences
- Academic support decisions
- Extra-curricular participation

### Interactions with Other Users
- **Child**: Monitor and support
- **Teachers**: Academic communication
- **Administration**: Fee and general queries
- **Other Parents**: Community interaction

### Pain Points
- Understanding academic performance
- Managing fee payments
- Interpreting attendance data
- Communication gaps
- Technical access issues

### Success Metrics
- Child's academic performance
- Fee payment compliance
- Attendance compliance
- Communication effectiveness
- Parent satisfaction

---

## Counsellor Journey

### Who is Counsellor?
Counsellor provides guidance to applicants for program selection, career advice, and admission support. They are empanelled by the university and compensated based on enrollment attribution.

### Typical Day in the Life

#### Morning: Request Review
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views pending counselling requests
- Checks assigned requests
- Reviews response targets
- Monitors enrollment credits

#### Mid-Day: Counselling Sessions
**Counselling Desk**: CounsellingDeskPage.tsx
- Reviews assigned requests
- Studies applicant profiles
- Prepares guidance materials
- Initiates counselling conversation

**Guidance Delivery**: CounsellingDeskPage.tsx
- Provides program information
- Discusss career options
- Recommends suitable programs
- Answers applicant questions
- Guides application process

**Follow-up Communication**: CounsellingDeskPage.tsx
- Responds to applicant queries
- Provides additional information
- Shares program details
- Assists with application

#### Afternoon: Application Support
**Application Assistance**: CounsellingDeskPage.tsx
- Helps applicants with forms
- Reviews application details
- Provides document guidance
- Assists with fee payment process

**Application Tracking**: CounsellingDeskPage.tsx
- Monitors submitted applications
- Tracks admission status
- Provides status updates
- Assists with next steps

#### Evening: Reporting and Compensation
**Performance Review**: CounsellingAdminPage.tsx
- Reviews counselling statistics
- Monitors response time
- Tracks enrollment attribution
- Views compensation details

**Documentation**: CounsellingDeskPage.tsx
- Documents counselling sessions
- Records recommendations made
- Updates applicant profiles
- Maintains interaction history

**Feedback Collection**: CounsellingDeskPage.tsx
- Requests applicant feedback
- Reviews ratings received
- Identifies improvement areas
- Updates counselling approach

### Key Responsibilities

1. **Applicant Guidance**
   - Provide program information
   - Offer career advice
   - Assist with application process
   - Support decision making

2. **Communication**
   - Respond to applicant queries
   - Provide timely information
   - Maintain professional communication
   - Build rapport with applicants

3. **Application Support**
   - Assist with form filling
   - Guide document preparation
   - Support fee payment process
   - Track application status

4. **Performance Management**
   - Meet response time targets
   - Achieve enrollment attribution
   - Maintain quality ratings
   - Improve counselling effectiveness

### Screens Frequently Used
- DashboardPage.tsx
- CounsellingDeskPage.tsx
- CounsellingAdminPage.tsx
- AnalyticsPage.tsx

### Decisions Made
- Program recommendations
- Application guidance
- Communication priorities
- Follow-up strategies
- Improvement initiatives

### Interactions with Other Users
- **Applicants**: Primary interaction
- **University Admin**: Contract and compensation
- **Admission Team**: Application coordination
- **Other Counsellors**: Best practice sharing

### Pain Points
- Managing high request volume
- Providing timely responses
- Achieving enrollment targets
- Maintaining quality ratings
- Handling difficult cases

### Success Metrics
- Response time
- Enrollment attribution
- Applicant satisfaction ratings
- Application completion rate
- Compensation earned

---

## Summary

This UniversityERP system serves diverse user types with distinct journeys:

**Administrative Users:**
- SuperAdmin: System-wide configuration and oversight
- University Admin: Academic governance and coordination
- Institute Admin: Day-to-day operations and management

**Academic Users:**
- Student: Learning, assessment, and services
- Teaching Faculty: Teaching, evaluation, and guidance
- HOD: Department leadership and coordination

**Support Staff:**
- Librarian: Library services and management
- Accountant: Financial operations and reporting
- Warden: Hostel management and student welfare

**External Users:**
- Applicant: Admission process and onboarding
- Parent: Student monitoring and support
- Counsellor: Guidance and enrollment support

Each user journey is designed to:
- Support the user's primary responsibilities
- Provide relevant information and tools
- Enable efficient task completion
- Facilitate communication with stakeholders
- Support decision-making processes

The system's role-based access control ensures users see only relevant features and data, while workflow automation streamlines approval processes and notifications keep all stakeholders informed.

---

**Document Version**: 1.0  
**Last Updated**: 2025-08-05



---


# Data Flow and Lifecycle Documentation

## Table of Contents
1. [Student Data Lifecycle](#student-data-lifecycle)
2. [Fee Data Lifecycle](#fee-data-lifecycle)
3. [Examination Data Lifecycle](#examination-data-lifecycle)
4. [Workflow Data Lifecycle](#workflow-data-lifecycle)
5. [Document Data Lifecycle](#document-data-lifecycle)
6. [Attendance Data Lifecycle](#attendance-data-lifecycle)
7. [Academic Result Data Lifecycle](#academic-result-data-lifecycle)
8. [Library Data Lifecycle](#library-data-lifecycle)
9. [Hostel Data Lifecycle](#hostel-data-lifecycle)
10. [Notification Data Lifecycle](#notification-data-lifecycle)

---

## Student Data Lifecycle

### Purpose
Track the complete journey of a student from registration to alumni status, including all data transformations and state changes.

### Lifecycle Stages

#### Stage 1: Registration Request
**Origin**: User submits registration form via RegisterPage.tsx

**Data Created**:
- `User` record (initial state: `isActive: false`)
- `RegistrationRequest` record (status: "registered")
- `MobileOtp` record (if mobile verification enabled)

**Data Fields**:
- User: email, passwordHash, firstName, lastName, phone, dateOfBirth
- RegistrationRequest: universityId, role, status, profileData

**Processing**:
- AuthService.register() validates and creates records
- OTP verification triggers activation
- Email/SMS notification sent

**State Change**: `registration.requested` → `registration.verified`

**Next Stage**: Application Form (if applicant) or Direct Onboarding (if staff import)

---

#### Stage 2: Application Form (Applicant Path)
**Origin**: Applicant fills admission form via StudentApplicationsPage.tsx

**Data Created**:
- `FormSubmission` record
- `WorkflowInstance` record (if workflow configured)
- `FeeDemand` record (application fee)

**Data Fields**:
- FormSubmission: formTemplateId, data (JSON), status
- WorkflowInstance: definitionId, entityType, entityId, initiatorUserId
- FeeDemand: userId, amount, feeHeadId, status

**Processing**:
- FormsService.submit() processes form data
- File uploads stored in MinIO
- WorkflowEngineService.startInstance() creates workflow
- FeeService creates demand for application fee

**State Change**: `application.submitted` → `application.fee_pending`

**Next Stage**: Application Fee Payment

---

#### Stage 3: Application Fee Payment
**Origin**: Applicant pays via Razorpay

**Data Created**:
- `Payment` record
- `FeeLedger` record
- Updated `FeeDemand` status

**Data Fields**:
- Payment: amount, razorpayPaymentId, status, paymentDate
- FeeLedger: userId, credit/debit, balance, transactionId

**Processing**:
- Razorpay callback processed by WorkflowPaymentService
- Payment recorded in FeeLedger
- Workflow advanced to next state
- Receipt generated

**State Change**: `application.fee_pending` → `application.under_review`

**Next Stage**: Coordinator Review

---

#### Stage 4: Coordinator Review
**Origin**: Admission coordinator reviews application

**Data Updated**:
- `FormSubmission` status and reviewData
- `WorkflowInstance` state
- `WorkflowTask` created for approver

**Data Fields**:
- FormSubmission: status, reviewData (comments, decision)
- WorkflowInstance: currentState, dataBag
- WorkflowTask: assigneeUserId, status

**Processing**:
- AdmissionsService.review() validates permissions
- WorkflowEngineService advances state
- Notification sent to approver

**State Change**: `application.under_review` → `application.pending_approval`

**Next Stage**: Approver Decision

---

#### Stage 5: Approver Decision
**Origin`: Designated approver approves application

**Data Updated**:
- `WorkflowInstance` state and outcome
- `WorkflowTask` status
- `FormSubmission` final status

**Data Fields**:
- WorkflowInstance: currentState, outcome, completedAt
- FormSubmission: status, approvedBy, approvedAt

**Processing**:
- WorkflowEngineService.completeTask() executes transition
- If approved: triggers seat allocation
- If rejected: notifies applicant
- Notification sent to relevant parties

**State Change**: `application.pending_approval` → `application.approved` or `application.rejected`

**Next Stage**: Seat Allocation (if approved)

---

#### Stage 6: Seat Allocation
**Origin**: System or admin allocates seat

**Data Created**:
- `Student` record
- `StudentProfile` record
- `StudentSubjectEnrollment` records (auto-enroll)
- Updated `ProgramSeatApproval`

**Data Fields**:
- Student: userId, sectionId, enrollmentNo, status
- StudentProfile: userId, enrollmentNo, additional personal data
- StudentSubjectEnrollment: studentId, batchTermSubjectId, enrollmentType

**Processing**:
- AdmissionsService.allocateSeat() checks availability
- Creates Student record linked to User
- Assigns section and enrollment number
- Auto-enrolls in mandatory subjects based on batch configuration
- IdGeneratorService generates enrollment number

**State Change**: `application.approved` → `student.enrolled`

**Next Stage**: Fee Payment and Activation

---

#### Stage 7: Fee Payment and Activation
**Origin**: Student pays admission fee

**Data Created**:
- `Payment` record
- `FeeLedger` record
- Updated `FeeDemand` records
- `FeeReceipt` record

**Data Updated**:
- `Student` status
- `User` isActive flag

**Processing**:
- FeeService.recordPayment() processes payment
- Student status updated to "active"
- User account fully activated
- Document generation triggered (ID card)

**State Change**: `student.enrolled` → `student.active`

**Next Stage**: Academic Activities

---

#### Stage 8: Academic Activities (Ongoing)
**Origin**: Student participates in academic life

**Data Created/Updated**:
- `StudentAttendance` records (daily)
- `StudentMarks` records (per exam)
- `StudentTermElection` records (elective selection)
- `LeaveApplication` records (if applicable)

**Data Fields**:
- StudentAttendance: studentId, date, status, markedBy
- StudentMarks: studentId, batchTermSubjectId, marks, grade
- StudentTermElection: studentId, subjectIds, status

**Processing**:
- Attendance marked by faculty via AttendancePage
- Marks entered via ExaminationsPage
- Electives selected via ElectivesPage
- Continuous updates throughout academic year

**State Change**: `student.active` (ongoing)

**Next Stage**: Results and Graduation

---

#### Stage 9: Results and Graduation
**Origin**: Student completes program requirements

**Data Created**:
- `StudentTermResult` records (per term)
- `StudentCumulativeResult` record
- `IssuedDocument` records (degree certificate, mark sheets)

**Data Updated**:
- `Student` status
- `User` role (to Alumni)

**Data Fields**:
- StudentTermResult: studentId, batchTermId, sgpa, status
- StudentCumulativeResult: studentId, cgpa, totalCredits
- IssuedDocument: userId, documentTemplateId, issuedAt

**Processing**:
- AcademicService.computeResult() calculates SGPA/CGPA
- AcademicService.publishResult() makes results visible
- DocumentsService.generate() creates certificates
- User role updated to Alumni upon graduation

**State Change**: `student.active` → `student.graduated` → `alumni.active`

**Final State**: Alumni with access to certain services

---

### Data Relationships

```
User (1) → (1) RegistrationRequest
User (1) → (1) Student
User (1) → (N) FormSubmission
Student (1) → (N) StudentSubjectEnrollment
Student (1) → (N) StudentAttendance
Student (1) → (N) StudentMarks
Student (1) → (N) StudentTermResult
Student (1) → (1) StudentCumulativeResult
Student (1) → (N) IssuedDocument
```

### Key Data Transformations

1. **User → Student**: User record linked to Student record upon enrollment
2. **RegistrationRequest → Student**: Application data migrates to Student profile
3. **FormSubmission → WorkflowInstance**: Form data triggers workflow process
4. **StudentSubjectEnrollment → StudentMarks**: Enrollment enables marks entry
5. **StudentMarks → StudentTermResult**: Marks aggregated into term results
6. **StudentTermResult → StudentCumulativeResult**: Term results aggregated into CGPA

### Data Retention and Archival

- **Active Data**: All current student data retained in main tables
- **Historical Data**: Student records maintained indefinitely for transcripts
- **Audit Trail**: All changes logged in AuditLog and WorkflowInstanceEvent
- **Document Storage**: Issued documents stored in MinIO with database references
- **Backup**: Full database backups scheduled per university configuration

---

## Fee Data Lifecycle

### Purpose
Track the complete lifecycle of fee-related data from demand creation to payment processing and refund handling.

### Lifecycle Stages

#### Stage 1: Fee Structure Configuration
**Origin**: Admin configures fee structure via ProgramFeeManager.tsx

**Data Created**:
- `FeeStructure` record
- `FeeHead` records (components)

**Data Fields**:
- FeeStructure: programmeId, name, effectiveFrom, components (JSON)
- FeeHead: name, type, amount, applicableTo, recurrence

**Processing**:
- FeeService.createStructure() validates configuration
- FeeHead records created for each component
- Linked to programmes/batches
- Effective dates set for versioning

**State Change**: `fee_structure.configured`

**Next Stage**: Demand Generation

---

#### Stage 2: Demand Generation
**Origin**: System generates fee demands (automated or manual)

**Data Created**:
- `FeeDemand` records (per student)

**Data Fields**:
- FeeDemand: userId, amount, feeHeadId, dueDate, status, sourceRef

**Processing**:
- RecurringBillingService.run() generates demands daily at 2 AM
- Manual demand creation via FeesPage
- Applies StudentConcession discounts
- Uses sourceRef to prevent duplicate demands
- Links to Student or RegistrationRequest

**State Change**: `fee_demand.created` → `fee_demand.pending`

**Next Stage**: Payment Processing

---

#### Stage 3: Payment Processing
**Origin**: Student pays fee via Razorpay or manual payment

**Data Created**:
- `Payment` record
- `FeeLedger` record
- `FeeReceipt` record

**Data Updated**:
- `FeeDemand` status
- `StudentConcession` (if applicable)

**Data Fields**:
- Payment: amount, mode, razorpayPaymentId, status, paymentDate
- FeeLedger: userId, credit/debit, balance, transactionId, relatedDemandId
- FeeReceipt: paymentId, receiptNumber, issuedAt

**Processing**:
- Razorpay payment processed by WorkflowPaymentService
- Manual payment recorded by FeeService.recordPayment
- FeeLedger updated with transaction
- FeeDemand status updated to "paid"
- Receipt generated and stored

**State Change**: `fee_demand.pending` → `fee_demand.paid`

**Next Stage**: Concession Application (optional)

---

#### Stage 4: Concession Application
**Origin**: Student applies for fee concession via FormsPage.tsx

**Data Created**:
- `FormSubmission` record
- `WorkflowInstance` record

**Data Updated**:
- `StudentConcession` record (upon approval)

**Data Fields**:
- StudentConcession: studentId, programmeId, concessionType, percentage, validUntil

**Processing**:
- Workflow processes concession request
- On approval: StudentConcession record created
- Existing demands recalculated with discount
- Future billing applies concession automatically

**State Change**: `concession.requested` → `concession.approved`

**Next Stage**: Recurring Billing Adjustment

---

#### Stage 5: Recurring Billing Adjustment
**Origin**: System applies concessions to recurring billing

**Data Updated**:
- `FeeDemand` records (recalculated amounts)
- `StudentConcession` usage tracking

**Processing**:
- RecurringBillingService applies concession rules
- Calculates discounted amounts
- Generates demands with concession applied
- Tracks concession usage against limits

**State Change**: `fee_demand.adjusted`

**Next Stage**: Refund Processing (optional)

---

#### Stage 6: Refund Request
**Origin**: Student requests deposit refund via FeesPage.tsx

**Data Created**:
- `ProgramDepositRefundRequest` or `HostelRefundRequest` record
- `WorkflowInstance` record

**Data Fields**:
- ProgramDepositRefundRequest: studentId, amount, bankAccountDetails, status
- HostelRefundRequest: studentId, hostelAllocationId, amount, status

**Processing**:
- FeeService.initiateRefund() validates eligibility
- Workflow approval process initiated
- Bank account details verified
- Deductions calculated (if any)

**State Change**: `refund.requested` → `refund.pending_approval`

**Next Stage**: Refund Approval

---

#### Stage 7: Refund Approval and Processing
**Origin**: Finance officer approves and processes refund

**Data Created**:
- `Payment` record (refund type)
- `FeeLedger` record (credit)

**Data Updated**:
- Refund request status
- `FeeDemand` (if related to specific fee)

**Processing**:
- Workflow approval processed
- Bank transfer initiated
- Payment recorded as refund
- FeeLedger credited with refund amount
- Notification sent to student

**State Change**: `refund.pending_approval` → `refund.processed`

**Final State**: Refund completed, financial record updated

---

### Data Relationships

```
User (1) → (N) FeeDemand
User (1) → (N) FeeLedger
User (1) → (N) Payment
User (1) → (N) FeeReceipt
Student (1) → (N) StudentConcession
FeeDemand (1) → (1) FeeHead
FeeDemand (1) → (N) Payment
Payment (1) → (1) FeeReceipt
FeeStructure (1) → (N) FeeHead
Programme (1) → (N) FeeStructure
```

### Key Data Transformations

1. **FeeStructure → FeeDemand**: Configuration translated into individual demands
2. **StudentConcession → FeeDemand**: Discounts applied to demand amounts
3. **Payment → FeeLedger**: Transaction recorded in financial ledger
4. **FeeDemand → Payment**: Demand fulfilled by payment
5. **RefundRequest → Payment**: Refund processed as negative payment

### Data Retention Policies

- **Fee Structures**: Retained indefinitely for historical reference
- **Fee Demands**: Retained for audit trail (7+ years)
- **Payments**: Retained indefinitely for financial records
- **FeeLedger**: Permanent financial record
- **Receipts**: Retained indefinitely, stored in MinIO
- **Concessions**: Retained while student is active + 7 years

---

## Examination Data Lifecycle

### Purpose
Track the complete lifecycle of examination data from question bank to result processing and revaluation.

### Lifecycle Stages

#### Stage 1: Question Bank Management
**Origin**: Faculty adds questions via ExaminationsPage.tsx

**Data Created**:
- `Question` record

**Data Fields**:
- Question: text, type, difficulty, subjectId, answerKey, tags

**Processing**:
- QuestionBankService.addQuestion() validates format
- Math formulas supported via KaTeX
- Bulk import from Excel
- Tagged with subject and difficulty level

**State Change**: `question.created`

**Next Stage**: Exam Paper Creation

---

#### Stage 2: Exam Paper Creation
**Origin**: Exam controller creates paper via ExaminationsPage.tsx

**Data Created**:
- `ExamPaper` record
- `ExamPaperQuestion` records

**Data Fields**:
- ExamPaper: name, code, subjectId, duration, totalMarks
- ExamPaperQuestion: examPaperId, questionId, marks, order

**Processing**:
- ExaminationService.createPaper() configures paper
- Questions selected from bank
- Marking scheme defined
- Paper code generated
- Total marks calculated

**State Change**: `exam_paper.created`

**Next Stage**: Exam Scheduling

---

#### Stage 3: Exam Scheduling
**Origin**: Admin schedules exam via ExaminationsPage.tsx

**Data Created**:
- `ExamSchedule` record
- `ExamInvigilator` records

**Data Fields**:
- ExamSchedule: examPaperId, batchId, date, venue
- ExamInvigilator: examScheduleId, userId, role

**Processing**:
- ExamSchedulerService creates schedule
- Invigilators assigned
- Hall tickets generated
- Resource conflicts checked
- Notifications sent to students and invigilators

**State Change**: `exam.scheduled`

**Next Stage**: Exam Execution

---

#### Stage 4: Exam Execution (CBE)
**Origin**: Student takes online exam via ExamTakePage.tsx

**Data Created**:
- `ExamAttempt` record
- `ExamResponse` records
- `ExamProctorEvent` records (if integrity violations)
- `ExamSnapshot` records (periodic webcam images)

**Data Fields**:
- ExamAttempt: examPaperId, studentId, startTime, endTime, deviceFingerprint
- ExamResponse: examAttemptId, questionId, answer, markedForReview
- ExamProctorEvent: examAttemptId, eventType, timestamp, details
- ExamSnapshot: examAttemptId, imageData, timestamp

**Processing**:
- ExaminationService.startExam() creates attempt
- Frontend tracks proctoring events
- Periodic snapshots uploaded
- Answers saved periodically
- Tab switches and integrity violations logged
- Auto-submit on timeout

**State Change**: `exam.in_progress` → `exam.submitted`

**Next Stage**: Grading

---

#### Stage 5: Grading and Evaluation
**Origin**: Faculty grades papers via ExaminationsPage.tsx

**Data Created**:
- `StudentMarks` records

**Data Updated**:
- `ExamAttempt` status
- `ExamResponse` (graded answers)

**Data Fields**:
- StudentMarks: studentId, batchTermSubjectId, examPaperId, marks, grade, remarks

**Processing**:
- MCQs auto-graded by system
- Descriptive answers manually graded
- Marks entered per question
- Grades assigned based on StreamLabel rules
- Feedback comments added

**State Change**: `exam.submitted` → `exam.graded`

**Next Stage**: Question Challenge (optional)

---

#### Stage 6: Question Challenge
**Origin**: Student challenges question via ExaminationsPage.tsx

**Data Created**:
- `QuestionChallenge` record

**Data Fields**:
- QuestionChallenge: examPaperId, questionId, studentId, reason, status

**Processing**:
- ExaminationService.challengeQuestion() creates challenge
- Routes to examiner for review
- Holds on mark adjustment
- If approved: adjusts marks for all affected students

**State Change**: `challenge.requested` → `challenge.resolved`

**Next Stage**: Result Processing

---

#### Stage 7: Result Processing
**Origin**: System computes results via AcademicModule

**Data Created**:
- `StudentTermResult` records
- Updated `StudentCumulativeResult` record

**Data Fields**:
- StudentTermResult: studentId, batchTermId, sgpa, totalCredits, status
- StudentCumulativeResult: studentId, cgpa, totalCredits, overallStatus

**Processing**:
- AcademicService.computeResult() aggregates marks
- SGPA calculated using StreamLabel grade boundaries
- Pass/fail determined per subject
- Term result created
- CGPA updated in cumulative result
- Result holds applied if fee defaulters

**State Change**: `result.computed` → `result.pending_approval`

**Next Stage**: Result Publication

---

#### Stage 8: Result Publication
**Origin**: Admin publishes results via ExaminationsPage.tsx

**Data Updated**:
- `StudentTermResult` status
- `StudentCumulativeResult` (if final)

**Processing**:
- AcademicService.publishResult() updates status
- Results become visible to students
- Notifications sent to students
- Mark sheets generated
- Revaluation window opened

**State Change**: `result.pending_approval` → `result.published`

**Next Stage**: Revaluation (optional)

---

#### Stage 9: Revaluation Request
**Origin**: Student applies for revaluation via FormsPage.tsx

**Data Created**:
- `ReAssessmentRequest` record
- `WorkflowInstance` record
- `FeeDemand` record (revaluation fee)

**Data Fields**:
- ReAssessmentRequest: studentId, examPaperId, type, status, fee

**Processing**:
- Workflow processes revaluation request
- Fee payment required
- Paper re-evaluated by examiner
- Marks updated if changed
- SGPA/CGPA recalculated if needed

**State Change**: `revaluation.requested` → `revaluation.processed`

**Final State**: Results finalized with revaluation incorporated

---

### Data Relationships

```
Question (1) → (N) ExamPaperQuestion
ExamPaper (1) → (N) ExamPaperQuestion
ExamPaper (1) → (N) ExamSchedule
ExamSchedule (1) → (N) ExamInvigilator
ExamPaper (1) → (N) ExamAttempt
ExamAttempt (1) → (N) ExamResponse
ExamAttempt (1) → (N) ExamProctorEvent
ExamAttempt (1) → (N) ExamSnapshot
Student (1) → (N) StudentMarks
Student (1) → (N) ExamAttempt
StudentMarks (1) → (1) StudentTermResult
StudentTermResult (1) → (1) StudentCumulativeResult
Question (1) → (N) QuestionChallenge
```

### Key Data Transformations

1. **Question → ExamPaperQuestion**: Question bank to paper mapping
2. **ExamResponse → StudentMarks**: Answers translated to marks
3. **StudentMarks → StudentTermResult**: Marks aggregated to term results
4. **StudentTermResult → StudentCumulativeResult**: Term results aggregated to CGPA
5. **QuestionChallenge → StudentMarks**: Approved challenges trigger mark updates

### Data Retention Policies

- **Questions**: Retained indefinitely for question bank
- **Exam Papers**: Retained for 7+ years for audit
- **Exam Attempts**: Retained for 7+ years
- **Proctoring Data**: Retained for 1 year (storage optimization)
- **Results**: Retained indefinitely for transcripts
- **Revaluation Records**: Retained for 7+ years

---

## Workflow Data Lifecycle

### Purpose
Track the complete lifecycle of workflow instances from initiation to completion, including all state transitions and task assignments.

### Lifecycle Stages

#### Stage 1: Workflow Definition
**Origin**: Admin designs workflow via WorkflowDesignerPage.tsx

**Data Created**:
- `WorkflowDefinition` record
- `WorkflowState` records
- `WorkflowTransition` records

**Data Fields**:
- WorkflowDefinition: name, entityType, version, initial
- WorkflowState: key, type, assigneeRole, actions
- WorkflowTransition: fromState, toState, decision, actions

**Processing**:
- WorkflowDefinitionService creates definition
- States configured with assignee roles
- Transitions defined with conditions
- Actions bound to transitions
- Version management supported

**State Change**: `workflow.defined`

**Next Stage**: Instance Initiation

---

#### Stage 2: Instance Initiation
**Origin**: User action triggers workflow (form submission, request, etc.)

**Data Created**:
- `WorkflowInstance` record
- `WorkflowTask` record (initial task)
- `WorkflowReservation` records (if resource holds)

**Data Fields**:
- WorkflowInstance: definitionId, entityType, entityId, initiatorUserId, currentState
- WorkflowTask: instanceId, assigneeUserId, status, dueDate
- WorkflowReservation: instanceId, resourceType, resourceId, status

**Processing**:
- WorkflowEngineService.startInstance() creates instance
- Initial state set from definition
- Initial task created for assignee
- Resource holds created if needed
- Data bag initialized with form data
- Notification sent to assignee

**State Change**: `workflow.started` → `workflow.in_progress`

**Next Stage**: Task Assignment

---

#### Stage 3: Task Assignment
**Origin**: Workflow assigns task to user based on role/resolver

**Data Created/Updated**:
- `WorkflowTask` record
- Notification sent to assignee

**Data Fields**:
- WorkflowTask: assigneeUserId, status, data, dueDate

**Processing**:
- WorkflowActorResolver resolves assignee
- Task created with assignee
- Due date set based on SLA
- Notification sent via NotificationsService
- Task appears in user's MyTasks inbox

**State Change**: `workflow.task_assigned`

**Next Stage**: Task Completion

---

#### Stage 4: Task Completion
**Origin**: User completes task via MyTasksPage.tsx

**Data Updated**:
- `WorkflowTask` status
- `WorkflowInstance` state and dataBag
- `WorkflowInstanceEvent` record created
- `WorkflowReservation` records updated

**Data Fields**:
- WorkflowTask: status, completedAt, result
- WorkflowInstance: currentState, dataBag
- WorkflowInstanceEvent: fromState, toState, actorUserId, timestamp

**Processing**:
- WorkflowEngineService.completeTask() processes completion
- Transition executed based on decision
- Actions executed (email, SMS, resource operations)
- Data bag updated with task result
- Event logged for audit
- Next task created if applicable
- Resource reservations updated/confirmed/released

**State Change**: `workflow.task_completed` → `workflow.next_state` or `workflow.completed`

**Next Stage**: Payment Gate (if applicable)

---

#### Stage 5: Payment Gate
**Origin**: Workflow requires payment before proceeding

**Data Created**:
- `FeeDemand` record
- `WorkflowInstance` data updated with payment gate info

**Data Fields**:
- FeeDemand: userId, amount, feeHeadId, sourceRef (workflow instance)

**Processing**:
- WorkflowPaymentService creates demand
- User redirected to payment gateway
- Razorpay payment processed
- On success: workflow advances
- On failure: workflow stays in payment state

**State Change**: `workflow.payment_pending` → `workflow.payment_completed`

**Next Stage**: Terminal State

---

#### Stage 6: Terminal State
**Origin**: Workflow reaches approved/rejected/cancelled state

**Data Updated**:
- `WorkflowInstance` outcome and completedAt
- `WorkflowTask` final status
- `WorkflowReservation` final status

**Data Fields**:
- WorkflowInstance: outcome, completedAt, finalData
- WorkflowTask: status (all tasks closed)
- WorkflowReservation: status (confirmed or released)

**Processing**:
- Workflow reaches terminal state
- Outcome determined (approved/rejected/cancelled)
- All pending tasks closed
- Resource reservations:
  - Confirmed if approved
  - Released if rejected/cancelled
- Final actions executed
- Notifications sent to all stakeholders
- Instance archived for audit

**State Change**: `workflow.in_progress` → `workflow.completed`

**Final State**: Workflow instance complete with audit trail

---

### Data Relationships

```
WorkflowDefinition (1) → (N) WorkflowState
WorkflowDefinition (1) → (N) WorkflowTransition
WorkflowDefinition (1) → (N) WorkflowInstance
WorkflowInstance (1) → (N) WorkflowTask
WorkflowInstance (1) → (N) WorkflowInstanceEvent
WorkflowInstance (1) → (N) WorkflowReservation
WorkflowState (1) → (N) WorkflowTransition (from)
WorkflowState (1) → (N) WorkflowTransition (to)
WorkflowTask (1) → (1) User (assignee)
WorkflowReservation (1) → (1) ResourceReservation (confirmed)
```

### Key Data Transformations

1. **WorkflowDefinition → WorkflowInstance**: Template instantiated with specific entity
2. **WorkflowState → WorkflowTask**: State translated into user task
3. **WorkflowTask → WorkflowInstanceEvent**: Task completion logged as event
4. **WorkflowInstance → WorkflowReservation**: Instance creates resource holds
5. **WorkflowReservation → ResourceReservation**: Confirmed holds become actual bookings

### Data Retention Policies

- **WorkflowDefinitions**: Retained indefinitely (active configurations)
- **WorkflowInstances**: Retained for 7+ years for audit
- **WorkflowTasks**: Retained with instance
- **WorkflowInstanceEvents**: Retained with instance (complete audit trail)
- **WorkflowReservations**: Retained for 1 year after instance completion

---

## Document Data Lifecycle

### Purpose
Track the complete lifecycle of document generation from template configuration to issuance and archival.

### Lifecycle Stages

#### Stage 1: Template Configuration
**Origin**: Admin configures document template via DocumentsPage.tsx

**Data Created**:
- `DocumentTemplate` record

**Data Fields**:
- DocumentTemplate: name, type, layout (JSON), signatureConfig, approvalRequired

**Processing**:
- DocumentsService.createTemplate() saves configuration
- Layout designed with visual editor
- Field placeholders defined
- Signature configuration set
- Approval workflow configured if needed

**State Change**: `template.configured`

**Next Stage**: Document Request

---

#### Stage 2: Document Request
**Origin**: User requests document via FormsPage.tsx

**Data Created**:
- `FormSubmission` record
- `WorkflowInstance` record (if approval required)
- `FeeDemand` record (if fee applicable)

**Data Fields**:
- FormSubmission: formTemplateId, data (JSON), status
- WorkflowInstance: definitionId, entityType, entityId
- FeeDemand: userId, amount, feeHeadId

**Processing**:
- Form submitted with document details
- Workflow initiated if approval required
- Fee demand created if applicable
- User notified of request status

**State Change**: `document.requested` → `document.pending_approval` (if workflow) or `document.pending_generation`

**Next Stage**: Fee Payment (if applicable)

---

#### Stage 3: Fee Payment (if applicable)
**Origin**: User pays document fee via Razorpay

**Data Created**:
- `Payment` record
- `FeeLedger` record

**Data Updated**:
- `FeeDemand` status
- `WorkflowInstance` state

**Processing**:
- Payment processed via Razorpay
- Workflow advanced to next state
- Generation authorized

**State Change**: `document.fee_paid` → `document.pending_generation`

**Next Stage**: Document Generation

---

#### Stage 4: Document Generation
**Origin**: System generates document (automated after approval/payment)

**Data Created**:
- `IssuedDocument` record
- PDF file stored in MinIO

**Data Fields**:
- IssuedDocument: userId, documentTemplateId, filePath, issuedAt, status

**Processing**:
- DocumentsService.generate() retrieves template
- Fetches user/student data
- Replaces placeholders with actual data
- Generates PDF using certificate generator
- Stores PDF in MinIO
- Creates IssuedDocument record
- Applies digital signature if configured

**State Change**: `document.generated` → `document.pending_issuance`

**Next Stage**: Document Issuance

---

#### Stage 5: Document Issuance
**Origin**: Admin verifies and issues document via DocumentsPage.tsx

**Data Updated**:
- `IssuedDocument` status
- Digital signature applied if not already

**Processing**:
- Admin reviews generated document
- Applies official digital signature
- Updates status to "issued"
- Notification sent to user
- Download enabled for user

**State Change**: `document.pending_issuance` → `document.issued`

**Final State**: Document available for user download

---

### Data Relationships

```
DocumentTemplate (1) → (N) IssuedDocument
FormSubmission (1) → (1) WorkflowInstance (if approval)
WorkflowInstance (1) → (1) IssuedDocument (after approval)
User (1) → (N) IssuedDocument
Student (1) → (N) IssuedDocument
IssuedDocument (1) → (1) DocumentTemplate
```

### Key Data Transformations

1. **DocumentTemplate → IssuedDocument**: Template instantiated with user data
2. **FormSubmission → WorkflowInstance**: Request triggers approval process
3. **WorkflowInstance → IssuedDocument**: Approval authorizes generation
4. **User Data → Document Content**: Placeholder replacement
5. **IssuedDocument → PDF File**: Database record linked to MinIO file

### Data Retention Policies

- **DocumentTemplates**: Retained indefinitely (active configurations)
- **IssuedDocuments**: Retained indefinitely for legal/compliance requirements
- **PDF Files**: Retained indefinitely in MinIO
- **FormSubmissions**: Retained for 7+ years for audit
- **WorkflowInstances**: Retained for 7+ years for audit

---

## Attendance Data Lifecycle

### Purpose
Track the complete lifecycle of attendance data from marking to defaulter identification and reporting.

### Lifecycle Stages

#### Stage 1: Attendance Configuration
**Origin**: Admin configures attendance policies via SettingsPage.tsx

**Data Created**:
- `AttendanceConfig` record

**Data Fields**:
- AttendanceConfig: requiredPercentage, workingDays, gracePeriod

**Processing**:
- AttendanceService.configure() saves policies
- Required percentage set (typically 75%)
- Working days configured
- Grace period defined

**State Change**: `attendance.configured`

**Next Stage: Daily Attendance Marking`

---

#### Stage 2: Daily Attendance Marking
**Origin**: Faculty marks attendance via AttendancePage.tsx

**Data Created**:
- `StudentAttendance` records (per student)
- `FacultyAttendance` record (for faculty)

**Data Fields**:
- StudentAttendance: studentId, date, status, markedBy, remarks
- FacultyAttendance: userId, date, status, markedBy

**Processing**:
- AttendanceService.mark() processes attendance
- Status: present/absent/late/excused
- Marked by faculty recorded
- Remarks added if needed
- Real-time validation of duplicate marking

**State Change**: `attendance.marked`

**Next Stage: Attendance Aggregation**

---

#### Stage 3: Attendance Aggregation
**Origin**: System aggregates attendance (scheduled job)

**Data Created**:
- `SubjectAttendanceSummary` records
- Updated `StudentSubjectAttendance` records

**Data Fields**:
- SubjectAttendanceSummary: studentId, batchTermSubjectId, presentCount, totalCount, percentage
- StudentSubjectAttendance: studentId, batchTermSubjectId, attendanceData

**Processing**:
- Scheduled job aggregates daily attendance
- Calculates subject-wise percentages
- Updates cumulative attendance
- Identifies defaulters
- Generates defaulter reports

**State Change**: `attendance.aggregated`

**Next Stage: Defaulter Identification**

---

#### Stage 4: Defaulter Identification
**Origin**: System identifies attendance defaulters

**Data Updated**:
- `Student` records (defaulter flag if applicable)
- Defaulter reports generated

**Processing**:
- Compares attendance against required percentage
- Flags students below threshold
- Generates defaulter lists
- Sends notifications to students
- May result in result hold (if severe)

**State Change**: `defaulter.identified`

**Next Stage: Defaulter Actions**

---

#### Stage 5: Defaulter Actions
**Origin**: System/admin takes action on defaulters

**Data Updated**:
- `ResultHold` records (if attendance affects results)
- Student status updates

**Processing**:
- Result hold applied if attendance critically low
- Student notified of consequences
- Counselling recommended
- Attendance improvement plan created

**State Change**: `defaulter.action_taken`

**Final State**: Attendance record complete with defaulter handling

---

### Data Relationships

```
Student (1) → (N) StudentAttendance
Student (1) → (N) StudentSubjectAttendance
Student (1) → (N) SubjectAttendanceSummary
BatchTermSubject (1) → (N) StudentSubjectAttendance
BatchTermSubject (1) → (N) SubjectAttendanceSummary
User (1) → (N) FacultyAttendance
AttendanceConfig (1) → (N) BatchTermSubject (policy application)
```

### Key Data Transformations

1. **StudentAttendance → SubjectAttendanceSummary**: Daily marks aggregated to subject summary
2. **SubjectAttendanceSummary → Defaulter List**: Percentages compared against threshold
3. **Defaulter List → ResultHold**: Severe defaulters trigger result holds
4. **AttendanceConfig → Attendance Rules**: Configuration applied to marking logic

### Data Retention Policies

- **StudentAttendance**: Retained indefinitely for academic record
- **FacultyAttendance**: Retained for 7+ years for HR records
- **SubjectAttendanceSummary**: Retained indefinitely for transcripts
- **AttendanceConfig**: Retained indefinitely (active policies)
- **Defaulter Reports**: Retained for 7+ years for audit

---

## Academic Result Data Lifecycle

### Purpose
Track the complete lifecycle of academic result data from marks entry to CGPA calculation and transcript generation.

### Lifecycle Stages

#### Stage 1: Marks Entry
**Origin**: Faculty enters marks via ExaminationsPage.tsx

**Data Created**:
- `StudentMarks` records

**Data Fields**:
- StudentMarks: studentId, batchTermSubjectId, marksObtained, marksMax, grade, remarks

**Processing**:
- ExaminationService.gradePaper() processes marks
- Grades assigned based on StreamLabel rules
- Remarks added for feedback
- Validation against maximum marks
- Marks locked after entry period

**State Change**: `marks.entered`

**Next Stage: Result Computation**

---

#### Stage 2: Result Computation
**Origin**: System computes term results via AcademicModule

**Data Created**:
- `StudentTermResult` record
- Updated `StudentCumulativeResult` record

**Data Fields**:
- StudentTermResult: studentId, batchTermId, sgpa, totalCredits, passedSubjects, failedSubjects
- StudentCumulativeResult: studentId, cgpa, totalCredits, overallStatus

**Processing**:
- AcademicService.computeResult() aggregates marks
- Credits calculated per subject
- SGPA computed using grade points
- Pass/fail determined per subject
- CGPA updated with new term
- Result hold applied if applicable

**State Change**: `result.computed` → `result.pending_approval`

**Next Stage: Result Approval**

---

#### Stage 3: Result Approval
**Origin**: Admin approves results via ExaminationsPage.tsx

**Data Updated**:
- `StudentTermResult` status
- `StudentCumulativeResult` status (if final)

**Processing**:
- AcademicService.approveResult() updates status
- Quality checks performed
- Statistical analysis conducted
- Anomalies flagged for review
- Approval logged with auditor

**State Change**: `result.pending_approval` → `result.approved`

**Next Stage: Result Publication**

---

#### Stage 4: Result Publication
**Origin**: Admin publishes results via ExaminationsPage.tsx

**Data Updated**:
- `StudentTermResult` status (published)
- Notifications sent to students

**Processing**:
- AcademicService.publishResult() makes results visible
- Students can view results
- Mark sheets generated
- Parents notified (if configured)
- Revaluation window opened

**State Change**: `result.approved` → `result.published`

**Next Stage: Revaluation (optional)**

---

#### Stage 5: Revaluation Processing
**Origin**: Student applies for revaluation via FormsPage.tsx

**Data Created**:
- `ReAssessmentRequest` record
- Updated `StudentMarks` (if changed)

**Processing**:
- Paper re-evaluated by examiner
- Marks updated if justified
- SGPA/CGPA recalculated if marks changed
- Additional fee charged for revaluation
- Result updated with new marks

**State Change**: `revaluation.requested` → `revaluation.processed`

**Final State**: Results finalized with all revaluations incorporated

---

### Data Relationships

```
Student (1) → (N) StudentMarks
Student (1) → (N) StudentTermResult
Student (1) → (1) StudentCumulativeResult
BatchTermSubject (1) → (N) StudentMarks
BatchTerm (1) → (N) StudentTermResult
StudentMarks (1) → (1) StudentTermResult (aggregation)
StudentTermResult (1) → (1) StudentCumulativeResult (CGPA update)
```

### Key Data Transformations

1. **StudentMarks → StudentTermResult**: Marks aggregated to term result
2. **StudentTermResult → StudentCumulativeResult**: Term results update CGPA
3. **StreamLabel → Grade Assignment**: Academic rules determine grades
4. **ReAssessmentRequest → StudentMarks**: Revaluation updates marks
5. **ResultHold → Result Visibility**: Holds prevent result publication

### Data Retention Policies

- **StudentMarks**: Retained indefinitely for academic record
- **StudentTermResult**: Retained indefinitely for transcripts
- **StudentCumulativeResult**: Retained indefinitely for permanent record
- **ReAssessmentRequest**: Retained for 7+ years for audit
- **ResultHold**: Retained until condition resolved

---

## Library Data Lifecycle

### Purpose
Track the complete lifecycle of library data from book acquisition to circulation and archival.

### Lifecycle Stages

#### Stage 1: Book Acquisition
**Origin**: Librarian adds books via LibraryPage.tsx

**Data Created**:
- `Book` record
- `BookCopy` records (multiple copies)

**Data Fields**:
- Book: isbn, title, author, category, location
- BookCopy: bookId, barcode, status, acquisitionDate

**Processing**:
- LibraryService.addBook() processes addition
- ISBN validation performed
- Barcode generation for each copy
- Location assignment
- Bulk import supported

**State Change**: `book.acquired`

**Next Stage: Book Issue**

---

#### Stage 2: Book Issue
**Origin**: Student borrows book via LibraryPage.tsx

**Data Created**:
- `BookIssue` record

**Data Updated**:
- `BookCopy` status (issued)

**Data Fields**:
- BookIssue: bookCopyId, userId, issueDate, dueDate, status

**Processing**:
- LibraryService.issueBook() validates eligibility
- Checks book availability
- Calculates due date based on loan period
- Updates book copy status
- Creates issue record
- Notification sent to user

**State Change**: `book.issued`

**Next Stage: Book Return**

---

#### Stage 3: Book Return
**Origin**: Student returns book via LibraryPage.tsx

**Data Updated**:
- `BookIssue` record (return date)
- `BookCopy` status (available)
- `FeeDemand` record (if overdue fine)

**Data Fields**:
- BookIssue: returnDate, fineAmount, status
- FeeDemand: userId, amount, feeHeadId (library fine)

**Processing**:
- LibraryService.returnBook() processes return
- Calculates overdue days
- Computes fine amount
- Creates fee demand if fine applicable
- Updates book copy status
- Notifies next in reservation queue

**State Change**: `book.returned`

**Next Stage: Fine Payment (if applicable)**

---

#### Stage 4: Fine Payment
**Origin**: Student pays library fine via FeesPage.tsx

**Data Created**:
- `Payment` record
- `FeeLedger` record

**Data Updated**:
- `FeeDemand` status

**Processing**:
- Fee payment processed
- Fine cleared
- Student borrowing privileges restored

**State Change**: `fine.paid`

**Next Stage: Book Reservation**

---

#### Stage 5: Book Reservation
**Origin**: Student reserves unavailable book via LibraryPage.tsx

**Data Created**:
- `BookReservation` record

**Data Fields**:
- BookReservation: bookCopyId, userId, requestDate, status

**Processing**:
- LibraryService.reserveBook() creates reservation
- Adds to queue for that book
- Sets expiration if configured
- Notifies when book becomes available

**State Change**: `book.reserved`

**Next Stage: Reservation Fulfillment**

---

#### Stage 6: Reservation Fulfillment (Automated)
**Origin**: System processes reservations (daily midnight)

**Data Updated**:
- `BookReservation` records
- `BookCopy` status

**Processing**:
- LibrarySchedulerService processes queue
- Notifies next in queue when available
- Expires old reservations
- Updates reservation status

**State Change**: `reservation.fulfilled` or `reservation.expired`

**Final State**: Book circulation cycle complete

---

### Data Relationships

```
Book (1) → (N) BookCopy
BookCopy (1) → (N) BookIssue
BookCopy (1) → (N) BookReservation
User (1) → (N) BookIssue
User (1) → (N) BookReservation
BookIssue (1) → (1) FeeDemand (if fine)
LibraryConfig (1) → (N) BookCopy (policy application)
```

### Key Data Transformations

1. **Book → BookCopy**: Catalog entry split into physical copies
2. **BookCopy → BookIssue**: Available copy becomes issued
3. **BookIssue → FeeDemand**: Overdue return triggers fine
4. **BookReservation → BookIssue**: Reservation becomes issue when available
5. **LibraryConfig → Circulation Rules**: Policy applied to all operations

### Data Retention Policies

- **Book**: Retained indefinitely (catalog)
- **BookCopy**: Retained indefinitely (inventory)
- **BookIssue**: Retained for 7+ years for audit
- **BookReservation**: Retained for 1 year
- **LibraryConfig**: Retained indefinitely (active policies)

---

## Hostel Data Lifecycle

### Purpose
Track the complete lifecycle of hostel data from room allocation to fee management and vacating.

### Lifecycle Stages

#### Stage 1: Hostel Configuration
**Origin**: Admin configures hostel via HostelPage.tsx

**Data Created**:
- `Hostel` record
- `HostelRoom` records
- `HostelFeeComponent` records

**Data Fields**:
- Hostel: name, wardenUserId, capacity, config
- HostelRoom: hostelId, roomNo, capacity, amenities
- HostelFeeComponent: hostelId, name, amount, type

**Processing**:
- HostelService.configure() creates infrastructure
- Rooms configured with capacity
- Fee components defined (mess, deposit)
- Warden assigned

**State Change**: `hostel.configured`

**Next Stage: Hostel Application**

---

#### Stage 2: Hostel Application
**Origin**: Student applies for hostel via FormsPage.tsx

**Data Created**:
- `HostelRequest` record
- `WorkflowInstance` record
- `FeeDemand` record (security deposit)

**Data Fields**:
- HostelRequest: studentId, preferences, status
- WorkflowInstance: definitionId, entityType, entityId
- FeeDemand: userId, amount, feeHeadId (security deposit)

**Processing**:
- Workflow processes hostel request
- Security deposit demand created
- Routed to warden for review

**State Change**: `hostel.requested` → `hostel.pending_approval`

**Next Stage: Room Allocation**

---

#### Stage 3: Room Allocation
**Origin**: Warden allocates room via MyTasksPage.tsx

**Data Created**:
- `HostelAllocation` record

**Data Updated**:
- `HostelRequest` status
- `HostelRoom` occupancy
- `WorkflowInstance` state

**Data Fields**:
- HostelAllocation: studentId, hostelRoomId, allocatedAt, status
- HostelRoom: currentOccupancy

**Processing**:
- Workflow approves request
- Room assigned based on preferences
- Occupancy updated
- Mess fee billing initiated
- Student notified

**State Change**: `hostel.allocated`

**Next Stage: Hostel Fee Billing**

---

#### Stage 4: Hostel Fee Billing
**Origin**: System bills hostel fees (recurring)

**Data Created**:
- `FeeDemand` records (mess fees)

**Data Fields**:
- FeeDemand: userId, amount, feeHeadId, dueDate, recurrence

**Processing**:
- RecurringBillingService runs daily
- Mess fees billed monthly
- Pro-rating applied for mid-term joining
- Concessions applied if applicable

**State Change**: `hostel.fee_billed`

**Next Stage: Fee Payment**

---

#### Stage 5: Fee Payment
**Origin**: Student pays hostel fees via FeesPage.tsx

**Data Created**:
- `Payment` record
- `FeeLedger` record

**Data Updated**:
- `FeeDemand` status

**Processing**:
- Payment processed via Razorpay
- Fee ledger updated
- Receipt generated

**State Change**: `hostel.fee_paid`

**Next Stage: Vacating Request**

---

#### Stage 6: Vacating Request
**Origin**: Student requests to vacate via HostelPage.tsx

**Data Created**:
- `HostelRefundRequest` record
- `WorkflowInstance` record

**Data Fields**:
- HostelRefundRequest: studentId, hostelAllocationId, amount, bankDetails, status

**Processing**:
- Refund request workflow initiated
- Room condition verified
- Deductions calculated (damages, etc.)
- Refund amount determined

**State Change**: `hostel.vacating_requested` → `hostel.pending_refund_approval`

**Next Stage: Refund Processing**

---

#### Stage 7: Refund Processing
**Origin**: Warden approves refund via MyTasksPage.tsx

**Data Created**:
- `Payment` record (refund)
- `FeeLedger` record (credit)

**Data Updated**:
- `HostelRefundRequest` status
- `HostelAllocation` status
- `HostelRoom` occupancy

**Processing**:
- Workflow approves refund
- Room vacated
- Occupancy reduced
- Refund processed
- Notification sent

**State Change**: `hostel.refund_processed`

**Final State**: Hostel allocation cycle complete

---

### Data Relationships

```
Hostel (1) → (N) HostelRoom
Hostel (1) → (N) HostelFeeComponent
HostelRoom (1) → (N) HostelAllocation
HostelRoom (1) → (1) User (warden)
HostelAllocation (1) → (1) Student
HostelAllocation (1) → (1) HostelRefundRequest
HostelFeeComponent (1) → (N) FeeDemand
HostelRequest (1) → (1) WorkflowInstance
```

### Key Data Transformations

1. **HostelRequest → HostelAllocation**: Approved request becomes allocation
2. **HostelAllocation → FeeDemand**: Allocation triggers recurring billing
3. **HostelAllocation → HostelRefundRequest**: Vacating triggers refund process
4. **HostelRefundRequest → Payment**: Approved refund becomes payment
5. **HostelRoom Occupancy**: Updated on allocation and vacating

### Data Retention Policies

- **Hostel**: Retained indefinitely (infrastructure)
- **HostelRoom**: Retained indefinitely (inventory)
- **HostelAllocation**: Retained for 7+ years for audit
- **HostelRequest**: Retained for 7+ years for audit
- **HostelRefundRequest**: Retained for 7+ years for audit
- **HostelFeeComponent**: Retained indefinitely (active configuration)

---

## Notification Data Lifecycle

### Purpose
Track the complete lifecycle of notification data from creation to delivery and archival.

### Lifecycle Stages

#### Stage 1: Notification Creation
**Origin**: System event triggers notification

**Data Created**:
- `Notification` record
- `NotificationLog` records (per channel)

**Data Fields**:
- Notification: userId, title, body, type, status, entityType, entityId
- NotificationLog: notificationId, channel, status, sentAt, error

**Processing**:
- NotificationsService.create() creates notification
- Linked to triggering entity (user, workflow, etc.)
- Type determined (info, warning, alert, etc.)
- Multi-channel delivery configured

**State Change**: `notification.created`

**Next Stage: Channel Delivery**

---

#### Stage 2: Channel Delivery
**Origin**: System delivers notification via channels

**Data Created**:
- `NotificationLog` records (in-app, email, SMS)

**Data Fields**:
- NotificationLog: channel (in-app, email, sms), status, sentAt, error

**Processing**:
- In-app: Stored in database, visible in UI
- Email: Sent via EmailService, SMTP delivery
- SMS: Sent via SmsService, gateway delivery
- Template rendering if configured
- Retry logic for failed deliveries

**State Change**: `notification.delivered` or `notification.failed`

**Next Stage: User Interaction**

---

#### Stage 3: User Interaction
**Origin**: User views/dismisses notification

**Data Updated**:
- `Notification` status (read/dismissed)

**Processing**:
- User views notification in UI
- Status updated to "read"
- User can dismiss notification
- Read notifications archived after period

**State Change**: `notification.read` → `notification.archived`

**Final State**: Notification lifecycle complete

---

### Data Relationships

```
User (1) → (N) Notification
Notification (1) → (N) NotificationLog
WorkflowInstance (1) → (N) Notification (triggered)
MessageTemplate (1) → (N) Notification (rendered)
```

### Key Data Transformations

1. **System Event → Notification**: Event triggers notification creation
2. **Notification → NotificationLog**: Single notification split by channel
3. **MessageTemplate → Notification**: Template rendered with variables
4. **NotificationLog → External Delivery**: Log tracks delivery to email/SMS

### Data Retention Policies

- **Notification**: Retained for 90 days, then archived
- **NotificationLog**: Retained for 1 year for delivery audit
- **MessageTemplate**: Retained indefinitely (active configurations)

---

## Summary

This UniversityERP system manages complex data lifecycles across multiple domains:

**Key Characteristics:**

1. **Multi-Stage Workflows**: Most data goes through multiple stages with state transitions
2. **Audit Trails**: Every data change is logged for accountability
3. **Workflow Integration**: Many processes use the workflow engine for approvals
4. **Automated Processing**: Scheduled jobs process data at regular intervals
5. **Data Relationships**: Complex relationships between entities support business processes
6. **Retention Policies**: Different data types have different retention requirements
7. **Archival Strategy**: Active data vs. historical data vs. archived data

**Data Flow Patterns:**

- **Creation → Processing → Approval → Finalization** (common workflow pattern)
- **Configuration → Demand Generation → Payment → Record** (financial pattern)
- **Entry → Aggregation → Analysis → Reporting** (analytical pattern)
- **Request → Approval → Action → Completion** (approval pattern)

**State Management:**

- Every major entity has status fields tracking lifecycle stage
- State transitions trigger business logic and notifications
- Terminal states represent completion (approved, rejected, completed, etc.)
- Some entities support re-opening (revaluation, refund requests)

**Integration Points:**

- Workflow engine coordinates multi-step processes
- Payment gateway handles financial transactions
- Notification system keeps stakeholders informed
- Scheduler automates recurring operations
- Audit system tracks all changes

This comprehensive data lifecycle management ensures data integrity, process visibility, and accountability across the entire UniversityERP system.

---

**Document Version**: 1.0  
**Last Updated**: 2025-08-05



---


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



---


# Module-by-Module Directory

## Overview
This document provides an exhaustive index and detailed reference for all **38 domain modules** implemented in `apps/core-api/src/modules/`. Each section details the module's business purpose, key backend controllers and services, database models, frontend UI pages, permissions, and operational status.

---

## Complete Module Reference

### 1. Academic Module (`apps/core-api/src/modules/academic`)
- **Business Purpose**: Manages academic programs, batches, sections, terms, and elective subject pooling. Enforces versioned academic rules via immutable `StreamLabel` and `SubjectLabel` snapshots.
- **Key Backend Files**: `academic.controller.ts`, `academic.service.ts`, `stream-label.service.ts`, `subject-pool.service.ts`
- **Database Models**: `Program`, `Batch`, `Section`, `Term`, `Subject`, `StreamLabel`, `SubjectLabel`, `SubjectPool`, `StudentElectiveChoice`
- **Frontend Pages**: `MasterDataPage.tsx`, `ElectivesPage.tsx`
- **Status**: **Fully Operational**

---

### 2. Admissions Module (`apps/core-api/src/modules/admissions`)
- **Business Purpose**: Handles student application processing, document verification, merit list generation, and seat allocation.
- **Key Backend Files**: `admissions.controller.ts`, `admissions.service.ts`, `merit-list.service.ts`
- **Database Models**: `ApplicationForm`, `FormSubmission`, `MeritList`, `MeritListCandidate`, `AdmissionSeat`
- **Frontend Pages**: `AdmissionsPage.tsx`, `StudentApplicationsPage.tsx`, `MeritListPage.tsx`
- **Status**: **Fully Operational**

---

### 3. Analytics Module (`apps/core-api/src/modules/analytics`)
- **Business Purpose**: Provides system-wide dashboard metrics, enrollment trends, revenue reports, exam performance statistics, and user activity analytics.
- **Key Backend Files**: `analytics.controller.ts`, `analytics.service.ts`
- **Database Models**: Aggregates data from `User`, `FeeDemand`, `ExamResult`, `AttendanceRecord`
- **Frontend Pages**: `AnalyticsPage.tsx`, `DashboardPage.tsx`
- **Status**: **Fully Operational**

---

### 4. Attendance Module (`apps/core-api/src/modules/attendance`)
- **Business Purpose**: Tracks daily and session-wise attendance for students and staff; calculates attendance percentages and generates eligibility flags for examinations.
- **Key Backend Files**: `attendance.controller.ts`, `attendance.service.ts`
- **Database Models**: `AttendanceRecord`, `AttendanceSession`, `StudentAttendanceSummary`
- **Frontend Pages**: `AttendancePage.tsx`
- **Status**: **Fully Operational**

---

### 5. Audit Module (`apps/core-api/src/modules/audit`)
- **Business Purpose**: Tracks all database write operations (create, update, delete) across the system, storing before-and-after JSON diffs for security compliance and governance.
- **Key Backend Files**: `audit.controller.ts`, `audit.service.ts`, `audit-middleware.ts`
- **Database Models**: `AuditLog`
- **Frontend Pages**: `AuditLogPage.tsx`
- **Status**: **Fully Operational**

---

### 6. Auth Module (`apps/core-api/src/modules/auth`)
- **Business Purpose**: Manages authentication, JWT token generation, refresh tokens, password hashing, OTP verification, initial account setup, and password reset flows.
- **Key Backend Files**: `auth.controller.ts`, `auth.service.ts`, `jwt.strategy.ts`
- **Database Models**: `User`, `MobileOtp`, `PasswordHistory`, `RegistrationRequest`
- **Frontend Pages**: `LoginPage.tsx`, `RegisterPage.tsx`, `ForgotPasswordPage.tsx`, `ResetPasswordPage.tsx`, `SetupAccountPage.tsx`
- **Status**: **Fully Operational**

---

### 7. Backup Module (`apps/core-api/src/modules/backup`)
- **Business Purpose**: Triggers PostgreSQL database dumps (`pg_dump`), compresses archives, uploads backups to MinIO object storage, verifies backup integrity, and coordinates database restore operations.
- **Key Backend Files**: `backup.controller.ts`, `backup.service.ts`
- **Database Models**: `BackupRecord`
- **Frontend Pages**: `SettingsPage.tsx` (Backup Tab)
- **Status**: **Fully Operational**

---

### 8. Banners Module (`apps/core-api/src/modules/banners`)
- **Business Purpose**: Manages system login banners, promotional announcements, and emergency broadcast messages displayed on the login page or user dashboards.
- **Key Backend Files**: `banners.controller.ts`, `banners.service.ts`
- **Database Models**: `Banner`
- **Frontend Pages**: `BannersPage.tsx`
- **Status**: **Fully Operational**

---

### 9. Branding Module (`apps/core-api/src/modules/branding`)
- **Business Purpose**: Customizes university and institute visual themes, including logos, login cover images, primary/secondary color schemes, and header titles.
- **Key Backend Files**: `branding.controller.ts`, `branding.service.ts`
- **Database Models**: `University` (branding field), `Institute` (branding field)
- **Frontend Pages**: `SettingsPage.tsx` (Branding Tab)
- **Status**: **Fully Operational**

---

### 10. Counselling Module (`apps/core-api/src/modules/counselling`)
- **Business Purpose**: Manages student counselling sessions, advisor assignments, slot scheduling, confidential meeting notes, and follow-up tracking.
- **Key Backend Files**: `counselling.controller.ts`, `counselling.service.ts`
- **Database Models**: `CounsellorProfile`, `CounsellingSlot`, `CounsellingAppointment`, `CounsellingNote`
- **Frontend Pages**: `CounsellingAdminPage.tsx`, `CounsellingDeskPage.tsx`
- **Status**: **Fully Operational**

---

### 11. Directory Module (`apps/core-api/src/modules/directory`)
- **Business Purpose**: Provides a searchable university staff and student directory with contact cards, department listings, and role hierarchies.
- **Key Backend Files**: `directory.controller.ts`, `directory.service.ts`
- **Database Models**: `User`, `StaffProfile`, `StudentProfile`
- **Frontend Pages**: `DirectoryPage.tsx`
- **Status**: **Fully Operational**

---

### 12. Documents Module (`apps/core-api/src/modules/documents`)
- **Business Purpose**: Renders, compiles, and issues official PDF documents including hall tickets, bonafide certificates, grade transcripts, fee receipts, and staff leave letters.
- **Key Backend Files**: `documents.controller.ts`, `documents.service.ts`, `render.ts`, `field-catalog.ts`
- **Database Models**: `DocumentTemplate`, `GeneratedDocument`
- **Frontend Pages**: `DocumentsPage.tsx`
- **Status**: **Fully Operational**

---

### 13. Examination Module (`apps/core-api/src/modules/examination`)
- **Business Purpose**: Manages offline and online Computer-Based Exams (CBE), exam paper creation, hall ticket generation, AI webcam proctoring, question challenges, grade calculations (SGPA/CGPA), and marksheets.
- **Key Backend Files**: `examination.controller.ts`, `examination.service.ts`, `exam-scheduler.service.ts`
- **Database Models**: `ExamSchedule`, `ExamPaper`, `ExamAttempt`, `ExamProctorLog`, `QuestionChallenge`, `ExamResult`
- **Frontend Pages**: `ExaminationsPage.tsx`, `ExamTakePage.tsx`, `ExamMonitorPage.tsx`, `ExamItemAnalysisPage.tsx`, `MyInvigilationPage.tsx`
- **Status**: **Fully Operational**

---

### 14. Fee Module (`apps/core-api/src/modules/fee`)
- **Business Purpose**: Handles fee structure definition, head-wise billing, daily automated recurring billing (2 AM cron), Razorpay online payment integration, scholarships, concessions, government reimbursements, and deposit refunds.
- **Key Backend Files**: `fee.controller.ts`, `fee.service.ts`, `recurring-billing.service.ts`, `program-deposit-refund.service.ts`
- **Database Models**: `FeeHead`, `FeeStructure`, `FeeDemand`, `FeeLedger`, `Payment`, `Scholarship`, `DepositRefund`
- **Frontend Pages**: `FeesPage.tsx`, `ProgramFeeManager.tsx`, `ResourceFeeManager.tsx`
- **Status**: **Fully Operational**

---

### 15. Forms Module (`apps/core-api/src/modules/forms`)
- **Business Purpose**: Dynamic form builder enabling admins to create custom application forms, surveys, and feedback questionnaires with field validation and submission tracking.
- **Key Backend Files**: `forms.controller.ts`, `forms.service.ts`
- **Database Models**: `FormTemplate`, `FormSubmission`
- **Frontend Pages**: `FormsPage.tsx`
- **Status**: **Fully Operational**

---

### 16. Hostel Module (`apps/core-api/src/modules/hostel`)
- **Business Purpose**: Manages hostel blocks, room allocations, bed capacity, mess fee billing, gate pass approvals, warden assignments, and security deposit management.
- **Key Backend Files**: `hostel.controller.ts`, `hostel.service.ts`
- **Database Models**: `HostelBlock`, `HostelRoom`, `HostelBed`, `HostelAllocation`, `HostelGatePass`
- **Frontend Pages**: `HostelPage.tsx`
- **Status**: **Fully Operational**

---

### 17. HR Module (`apps/core-api/src/modules/hr`)
- **Business Purpose**: Oversees staff onboarding, employee profiles, leave types, leave requests, approval hierarchies, and leave balance tracking.
- **Key Backend Files**: `hr.controller.ts`, `hr.service.ts`, `leave.service.ts`
- **Database Models**: `StaffProfile`, `LeaveType`, `LeaveRequest`, `LeaveBalance`
- **Frontend Pages**: `HRPage.tsx`, `LeaveRequestsPage.tsx`
- **Status**: **Fully Operational**

---

### 18. ID Format Module (`apps/core-api/src/modules/id-format`)
- **Business Purpose**: Configures customizable auto-numbering formats for student enrollment numbers, staff IDs, fee receipt numbers, application numbers, and exam roll numbers.
- **Key Backend Files**: `id-format.controller.ts`, `id-format.service.ts`
- **Database Models**: `IdFormatConfig`
- **Frontend Pages**: `IdFormatsPage.tsx`
- **Status**: **Fully Operational**

---

### 19. Library Module (`apps/core-api/src/modules/library`)
- **Business Purpose**: Manages book cataloging, circulation (issue/return), digital book reservations, automated reservation cleanup cron (midnight), and library fine generation.
- **Key Backend Files**: `library.controller.ts`, `library.service.ts`
- **Database Models**: `Book`, `BookCopy`, `BookLoan`, `BookReservation`, `LibraryFine`
- **Frontend Pages**: `LibraryPage.tsx`
- **Status**: **Fully Operational**

---

### 20. Master Data Module (`apps/core-api/src/modules/master-data`)
- **Business Purpose**: Central repository for university structure setup, institute creation, department setup, academic year definitions, and global lookup tables.
- **Key Backend Files**: `master-data.controller.ts`, `master-data.service.ts`
- **Database Models**: `University`, `Institute`, `Department`, `UniversityDepartment`, `AcademicYear`
- **Frontend Pages**: `MasterDataPage.tsx`
- **Status**: **Fully Operational**

---

### 21. Notice Board Module (`apps/core-api/src/modules/notice-board`)
- **Business Purpose**: Enables faculty and admins to publish official notices with target audience filters (by institute/dept/role), attachment links, and automated expiry tracking.
- **Key Backend Files**: `notice-board.controller.ts`, `notice-board.service.ts`
- **Database Models**: `Notice`
- **Frontend Pages**: `NoticeBoardPage.tsx`
- **Status**: **Fully Operational**

---

### 22. Notifications Module (`apps/core-api/src/modules/notifications`)
- **Business Purpose**: Dispatches in-app, email, and SMS notifications; manages notification templates, delivery logs, and user preference settings.
- **Key Backend Files**: `notifications.controller.ts`, `notifications.service.ts`
- **Database Models**: `Notification`, `NotificationTemplate`, `NotificationLog`
- **Frontend Pages**: Integrated into top navigation bar and user profile preferences
- **Status**: **Fully Operational**

---

### 23. Onboarding Module (`apps/core-api/src/modules/onboarding`)
- **Business Purpose**: Manages multi-step onboarding workflows for newly admitted students and new staff members, including document uploads and profile verification.
- **Key Backend Files**: `onboarding.controller.ts`, `onboarding.service.ts`
- **Database Models**: `OnboardingStep`, `StudentOnboardingProgress`
- **Frontend Pages**: `OnboardStudentsPage.tsx`
- **Status**: **Fully Operational**

---

### 24. Parent Portal Module (`apps/core-api/src/modules/parent-portal`)
- **Business Purpose**: Grants parents or guardians read-only visibility into their ward's academic marks, attendance percentage, fee demand status, and official university notices.
- **Key Backend Files**: `parent-portal.controller.ts`, `parent-portal.service.ts`
- **Database Models**: `ParentMapping`
- **Frontend Pages**: `StudentProfilePage.tsx` (Parent View)
- **Status**: **Fully Operational**

---

### 25. Question Bank Module (`apps/core-api/src/modules/question-bank`)
- **Business Purpose**: Repository for managing subject-wise question banks, question categories, difficulty levels, multiple-choice options, and numerical answer keys.
- **Key Backend Files**: `question-bank.controller.ts`, `question-bank.service.ts`
- **Database Models**: `Question`, `QuestionOption`, `QuestionCategory`
- **Frontend Pages**: `ExaminationsPage.tsx` (Question Bank Tab)
- **Status**: **Fully Operational**

---

### 26. Resource Optimisation Module (`apps/core-api/src/modules/resource-optimisation`)
- **Business Purpose**: Analyzes classroom, lab, and faculty utilization rates to provide optimization recommendations and prevent scheduling bottlenecks.
- **Key Backend Files**: `resource-optimisation.controller.ts`, `resource-optimisation.service.ts`
- **Database Models**: Analyzes `ScheduleRun`, `TimetableSlot`, `InstituteResource`
- **Frontend Pages**: `AnalyticsPage.tsx`
- **Status**: **Fully Operational**

---

### 27. Resource Reservation Module (`apps/core-api/src/modules/resource-reservation`)
- **Business Purpose**: Booking system for generic institute resources (auditoriums, labs, project rooms, sports facilities) with availability checks and approval workflows.
- **Key Backend Files**: `resource-reservation.controller.ts`, `resource-reservation.service.ts`
- **Database Models**: `InstituteResource`, `InstituteResourceType`, `ResourceReservation`
- **Frontend Pages**: `ResourceFeeManager.tsx`
- **Status**: **Fully Operational**

---

### 28. Roles Module (`apps/core-api/src/modules/roles`)
- **Business Purpose**: Defines custom functional roles, permission matrices, and scope assignments (university, institute, or department-level).
- **Key Backend Files**: `roles.controller.ts`, `roles.service.ts`
- **Database Models**: `Role`, `Permission`, `UserRole`
- **Frontend Pages**: `SettingsPage.tsx` (Roles Tab)
- **Status**: **Fully Operational**

---

### 29. Settings Module (`apps/core-api/src/modules/settings`)
- **Business Purpose**: Controls system-wide configurations, module access toggles, email/SMS gateway credentials, password security rules, and integration settings.
- **Key Backend Files**: `settings.controller.ts`, `settings.service.ts`
- **Database Models**: `SystemSetting`, `ModuleAccess`
- **Frontend Pages**: `SettingsPage.tsx`
- **Status**: **Fully Operational**

---

### 30. Social Monitoring Module (`apps/core-api/src/modules/social-monitoring`)
- **Business Purpose**: Monitors institutional social media mention channels and public sentiment feeds for brand reputation management.
- **Key Backend Files**: `social-monitoring.controller.ts`, `social-monitoring.service.ts`
- **Database Models**: `SocialMention`, `SocialSentimentLog`
- **Frontend Pages**: `AnalyticsPage.tsx`
- **Status**: **Fully Operational**

---

### 31. Staff-Subject Module (`apps/core-api/src/modules/staff-subject`)
- **Business Purpose**: Assigns teaching faculty to specific course subjects, sections, and academic terms; feeds directly into timetable scheduling and grading permissions.
- **Key Backend Files**: `staff-subject.controller.ts`, `staff-subject.service.ts`
- **Database Models**: `StaffSubjectAssignment`
- **Frontend Pages**: `HRPage.tsx`, `TimetablePage.tsx`
- **Status**: **Fully Operational**

---

### 32. Student Profile Module (`apps/core-api/src/modules/student-profile`)
- **Business Purpose**: Central repository for student academic records, personal information, emergency contacts, stream label history, fee ledger, and transcript history.
- **Key Backend Files**: `student-profile.controller.ts`, `student-profile.service.ts`
- **Database Models**: `StudentProfile`, `User`
- **Frontend Pages**: `StudentProfilePage.tsx`
- **Status**: **Fully Operational**

---

### 33. Timetable Module (`apps/core-api/src/modules/timetable`)
- **Business Purpose**: Automates class timetable generation using constraint satisfaction algorithms; detects faculty and classroom double-bookings; handles manual slot adjustments.
- **Key Backend Files**: `timetable.controller.ts`, `timetable.service.ts`
- **Database Models**: `TimetableSlot`, `ScheduleRun`
- **Frontend Pages**: `TimetablePage.tsx`
- **Status**: **Fully Operational**

---

### 34. Transport Module (`apps/core-api/src/modules/transport`)
- **Business Purpose**: Manages transport routes, bus stops, vehicle fleets, driver assignments, bus pass generation, and transport fee demands.
- **Key Backend Files**: `transport.controller.ts`, `transport.service.ts`
- **Database Models**: `TransportRoute`, `TransportStop`, `TransportVehicle`, `TransportPass`
- **Frontend Pages**: `TransportPage.tsx`
- **Status**: **Fully Operational**

---

### 35. Upload Module (`apps/core-api/src/modules/upload`)
- **Business Purpose**: Handles multi-part file uploads, mime-type validation, virus checks, and storage dispatch to MinIO S3 buckets with pre-signed retrieval URLs.
- **Key Backend Files**: `upload.controller.ts`, `upload.service.ts`
- **Database Models**: Stores metadata across entity attachments
- **Frontend Pages**: Integrated across all form upload components
- **Status**: **Fully Operational**

---

### 36. Users Module (`apps/core-api/src/modules/users`)
- **Business Purpose**: CRUD operations for user accounts, account activation/deactivation, password resets, profile updates, and bulk user imports via CSV/Excel.
- **Key Backend Files**: `users.controller.ts`, `users.service.ts`
- **Database Models**: `User`, `UserRole`
- **Frontend Pages**: `UserManagementPage.tsx`
- **Status**: **Fully Operational**

---

### 37. Validation Module (`apps/core-api/src/modules/validation`)
- **Business Purpose**: Validates data integrity before batch operations, checks prerequisite subject completions, and verifies document authenticity via digital signatures.
- **Key Backend Files**: `validation.controller.ts`, `validation.service.ts`
- **Database Models**: Evaluates domain entities
- **Frontend Pages**: `ValidationPage.tsx`
- **Status**: **Fully Operational**

---

### 38. Workflow Module (`apps/core-api/src/modules/workflow`)
- **Business Purpose**: Visual workflow engine supporting multi-step approval processes, dynamic actor resolution, payment gate holds (Razorpay), resource holds (Saga pattern), and workflow step execution.
- **Key Backend Files**: `workflow-engine.service.ts`, `workflow-definition.service.ts`, `workflow-payment.service.ts`, `workflow-scheduler.service.ts`, `reservation.service.ts`
- **Database Models**: `WorkflowDefinition`, `WorkflowState`, `WorkflowTransition`, `WorkflowInstance`, `WorkflowStepInstance`, `WorkflowHold`
- **Frontend Pages**: `WorkflowDesignerPage.tsx`, `WorkflowMonitorPage.tsx`, `MyTasksPage.tsx`
- **Status**: **Fully Operational**



---



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



---


# Incomplete, Missing & System Limitation Audit

## Purpose
This document provides a transparent, zero-assumption audit of system areas that are partially implemented, stubbed out, or architecturally consolidated. Grounded strictly in empirical codebase inspection, this report establishes what is production-ready versus what remains work-in-progress.

---

## Codebase Audit Summary

| Component / Feature Area | Declared Architecture | Empirical Codebase Finding | Operational Impact | Recommended Path Forward |
| :--- | :--- | :--- | :--- | :--- |
| **Student Portal Frontend** | `web/student-portal` | Package exists, but `src/pages` is an empty directory. | All student workflows (exam taking, fee payment, registration) run inside `web/admin-portal`. | Maintain single SPA or extract student routes to `web/student-portal`. |
| **CBE Microservice Engine** | `apps/cbe-engine` | Basic NestJS scaffolding stub (`ConfigModule` only). | All CBE exam logic, proctoring, and question paper generation are served by `core-api/src/modules/examination`. | Keep in `core-api` or complete microservice extraction. |
| **Certificate Generator Service** | `apps/cert-generator` | Basic NestJS scaffolding stub (`ConfigModule` only). | PDF generation is executed inside `core-api/src/modules/documents` using Handlebars and PDFKit. | Keep in `core-api` or complete microservice extraction. |
| **Notification Worker Service** | `apps/notification-worker` | Basic NestJS scaffolding stub (`ConfigModule` only). | Notifications are dispatched inside `core-api/src/modules/notifications` via Redis/Bull queues. | Keep in `core-api` or complete microservice extraction. |
| **Shared Libraries** | `libs/` | Folder exists, but contains no packages or code. | Code models and types are managed locally within `apps/core-api` and `web/admin-portal`. | Populate `libs/` with shared TypeScript interfaces. |
| **Parent Portal App** | Dedicated Parent Mobile/Web App | Backend endpoints exist (`ParentPortalModule`), but UI is served via `StudentProfilePage.tsx`. | Parents view ward data through `admin-portal` using assigned parent roles. | Build dedicated parent dashboard or mobile client. |

---

## Detailed System Findings

### 1. Monolithic Realization vs Microservice Intent
The project repository contains multiple application folders under `apps/` (`cbe-engine`, `cert-generator`, `notification-worker`). Inspection of `main.ts` and `app.module.ts` in those subdirectories confirms they contain minimal NestJS boilerplate without domain controllers or services. 

All domain features—including online examination proctoring, PDF compilation, and notification queues—are fully implemented and operational inside **`apps/core-api`**.

> **Takeaway**: The system is an operational **modular monolith**. The extra folders represent future microservice targets.

### 2. Single Frontend Portal Architecture
The repository structure suggests a split between `web/admin-portal` and `web/student-portal`. However, `web/student-portal/src/pages` is currently empty. 

All 45 frontend pages—handling administrative setup, faculty grading, librarian cataloging, accountant ledger management, as well as **student exam taking (`ExamTakePage.tsx`)** and **student fee payment (`FeesPage.tsx`)**—are contained inside `web/admin-portal`.

> **Takeaway**: System access is unified under `web/admin-portal`. Navigation and page routes are rendered dynamically based on the user's active role.

### 3. Verification & Automated Test Coverage
While core API contracts and Prisma migrations are strictly defined, automated test suites (Jest unit tests or Cypress/Playwright E2E tests) are sparse across backend modules. Reliability currently relies on NestJS compile-time type safety, Prisma schema validation, and manual verification pipelines.

---

## Known Workarounds & Architectural Guidelines

1. **Deployment Simplicity**: Deploying `apps/core-api` and `web/admin-portal` is sufficient to run 100% of implemented system capabilities.
2. **Role-Based Access Control**: Ensure `ModuleAccess` and `Role` configurations are properly seeded to ensure students only see student-relevant pages inside `admin-portal`.


---

# UniversityERP - Single Source of Truth Documentation Repository

Welcome to the official, complete knowledge repository for **UniversityERP**. This documentation suite has been engineered directly from a comprehensive reverse-engineering audit of the codebase to provide an exhaustive, zero-assumption single source of truth for the entire product.

---

## Documentation Navigation Hub

This repository is organized into **8 core knowledge documents**, each addressing a specific domain of the application:

```
APPLICATION_KNOWLEDGE_DOCUMENTATION/
├── README.md                                    # Master Navigation & Repository Map (This Document)
├── 00_APPLICATION_OVERVIEW.md                   # High-Level Product Purpose, System Architecture & Principles
├── 01_BUSINESS_PROCESSES.md                     # Step-by-Step Real-World End-to-End Workflows (12 Processes)
├── 02_USER_JOURNEYS.md                          # Role-Based Experiences & Journeys for 12 User Roles
├── 03_DATA_FLOW_AND_LIFECYCLE.md                # Data Lifecycles, Origin, Mutations, and Transformations
├── 04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md # Technical Infrastructure, Security Guards, Crons & Microservices
├── 05_MODULE_BY_MODULE_DIRECTORY.md             # Detailed Guide for all 38 NestJS Modules in Core API
├── 06_API_AND_DATABASE_REFERENCE.md             # 100+ Database Tables, Schema Models, Enums & REST API Rules
└── 07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md # Audit of Incomplete Flows, Stubs & System Limitations
```

---

## Quick Reference by Stakeholder Role

| Role | Recommended Starting Point | Key Insights Gained |
| :--- | :--- | :--- |
| **Product Manager / Business Analyst** | [`00_APPLICATION_OVERVIEW.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/00_APPLICATION_OVERVIEW.md) & [`01_BUSINESS_PROCESSES.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/01_BUSINESS_PROCESSES.md) | High-level business domains, fee billing workflows, admission pipelines, and examination rules. |
| **QA & Test Engineers** | [`01_BUSINESS_PROCESSES.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/01_BUSINESS_PROCESSES.md) & [`02_USER_JOURNEYS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/02_USER_JOURNEYS.md) | Exact step-by-step user actions, screen transitions, expected database state changes, and edge cases. |
| **Software Engineers & Architects** | [`04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md) & [`05_MODULE_BY_MODULE_DIRECTORY.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/05_MODULE_BY_MODULE_DIRECTORY.md) | NestJS guard execution pipelines, Prisma middleware diffing, Redis/Bull queue wiring, and module breakdowns. |
| **Database Administrators (DBAs)** | [`03_DATA_FLOW_AND_LIFECYCLE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/03_DATA_FLOW_AND_LIFECYCLE.md) & [`06_API_AND_DATABASE_REFERENCE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/06_API_AND_DATABASE_REFERENCE.md) | 100+ Prisma models, foreign key dependencies, field-level audit log structures, and transactional flows. |
| **DevOps & Infrastructure Leads** | [`04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md) & [`07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md) | Service deployment realities (`core-api` monolith vs microservices stubs), MinIO storage, and background crons. |

---

## Default System Credentials & Setup Quick Start

- **Default University**: SlashCurate University (`slashcurate.edu`)
- **SuperAdmin Email**: `erpsupport@slashcurate.com`
- **Default Password**: `Admin@1234` (requires mandatory password change upon initial login)
- **Primary Backend API**: `http://localhost:3000/api/v1`
- **Admin Portal UI**: `http://localhost:5173`
- **Swagger Documentation**: `http://localhost:3000/api/docs` (Non-production environments)

---

## Key System Highlights

1. **Versioned Academic Rules**: Student enrollments are tied to immutable `StreamLabel` snapshots so curriculum updates never invalidate ongoing student batches.
2. **Generic Approval Workflows**: Visual workflow builder supporting multi-actor routing, Razorpay payment holds, and resource reservations using the Saga pattern.
3. **Computer-Based Examination (CBE)**: Full online examination platform featuring AI webcam proctoring, tab-switch monitoring, screen locking, and post-exam question challenge processing.
4. **Daily Recurring Billing**: Automated 2:00 AM cron generating head-wise fee demands per term for all active student enrollments.


---
