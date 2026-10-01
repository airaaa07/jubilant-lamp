# Master Database Schema & Relational Entity Dictionary
## Exhaustive Technical Reference for all 138 Prisma Models in UniversityERP

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-DB-DATA-DICTIONARY-V4.2
CLASSIFICATION: TECHNICAL REFERENCE & SYSTEM DATABASE SPECIFICATION
AUTHORITY: PRINCIPAL DATABASE ARCHITECT & CHIEF DATA OFFICER
ENGINE: POSTGRESQL 16 / PRISMA ORM 5.x / 138 RELATIONAL MODELS
========================================================================================================================
```

---

## Executive Overview: The Unified Relational Continuum

The persistence layer of **UniversityERP** consists of **138 relational models** managed via Prisma ORM on a clustered PostgreSQL 16 database. Unlike fragmented campus databases where admissions, fees, attendance, and examinations reside in disconnected tables or silos, UniversityERP models the institutional continuum with strict referential integrity, foreign key cascades, unique constraints, and performance indexes.

```
+--------------------------------------------------------------------------------------------------------------------+
|                                    138 PRISMA MODELS: DOMAIN CLUSTER BREAKDOWN                                     |
+--------------------------------------------------------------------------------------------------------------------+
  01. Multi-Tenant Core, Identity & Security     │ 11 Models (University, Institute, User, RefreshToken, Roles...)
  02. Institutional Hierarchy & Master Catalog   │ 13 Models (UnivDept, UnivCourse, UnivStream, StreamLabel...)
  03. Human Resources & Staff Operations         │ 07 Models (Staff, StaffSubject, LeaveApplication, LeaveBalance...)
  04. Academic Curriculum, CBCS & Timetables     │ 15 Models (SubjectPool, BatchTermSubject, TimetableEntry...)
  05. Admissions, Enrollment & Student Lifecycle │ 14 Models (Student, StudentProfile, CancelEnrollmentRequest...)
  06. Examinations, Grading, Question Bank & CBE │ 24 Models (Question, ExamPaper, ExamAttempt, AnonCode, Marks...)
  07. Fees, Invoicing & Double-Entry Ledgers     │ 13 Models (FeeHead, FeeStructure, FeeDemand, FeeLedger, Payment...)
  08. Campus Facilities, Housing & Library       │ 16 Models (Hostel, HostelRoom, TransportPass, Book, BookCopy...)
  09. Documents, Canvas & Certificate Stock      │ 06 Models (DocumentTemplate, CertificateStockBatch, IssuedDoc...)
  10. Governance, Workflows, Forms & Comms       │ 19 Models (WorkflowInstance, FormTemplate, Notice, Banner...)
======================================================================================================================
  TOTAL ACTIVE RELATIONAL ENTITIES: 138 PRISMA MODELS
