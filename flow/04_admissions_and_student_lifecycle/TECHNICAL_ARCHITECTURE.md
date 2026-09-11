# Module 04: Admissions & Student Lifecycle — Technical Architecture

> **Scope**: Complete lifecycle state machines from Applicant to Student to Alumni, Seat Master capacity reservation equations, and rollback boundaries.

---

## 1. Student Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> REGISTERED: Public /register (Role: Applicant)
    REGISTERED --> APPLICATION_DRAFT: Start Application Form
    APPLICATION_DRAFT --> PENDING_PAYMENT: Submit Details & Documents
    PENDING_PAYMENT --> UNDER_REVIEW: Application Fee Paid (Razorpay)
    
    state UNDER_REVIEW {
        [*] --> DocumentVerification
        DocumentVerification --> EligibilityApproved: Documents Verified
        DocumentVerification --> Deficient: Document Defective (Re-upload requested)
        Deficient --> DocumentVerification: Applicant Re-uploads
    }

    EligibilityApproved --> MERIT_RANKED: Merit Formula Calculated
    MERIT_RANKED --> SEAT_OFFERED: Within Cutoff Rank
    SEAT_OFFERED --> ADMITTED: Admission Fee Paid & Offer Accepted
    SEAT_OFFERED --> OFFER_EXPIRED: Acceptance Deadline Lapsed
    
    ADMITTED --> ENROLLED: OnboardStudentsPage (Role: Student)
    
    state ENROLLED {
        [*] --> ActiveStudies
        ActiveStudies --> OnboardingReverted: SuperAdmin/InstAdmin "Remove a student" (Commit f6baee56)
        ActiveStudies --> TermPromoted: Progresses Terms
        ActiveStudies --> Suspended: Disciplinary Action
        Suspended --> ActiveStudies: Reinstated
    }

    OnboardingReverted --> SEAT_OFFERED: Restored for Correction
    TermPromoted --> GRADUATED: Final Degree Requirements Completed
    GRADUATED --> ALUMNI: Convocation & Alumni Registry
    ALUMNI --> [*]
```

---

## 2. Seat Master Accounting Equations

The Seat Master tracks three concurrent metrics to prevent over-admission while honoring statutory intake limits set by regulatory bodies (AICTE, UGC, Bar Council, etc.).

$$\text{Approved Intake} \ge \text{Target Batch Size}$$
$$\text{Available Capacity} = \text{Target Batch Size} - (\text{Filled / Enrolled} + \text{Active Unexpired Offers})$$

```mermaid
flowchart TD
    Approved["Statutory Approved Intake<br/>(e.g., 120 seats)"] --> Size["Configured Batch Size<br/>(e.g., 120 seats)"]
    Size --> Allocated["Total Allocated"]
    Allocated --> Filled["Filled / Enrolled Students<br/>(Active Student records)"]
    Allocated --> Offered["Offered Seats<br/>(Offers issued, pending payment deadline)"]
    Size --> Available["Available Open Seats<br/>(Batch Size - Filled - Offered)"]
```

---

## 3. Profile Governance & Change Request Architecture

Student personal details (Name, DOB, Parent Names, Category) are legally governed. Once enrolled, a student cannot directly mutate their profile; changes must pass through a governed workflow.

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant Portal as StudentProfilePage.tsx
    participant API as ProfileGovernanceController
    participant Admin as InstAdmin / Registrar
    participant DB as Prisma (ProfileChangeRequest & Log)

    Student->>Portal: Requests Name Correction (Uploads Gazette Notification)
    Portal->>API: POST /api/profile-governance/requests { field: "legalName", newValue: "...", proofDocId }
    API->>DB: profileChangeRequest.create({ status: "PENDING_APPROVAL" })
    API-->>Portal: Toast: "Change request submitted for registrar approval"
    Admin->>API: GET /api/profile-governance/requests
    Admin->>API: PATCH /api/profile-governance/requests/:id/approve
    API->>DB: $transaction [
        1. Update Student / User legalName
        2. Set profileChangeRequest.status = 'APPROVED'
        3. Insert into ProfileChangeLog for permanent legal audit trail
    ]
    API-->>Admin: Success
    API->>Student: Notification: "Profile update approved"
```
