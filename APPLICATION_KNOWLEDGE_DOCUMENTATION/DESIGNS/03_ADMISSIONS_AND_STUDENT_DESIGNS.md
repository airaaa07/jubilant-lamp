# UI Design Specs: Admissions & Student Profile Screens

## Pages Covered
- `AdmissionsPage.tsx`
- `StudentApplicationsPage.tsx`
- `MeritListPage.tsx`
- `FormsPage.tsx`
- `StudentProfilePage.tsx`

---

## 1. Student Applications Console (`StudentApplicationsPage.tsx`)

### Screen Purpose
Admissions desk workspace for viewing submitted student application forms, verifying uploaded marksheets/certificates, and executing workflow reviews.

### Layout & Component Specs
- **Filter Toolbar**: Multi-select dropdowns for Academic Year, Program Choice, Application Status (`Submitted`, `Under Review`, `Approved`, `Rejected`).
- **Application Split-View**:
  - Left Panel: List of candidate applications with score badges.
  - Right Panel: Detailed view displaying applicant personal info, document preview modal, fee payment confirmation tag, and decision actions (`Approve for Merit List`, `Request Document Correction`, `Reject Application`).

---

## 2. Student 360° Profile Page (`StudentProfilePage.tsx`)

### Screen Purpose
Comprehensive profile view for a single student, consolidating academic history, attendance percentage, fee demand balance, hostel room allocation, and issued certificates.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│ [ Avatar ]  Alex Kim  (Roll: CS2024-042)      [ Active ]     │
│ B.Tech Computer Science — Batch of 2024-2028                 │
├──────────────────────────────────────────────────────────────┤
│ [ Academic ] [ Fees & Ledger ] [ Attendance ] [ Hostel/Lib ] │
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
- **Profile Header Card**: Dark glass container with student photo avatar, roll number, assigned program, and status pill (`bg-emerald-500/10 text-emerald-400 border border-emerald-500/20`).
- **Tabbed Sub-Panels**:
  - **Academic Tab**: Term-wise SGPA/CGPA charts, grade sheets, stream rule snapshot status.
  - **Fees & Ledger Tab**: Outstanding fee demands, payment history ledger, deposit status.
  - **Attendance Tab**: Session-wise attendance percentage circular progress rings.
  - **Hostel & Library Tab**: Allocated room details, library book loans, gate pass history.
