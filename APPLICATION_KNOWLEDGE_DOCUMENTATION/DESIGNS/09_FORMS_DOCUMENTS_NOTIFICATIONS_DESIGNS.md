# UI Design Specs: Forms, Documents & Notifications Screens

## Pages Covered
- `FormsPage.tsx`
- `DocumentsPage.tsx`
- `NotificationsPage.tsx`
- `CanvasDocumentDesigner.tsx`
- `NotificationBell.tsx`
- `ReadOnlyFormView.tsx`

---

## 1. Dynamic Forms Builder & Submissions (`FormsPage.tsx`)

### Screen Purpose
Comprehensive form management system (154KB — third largest page) for creating dynamic form templates, publishing forms, collecting submissions, and reviewing responses. Powers the admission application forms, general surveys, and custom data collection.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Forms & Surveys                                             │
│  [ My Forms ] [ Active Forms ] [ My Submissions ]            │
├──────────────────────────────────────────────────────────────┤
│  Form Templates                              [ + Create ]    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Name                │ Status  │ Responses │ Actions    │  │
│  ├─────────────────────┼─────────┼───────────┼────────────┤  │
│  │ Admission Form 2024 │ ACTIVE  │ 342       │ [Edit][▶]  │  │
│  │ Feedback Survey     │ DRAFT   │ 0         │ [Edit][▶]  │  │
│  │ Hostel Application  │ ACTIVE  │ 120       │ [Edit][⏸]  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Form Template Builder**: Visual field editor supporting:
  - Text inputs, textareas, number fields
  - Dropdown selects, radio buttons, checkboxes
  - Date pickers, file upload fields
  - Section dividers, conditional logic
  - Cascading field dependencies
- **Form Lifecycle**: Draft → Active → Deactivated
- **Submission Views**:
  - Admin: Review all submissions per form, approve/reject
  - Student: View active forms, fill and submit, track progress
  - Read-Only View (`ReadOnlyFormView.tsx`): Display submitted form data without edit
- **Admission Form Integration**: Dedicated `GET /api/forms/admission-form` endpoint returns the form template configured for admission use
- **Save Draft**: Students can save partial submissions and resume later

### Forms API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/forms` | List all form templates (admin) |
| GET | `/api/forms/active` | List active forms (students) |
| GET | `/api/forms/my-submissions` | Student's own submissions |
| GET | `/api/forms/admission-form` | Get admission form template |
| GET | `/api/forms/:id` | Get specific form template |
| POST | `/api/forms` | Create form template |
| PUT | `/api/forms/:id` | Update form template |
| POST | `/api/forms/:id/activate` | Activate form |
| POST | `/api/forms/:id/deactivate` | Deactivate form |
| DELETE | `/api/forms/:id` | Delete form |
| GET | `/api/forms/:id/submissions` | List submissions for form |
| POST | `/api/forms/:id/save-draft` | Save draft submission |
| POST | `/api/forms/:id/submit` | Submit form |
| PATCH | `/api/forms/submissions/:id/review` | Review submission (approve/reject) |
| GET | `/api/forms/submissions/:id/progress` | Submission workflow progress |

