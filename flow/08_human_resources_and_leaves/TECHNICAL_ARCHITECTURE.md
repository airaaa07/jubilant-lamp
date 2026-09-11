# Module 08: Human Resources & Leaves — Technical Architecture

> **Scope**: Leave balance accounting algorithms, substitute faculty scheduling integration, multi-level approval workflows, and staff entity relationships.

---

## 1. HR & Staff Entity Relationships

```mermaid
erDiagram
    Department ||--o{ Staff : "employs"
    Staff ||--o{ StaffSubject : "teaches"
    Staff ||--o{ LeaveApplication : "submits"
    Staff ||--o{ LeaveBalance : "holds annual quotas"
    Staff ||--o{ StaffDocument : "stores credentials"
    LeaveType ||--o{ LeaveApplication : "categorizes"
    LeaveType ||--o{ LeaveBalance : "allocates"

    Staff {
        string id PK
        string userId FK
        string employeeCode UK
        string designation
        string staffType
        datetime joiningDate
        boolean isActive
    }

    LeaveBalance {
        string id PK
        string staffId FK
        string leaveTypeId FK
        int year
        decimal totalAllocated
        decimal consumedDays
        decimal remainingDays
    }

    LeaveApplication {
        string id PK
        string staffId FK
        string leaveTypeId FK
        datetime startDate
        datetime endDate
        decimal totalDays
        string status
        string substituteStaffId
    }
```

---

## 2. Leave Approval State Machine

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Staff prepares application
    DRAFT --> PENDING_SUBSTITUTE: Applied with substitute faculty
    PENDING_SUBSTITUTE --> PENDING_HOD: Substitute faculty accepts lecture swap
    PENDING_SUBSTITUTE --> REJECTED: Substitute faculty declines
    
    PENDING_HOD --> APPROVED: HOD approves (<= 3 days)
    PENDING_HOD --> PENDING_REGISTRAR: HOD endorses (> 3 days or Long Leave)
    PENDING_REGISTRAR --> APPROVED: Registrar sanctions
    
    PENDING_HOD --> REJECTED: HOD declines with remarks
    PENDING_REGISTRAR --> REJECTED: Registrar declines

    APPROVED --> CANCELLED: Staff cancels before start date (Balance restored)
    APPROVED --> TAKEN: Leave window passes
    TAKEN --> [*]
```
