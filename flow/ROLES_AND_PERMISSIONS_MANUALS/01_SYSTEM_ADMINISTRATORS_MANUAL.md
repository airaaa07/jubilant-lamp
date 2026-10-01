# System Administrators Master Operating Manual & Standard Operating Procedures (SOP)
## Authoritative Technical Playbook for SuperAdmin, UnivAdmin, and InstAdmin Personas

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-SOP-SYSADMIN-V4.2
CLASSIFICATION: CONFIDENTIAL // ENTERPRISE SYSTEM ADMINISTRATION MANUAL
AUTHORITY: OFFICE OF THE CHIEF INFORMATION OFFICER & PRINCIPAL ENTERPRISE ARCHITECT
APPLIES TO: MULTI-TENANT CLOUD, HYBRID CAMPUS & ON-PREMISE PRIVATE CLUSTER DEPLOYMENTS
========================================================================================================================
```

---

## 1. Governance Architecture & Multi-Tenant Security Hierarchy

UniversityERP is architected to support complex multi-campus university systems, collegiate consortiums, and affiliated state university networks. Administrative authority is segmented into three distinct, non-overlapping operational tiers:

```
+--------------------------------------------------------------------------------------------------------------------+
|                                      GLOBAL MULTI-TENANT CLUSTER RUNTIME                                           |
+--------------------------------------------------------------------------------------------------------------------+
                                                          |
                                                          v
                                     +------------------------------------------+
                                     |         Tier 1: SuperAdmin (Root)        |
                                     |  - Multi-tenant tenant lifecycle         |
                                     |  - Database snapshots, backup & restore  |
                                     |  - Global maintenance mode & banners     |
                                     |  - User impersonation & security audit   |
                                     +------------------------------------------+
                                                          |
                                  +-----------------------+-----------------------+
                                  |                                               |
                                  v                                               v
              +---------------------------------------+       +---------------------------------------+
              |    Tier 2: UnivAdmin (University A)   |       |    Tier 2: UnivAdmin (University B)   |
              |  - Central statutory degree catalog   |       |  - Central statutory degree catalog   |
              |  - Multi-campus fee head definitions  |       |  - Multi-campus fee head definitions  |
              |  - Central user RBAC & policies       |       |  - Central user RBAC & policies       |
              |  - DLT SMS communication gateways     |       |  - DLT SMS communication gateways     |
              +---------------------------------------+       +---------------------------------------+
                                  |                                               |
                +-----------------+-----------------+                             +-----------+
                |                                   |                                         |
                v                                   v                                         v
+-------------------------------+   +-------------------------------+         +-------------------------------+
|  Tier 3: InstAdmin (Campus 1) |   |  Tier 3: InstAdmin (Campus 2) |         |  Tier 3: InstAdmin (Campus 3) |
|  - Batches, Sections & Intake |   |  - Batches, Sections & Intake |         |  - Batches, Sections & Intake |
|  - Seat Master live ledger    |   |  - Seat Master live ledger    |         |  - Seat Master live ledger    |
|  - Timetable & Room grids     |   |  - Timetable & Room grids     |         |  - Timetable & Room grids     |
|  - Campus fee collections     |   |  - Campus fee collections     |         |  - Campus fee collections     |
+-------------------------------+   +-------------------------------+         +-------------------------------+
```

---

## 2. The SuperAdmin Persona (Global Infrastructure & Platform Root)

### 2.1 Role Profile & Cryptographic Authority
- **Canonical Role String**: `SuperAdmin`
- **Scope Identifier**: `university` (with runtime `bypassTenantCheck = true`)
- **Assigned Identities**: Enterprise Infrastructure Engineers, Chief Information Security Officer (CISO), Principal Site Reliability Engineers (SRE).
- **Core Security Directives**:
  - SuperAdmin accounts **must** enforce Hardware Token / Multi-Factor Authentication (MFA).
  - All SuperAdmin API invocations are permanently logged to `AuditLog` with remote IP address, TLS cipher suite, and user agent.
  - SuperAdmin credentials bypass all standard `RolesGuard` and `ModuleAccessGuard` checks via `roles.util.ts`:
    ```typescript
    if (user.roles.includes('SuperAdmin') || user.applicationRole === 'SuperAdmin') return true;
    ```

---

### 2.2 Standard Operating Procedure: Initial Platform Provisioning & Seeding (SOP-ADM-001)

When spinning up a new institutional environment or deploying a new multi-tenant database:

#### Step 1: Environment Variables Validation
Ensure `/apps/core-api/.env` contains mandatory production secrets:
```bash
# Database & Connection Pooling
DATABASE_URL="postgresql://postgres:SecureVaultPass2026@pg-cluster.internal:5432/university_erp?schema=public&connection_limit=50&pool_timeout=20"
REDIS_URL="redis://:RedisVaultAuth2026@redis-cluster.internal:6379/0"

