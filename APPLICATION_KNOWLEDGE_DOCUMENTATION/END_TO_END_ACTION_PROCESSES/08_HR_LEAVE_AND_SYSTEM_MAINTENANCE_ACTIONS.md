# Action Lifecycle Manual: HR Leave, Counselling & System Maintenance

## Action 8.1: Staff Leave Application, Approval & Timetable Rescheduling

### 1. Leave Application Submission
- **Role**: Faculty / Teaching Staff
- **Screen**: `LeaveRequestsPage.tsx`
- Selects Leave Type (Casual, Sick, Earned), Start Date, End Date, Reason.
- `POST /api/hr/leave-requests` -> checks remaining leave quota.

### 2. Approval & Automated Class Rescheduling
- HOD opens `LeaveRequestsPage.tsx` / `MyTasksPage.tsx`, clicks **Approve**.
- `PATCH /api/hr/leave-requests/:id { action: 'APPROVED' }`.
- `LeaveRescheduleService` automatically detects affected teaching timetable slots during leave period:
  - Assigns designated substitute faculty where configured.
  - Or moves slots to makeup pool and alerts students.

---

## Action 8.2: Student Counselling Session Lifecycle

### 1. Booking & Scheduling
- **Screen**: `CounsellingDeskPage.tsx` (Student View).
- Student picks counsellor and available slot -> `POST /api/counselling/sessions`.

### 2. Confidential Notes & Completion
- Counsellor opens `CounsellingDeskPage.tsx` -> conducts session -> records confidential encrypted clinical/academic notes -> `PATCH /api/counselling/sessions/:id`.

---

## Action 8.3: System Maintenance Lockout & Production Promotion

### 1. Maintenance Mode Activation
- **Screen**: `SettingsPage.tsx`.
- SuperAdmin enables maintenance toggle -> `POST /api/settings/maintenance { enabled: true }`.
- `MaintenanceGuard` intercepts subsequent non-SuperAdmin requests with `503 Service Unavailable`.

### 2. Production Promotion
- **Screen**: `SettingsPage.tsx` / System Status console.
- Calls `POST /api/auth/promote-to-production`:
  - Validates email SMTP configuration is active.
  - Rotates JWT signing secrets.
  - Revokes seed SuperAdmin credential.
  - Dispatches commissioning snapshot email to administrator.
