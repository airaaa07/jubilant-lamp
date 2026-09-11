# Module 02: Master Data & Academic Structure — Technical Architecture

> **Scope**: Academic entity relationship hierarchy, cascading lifecycle constraints, configurable academic structure (custom level names and disable-able middle layer per commit `0d04842c`), and transaction boundaries.

---

## 1. Academic Hierarchy & Entity Relationships

The academic hierarchy supports multi-tenant university environments with flexible tier configurations.

```mermaid
erDiagram
    University ||--o{ Institute : "contains"
    University ||--o{ UniversityDepartment : "defines global"
    University ||--o{ UniversityCourse : "defines global"
    University ||--o{ UniversityStream : "defines global"
    University ||--o{ UniversitySubject : "defines global"
    
    Institute ||--o{ Department : "operates"
    Institute ||--o{ InstituteResource : "owns physical assets"
    Department ||--o{ Programme : "hosts"
    Programme ||--o{ Course : "offers"
    Course ||--o{ Batch : "runs cohorts"
    Batch ||--o{ BatchTerm : "progresses through terms"
    BatchTerm ||--o{ Section : "subdivides into"
    BatchTerm ||--o{ BatchTermSubject : "teaches subjects in"

    University {
        string id PK
        string code UK
        string name
        json config
    }

    Institute {
        string id PK
        string universityId FK
        string code
        string name
        boolean isActive
    }

    Programme {
        string id PK
        string departmentId FK
        string code
        string name
        int totalTerms
    }

    Batch {
        string id PK
        string courseId FK
        string name
        int startYear
        int endYear
        int intakeCapacity
    }

    BatchTerm {
        string id PK
        string batchId FK
        int termNumber
        string name
        string status
        boolean isLocked
    }
```

---

## 2. Configurable Academic Hierarchy (Commit `0d04842c`)

Universities can configure custom naming conventions (e.g., "Faculty" vs "School" vs "Institute", or "Department" vs "Division") and optionally disable the middle layer (e.g. running Programmes directly under Institutes without Departments).

```mermaid
flowchart TD
    UniConfig["University.config.academicStructure"] --> LevelNames["Custom Level Labels<br/>{ institute: 'College', department: 'Faculty', programme: 'Degree' }"]
    UniConfig --> MiddleLayer["disableMiddleLayer: boolean"]
    
    MiddleLayer -->|false (Default)| FullHierarchy["Institute -> Department -> Programme -> Course"]
    MiddleLayer -->|true| CollapsedHierarchy["Institute -> Programme -> Course (Direct link)"]
    
    LevelNames --> DynamicUI["MasterDataPage.tsx: Dynamic Tab & Column Labels"]
    LevelNames --> ValidationEngine["ValidationPage.tsx: Schema Integrity Engine"]
```

---

## 3. Batch Term Lifecycle & Lock Integrity

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Batch Created
    DRAFT --> ACTIVE: Terms Initialized & Subjects Mapped
    ACTIVE --> LOCKED: Examination Commences / Term Concludes
    
    state LOCKED {
        [*] --> TermFinished
        TermFinished --> Reopened: SuperAdmin Unlock (Requires 0 Enrolled Students)
    }

    Reopened --> ACTIVE: Modifiable by Dept Coordinator
    LOCKED --> ARCHIVED: Results Published & Promoted to Next Term
    ARCHIVED --> [*]
```

### Locking Invariants
1. A locked `BatchTerm` cannot have subjects added, removed, or credit weightages modified.
2. A locked `BatchTerm` cannot be unlocked by regular `InstAdmin` or `HOD` if any student has grade records or marksheet entries.
3. SuperAdmin override unlock requires an explicit validation that `StudentSubjectEnrollment.count == 0` to prevent database inconsistency.
