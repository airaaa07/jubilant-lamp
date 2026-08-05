# Technical Workflow Architecture: Admissions, Merit & Onboarding

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, state machine transitions, and database interactions for student application processing, document uploads, application fee payment, merit list ranking algorithms, seat allocation, and onboarding.

---

## 🔄 End-to-End Sequence Diagram: Admissions & Merit Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Applicant as Applicant / Student
    participant FormsC as FormsController
    participant MinIO as MinIO S3 Storage
    participant FeeS as FeeService
    participant PayG as Razorpay Payment Gateway
    participant WorkflowE as WorkflowEngineService
    participant MeritS as MeritListService
    participant DB as PostgreSQL Database

    Applicant->>FormsC: POST /api/v1/forms/submissions (Personal info, marks)
    FormsC->>MinIO: Upload Marksheets & Passports -> Store MinIO Object Key
    FormsC->>DB: INSERT into form_submissions (status: "SUBMITTED")
    
    FormsC->>FeeS: createApplicationFeeDemand(userId, programId)
    FeeS->>DB: INSERT into fee_demands (status: "PENDING")
    FormsC-->>Applicant: Application Submitted (Fee Pending)

    Applicant->>PayG: Execute Razorpay Payment
    PayG-->>FeeS: Payment Success Webhook Callback
    FeeS->>DB: UPDATE fee_demands status = "PAID", INSERT fee_ledger
    FeeS->>WorkflowE: triggerTransition("FEE_PAID")
    WorkflowE->>DB: UPDATE form_submissions status = "UNDER_REVIEW"

    note over MeritS: Admission Coordinator Executes Merit Processing
    MeritS->>DB: Query form_submissions WHERE status = "UNDER_REVIEW"
    MeritS->>MeritS: Execute Rank Calculation Algorithm (Qualifying Marks + Cutoff)
    MeritS->>DB: INSERT into merit_lists & merit_list_candidates
    MeritS->>DB: UPDATE form_submissions status = "OFFERED"

    Applicant->>FormsC: Accept Admission Offer & Submit Onboarding Form
    FormsC->>DB: UPDATE users role = "Student", create StudentProfile record
    FormsC->>DB: INSERT into student_onboarding_progress
```

---

## 🔀 Application State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Fill Application Form
    DRAFT --> SUBMITTED: Submit Form
    SUBMITTED --> FEE_PENDING: Demand Created
    FEE_PENDING --> UNDER_REVIEW: Application Fee Paid
    UNDER_REVIEW --> MERIT_LISTED: Evaluated & Ranked
    UNDER_REVIEW --> REJECTED: Ineligible / Criteria Failed
    MERIT_LISTED --> OFFERED: Seat Allocated
    MERIT_LISTED --> WAITLISTED: Capacity Full
    WAITLISTED --> OFFERED: Seat Vacuum Available
    OFFERED --> ADMITTED: Offer Accepted & Onboarding Completed
    OFFERED --> EXPIRED: Decision Deadline Elapsed
    ADMITTED --> [*]
```

---

## 📊 Database Mutations & Entity Relationships

1. **`FormSubmission`**:
   - Created with `formTemplateId`, `data` (JSON of form answers), `status`.
   - Transitions: `SUBMITTED` -> `FEE_PENDING` -> `UNDER_REVIEW` -> `OFFERED` -> `ADMITTED`.
2. **`MeritList` & `MeritListCandidate`**:
   - `MeritList`: Scoped to `programId` and `academicYearId`.
   - `MeritListCandidate`: Stores `rank`, `score`, `category`, and seat allocation status (`ALLOCATED`, `WAITLISTED`, `REJECTED`).
3. **`StudentProfile` & `User`**:
   - Upon offer acceptance (`ADMITTED` state):
     - `UPDATE users SET role = 'Student', is_active = true`
     - `INSERT INTO student_profiles (user_id, enrollment_number, roll_number, stream_label_id, batch_id)`
