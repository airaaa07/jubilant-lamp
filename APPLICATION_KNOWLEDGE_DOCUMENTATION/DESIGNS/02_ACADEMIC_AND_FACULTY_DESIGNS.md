# UI Design Specs: Academic & Faculty Management Screens

## Pages Covered
- `MasterDataPage.tsx`
- `ElectivesPage.tsx`
- `TimetablePage.tsx`
- `AttendancePage.tsx`
- `DirectoryPage.tsx`
- `MySubjectsPage.tsx`
- `ValidationPage.tsx`

---

## 1. Master Data Management Page (`MasterDataPage.tsx`)

### Screen Purpose
Central administrative console for building and maintaining the multi-tenant university structure, institute entities, departments, programs, batches, terms, sections, courses, campus resources, and versioned rules (`StreamLabel` & `SubjectLabel`). Supports bulk import via CSV.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Academic Structure & Master Data                            │
│  [ Universities ] [ Institutes ] [ Depts ] [ Programs ]      │
│  [ Batches ] [ Courses ] [ Streams ] [ Subjects ] [ Sections]│
│  [ Campus Resources ] [ Bulk Import ]                        │
├──────────────────────────────────────────────────────────────┤
│  Entity List                               [ + Add New ]     │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Code  │ Entity Name           │ Count │ Head │ Status  │  │
│  ├───────┼───────────────────────┼───────┼──────┼─────────┤  │
│  │ ENG01 │ School of Engineering │   6   │ Dr.A │ ACTIVE  │  │
│  │ MED02 │ School of Medicine    │   4   │ Dr.B │ ACTIVE  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Top Tab Bar**: Horizontal tab strip with pills for each entity type — `Universities`, `Institutes`, `Departments`, `Programmes`, `Batches`, `Batch Terms`, `Courses`, `Stream Labels`, `Subject Labels`, `Sections`, `Campus Resources`, `University Courses`, `University Departments`, `University Streams`, `University Subjects`.
- **Entity Data Table**: High-density table with sorting, search filtering, inline action buttons (`Edit`, `Manage Rules`, `Deactivate`).
- **Stream Label Rules Modal** (`StreamLabelDetailModal.tsx`): Slide-over panel for configuring immutable batch graduation rules (Total Credits, Core Credits, Elective Credits, Min GPA). Uses `ProgramLabelDetailModal.tsx` for programme-level label views.
- **Subject Label Detail Modal** (`SubjectLabelDetailModal.tsx`): Subject-level curriculum rule viewer.
- **Bulk Import**: CSV file upload for mass entity creation (`POST /api/master-data/bulk-import/upload`).
- **Batch Setup Integration** (`BatchSetupWizard.tsx` + `BatchSetupList.tsx`): 38KB wizard for creating complete batch structures with terms, sections, and subject assignments in a guided multi-step process.

### API Endpoints (Master Data Module)
| Controller | Key Endpoints |
|:---|:---|
| `university.controller.ts` | CRUD `/api/master-data/universities` |
| `institute.controller.ts` | CRUD `/api/master-data/institutes` |
| `department.controller.ts` | CRUD `/api/master-data/departments` |
| `programme.controller.ts` | CRUD `/api/master-data/programmes` |
| `batch.controller.ts` | CRUD `/api/master-data/batches` |
| `batch-term.controller.ts` | CRUD `/api/master-data/batch-terms` |
| `course.controller.ts` | CRUD `/api/master-data/courses` |
| `section.controller.ts` | CRUD `/api/master-data/sections` |
| `stream-label.controller.ts` | CRUD `/api/master-data/stream-labels` |
| `subject-label.controller.ts` | CRUD `/api/master-data/subject-labels` |
| `campus-resource.controller.ts` | CRUD `/api/master-data/campus-resources` |
| `university-course.controller.ts` | CRUD `/api/master-data/university-courses` |
| `university-department.controller.ts` | CRUD `/api/master-data/university-departments` |
| `university-stream.controller.ts` | CRUD `/api/master-data/university-streams` |
| `university-subject.controller.ts` | CRUD `/api/master-data/university-subjects` |
| `bulk-import.controller.ts` | POST `/api/master-data/bulk-import/upload` |

---

## 2. Interactive Timetable Scheduler Page (`TimetablePage.tsx`)

### Screen Purpose
Grid view displaying class schedules per section, room allocation, and faculty availability. Supports auto-scheduler solver execution and manual drag-and-drop slot adjustments. Manages schedule runs across terms.

### Layout & Component Specs
- **Weekly Schedule Matrix**: 7-column grid (Monday to Sunday) across period time slots (8:00 AM to 5:00 PM).
- **Class Slot Cards**: Rounded grid cards color-coded by subject type:
  - Lecture: Blue gradient container (`bg-blue-950/40 border-blue-800`)
  - Lab Session: Emerald gradient container (`bg-emerald-950/40 border-emerald-800`)
  - Tutorial: Purple gradient container (`bg-purple-950/40 border-purple-800`)
