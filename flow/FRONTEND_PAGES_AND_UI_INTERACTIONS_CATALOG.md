# Master Frontend Pages & UI Interactions Catalog
## Exhaustive Technical Reference for all 49 React Pages in UniversityERP

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-UI-CATALOG-V4.2
CLASSIFICATION: TECHNICAL REFERENCE & USER INTERFACE CATALOG
AUTHORITY: PRINCIPAL FRONTEND ARCHITECT & UX LEAD
STACK: REACT 18 / VITE / TYPESCRIPT / TAILWIND CSS / TANSTACK QUERY / LUCIDE ICONS / 49 PAGES
========================================================================================================================
```

---

## Executive Overview: The Universal Web & Mobile Portal

The frontend layer of **UniversityERP** is built as a responsive Single Page Application (SPA) with Progressive Web App (PWA) capabilities. It provides role-tailored workspaces across **49 dedicated page views**, adapting dynamically based on the authenticated user's `effectiveRoles` and multi-tenant scope.

```
+--------------------------------------------------------------------------------------------------------------------+
|                                    49 REACT PAGES: WORKSPACE CATEGORIZATION                                        |
+--------------------------------------------------------------------------------------------------------------------+
  01. Authentication & Account Access       │ 05 Pages (LoginPage, RegisterPage, ForgotPassword, ResetPassword, Setup)
  02. System Master Data & Architecture      │ 04 Pages (MasterDataPage, ValidationPage, BatchSetup, ProgramFeeManager)
  03. Admissions & Student Enrollment        │ 05 Pages (AdmissionsPage, MeritListPage, Applications, Onboarding, Profile)
  04. Academic Operations, Timetable & Attn  │ 04 Pages (TimetablePage, AttendancePage, ElectivesPage, MySubjectsPage)
  05. Examinations & Fullscreen CBE Proctor  │ 07 Pages (Examinations, ExamTake, Monitor, ItemAnalysis, Invigilation...)
  06. Fees, Finance & Payment Checkout       │ 03 Pages (FeesPage, ProgramFeeManager, ResourceFeeManager)
  07. Campus Logistics, Housing & Fleet      │ 03 Pages (HostelPage, TransportPage, LibraryPage)
  08. Human Resources & Staff Operations     │ 03 Pages (HRPage, LeaveRequestsPage, DirectoryPage)
  09. Student Welfare & Counselling Desk     │ 02 Pages (CounsellingAdminPage, CounsellingDeskPage)
  10. Documents, Canvas Designer & Verify    │ 04 Pages (DocumentsPage, PublicVerifyPage, IdFormatsPage, PublicResults)
  11. Dynamic Forms, Workflows & Tasks       │ 04 Pages (FormsPage, WorkflowDesigner, WorkflowMonitor, MyTasksPage)
  12. Institutional Governance & Comms       │ 05 Pages (Dashboard, Analytics, NoticeBoard, Banners, AuditLogPage)
======================================================================================================================
  TOTAL REGISTERED PAGES: 49 REACT VIEWS
