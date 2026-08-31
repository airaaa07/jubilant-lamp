# Action Lifecycle Manual: User Accounts, Auth & Security

## Action 1.1: Multi-Step Registration with Captcha & Dual-Channel OTP

### 1. User Action & Frontend Trigger
- **User Role**: Applicant / Public Guest
- **Screen**: `RegisterPage.tsx`
- **User Input**: First Name, Last Name, Email, Password, Mobile Phone, Captcha Solution, Target Institute / Department / Programme / Batch / Stream.
- **Trigger**: Clicks **Register Account** button.

### 2. Frontend State & Payload Construction
- Retrieves active registration config via `GET /api/auth/public/registration-config` to check if mobile OTP, email OTP, or both are required.
- Obtains Captcha SVG and token via `GET /api/auth/captcha`.
- Verifies mobile via `POST /api/auth/register/send-otp` -> `POST /api/auth/register/verify-otp` (returns `phoneVerifyToken`).
- Verifies email via `POST /api/auth/register/send-email-otp` -> `POST /api/auth/register/verify-email-otp` (returns `emailVerifyToken`).
- Constructs payload with `phoneVerifyToken`, `emailVerifyToken`, `captchaToken`, and programme details:
  ```json
  {
    "email": "applicant@university.edu",
    "password": "SecurePassword@2026",
    "firstName": "John",
    "lastName": "Doe",
    "phone": "+1234567890",
    "captchaToken": "signed-token-string",
    "captchaSolution": "482910",
    "phoneVerifyToken": "jwt-phone-token",
    "emailVerifyToken": "jwt-email-token",
    "programmeId": "prog-uuid-123",
    "batchId": "batch-uuid-456",
    "streamLabelId": "stream-uuid-789"
  }
  ```

### 3. API Routing & Guard Pipeline
- **Endpoint**: `POST /api/auth/register`
- **Guards**: `ThrottlerGuard` (Sensitive limit: 5/min), `JwtAuthGuard` bypassed via `@Public()`.
- **Validation**: `ZodValidationPipe(RegisterSchema)`.

### 4. Backend Service Logic (`AuthService.register`)
- Validates Captcha signature and solution.
- Validates phone/email verify tokens.
- Checks password against dynamic `PasswordPolicy` (composition, dictionary words, username similarity).
- Hashes password using Bcrypt (`10` salt rounds).
- Creates User, Role Assignment (`Applicant`), and Registration record in database transaction.

### 5. Database Transactions & Persistence (Prisma)
- `prisma.user.create(...)` with hashed password, active status.
- `prisma.userRole.create(...)` assigning applicant role.
- `prisma.registration.create(...)` linking target programme, batch, and status `SUBMITTED`.
- `prisma.auditLog.create(...)` recording user creation.

### 6. Verification & Final State Outcome
- Account created with initial role `Applicant`.
- Frontend redirects user to `LoginPage.tsx` with success alert.

---

## Action 1.2: User Login, Rate Limiting & Session Management

### 1. User Action & Frontend Trigger
- **User Role**: Any (Student, Faculty, Staff, Admin)
- **Screen**: `LoginPage.tsx`
- **User Input**: Email & Password.
- **Trigger**: Click **Sign In to Portal** button.

### 2. Frontend State & Payload
- Sends `POST /api/auth/login`:
  ```json
  {
    "email": "admin@university.edu",
    "password": "AdminPassword@2026"
  }
  ```

### 3. API Routing & Guard Pipeline
- **Endpoint**: `POST /api/auth/login`
- **Guards**: `ThrottlerGuard` (5 req/min), `@Public()`.
- **Validation**: `ZodValidationPipe(LoginSchema)`.

### 4. Backend Service Logic (`AuthService.login`)
- Verifies system maintenance status via `assertMaintenanceAllowed`: if maintenance mode is enabled and user is not `SuperAdmin`, throws `503 Service Unavailable`.
- Queries user record including `passwordHash`, `lockedUntil`, `failedLoginAttempts`, `isActive`.
- If account is locked (`lockedUntil > now()`), calculates remaining time and throws `403 Forbidden`.
- Verifies Bcrypt hash:
  - If mismatch: increments `failedLoginAttempts`. If `failedLoginAttempts >= maxAttempts`, sets `lockedUntil = now() + lockMinutes`.
  - If match: resets `failedLoginAttempts = 0`, updates `lastLoginAt = now()`.
- Generates JWT Access Token (`15m` expiry) and Refresh Token (`7d` expiry).

### 5. Database Mutations
- `prisma.user.update(...)` updating `failedLoginAttempts`, `lastLoginAt`, and `lockedUntil`.
- `prisma.refreshToken.create(...)` persisting active refresh session.
- `prisma.auditLog.create(...)` recording successful login event with client IP and User-Agent.

### 6. Outcome
- Returns `{ accessToken, refreshToken, user: { id, email, firstName, lastName, roles, mustChangePassword } }`.
- If `mustChangePassword === true`, frontend redirects to `SetupAccountPage.tsx`; otherwise redirects to `DashboardPage.tsx`.

---

## Action 1.3: SuperAdmin Impersonation

### 1. Trigger
- **Role**: SuperAdmin only.
- **Trigger**: Clicks "Impersonate" next to any user row on `UserManagementPage.tsx`.

### 2. API & Guards
- `POST /api/auth/impersonate/:userId`
- Guards: `JwtAuthGuard`, `RolesGuard('SuperAdmin')`.
- Prohibits impersonating self or another SuperAdmin.

### 3. Backend Execution (`AuthService.impersonate`)
- Validates target user exists and is active.
- Generates JWT Access Token for target user with special claim `{ impersonatedBy: caller.userId }`.
- Records audit log: `USER_IMPERSONATION_STARTED`.

### 4. Outcome & Exit
- Frontend switches state to target user's context, displaying yellow top banner.
- Clicks "Exit Impersonation" -> `POST /api/auth/impersonate-exit` -> logs `USER_IMPERSONATION_ENDED` -> reverts token to SuperAdmin.
