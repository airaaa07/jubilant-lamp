# Action Lifecycle Manual: Admissions & Student Onboarding

## Action 2.1: Student Application Submission & Document Upload

### 1. User Action & Frontend Trigger
- **User Role**: Applicant
- **Screen**: `StudentApplicationsPage.tsx` / `AdmissionApplyModal.tsx`
- **Input**: Personal details, past academic qualifications, scanned documents (10th/12th marksheets, caste certificate, photo).
- **Trigger**: Click **Submit Application** button.

### 2. Frontend Flow & MinIO Upload
- Documents are uploaded to MinIO object storage via `POST /api/upload/file` using multipart/form-data.
- Receives file keys / URLs and binds them to the application form schema.
- Sends application payload:
  ```json
  {
    "programmeId": "prog-uuid-123",
    "batchId": "batch-uuid-456",
    "academicHistory": [
      { "qualification": "10th", "score": 92.5, "documentUrl": "minio://docs/10th.pdf" },
      { "qualification": "12th", "score": 89.0, "documentUrl": "minio://docs/12th.pdf" }
    ],
    "category": "GENERAL"
  }
  ```

### 3. API Routing & Guard Pipeline
- **Endpoint**: `POST /api/forms/:id/submit` (or `POST /api/admissions/apply`)
- **Guards**: `JwtAuthGuard`.

### 4. Backend Processing
- Validates batch seat availability with `SeatMasterService`.
- Creates `FormSubmission` and links to `Registration`.
- Triggers application fee demand creation via `FeeService`.

### 5. Application Fee Payment (Razorpay)
- User opens `ApplicationFeeModal.tsx`.
- Calls `POST /api/fee/payments/create-order` -> Razorpay order created.
- User completes checkout; Webhook `POST /api/fee/webhooks/razorpay` verifies signature and marks demand `PAID`.
- Status transitions: `DRAFT` -> `SUBMITTED` -> `UNDER_REVIEW`.

---

## Action 2.2: Application Review, Merit List Generation & Seat Allotment

### 1. Admission Desk Verification
- **Screen**: `StudentApplicationsPage.tsx` (Admin view).
- Coordinator verifies documents, enters verification note.
- `PATCH /api/auth/registrations/:id/review { action: "APPROVED" }`.
- Status becomes `VERIFIED`.

### 2. Merit List Computation
- **Role**: HOD / Admission In-Charge.
- **Screen**: `MeritListPage.tsx`.
- Trigger: Clicks **Run Merit Ranking**.
- `POST /api/admissions/merit-list/:batchId/compute`.
- Backend executes merit ranking algorithm based on 10th/12th weighted scores, reservation category rules, and batch seat capacity.
- Generates rank list in `merit_list_entries`.

### 3. Publishing & Seat Offers
- Click **Publish Merit List** -> `POST /api/admissions/merit-list/:batchId/publish`.
- Status for top candidates updated to `OFFERED`.
- Notification emails dispatched with offer deadline.

---

## Action 2.3: Student Onboarding, Role Conversion & ID Generation

### 1. Applicant Accepts Offer & Pays Admission Fee
- Applicant logs in, clicks **Accept Seat**.
- Pays admission fee via Razorpay modal.
- System transitions user role from `Applicant` to `Student`.

### 2. Administrator ID Generation & Profile Commitment
- **Screen**: `OnboardStudentsPage.tsx`.
- Administrator reviews accepted candidate.
- Clicks **Generate Student ID** -> `POST /api/onboarding/commit`.
- `IdGeneratorService` evaluates the configured ID format (e.g. `CS/2026/0042`), reserves sequence, and commits `student_profiles` record.
- Student is enrolled in Term 1 and sections are assigned.
