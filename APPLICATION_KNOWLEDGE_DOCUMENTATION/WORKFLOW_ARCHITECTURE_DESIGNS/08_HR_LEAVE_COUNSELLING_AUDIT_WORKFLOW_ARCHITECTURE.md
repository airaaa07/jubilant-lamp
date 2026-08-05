# Technical Workflow Architecture: HR, Leave, Audit & Maintenance

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, leave approval hierarchies, field-level Prisma audit logging middleware, and database backup/restore maintenance gate modes.

---

## 🔄 End-to-End Sequence Diagram: Staff Leave Approval Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Staff as Staff Member / Faculty
    actor Manager as HOD / Reporting Manager
    actor HR as HR Admin
    participant HrC as HrController
    participant HrS as HrService
    participant DB as PostgreSQL Database

    Staff->>HrC: POST /api/v1/hr/leave-requests (Submit Leave Application)
    HrS->>DB: Check Leave Balance for LeaveType (Casual / Sick)
    
    alt Insufficient Leave Balance
        HrS-->>Staff: Throw 400 Bad Request ("Insufficient balance")
    else Balance Available
        HrS->>DB: INSERT into leave_requests (status: "PENDING_HOD")
        HrS-->>Staff: Leave Request Submitted
    end

    Manager->>HrC: POST /api/v1/hr/leave-requests/:id/action (Approve/Reject)
    
    alt Approved by HOD
        HrS->>DB: UPDATE leave_requests status = "APPROVED"
        HrS->>DB: UPDATE leave_balances SET used_days = used_days + N, remaining_days = remaining_days - N
    else Rejected by HOD
        HrS->>DB: UPDATE leave_requests status = "REJECTED", rejection_reason
    end
```

---

## 🛡️ Field-Level Prisma Audit Logging Architecture

All database write operations pass through the custom `PrismaService` audit middleware:

```mermaid
flowchart TD
    Operation["Prisma Write Action<br/>(create, update, delete, upsert, updateMany)"] --> FetchOld["1. Fetch Current Record State (if update/delete)"]
    FetchOld --> ExecOp["2. Execute Database Transaction"]
    ExecOp --> FetchNew["3. Extract New Record State"]
    FetchNew --> ComputeDiff["4. Compute JSON Field-Level Diffs<br/>(oldValues vs newValues)"]
    ComputeDiff --> WriteAudit["5. INSERT into audit_logs<br/>(userId, action, entityName, entityId, oldValues, newValues, ipAddress)"]
```

---

## ⚙️ Maintenance Mode & Backup Restore Gate Architecture

When a database backup or restore procedure is triggered by SuperAdmin (`BackupService`):

1. **Gate Engagement**: Sets system state `MAINTENANCE_MODE = true`.
2. **Request Interception**: `MaintenanceGuard` intercepts all incoming requests to `core-api`:
   - Checks `req.user.roles`.
   - **SuperAdmin Account**: Allowed access to monitor restore progress.
   - **Health Check (`/api/v1/health`)**: Allowed for infrastructure monitoring.
   - **All Other Users**: Intercepted and returned **HTTP 503 Service Unavailable** with message `"System is currently undergoing scheduled database maintenance. Please try again shortly."`
3. **Completion & Lock Release**: Upon successful verification of database dump restoration, `MAINTENANCE_MODE` is reset to `false` and normal request routing resumes.
