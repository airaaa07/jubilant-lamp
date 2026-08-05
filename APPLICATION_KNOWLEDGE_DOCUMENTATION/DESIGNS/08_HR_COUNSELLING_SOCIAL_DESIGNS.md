# UI Design Specs: HR, Counselling, Settings & Operations Screens

## Pages Covered
- `HRPage.tsx`
- `LeaveRequestsPage.tsx`
- `CounsellingAdminPage.tsx`
- `CounsellingDeskPage.tsx`
- `NoticeBoardPage.tsx`
- `AuditLogPage.tsx`
- `SettingsPage.tsx`
- `IdFormatsPage.tsx`
- `ValidationPage.tsx`
- `AnalyticsPage.tsx`
- `DashboardPage.tsx`

---

## 1. Executive Analytics & Dashboard (`DashboardPage.tsx` & `AnalyticsPage.tsx`)

### Screen Purpose
The main control center for university leadership, presenting overall system health, enrollment statistics, fee revenue charts, live exam activity, and operational alerts.

### Visual Mockup Render
![Executive Admin Dashboard UI Mockup](/home/admin/.gemini/antigravity-ide/brain/61696b17-1fe4-429b-b9b6-60a5b523471f/dashboard_ui_mockup_1785931486163.png)

### Component Specs
- **Metrics Grid**: 4 stat cards displaying Total Students, Live AI Proctored Exams, Fee Revenue Progress Bar Chart, and Recent Admissions Timeline.
- **Data Table Panel**: Recent financial transactions and recent user activities table.

---

## 2. Staff HR & Leave Requests Page (`HRPage.tsx` & `LeaveRequestsPage.tsx`)

### Screen Purpose
Oversees staff employee records, leave balance tracking (Casual Leave, Sick Leave, Earned Leave), leave application submissions, and manager approvals.

### Component Specs
- **Leave Balance Cards**: 3 stat pills showing Remaining Days per leave type.
- **Leave Request Table**: List of leave applications with status pills (`APPROVED` green, `PENDING` yellow, `REJECTED` red).

---

## 3. Counselling Desk Page (`CounsellingDeskPage.tsx`)

### Screen Purpose
Provides student counsellors with session slot scheduling, appointment tracking, confidential session notes, and follow-up reminders.

---

## 4. Settings & Roles Console (`SettingsPage.tsx`)

### Screen Purpose
System settings hub for configuring university branding (logos, colors), email/SMS SMTP credentials, database backup schedules, and custom role permissions matrices.
