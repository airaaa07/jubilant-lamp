# Action Lifecycle Manual: Academic Catalog, Curriculum & Timetable

## Action 3.1: Immutable Stream Label & Subject Label Rule Definition

### 1. User Action & Frontend Trigger
- **User Role**: Dean / UnivAdmin / Academic Head
- **Screen**: `MasterDataPage.tsx` -> `StreamLabelDetailModal.tsx`
- **Input**: Programme ID, Version Identifier (e.g. `BTECH_CS_2026_V1`), Total Credits (`160`), Core Credits (`120`), Elective Credits (`40`), Min CGPA (`2.0`), Subject Credit Rules list.
- **Trigger**: Click **Freeze & Publish Rule** button.

### 2. Frontend Payload Construction
- ```json
  {
    "programmeId": "prog-uuid-101",
    "name": "B.Tech CSE 2026 Regulations",
    "version": "V1",
    "totalCredits": 160,
    "coreCredits": 120,
    "electiveCredits": 40,
    "minCgpa": 2.0,
    "isFrozen": true,
    "subjectRules": [
      { "subjectId": "subj-101", "credits": 4, "isMandatory": true, "termNumber": 1 },
      { "subjectId": "subj-102", "credits": 3, "isMandatory": true, "termNumber": 1 }
    ]
  }
  ```

### 3. API Routing & Guard Pipeline
- **Endpoint**: `POST /api/master-data/stream-labels`
- **Guards**: `JwtAuthGuard`, `RolesGuard('UnivAdmin', 'SuperAdmin', 'Dean')`.

### 4. Backend Processing & Immutability Enforcement
- Checks if existing batch has already completed terms under this label.
- If `isFrozen === true`, creates immutable rule record.
- Any future modifications require creating a new version (`V2`) rather than mutating existing frozen rules.

---

## Action 3.2: Automated Timetable Generation & Constraint Solving

### 1. User Action
- **Screen**: `TimetablePage.tsx`
- **Trigger**: Click **Generate Timetable Schedule**.

### 2. API Routing
- `POST /api/timetable/generate` with `{ batchTermId, roomIds, facultyIds, maxHoursPerDay: 6 }`.

### 3. Solver Execution Logic
- Constraint solver evaluates:
  - No faculty double-booking across sections.
  - Classroom capacity >= section enrollment count.
  - Lab sessions allocated to designated lab resources in contiguous 2-3 hour blocks.
  - Faculty daily teaching load capped at policy maximum.
- Generates weekly slot matrix in `timetable_slots`.

### 4. Conflict Highlight & Manual Adjustment
- Frontend renders 7-day interactive grid.
- Faculty or room conflicts highlight with red pulse ring (`ring-2 ring-rose-500`).
- Drag-and-drop slot repositioning invokes `PATCH /api/timetable/slots/:id`.

---

## Action 3.3: Attendance Marking & Defaulter Generation

### 1. Faculty Attendance Session
- **Screen**: `AttendancePage.tsx`
- Faculty selects subject, date, period slot.
- Toggle buttons for each student: `PRESENT` (green), `ABSENT` (red), `EXCUSED` (yellow).
- Clicks **Submit Attendance** -> `POST /api/attendance`.

### 2. Analytics & Low Attendance Detection
- Calculates cumulative percentage per student per subject: `(attended / total) * 100`.
- If attendance < 75% policy threshold, student profile flagged as `ATTENDANCE_DEFAULTER`.
- Triggers notification to student and parent portal.
