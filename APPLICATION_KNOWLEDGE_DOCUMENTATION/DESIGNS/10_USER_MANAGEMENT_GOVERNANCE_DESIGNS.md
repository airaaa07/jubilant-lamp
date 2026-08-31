# UI Design Specs: User Management, Governance & System Administration

## Pages Covered
- `UserManagementPage.tsx`
- `GovernedProfileSection.tsx` (component)
- `IdFormatsPage.tsx`
- `BatchSetupWizard.tsx` & `BatchSetupList.tsx` (components)
- Roles Module
- Profile Governance Module
- Parent Portal Module
- Branding Module

---

## 1. User Management Console (`UserManagementPage.tsx`)

### Screen Purpose
Central user administration hub (120KB) for creating, importing, editing, and managing all system users — students, teaching staff, non-teaching staff, and administrators. Handles role assignments, password resets, account locking/unlocking, and bulk user import.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  User Management                                             │
│  [ All Users ] [ By Role ] [ Bulk Import ]                   │
├──────────────────────────────────────────────────────────────┤
│  Search: [________________________] Role: [All ▼]            │
│  Status: [Active ▼]                                          │
│                                                              │
│  Users Table                              [ + Create User ]  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Name      │ Email           │ Role    │ Status│Actions │  │
│  ├───────────┼─────────────────┼─────────┼───────┼────────┤  │
│  │ Dr. Patel │ patel@univ.edu  │ HOD     │ ✅    │ [⚙][🔑]│  │
│  │ Alex Kim  │ alex@univ.edu   │ Student │ ✅    │ [⚙][🔑]│  │
│  │ Sara Chen │ sara@univ.edu   │ Staff   │ 🔒    │ [⚙][🔓]│  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **User Table**: Paginated, sortable, searchable table with role/status filters.
- **Grouped View**: Users grouped by role with counts (`GET /api/users/grouped`).
- **Create User Form**: Single user creation with role assignment.
- **Bulk Import**: CSV upload for mass user creation (`POST /api/users/bulk` with multipart file upload, max 5MB).
- **User Settings Modal** (`UserManagementSettingsModal.tsx`, 26KB): Role-based access matrix.
- **Account Actions**: Activate, deactivate, unlock, reset password.

### Users API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/users` | List users (paginated, filtered) |
| GET | `/api/users/grouped` | Users grouped by role |
| GET | `/api/users/:id` | Get single user |
| POST | `/api/users` | Create user |
| PATCH | `/api/users/:id` | Update user |
| POST | `/api/users/bulk` | Bulk import from CSV |
| POST | `/api/users/:id/reset-password` | Admin password reset |
| PATCH | `/api/users/:id/activate` | Activate user |
| PATCH | `/api/users/:id/unlock` | Unlock locked account |
| DELETE | `/api/users/:id` | Deactivate user |

### Multi-Role Assignment System
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/users/:id/roles` | Get role assignments |
| PUT | `/api/users/:id/roles` | Set role assignments (with per-role scope/institute) |
| GET | `/api/users/:id/derived-department` | Get derived department from assignments |

---

## 2. Roles Module (`roles.controller.ts`)

### Screen Purpose
Custom role definition and permission management. Roles define what actions users can perform across modules.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/roles` | List all roles |
| POST | `/api/roles` | Create custom role |
| PATCH | `/api/roles/:id` | Update role permissions |
| DELETE | `/api/roles/:id` | Delete role |

---

## 3. Profile Governance Module (`GovernedProfileSection.tsx`)

### Screen Purpose
Maker-checker pipeline for sensitive profile field changes. When Profile Governance is enabled, changes to governed fields (e.g., name, date of birth, photograph) require approval before taking effect.

### Component Specs
- **GovernedProfileSection** (18KB): UI section that renders governed fields with pending-change indicators.
- **Submit Change Request**: Users submit proposed changes for review.
- **Approval Inbox**: Administrators review, approve, or reject profile change requests.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/profile-governance/submit` | Submit profile change request |
| GET | `/api/profile-governance/pending` | List pending change requests |
| PATCH | `/api/profile-governance/:id/approve` | Approve change |
| PATCH | `/api/profile-governance/:id/reject` | Reject change |

---

## 4. Batch Setup Wizard (`BatchSetupWizard.tsx` & `BatchSetupList.tsx`)

### Screen Purpose
Guided multi-step wizard (39KB) for creating complete batch structures. Walks administrators through:
1. Select Programme & Academic Year
2. Define Terms (semesters/trimesters)
3. Create Sections per term
4. Assign Subjects to each term
5. Configure Stream Label binding
6. Review & Confirm

### Component Specs
- **Wizard Steps**: Progress indicator with back/next navigation.
- **BatchSetupList** (9KB): List view of existing batch configurations.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/batch-setup` | List batch setups |
| POST | `/api/batch-setup` | Create batch setup |
| PATCH | `/api/batch-setup/:id` | Update setup |

---

## 5. Parent Portal Module (`parent-portal.controller.ts`)

### Screen Purpose
Read-only portal for parents to view their ward's academic progress, attendance, fees, and notifications.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/parent-portal/ward` | Get linked student info |
| GET | `/api/parent-portal/attendance` | Ward attendance |
| GET | `/api/parent-portal/fees` | Ward fee status |
| GET | `/api/parent-portal/results` | Ward exam results |

---

## 6. Branding Module (`branding.controller.ts`)

### Screen Purpose
University branding configuration — logo uploads, color scheme selection, cover images, and portal appearance customization. Integrated into Settings page.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/branding` | Get branding config |
| PATCH | `/api/branding` | Update branding |
| POST | `/api/branding/upload` | Upload branding asset |

---

## 7. ID Format Management (`IdFormatsPage.tsx`)

### Screen Purpose
Configure auto-generated ID patterns (16KB) for:
- Student enrollment numbers (e.g., `CS2024001`)
- Roll numbers
- Application IDs
- Staff employee codes
- Document serial numbers

### Component Specs
- **Format Template Editor**: Pattern builder with placeholders — `{DEPT}`, `{YEAR}`, `{SEQ:3}`, `{BATCH}`.
- **Preview**: Live preview of generated ID from template.
- **Sequence Management**: View/reset counters.

### Backend Services
- **`id-format.service.ts`**: Template CRUD, pattern validation.
- **`id-generator.service.ts`**: Runtime generation — resolves placeholders, increments sequences, ensures uniqueness.
