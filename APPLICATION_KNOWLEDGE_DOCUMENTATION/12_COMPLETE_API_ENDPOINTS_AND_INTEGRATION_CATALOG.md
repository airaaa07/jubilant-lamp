# Complete API Endpoints & Integration Catalog

## Overview
This document provides an exhaustive inventory of all REST API endpoints implemented across the **38 backend modules** in `apps/core-api`. Every route is documented with its HTTP method, URL pattern, authentication requirement, guard pipeline, request body DTO, and response contract.

---

## 🔒 Global API Conventions & Auth Headers

### Request Headers
```http
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
x-tenant-id: <university_uuid>
x-institute-id: <institute_uuid>
```

---

## 1. Auth & User Management APIs (`AuthModule` & `UsersModule`)

| Method | Endpoint Route | Access / Guard | Description | Request DTO / Params | Response Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | `@Public()` | Registers a new user account & triggers OTP. | `RegisterDto` (email, password, phone, role) | `{ userId, status: "PENDING_OTP" }` |
| `POST` | `/api/v1/auth/verify-otp` | `@Public()` | Verifies 6-digit OTP & activates account. | `VerifyOtpDto` (userId, otpCode) | `{ success: true, message: "Account activated" }` |
| `POST` | `/api/v1/auth/login` | `@Public()` (5 req/min) | Authenticates credentials & issues JWT. | `LoginDto` (email, password) | `{ accessToken, refreshToken, user }` |
| `POST` | `/api/v1/auth/refresh` | `@Public()` | Refreshes expired access token using refresh token. | `RefreshTokenDto` (refreshToken) | `{ accessToken, refreshToken }` |
| `POST` | `/api/v1/auth/setup-account` | `Bearer JWT` | Initial account password change for imported users. | `SetupAccountDto` (newPassword) | `{ success: true }` |
| `GET` | `/api/v1/users/me` | `Bearer JWT` | Returns active user profile, roles, and scope boundaries. | None | `UserProfileDto` |
| `GET` | `/api/v1/users` | `Bearer JWT` (`InstAdmin`) | Lists users filtered by institute/department. | Query: `page`, `limit`, `role`, `search` | `{ data: User[], total, page }` |

---

## 2. Academic & Rules APIs (`AcademicModule`)

| Method | Endpoint Route | Access / Guard | Description | Request DTO / Params | Response Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/academic/programs` | `Bearer JWT` | Lists academic degree/diploma programs. | Query: `instituteId` | `Program[]` |
| `POST` | `/api/v1/academic/programs` | `Bearer JWT` (`UnivAdmin`) | Creates a new academic program. | `CreateProgramDto` (name, code, duration) | `Program` |
| `POST` | `/api/v1/academic/stream-labels` | `Bearer JWT` (`UnivAdmin`) | Creates immutable versioned rule snapshot. | `CreateStreamLabelDto` (credits, rules) | `StreamLabel` |
| `GET` | `/api/v1/academic/batches` | `Bearer JWT` | Lists academic cohorts/batches. | Query: `programId` | `Batch[]` |
| `POST` | `/api/v1/academic/electives/select` | `Bearer JWT` (`Student`) | Submits student elective subject choice. | `SelectElectiveDto` (poolId, subjectId) | `{ success: true }` |

---

## 3. Admissions APIs (`AdmissionsModule`)

| Method | Endpoint Route | Access / Guard | Description | Request DTO / Params | Response Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/admissions/applications` | `Bearer JWT` (`Applicant`) | Submits dynamic admission form. | `SubmitApplicationDto` (templateId, answers) | `FormSubmission` |
| `GET` | `/api/v1/admissions/applications` | `Bearer JWT` (`InstAdmin`) | Lists candidate applications for review. | Query: `status`, `programId` | `FormSubmission[]` |
| `POST` | `/api/v1/admissions/applications/:id/verify` | `Bearer JWT` (`InstAdmin`) | Officer verifies marksheets & approves. | `VerifyApplicationDto` (status, notes) | `FormSubmission` |
| `POST` | `/api/v1/admissions/merit-list/generate` | `Bearer JWT` (`HOD`) | Runs algorithmic merit ranking. | `GenerateMeritDto` (programId, cutoff) | `MeritList` |

---

## 4. Fee & Payment APIs (`FeeModule`)

| Method | Endpoint Route | Access / Guard | Description | Request DTO / Params | Response Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/fee/demands/my-demands` | `Bearer JWT` (`Student`) | Lists outstanding fee demands for student. | None | `FeeDemand[]` |
| `POST` | `/api/v1/fee/demands/:id/pay` | `Bearer JWT` (`Student`) | Initiates Razorpay checkout order. | None | `{ razorpayOrderId, amount, key }` |
| `POST` | `/api/v1/fee/webhooks/razorpay` | `@Public()` (HMAC) | Webhook callback settling payment & ledger. | Razorpay Webhook Payload | `{ status: "ok" }` |
| `GET` | `/api/v1/fee/ledger` | `Bearer JWT` (`Accountant`) | Returns double-entry transaction history. | Query: `userId`, `fromDate`, `toDate` | `FeeLedger[]` |

---

## 5. Examination & CBE APIs (`ExaminationModule`)

| Method | Endpoint Route | Access / Guard | Description | Request DTO / Params | Response Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/examination/cbe/start-attempt` | `Bearer JWT` (`Student`) | Starts proctored online exam session. | `StartAttemptDto` (examPaperId) | `{ attemptId, questions, duration }` |
| `POST` | `/api/v1/examination/cbe/save-answer` | `Bearer JWT` (`Student`) | Auto-saves answer choice during exam. | `SaveAnswerDto` (questionId, optionId) | `{ saved: true }` |
| `POST` | `/api/v1/examination/cbe/proctor-event` | `Bearer JWT` (`Student`) | Logs tab switch / security warning. | `ProctorEventDto` (eventType, details) | `{ tabSwitches, warningCount }` |
| `GET` | `/api/v1/examination/cbe/live-monitor` | `Bearer JWT` (`Invigilator`)| Live dashboard for monitoring exam room. | Query: `examScheduleId` | `LiveMonitorDto[]` |
| `POST` | `/api/v1/examination/cbe/submit` | `Bearer JWT` (`Student`) | Submits exam paper for auto-grading. | `SubmitExamDto` (attemptId) | `{ score, status: "SUBMITTED" }` |

---

## 6. Workflow Engine APIs (`WorkflowModule`)

| Method | Endpoint Route | Access / Guard | Description | Request DTO / Params | Response Contract |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/workflow/definitions` | `Bearer JWT` (`SuperAdmin`) | Defines graph states, transitions & roles. | `WorkflowDefDto` (name, graphJson) | `WorkflowDefinition` |
| `GET` | `/api/v1/workflow/tasks/my-tasks` | `Bearer JWT` | Fetches pending workflow tasks for user. | None | `WorkflowTask[]` |
| `POST` | `/api/v1/workflow/instances/:id/action` | `Bearer JWT` | Approves / rejects workflow step. | `WorkflowActionDto` (action, comments) | `WorkflowStepInstance` |