- **Conflict Highlight Overlay**: Red pulse outline (`ring-2 ring-rose-500 animate-pulse`) displayed over slots with faculty or classroom double-booking conflicts.
- **Auto-Solver Trigger**: Button to execute constraint solving (`POST /api/timetable/generate`) resolving faculty conflicts, room capacity, daily teaching balance.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/timetable/generate` | Run constraint solver |
| GET | `/api/timetable` | Fetch schedule grid |
| PATCH | `/api/timetable/slots/:id` | Manual slot adjustment |

---

## 3. Attendance Recording Page (`AttendancePage.tsx`)

### Screen Purpose
Allows teaching faculty to mark daily class attendance, review attendance percentages, and generate low-attendance alert notices. Supports both class-level and subject-level attendance tracking.

### Layout & Component Specs
- **Attendance Toggle Grid**: Student list with quick toggle buttons for each student (`PRESENT` green pill / `ABSENT` red pill / `EXCUSED` yellow pill).
- **Summary Header Widget**: Donut chart showing overall session attendance percentage (e.g. `88% Present - 44 / 50 Students`).
- **Bulk Actions**: Mark all present/absent with single click.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/attendance` | Fetch attendance records |
| POST | `/api/attendance` | Submit attendance marking |
| GET | `/api/academic/attendance` | Academic attendance analytics |

---

## 4. Electives & Course Election Page (`ElectivesPage.tsx`)

### Screen Purpose
Enables students to view available elective courses, submit elective preferences, and view election results. Supports election roster management for administrators.

### Layout & Component Specs
- **Available Electives Grid**: Card view of available elective courses with seats remaining, credits, instructor details.
- **Preference Ranking**: Drag-to-rank interface for elective preference ordering.
- **Election Roster Modal** (`ElectionRosterModal.tsx`): Admin view showing election results, allotment statistics.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/academic/elections` | List available elections |
| POST | `/api/academic/elections/submit` | Submit elective preferences |
| GET | `/api/academic/elections/results` | View allotment results |

---

## 5. My Subjects Page (`MySubjectsPage.tsx`)

### Screen Purpose
Faculty-facing page displaying subjects assigned to the logged-in instructor for the current term, with class details, section info, and links to marks entry.

### Layout & Component Specs
- **Subject Cards**: Card grid showing subject name, code, section, student count, schedule slot info.
- **Quick Actions**: Navigate to marks entry, attendance recording, and student list per subject.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/staff-subject` | Get assigned subjects for current user |
| POST | `/api/staff-subject` | Assign staff to subject |
| DELETE | `/api/staff-subject/:id` | Remove assignment |

---

## 6. Directory Page (`DirectoryPage.tsx`)

### Screen Purpose
University-wide searchable directory of students, staff, and departments. Provides contact cards, filtering by institute/department/role, and quick-access profiles.

### Layout & Component Specs
- **Search & Filter Bar**: Full-text search with dropdown filters for Institute, Department, Role, Status.
- **Contact Cards Grid**: Card view with avatar, name, role, department, email, phone.
- **Profile Quick View**: Click to expand inline profile detail with academic/employment info.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/directory` | Search and list directory entries |

---

## 7. Validation Dashboard Page (`ValidationPage.tsx`)

### Screen Purpose
System validation console for checking data integrity, configuration completeness, and prerequisite validation across modules. Helps administrators identify missing configurations before going live.

### Layout & Component Specs
- **Validation Check Cards**: Grid of validation categories with pass/fail/warning indicators.
- **Detail Drill-Down**: Click each validation to see specific issues and remediation guidance.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/validation` | Run validation checks |
| GET | `/api/validation/:category` | Get specific category results |

---

## 8. Academic Sub-Modules (Embedded in Examinations & Results Pages)

### Marks Entry (`marks.controller.ts`)
- Faculty enters subject marks per student per exam component
- `GET /api/academic/marks` — fetch marks grid
- `POST /api/academic/marks` — save marks batch
- `POST /api/academic/marks/lock` — lock marks for review

### Results Pipeline (`results.controller.ts`)
- Multi-stage result processing: Compute → Review → Approve → Publish
- Role-based access: `GET /api/academic/results/roles`, `PUT /api/academic/results/roles`
- Pipeline dashboard: `GET /api/academic/results/pipeline`
- SGPA/CGPA computation: `POST /api/academic/results/compute`, `POST /api/academic/results/compute-cgpa`
- Promotion: `GET /api/academic/results/promote-preview`, `POST /api/academic/results/promote`
- Bulk operations: `POST /api/academic/results/review-all`, `POST /api/academic/results/approve-all`, `POST /api/academic/results/publish-all`

### Enrollment (`enrollment.controller.ts`)
- Student enrollment management, section assignment
- `GET /api/academic/enrollments` — list enrolled students
- `POST /api/academic/enrollments` — enroll student in subjects

### Reassessment & Marksheets (`reassessment.controller.ts`)
- Reassessment applications: `GET /api/academic/reassessments`, `POST /api/academic/reassessments`
- Result holds: `POST /api/academic/result-holds`, `POST /api/academic/result-holds/:id/clear`
- Marksheet issuance: `POST /api/academic/marksheet/check-issuable`, `GET /api/academic/marksheet`

### Supplementary Exams (`supplementary.controller.ts`)
- Backlog tracking: `GET /api/academic/supplementary/backlogs`
- Supplementary registration: `POST /api/academic/supplementary/register`
- Result recording: `PATCH /api/academic/supplementary/:id/result`
- Cancellation: `PATCH /api/academic/supplementary/:id/cancel`
