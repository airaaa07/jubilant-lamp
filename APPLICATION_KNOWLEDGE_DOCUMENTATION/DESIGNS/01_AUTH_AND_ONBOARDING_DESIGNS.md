# UI Design Specs: Authentication & Onboarding Screens

## Pages Covered
- `LoginPage.tsx`
- `RegisterPage.tsx`
- `ForgotPasswordPage.tsx`
- `ResetPasswordPage.tsx`
- `SetupAccountPage.tsx`
- `OnboardStudentsPage.tsx`
- `BannersPage.tsx`

---

## 1. Login Page (`LoginPage.tsx`)

### Screen Purpose
The gateway for all system users (Students, Staff, Admins). Handles credentials entry, password visibility toggle, tenant branding background image, and redirection based on user role. Supports maintenance-mode awareness (users blocked during maintenance see an overlay banner).

### Visual Wireframe & Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                      Cover Branding Image                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                [ University Logo ]                    │  │
│  │               Welcome to UniversityERP                │  │
│  │                                                       │  │
│  │ Email Address:   [ admin@university.edu             ] │  │
│  │ Password:        [ •••••••••••••••••               ] │  │
│  │                                                       │  │
│  │ [✓] Remember Me             [ Forgot Password? ]      │  │
│  │                                                       │  │
│  │                 [ SIGN IN TO PORTAL ]                 │  │
│  │                                                       │  │
│  │ Don't have an account? [ Register Now ]               │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Background Banner Container**: Full-screen relative container displaying the university cover image (`coverPath`) with a dark radial overlay gradient (`from-slate-950/90 to-slate-900/95`).
- **Glassmorphism Modal Card**: Centered elevated panel (`max-w-md w-full p-8 rounded-2xl bg-slate-900/80 backdrop-blur-xl border border-slate-800 shadow-2xl`).
- **Logo & Header**: University logo (`logoPath`) centered above dynamic welcome text.
- **Input Fields**: Floating label text inputs with icon prefixes (`Mail`, `Lock`), password visibility toggle button (`Eye` / `EyeOff` icons).
- **Submit Button**: Gradient primary button (`bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-medium py-3 rounded-xl transition-all shadow-lg shadow-indigo-500/20`).
- **Rate-Limited Login**: Backend enforces `ThrottlerGuard` at 5 attempts/minute. Frontend shows error toast on 429.
- **Account Lockout Display**: When account is locked (after exceeding `maxAttempts`), the error message either shows a countdown or "Contact administrator to unlock" depending on `lockMinutes` setting.
- **Must-Change-Password Redirect**: If `user.mustChangePassword` is true after login, user is redirected to `SetupAccountPage.tsx` instead of Dashboard.

