# Module 09: Counselling & Student Welfare — End-to-End Action Processes

> **Scope**: Backend API lifecycles, auto-assignment heuristics, counsellor contract credits, encrypted case comments, and session rating submissions.

---

## Action 1: Create Counselling Request (`POST /api/counselling/requests`)

- **HTTP Method & URL**: `POST /api/counselling/requests`
- **Guards**: `JwtAuthGuard` (Accessible by Students and Applicants)
- **Request Body (DTO: `CreateCounsellingRequestDto`)**:
  ```json
  {
    "category": "CAREER_GUIDANCE",
    "urgency": "NORMAL",
    "description": "Seeking advice regarding elective specialization in Artificial Intelligence vs Cybersecurity.",
    "preferredMode": "ONLINE_MEETING"
  }
  ```
- **Backend Auto-Assignment Heuristic**:
  1. Identifies available counsellors registered under the same `universityId`.
  2. Filters by matching specialization tags.
  3. Sorts by lowest active case count (least loaded) and contract credit limits.
  4. Auto-assigns case if `autoAssign: true` in `CounsellingConfig`.
- **Prisma Database Mutation**:
  ```prisma
  const request = await prisma.counsellingRequest.create({
    data: {
      studentId: req.user.studentId,
      applicantId: req.user.applicantId,
      category: dto.category,
      urgency: dto.urgency,
      description: dto.description,
      status: assignedCounsellorId ? "ASSIGNED" : "PENDING_ASSIGNMENT",
      counsellorId: assignedCounsellorId ?? null,
      assignedAt: assignedCounsellorId ? new Date() : null
    }
  });
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "creq_9941",
    "status": "ASSIGNED",
    "counsellorName": "Dr. Sarah Jenkins",
    "createdAt": "2026-09-11T12:00:00.000Z"
  }
  ```

---

## Action 2: Submit Confidential Recommendation & Credit Award (`POST /api/counselling/requests/:id/recommend`)

- **HTTP Method & URL**: `POST /api/counselling/requests/:id/recommend`
- **Guards**: `JwtAuthGuard`, `RolesGuard('Counsellor')`
- **Request Body**:
  ```json
  {
    "recommendation": "Advised candidate to pursue AI specialization based on strong linear algebra scores.",
    "followUpRequired": false,
    "sessionDurationMinutes": 45
  }
  ```
- **Backend Flow**:
  1. Verifies caller is the assigned counsellor for this case.
  2. Updates request status to `RESOLVED`.
  3. Inserts `CounsellorEnrollmentCredit` record to credit counsellor contract quota.
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "status": "RESOLVED",
    "creditAwarded": 1
  }
  ```
