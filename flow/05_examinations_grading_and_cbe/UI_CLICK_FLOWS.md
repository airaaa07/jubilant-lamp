# Module 05: Examinations, Grading & CBE — UI Click Flows

> **Scope**: Examination session scheduling, Paper authoring, Question Bank, Fullscreen Computer-Based Exam (CBE) execution (`/exam/:paperId`), Real-time Proctor Monitoring (`/exams/:paperId/monitor`), Item Analysis (`/exams/:paperId/analysis`), Invigilation Duty allocation (`/my-invigilation`), Grading Component Locks, and Public Result Verification (`/results`).

---

## Screen Inventory

| Route | Page Component | Primary Actors | Key Capabilities |
|:---|:---|:---|:---|
| `/exams` | `ExaminationsPage.tsx` | ExaminationController, InstAdmin, HOD | Master exam console: Schedules, Admit Cards, Seat Allocation, Anonymous Codes, Component Locks, Question Bank, Results publication. |
| `/exam/:paperId` | `ExamTakePage.tsx` | Student Candidate | Fullscreen locked exam environment: question palette, timer countdown, MCQ/MSQ/Coding answers, flag for review, proctor heartbeat, question challenges. |
| `/exams/:paperId/monitor` | `ExamMonitorPage.tsx` | Invigilator, Exam Admin | Real-time candidate roster, live heartbeat status, tab switch / focus loss warning alerts, webcam snapshots, force-terminate actions. |
| `/exams/:paperId/analysis` | `ExamItemAnalysisPage.tsx` | Exam Controller, Subject Expert | Question psychometrics: Facility Value, Discrimination Index, Distractor Efficiency analysis charts. |
| `/my-invigilation` | `MyInvigilationPage.tsx` | Assigned Teaching Faculty | Faculty duty calendar, room allocation, physical attendance marking, answersheet serial logging. |
| `/results` | `PublicResultsPage.tsx` | Public, Students, Employers | Public transcript & result lookup by Roll Number / DOB without requiring authentication. |

---

## Flow 1: Student Fullscreen CBE Exam Journey (`/exam/:paperId`)

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as ExamTakePage.tsx
    participant CBE as CBE Engine (:3002 / Core API)
    participant Monitor as ExamMonitorPage.tsx

    Student->>UI: Visits /exam/:paperId
    UI->>UI: System checks fullscreen capabilities & webcam permissions
    UI->>UI: Prompts: "Exam requires locked fullscreen mode. Click 'Enter Exam'."
    Student->>UI: Clicks "Enter Exam & Fullscreen"
    UI->>CBE: POST /api/cbe/start { paperId }
    CBE-->>UI: Returns questions array (randomized per candidate), timeRemaining
    UI->>UI: Locks window, initializes timer countdown and question palette
    
    loop Every 30 seconds
        UI->>CBE: POST /api/cbe/heartbeat { attemptId, currentQuestionIndex }
        UI->>CBE: POST /api/cbe/snapshot (Webcam frame blob)
        CBE->>Monitor: Pushes live status to proctor dashboard
    end

    alt Candidate Alt-Tabs / Exits Fullscreen
        UI->>UI: Increments tabSwitchViolations counter; displays red warning banner
        UI->>CBE: POST /api/cbe/proctor-event { eventType: "FOCUS_LOST" }
        CBE->>Monitor: Red alert flag on candidate tile
    end

    Student->>UI: Answers questions, clicks "Save & Next"
    UI->>CBE: POST /api/cbe/response { questionId, selectedOptions, textAnswer }
    Student->>UI: Clicks "Finish Exam" -> Confirms submission dialog
    UI->>CBE: POST /api/cbe/finish { attemptId }
    CBE-->>UI: 200 OK -> Exam submitted confirmation screen
    UI->>UI: Exits fullscreen mode
