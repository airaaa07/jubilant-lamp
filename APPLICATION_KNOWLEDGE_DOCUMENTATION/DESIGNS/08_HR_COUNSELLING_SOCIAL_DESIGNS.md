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
- `AnalyticsPage.tsx`
- `DashboardPage.tsx`
- `HelpCenterPage.tsx`

---

## 1. Executive Dashboard & Analytics (`DashboardPage.tsx` & `AnalyticsPage.tsx`)

### Screen Purpose
Main control center for university leadership. `DashboardPage.tsx` shows role-specific views: `ExecDashboard.tsx` for admins (23KB) and `PersonalDashboard.tsx` for students/staff (15KB).

### Component Specs
- **ExecDashboard** (`ExecDashboard.tsx`): 4 stat cards (Total Students, Live Exams, Fee Revenue, Recent Admissions), data tables for transactions and activities.
- **PersonalDashboard** (`PersonalDashboard.tsx`): Student-facing — upcoming classes, fee dues, exam schedule, attendance summary, notifications.
- **System Status** (`SystemStatus.tsx`, 13KB): Deployment info, service health, port status, module inventory — used by Settings and production promotion.
- **Analytics Page** (`AnalyticsPage.tsx`): Deep-dive charts and KPIs with date range filtering.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/analytics` | Dashboard analytics data |
| GET | `/api/analytics/me` | Personal dashboard data (student/staff) |

---

## 2. Staff HR & Leave Management (`HRPage.tsx` & `LeaveRequestsPage.tsx`)

### Screen Purpose
HR module for staff employee records, leave balance tracking (Casual, Sick, Earned Leave), leave application submissions, manager approvals, and leave reschedule management.

### Component Specs
- **Leave Balance Cards**: 3 stat pills showing Remaining Days per leave type.
- **Leave Request Table**: Applications with status pills (`APPROVED` green, `PENDING` yellow, `REJECTED` red).
- **Leave Reschedule**: Handles class/duty rescheduling when leave is approved.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/hr/staff` | List staff members |
| POST | `/api/hr/leave-requests` | Submit leave application |
| GET | `/api/hr/leave-requests` | List leave requests |
| PATCH | `/api/hr/leave-requests/:id` | Approve/reject leave |

### Backend Services
- **`hr.service.ts`**: Core HR operations, staff management.
- **`leave-reschedule.service.ts`**: Automated class rescheduling on leave approval.

---

## 3. Counselling Administration (`CounsellingAdminPage.tsx`)

### Screen Purpose
Admin configuration (33KB) for the counselling module — managing counsellor assignments, session types, availability schedules, and reporting.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/counselling/counsellors` | List counsellors |
| POST | `/api/counselling/counsellors` | Assign counsellor |
| GET | `/api/counselling/sessions` | List all sessions |
| GET | `/api/counselling/reports` | Analytics reports |

---

## 4. Counselling Desk Page (`CounsellingDeskPage.tsx`)

### Screen Purpose
Counsellor workspace (20KB) for session slot scheduling, appointment tracking, confidential session notes, and follow-up reminders.

### Component Specs
- **Session Calendar**: Day/week view of booked counselling appointments.
- **Session Notes Panel**: Confidential note-taking with encryption indicators.
- **Follow-up Reminders**: Scheduled reminder dispatch to students.

---

## 5. Notice Board Page (`NoticeBoardPage.tsx`)

### Screen Purpose
University-wide notice board (20KB) with category-based notices, scheduled publishing, expiry dates, and targeted audience (institute/department/role).

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/notice-board` | List notices |
| POST | `/api/notice-board` | Create notice |
| PATCH | `/api/notice-board/:id` | Update notice |
| DELETE | `/api/notice-board/:id` | Delete notice |

### Backend Services
- **`notice-board.service.ts`**: Notice CRUD.
- **`notice-board.scheduler.service.ts`**: Scheduled publish/expire operations.

---

## 6. Audit Log Page (`AuditLogPage.tsx`)

### Screen Purpose
Comprehensive audit trail viewer (43KB) with advanced filtering — by module, action type, actor, entity, date range, IP address. Shows login/logout events with device fingerprinting (OS, browser, hostname).

### Component Specs
- **Filter Bar**: Multi-select filters for Module, Action Type, Actor Role, Date Range, IP Address.
- **Log Table**: Timestamped entries with actor, action, entity, old/new value diff, IP/device info.
- **Drill Modal** (`DrillModal.tsx`): Detailed view of a single audit entry with full JSON diff.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/audit` | List audit log entries with filters |
| GET | `/api/audit/:id` | Get single entry detail |

---

## 7. Settings Console (`SettingsPage.tsx`)

### Screen Purpose
System settings hub (203KB — second largest page) for configuring:
- University branding (logos, colors, cover images)
- Email/SMS SMTP/gateway credentials and templates
- Database backup schedules and triggers
- Maintenance mode toggle
- Password policy configuration
- Notification preferences (daily summary settings)
- Social monitoring settings
- Custom role permissions matrices

### Component Specs
- **Tab Navigation**: Branding, Integrations (Email, SMS, LDAP), Security (Password Policy, Maintenance), Backup, Notifications, About.
- **Branding Module** (`branding.controller.ts`): Logo upload, color scheme, cover image.
- **Backup Module** (`backup.controller.ts`): Manual backup trigger, scheduled backup config, backup history, download.
- **User Management Settings Modal** (`UserManagementSettingsModal.tsx`, 26KB): Role-based access matrix configuration.
- **Document Settings Modal** (`DocumentSettingsModal.tsx`, 45KB): Certificate template default settings.
- **Day Summary Settings Modal** (`DaySummarySettingsModal.tsx`): Daily notification digest schedule.

---

## 8. ID Formats Page (`IdFormatsPage.tsx`)

### Screen Purpose
Configure auto-generated ID patterns for enrollment numbers, roll numbers, application IDs, and other system identifiers.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/id-format` | List ID format configurations |
| POST | `/api/id-format` | Create format |
| PATCH | `/api/id-format/:id` | Update format |

### Backend Services
- **`id-format.service.ts`**: Format template management.
- **`id-generator.service.ts`**: Runtime ID generation using configured templates.

---

## 9. Help Center Page (`HelpCenterPage.tsx`)

### Screen Purpose
Contextual help and knowledge base (5KB) with searchable articles, FAQ sections, and contact support info.

### Component Specs
- **Help Drawer** (`HelpDrawer.tsx`, 6KB): Slide-out contextual help panel available from any page.
- **Search Interface**: Full-text search across help articles.

---

## 10. Social Monitoring Module (`social-monitoring.controller.ts`)

### Screen Purpose
Social media monitoring for brand/reputation management — tracks mentions, sentiment analysis, and alert triggers.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/social-monitoring` | List monitored mentions |
| POST | `/api/social-monitoring/config` | Configure monitoring settings |