======================================================================================================================
```

---

## 1. Authentication & Account Lifecycle Pages (5 Pages)

### `LoginPage` (`web/admin-portal/src/pages/LoginPage.tsx`)
- **Route**: `/login`
- **Access**: Public / Unauthenticated
- **Features**: Dual-login tabs (Email + Password or Mobile Number + OTP), password visibility toggle, remember-me checkbox, institutional logo branding, automated lockout alert when failed attempts exceed 5.
- **Interactions**: Submits credentials to `POST /auth/login`; stores JWT tokens in secure storage; redirects to role-appropriate home view.

### `RegisterPage` (`web/admin-portal/src/pages/RegisterPage.tsx`)
- **Route**: `/register`
- **Access**: Public / Prospective Candidates
- **Features**: Multi-step candidate registration, real-time email syntax validator, E.164 phone normalization, 6-digit SMS OTP verification modal with 60-second resend countdown.

### `ForgotPasswordPage` & `ResetPasswordPage`
- **Routes**: `/forgot-password`, `/reset-password`
- **Features**: Secure password recovery via signed one-time link or mobile OTP; password strength entropy meter (requires uppercase, lowercase, numeral, special symbol); disallows previous 5 passwords.

### `SetupAccountPage` (`web/admin-portal/src/pages/SetupAccountPage.tsx`)
- **Route**: `/setup-account`
- **Features**: First-time login onboarding for newly matriculated students and faculty members. Enforces password change and acceptance of institutional IT usage charter.

---

## 2. Master Data & Academic Architecture Pages (4 Pages)

### `MasterDataPage` (`web/admin-portal/src/pages/MasterDataPage.tsx`)
- **Route**: `/master-data`
- **Allowed Roles**: `SuperAdmin`, `UnivAdmin`, `InstAdmin`
- **Features**:
  - Top Tabs: *Campuses*, *Departments*, *Courses (Degrees)*, *Programs (Streams)*, *Batches*, *Sections*.
  - Collapsible relational tree with search filters.
  - **Program Label Modal (5-Tab Rule Designer)**: Configures passing aggregate (50%), attendance bar (75%), letter grade scale (`O`, `A+`, `A`, `B+`, `B`, `C`, `F`), and NEP 2020 graduation credits (160).
  - Bulk Import / Export Modal: Supports CSV upload with dry-run schema validation.

### `ValidationPage` (`web/admin-portal/src/pages/ValidationPage.tsx`)
- **Route**: `/master-data/validation`
- **Features**: System-wide referential integrity audit tool. Highlights orphan sections, unassigned courses, and missing curriculum labels with automated 1-click repair scripts.

### `ProgramFeeManager` & `ResourceFeeManager`
- **Routes**: `/master-data/program-fees`, `/master-data/resource-fees`
- **Features**: Matrix editor linking statutory tuition and lab fees to specific program cohorts and laboratory rooms.

---

## 3. Admissions & Student Lifecycle Pages (5 Pages)

### `AdmissionsPage` (`web/admin-portal/src/pages/AdmissionsPage.tsx`)
- **Route**: `/admissions`
- **Allowed Roles**: `SuperAdmin`, `UnivAdmin`, `InstAdmin`, `Admission Approver`
- **Features**:
  - Live Admissions Funnel: *Leads* $\to$ *Applications Submitted* $\to$ *Documents Verified* $\to$ *Offers Issued* $\to$ *Enrolled*.
  - **Seat Master Ledger**: Interactive collapsible capacity tree (`SeatMasterService`) displaying Approved Statutory Intake vs Batch Allocated Seats.
  - **Export Capabilities**: 1-click export of certified seat allocations in **XLSX** and **PDF** formats (`seatMasterExport.ts`) for AICTE/UGC compliance.

### `MeritListPage` (`web/admin-portal/src/pages/MeritListPage.tsx`)
- **Route**: `/admissions/merit-list`
- **Features**:
  - Cohort selector (e.g. `B.Tech CSE 2026`).
  - Candidates sorted by composite entrance percentile and reservation quotas (General, OBC, SC, ST, EWS).
  - Multi-select candidate checkboxes with floating action bar: **Issue Bulk Provisional Offers** (activates 72-hour countdown hold timer).

### `StudentApplicationsPage` (`web/admin-portal/src/pages/StudentApplicationsPage.tsx`)
- **Route**: `/admissions/applications`
- **Features**: Dual-pane scrutiny workbench. Left: candidate data; Right: embedded PDF/image viewer for 10th/12th marksheets. Includes **Verify Document** and **Raise Scrutiny Defect** modals with 48-hour cure timers.

### `OnboardStudentsPage` (`web/admin-portal/src/pages/OnboardStudentsPage.tsx`)
- **Route**: `/onboarding/students`
- **Features**:
  - Bulk CSV / Excel upload with two-phase execution: **Dry-Run Validation** (checks foreign keys, reports errors with row numbers) and **Commit** (creates students and history in atomic transaction).
  - **Undo Onboarding / Guarded Deletion**: Student lookup input; permits removal only if zero academic/financial footprint exists.

### `StudentProfilePage` (`web/admin-portal/src/pages/StudentProfilePage.tsx`)
- **Route**: `/students/:id`
- **Features**: Comprehensive 360-degree student view: Demographic bio-data, parent links, enrolled subjects, real-time attendance percentage gauge, double-entry fee ledger, exam results, and issued credentials.

---

## 4. Academic Operations, Timetable & Attendance Pages (4 Pages)

### `TimetablePage` (`web/admin-portal/src/pages/TimetablePage.tsx`)
- **Route**: `/timetable`
- **Allowed Roles**: `InstAdmin`, `Dean/HOD`, `TeachingFaculty`, `Student`
- **Features**:
  - Interactive weekly grid (Monday through Saturday, Slots 1 to 8).
  - Drag-and-drop lecture assignment with **automated collision warnings** (faculty double-booking or room conflicts).
  - Filters by Section, Faculty, or Classroom Hall.
  - 1-click printable timetable PDF generation (`timetablePdfExport.ts`).

### `AttendancePage` (`web/admin-portal/src/pages/AttendancePage.tsx`)
- **Route**: `/attendance`
- **Features**:
  - Daily classroom register grid with student photos and roll numbers.
  - Modes: *Quick Mark Present*, *Manual Call*, and *Biometric Device Punch Ingestion*.
  - Real-time statutory attendance bar calculation (<75% triggers red highlight).

### `ElectivesPage` (`web/admin-portal/src/pages/ElectivesPage.tsx`)
- **Route**: `/academics/electives`
- **Features**: NEP 2020 Choice-Based Credit System basket configuration. Live progress bar of student enrollments per elective; HOD **Lock Elective Roster** action button.

### `MySubjectsPage` (`web/admin-portal/src/pages/MySubjectsPage.tsx`)
- **Route**: `/my-subjects`
- **Features**: Faculty instructional dashboard. Displays assigned courses, syllabus completion percentage, CIA marks entry grid, and class average analytics.

---

## 5. Examinations & Fullscreen CBE Proctoring Pages (7 Pages)

### `ExaminationsPage` (`web/admin-portal/src/pages/ExaminationsPage.tsx`)
- **Route**: `/examinations`
- **Features**: Master university exam schedule management, slot allocation, double-blind anonymous coding (`ExamAnonCode`), and Hall Ticket eligibility gate configuration.

### `ExamTakePage` (`web/admin-portal/src/pages/ExamTakePage.tsx`)
- **Route**: `/exam/:id`
- **Features**:
  - Fullscreen Computer-Based Exam (CBE) execution client.
  - Hardware pre-flight check (webcam feed, microphone, single monitor lock).
  - Question navigation palette, flagged for review indicators, countdown timer.
  - Fullscreen violation detection with instant warning modal.

### `ExamMonitorPage` (`web/admin-portal/src/pages/ExamMonitorPage.tsx`)
- **Route**: `/examinations/monitor`
- **Features**: Real-time live proctoring cockpit. Displays candidate webcam feeds, live violation alerts (blur events, multiple faces detected, audio anomalies), and remote termination trigger.

### `ExamItemAnalysisPage` (`web/admin-portal/src/pages/ExamItemAnalysisPage.tsx`)
- **Route**: `/examinations/item-analysis`
- **Features**: Question Bank psychometric telemetry. Visual scatter plot of Facility Index ($P$) vs Discrimination Index ($D$) mapped across Bloom's Taxonomy levels.

### `MyInvigilationPage` (`web/admin-portal/src/pages/MyInvigilationPage.tsx`)
- **Route**: `/my-invigilation`
- **Features**: Mobile-friendly invigilator terminal. Scans student Hall Ticket QR codes at the exam hall door to verify seating allocations and mark physical attendance.

### `PublicResultsPage` (`web/admin-portal/src/pages/PublicResultsPage.tsx`)
- **Route**: `/results/public`
- **Features**: Public examination result lookup portal. Candidates enter Enrollment Number + Date of Birth to view gazetted SGPA/CGPA grade sheets.

---

## 6. Fees, Finance & Payment Gateways Pages (3 Pages)

### `FeesPage` (`web/admin-portal/src/pages/FeesPage.tsx`)
- **Route**: `/fees`
- **Features**:
  - Invoicing statistics cards: Total Billed, Total Collected, Outstanding Receivables.
  - **Payment Windows Gear Modal (`FeeSettingsModal.tsx`)**: Configures application fee validity hours (e.g. 48h) and admission offer hold hours (e.g. 72h).
  - **Collect Fee Counter Modal**: Offline cashier desk for Cash, Demand Draft, and POS settlements with instant receipt printing (`REC-XXXXX`).
  - **Cancelled Enrollment Ledger Tab**: UGC statutory refund entitlement calculations and caution deposit return vouchers.

---

## 7. Campus Facilities, Housing & Logistics Pages (3 Pages)

### `HostelPage` (`web/admin-portal/src/pages/HostelPage.tsx`)
- **Route**: `/hostel`
- **Features**: Visual block-and-floor room occupancy matrix (Single AC, Double Non-AC). Room check-in inventory modal, damage assessment penalty logs, and residential No Dues clearance.

### `TransportPage` (`web/admin-portal/src/pages/TransportPage.tsx`)
- **Route**: `/transport`
- **Features**: Route stop planner, bus fleet capacity monitors, driver contact directory, and digital QR transit pass issuance.

### `LibraryPage` (`web/admin-portal/src/pages/LibraryPage.tsx`)
- **Route**: `/library`
- **Features**: OPAC book search catalog, RFID barcode circulation desk (14-day checkout with automatic overdue fine computation), and library No Dues audit.

---

## 8. Human Resources, Leaves & Staff Pages (3 Pages)

### `HRPage` (`web/admin-portal/src/pages/HRPage.tsx`)
- **Route**: `/hr`
- **Features**: Institutional employee directory, designation management, staff document vault, and faculty workload distribution.

### `LeaveRequestsPage` (`web/admin-portal/src/pages/LeaveRequestsPage.tsx`)
- **Route**: `/leave-requests`
- **Features**: Leave application queue. Displays proposed substitute lecture arrangements with colleague confirmation badges prior to HOD sanction.

### `DirectoryPage` (`web/admin-portal/src/pages/DirectoryPage.tsx`)
- **Route**: `/directory`
- **Features**: Searchable campus directory of faculty, administrative staff, and departments with direct email and extension numbers.

---

## 9. Student Welfare & Counselling Pages (2 Pages)

### `CounsellingAdminPage` & `CounsellingDeskPage`
- **Routes**: `/counselling`, `/counsellor-desk`
- **Features**:
  - Student mental health and career counselling booking calendar.
  - Confidential Counsellor Desk: Displays private appointments.
  - Zero-knowledge AES-256 encrypted case logs (`CounsellingComment.comment`) completely isolated from general faculty.

---

## 10. Documents, Canvas Designer & Public Verification Pages (4 Pages)

### `DocumentsPage` (`web/admin-portal/src/pages/DocumentsPage.tsx`)
- **Route**: `/documents`
- **Features**:
  - **Canvas Visual Template Designer**: Drag-and-drop placement of text, images, QR codes, student details (1|2|3 pair layouts), and marksheet tables (`firstRowHeader`).
  - **Certificate Stock Inventory**: Paging (`5/10/20`), serial number search, status badges (`AVAILABLE`, `ISSUED`, `DAMAGED`), and actor audit comments (`issued: 2024CSE0042/user@univ.edu`).
  - High-resolution in-app A4 preview modal with direct print streaming.

### `PublicVerifyPage` (`web/admin-portal/src/pages/PublicVerifyPage.tsx`)
- **Route**: `/verify`
- **Features**: Public unauthenticated credential verification desk. Scanning degree QR codes displays official university attestation with candidate details and integrity hash.

### `IdFormatsPage` (`web/admin-portal/src/pages/IdFormatsPage.tsx`)
- **Route**: `/id-formats`
- **Features**: Configures deterministic sequential identifier patterns (`{{YEAR}}{{DEPT}}{{SEQ:4}}`) for Enrollment Numbers and Employee IDs.

---

## 11. Dynamic Forms, Workflows & Tasks Pages (4 Pages)

### `FormsPage` (`web/admin-portal/src/pages/FormsPage.tsx`)
- **Route**: `/forms`
- **Features**: Visual drag-and-drop form schema builder. Supports text, number, date, dropdown, file upload, and digital signature elements with conditional visibility rules.

### `WorkflowDesignerPage` & `WorkflowMonitorPage`
- **Routes**: `/workflows/designer`, `/workflows/monitor`
- **Features**: Node-based DFA workflow editor powered by `@xyflow/react`. Defines states, transitions, authorized actor roles, SLA escalation timers, and resource reservation holds.

### `MyTasksPage` (`web/admin-portal/src/pages/MyTasksPage.tsx`)
- **Route**: `/my-tasks`
- **Features**: Unified task inbox for all approver personas. Aggregates pending admission scrutiny, leave approvals, document requests, and cancellation reviews.

---

## 12. Institutional Governance & Executive Dashboards (5 Pages)

### `DashboardPage` & `AnalyticsPage`
- **Routes**: `/dashboard`, `/analytics`
- **Features**:
  - Executive KPI cards: Total Matriculated Students, Active Faculty, Fee Collection vs Receivables, Room Occupancy.
  - NAAC/NIRF accreditation telemetry charts.
  - Real-time student attendance distribution graphs.

### `NoticeBoardPage` (`web/admin-portal/src/pages/NoticeBoardPage.tsx`)
- **Route**: `/notice-board`
- **Features**: Campus digital bulletin board with targeted audience filters (`All Students`, `Teaching Faculty`, `Hostel Residents`) and official PDF circular attachments.

### `BannersPage` (`web/admin-portal/src/pages/BannersPage.tsx`)
- **Route**: `/banners`
- **Features**: Emergency campus broadcast banner publisher with role-specific targeting and user dismissal tracking.

### `AuditLogPage` (`web/admin-portal/src/pages/AuditLogPage.tsx`)
- **Route**: `/audit-logs`
- **Features**: System security audit trail with user identity, timestamp, IP address, and JSON diff viewer for mutations.

---
```
========================================================================================================================
END OF CATALOG: MASTER FRONTEND PAGES & UI INTERACTIONS CATALOG (UERP-UI-CATALOG-V4.2)
========================================================================================================================
```
