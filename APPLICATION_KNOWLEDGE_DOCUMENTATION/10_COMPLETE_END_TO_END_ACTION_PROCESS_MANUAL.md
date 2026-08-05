# Complete End-to-End Action Process Execution Manual

## Overview
This document serves as the master execution manual for **every single end-to-end user action and system process** in UniversityERP. It traces each action from user button click to frontend state, API payload, NestJS guard pipeline, database transaction, background job dispatch, and final state outcome.

---

## 🏗️ The 6-Stage Action Lifecycle Standard

Every action in this manual is documented across six execution phases:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Action & Frontend Trigger (Button Click / Form Submission)
├─────────────────────────────────────────────────────────────┤
│ 2. Frontend State & Payload Construction (React / TanStack Query)
├─────────────────────────────────────────────────────────────┤
│ 3. API Routing & Guard Pipeline (Throttler / Auth / Maintenance)
├─────────────────────────────────────────────────────────────┤
│ 4. Backend Service Logic & Domain Business Rules (core-api)
├─────────────────────────────────────────────────────────────┤
│ 5. Database Transactions & Persistence (Prisma / PostgreSQL)
├─────────────────────────────────────────────────────────────┤
│ 6. Asynchronous Side Effects & Notifications (Redis / Bull / MinIO)
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Separated End-to-End Action Process Documents

All system actions are categorized into **8 dedicated action lifecycle documents** located in [`APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/):

1. **[`END_TO_END_ACTION_PROCESSES/01_USER_ACCOUNT_AND_SECURITY_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/01_USER_ACCOUNT_AND_SECURITY_ACTIONS.md)**
   - Registration, OTP email/SMS verification, Login, JWT refresh, Forced password setup, Password reset, Role scope assignment.
2. **[`END_TO_END_ACTION_PROCESSES/02_ADMISSION_AND_STUDENT_ONBOARDING_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/02_ADMISSION_AND_STUDENT_ONBOARDING_ACTIONS.md)**
   - Form submission, MinIO document upload, Application fee demand payment, Officer verification, Merit ranking execution, Seat offer acceptance, Student profile generation.
3. **[`END_TO_END_ACTION_PROCESSES/03_ACADEMIC_CATALOG_AND_TIMETABLE_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/03_ACADEMIC_CATALOG_AND_TIMETABLE_ACTIONS.md)**
   - Tenant hierarchy setup, Immutable `StreamLabel` rule snapshot creation, Elective subject choices, Staff-subject section mapping, Timetable constraint solver execution.
4. **[`END_TO_END_ACTION_PROCESSES/04_FEE_BILLING_AND_REVENUE_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/04_FEE_BILLING_AND_REVENUE_ACTIONS.md)**
   - Global fee head & structure creation, Daily 2 AM recurring billing cron execution, Razorpay order checkout & webhook settlement, Deposit refund workflows, Revenue report export.
5. **[`END_TO_END_ACTION_PROCESSES/05_EXAMINATION_CBE_AND_GRADING_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/05_EXAMINATION_CBE_AND_GRADING_ACTIONS.md)**
   - Question bank creation, Exam paper shuffle, Student CBE online exam session navigation, AI proctoring telemetry capture (webcam/tab switch), Auto-grading, SGPA/CGPA result publication, Question challenge submission.
6. **[`END_TO_END_ACTION_PROCESSES/06_WORKFLOW_ENGINE_AND_RESOURCE_HOLD_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/06_WORKFLOW_ENGINE_AND_RESOURCE_HOLD_ACTIONS.md)**
   - Visual workflow graph creation, Multi-actor approval inbox decisions, Saga pattern resource reservation hold creation, Midnight hold release cron execution.
7. **[`END_TO_END_ACTION_PROCESSES/07_INFRASTRUCTURE_AND_FACILITIES_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/07_INFRASTRUCTURE_AND_FACILITIES_ACTIONS.md)**
   - Hostel room bed allocation, Warden gate pass outing approval & QR scan, Transport route bus pass issuance, Library circulation checkout/return & fine billing, Midnight reservation cleanup cron.
8. **[`END_TO_END_ACTION_PROCESSES/08_HR_LEAVE_AND_SYSTEM_MAINTENANCE_ACTIONS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/END_TO_END_ACTION_PROCESSES/08_HR_LEAVE_AND_SYSTEM_MAINTENANCE_ACTIONS.md)**
   - Staff onboarding, Multi-level leave application & manager approval, Counselling session booking & confidential notes, Automated database backup dump, Restore maintenance gate lock.
