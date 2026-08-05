# Action Lifecycle Manual: HR, Audit & System Maintenance

## Action 8.1: Staff Multi-Tier Leave Request Approval

### 1. User Action & Frontend Trigger
- **User Role**: Lecturer / Staff (`role: Lecturer`)
- **Screen**: `LeaveRequestsPage.tsx`
- **User Input**: Selects Leave Type (Casual Leave), Start Date, End Date (3 days), Reason (`"Medical checkup"`).
- **Trigger**: Click **Submit Leave Application**.

### 2. Backend Logic & Guard Check (`HrService.applyLeave`)
- `POST /api/v1/hr/leave-requests`
- Checks `leave_balances.remaining_days` for employee.
- Verifies `remaining_days >= requestedDays`.

### 3. Database Mutations & Manager Approval
- `INSERT INTO leave_requests (id, staff_user_id, leave_type_id, days = 3, status = 'PENDING_HOD')`
- HOD opens `LeaveRequestsPage.tsx` -> Clicks **Approve**:
  - `UPDATE leave_requests SET status = 'APPROVED', approved_by = :hodUserId`
  - `UPDATE leave_balances SET used_days = used_days + 3, remaining_days = remaining_days - 3 WHERE staff_user_id = :id`

---

## Action 8.2: Automated Database Backup Dump & Maintenance Gate Lock

### 1. Trigger & Execution
- **Initiator**: SuperAdmin / Configured Backup Cron (`BackupService.runAutomatedBackup`)
- **Screen / API**: `SettingsPage.tsx` -> `POST /api/v1/backup/trigger`

### 2. Maintenance Mode Lock Phase
- `BackupService` sets system flag `MAINTENANCE_MODE = true`.
- `MaintenanceGuard` intercepts all incoming user requests:
  - Non-SuperAdmin API requests return **HTTP 503 Service Unavailable**.
  - `DashboardPage.tsx` displays overlay banner: `"System Undergoing Scheduled Maintenance"`.

### 3. Database Dump & Object Storage Upload
- Spawns child process `pg_dump -h localhost -U postgres -d university_erp | gzip > backup_2026-08-05.sql.gz`.
- Uploads compressed archive to MinIO `system-backups` S3 bucket.
- Verifies archive byte integrity and checksum.

### 4. Lock Release & Completion
- `INSERT INTO backup_records (file_key, size_bytes, checksum, status = 'VERIFIED')`
- `BackupService` resets `MAINTENANCE_MODE = false`.
- `MaintenanceGuard` releases request gate; normal API operations resume.
