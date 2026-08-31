# UI Design Specs: Examinations & Computer-Based Exam (CBE) Screens

## Pages Covered
- `ExaminationsPage.tsx`
- `ExamTakePage.tsx`
- `ExamMonitorPage.tsx`
- `ExamItemAnalysisPage.tsx`
- `MyInvigilationPage.tsx`
- `PublicResultsPage.tsx`

---

## 1. Examinations Management Console (`ExaminationsPage.tsx`)

### Screen Purpose
Comprehensive examination management hub (536KB — largest page in the system) for creating exam papers, scheduling exams, managing question banks, configuring exam components, assigning invigilators, managing admit cards, handling answersheet serial recording, and PBE anonymisation settings.

### Layout & Component Specs
- **Tab Navigation**: Papers, Schedule, Question Bank, Subject Exam Config, Admit Cards, Results Config, Attendance
- **Paper Management**:
  - Create paper: `POST /api/examination` with batch term, subject, exam type, duration, marks configuration
  - List papers: `GET /api/examination` with filters for batch, term, status
  - Schedule validation: `POST /api/examination/schedule/validate`
  - Schedule lock: `POST /api/examination/schedule/lock`
  - Paper rollback: `POST /api/examination/rollback`
- **Exam Scheduling Engine**:
  - Subject offerings: `GET /api/examination/scheduling/offerings`
  - Term-level scheduling: `POST /api/examination/schedule-term`
  - Individual exam scheduling: `POST /api/examination/schedule`
  - Supplementary targets: `GET /api/examination/supplementary-targets`
  - Supplementary scheduling: `POST /api/examination/schedule-supplementary`
- **Admit Card System**:
  - Preview: `POST /api/examination/admit-card-preview`
  - Release: `POST /api/examination/release-admit-card` (with ineligibility override list)
- **Answersheet Serial Management** (PBE Anonymisation):
  - Get serial sheet: `GET /api/examination/answersheet-serials?paperId=`
  - Save serials: `PUT /api/examination/answersheet-serials`
  - Lock serials: `POST /api/examination/answersheet-serials/lock`
  - Unlock serials: `POST /api/examination/answersheet-serials/unlock`
  - Anonymisation settings: `GET/PUT /api/examination/pbe-anon-settings`
  - Per-exam anonymisation toggle: `PUT /api/examination/exam-anonymise`
- **Exam In-Charge Assignment**:
  - Get in-charge: `GET /api/examination/exam-incharge?paperId=`
  - Assign in-charge: `PUT /api/examination/exam-incharge`
  - Batch in-charge lookup: `GET /api/examination/exam-incharges?paperIds=`
- **Exam Configuration**:
  - Get config: `GET /api/examination/config`
  - Save config: `PUT /api/examination/config`
- **Public Results Configuration**:
  - Get enabled terms: `GET /api/examination/public-results-terms`
  - Toggle term visibility: `PUT /api/examination/public-results-terms/:batchTermId`
- **Attendance Sheet**: `GET /api/examination/attendance-sheet?paperId=`
- **Mock Exam Assembly**: `POST /api/examination/mock/assemble`

---

## 2. Computer-Based Examination Taking Screen (`ExamTakePage.tsx`)

### Screen Purpose
Locked, proctored test environment where students take online examinations. Enforces AI proctoring, webcam monitoring, tab switch limits, and auto-saves answer selections. Full-screen route at `/exam/:paperId`.

### Layout & Component Specs
- **Top Security Header**: Fixed dark header bar with exam title, countdown timer, student roll number, session security status pill (`SECURE SESSION`).
- **Main Question Workspace**:
  - Question text card with math LaTeX rendering support
  - Radio button option list with hover state
  - Navigation controls (`Previous`, `Next`, `Flag for Review`, `Finish Exam`)
- **Right Sidebar (Question Palette & Proctoring)**:
  - **Live AI Proctoring Feed Widget**: Webcam video stream with green AI eye-tracking indicator and warning alert counter
  - **Numbered Question Palette Grid**: 10×5 grid color-coded by state:
    - Green (`bg-emerald-600`): Answered
    - Amber (`bg-amber-600`): Flagged for Review
    - Dark Slate (`bg-slate-800`): Unvisited

### CBE API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/examination/cbe/save-answer` | Auto-save answer selection |
| POST | `/api/examination/cbe/proctor-event` | Log proctoring violation |
| POST | `/api/examination/cbe/submit` | Final exam submission |

---

## 3. Invigilator Live Exam Monitor (`ExamMonitorPage.tsx`)

### Screen Purpose
Real-time dashboard for exam invigilators at `/exams/:paperId/monitor`. Monitors active student sessions, webcam feeds, tab-switch alerts, and provides emergency controls.

### Layout & Component Specs
- **Grid of Student Proctor Cards**: Multi-card grid with student name, roll number, tab switch count, live webcam snapshot, action buttons (`SendMessage`, `PauseSession`, `TerminateExam`).
- **Alert Banner**: Flashing alert for students exceeding violation thresholds.

---

## 4. Exam Item Analysis Page (`ExamItemAnalysisPage.tsx`)

### Screen Purpose
Post-exam statistical analysis at `/exams/:paperId/analysis`. Displays question-level difficulty indices, discrimination indices, distractor effectiveness charts, and overall paper quality metrics.

---

## 5. My Invigilation Page (`MyInvigilationPage.tsx`)

### Screen Purpose
Faculty-facing page showing invigilation assignments for the current user.

### API Endpoint
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/examination/invigilation/mine` | My invigilation schedule |

---

## 6. Public Results Page (`PublicResultsPage.tsx`)

### Screen Purpose
Public (no-auth) page at `/results` for students to check published exam results using enrollment number. Only terms enabled via `public-results-terms` API are visible.

---

## 7. Question Bank Module (`question-bank.controller.ts`)

### Screen Purpose
Embedded within ExaminationsPage — repository of exam questions organized by subject, topic, difficulty, and type (MCQ, Descriptive, Numerical).

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/question-bank` | List questions with filters |
| POST | `/api/question-bank` | Create question |
| PATCH | `/api/question-bank/:id` | Update question |
| DELETE | `/api/question-bank/:id` | Delete question |

---

## 8. Subject Exam Configuration (`subject-exam-config.controller.ts`)

### Screen Purpose
Configure exam component weightages per subject (e.g., Internal Assessment: 30%, Mid-Term: 20%, Final: 50%). Defines grading rubrics and mark distribution.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/subject-exam-config` | Get config for subject |
| POST | `/api/subject-exam-config` | Create/update config |

---

## 9. PBE Paper Module (`pbe-paper.controller.ts`)

### Screen Purpose
Paper-Based Examination paper management — generating formatted question paper PDFs with randomised sets and answer keys.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/pbe-paper` | List PBE papers |
| POST | `/api/pbe-paper` | Generate PBE paper |
| GET | `/api/pbe-paper/:id` | Get specific paper |