# Cryptographic Keys
JWT_SECRET="c8e1f3a5b7d902468ace013579bdf2468ace013579bdf2468ace013579bdf246"
JWT_REFRESH_SECRET="e9f2a4b6c8d013579bdf02468ace13579bdf02468ace13579bdf02468ace1357"
ENCRYPTION_KEY="32_BYTE_HEX_KEY_FOR_AES_256_GCM_ENCRYPTED_FIELDS"

# S3 / Object Storage
MINIO_ENDPOINT="s3.internal.university.edu"
MINIO_PORT="9000"
MINIO_ACCESS_KEY="UERP_MINIO_ADMIN"
MINIO_SECRET_KEY="SecureMinIOClusterSecret2026"
MINIO_BUCKET="university-erp-vault"
```

#### Step 2: Database Migration Deployment
Execute Prisma schema migrations without running destructive schema push:
```bash
cd /home/admin/UniversityERP/apps/core-api
npx prisma migrate deploy
```
*Verification Check*: Query PostgreSQL to confirm 138 relational tables exist:
```sql
SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';
-- Expected result: 138
```

#### Step 3: Sequential Idempotent Seeding
Execute the master institutional seeders in strict topological order:
```bash
# 1. SuperAdmin Root Account
node prisma/seed-superadmin.js

# 2. Universal RBAC Roles & Scopes
node prisma/seed-roles.js

# 3. Security Defaults, Password Policies & System Config
node prisma/seed-config.js
node prisma/seed-settings.js

# 4. Canonical Academic Degree Catalog
node prisma/seed-catalog.js

# 5. Document Canvas Templates & Security Certificate Formats
node prisma/seed-document-templates.js

# 6. Workflow Engines (Admissions, Document Verification, Leaves, Reservations)
node prisma/seed-workflow-admission.js
node prisma/seed-workflow-leave.js
node prisma/seed-workflow-reservations.js
```

---

### 2.3 Standard Operating Procedure: Live User Impersonation (SOP-ADM-002)

To troubleshoot complex production anomalies without requesting user passwords or violating privacy statutes:

```mermaid
sequenceDiagram
    autonumber
    actor SA as SuperAdmin
    participant UI as Universal Admin Shell
    participant API as Core API Gateway
    participant AUD as Audit Log Engine
    actor TARGET as Target User Profile

    SA->>UI: Clicks "Impersonate User" in top navigation bar
    UI->>SA: Displays User Search Modal (Email / Emp ID / Enr No)
    SA->>UI: Enters search query "2024CSE0042" (Student)
    UI->>API: POST /auth/impersonate { targetUserId: "usr_8f91a2b" }
    API->>API: Validates caller holds 'SuperAdmin' role
    API->>AUD: Appends immutable AuditLog record (Action: IMPERSONATE_START)
    API->>UI: Issues ephemeral 15-minute JWT with "impersonatedBy" claim
    UI->>UI: Re-renders viewport as Target User with Amber Header Banner
    SA->>UI: Inspects exact broken UI state, form validation, or marks discrepancy
    SA->>UI: Clicks "Exit Impersonation" on Banner
    UI->>API: POST /auth/impersonate/exit
    API->>AUD: Appends AuditLog record (Action: IMPERSONATE_END)
    UI->>UI: Restores original SuperAdmin authentication session
