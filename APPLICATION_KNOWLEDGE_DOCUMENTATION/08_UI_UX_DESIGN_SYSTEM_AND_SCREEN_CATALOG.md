# UI/UX Design System & Master Screen Design Catalog

## Overview
This document serves as the master catalog for all **45 user interface screens and component design specifications** implemented across UniversityERP. It defines the universal design system, color palette, typography hierarchy, layout grid, interactive state guidelines, and visual wireframe breakdowns for every page in the application.

---

## 🎨 Global Design System Specifications

### 1. Theme & Color Palette
The application utilizes a sleek, state-of-the-art dark mode UI with vibrant neon accent highlights and subtle glassmorphism container elevation.

| Color Category | Token Name | Hex Code / HSL | Usage Application |
| :--- | :--- | :--- | :--- |
| **Background Dark Base** | `bg-slate-950` | `#020617` | Root viewport background |
| **Surface Card (Glass)** | `bg-slate-900/80` | `#0f172a` (80% Opacity) | Container cards with `backdrop-blur-md` |
| **Border Glow** | `border-slate-800` | `#1e293b` | Subtle divider and card outlines |
| **Primary Accent (Indigo)**| `accent-indigo` | `#6366f1` | Active navigation, primary buttons, focus states |
| **Secondary Accent (Cyan)** | `accent-cyan` | `#06b6d4` | Live status indicators, proctoring active states |
| **Success Status** | `status-emerald` | `#10b981` | Paid status, approved workflows, passed exams |
| **Warning Status** | `status-amber` | `#f59e0b` | Pending approvals, partial payments, exam flags |
| **Danger Status** | `status-rose` | `#f43f5e` | Overdue fee demands, proctoring violations, account lock |

---

### 2. Typography Hierarchy
Typography is powered by clean modern sans-serif typefaces (`Inter`, `Outfit`, `Roboto` via Google Fonts).

- **Display H1**: `2.25rem (36px)` / `Font-Weight: 700` / `Tracking: -0.025em` (Page Titles)
- **Section H2**: `1.5rem (24px)` / `Font-Weight: 600` (Module Headers, Card Titles)
- **Subhead H3**: `1.125rem (18px)` / `Font-Weight: 500` (Form Section Labels)
- **Body Regular**: `0.875rem (14px)` / `Font-Weight: 400` / `Leading: 1.5` (Table data, body text)
- **Caption / Badge**: `0.75rem (12px)` / `Font-Weight: 600` / `Uppercase` (Status badges, pill labels)

---

### 3. Layout Grid & Component Tokens

```
┌───────────────────────────────────────────────────────────────┐
│                        Top Navbar Header                      │
│ ┌──────────────┐  [ Search bar... ]   (Notif) [ User Avatar ] │
├────────────────┴──────────────────────────────────────────────┤
│ Left Sidebar │               Main Content Area                │
│ Navigation   │ ┌──────────────────┐  ┌──────────────────────┐ │
│ ├── Dashboard│ │ Metric Card 1    │  │ Metric Card 2        │ │
│ ├── Academics│ └──────────────────┘  └──────────────────────┘ │
│ ├── Finance  │ ┌──────────────────────────────────────────┐ │
│ ├── Exams    │ │ Interactive Data Table / Main Workspace  │ │
│ └── Settings │ └──────────────────────────────────────────┘ │
└──────────────┴────────────────────────────────────────────────┘
```

---

## 🖼️ Representative UI Visual Mockups

### 1. Executive Dashboard UI
![Executive Admin Dashboard UI Mockup](/home/admin/.gemini/antigravity-ide/brain/61696b17-1fe4-429b-b9b6-60a5b523471f/dashboard_ui_mockup_1785931486163.png)

### 2. Computer-Based Examination (CBE) & AI Proctoring UI
![CBE Online Exam and AI Proctoring UI Mockup](/home/admin/.gemini/antigravity-ide/brain/61696b17-1fe4-429b-b9b6-60a5b523471f/cbe_exam_proctoring_1785931500481.png)

### 3. Visual Workflow Designer UI
![Visual Workflow Designer UI Mockup](/home/admin/.gemini/antigravity-ide/brain/61696b17-1fe4-429b-b9b6-60a5b523471f/workflow_designer_ui_1785931519025.png)

---

## 📂 Separated Domain Screen Design Files

The complete design specifications for all 45 application pages have been cataloged into **8 individual design documents** located in [`APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/):

1. **[`DESIGNS/01_AUTH_AND_ONBOARDING_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/01_AUTH_AND_ONBOARDING_DESIGNS.md)**
   - `LoginPage.tsx`, `RegisterPage.tsx`, `ForgotPasswordPage.tsx`, `ResetPasswordPage.tsx`, `SetupAccountPage.tsx`, `OnboardStudentsPage.tsx`, `BannersPage.tsx`.
2. **[`DESIGNS/02_ACADEMIC_AND_FACULTY_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/02_ACADEMIC_AND_FACULTY_DESIGNS.md)**
   - `MasterDataPage.tsx`, `ElectivesPage.tsx`, `TimetablePage.tsx`, `AttendancePage.tsx`, `DirectoryPage.tsx`.
3. **[`DESIGNS/03_ADMISSIONS_AND_STUDENT_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/03_ADMISSIONS_AND_STUDENT_DESIGNS.md)**
   - `AdmissionsPage.tsx`, `StudentApplicationsPage.tsx`, `MeritListPage.tsx`, `FormsPage.tsx`, `StudentProfilePage.tsx`.
4. **[`DESIGNS/04_EXAMINATIONS_AND_CBE_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/04_EXAMINATIONS_AND_CBE_DESIGNS.md)**
   - `ExaminationsPage.tsx`, `ExamTakePage.tsx`, `ExamMonitorPage.tsx`, `ExamItemAnalysisPage.tsx`, `MyInvigilationPage.tsx`.
5. **[`DESIGNS/05_FEE_AND_FINANCIAL_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/05_FEE_AND_FINANCIAL_DESIGNS.md)**
   - `FeesPage.tsx`, `ProgramFeeManager.tsx`, `ResourceFeeManager.tsx`, Razorpay Payment Modal UI.
6. **[`DESIGNS/06_INFRASTRUCTURE_FACILITIES_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/06_INFRASTRUCTURE_FACILITIES_DESIGNS.md)**
   - `HostelPage.tsx`, `TransportPage.tsx`, `LibraryPage.tsx`.
7. **[`DESIGNS/07_WORKFLOW_AND_AUTOMATION_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/07_WORKFLOW_AND_AUTOMATION_DESIGNS.md)**
   - `WorkflowDesignerPage.tsx`, `WorkflowMonitorPage.tsx`, `MyTasksPage.tsx`.
8. **[`DESIGNS/08_HR_COUNSELLING_SOCIAL_DESIGNS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/DESIGNS/08_HR_COUNSELLING_SOCIAL_DESIGNS.md)**
   - `HRPage.tsx`, `LeaveRequestsPage.tsx`, `CounsellingAdminPage.tsx`, `CounsellingDeskPage.tsx`, `NoticeBoardPage.tsx`, `AuditLogPage.tsx`, `SettingsPage.tsx`, `IdFormatsPage.tsx`, `ValidationPage.tsx`, `AnalyticsPage.tsx`, `DashboardPage.tsx`, `HelpCenterPage.tsx`.
