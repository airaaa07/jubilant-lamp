# Master API Controller & REST Endpoint Catalog
## Exhaustive Technical Reference for all 71 NestJS Controllers in UniversityERP

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-API-CATALOG-V4.2
CLASSIFICATION: TECHNICAL REFERENCE & SYSTEM API SPECIFICATION
AUTHORITY: PRINCIPAL API ARCHITECT & BACKEND LEAD
ENGINE: NESTJS / FASTIFY-EXPRESS RUNTIME / 71 CONTROLLERS / 350+ ENDPOINTS
========================================================================================================================
```

---

## Executive Overview: The Unified REST API Continuum

All frontend applications (Universal React Web Portal, Mobile PWA, Public Verification Portal, and External Statutory Gateways) interface with the backend through a high-performance REST API hosted on port `:3000`.

Every endpoint is secured across three layers:
1. **`JwtAuthGuard`**: Validates the Bearer token signature, issuer, and expiration.
2. **`RolesGuard` / `@Roles(...)`**: Evaluates caller's effective roles union (`roles.util.ts`).
3. **`ModuleAccessGuard`**: Enforces dynamic tenant-specific module write locks.

---

## 1. Identity, Authentication & Security Controllers

### `AuthController` (`apps/core-api/src/modules/auth/auth.controller.ts`)
- **Prefix**: `/auth`
- **Guards**: Public (selective endpoints) / `JwtAuthGuard`
- **Endpoints**:
  - `POST /auth/login`: Authenticates via email/phone + password; returns `{ accessToken, refreshToken, user }`.
  - `POST /auth/refresh`: Issues new access token via cryptographic refresh token rotation.
  - `POST /auth/logout`: Revokes refresh token and blacklists session.
  - `POST /auth/impersonate`: (SuperAdmin only) Issues ephemeral impersonation JWT.
  - `POST /auth/impersonate/exit`: Reverts back to SuperAdmin session.
  - `POST /auth/register-request`: Public applicant registration with mobile OTP generation.
  - `POST /auth/verify-otp`: Validates 6-digit numeric OTP.
  - `POST /auth/forgot-password` & `POST /auth/reset-password`: Time-bound password recovery.
  - `POST /auth/setup-account`: One-time password setup for newly created staff/students.

### `UsersController` (`apps/core-api/src/modules/users/users.controller.ts`)
- **Prefix**: `/users`
- **Guards**: `JwtAuthGuard`, `RolesGuard` (`Roles('SuperAdmin', 'UnivAdmin', 'InstAdmin')`)
- **Endpoints**:
  - `GET /users`: Paginated listing with multi-role filters and scope filters.
  - `POST /users`: Provisions new user credential with assigned application role.
  - `PATCH /users/:id`: Updates demographic details or activates/deactivates account.
  - `PATCH /users/:id/password`: Administrative password reset.
  - `DELETE /users/:id`: Soft-deletes user (if no academic/financial footprint).

### `RolesController` (`apps/core-api/src/modules/roles/roles.controller.ts`)
- **Prefix**: `/roles`
- **Guards**: `JwtAuthGuard`, `RolesGuard` (`Roles('SuperAdmin', 'UnivAdmin')`)
- **Endpoints**:
  - `GET /roles`: Lists system roles filtered by scope (`university/institute`).
  - `POST /roles`: Creates custom institutional role definition.
  - `PATCH /roles/:id`: Renames role and automatically cascades update across all `User`, `UserRoleAssignment`, `WorkflowState`, and `ModuleAccess` records.

### `AuditController` (`apps/core-api/src/modules/audit/audit.controller.ts`)
- **Prefix**: `/audit-logs`
- **Guards**: `JwtAuthGuard`, `RolesGuard` (`Roles('SuperAdmin', 'UnivAdmin')`)
- **Endpoints**:
  - `GET /audit-logs`: Streams paginated, non-repudiation audit trail with user, entity, and diff inspection.

---

## 2. Master Data & Academic Structural Hierarchy Controllers

### `UniversityController`, `InstituteController`, `DepartmentController`
- **Prefixes**: `/master-data/universities`, `/master-data/institutes`, `/master-data/departments`
- **Guards**: `JwtAuthGuard`, `RolesGuard`
- **Endpoints**:
  - `GET /master-data/universities`: Root university details.
  - `POST /master-data/institutes`: Provisions new campus unit.
  - `GET /master-data/institutes`: Lists campuses with schema names.
  - `POST /master-data/departments`: Creates teaching departments.

### `ProgrammeController` & `CourseController`
- **Prefixes**: `/master-data/programmes`, `/master-data/courses`
- **Endpoints**:
  - `GET /master-data/programmes`: Lists degrees offered per department.
  - `POST /master-data/courses`: Defines campus course specializations with fee schedules.

### `BatchController` & `SectionController`
- **Prefixes**: `/master-data/batches`, `/master-data/sections`
- **Endpoints**:
  - `POST /master-data/batches`: Initializes new student academic cohorts.
  - `POST /master-data/sections`: Divides batches into classroom divisions (`Section A`, `Section B`).

### `StreamLabelController` & `SubjectLabelController`
- **Prefixes**: `/master-data/stream-labels`, `/master-data/subject-labels`
- **Endpoints**:
  - `POST /master-data/stream-labels`: Publishes NEP 2020 curriculum version rules (5-tab designer).
  - `GET /master-data/stream-labels/:id`: Retrieves letter grade boundaries and credit limits.

### `BulkImportController` (`apps/core-api/src/modules/master-data/controllers/bulk-import.controller.ts`)
- **Prefix**: `/master-data/bulk-import`
- **Endpoints**:
  - `POST /master-data/bulk-import/catalog`: Round-trip hierarchical catalog import.
  - `GET /master-data/bulk-import/catalog`: Exports catalog in ingestion shape.
  - `POST /master-data/bulk-import/subjects`: Ingests university subjects with preview.
  - `POST /master-data/bulk-import/institutes`: Ingests full campus tree down to sections.

---

## 3. Admissions & Student Lifecycle Controllers

### `AdmissionsController` (`apps/core-api/src/modules/admissions/admissions.controller.ts`)
- **Prefix**: `/admissions`
- **Endpoints**:
  - `GET /admissions/seat-master`: Returns hierarchical capacity tree with approved vs allocated seats.
  - `POST /admissions/seat-master/approvals`: Records statutory intake approvals with attachments.
  - `PATCH /admissions/seat-master/batches/:id/seats`: Edits batch seat quota.
  - `GET /admissions/applications`: Lists live candidate applications with status filters.
  - `GET /admissions/merit-list/:batchId`: Returns composite ranked merit list for cohort.
  - `POST /admissions/merit-list/:batchId/offer`: Issues bulk provisional admission offers with hold timers.
  - `POST /admissions/merit-list/:batchId/reject`: Rejection and waitlist rollover.

### `CancelEnrollmentController` (`apps/core-api/src/modules/admissions/cancel-enrollment.controller.ts`)
- **Prefix**: `/admissions/cancel-enrollment`
- **Endpoints**:
  - `GET /admissions/cancel-enrollment/roles`: Returns configured requester, reviewer, and approver roles.
  - `PUT /admissions/cancel-enrollment/roles`: Configures cancellation approval hierarchy.
  - `POST /admissions/cancel-enrollment`: Initiates cancellation request for enrolled student.
  - `GET /admissions/cancel-enrollment/tasks`: Returns pending review and approval tasks.
  - `POST /admissions/cancel-enrollment/:id/review`: Dean's review decision.
  - `POST /admissions/cancel-enrollment/:id/approve`: Registrar's final approval with 15-day deactivation timer.

### `OnboardingController` (`apps/core-api/src/modules/onboarding/onboarding.controller.ts`)
- **Prefix**: `/onboarding/students`
- **Endpoints**:
  - `POST /onboarding/students/validate`: Dry-run validation of bulk student import payload.
  - `POST /onboarding/students/commit`: Idempotent bulk creation of students and historical footprint.
  - `GET /onboarding/students/lookup`: Checks whether a student can be safely deleted.
  - `POST /onboarding/students/delete`: Guarded deletion (refuses if any marks/fees exist).
  - `GET /onboarding/students/template`: Downloads standardized onboarding template payload.

---

## 4. Academics, Curriculum, Timetable & Attendance Controllers

### `AttendanceController` (`apps/core-api/src/modules/academic/controllers/attendance.controller.ts`)
- **Prefix**: `/academic/attendance`
- **Endpoints**:
  - `POST /academic/attendance/record`: Submits daily lecture attendance register.
  - `GET /academic/attendance/student/:id`: Retrieves student course-wise attendance percentage.
  - `POST /academic/attendance/lock`: Freezes attendance records prior to exam eligibility audit.

### `ElectionController` (`apps/core-api/src/modules/academic/controllers/election.controller.ts`)
- **Prefix**: `/academic/election`
- **Endpoints**:
  - `GET /academic/election/pools`: Returns available NEP 2020 elective baskets for student's term.
  - `POST /academic/election/submit`: Student submits elective course choices.
  - `POST /academic/election/lock`: HOD locks elective roster into permanent enrollments.

### `MarksController` (`apps/core-api/src/modules/academic/controllers/marks.controller.ts`)
- **Prefix**: `/academic/marks`
- **Endpoints**:
  - `POST /academic/marks/entry`: Faculty submits internal CIA marks (Internal 1/2, Lab, Assignments).
  - `POST /academic/marks/lock`: HOD locks department marks register.
  - `GET /academic/marks/summary/:batchTermSubjectId`: Statistical summary of marks distribution.

### `TimetableController` (`apps/core-api/src/modules/timetable/timetable.controller.ts`)
- **Prefix**: `/timetable`
- **Endpoints**:
  - `GET /timetable/section/:id`: Retrieves weekly timetable grid for classroom section.
  - `GET /timetable/faculty/my`: Returns logged-in faculty's personalized weekly schedule.
  - `POST /timetable/entries`: Creates/updates lecture slot with automated collision checks.

---

## 5. Examinations, CBE Proctoring & Results Controllers

### `ExaminationController` (`apps/core-api/src/modules/examination/examination.controller.ts`)
- **Prefix**: `/examination`
- **Endpoints**:
  - `POST /examination/schedules`: Creates master examination schedule.
  - `GET /examination/admit-card/:studentId`: Releases QR-coded Hall Ticket (if eligible).
  - `POST /examination/anonymous-codes/generate`: Generates double-blind pseudorandom evaluation barcodes.
  - `POST /examination/results/publish`: Gazettes official semester SGPA and CGPA results.

### `QuestionBankController` (`apps/core-api/src/modules/question-bank/question-bank.controller.ts`)
- **Prefix**: `/question-bank`
- **Endpoints**:
  - `POST /question-bank/questions`: Authors new question item with Bloom's taxonomy metadata.
  - `GET /question-bank/item-analysis`: Retrieves empirical Facility ($P$) and Discrimination ($D$) indexes.
  - `PATCH /question-bank/questions/:id/approve`: Vets and locks item into live exam pool.

---

## 6. Fees, Billing, Ledgers & Gateways Controllers

### `FeeController` (`apps/core-api/src/modules/fee/fee.controller.ts`)
- **Prefix**: `/fee`
- **Endpoints**:
  - `POST /fee/heads`: Creates institutional fee heads (`TUITION`, `LAB`, `CAUTION`).
  - `POST /fee/structures`: Publishes program fee schedules.
  - `POST /fee/recurring/run`: Executes bulk semester recurring invoicing batch.
  - `POST /fee/demands/bulk`: Generates individual demand line items.
  - `PATCH /fee/demands/:id/pay`: Frontline offline cashiering with official receipt generation.
  - `GET /fee/payments/receipt/:receiptNo`: Retrieves official signed payment receipt PDF.
  - `GET /fee/reports/defaulters`: Returns delinquent student roster with outstanding balances.
  - `POST /fee/razorpay/demand-order`: Creates Razorpay checkout order for student invoices.
  - `POST /fee/razorpay/verify-payment`: Verifies server-side HMAC-SHA256 payment signature.
  - `GET /fee/demands/cancelled-enrollment-ledger`: Displays refund entitlements under UGC guidelines.
  - `PATCH /fee/demands/:id/refund`: Authorizes caution deposit refund voucher.

---

## 7. Facilities, Campus Logistics & Auxiliary Operations Controllers

### `HostelController` (`apps/core-api/src/modules/hostel/hostel.controller.ts`)
- **Prefix**: `/hostel`
- **Endpoints**:
  - `GET /hostel/rooms`: Returns room occupancy matrix across blocks.
  - `POST /hostel/allocations`: Allocates room and bed to student; posts room rent fee.
  - `POST /hostel/vacate`: Executes check-out inspection, records damage claims, and clears No Dues.

### `TransportController` (`apps/core-api/src/modules/transport/transport.controller.ts`)
- **Prefix**: `/transport`
- **Endpoints**:
  - `POST /transport/routes`: Configures bus routes, stops, and morning pickup times.
  - `POST /transport/passes`: Generates digital QR transit pass for mobile app.
  - `GET /transport/verify-pass/:passNumber`: Conductor barcode scanner endpoint.

### `LibraryController` (`apps/core-api/src/modules/library/library.controller.ts`)
- **Prefix**: `/library`
- **Endpoints**:
  - `POST /library/books`: Catalogs book metadata and assigns Dewey call numbers.
  - `POST /library/issue`: Issues book copy to student Smart ID Card (14-day loan).
  - `POST /library/return`: Scans returned copy, calculates overdue fines, and updates shelf inventory.
  - `GET /library/no-dues/:studentId`: Checks zero outstanding loans and fines.

---

## 8. Documents, Canvas Designer & Verification Controllers

### `DocumentsController` & `DocumentExtrasController`
- **Prefix**: `/documents`
- **Endpoints**:
  - `GET /documents/templates`: Lists Canvas document templates.
  - `POST /documents/render`: Merges student runtime data with Canvas template to stream PDF.
  - `POST /documents/certificate-stock/batches`: Creates security parchment paper stock batches.
  - `POST /documents/certificate-stock/issue`: Issues degree with physical serial number and actor audit comment.
  - `GET /documents/verify/:serialNo`: Public unauthenticated verification endpoint returning document integrity attestation.

---

## 9. Specialized Auxiliary Controllers

### `AnalyticsController` & `MeController` (`apps/core-api/src/modules/analytics`)
- **Prefix**: `/analytics`
- **Endpoints**:
  - `GET /analytics/dashboard`: Returns executive institutional metrics (Enrollment Funnel, Fee Collection vs Receivables, Attendance Shortages, Pass Percentages).
  - `GET /analytics/me`: Returns user-specific workload, teaching performance, and task metrics.

### `BannersController` (`apps/core-api/src/modules/banners/banners.controller.ts`)
- **Prefix**: `/banners`
- **Endpoints**:
  - `POST /banners`: Publishes emergency campus broadcasts targeted by user role.
  - `POST /banners/:id/dismiss`: Tracks individual user acknowledgment receipt.

### `CounsellingController` (`apps/core-api/src/modules/counselling/counselling.controller.ts`)
- **Prefix**: `/counselling`
- **Endpoints**:
  - `POST /counselling/appointments`: Books confidential guidance session.
  - `POST /counselling/comments`: Records AES-256 encrypted clinical case notes.

### `BackupController` (`apps/core-api/src/modules/backup/backup.controller.ts`)
- **Prefix**: `/backup`
- **Endpoints**:
  - `POST /backup/create`: Spawns on-demand PostgreSQL compressed binary snapshot.
  - `GET /backup/list`: Lists available snapshots with SHA-256 hashes.
  - `POST /backup/restore/:id`: Restores database snapshot in single-user mode.

---
```
========================================================================================================================
END OF CATALOG: MASTER API CONTROLLER & REST ENDPOINT CATALOG (UERP-API-CATALOG-V4.2)
========================================================================================================================
```