```

#### Operational Rules for Impersonation:
1. **Financial Transaction Invalidation**: Financial payments (Razorpay checkout) are automatically disabled during impersonated sessions to prevent fraud.
2. **Read-Only Enforced Actions**: Any profile modifications executed under impersonation require a mandatory audit reason prompt.
3. **Audit Trail Immutability**: The resulting `AuditLog` row stores:
   - `action`: `'IMPERSONATE'`
   - `userId`: Target user ID
   - `impersonatedBy`: SuperAdmin primary user ID
   - `ipAddress`: Originating IP
   - `metadata`: Reason entered by the SuperAdmin.

---

### 2.4 Standard Operating Procedure: Disaster Recovery, Snapshots & Restores (SOP-ADM-003)

#### Creating a Pre-Cutover Backup Snapshot
1. Navigate to `/settings` $\to$ **Backup & Disaster Recovery**.
2. Click **Create Manual Snapshot**.
3. Select Backup Profile:
   - **Full Database Snapshot** (Schema, Data, RBAC, Configurations).
   - **Data-Only Export** (Excludes table definitions).
   - **Configuration Only** (Excludes student transaction records).
4. System invokes `backup.controller.ts` $\to$ spawns background worker executing:
   ```bash
   pg_dump -h pg-cluster.internal -U postgres -d university_erp -Fc -f /backups/snapshot_2026_09_11_T1400.dump
   ```
5. File is validated with SHA-256 hash and uploaded to encrypted MinIO disaster recovery bucket.

#### Executing a Point-in-Time Database Restore
> [!CAUTION]
> A database restore terminates all active connections, rolls back state, and replaces relational tables. This procedure must only be authorized during catastrophic data corruption or planned disaster recovery drills.

1. SuperAdmin activates **Maintenance Mode** across all university portals.
2. Navigates to `/settings` $\to$ **Backup & Disaster Recovery** $\to$ **Snapshot Catalog**.
3. Locates target verified snapshot (e.g. `snapshot_2026_09_11_T1400.dump`).
4. Clicks **Restore Snapshot**.
5. Modal demands typed confirmation: `RESTORE-DATABASE-CONFIRM`.
6. System terminates active client connections via PgBouncer:
   ```sql
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'university_erp' AND pid <> pg_backend_pid();
   ```
7. Executes `pg_restore --clean --if-exists -d university_erp /backups/snapshot_2026_09_11_T1400.dump`.
8. Runs post-restore integrity script (`/scripts/verify-integrity.ts`):
   - Validates row counts across `University`, `Student`, `User`, `FeeLedger`.
   - Confirms foreign key parity.
9. Disables Maintenance Mode; broadcasts system restoration notice.

---

## 3. The UnivAdmin Persona (Central University IT Director)

### 3.1 Scope & Authority
- **Canonical Role String**: `UnivAdmin`
- **Scope Identifier**: `university`
- **Assigned Identities**: University Registrar IT, Director of Academic Computing, University System Governance Team.
- **Authority**: Full administrative purview over all constituent colleges, schools, institutes, degree programs, fee heads, and centralized user authentication policies.

---

### 3.2 Standard Operating Procedure: Master Academic Catalog Governance (SOP-ADM-004)

The statutory academic hierarchy of UniversityERP is strictly modeled in `schema.prisma`:

```
  University (Root Charter)
      │
      ├── UniversityDepartment (e.g. FOE - Faculty of Engineering)
      │       │
      │       └── UniversityCourse (e.g. BTECH - Bachelor of Technology)
      │               │
      │               └── UniversityStream (e.g. CSE - Computer Science & Engineering)
      │                       │
      │                       ├── StreamLabel (NEP 2020 Rules, Credits, Grading)
      │                       └── UniversitySubject (Canonical Curriculum Syllabus)
