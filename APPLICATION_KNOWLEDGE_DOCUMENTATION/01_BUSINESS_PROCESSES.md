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
