# Technical Workflow Architecture: Academic Catalog & Versioned Rules

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, immutable rule versioning logic, subject pool elections, and automated timetable scheduling constraint algorithms.

---

## 🔄 End-to-End Sequence Diagram: Academic Setup & Versioned Stream Rules

```mermaid
sequenceDiagram
    autonumber
    actor Admin as InstAdmin / UnivAdmin
    participant AcadC as AcademicController
    participant StreamS as StreamLabelService
    participant TimetableS as TimetableService
    participant DB as PostgreSQL Database

    Admin->>AcadC: POST /api/v1/academic/programs (Create Program B.Tech CS)
    AcadC->>DB: INSERT into programs & departments

    Admin->>AcadC: POST /api/v1/academic/stream-labels (Define Graduation Rules)
    AcadC->>StreamS: createVersionedStreamLabel(dto)
    Note over StreamS: Generate Immutable Rule Snapshot<br/>(CS_LABEL_V1: Core 120 Cr, Elective 40 Cr)
    StreamS->>DB: INSERT into stream_labels (is_active: true, version: 1)

    Admin->>AcadC: POST /api/v1/academic/batches (Create Batch 2024-2028)
    AcadC->>DB: INSERT into batches (stream_label_id: CS_LABEL_V1)

    note over StreamS: 2 Years Later - Admin Modifies Program Rules
    Admin->>AcadC: POST /api/v1/academic/stream-labels (Create New Curriculum)
    StreamS->>DB: INSERT into stream_labels (version: 2, CS_LABEL_V2)
    note over StreamS: Batch 2024-2028 Remains Frozen on CS_LABEL_V1<br/>New Batch 2026-2030 Assigned CS_LABEL_V2

    note over TimetableS: Faculty Executes Timetable Auto-Scheduler Solver
    Admin->>AcadC: POST /api/v1/timetable/generate
    TimetableS->>DB: Fetch Courses, Faculty Assignments, Classrooms
    TimetableS->>TimetableS: Run Constraint Solver (No double-booking, load balancing)
    TimetableS->>DB: INSERT into schedule_runs & timetable_slots
```

---

## 🔀 Versioned Stream Rule & Student Binding Topology

```
                  ┌─────────────────────────────────────┐
                  │    StreamLabel: CS_RULES_2024_V1    │  (Immutable Snapshot)
                  │    • Total Credits: 160            │
                  │    • Core Subjects: 30              │
                  │    • Elective Pools: 4              │
                  └──────────────────┬──────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           │                                                   │
┌──────────▼──────────┐                             ┌──────────▼──────────┐
│   Batch 2024-2028   │                             │  Student Profile A  │
│  (Bound at Entry)   │                             │ (Roll: CS2024-001)  │
└─────────────────────┘                             └─────────────────────┘

               --- Program Rules Updated for 2026 ---

                  ┌─────────────────────────────────────┐
                  │    StreamLabel: CS_RULES_2026_V2    │  (New Immutable Snapshot)
                  │    • Total Credits: 164            │
                  │    • Core Subjects: 32              │
                  │    • AI/ML Elective Mandatory       │
                  └──────────────────┬──────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           │                                                   │
┌──────────▼──────────┐                             ┌──────────▼──────────┐
│   Batch 2026-2030   │                             │  Student Profile B  │
│  (Bound at Entry)   │                             │ (Roll: CS2026-001)  │
└─────────────────────┘                             └─────────────────────┘
```

---

## ⚙️ Timetable Constraint Solving Engine

The `TimetableService` executes a multi-constraint solving algorithm to map courses, faculty, sections, and classrooms into `timetable_slots`:

1. **Hard Constraints**:
   - No faculty member can be assigned to two classes simultaneously.
   - No classroom/lab can host two sections simultaneously.
   - Student sections cannot have overlapping mandatory lecture slots.
2. **Soft Constraints**:
   - Equal distribution of faculty teaching hours across weekdays.
   - Lab sessions assigned to morning slots where available.
