# University ERP - Project Index

## Documentation Files

This repository has been reverse-engineered and documented in the following files:

1. **00_PROJECT_INDEX.md** (this file) - Navigation index
2. **01_SYSTEM_OVERVIEW.md** - High-level system architecture and purpose
3. **02_REPOSITORY_STRUCTURE.md** - Complete folder structure and organization
4. **03_BACKEND_ARCHITECTURE.md** - NestJS backend modules, controllers, services
5. **04_FRONTEND_ARCHITECTURE.md** - React frontend structure and components
6. **05_DATABASE.md** - Prisma schema, entities, relations, and ER diagram
7. **06_API_REFERENCE.md** - Complete API endpoint documentation
8. **07_FEATURE_FLOWS.md** - Major feature execution flows and sequence diagrams
9. **08_WORKERS_AND_QUEUES.md** - Background workers and Bull queues
10. **09_STORAGE_AND_MINIO.md** - Object storage configuration and usage
11. **10_REDIS.md** - Redis caching and session management
12. **11_ELASTICSEARCH.md** - Search and indexing configuration
13. **12_AUTHENTICATION.md** - JWT authentication, guards, and authorization
14. **13_EMAIL_AND_SMTP.md** - Email sending and SMTP configuration
15. **14_CERTIFICATE_ENGINE.md** - Certificate generation service
16. **15_CONFIGURATION.md** - System configuration and settings
17. **16_ENVIRONMENT_VARIABLES.md** - Complete environment variable reference
18. **17_INFRASTRUCTURE.md** - Docker, deployment, and infrastructure
19. **18_DEPENDENCY_GRAPH.md** - Service dependencies and relationships
20. **19_REQUEST_LIFECYCLES.md** - Request processing and execution flow
21. **20_LEARNING_GUIDE.md** - Developer onboarding roadmap
22. **21_UNKNOWNS_AND_OPEN_QUESTIONS.md** - Unknowns and gaps discovered

## Quick Start

### For New Developers

1. Read **01_SYSTEM_OVERVIEW.md** to understand what this system does
2. Read **02_REPOSITORY_STRUCTURE.md** to understand the codebase layout
3. Read **20_LEARNING_GUIDE.md** for a structured learning path
4. Refer to specific documentation files as needed during development

### For Specific Tasks

- **Modifying authentication**: Read 12_AUTHENTICATION.md
- **Adding API endpoints**: Read 03_BACKEND_ARCHITECTURE.md and 06_API_REFERENCE.md
- **Database changes**: Read 05_DATABASE.md
- **Frontend changes**: Read 04_FRONTEND_ARCHITECTURE.md
- **Background jobs**: Read 08_WORKERS_AND_QUEUES.md
- **Storage operations**: Read 09_STORAGE_AND_MINIO.md
- **Deployment**: Read 17_INFRASTRUCTURE.md

## System Summary

**University ERP** is a comprehensive university management system built with:

- **Backend**: NestJS (TypeScript) with 36 functional modules
- **Frontend**: React 19 with Vite, TailwindCSS, and 41 admin pages
- **Database**: PostgreSQL with Prisma ORM (100+ models)
- **Storage**: MinIO/S3 with Azure Blob fallback
- **Cache**: Redis for sessions and caching
- **Search**: Elasticsearch for search functionality
- **Queues**: Bull for background job processing
- **Real-time**: Socket.IO for exam engine (CBE)
- **Infrastructure**: Docker Compose with 5 infrastructure services

## Key Services

1. **core-api** (port 3000) - Main NestJS API server
2. **cbe-engine** (port 3001) - Computer-Based Examination engine with WebSockets
3. **notification-worker** (port 3002) - Email/SMS notification worker
4. **cert-generator** (port 3003) - Certificate generation with Puppeteer
5. **admin-portal** (port 5173) - React admin interface

## Technology Stack

### Backend
- NestJS 10.x
- Prisma 5.x
- PostgreSQL 16
- Redis 7
- MinIO
- Elasticsearch 8.13
- Bull 4.x (queues)
- Passport JWT
- Nodemailer

### Frontend
- React 19
- Vite 8
- TypeScript 6
- TailwindCSS 3
- React Router 7
- TanStack Query 5
- TipTap 3 (rich text)
- Recharts 3 (charts)

### Infrastructure
- Docker Compose
- PostgreSQL 16 Alpine
- Redis 7 Alpine
- MinIO latest
- Elasticsearch 8.13
- Nginx Alpine

## Module Overview

The system contains 36 NestJS modules covering:

- **Academic**: Attendance, marks, results, examinations, timetable
- **Administration**: Master data, users, roles, settings
- **Student Management**: Admissions, profiles, onboarding
- **Financial**: Fee management, payments, scholarships
- **Infrastructure**: Hostel, transport, library
- **Workflow**: Generic workflow engine for approvals
- **Documents**: Document templates and generation
- **Communication**: Notifications, notices, banners
- **Examinations**: CBE (computer-based exams), question banks
- **HR**: Staff management, leave applications
- **Counselling**: Student counselling module

## Database Schema Highlights

- **100+ Prisma models** covering all university operations
- **Multi-tenancy**: University → Institute → Department hierarchy
- **Academic configuration**: Stream labels, subject labels, versioned rules
- **Workflow engine**: Generic state machine for approvals
- **Exam system**: CBE with proctoring, question banks, auto-grading
- **Fee system**: Fee heads, demands, payments, waivers

## Unknowns and Gaps

See **21_UNKNOWNS_AND_OPEN_QUESTIONS.md** for:
- Elasticsearch usage details (configured but not deeply explored)
- Student portal implementation (placeholder exists)
- Some worker queue implementations (minimal app modules)
- Specific workflow configurations
- Integration testing coverage

## Version

- **Project Version**: 1.3.1
- **Last Updated**: July 2026
