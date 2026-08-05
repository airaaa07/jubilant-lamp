# Action Lifecycle Manual: Examinations, CBE Engine & AI Proctoring

## Action 5.1: Student Online CBE Exam Navigation & Answer Recording

### 1. User Action & Frontend Trigger
- **User Role**: Student (`role: Student`)
- **Screen**: `ExamTakePage.tsx`
- **User Input**: Enters Exam Code (`EXAM-CS301-FINAL`), completes webcam environment check, selects radio option B for Question 14, clicks **Next Question**.

### 2. Frontend State & Telemetry Capture
- Web app enters full-screen browser mode via HTML5 Fullscreen API.
- Tab switch listener tracks `window.onblur` and `document.onvisibilitychange`.
- Sends HTTP POST payload:
  ```json
  {
    "attemptId": "attempt-9901-uuid",
    "questionId": "q-14-uuid",
    "selectedOptionId": "opt-b-uuid",
    "timeSpentSeconds": 45
  }
  ```

### 3. API Routing & Guard Pipeline
- `POST /api/v1/examination/cbe/save-answer`
- `GlobalJwtAuthGuard` verifies token. `ExaminationService` verifies exam session is active and not expired.

### 4. Database Mutations
- `UPSERT INTO exam_attempt_answers (attempt_id, question_id, selected_option_id, time_spent)`
- Question palette grid index button #14 changes from slate to green (`bg-emerald-600`).

---

## Action 5.2: AI Proctoring Violation Detection & Telemetry Capture

### 1. Event Trigger (Tab Switch / Window Blur)
- Student attempts to open a search engine tab or minimize browser window.
- Browser triggers `visibilitychange` event.

### 2. Frontend Security Payload
- Increments local violation counter (`tabSwitches += 1`).
- Sends warning notification:
  ```json
  {
    "attemptId": "attempt-9901-uuid",
    "eventType": "TAB_SWITCH",
    "timestamp": "2026-08-05T17:45:00.000Z",
    "details": "User switched away from exam tab"
  }
  ```

### 3. Backend Processing (`ExaminationService.logProctorEvent`)
- `POST /api/v1/examination/cbe/proctor-event`
- Increments `exam_proctor_logs.tab_switches`.
- Compares `tab_switches` against `max_allowed_switches` (e.g. 3).

### 4. Database Mutations
- `UPDATE exam_proctor_logs SET tab_switches = tab_switches + 1 WHERE attempt_id = :id`
- If `tab_switches > 3`:
  - `UPDATE exam_attempts SET status = 'TERMINATED_PROCTOR', end_time = NOW()`
  - Websocket event sent to `ExamMonitorPage.tsx` alerting invigilator.

### 5. Final Outcome
- Student screen locked with red alert message: `"Exam Terminated Due to Repeated Security Violations."`