```

### Granular Step-by-Step Table

| Step | Screen | User Interaction | Visual Changes & State | System Action / API Call | Redirection / Modal |
|:---|:---|:---|:---|:---|:---|
| 1.1 | `/exam/:paperId` | Enters exam route | Pre-exam checklist: Hardware checks (Camera, Microphone, Screen Resolution, Browser version). | None | Instructions screen |
| 1.2 | `/exam/:paperId` | Clicks **"Agree to Guidelines & Enter Fullscreen"** | Browser enters Fullscreen API mode; browser address bar and OS chrome hide. | `POST /api/examination/papers/:id/start` | Fullscreen locked |
| 1.3 | `/exam/:paperId` | Inspects exam UI | Left: Question content + options. Right: Question Palette grid (Answered=Green, Not Answered=Gray, Marked for Review=Purple). Top: Countdown clock. | None | Active exam layout |
| 1.4 | Question Palette | Clicks Question #14 | Jumps directly to question 14 without page reload. | None | Question renders |
| 1.5 | Question Area | Selects Option B, clicks **"Save & Next"** | Palette tile turns green. Current response cached locally and pushed to server. | `POST /api/examination/attempts/:id/response` | Advances to Question #15 |
| 1.6 | Question Toolbar | Clicks **"Mark for Review"** | Tile turns purple with small badge. | None | Flagged state |
| 1.7 | Question Toolbar | Clicks **"Challenge Question"** | Modal opens: candidate can submit error report (e.g. "Typo in equation") without leaving exam. | `POST /api/examination/questions/:id/challenge` | Toast confirmation |
| 1.8 | Top Bar | Clicks **"Submit Paper"** | Submission summary modal opens: "Answered: 45, Unanswered: 5, Marked for Review: 2. Confirm submit?". | None | ConfirmDialog opens |
| 1.9 | Modal | Clicks **"Confirm & End Exam"** | Screen displays score (if instant MCQ evaluation enabled) or receipt token; exits fullscreen. | `POST /api/examination/attempts/:id/finish` | Exam completed |

---

## Flow 2: Live Exam Proctoring Console (`/exams/:paperId/monitor`)

| Step | Screen | User Interaction | Visual Changes & State | System Action / API Call | Redirection / Modal |
|:---|:---|:---|:---|:---|:---|
| 2.1 | `/exams/:paperId/monitor` | Proctor opens dashboard | Grid of candidate cards renders showing candidate name, roll number, photo, live webcam feed. | `GET /api/examination/papers/:id/monitor` | Grid view active |
| 2.2 | Filter Bar | Toggles "Violations Only" | Filters view to only show candidates with $\ge 1$ violation flags (Tab Switch, Face Missing, Multiple Faces). | None | High-priority grid |
| 2.3 | Candidate Card | Clicks on red-flagged candidate | Drawer opens displaying timeline of proctor events with exact timestamps and captured webcam snapshots. | `GET /api/examination/attempts/:id/proctor-timeline` | Drawer opens |
| 2.4 | Drawer Actions | Clicks **"Send Warning Message"** | Types message: *"Please stay seated and face the camera"*. | `POST /api/examination/attempts/:id/directive` | Pops up on student screen |
| 2.5 | Drawer Actions | Clicks **"Terminate Exam (Disqualify)"** | Requires proctor comment. Immediately ends student's exam attempt on their machine. | `POST /api/examination/attempts/:id/terminate` | Student kicked out |

---

## Flow 3: Question Item Analysis Dashboard (`/exams/:paperId/analysis`)

| Step | Screen | User Interaction | Visual Changes & State | System Action / API Call | Redirection / Modal |
|:---|:---|:---|:---|:---|:---|
| 3.1 | `/exams/:paperId/analysis` | Opens psychometric view | Scatter plot renders showing **Facility Index** (Difficulty) vs **Discrimination Index** for all questions. | `GET /api/examination/papers/:id/analysis` | Charts render |
| 3.2 | Analysis Table | Inspects question row flagged with "Poor Discrimination" | Question text displayed with option breakdown: % of High-scoring group vs % of Low-scoring group who picked each distractor. | None | Distractor analysis |
| 3.3 | Action Column | Clicks **"Invalidate Question (Award Bonus)"** | Modal prompts for reason. Updates marks calculation to award credit to all candidates. | `POST /api/examination/papers/:id/bonus-question` | Scores recalculate |
