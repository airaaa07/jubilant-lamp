# Incomplete, Missing & System Limitation Audit

## Purpose
This document provides a transparent, zero-assumption audit of system areas that are partially implemented, stubbed out, or architecturally consolidated. Grounded strictly in empirical codebase inspection, this report establishes what is production-ready versus what remains work-in-progress.

---

## Codebase Audit Summary

| Component / Feature Area | Declared Architecture | Empirical Codebase Finding | Operational Impact | Recommended Path Forward |
| :--- | :--- | :--- | :--- | :--- |
| **Student Portal Frontend** | `web/student-portal` | Package exists, but `src/pages` is an empty directory. | All student workflows (exam taking, fee payment, registration) run inside `web/admin-portal`. | Maintain single SPA or extract student routes to `web/student-portal`. |
| **CBE Microservice Engine** | `apps/cbe-engine` | Basic NestJS scaffolding stub (`ConfigModule` only). | All CBE exam logic, proctoring, and question paper generation are served by `core-api/src/modules/examination`. | Keep in `core-api` or complete microservice extraction. |
| **Certificate Generator Service** | `apps/cert-generator` | Basic NestJS scaffolding stub (`ConfigModule` only). | PDF generation is executed inside `core-api/src/modules/documents` using Handlebars and PDFKit. | Keep in `core-api` or complete microservice extraction. |
| **Notification Worker Service** | `apps/notification-worker` | Basic NestJS scaffolding stub (`ConfigModule` only). | Notifications are dispatched inside `core-api/src/modules/notifications` via Redis/Bull queues. | Keep in `core-api` or complete microservice extraction. |
| **Shared Libraries** | `libs/` | Folder exists, but contains no packages or code. | Code models and types are managed locally within `apps/core-api` and `web/admin-portal`. | Populate `libs/` with shared TypeScript interfaces. |
| **Parent Portal App** | Dedicated Parent Mobile/Web App | Backend endpoints exist (`ParentPortalModule`), but UI is served via `StudentProfilePage.tsx`. | Parents view ward data through `admin-portal` using assigned parent roles. | Build dedicated parent dashboard or mobile client. |

---

## Detailed System Findings

### 1. Monolithic Realization vs Microservice Intent
The project repository contains multiple application folders under `apps/` (`cbe-engine`, `cert-generator`, `notification-worker`). Inspection of `main.ts` and `app.module.ts` in those subdirectories confirms they contain minimal NestJS boilerplate without domain controllers or services. 

All domain features—including online examination proctoring, PDF compilation, and notification queues—are fully implemented and operational inside **`apps/core-api`**.

> **Takeaway**: The system is an operational **modular monolith**. The extra folders represent future microservice targets.

### 2. Single Frontend Portal Architecture
The repository structure suggests a split between `web/admin-portal` and `web/student-portal`. However, `web/student-portal/src/pages` is currently empty. 

All 45 frontend pages—handling administrative setup, faculty grading, librarian cataloging, accountant ledger management, as well as **student exam taking (`ExamTakePage.tsx`)** and **student fee payment (`FeesPage.tsx`)**—are contained inside `web/admin-portal`.

> **Takeaway**: System access is unified under `web/admin-portal`. Navigation and page routes are rendered dynamically based on the user's active role.

### 3. Verification & Automated Test Coverage
While core API contracts and Prisma migrations are strictly defined, automated test suites (Jest unit tests or Cypress/Playwright E2E tests) are sparse across backend modules. Reliability currently relies on NestJS compile-time type safety, Prisma schema validation, and manual verification pipelines.

---

## Known Workarounds & Architectural Guidelines

1. **Deployment Simplicity**: Deploying `apps/core-api` and `web/admin-portal` is sufficient to run 100% of implemented system capabilities.
2. **Role-Based Access Control**: Ensure `ModuleAccess` and `Role` configurations are properly seeded to ensure students only see student-relevant pages inside `admin-portal`.