### API Endpoints Used
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/auth/login` | Authenticate with email + password |
| POST | `/api/auth/refresh` | Refresh access token using refresh token |
| POST | `/api/auth/logout` | Logout and delete all refresh tokens |
| GET | `/api/auth/me` | Get current user profile |

---

## 2. Registration Page (`RegisterPage.tsx`)

### Screen Purpose
Enables new applicants to register accounts with multi-step dual-channel OTP verification (mobile SMS + email), anti-bot captcha, and academic programme selection. Dynamically adapts based on `GET /api/auth/public/registration-config` which reports whether email OTP, mobile OTP, or both are required.

### Layout & Component Specs
- **Step Indicator Pipeline**: Multi-step progress wizard:
  - Step 1: Basic Profile — Name, Email, Phone, Password creation with real-time strength indicator
  - Step 2: Anti-Bot Captcha — SVG distorted-text captcha (`GET /api/auth/captcha`), 6-digit numeric answer
  - Step 3: Mobile OTP Verification (if SMS enabled) — 6 separate digit input boxes with auto-focus, resend timer (60s cooldown)
  - Step 4: Email OTP Verification (if email enabled) — Same 6-digit input pattern for email code
  - Step 5: Academic Programme Selection — Cascading selects: Institute → Department → Programme → Course → Batch → Stream Label
- **Role Selector Cards**: Selectable radio cards for role type (student, teaching_staff, non_teaching_staff, general_staff) with indigo ring highlight when active (`ring-2 ring-indigo-500 bg-indigo-950/30`).
- **Password Policy Display**: Real-time composition checklist sourced from `GET /api/auth/public/password-policy`:
  - Minimum length, uppercase, lowercase, digit, special character requirements
  - Dictionary word rejection, username/email similarity check
  - Visual strength meter (Red → Yellow → Green)
- **Captcha Widget**: Inline SVG captcha image + text input, refresh button to fetch new captcha
- **OTP Verification Boxes**: 6 separate digit input boxes with auto-focus movement, timer countdown (60s resend cooldown), attempt counter (max 5 attempts)
- **Programme Selection Cascade**: Dynamic dropdowns populated from public API endpoints:
  - `GET /api/auth/public/institutes` → `GET /api/auth/public/departments?instituteId=` → `GET /api/auth/public/programmes?departmentId=` → `GET /api/auth/public/courses?programmeId=` → `GET /api/auth/public/batches?courseId=` → `GET /api/auth/public/streams?programmeId=`
- **Fee Preview Card**: After programme selection, shows stream label fee detail and application fee via `GET /api/auth/public/stream-label-fee` and `GET /api/auth/public/application-fee`
- **Scholarship Display**: Lists available scholarships from `GET /api/auth/public/scholarships`

### API Endpoints Used
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/auth/public/registration-config` | Which OTP channels are required |
| GET | `/api/auth/public/password-policy` | Password composition rules |
| GET | `/api/auth/captcha` | Generate SVG captcha + signed token |
| POST | `/api/auth/register` | Submit registration (with captcha token + phone/email verify tokens) |
| POST | `/api/auth/register/send-otp` | Send SMS OTP (3 req/min rate limit) |
| POST | `/api/auth/register/verify-otp` | Verify SMS OTP → returns phoneVerifyToken |
| POST | `/api/auth/register/send-email-otp` | Send email OTP (3 req/min rate limit) |
| POST | `/api/auth/register/verify-email-otp` | Verify email OTP → returns emailVerifyToken |
| GET | `/api/auth/public/institutes` | List institutes for selection |
| GET | `/api/auth/public/departments` | List departments filtered by institute |
| GET | `/api/auth/public/programmes` | List programmes filtered by department |
| GET | `/api/auth/public/courses` | List courses filtered by programme |
| GET | `/api/auth/public/batches` | List batches filtered by course |
| GET | `/api/auth/public/streams` | List streams filtered by programme |
| GET | `/api/auth/public/course-types` | Available course type categories |
| GET | `/api/auth/public/stream-label-fee` | Fee preview for selected stream |
| GET | `/api/auth/public/application-fee` | Application fee amount for batch |
| GET | `/api/auth/public/scholarships` | Available scholarship schemes |
| GET | `/api/auth/public/stream-label-detail` | Detailed curriculum preview |

---

## 3. Forgot Password Page (`ForgotPasswordPage.tsx`)

### Screen Purpose
Allows users to request a password reset. Supports dual-channel recovery: email link (default) and SMS OTP (when SMS integration is enabled).

### Layout & Component Specs
- **Channel Toggle**: Tab toggle between "Reset via Email Link" and "Reset via SMS OTP"
- **Email Reset Flow**: Single email input → submits to `POST /api/auth/forgot-password` → displays generic success message (anti-enumeration)
- **SMS Reset Flow**: Identifier input (email or phone) → sends OTP via `POST /api/auth/forgot-password/sms` → OTP entry → new password entry → submits to `POST /api/auth/reset-password/sms`
- **Generic Response**: Always shows "If that email/account is registered, a reset link/code has been sent" to prevent user enumeration

---

## 4. Reset Password Page (`ResetPasswordPage.tsx`)

### Screen Purpose
Handles the email-link password reset flow. User arrives via link containing a token parameter (`/reset-password?token=xxx`). Token is a hex-encoded random value, hashed with SHA-256 and stored in the database with a 1-hour expiry.

### Layout & Component Specs
- **New Password Input**: Password field with visibility toggle and real-time policy validation checklist (sourced from password policy)
- **Confirm Password Input**: Must-match validation
- **Password History Enforcement**: Backend rejects passwords that match any of the last N historical passwords (configurable via `historyCount`)
- **Submit Action**: `POST /api/auth/reset-password { token, newPassword }` → redirects to Login on success

---

## 5. Account Setup Page (`SetupAccountPage.tsx`)

### Screen Purpose
Forced initial password change screen for accounts created by administrators, batch imported users, or users whose password has expired (policy-driven). Also surfaces after production promotion when the seed SuperAdmin credential is revoked. Enforces password composition and history policies.

