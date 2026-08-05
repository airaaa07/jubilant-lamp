# Action Lifecycle Manual: Academic Catalog & Timetable Engine

## Action 3.1: Defining Versioned StreamLabel & SubjectLabel Snapshots

### 1. User Action & Frontend Trigger
- **User Role**: University Admin (`role: UnivAdmin` / `SuperAdmin`)
- **Screen**: `MasterDataPage.tsx` (Version Rules Tab)
- **User Input**: Program Choice (B.Tech CS), Version Name (`CS_CURRICULUM_RULES_2024_V1`), Total Graduation Credits (`160`), Core Credits (`120`), Elective Pool Credits (`40`), Min Passing Grade (`D`).
- **Trigger**: Click **Freeze & Publish Immutable Stream Rule Snapshot**.

### 2. Frontend State & Payload Construction
- Sends HTTP POST:
  ```json
  {
    "programId": "prog-cs-01",
    "labelName": "CS_CURRICULUM_RULES_2024_V1",
    "totalCredits": 160,
    "coreCredits": 120,
    "electiveCredits": 40,
    "minGpa": 2.0,
    "subjectRules": [
      { "subjectId": "sub-cs101", "isRequired": true, "credits": 4 },
      { "subjectId": "sub-cs102", "isRequired": true, "credits": 4 }
    ]
  }
  ```

### 3. Backend Execution (`StreamLabelService.createSnapshot`)
- `POST /api/v1/academic/stream-labels`
- Checks if existing stream label rules exist for program; assigns version increment (`version = 1`).
- Locks record as immutable (`is_active = true, is_frozen = true`).

### 4. Database Persistence
- `INSERT INTO stream_labels (id, program_id, version, label_name, rules_json, is_frozen = true)`
- `INSERT INTO subject_labels (stream_label_id, subject_id, credit_weight, requirement_type)`

### 5. Impact & Outcome
- Future student enrollments for Batch 2024-2028 are bound to `CS_CURRICULUM_RULES_2024_V1`.
- Any subsequent program rule changes will create `CS_CURRICULUM_RULES_2026_V2` without altering ongoing student credit requirements.

---

## Action 3.2: Automated Timetable Solver Execution

### 1. User Action & Frontend Trigger
- **User Role**: Institute Administrator (`role: InstAdmin`)
- **Screen**: `TimetablePage.tsx`
- **User Input**: Academic Term (Term 3 Fall 2024), Target Institute, Working Days (Mon-Fri), Daily Periods (8 periods/day).
- **Trigger**: Click **Run Timetable Constraint Solver**.

### 2. Backend Engine Logic (`TimetableService.generateTimetable`)
- `POST /api/v1/timetable/generate`
- Queries all active subjects, section allocations, assigned faculty (`staff_subject_assignments`), and institute classroom capacities (`institute_resources`).
- Executes constraint solving loop:
  - Resolves faculty double-booking conflicts.
  - Resolves room occupancy capacity limits.
  - Balances daily teaching hours per instructor.

### 3. Database Mutations
- `INSERT INTO schedule_runs (institute_id, term_id, status = 'COMPLETED', conflict_count = 0)`
- `INSERT INTO timetable_slots (schedule_run_id, subject_id, section_id, faculty_user_id, resource_id, day_of_week, period_index)`

### 4. Outcome
- Grid matrix rendered on `TimetablePage.tsx`. Instructors and students see published schedules on their dashboards.
