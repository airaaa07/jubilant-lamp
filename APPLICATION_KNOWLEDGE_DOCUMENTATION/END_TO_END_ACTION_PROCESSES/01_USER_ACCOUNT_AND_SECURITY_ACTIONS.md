# Action Lifecycle Manual: User Accounts, Auth & Security

## Action 1.1: User Self-Registration & OTP Verification

### 1. User Action & Frontend Trigger
- **User Role**: Applicant / Public Guest
- **Screen**: `RegisterPage.tsx`
- **User Input**: Email (`john.doe@example.com`), Password (`SecurePass@123`), First Name (`John`), Last Name (`Doe`), Mobile Number (`+1234567890`), Target Institute ID.
- **Trigger**: Click **Register Account** button.

### 2. Frontend State & Payload Construction
- Form validation verifies password complexity regex (`/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/`).
- Sends HTTP POST request:
  ```json
  {
    "email": "john.doe@example.com",
    "password": "SecurePass@123",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+1234567890",
    "instituteId": "inst-123-uuid",
    "role": "Applicant"
  }
  ```

### 3. API Routing & Guard Pipeline
- **URL**: `POST /api/v1/auth/register`
- **Guards**: `ThrottlerGuard` (Max 5 attempts / minute), `GlobalJwtAuthGuard` (Bypassed via `@Public()`).

### 4. Backend Service Logic (`AuthService.register`)
- Hashes password using Bcrypt (`saltRounds = 10`).
- Generates 6-digit cryptographic numeric OTP (e.g. `482910`).
- Dispatches async email/SMS via `NotificationsService`.

### 5. Database Transactions & Persistence
- `INSERT INTO users (id, email, password_hash, first_name, last_name, phone, role = 'Applicant', is_active = false)`
- `INSERT INTO mobile_otps (user_id, otp_code, expires_at = NOW() + 10 min, retries_left = 3)`
- `INSERT INTO registration_requests (user_id, status = 'PENDING_OTP')`

### 6. Verification & Final State Outcome
- User enters `482910` on `RegisterPage.tsx` OTP screen.
- `POST /api/v1/auth/verify-otp { userId, otpCode }`.
- `UPDATE users SET is_active = true WHERE id = :id`.
- `UPDATE registration_requests SET status = 'VERIFIED'`.
- Account is activated; user redirected to `LoginPage.tsx`.

---

## Action 1.2: User Login & Session Authentication

### 1. User Action & Frontend Trigger
- **User Role**: Any (Student, Staff, Admin)
- **Screen**: `LoginPage.tsx`
- **User Input**: Email & Password.
- **Trigger**: Click **Sign In to Portal** button.

### 2. Frontend State & Payload
- `POST /api/v1/auth/login { email, password }`.

### 3. API Routing & Guard Pipeline
- `ThrottlerGuard` enforces strict rate limit (5 attempts/min). `@Public()` allowed.

### 4. Backend Service Logic (`AuthService.login`)
- Verifies Bcrypt hash against `user.passwordHash`.
- Checks `user.isActive` and `user.lockedUntil`.
- Generates JWT Access Token (Payload: `sub`, `email`, `roles`, `universityId`, `instituteId`, `departmentId`; Expiry: 15 min).
- Generates Refresh Token (Expiry: 7 days).

### 5. Database & Cache Mutations
- `UPDATE users SET failed_login_attempts = 0, last_login_at = NOW() WHERE id = :id`.
- `SETEX redis:refresh_token:<userId> 604800 <refreshTokenHash>`.
- `PrismaService` records login event in `audit_logs`.

### 6. Outcome
- Returns `{ accessToken, refreshToken, user: { id, name, roles, permissions } }`.
- Frontend stores tokens, hydrates Zustand/TanStack query state, redirects to `DashboardPage.tsx`.
