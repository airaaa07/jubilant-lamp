# UniversityERP - Single Source of Truth Documentation Repository

Welcome to the official, complete knowledge repository for **UniversityERP**. This documentation suite has been engineered directly from a comprehensive reverse-engineering audit of the codebase to provide an exhaustive, zero-assumption single source of truth for the entire product.

---

## Documentation Navigation Hub

This repository is organized into **8 core knowledge documents**, each addressing a specific domain of the application:

```
APPLICATION_KNOWLEDGE_DOCUMENTATION/
├── README.md                                    # Master Navigation & Repository Map (This Document)
├── 00_APPLICATION_OVERVIEW.md                   # High-Level Product Purpose, System Architecture & Principles
├── 01_BUSINESS_PROCESSES.md                     # Step-by-Step Real-World End-to-End Workflows (12 Processes)
├── 02_USER_JOURNEYS.md                          # Role-Based Experiences & Journeys for 12 User Roles
├── 03_DATA_FLOW_AND_LIFECYCLE.md                # Data Lifecycles, Origin, Mutations, and Transformations
├── 04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md # Technical Infrastructure, Security Guards, Crons & Microservices
├── 05_MODULE_BY_MODULE_DIRECTORY.md             # Detailed Guide for all 38 NestJS Modules in Core API
├── 06_API_AND_DATABASE_REFERENCE.md             # 100+ Database Tables, Schema Models, Enums & REST API Rules
├── 07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md # Audit of Incomplete Flows, Stubs & System Limitations
├── 08_UI_UX_DESIGN_SYSTEM_AND_SCREEN_CATALOG.md # Master UI/UX Design System Tokens & Visual Screen Wireframes
├── 09_END_TO_END_WORKFLOW_ARCHITECTURE_CATALOG.md # Master End-to-End Technical Workflow Architecture Catalog
├── DESIGNS/                                     # 8 Separated Domain Screen Design Specification Files
└── WORKFLOW_ARCHITECTURE_DESIGNS/               # 8 Separated Technical Workflow Architecture Design Files
```

---

## Quick Reference by Stakeholder Role

| Role | Recommended Starting Point | Key Insights Gained |
| :--- | :--- | :--- |
| **Product Manager / Business Analyst** | [`00_APPLICATION_OVERVIEW.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/00_APPLICATION_OVERVIEW.md) & [`01_BUSINESS_PROCESSES.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/01_BUSINESS_PROCESSES.md) | High-level business domains, fee billing workflows, admission pipelines, and examination rules. |
| **QA & Test Engineers** | [`01_BUSINESS_PROCESSES.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/01_BUSINESS_PROCESSES.md) & [`02_USER_JOURNEYS.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/02_USER_JOURNEYS.md) | Exact step-by-step user actions, screen transitions, expected database state changes, and edge cases. |
| **Software Engineers & Architects** | [`04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md) & [`05_MODULE_BY_MODULE_DIRECTORY.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/05_MODULE_BY_MODULE_DIRECTORY.md) | NestJS guard execution pipelines, Prisma middleware diffing, Redis/Bull queue wiring, and module breakdowns. |
| **Database Administrators (DBAs)** | [`03_DATA_FLOW_AND_LIFECYCLE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/03_DATA_FLOW_AND_LIFECYCLE.md) & [`06_API_AND_DATABASE_REFERENCE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/06_API_AND_DATABASE_REFERENCE.md) | 100+ Prisma models, foreign key dependencies, field-level audit log structures, and transactional flows. |
| **DevOps & Infrastructure Leads** | [`04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/04_SYSTEM_ARCHITECTURE_AND_INFRASTRUCTURE.md) & [`07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md`](file:///home/admin/UniversityERP/APPLICATION_KNOWLEDGE_DOCUMENTATION/07_INCOMPLETE_MISSING_AND_LIMITATION_AUDIT.md) | Service deployment realities (`core-api` monolith vs microservices stubs), MinIO storage, and background crons. |

---

## Default System Credentials & Setup Quick Start

- **Default University**: SlashCurate University (`slashcurate.edu`)
- **SuperAdmin Email**: `erpsupport@slashcurate.com`
- **Default Password**: `Admin@1234` (requires mandatory password change upon initial login)
- **Primary Backend API**: `http://localhost:3000/api/v1`
- **Admin Portal UI**: `http://localhost:5173`
- **Swagger Documentation**: `http://localhost:3000/api/docs` (Non-production environments)

---

## Key System Highlights

1. **Versioned Academic Rules**: Student enrollments are tied to immutable `StreamLabel` snapshots so curriculum updates never invalidate ongoing student batches.
2. **Generic Approval Workflows**: Visual workflow builder supporting multi-actor routing, Razorpay payment holds, and resource reservations using the Saga pattern.
3. **Computer-Based Examination (CBE)**: Full online examination platform featuring AI webcam proctoring, tab-switch monitoring, screen locking, and post-exam question challenge processing.
4. **Daily Recurring Billing**: Automated 2:00 AM cron generating head-wise fee demands per term for all active student enrollments.
