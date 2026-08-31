# Action Lifecycle Manual: Dynamic Forms, Document Generation & Notifications

## Action 9.1: Dynamic Form Creation, Submission & Review

### 1. Form Template Creation
- **Role**: Admin / Registrar
- **Screen**: `FormsPage.tsx`
- Adds fields (text, textarea, number, select, radio, checkbox, date, file upload) with validation rules and cascading logic.
- `POST /api/forms` -> creates form template in `forms`.
- Clicks **Activate** -> `POST /api/forms/:id/activate` (status becomes `ACTIVE`).

### 2. User Form Submission & Save Draft
- Student opens `FormsPage.tsx` -> selects active form.
- Can save progress at any time: `POST /api/forms/:id/save-draft`.
- Uploads required attachments to MinIO via `POST /api/upload/file`.
- Clicks **Submit** -> `POST /api/forms/:id/submit` -> creates `FormSubmission` with status `SUBMITTED`.

### 3. Review & Approval
- Admin opens submissions tab -> selects submission.
- Clicks **Approve / Reject** with notes -> `PATCH /api/forms/submissions/:id/review { action: 'approved', rejectionNote?: '...' }`.
- Workflow progress tracked via `GET /api/forms/submissions/:id/progress`.

---

## Action 9.2: Canvas Document Template Design, Issuance & Public Verification

### 1. Canvas Designer & Preview
- **Role**: SuperAdmin / Registrar
- **Screen**: `DocumentsPage.tsx` -> `CanvasDocumentDesigner.tsx`
- Selects subject type (student/staff) via `GET /api/documents/subjects`.
- Inspects bindable field catalog via `GET /api/documents/field-catalog?subject=student`.
- Selects authorized signatories via `GET /api/documents/signatory-candidates`.
- Drags layout elements, background crest, dynamic placeholders (`{{student.fullName}}`), and verification QR code onto canvas.
- Renders live preview: `POST /api/documents/templates/preview` (merges test student data).
- Clicks **Publish** -> `POST /api/documents/templates`.

### 2. Document Issuance & Tracking
- Admin selects template and target students -> `POST /api/documents/issue`.
- Generates document records with unique cryptographically formatted serial numbers (e.g. `DOC-2026-004918`).
- Updates physical print status: `PATCH /api/documents/:id/print-status { status: 'printed' }`.
- Updates physical delivery status: `PATCH /api/documents/:id/delivery` or `POST /api/documents/bulk-delivery`.

### 3. Public Verification (Anti-Fraud)
- Employer / Verifier scans QR code on certificate or opens `GET /api/documents/verify/:serialNo`.
- No authentication required (`@Public()` endpoint).
- Returns verification status, student name, degree awarded, graduation date, and tamper-evident PDF view via `GET /api/documents/verify/:serialNo/view`.

---

## Action 9.3: Real-Time Notification Lifecycle & Daily Digests

### 1. In-App Notification Trigger & Unread Count
- Backend event (e.g. fee demand created, exam admit card released, leave approved) calls `NotificationsService.sendNotification(...)`.
- Creates record in `notifications` table.
- Frontend `NotificationBell.tsx` checks `GET /api/notifications/unread-count` and displays badge count.

### 2. Mark Read & Cleanup
- User clicks notification -> `PATCH /api/notifications/:id/read`.
- Bulk mark read -> `PATCH /api/notifications/read-all`.
- Delete notification -> `DELETE /api/notifications/:id`.

### 3. Daily Summary Digest
- Scheduled cron `DailySummaryService` runs at configured hour (e.g. 8:00 AM).
- Compiles unread notifications and pending tasks into a responsive HTML email digest.
- Dispatches email via `EmailService` (SMTP).
