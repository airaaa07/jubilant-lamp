# UI Design Specs: Examinations & Computer-Based Exam (CBE) Screens

## Pages Covered
- `ExaminationsPage.tsx`
- `ExamTakePage.tsx`
- `ExamMonitorPage.tsx`
- `ExamItemAnalysisPage.tsx`
- `MyInvigilationPage.tsx`

---

## 1. Computer-Based Examination Taking Screen (`ExamTakePage.tsx`)

### Screen Purpose
The locked, proctored test environment where students take online examinations. Enforces AI proctoring, webcam monitoring, tab switch limits, and auto-saves answer selections.

### Visual Mockup Render
![CBE Online Exam and AI Proctoring UI Mockup](/home/admin/.gemini/antigravity-ide/brain/61696b17-1fe4-429b-b9b6-60a5b523471f/cbe_exam_proctoring_1785931500481.png)

### Layout & Component Specs
- **Top Security Header**: Fixed dark header bar displaying exam title, countdown timer (`01:45:22`), student roll number, and session security status pill (`SECURE SESSION`).
- **Main Question Workspace**:
  - Question text card with math LaTeX rendering support.
  - Radio button option list with hover state (`hover:bg-slate-800/60 hover:border-indigo-500/50`).
  - Navigation controls (`Previous`, `Next`, `Flag for Review`, `Finish Exam`).
- **Right Sidebar (Question Palette & Proctoring)**:
  - **Live AI Proctoring Feed Widget**: Embeds webcam video stream with green AI eye-tracking indicator and warning alert counter.
  - **Numbered Question Palette Grid**: Interactive 10x5 grid of numbered question buttons color-coded by state:
    - Green (`bg-emerald-600`): Answered
    - Amber (`bg-amber-600`): Flagged for Review
    - Dark Slate (`bg-slate-800`): Unvisited

---

## 2. Invigilator Live Exam Monitor (`ExamMonitorPage.tsx`)

### Screen Purpose
Real-time dashboard for exam invigilators to monitor all active student exam sessions, webcam proctor feeds, tab-switch alerts, and trigger emergency pause or termination controls.

### Layout & Component Specs
- **Grid of Student Proctor Cards**: Multi-card grid displaying student name, roll number, tab switch count (e.g. `Tab Switches: 2 / Max 3`), live webcam snapshot preview, and action buttons (`SendMessage`, `PauseSession`, `TerminateExam`).
- **Alert Banner**: Flashing alert banner triggered when a student exceeds suspicious movement thresholds.
