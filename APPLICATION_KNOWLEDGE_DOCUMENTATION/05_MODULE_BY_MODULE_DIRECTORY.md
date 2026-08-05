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
