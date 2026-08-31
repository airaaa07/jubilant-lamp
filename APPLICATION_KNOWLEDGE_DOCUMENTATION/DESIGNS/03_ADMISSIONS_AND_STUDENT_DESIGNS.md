# UI Design Specs: Admissions & Student Profile Screens

## Pages Covered
- `AdmissionsPage.tsx`
- `StudentApplicationsPage.tsx`
- `MeritListPage.tsx`
- `FormsPage.tsx` (Admission Form subset)
- `StudentProfilePage.tsx`
- `OnboardStudentsPage.tsx`
- `AdmissionApplyModal.tsx`
- `ApplicationFeeModal.tsx`

---

## 1. Admissions Management Page (`AdmissionsPage.tsx`)

### Screen Purpose
Central admissions console for managing application cycles, seat availability (via `SeatMasterService`), merit list generation, and bulk admission operations per batch.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Admissions Management                                       │
│  [ Applications ] [ Merit Lists ] [ Seat Matrix ]            │
├──────────────────────────────────────────────────────────────┤
│  Batch Selector:  [ B.Tech CS 2024-2028 ▼ ]                 │
│  Academic Year:   [ 2024-2025 ▼ ]                            │
│                                                              │
│  Application Stats Summary                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐    │
│  │ Total    │ │ Verified │ │ Offered  │ │ Enrolled     │    │
│  │ 342      │ │ 280      │ │ 120      │ │ 95           │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘    │
│                                                              │
│  Merit List Actions:  [Run Merit Ranking] [Publish] [Reject] │
└──────────────────────────────────────────────────────────────┘
```

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/admissions` | List applications with filters |
| POST | `/api/admissions/merit-list/:batchId/compute` | Run merit ranking algorithm |
| POST | `/api/admissions/merit-list/:batchId/publish` | Publish merit list & send offers |
| POST | `/api/admissions/merit-list/:batchId/reject` | Bulk reject applications |
| GET | `/api/admissions/seat-master` | Seat availability matrix |

---

## 2. Student Applications Console (`StudentApplicationsPage.tsx`)

### Screen Purpose
Admissions desk workspace for viewing submitted student application forms, verifying uploaded marksheets/certificates, and executing workflow reviews. Supports both applicant self-view (my-applications) and admin review view.

### Layout & Component Specs
- **Filter Toolbar**: Multi-select dropdowns for Academic Year, Program Choice, Application Status (`Submitted`, `Under Review`, `Verified`, `Offered`, `Enrolled`, `Rejected`).
- **Application Split-View**:
  - Left Panel: List of candidate applications with score badges
  - Right Panel: Detailed view with applicant personal info, document preview modal (PDFs from MinIO), fee payment status, and decision actions
- **Decision Actions**:
  - `Verify & Approve for Merit List` → `PATCH /api/auth/registrations/:id/review { action: 'APPROVED' }`
  - `Request Document Correction` → `PATCH /api/auth/registrations/:id/review { action: 'NEEDS_CORRECTION' }`
  - `Reject Application` → `PATCH /api/auth/registrations/:id/review { action: 'REJECTED' }`
  - `Close Registration` → `PATCH /api/auth/registrations/:id/close`
  - `Offer Admission` → `PATCH /api/auth/registrations/:id/offer`

### Admission Apply Modal (`AdmissionApplyModal.tsx`)
- 38KB full-screen modal for applicants to fill the dynamic admission form
- Cascading programme/batch/stream selection
- Document upload integration with MinIO
- Academic history entry fields
- Triggers workflow creation on submission

### Application Fee Modal (`ApplicationFeeModal.tsx`)
- 60KB modal handling the Razorpay payment flow for application fees
- Displays fee breakdown by head
- Razorpay checkout integration
- Payment verification webhook handling
- Receipt generation post-payment

---

## 3. Merit List Page (`MeritListPage.tsx`)