======================================================================================================================
```

---

## Domain Cluster 01: Multi-Tenant Core, Identity & Access Control (11 Models)

### 1. `University`
- **Table Name**: `universities`
- **Purpose**: Root charter tenant entity representing the overarching university system or state collegiate authority.
- **Primary Key**: `id` (`UUID`)
- **Key Fields**: `name` (`VARCHAR`), `code` (`VARCHAR UNIQUE`), `subdomain` (`VARCHAR UNIQUE`), `config` (`JSONB` - holds global security policies, Razorpay credentials, DLT headers, lockout timers).
- **Relations**: Has many `institutes`, `users`, `departments`, `programs`, `documentTemplates`, `workflowDefinitions`.

### 2. `Institute`
- **Table Name**: `institutes`
- **Purpose**: Constituent campus, autonomous college, or affiliated institutional unit.
- **Primary Key**: `id` (`UUID`)
- **Key Fields**: `universityId` (`UUID FK`), `name` (`VARCHAR`), `shortName` (`VARCHAR`), `schemaName` (`VARCHAR UNIQUE`), `address` (`TEXT`).
- **Relations**: Belongs to `University`; has many `departments`, `staff`, `students`, `hostels`, `buses`.

### 3. `InstituteResourceType` & 4. `InstituteResource`
- **Table Names**: `institute_resource_types`, `institute_resources`
- **Purpose**: Physical infrastructure asset inventory (e.g. Smart Projectors, Servers, 3D Printers, Audiovisual systems).
- **Key Fields**: `typeId`, `name`, `code`, `capacity`, `isAvailable`.

### 5. `User`
- **Table Name**: `users`
- **Purpose**: Central authentication and identity credential account for all institutional actors.
- **Primary Key**: `id` (`UUID`)
- **Key Fields**: `universityId` (`UUID`), `instituteId` (`UUID NULLABLE`), `email` (`VARCHAR UNIQUE`), `phone` (`VARCHAR UNIQUE`), `passwordHash` (`VARCHAR`), `applicationRole` (`VARCHAR`), `scope` (`ENUM('university','institute')`), `isActive` (`BOOLEAN`), `failedLoginAttempts` (`INTEGER`), `lockedUntil` (`TIMESTAMP`).
- **Relations**: Linked 1:1 to `Student` or `Staff`; has many `refreshTokens`, `roleAssignments`, `auditLogs`.

### 6. `PasswordHistory`
- **Table Name**: `password_histories`
- **Purpose**: Cryptographic memory of previously utilized password hashes to enforce NIST compliance (prevents reuse of last 5 passwords).
- **Key Fields**: `userId` (`UUID FK`), `passwordHash` (`VARCHAR`), `createdAt` (`TIMESTAMP`).

### 7. `UserRoleAssignment` & 8. `Role`
- **Table Names**: `user_role_assignments`, `roles`
- **Purpose**: Multi-dimensional RBAC engine allowing users to hold multiple concurrent roles across scopes.
- **Key Fields**: `userId`, `roleId`, `roleName`, `scope`, `instituteId`, `isActive`.

### 9. `RefreshToken`
- **Table Name**: `refresh_tokens`
- **Purpose**: Cryptographic JWT refresh tokens with rotation and revocation mechanisms.
- **Key Fields**: `id`, `userId`, `tokenHash`, `expiresAt`, `revokedAt`.

### 10. `MobileOtp`
- **Table Name**: `mobile_otps`
- **Purpose**: Ephemeral 6-digit one-time password store for candidate registrations and parent passwordless login.
- **Key Fields**: `phone`, `otpHash`, `purpose`, `expiresAt`, `verified`.

### 11. `AuditLog`
- **Table Name**: `audit_logs`
- **Purpose**: Append-only immutable system event audit trail tracking every administrative mutation.
- **Key Fields**: `id`, `universityId`, `userId`, `impersonatedBy`, `action`, `entity`, `entityId`, `oldValues` (`JSONB`), `newValues` (`JSONB`), `ipAddress`, `userAgent`, `createdAt`.

---

## Domain Cluster 02: Institutional Hierarchy & Master Academic Catalog (13 Models)

### 12. `UniversityDepartment`
- **Table Name**: `university_departments`
- **Purpose**: Central statutory faculty/school (e.g. Faculty of Engineering, School of Law).
- **Key Fields**: `universityId`, `code`, `name`, `isAcademic`.

### 13. `UniversityCourse`
- **Table Name**: `university_courses`
- **Purpose**: Canonical degree level (e.g. `BTECH`, `MTECH`, `MBA`, `BCA`).
- **Key Fields**: `departmentId`, `code`, `name`, `durationYears`.

### 14. `UniversityStream`
- **Table Name**: `university_streams`
- **Purpose**: Degree specialization / stream (e.g. `CSE`, `ECE`, `MECH`).
- **Key Fields**: `courseId`, `code`, `name`, `streamType`, `regulatedBy` (AICTE/UGC).

### 15. `StreamLabel`
- **Table Name**: `stream_labels`
- **Purpose**: Published NEP 2020 curriculum version rule container (5-Tab designer rules).
- **Key Fields**: `streamId`, `name`, `academicYear`, `version`, `totalCredits` (160), `unitName` ('Semester'), `unitCount` (8), `minAttendance` (75), `gradeBoundaries` (`JSONB`).

### 16. `UniversitySubject`
- **Table Name**: `university_subjects`
- **Purpose**: Canonical syllabus course catalog.
- **Key Fields**: `streamId`, `code`, `name`, `part` (Year 1/2/3/4), `isElective`, `syllabus` (`TEXT`).

### 17. `Department` (Institute Level)
- **Table Name**: `departments`
- **Purpose**: Operational teaching department inside a constituent college (e.g. Dept of Computer Science at Campus 1).
- **Key Fields**: `instituteId`, `universityDeptId`, `code`, `name`, `headStaffId`.

### 18. `Programme` (Institute Level)
- **Table Name**: `programmes`
- **Purpose**: Operational program delivered at campus level.
- **Key Fields**: `departmentId`, `code`, `name`, `durationYears`, `totalCredits`.

### 19. `Course` (Institute Level)
- **Table Name**: `courses`
- **Purpose**: Campus-level course container carrying tuition, admission, and lab fee baselines.
- **Key Fields**: `programmeId`, `code`, `name`, `tuitionFee`, `admissionFee`, `labFee`, `miscFee`.

### 20. `ProgramSeatApproval`
- **Table Name**: `program_seat_approvals`
- **Purpose**: Regulatory intake approvals issued by state bodies or AICTE.
- **Key Fields**: `courseId`, `approvedSeats`, `effectiveDate`, `note`, `attachmentUrl`.

### 21. `Batch`
- **Table Name**: `batches`
- **Purpose**: Student academic year cohort (e.g. `B.Tech CSE 2026-2030`).
- **Key Fields**: `courseId`, `batchName`, `academicYear`, `yearNumber`, `batchSize`.

### 22. `Section`
- **Table Name**: `sections`
- **Purpose**: Physical classroom cohort division (`Section A`, `Section B`).
- **Key Fields**: `batchId`, `name`, `sectionSize`, `roomAssigned`.

### 23. `BatchSetupDraft`
- **Table Name**: `batch_setup_drafts`
- **Purpose**: Ephemeral multi-step wizard state for administrative cohort initialization.
- **Key Fields**: `universityId`, `step`, `data` (`JSONB`), `updatedAt`.

### 24. `StreamLabel` & `SubjectLabel`
- **Table Name**: `subject_labels`
- **Purpose**: Subject syllabus revision stamping.

---

## Domain Cluster 03: Human Resources & Faculty Management (7 Models)

### 25. `Staff`
- **Table Name**: `staff`
- **Purpose**: Employment record of teaching, non-teaching, and administrative personnel.
- **Primary Key**: `id` (`UUID`)
- **Key Fields**: `instituteId`, `departmentId`, `employeeId UNIQUE`, `firstName`, `lastName`, `email`, `phone`, `staffType` (`ENUM('teaching','non_teaching')`), `designation`, `dateOfJoining`, `experienceYears`.

### 26. `StaffSubject`
- **Table Name**: `staff_subjects`
- **Purpose**: Junction mapping faculty instructors to specific subjects and sections.
- **Key Fields**: `staffId`, `subjectId`, `sectionId`, `academicYear`.

### 27. `LeaveType`
- **Table Name**: `leave_types`
- **Purpose**: Institutional leave categories (Casual Leave - CL, Earned Leave - EL, Medical Leave - ML, On Duty - OD).
- **Key Fields**: `universityId`, `name`, `code`, `daysAllowedPerYear`, `carryForward`.

### 28. `LeaveApplication`
- **Table Name**: `leave_applications`
- **Purpose**: Faculty leave requests carrying mandatory substitute lecture mapping.
- **Key Fields**: `staffId`, `leaveTypeId`, `startDate`, `endDate`, `reason`, `substituteArrangements` (`JSONB`), `status` (`ENUM('pending','approved','rejected')`), `approvedByStaffId`.

### 29. `LeaveBalance`
- **Table Name**: `leave_balances`
- **Purpose**: Current available leave credit quotas per staff member.
- **Key Fields**: `staffId`, `leaveTypeId`, `academicYear`, `allocated`, `used`, `balance`.

### 30. `StaffDocument`
- **Table Name**: `staff_documents`
- **Purpose**: Employment contracts, educational degrees, and service records.
- **Key Fields**: `staffId`, `documentType`, `fileUrl`, `verified`.

### 31. `HolidayCalendar`
- **Table Name**: `holiday_calendars`
- **Purpose**: Statutory gazetted holidays and vacation periods.
- **Key Fields**: `universityId`, `instituteId`, `name`, `date`, `isRestricted`.

---

## Domain Cluster 04: Academic Curriculum, CBCS & Timetables (15 Models)

### 32. `SubjectPool` & 33. `SubjectPoolMember`
- **Table Names**: `subject_pools`, `subject_pool_members`
- **Purpose**: NEP 2020 elective choice baskets (Core, Elective, SEC, VAC).
- **Key Fields**: `batchTermId`, `name`, `category`, `minCredits`, `maxCredits`, `minCapacity`, `maxCapacity`.

### 34. `BatchTerm`
- **Table Name**: `batch_terms`
- **Purpose**: Specific semester container for a batch (e.g. Batch 2026, Term 3).
- **Key Fields**: `batchId`, `termNumber`, `startDate`, `endDate`, `isLocked`.

### 35. `BatchTermSubject`
- **Table Name**: `batch_term_subjects`
- **Purpose**: Live teaching course instance for a term.
- **Key Fields**: `batchTermId`, `subjectId`, `subjectLabel`, `credits`, `isElective`.

### 36. `StudentSubjectEnrollment`
- **Table Name**: `student_subject_enrollments`
- **Purpose**: Student registration into a specific term course instance.
- **Key Fields**: `studentId`, `batchTermSubjectId`, `enrollmentType`, `isApproved`.

### 37. `StudentTermElection`
- **Table Name**: `student_term_elections`
- **Purpose**: Temporary student elective basket selection prior to HOD locking.
- **Key Fields**: `studentId`, `subjectPoolId`, `selectedSubjectIds` (`JSONB`).

### 38. `SubjectComponentLock`
- **Table Name**: `subject_component_locks`
- **Purpose**: Academic audit locks preventing grade or attendance modification post-submission.
- **Key Fields**: `batchTermSubjectId`, `componentType`, `lockedBy`, `lockedAt`.

### 39. `TimeSlot`
- **Table Name**: `time_slots`
- **Purpose**: Master daily bell schedule (e.g. Slot 1: 09:00 - 09:55 AM).
- **Key Fields**: `instituteId`, `slotIndex`, `startTime`, `endTime`, `isBreak`.

### 40. `TimetableEntry`
- **Table Name**: `timetable_entries`
- **Purpose**: Master weekly class scheduling grid.
- **Key Fields**: `sectionId`, `subjectId`, `staffId`, `roomId`, `timeSlotId`, `dayOfWeek`.

### 41. `SpecialLecture`
- **Table Name**: `special_lectures`
- **Purpose**: Guest seminars, extra makeup classes, and workshop sessions.
- **Key Fields**: `batchId`, `subjectId`, `speakerName`, `scheduledAt`, `durationMinutes`.

### 42. `StudentAttendance` & 43. `StudentSubjectAttendance`
- **Table Names**: `student_attendances`, `student_subject_attendances`
- **Purpose**: Granular class-by-class attendance logs.
- **Key Fields**: `studentId`, `batchTermSubjectId`, `date`, `attended` (`0 | 1`), `attendanceType` (`lecture/lab`).

### 44. `SubjectAttendanceSummary`
- **Table Name**: `subject_attendance_summaries`
- **Purpose**: Real-time aggregated attendance percentage per student per subject.
- **Key Fields**: `studentId`, `batchTermSubjectId`, `totalSessions`, `attendedSessions`, `percentage`.

### 45. `AttendanceConfig` & 46. `ScheduleRun`
- **Table Names**: `attendance_configs`, `schedule_runs`
- **Purpose**: Automated cron schedule configurations for daily attendance rollups and alerts.

---

## Domain Cluster 05: Admissions & Student Lifecycle (14 Models)

### 47. `Student`
- **Table Name**: `students`
- **Purpose**: Core student matriculation record.
- **Primary Key**: `id` (`UUID`)
- **Key Fields**: `userId` (`UUID FK`), `batchId` (`UUID FK`), `sectionId` (`UUID FK`), `enrollmentNo` (`VARCHAR UNIQUE`), `rollNo` (`VARCHAR`), `admissionDate` (`DATE`), `status` (`ENUM('active','cancelled','suspended','graduated')`).

### 48. `StudentProfile`
- **Table Name**: `student_profiles`
- **Purpose**: Comprehensive demographic, identity, medical, and domicile profile.
- **Key Fields**: `userId`, `dateOfBirth`, `gender`, `category`, `guardianName`, `guardianMobile`, `guardianEmail`, `permanentAddress`, `bloodGroup`, `ext` (`JSONB` - holds APAAR/ABC ID).

### 49. `ParentLink`
- **Table Name**: `parent_links`
- **Purpose**: Cryptographic association linking verified guardian mobile numbers to student records.
- **Key Fields**: `studentId`, `guardianMobile`, `guardianEmail`, `relationship`, `isVerified`.

### 50. `RegistrationRequest`
- **Table Name**: `registration_requests`
- **Purpose**: Self-registered candidate onboarding prior to matriculation.
- **Key Fields**: `email`, `phone`, `data` (`JSONB`), `status` (`PENDING/VERIFIED`).

### 51. `CancelEnrollmentRequest`
- **Table Name**: `cancel_enrollment_requests`
- **Purpose**: Multi-tier voluntary withdrawal and cancellation workflow engine.
- **Key Fields**: `instanceId`, `studentUserId`, `enrollmentNo`, `requestedBy`, `justification`, `reviewedBy`, `reviewComment`, `approvedBy`, `approvalComment`, `deactivateAt`, `deactivatedAt`, `status` (`pending_review/pending_approval/approved/rejected`).

### 52. `ProfileChangeRequest` & 53. `ProfileChangeLog`
- **Table Names**: `profile_change_requests`, `profile_change_logs`
- **Purpose**: Student demographic change verification audit trail.
- **Key Fields**: `studentId`, `fieldName`, `oldValue`, `newValue`, `proofDocumentUrl`, `approvedByStaffId`.

### 54. `StudentConcession`
- **Table Name**: `student_concessions`
- **Purpose**: Category-based tuition fee concessions (e.g. SC/ST, Sports quota).
- **Key Fields**: `studentId`, `feeHeadId`, `percentage`, `validUntil`.

### 55. `ProgramDepositRefundRequest`
- **Table Name**: `program_deposit_refund_requests`
- **Purpose**: Caution deposit settlement advice for departing students.
- **Key Fields**: `studentId`, `cautionDepositAmount`, `damageDeductions`, `netRefund`, `status`.

---

## Domain Cluster 06: Examinations, Grading & Computer-Based Testing (24 Models)

### 56. `Question`, 57. `QuestionVersion` & 58. `QuestionChangeRequest`
- **Table Names**: `questions`, `question_versions`, `question_change_requests`
- **Purpose**: Question Bank items, version histories, and psychometric classifications.
- **Key Fields**: `subjectId`, `questionType`, `content` (`JSONB`), `options` (`JSONB`), `correctAnswer` (`JSONB`), `bloomTaxonomyLevel`, `difficultyIndex`.

### 59. `ExamPaper` & 60. `ExamPaperQuestion`
- **Table Names**: `exam_papers`, `exam_paper_questions`
- **Purpose**: Generated examination question papers linking blueprint items.
- **Key Fields**: `subjectId`, `paperCode`, `totalMarks`, `durationMinutes`, `isRandomized`.

### 61. `ExamSchedule`
- **Table Name**: `exam_schedules`
- **Purpose**: Master university examination timetable.
- **Key Fields**: `batchTermSubjectId`, `examDate`, `startTime`, `endTime`, `slotCode`.

### 62. `ExamSeatAllocation` & 63. `ExamRollNo`
- **Table Names**: `exam_seat_allocations`, `exam_roll_nos`
- **Purpose**: Examination center hall and desk assignments.
- **Key Fields**: `studentId`, `examScheduleId`, `roomCode`, `deskNumber`.

### 64. `ExamAnonCode`
- **Table Name**: `exam_anon_codes`
- **Purpose**: Double-blind pseudorandom examination evaluation codes.
- **Key Fields**: `studentId`, `examScheduleId`, `anonymousCode` (`VARCHAR UNIQUE`), `isDecoded`.

### 65. `ExamAdmitCardIneligibility`
- **Table Name**: `exam_admit_card_ineligibilities`
- **Purpose**: Automated gate blocking Hall Ticket release for defaulters.
- **Key Fields**: `studentId`, `examScheduleId`, `ineligibilityReason` (`ATTENDANCE_SHORTAGE / FEE_DEFAULT`).

### 66. `ExamAttempt`, 67. `ExamDirective`, 68. `ExamProctorEvent`, 69. `ExamSnapshot` & 70. `ExamResponse`
- **Table Names**: `exam_attempts`, `exam_directives`, `exam_proctor_events`, `exam_snapshots`, `exam_responses`
- **Purpose**: Real-time Computer-Based Exam (CBE) execution telemetry, proctoring blur events, and webcam snapshots.
- **Key Fields**: `studentId`, `examPaperId`, `startedAt`, `submittedAt`, `score`, `proctorViolationsCount`.

### 71. `StudentMarks`
- **Table Name**: `student_marks`
- **Purpose**: Granular CIA and End-Semester scores.
- **Key Fields**: `enrollmentId`, `componentType` (`internal_1/internal_2/external`), `marksObtained`, `maxMarks`.

### 72. `StudentTermResult` & 73. `StudentCumulativeResult`
- **Table Names**: `student_term_results`, `student_cumulative_results`
- **Purpose**: Official semester SGPA and cumulative CGPA academic records.
- **Key Fields**: `studentId`, `termNumber`, `sgpa`, `cgpa`, `totalCreditsEarned`, `degreeClass`, `degreeAwarded`.

### 74. `ResultHold`
- **Table Name**: `result_holds`
- **Purpose**: Administrative and disciplinary holds withholding result publication.
- **Key Fields**: `studentId`, `termNumber`, `reason`, `placedBy`, `releasedAt`.

### 75. `PbePaperSet` & 76. `PbePaperDraft`
- **Table Names**: `pbe_paper_sets`, `pbe_paper_drafts`
- **Purpose**: Traditional Paper-Based Exam (PBE) draft generator, sets (Set A/B/C), and watermarked PDFs.

### 77. `ReAssessmentRequest` & 78. `SupplementaryExam`
- **Table Names**: `re_assessment_requests`, `supplementary_exams`
- **Purpose**: Post-result re-checking applications and backlog exam registrations.

### 79. `AnswersheetSerial`
- **Table Name**: `answersheet_serials`
- **Purpose**: Physical barcode tracking of physical paper answer booklets.

---

## Domain Cluster 07: Fees, Billing & Financial Ledgers (13 Models)

### 80. `FeeHead`
- **Table Name**: `fee_heads`
- **Purpose**: Master fee classification categories (Tuition, Lab, Caution, Exam).
- **Key Fields**: `instituteId`, `code`, `name`, `category` (`ACADEMIC/DEPOSIT/HOSTEL`), `isRefundable`, `isRecurring`.

### 81. `FeeStructure`
- **Table Name**: `fee_structures`
- **Purpose**: Master fee schedules linking programs, academic years, and terms.
- **Key Fields**: `programmeId`, `academicYear`, `termNumber`, `totalAmount`, `dueDate`, `lateFineDaily`.

### 82. `FeeDemand`
- **Table Name**: `fee_demands`
- **Purpose**: Invoiced student receivables / billing obligations.
- **Key Fields**: `studentId`, `feeHeadId`, `demandNo UNIQUE`, `amountDue`, `amountPaid`, `dueDate`, `status` (`unpaid/paid/waived`).

### 83. `FeeLedger`
- **Table Name**: `fee_ledgers`
- **Purpose**: Double-entry financial running balance ledger.
- **Key Fields**: `studentId`, `demandId`, `paymentId`, `entryType` (`DEBIT/CREDIT`), `amount`, `balanceAfter`.

### 84. `Payment`
- **Table Name**: `payments`
- **Purpose**: Verified settlement transaction record.
- **Key Fields**: `studentId`, `receiptNo UNIQUE`, `amount`, `paymentMode` (`ONLINE/CASH/DD`), `transactionRef`, `status` (`SUCCESS`).

### 85. `FeeWaiver`
- **Table Name**: `fee_waivers`
- **Purpose**: Institutional administrative fee waivers.
- **Key Fields**: `demandId`, `amount`, `justification`, `approvedByUserId`.

### 86. `Scholarship`
- **Table Name**: `scholarships`
- **Purpose**: Endowment and merit/means financial aid endowments.
- **Key Fields**: `studentId`, `name`, `amount`, `disbursedDate`.

### 87. `GovtReimbursement`
- **Table Name**: `govt_reimbursements`
- **Purpose**: State welfare fee reimbursements (e.g. Post-Matric SC/ST Scholarships).
- **Key Fields**: `studentId`, `stateClaimNo`, `sanctionedAmount`, `receivedDate`.

### 88. `StudentPayable`
- **Table Name**: `student_payables`
- **Purpose**: Discretionary student charges (library fines, breakage penalties).

---

## Domain Cluster 08: Campus Logistics, Housing & Central Library (16 Models)

### 89. `Hostel`, 90. `HostelRoom` & 91. `HostelAllocation`
- **Table Names**: `hostels`, `hostel_rooms`, `hostel_allocations`
- **Purpose**: Campus residential housing management, room capacity, and student bed assignments.
- **Key Fields**: `hostelCode`, `roomNumber`, `roomType` (`SINGLE/DOUBLE`), `capacity`, `checkInDate`, `checkOutDate`.

### 92. `HostelFeeComponent` & 93. `HostelRefundRequest`
- **Table Names**: `hostel_fee_components`, `hostel_refund_requests`
- **Purpose**: Room rent, monthly dining mess advances, and room vacation damage settlements.

### 94. `HostelRequest` & 95. `HostelConfig`
- **Table Names**: `hostel_requests`, `hostel_configs`
- **Purpose**: Student residential applications and facility rules.

### 96. `TransportRoute`, 97. `TransportVehicle` & 98. `TransportPass`
- **Table Names**: `transport_routes`, `transport_vehicles`, `transport_passes`
- **Purpose**: Campus transit fleet, routes, stops, and scannable digital bus passes.
- **Key Fields**: `routeNumber`, `vehicleRegNo`, `driverName`, `passNumber UNIQUE`, `stopName`, `validTill`.

### 99. `Book`, 100. `BookCopy`, 101. `BookIssue` & 102. `BookReservation`
- **Table Names**: `books`, `book_copies`, `book_issues`, `book_reservations`
- **Purpose**: Central library bibliographic catalog, physical barcode/RFID copies, loans, and reservations.
- **Key Fields**: `isbn`, `title`, `callNumber`, `barcode UNIQUE`, `loanDate`, `dueDate`, `returnedDate`, `fineAmount`.

### 103. `LibraryConfig`
- **Table Name**: `library_configs`
- **Purpose**: Maximum loan durations and daily overdue fine rates.

### 104. `Room` & 105. `Equipment`
- **Table Names**: `rooms`, `equipment`
- **Purpose**: Master physical space and laboratory equipment registry.

---

## Domain Cluster 09: Documents, Templates & Anti-Counterfeit Credentials (6 Models)

### 106. `DocumentTemplate`
- **Table Name**: `document_templates`
- **Purpose**: Visual Canvas layouts (Degrees, Transcripts, ID Cards, Bonafide certificates).
- **Key Fields**: `universityId`, `name`, `code UNIQUE`, `subjectType` (`student/staff`), `canvasState` (`JSONB`).

### 107. `CertificateStockBatch` & 108. `CertificateStock`
- **Table Names**: `certificate_stock_batches`, `certificate_stocks`
- **Purpose**: Security parchment paper vault tracking, individual paper serials, and damage tracking.
- **Key Fields**: `prefix`, `startNumber`, `endNumber`, `serialNumber UNIQUE`, `status` (`AVAILABLE/ISSUED/DAMAGED`), `comment` (`'issued: <enr>/<email>'`).

### 109. `IssuedDocument`
- **Table Name**: `issued_documents`
- **Purpose**: Cryptographic record of all generated certificates with verification URLs.
- **Key Fields**: `studentId`, `templateId`, `serialNo UNIQUE`, `verifyUrl`, `integrityHash` (SHA-256), `issuedAt`.

### 110. `DocumentVerificationRequest`
- **Table Name**: `document_verification_requests`
- **Purpose**: Third-party verification requests submitted by employers or screening agencies.

---

## Domain Cluster 10: Governance, Workflows, Forms & Communications (19 Models)

### 111. `WorkflowDefinition`, 112. `WorkflowState`, 113. `WorkflowTransition` & 114. `WorkflowInstance`
- **Table Names**: `workflow_definitions`, `workflow_states`, `workflow_transitions`, `workflow_instances`
- **Purpose**: Visual node-based deterministic finite state machine (DFA) workflow engine.
- **Key Fields**: `entityType` (`ADMISSION/LEAVE/NO_DUES`), `status`, `currentStateId`, `initiatorUserId`, `data` (`JSONB`).

### 115. `WorkflowTask` & 116. `WorkflowInstanceEvent`
- **Table Names**: `workflow_tasks`, `workflow_instance_events`
- **Purpose**: Centralized `/my-tasks` task inbox and step-by-step workflow audit logs.

### 117. `WorkflowReservation`
- **Table Name**: `workflow_reservations`
- **Purpose**: Saga-pattern resource holds (e.g. holding an admission seat during checkout).

### 118. `FormTemplate` & 119. `FormSubmission`
- **Table Names**: `form_templates`, `form_submissions`
- **Purpose**: Visual drag-and-drop dynamic forms and survey submission engine.
- **Key Fields**: `title`, `schema` (`JSONB`), `applicantUserId`, `responses` (`JSONB`), `status`.

### 120. `IdFormat`, 121. `IdSequenceCounter` & 122. `IdCustomToken`
- **Table Names**: `id_formats`, `id_sequence_counters`, `id_custom_tokens`
- **Purpose**: Deterministic sequential identifier engine for Enrollment Numbers, Employee IDs, and Receipts.
- **Key Fields**: `pattern` (`{{YEAR}}{{DEPT}}{{SEQ:4}}`), `currentValue`, `padding`.

### 123. `ResourceReservation` & 124. `BatchTermSubjectResource`
- **Table Names**: `resource_reservations`, `batch_term_subject_resources`
- **Purpose**: Campus space booking and equipment reservations.

### 125. `Banner` & 126. `BannerReceipt`
- **Table Names**: `banners`, `banner_receipts`
- **Purpose**: Targeted institutional broadcast banners and user acknowledgment tracking.

### 127. `Notice` & 128. `NoticeTag`
- **Table Names**: `notices`, `notice_tags`
- **Purpose**: Digital notice board circulars with audience filters.

### 129. `Notification` & 130. `NotificationLog`
- **Table Names**: `notifications`, `notification_logs`
- **Purpose**: In-app notifications, push feeds, and SMS delivery status tracking.

### 131. `SocialHandle` & 132. `SocialPost`
- **Table Names**: `social_handles`, `social_posts`
- **Purpose**: Campus sentiment monitoring and social media brand tracking.

### 133. `ModuleAccess`
- **Table Name**: `module_accesses`
- **Purpose**: Dynamic per-module RBAC permissions stored in database (`readRoles`, `writeRoles`).

### 134. `Counsellor`, 135. `CounsellorContract`, 136. `CounsellingRequest`, 137. `CounsellingComment` & 138. `CounsellorEnrollmentCredit`
- **Table Names**: `counsellors`, `counsellor_contracts`, `counselling_requests`, `counselling_comments`, `counsellor_enrollment_credits`
- **Purpose**: Student psychological welfare, booking desk, and AES-256 encrypted confidential case logs.

---
```
========================================================================================================================
END OF SPECIFICATION: DATABASE SCHEMA & ENTITY DICTIONARY (UERP-DB-DATA-DICTIONARY-V4.2)
========================================================================================================================
```