```

#### Step-by-Step Catalog Configuration via `/master-data`:
1. **Create Statutory School / Faculty**:
   - Navigate to `/master-data` $\to$ **University Departments**.
   - Click **Add Department**.
   - Input:
     - Department Code: `FOE`
     - Legal Name: `Faculty of Engineering & Technology`
     - Short Name: `FOE`
     - Is Academic: `Checked (true)`
2. **Create Statutory Degree**:
   - Select `FOE` $\to$ Navigate to **Courses (Degrees)** tab.
   - Click **Add Course**.
   - Input:
     - Course Code: `BTECH`
     - Legal Name: `Bachelor of Technology`
     - Duration: `4 Years`
3. **Create Degree Specialization / Stream**:
   - Select `BTECH` $\to$ Navigate to **Streams (Programs)** tab.
   - Click **Add Stream**.
   - Input:
     - Stream Code: `CSE`
     - Name: `Computer Science & Engineering`
     - Regulated By: `AICTE`
     - Stream Type: `Regular`
4. **Configure the 5-Tab Program Label Designer**:
   - Select `CSE` $\to$ Click **Edit Program Label Rules** (`StreamLabel`):
     - **Tab 1: Basic Information**: Academic Year (`2026`), Curriculum Version (`v01`), Medium (`English`).
     - **Tab 2: Term Structure**: Unit Name (`Semester`), Unit Count (`8 Terms`), Total Graduation Credits (`160 Credits`).
     - **Tab 3: Academic Thresholds**:
       - Minimum Passing Aggregate: `50.0%`
       - Minimum Passing Grade Point: `5.0 / 10.0`
       - Statutory Minimum Attendance: `75.0%`
     - **Tab 4: Letter Grade Boundaries**:
       - `O` (Outstanding): 90%–100% (Grade Point: 10)
       - `A+` (Excellent): 80%–89% (Grade Point: 9)
       - `A` (Very Good): 70%–79% (Grade Point: 8)
       - `B+` (Good): 60%–69% (Grade Point: 7)
       - `B` (Above Average): 55%–59% (Grade Point: 6)
       - `C` (Average): 50%–54% (Grade Point: 5)
       - `F` (Fail): Below 50% (Grade Point: 0)
     - **Tab 5: Document Layouts**: Bind default Canvas marksheet and degree certificate layouts.
   - Click **Publish Program Label**.

---

### 3.3 Standard Operating Procedure: Central Security Policy Configuration (SOP-ADM-005)

Enforced via the Security Gear Modal on `/users` (`UserManagementSettingsModal.tsx`):

```
+----------------------------------------------------------------------------------------------------+
|                                    SECURITY POLICY CONFIGURATION                                   |
+----------------------------------------------------------------------------------------------------+
  [1] Account Brute-Force & Lockout Rules
      * Failed Login Threshold: 5 failed attempts
      * Lockout Duration: 30 minutes
      * Reset Counter Window: 15 minutes of zero failed activity
      * Action on Lockout: IP recorded, Account state locked, SMS alert sent to registered mobile

  [2] Cryptographic Password Entropy Standards
      * Minimum Password Length: 12 characters (Admin/Finance), 8 characters (Student)
      * Complexity: At least 1 uppercase, 1 lowercase, 1 numeral, 1 special symbol (!@#$%^&*)
      * Password History Memory: Disallow reuse of last 5 previous passwords (via `PasswordHistory`)
      * Expiration Interval: 90 days for administrative roles; 180 days for faculty

  [3] Session Security & Inactivity Governance
      * Inactivity Idle Timeout: 15 minutes (Finance/Cashier), 60 minutes (Faculty/Student)
      * Absolute Session Lifespan: Maximum 8 hours (forces daily re-authentication)
      * Concurrent Session Policy: Terminate prior active session on new device login
+----------------------------------------------------------------------------------------------------+
```

---

### 3.4 Standard Operating Procedure: TRAI DLT SMS & Telephony Setup (SOP-ADM-006)

To comply with the Telecom Regulatory Authority of India (TRAI) Distributed Ledger Technology (DLT) regulations for institutional transactional messaging:

1. Navigate to `/settings` $\to$ **SMS & Communication Gateway**.
2. Register Enterprise Header:
   - Entity ID (`PE_ID`): Registered Principal Entity ID from telecom operator (e.g. Jio / Airtel DLT).
   - Sender Header (`HEADER_ID`): Approved 6-alpha header (e.g. `UNIVER`).
3. Configure 4-Column Template Layout in UI:
   - **Column 1: Template Identifier**: Unique internal event key (e.g. `ADMISSION_OFFER_ALERT`).
   - **Column 2: DLT Template ID**: 12-digit telecom approved numeric string (e.g. `110716892041235`).
   - **Column 3: Static Body with Dynamic Placeholders**:
     ```
     Dear {#var#}, congratulations! You have been offered admission to {#var#} at STU. Pay fees before {#var#}: {#var#} - UNIVER
     ```
   - **Column 4: Variable Mapping**: Map `{#var#}` sequentially to `[student.firstName, academic.programme, fees.dueDate, paymentUrl]`.
4. Click **Test Dispatch**: Sends live test SMS to specified mobile number and verifies delivery receipt callback (`NotificationLog`).

---

## 4. The InstAdmin Persona (Constituent Campus Director / Principal IT)

### 4.1 Scope & Authority
- **Canonical Role String**: `InstAdmin`
- **Scope Identifier**: `institute` (Evaluated via `canAccessInstitute(user, instituteId)`)
- **Assigned Identities**: College Principals, Academic Deans, Campus Operations Directors.
- **Authority**: Unrestricted governance over the specific constituent campus: batches, classroom sections, faculty course assignments, local fee demands, and facility allocations.

---

### 4.2 Standard Operating Procedure: Setting Up an Incoming Academic Batch (SOP-ADM-007)

When onboarding a new academic cohort for the upcoming academic year:

1. Navigate to `/master-data` $\to$ **Institute Academic Tree**.
2. Select Constituent College $\to$ Select Department (e.g. `DEPT_CSE`) $\to$ Select Programme (`BTECH_CS`).
3. Select Specialization (`CSE_CORE`) $\to$ Click **Create Batch**:
   - Batch Cohort Name: `B.Tech CSE 2026-2030`
   - Admission Year: `2026`
   - Initial Semester: `Semester I`
   - Year Index: `1`
   - Statutory Intake Capacity: `120 Students`
4. Create Classroom Sections:
   - Section 1: Name: `Section A`, Maximum Size: `60 Students`, Assigned Classroom: `Hall 101`.
   - Section 2: Name: `Section B`, Maximum Size: `60 Students`, Assigned Classroom: `Hall 102`.
5. Map Curriculum Version:
   - Link Batch to published University Stream Label (`CSE_2026_v01`).
   - System automatically generates `BatchTerm` records (Terms 1 through 8) and populates `BatchTermSubject` containers.

---

### 4.3 Standard Operating Procedure: Seat Master Governance & Compliance Audits (SOP-ADM-008)

To ensure campus admissions strictly adhere to state regulatory quotas without over-enrolling:

```mermaid
flowchart TD
    START[Open /admissions/seat-master] --> TREE[Expand Campus Hierarchy Tree]
    TREE --> AUDIT[Inspect Approved Intake Pool vs Allocated Batch Seats]
    AUDIT --> CHECK{Sum of Sections <= Approved Pool?}
    
    CHECK -->|Yes: Compliant| EXPORT[Export Capacity Report]
    EXPORT --> PDF[Generate Official PDF with Campus Stamp]
    EXPORT --> XLSX[Generate Master Excel Spreadsheet]
    
    CHECK -->|No: Breach Detected| REVISE[Reduce Section Capacity or Apply for Approval]
    REVISE --> REQ[POST /admissions/seat-master/approvals]
    REQ --> REG_SIGN[Forward to University Registrar for Sanction]
```

#### Step-by-Step UI Execution:
1. InstAdmin opens `/admissions/seat-master`.
2. Inspects live statistics cards:
   - **Total University Approved Intake**: e.g., 480 Seats.
   - **Currently Allocated in Batches**: e.g., 420 Seats.
   - **Unallocated Buffer**: e.g., 60 Seats.
   - **Matriculated Students**: e.g., 395 Students.
3. If additional quota was sanctioned by the state government:
   - Click **Add Statutory Approval** (`POST /admissions/seat-master/approvals`).
   - Inputs: Approved Seats (`+30`), Effective Date (`2026-06-01`), Regulatory Order Attachment URL (`order_aicte_2026_42.pdf`).
4. Generates regulatory compliance exports:
   - Click **Export Seat Master** $\to$ Select **PDF Report** (renders formatted table with institutional header, approval order references, and digital signature lines for AICTE inspectors).

---

## 5. Administrative Error Handling & Incident Runbooks

### 5.1 Incident Runbook: Resolving Database Lock Contention (INC-ADM-001)
- **Symptom**: API requests timing out (`504 Gateway Timeout`); logs show `PrismaClientKnownRequestError: P2028: Transaction API error: Transaction already closed`.
- **Diagnostic Command**:
  ```sql
  SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
  FROM pg_stat_activity
  WHERE state <> 'idle' AND now() - pg_stat_activity.query_start > interval '30 seconds';
  ```
- **Resolution**:
  1. Identify offending PID holding row-level locks on `FeeDemand` or `Student`.
  2. Terminate the blocking backend PID:
     ```sql
     SELECT pg_cancel_backend(blocking_pid);
     -- If stubborn:
     SELECT pg_terminate_backend(blocking_pid);
     ```
  3. Inspect Redis BullMQ job queues for stalled batch charging jobs (`bull:fee-charge:stalled`).

---

### 5.2 Incident Runbook: Restoring an Accidentally Deleted User Profile (INC-ADM-002)
- **Symptom**: Clerk reports accidental student onboarding removal.
- **Architectural Safeguard**: UniversityERP enforces guarded deletion (`onboarding.service.ts:lookupForDelete`). If the student carries any marks, attendance, fee demands, or documents, deletion is **hard-rejected**.
- **If Base Record Deleted**:
  1. SuperAdmin inspects `AuditLog` where `entity = 'Student'` and `action = 'DELETE'`.
  2. Retrieves pre-deletion JSON payload stored in `AuditLog.oldValues`.
  3. Executes idempotent restore script using the JSON payload via `POST /onboarding/students/commit`.

---
```
========================================================================================================================
END OF MANUAL: SYSTEM ADMINISTRATORS MASTER OPERATING MANUAL (UERP-SOP-SYSADMIN-V4.2)
========================================================================================================================
```