### Screen Purpose
Displays ranked candidate lists per programme/batch, showing merit scores, rank positions, seat allocation status, and offer actions.

### Layout & Component Specs
- **Merit Table**: Ranked list with columns — Rank, Name, Application ID, Merit Score, Category, Seat Status
- **Offer Controls**: Buttons for individual/bulk seat offers, waitlist management
- **Category Reservation View**: Seat allocation breakdown by reservation category

---

## 4. Student 360° Profile Page (`StudentProfilePage.tsx`)

### Screen Purpose
Comprehensive profile view for a single student, consolidating academic history, attendance, fees, hostel, transport, exam results, and issued documents.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│ [ Avatar ]  Alex Kim  (Roll: CS2024-042)      [ Active ]     │
│ B.Tech Computer Science — Batch of 2024-2028                 │
├──────────────────────────────────────────────────────────────┤
│ [Academic] [Fees] [Attendance] [Exams] [Results] [Docs]      │
│ [Hostel] [Transport] [Notifications]                         │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Cumulative GPA: 3.84 / 4.0      Total Credits: 64        │ │
│ │ Stream Rule Version: CS_LABEL_V2 (Immutable)             │ │
│ ├──────────────────────────────────────────────────────────┤ │
│ │ Current Term Enrolled Courses:                           │ │
│ │ • CS301: Data Structures & Algorithms (4 Credits)        │ │
│ │ • CS302: Database Management Systems (4 Credits)         │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Profile Header Card**: Dark glass container with student photo avatar, roll number, assigned program, and status pill.
- **Tabbed Sub-Panels** (each backed by separate API endpoints):
  - **Dashboard Tab**: `GET /api/student-profile/dashboard` — quick overview with key metrics
  - **Academic Tab**: Term-wise SGPA/CGPA charts, grade sheets, stream rule snapshot
  - **Fees & Ledger Tab**: `GET /api/student-profile/fees` — outstanding demands, payment history
  - **Attendance Tab**: `GET /api/student-profile/attendance` — session-wise percentage rings
  - **Exams Tab**: `GET /api/student-profile/exams` — upcoming/past exams
  - **Results Tab**: `GET /api/student-profile/results`, `GET /api/student-profile/term-results` — SGPA/CGPA per term, drill-down via `/term-results/:batchTermId`
  - **Documents Tab**: `GET /api/student-profile/documents` — issued certificates & marksheets
  - **Hostel Tab**: `GET /api/student-profile/hostel` — room allocation, mess details
  - **Transport Tab**: `GET /api/student-profile/transport` — bus route, pass details
  - **Notifications Tab**: `GET /api/student-profile/notifications` — in-app notifications with mark-read
- **Profile Completion Gate** (`ProfileCompletionGate.tsx`): Blocks access until mandatory profile fields are filled
- **Not Enrolled Notice** (`NotEnrolledNotice.tsx`): Shows when student has no active enrollment
- **Academic Info Card** (`AcademicInfoCard.tsx`): Compact academic summary widget

### Student Enrollment Controller
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/student-enrollment/my-status` | Enrollment status for current user |
| GET | `/api/student-enrollment/my-profile` | Full student profile data |
| POST | `/api/student-enrollment/change-password` | Student password change |

---

## 5. Cancel Enrollment Module (`cancel-enrollment.controller.ts`)

### Screen Purpose
Handles enrollment cancellation requests with a multi-tier approval workflow. Supports role-based approval chains.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/cancel-enrollment/roles` | Get approval role config |
| PUT | `/api/cancel-enrollment/roles` | Save approval role config |
| POST | `/api/cancel-enrollment` | Initiate cancellation request |
| GET | `/api/cancel-enrollment/tasks` | Get pending approval tasks |
| POST | `/api/cancel-enrollment/:id/review` | Review request (approve/reject) |
| POST | `/api/cancel-enrollment/:id/approve` | Final approval |
