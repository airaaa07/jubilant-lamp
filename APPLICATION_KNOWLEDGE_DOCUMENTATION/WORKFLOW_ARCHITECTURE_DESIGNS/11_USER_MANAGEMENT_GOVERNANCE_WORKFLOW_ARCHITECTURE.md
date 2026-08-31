# Technical Workflow Architecture: User Management, Multi-Role Governance & Profile Pipelines

## Overview
This document details the technical workflow architecture, sequence diagrams, RBAC / scope resolution mechanics, and maker-checker approval pipelines for User Administration, Multi-Role Assignment, and Profile Governance.

---

## 🔄 End-to-End Sequence Diagram: Profile Governance Maker-Checker Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor Student as Enrolled Student
    participant GovC as ProfileGovernanceController
    participant GovS as ProfileGovernanceService
    participant MinIO as MinIO Storage
    participant DB as PostgreSQL Database
    actor Admin as Governance Approver / Registrar

    Student->>GovC: POST /api/profile-governance/submit { fieldName, proposedValue, proofFile }
    GovC->>MinIO: Upload Proof of Legal Correction
    GovC->>GovS: submitChangeRequest(dto, user)
    GovS->>DB: INSERT into profile_change_requests (status: 'PENDING', oldValue, proposedValue)
    GovS->>DB: INSERT into audit_logs (PROFILE_CHANGE_REQUESTED)
    DB-->>GovC: Return Request ID & Status 'PENDING'
    GovC-->>Student: Change Request Submitted for Verification

    Admin->>GovC: GET /api/profile-governance/pending
    GovC->>GovS: getPendingRequests()
    GovS->>DB: Query profile_change_requests WHERE status = 'PENDING'
    DB-->>Admin: List Pending Change Requests with Proof Documents

    Admin->>GovC: PATCH /api/profile-governance/:id/approve
    GovC->>GovS: approveRequest(id, admin)
    GovS->>DB: Transaction: UPDATE user/student_profile SET [fieldName] = proposedValue
    GovS->>DB: UPDATE profile_change_requests SET status = 'APPROVED', approved_by = admin.id
    GovS->>DB: INSERT into audit_logs (PROFILE_CHANGE_APPROVED)
    GovS-->>Student: In-App Notification: "Profile Update Approved & Applied"
```

---

## 🔄 Role & Scope Resolution Pipeline

```mermaid
flowchart TD
    Req["Incoming Request with JWT"] --> Extract["Extract User ID & Roles Array"]
    Extract --> RoleCheck{"Has Required Role?"}
    RoleCheck -- No --> Deny403["403 Forbidden: Missing Role"]
    RoleCheck -- Yes --> ScopeCheck{"Evaluate Tenant Scope"}
    
    ScopeCheck -- "SuperAdmin / UnivAdmin" --> GlobalAccess["Access Granted: University-Wide Scope"]
    ScopeCheck -- "InstAdmin" --> MatchInst{"User instituteId == Target instituteId?"}
    MatchInst -- Yes --> AllowInst["Access Granted: Institute Scope"]
    MatchInst -- No --> DenyInst["403 Forbidden: Institute Mismatch"]
    
    ScopeCheck -- "Faculty / Dept Head" --> MatchDept{"User departmentId == Target departmentId?"}
    MatchDept -- Yes --> AllowDept["Access Granted: Department Scope"]
    MatchDept -- No --> DenyDept["403 Forbidden: Department Mismatch"]
```

---

## 📊 Database Mutations & Entity Relationships

1. **`User` (`users`)**:
   - `id`, `email`, `password_hash`, `first_name`, `last_name`, `phone`, `is_active`, `locked_until`, `failed_login_attempts`, `must_change_password`, `university_id`, `institute_id`, `department_id`.
2. **`UserRoleAssignment` (`user_role_assignments`)**:
   - `id`, `user_id`, `role_id`, `scope` (`UNIVERSITY`, `INSTITUTE`, `DEPARTMENT`), `institute_id`, `department_id`.
3. **`ProfileChangeRequest` (`profile_change_requests`)**:
   - `id`, `user_id`, `field_name`, `current_value`, `proposed_value`, `justification`, `proof_document_url`, `status` (`PENDING`, `APPROVED`, `REJECTED`), `reviewer_id`, `reviewed_at`, `rejection_reason`.
