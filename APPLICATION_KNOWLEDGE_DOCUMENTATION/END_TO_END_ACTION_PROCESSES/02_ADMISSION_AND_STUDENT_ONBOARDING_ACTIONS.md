# Action Lifecycle Manual: Admissions & Student Onboarding

## Action 2.1: Dynamic Application Form Submission & Attachment Upload

### 1. User Action & Frontend Trigger
- **User Role**: Applicant (`role: Applicant`)
- **Screen**: `StudentApplicationsPage.tsx`
- **User Input**: Program choice (e.g. B.Tech Computer Science), Previous Academic Percentage (88.5%), Address, Emergency Contact, 10th & 12th Marksheet PDFs.
- **Trigger**: Click **Submit Application & Pay Application Fee**.

### 2. Frontend State & Payload Construction
- Uploads PDF attachments to MinIO via `POST /api/v1/upload/file` -> Returns MinIO Object Keys (`docs/marksheet_12_john.pdf`).
- Sends HTTP POST payload:
  ```json
  {
    "formTemplateId": "template-cs-2024",
    "programId": "prog-cs-01",
    "academicYearId": "ay-2024-2025",
    "answers": {
      "qualifyingPercentage": 88.5,
      "boardName": "Central Board",
      "marksheetKey": "docs/marksheet_12_john.pdf"
    }
  }
  ```

### 3. API Routing & Guard Pipeline
- `POST /api/v1/admissions/applications`
- `GlobalJwtAuthGuard` verifies Bearer Token (`req.user.role == 'Applicant'`).

### 4. Backend Service Logic (`AdmissionsService.submitApplication`)
- Validates program seat availability and application deadline.
- Creates `FormSubmission` record in database.
- Calls `FeeService.createFeeDemand` for Application Processing Fee ($50).

### 5. Database Transactions & Persistence
- `INSERT INTO form_submissions (id, user_id, program_id, template_id, status = 'SUBMITTED', data = JSON)`
- `INSERT INTO fee_demands (user_id, amount = 50, status = 'PENDING', fee_head_id = 'HEAD_APP_FEE')`
- `INSERT INTO audit_logs (action = 'CREATE_APPLICATION', entity_id = :id)`

### 6. Side Effects & Outcome
- Application status set to `SUBMITTED`.
- Application Fee Demand ($50) generated; applicant redirected to Razorpay checkout screen.

---

## Action 2.2: Admission Officer Verification & Document Approval

### 1. User Action & Frontend Trigger
- **User Role**: Admission Officer (`role: InstAdmin` / Staff)
- **Screen**: `StudentApplicationsPage.tsx`
- **User Input**: Selects application `APP-2024-001`, reviews uploaded PDF preview in split-pane viewer, enters verification notes (`"Marksheet authentic, eligibility confirmed"`).
- **Trigger**: Click **Approve & Recommend for Merit List** button.

### 2. API & Service Logic
- `POST /api/v1/admissions/applications/:id/verify { status: "VERIFIED", notes: "..." }`.
- `GlobalJwtAuthGuard` & `RolesGuard` verify `InstAdmin` permissions.

### 3. Database Mutations
- `UPDATE form_submissions SET status = 'VERIFIED', review_data = JSON, verified_by = :userId, updated_at = NOW() WHERE id = :id`.
- `INSERT INTO notification_logs (user_id, template = 'APP_VERIFIED', status = 'SENT')`.

### 4. Outcome
- Candidate status updated to `VERIFIED`. Application moves into the Merit Ranking Pool.
