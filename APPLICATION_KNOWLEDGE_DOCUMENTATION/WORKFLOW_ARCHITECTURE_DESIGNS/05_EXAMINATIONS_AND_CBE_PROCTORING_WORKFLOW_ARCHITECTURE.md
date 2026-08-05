# Technical Workflow Architecture: Examinations, CBE Engine & AI Proctoring

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, question paper shuffle algorithms, AI proctoring telemetry capture, real-time invigilator controls, and automated SGPA/CGPA grade calculation pipelines.

---

## 🔄 End-to-End Sequence Diagram: CBE Exam & AI Proctoring Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student
    actor Invigilator as Invigilator / Faculty
    participant ExamC as ExaminationController
    participant ExamS as ExaminationService
    participant MinIO as MinIO Object Storage
    participant DB as PostgreSQL Database

    note over Invigilator,ExamS: Pre-Exam Setup & Paper Generation
    Invigilator->>ExamC: POST /api/v1/examination/paper (Create Exam Paper)
    ExamS->>DB: Fetch Questions from Question Bank by Category & Difficulty
    ExamS->>DB: INSERT into exam_papers & exam_schedules

    note over Student,ExamS: Exam Session Initialization
    Student->>ExamC: POST /api/v1/examination/cbe/start-attempt
    ExamS->>DB: Check Eligibility (Attendance >= 75%, Hall Ticket Issued)
    ExamS->>ExamS: Randomize Question Sequence & Option Order
    ExamS->>DB: INSERT into exam_attempts (status: "IN_PROGRESS")
    ExamS-->>Student: Return Randomized Paper Questions & Session Token

    note over Student,ExamS: During Exam: Answer Selection & Proctor Telemetry
    loop Every Answer / Proctor Event
        Student->>ExamC: POST /api/v1/examination/cbe/save-answer
        ExamS->>DB: UPSERT exam_attempt_answers (questionId, selectedOption)
        
        opt Tab Switch / Window Blur Event
            Student->>ExamC: POST /api/v1/examination/cbe/proctor-event (TAB_SWITCH)
            ExamS->>DB: UPDATE exam_proctor_logs (tab_switches += 1)
        end

        opt Periodic Webcam Snapshot (Every 60s)
            Student->>MinIO: Upload Webcam Snapshot Image
            Student->>ExamC: POST /api/v1/examination/cbe/webcam-snapshot (imageKey)
            ExamS->>DB: INSERT into exam_proctor_snapshots
        end
    end

    note over Invigilator: Invigilator Monitors Live Dashboard
    Invigilator->>ExamC: GET /api/v1/examination/cbe/live-monitor
    ExamS-->>Invigilator: Return Active Attempts & Proctor Warning Counts

    opt Excessive Proctor Violations (Tab Switches > Max Limit)
        Invigilator->>ExamC: POST /api/v1/examination/cbe/terminate-session
        ExamS->>DB: UPDATE exam_attempts status = "TERMINATED_PROCTOR"
    end

    Student->>ExamC: POST /api/v1/examination/cbe/submit
    ExamS->>ExamS: Execute Auto-Grading & Calculate Total Score
    ExamS->>DB: UPDATE exam_attempts status = "SUBMITTED", score
    ExamS->>ExamS: Compute SGPA & CGPA
    ExamS->>DB: INSERT into exam_results
```

---

## 🔀 Exam Attempt State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> NOT_STARTED: Hall Ticket Issued
    NOT_STARTED --> IN_PROGRESS: Start Attempt Clicked
    IN_PROGRESS --> PAUSED: Invigilator Temporary Pause
    PAUSED --> IN_PROGRESS: Session Resumed
    IN_PROGRESS --> SUBMITTED: Finished by Student / Time Expired
    IN_PROGRESS --> TERMINATED_PROCTOR: Security Violations Triggered
    SUBMITTED --> GRADED: Auto-Graded & Results Processed
    GRADED --> CHALLENGED: Question Challenge Filed
    CHALLENGED --> GRADED: Challenge Approved / Rejected
    GRADED --> [*]
    TERMINATED_PROCTOR --> [*]
```

---

## ⚙️ Grading & SGPA/CGPA Calculation Algorithm

1. **Term SGPA Calculation**:
   $$\text{SGPA} = \frac{\sum (\text{Course Credits} \times \text{Grade Points Earned})}{\sum \text{Course Credits}}$$
2. **Cumulative CGPA Calculation**:
   $$\text{CGPA} = \frac{\sum (\text{Term SGPA} \times \text{Term Total Credits})}{\sum \text{Total Program Credits Completed}}$$
