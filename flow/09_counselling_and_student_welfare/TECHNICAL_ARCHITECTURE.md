# Module 09: Counselling & Student Welfare — Technical Architecture

> **Scope**: Counsellor contract lifecycle, privacy fence architecture, auto-assignment heuristics, and data models.

---

## 1. Counselling Data Models & Privacy Fence

Case notes recorded during mental health or personal counselling are protected by an encrypted application-level privacy fence. Regular teaching faculty and non-administrative staff have zero database or API read access to `CounsellingComment` rows.

```mermaid
erDiagram
    University ||--o{ Counsellor : "contracts"
    Counsellor ||--o{ CounsellorContract : "agrees to"
    Counsellor ||--o{ CounsellingRequest : "advises"
    Student ||--o{ CounsellingRequest : "seeks help in"
    CounsellingRequest ||--o{ CounsellingComment : "contains encrypted"
    Counsellor ||--o{ CounsellorEnrollmentCredit : "accrues"

    Counsellor {
        string id PK
        string userId FK
        string[] specializations
        int activeCaseCount
        decimal averageRating
        boolean isAvailable
    }

    CounsellingRequest {
        string id PK
        string studentId FK
        string counsellorId FK
        string category
        string urgency
        string status
        datetime assignedAt
        datetime resolvedAt
    }

    CounsellingComment {
        string id PK
        string counsellingRequestId FK
        string authorId FK
        string encryptedBody
        boolean isPrivateToCounsellor
        datetime createdAt
    }
```

---

## 2. Request Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> SUBMITTED: Student creates request
    SUBMITTED --> ASSIGNED: Auto-assignment or Admin assignment
    ASSIGNED --> SCHEDULED: Appointment date & meeting link confirmed
    SCHEDULED --> IN_SESSION: Live counselling meeting
    IN_SESSION --> COMPLETED: Recommendations & summary logged
    COMPLETED --> RATED: Student submits feedback rating
    RATED --> [*]
    
    ASSIGNED --> REASSIGNED: Counsellor unavailable / conflict of interest
    REASSIGNED --> ASSIGNED
```