### Public Forms Controller (`forms-public.controller.ts`)
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/forms-public/:id` | Get public form (no auth) |
| POST | `/api/forms-public/:id/submit` | Submit public form |

---

## 2. Documents & Certificate Management (`DocumentsPage.tsx`)

### Screen Purpose
Document template design, issuance, printing, delivery tracking, and public verification system (44KB). Supports certificates, marksheets, transcripts, and custom documents.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Documents & Certificates                                    │
│  [ Templates ] [ Issued Documents ] [ My Documents ]         │
├──────────────────────────────────────────────────────────────┤
│  Template Library                          [ + Design New ]  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Template Name        │ Subject │ Status │ Issued Count │  │
│  ├──────────────────────┼─────────┼────────┼──────────────┤  │
│  │ B.Tech Degree Cert.  │ Student │ Active │ 450          │  │
│  │ Transfer Certificate │ Student │ Active │ 23           │  │
│  │ Staff ID Card        │ Staff   │ Draft  │ 0            │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Canvas Document Designer (`CanvasDocumentDesigner.tsx`)
51KB interactive canvas-based template designer:
- **Drag-and-Drop Elements**: Text blocks, dynamic data fields, images, signatures, QR codes, borders, watermarks
- **Field Catalog**: Bindable data attributes per subject type (student/staff) — name, enrollment number, programme, CGPA, etc. via `GET /api/documents/field-catalog`
- **Subject Types**: `GET /api/documents/subjects` — student, staff, custom
- **Signatory Configuration**: `GET /api/documents/signatory-candidates` — select officials as document signatories
- **Live Preview**: `POST /api/documents/templates/preview` — render with sample or real student data
- **Document Settings Modal** (`DocumentSettingsModal.tsx`, 45KB): Default signatories, header/footer, formatting

### Document Issuance & Tracking
| Category | Method | Endpoint | Purpose |
|:---|:---|:---|:---|
| **Templates** | POST | `/api/documents/templates` | Create template |
| | GET | `/api/documents/templates` | List templates |
| | GET | `/api/documents/templates/:id` | Get template |
| | PATCH | `/api/documents/templates/:id` | Update template |
| | PATCH | `/api/documents/templates/:id/active` | Toggle active |
| | DELETE | `/api/documents/templates/:id` | Delete template |
| **Issue** | POST | `/api/documents/issue` | Issue document to student/staff |
| | GET | `/api/documents/student-terms` | Student terms for document context |
| **Access** | GET | `/api/documents` | List issued documents |
| | GET | `/api/documents/my` | My issued documents (student) |
| | GET | `/api/documents/:id` | Get issued document |
| | GET | `/api/documents/:id/render` | Render document (PDF/HTML) |
| | GET | `/api/documents/serial/:serialNo` | Lookup by serial number |
| **Delivery** | PATCH | `/api/documents/:id/delivery` | Set delivery status |
| | POST | `/api/documents/bulk-delivery` | Bulk delivery update |
| | PATCH | `/api/documents/:id/mark-issued` | Mark as physically issued |
| | PATCH | `/api/documents/:id/print-status` | Set print status |
| **Revoke** | PATCH | `/api/documents/:id/revoke` | Revoke document |
| **Access Config** | GET | `/api/documents/access-config` | Role-based access config |
| | PUT | `/api/documents/access-config` | Save access config |
| **Public Verify** | GET | `/api/documents/verify/:serialNo` | Public verification (no auth) |
| | GET | `/api/documents/verify/:serialNo/view` | Public document view |

---

## 3. Notifications System

### Notification Bell Component (`NotificationBell.tsx`)
5.6KB persistent header component:
- **Unread Badge**: Red counter badge on bell icon showing unread count
- **Dropdown Panel**: Recent notifications preview with mark-read on click
- **Poll/Refresh**: Periodic unread count check via `GET /api/notifications/unread-count`

### Notifications Page (`NotificationsPage.tsx`)
Full notification center (6.5KB):
- **Notification List**: Chronological list with read/unread styling
- **Bulk Actions**: Mark all read, mark all unread, clear all
- **Individual Actions**: Mark read/unread, delete

### Notifications API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/notifications` | List notifications |
| GET | `/api/notifications/unread-count` | Unread count for badge |
| PATCH | `/api/notifications/read-all` | Mark all as read |
| PATCH | `/api/notifications/unread-all` | Mark all as unread |
| DELETE | `/api/notifications` | Clear all notifications |
| PATCH | `/api/notifications/:id/read` | Mark single as read |
| PATCH | `/api/notifications/:id/unread` | Mark single as unread |
| DELETE | `/api/notifications/:id` | Delete single notification |

### Backend Notification Services
- **`notifications.service.ts`**: Core notification creation, delivery, storage.
- **`email.service.ts`**: SMTP email delivery with template rendering.
- **`sms.service.ts`**: SMS gateway integration (DLT-compliant OTP templates).
- **`message-template.service.ts`**: Notification message templates with variable interpolation.
- **`daily-summary.service.ts`**: Scheduled daily digest email with activity summary.