### Layout & Component Specs
- **Password Strength Indicator Bar**: 4-segment dynamic progress bar color-coded by entropy (Red = Weak, Yellow = Moderate, Green = Strong).
- **Policy Validation Checklist**: Real-time bullet list with green checkmark / red cross icons:
  - Minimum length (configurable)
  - Contains upper & lower case letters
  - Contains number & special symbol
  - No dictionary words (when `rejectDictionary` enabled)
  - Must not match email/username (when `rejectUsername` enabled)
  - Must not match previous N passwords (when `historyCount > 0`)
- **API Endpoint**: `POST /api/auth/change-password { currentPassword, newPassword }` — clears `mustChangePassword` flag on success

---

## 6. Student Onboarding Page (`OnboardStudentsPage.tsx`)

### Screen Purpose
Admin screen for managing post-admission student onboarding. Displays applicants who have accepted admission offers and need document verification, student ID generation, and profile completion before being fully enrolled.

### Layout & Component Specs
- **Onboarding Progress Table**: Data table displaying candidate name, application number, program, onboarding step completion badges, and action buttons (`Verify Documents`, `Generate Student ID`).
- **Registration Review Panel**: Admin can review pending registrations (`GET /api/auth/registrations`), approve/reject with notes (`PATCH /api/auth/registrations/:id/review`), and make admission offers (`PATCH /api/auth/registrations/:id/offer`).
- **Self-Select Programme**: Applicants can update their programme choice post-registration via `PATCH /api/auth/registrations/self-select`.
- **Admission Status Tracker**: Applicant-facing card showing registration status, fees paid, hostel/transport allocation via `GET /api/auth/registrations/my-status`.

---

## 7. Banner Management Page (`BannersPage.tsx`)

### Screen Purpose
Admin interface for managing promotional banners displayed on the login page and dashboard. Controls banner images, display scheduling, and ordering.

### Layout & Component Specs
- **Banner List**: Card grid displaying current banners with preview thumbnails
- **Banner Upload Form**: Image upload, display title, link URL, scheduling dates, and display order
- **API Module**: `banners` controller with CRUD endpoints (`GET/POST/PATCH/DELETE /api/banners`)

---

## 8. Profile Self-Service (Embedded in `PATCH /api/auth/me`)

### Screen Purpose
Authenticated users can update their own profile information (name, phone, photograph, address, social links, about bio, interests). Fields governed by Profile Governance are excluded from self-edit and must go through the maker-checker pipeline.

### Editable Fields
- `salutation`, `firstName`, `lastName`, `middleName`, `fatherName`, `motherName`
- `phone`, `gender`, `dateOfBirth`
- `currentAddress`, `permanentAddress`
- `photograph` (upload)
- `socialLinks` (platform + URL + label array)
- `about` (bio text, sanitized)
- `interests` (string array, sanitized)

### Change Email / Mobile Flow
- **Email Change**: Two-step verified flow — `POST /api/auth/change-email/request { newEmail }` → sends verification code → `POST /api/auth/change-email/confirm { newEmail, code }` → swaps email
- **Mobile Change**: Two-step verified flow — `POST /api/auth/change-mobile/request { newPhone }` → sends OTP → `POST /api/auth/change-mobile/confirm { newPhone, code }` → swaps phone

---

## 9. SuperAdmin Features

### Impersonation System
- **Purpose**: SuperAdmin can log in as any other user to diagnose issues or verify workflows
- **Entry**: `POST /api/auth/impersonate/:userId` → returns access token scoped to target user with `impersonatedBy` marker
- **Exit**: `POST /api/auth/impersonate-exit` → logs the session end
- **Restrictions**: Cannot impersonate self, cannot impersonate another SuperAdmin, cannot nest impersonation sessions
- **Audit Trail**: Both start and end events logged to `audit_logs` with IP address

### Production Promotion
- **Purpose**: Commissioning a new installation — rotates JWT secret (VM only), revokes seed SuperAdmin credential, enables production mode flag
- **Endpoint**: `POST /api/auth/promote-to-production`
- **Prerequisites**: Email (SMTP) integration must be enabled (seed recovery requires email reset link)
- **Status Check**: `GET /api/auth/production-status` — returns `promoted`, `promotedAt`, `emailEnabled`
- **Post-Promotion**: Sends System Status email snapshot to admin email, triggers PM2 reload on VM deployments
