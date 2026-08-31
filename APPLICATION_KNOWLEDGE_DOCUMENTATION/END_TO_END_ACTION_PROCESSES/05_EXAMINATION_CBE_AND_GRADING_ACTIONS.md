# Action Lifecycle Manual: Examinations, CBE & Grading Pipeline

## Action 5.1: Exam Paper Creation, Scheduling & Admit Card Release

### 1. Paper Definition & Question Assembly
- **Role**: Examination Controller / InstAdmin
- **Screen**: `ExaminationsPage.tsx`
- Input: Batch Term, Subject, Exam Type (Mid-Term, Final, Internal), Duration (120 mins), Total Marks (100).
- `POST /api/examination` -> paper created in `exam_papers`.
- Adds questions from question bank (`GET /api/question-bank`) or uploads new questions.

### 2. Schedule Validation & Lock
- Sets exam date, start time, end time, and classroom venues.
- Clicks **Validate Schedule** -> `POST /api/examination/schedule/validate` (checks classroom capacity and student conflict).
- Clicks **Lock Schedule** -> `POST /api/examination/schedule/lock`.

### 3. Admit Card Generation & Release
- Clicks **Release Admit Cards** -> `POST /api/examination/release-admit-card`.
- Can exclude students with ineligibility reasons (e.g. low attendance, unpaid fees).
- Students can download admit card with QR code verification.

---

## Action 5.2: Computer-Based Exam (CBE) Live Session & AI Proctoring

### 1. Student Session Initialization
- **Screen**: `ExamTakePage.tsx` (`/exam/:paperId`).
- Checks browser fullscreen and camera access.
- Timer countdown begins.

### 2. Live Auto-Save & Question Navigation
- Student clicks option on MCQ -> `POST /api/examination/cbe/save-answer { paperId, questionId, selectedOption, answerText }`.
- Frontend palette marks question answered (green) or flagged (amber).

### 3. Proctoring Violation Detection & Live Monitoring
- If student switches browser tabs -> `POST /api/examination/cbe/proctor-event { eventType: 'TAB_SWITCH' }`.
- Invigilator monitors active sessions on `ExamMonitorPage.tsx` (`/exams/:paperId/monitor`).
- If tab violations exceed threshold (3), invigilator or automated rule terminates exam session.
- Student clicks **Finish Exam** -> `POST /api/examination/cbe/submit` -> marks finalized.

---

## Action 5.3: PBE Anonymisation & Answersheet Serial Recording

### 1. Serial Number Binding
- For Paper-Based Exams (PBE), invigilator records dummy booklet serials via `PUT /api/examination/answersheet-serials`.
- Clicks **Lock Serials** -> `POST /api/examination/answersheet-serials/lock`.
- Marks entry displays only serial numbers, preventing evaluator bias.

---

## Action 5.4: Results Processing Pipeline & CGPA Computation

### 1. Marks Entry & Lock
- Faculty enters subject component marks on `MySubjectsPage.tsx` / `MarksPage`.
- `POST /api/academic/marks` -> saves marks.
- `POST /api/academic/marks/lock` -> locks marks for processing.

### 2. 4-Stage Result Progression
1. **Compute**: `POST /api/academic/results/compute` -> computes SGPA, grade points, pass/fail status per student.
2. **Review**: `POST /api/academic/results/review-all` -> marks reviewed by examination committee.
3. **Approve**: `POST /api/academic/results/approve-all` -> Dean / Controller approval.
4. **Publish**: `POST /api/academic/results/publish-all` -> results visible to students on `StudentProfilePage.tsx` and public portal (`PublicResultsPage.tsx`).
5. **CGPA Update**: `POST /api/academic/results/compute-cgpa` -> updates cumulative GPA across all completed terms.
