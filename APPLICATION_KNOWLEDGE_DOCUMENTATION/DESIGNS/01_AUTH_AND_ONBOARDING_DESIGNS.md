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
The gateway for all system users (Students, Staff, Admins). Handles credentials entry, password visibility toggle, tenant branding background image, and redirection based on user role.

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

---

## 2. Registration Page (`RegisterPage.tsx`)

### Screen Purpose
Enables new applicants or staff members to register accounts with multi-step OTP email/mobile verification.

### Layout & Component Specs
- **Step Indicator Pipeline**: Top 3-step progress wizard:
  - Step 1: Basic Profile & Account Role selection
  - Step 2: 6-Digit OTP Verification
  - Step 3: Password Creation & Confirmation
- **Role Selector Cards**: Selectable radio cards for role type (Applicant / Student / Faculty) with indigo ring highlight when active (`ring-2 ring-indigo-500 bg-indigo-950/30`).
- **OTP Verification Box**: 6 separate digit input boxes with auto-focus movement, timer countdown display (e.g. `Resend OTP in 00:59`), and status badge.

---

## 3. Account Setup Page (`SetupAccountPage.tsx`)

### Screen Purpose
Forced initial password change screen for accounts created by administrators or batch imported. Enforces password history and complexity policies.

### Layout & Component Specs
- **Password Strength Indicator Bar**: 4-segment dynamic progress bar color-coded by entropy (Red = Weak, Yellow = Moderate, Green = Strong).
- **Policy Validation Checklist**: Real-time bullet list with green checkmark / red cross icons:
  - Minimum 8 characters
  - Contains upper & lower case letters
  - Contains number & special symbol (`@#$%^&*`)
  - Must not match previous 3 passwords

---

## 4. Student Onboarding Page (`OnboardStudentsPage.tsx`)

### Screen Purpose
Admin screen for managing post-admission student onboarding, document verification checklist, and initial profile generation.

### Layout & Component Specs
- **Onboarding Progress Table**: Data table displaying candidate name, application number, program, onboarding step completion badges, and action buttons (`Verify Documents`, `Generate Student ID`).
