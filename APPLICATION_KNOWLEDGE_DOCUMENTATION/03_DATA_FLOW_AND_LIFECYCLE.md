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
