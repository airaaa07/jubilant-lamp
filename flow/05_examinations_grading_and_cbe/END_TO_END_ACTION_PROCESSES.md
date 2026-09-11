# Module 05: Examinations, Grading & CBE — End-to-End Action Processes

> **Scope**: Backend request pipelines, real-time CBE execution endpoints, proctoring websocket/polling protocol, question response persistence, automated grading algorithms, and grading component locks.

---

## Action 1: Start CBE Attempt (`POST /api/examination/papers/:id/start`)

- **HTTP Method & URL**: `POST /api/examination/papers/:id/start`
- **Guards**: `JwtAuthGuard`, `StudentGuard`
- **Backend Flow**:
  1. Validates `ExamPaper` exists, paper window is currently open (`startTime <= now <= endTime`), and student is eligible (checks `ExamAdmitCardIneligibility`).
  2. Queries or creates `ExamAttempt` row. If previously started, resumes attempt with remaining elapsed time.
  3. If paper has `shuffleQuestions: true`, generates deterministic randomized question sequence per `studentId`.
  4. Returns sanitized question list (answers stripped).
- **Prisma Database Mutation**:
  ```prisma
  const attempt = await prisma.examAttempt.upsert({
    where: {
      examPaperId_studentId: {
        examPaperId: id,
        studentId: req.user.studentId
      }
    },
    create: {
      examPaperId: id,
      studentId: req.user.studentId,
      status: "IN_PROGRESS",
      startedAt: new Date(),
      ipAddress: req.ip
    },
    update: {
      lastHeartbeatAt: new Date()
    },
    include: {
      examPaper: {
        include: {
          questions: {
            select: {
              id: true,
              questionType: true,
              content: true,
              options: true,
              marks: true,
              sortOrder: true
            }
          }
        }
      }
    }
  });
  ```
- **Response (200 OK)**:
  ```json
  {
    "attemptId": "att_882910",
    "paperTitle": "Mid-Term Examination: Computer Networks",
    "durationMinutes": 60,
    "remainingSeconds": 3540,
    "questions": [
      {
        "id": "q_101",
        "type": "MCQ",
        "content": "Which layer of the OSI model does TCP operate on?",
        "options": ["Transport", "Network", "Data Link", "Session"],
        "marks": 2
      }
    ]
  }
  ```

---

## Action 2: Save Question Response (`POST /api/examination/attempts/:id/response`)

- **HTTP Method & URL**: `POST /api/examination/attempts/:id/response`
- **Request Body**:
  ```json
  {
    "questionId": "q_101",
    "selectedOptions": [0],
    "textResponse": null,
    "timeSpentSeconds": 24
  }
  ```
- **Backend Flow**:
  1. Validates `ExamAttempt` is in `IN_PROGRESS` state and within time limit.
  2. Upserts `ExamResponse` record.
  3. Updates `attempt.lastHeartbeatAt = now()`.
- **Prisma Mutation**:
  ```prisma
  await prisma.examResponse.upsert({
    where: {
      examAttemptId_questionId: {
        examAttemptId: id,
        questionId: dto.questionId
      }
    },
    create: {
      examAttemptId: id,
      questionId: dto.questionId,
      selectedOptions: dto.selectedOptions,
      textResponse: dto.textResponse,
      timeSpentSeconds: dto.timeSpentSeconds
    },
    update: {
      selectedOptions: dto.selectedOptions,
      textResponse: dto.textResponse,
      timeSpentSeconds: { increment: dto.timeSpentSeconds }
    }
  });
  ```
- **Response (200 OK)**: `{ "saved": true, "timestamp": "2026-09-11T12:05:00Z" }`

---

## Action 3: Ingest Proctoring Violation Event (`POST /api/examination/attempts/:id/proctor-event`)

- **HTTP Method & URL**: `POST /api/examination/attempts/:id/proctor-event`
- **Request Body**:
  ```json
  {
    "eventType": "FOCUS_LOST",
    "details": { "durationMs": 4200, "windowBlurred": true }
  }
  ```
- **Prisma Mutation**:
  ```prisma
  await prisma.examProctorEvent.create({
    data: {
      examAttemptId: id,
      eventType: dto.eventType,
      severity: "WARNING",
      metadata: dto.details,
      timestamp: new Date()
    }
  });

  await prisma.examAttempt.update({
    where: { id },
    data: { violationCount: { increment: 1 } }
  });
  ```
- **Response (200 OK)**: `{ "recorded": true, "totalViolations": 2 }`
