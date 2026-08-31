# Technical Workflow Architecture: Forms, Documents & Notifications

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, state machine transitions, and database mutations for dynamic form generation, submission reviews, the Canvas Document Designer, certificate issuance & printing, public anti-fraud verification, and multi-channel notifications.

---

## 🔄 End-to-End Sequence Diagram: Dynamic Forms & Submissions

```mermaid
sequenceDiagram
    autonumber
    actor User as Student / Applicant
    participant FormsC as FormsController
    participant FormsS as FormsService
    participant MinIO as MinIO Storage
    participant DB as PostgreSQL Database
    actor Admin as Form Reviewer / Admin

    User->>FormsC: GET /api/forms/active
    FormsC->>FormsS: getActiveForms(userScope)
    FormsS->>DB: Query forms WHERE is_active = true
    DB-->>FormsC: Return Active Form Templates
    FormsC-->>User: Form Schema & Field Catalog

    User->>FormsC: POST /api/forms/:id/save-draft (Partial answers)
    FormsC->>FormsS: saveDraft(id, dto, user)
    FormsS->>DB: UPSERT into form_submissions (status: 'DRAFT')
    DB-->>FormsC: Draft Saved

    User->>FormsC: POST /api/forms/:id/submit (Final Submission)
    FormsC->>FormsS: submit(id, dto, user)
    FormsS->>DB: UPDATE form_submissions SET status = 'SUBMITTED', submitted_at = now()
    FormsS->>DB: INSERT into audit_logs (FORM_SUBMITTED)
    DB-->>FormsC: Return Submission ID & Status

    Admin->>FormsC: PATCH /api/forms/submissions/:id/review { action: 'approved' }
    FormsC->>FormsS: reviewSubmission(id, dto, admin)
    FormsS->>DB: UPDATE form_submissions SET status = 'APPROVED', reviewer_id = admin.id
    FormsS-->>User: Notification: "Form Submission Approved"
```

---

## 🔄 End-to-End Sequence Diagram: Canvas Document Designer & Verification

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Registrar / SuperAdmin
    participant DocsC as DocumentsController
    participant DocsS as DocumentsService
    participant DB as PostgreSQL Database
    actor Verifier as Public Employer / Verifier

    Admin->>DocsC: POST /api/documents/templates (Canvas Layout JSON, Fields, QR)
    DocsC->>DocsS: createTemplate(dto)
    DocsS->>DB: INSERT into document_templates (status: 'ACTIVE')
    
    Admin->>DocsC: POST /api/documents/issue (templateId, studentIds)
    DocsC->>DocsS: issueDocument(dto)
    DocsS->>DocsS: Generate Unique Serial (e.g. DOC-2026-98124)
    DocsS->>DB: INSERT into issued_documents (serial_no, status: 'ISSUED')
    
    Verifier->>DocsC: GET /api/documents/verify/DOC-2026-98124 (@Public)
    DocsC->>DocsS: verifyDocument(serialNo)
    DocsS->>DB: Query issued_documents + student + template
    DB-->>DocsC: Return Verified Document Data
    DocsC-->>Verifier: Tamper-Evident Verification Card + Digital Copy
```

---

## 🔀 Document Issuance State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Create Template
    DRAFT --> ACTIVE: Publish Template
    ACTIVE --> ISSUED: Issue to Student
    ISSUED --> PRINTED: Marked Physical Print
    PRINTED --> DELIVERED: Handed to Student
    ISSUED --> REVOKED: Cancelled / Disciplinary Action
    PRINTED --> REVOKED: Revoked Post-Print
    DELIVERED --> REVOKED: Revoked Post-Delivery
    REVOKED --> [*]
    DELIVERED --> [*]
```

---

## 📊 Database Mutations & Schema Entities

1. **`FormTemplate` (`forms`)**:
   - `id`, `title`, `description`, `fields` (JSON Schema), `is_active`, `course_type`, `institute_id`.
2. **`FormSubmission` (`form_submissions`)**:
   - `id`, `form_id`, `user_id`, `data` (JSON response payload), `status` (`DRAFT`, `SUBMITTED`, `APPROVED`, `REJECTED`), `rejection_note`, `reviewed_at`.
3. **`DocumentTemplate` (`document_templates`)**:
   - `id`, `name`, `subject` (`STUDENT`, `STAFF`), `canvas_layout` (JSON coordinates & elements), `signatories` (JSON array), `is_active`.
4. **`IssuedDocument` (`issued_documents`)**:
   - `id`, `template_id`, `recipient_id`, `serial_no`, `print_status` (`PENDING`, `PRINTED`), `delivery_status` (`PENDING`, `DELIVERED`), `is_revoked`, `revoked_reason`.
5. **`Notification` (`notifications`)**:
   - `id`, `user_id`, `title`, `message`, `type`, `is_read`, `action_url`, `created_at`.
