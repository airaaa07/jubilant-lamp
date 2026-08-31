# Action Lifecycle Manual: User Management, Roles & Profile Governance

## Action 10.1: User Administration, Multi-Role Assignment & Bulk CSV Import

### 1. User Creation & Scoped Roles
- **Role**: SuperAdmin / UnivAdmin / InstAdmin
- **Screen**: `UserManagementPage.tsx`
- Form: First Name, Last Name, Email, Password, Primary Role, Scoped Roles (e.g. InstAdmin for Engineering, Faculty for Computer Science).
- `POST /api/users` -> creates user and default role assignments.
- Update role assignments with explicit scopes: `PUT /api/users/:id/roles { roles: [{ roleName: "InstAdmin", instituteId: "inst-101" }] }`.

### 2. Bulk User CSV Import
- Admin uploads CSV on `UserManagementPage.tsx` -> `POST /api/users/bulk` (multipart file upload).
- Backend parses CSV, validates duplicate emails, hashes initial passwords, sets `mustChangePassword = true`.
- Creates users in batch database transaction.

### 3. Account Unlocking & Administrative Password Reset
- If account is locked from too many failed attempts: Admin clicks **Unlock** -> `PATCH /api/users/:id/unlock`.
- Admin forced reset: Clicks **Reset Password** -> `POST /api/users/:id/reset-password { newPassword, mustChangePassword: true }`.

---

## Action 10.2: Profile Governance Maker-Checker Pipeline

### 1. Governed Field Change Request
- When Profile Governance is enabled, sensitive fields (Full Name, Date of Birth, National ID, Photograph) cannot be edited directly by users.
- User inputs proposed change on `StudentProfilePage.tsx` / `GovernedProfileSection.tsx`.
- Clicks **Submit Change Request** -> `POST /api/profile-governance/submit { fieldName: 'firstName', proposedValue: 'Alexander', justification: 'Legal name correction', documentProofUrl: 'minio://docs/gazette.pdf' }`.
- System creates pending record in `profile_change_requests`.

### 2. Administrator Review & Approval
- Administrator reviews pending change requests via `GET /api/profile-governance/pending`.
- Inspects uploaded proof document.
- Action:
  - **Approve**: `PATCH /api/profile-governance/:id/approve` -> atomically mutates user profile field in database and logs audit entry.
  - **Reject**: `PATCH /api/profile-governance/:id/reject { reason: 'Insufficient proof' }` -> leaves user profile unchanged, alerts student.
