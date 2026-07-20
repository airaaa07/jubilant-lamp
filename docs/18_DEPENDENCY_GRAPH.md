# University ERP - Dependency Graph

## Overview

This document describes the dependencies between services, modules, and components in the University ERP system.

## Service Dependencies

### Core API Dependencies

```
Core API (port 3000)
├── PostgreSQL (port 5432) - Required
├── Redis (port 6379) - Required
├── MinIO (port 9000) - Required
└── Elasticsearch (port 9200) - Optional
```

### CBE Engine Dependencies

```
CBE Engine (port 3001)
├── PostgreSQL (port 5432) - Required
└── Redis (port 6379) - Required
```

### Notification Worker Dependencies

```
Notification Worker (port 3002)
└── Redis (port 6379) - Required
```

### Certificate Generator Dependencies

```
Certificate Generator (port 3003)
├── PostgreSQL (port 5432) - Required
├── MinIO (port 9000) - Required
└── Redis (port 6379) - Required
```

### Admin Portal Dependencies

```
Admin Portal (port 5173)
└── Core API (port 3000) - Required
```

## Module Dependencies (Core API)

### Core Dependencies

All modules depend on:

- **PrismaService** - Database access
- **RedisService** - Caching and queues
- **MinioService** - Object storage
- **ConfigService** - Configuration

### Auth Module

```
AuthModule
├── PrismaService
├── RedisService
├── MailService (integrated)
├── SmsService (integrated)
└── JwtService
```

### Master Data Module

```
MasterDataModule
├── PrismaService
├── RedisService
└── UniversityService
├── InstituteService
└── DepartmentService
```

### Admissions Module

```
AdmissionsModule
├── PrismaService
├── RedisService
├── WorkflowModule
├── FormsModule
└── FeeModule
```

### Academic Module

```
AcademicModule
├── PrismaService
├── RedisService
├── AttendanceModule
├── ExaminationModule
└── TimetableModule
```

### Examination Module

```
ExaminationModule
├── PrismaService
├── RedisService
├── MinioService
├── QuestionBankModule
└── CBE Engine (WebSocket)
```

### Fee Module

```
FeeModule
├── PrismaService
├── RedisService
├── Razorpay (external)
└── NotificationModule
```

### Workflow Module

```
WorkflowModule
├── PrismaService
├── RedisService
├── ResourceReservationModule
└── NotificationModule
```

### Documents Module

```
DocumentsModule
├── PrismaService
├── MinioService
├── Certificate Generator (queue)
└── NotificationModule
```

### Notification Module

```
NotificationModule
├── PrismaService
├── RedisService
├── MailService
├── SmsService
└── Notification Worker (queue)
```

## Frontend Dependencies

### Admin Portal

```
Admin Portal
├── Core API (HTTP)
├── React Router
├── React Query
├── TailwindCSS
├── Headless UI
└── Lucide Icons
```

### Page Dependencies

```
DashboardPage
├── Analytics API
└── Notifications API

MasterDataPage
├── Universities API
├── Institutes API
└── Departments API

AdmissionsPage
├── Admissions API
├── Workflow API
└── Forms API

ExaminationsPage
├── Exam Papers API
├── Questions API
└── Results API

ExamTakePage
├── CBE Engine (WebSocket)
└── Exam Attempts API

FeesPage
├── Fee Ledger API
└── Payments API

DocumentsPage
├── Document Templates API
└── Issued Documents API
```

## Infrastructure Dependencies

### PostgreSQL

```
PostgreSQL
├── Core API
├── CBE Engine
└── Certificate Generator
```

### Redis

```
Redis
├── Core API (caching, sessions)
├── CBE Engine (WebSocket sessions)
├── Notification Worker (queue backend)
└── Certificate Generator (queue backend)
```

### MinIO

```
MinIO
├── Core API
└── Certificate Generator
```

### Elasticsearch

```
Elasticsearch
└── Core API (optional, not deeply integrated)
```

## External Service Dependencies

### Payment Gateway

```
Razorpay
└── FeeModule (payment processing)
```

### Email Service

```
SMTP Server
├── AuthModule (OTP emails)
├── NotificationModule (notifications)
└── DocumentsModule (document delivery)
```

### SMS Service

```
SMS Gateway
├── AuthModule (OTP SMS)
└── NotificationModule (SMS notifications)
```

### Cloud Storage

```
Azure Blob Storage (optional)
└── MinioService (fallback for MinIO)
```

### Secret Management

```
AWS Secrets Manager (optional)
├── VaultService (AWS provider)
└── Core API (configuration)

Azure Key Vault (optional)
├── VaultService (Azure provider)
└── Core API (configuration)

Google Secret Manager (optional)
├── VaultService (Google provider)
└── Core API (configuration)
```

## Dependency Graph Visualization

### Service Level

```
┌─────────────────────────────────────────────────────────┐
│                      Nginx                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Admin Portal  │  │    Core API     │  │   CBE Engine    │
└────────────────┘  └────────┬────────┘  └────────┬────────┘
                           │                     │
        ┌──────────────────┼──────────────────┐ │
        │                  │                  │ │
┌───────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
│ Notification   │ │ Cert Gen    │ │  PostgreSQL     │
│   Worker       │ │              │ └─────────────────┘
└────────┬────────┘ └──────────────┘
         │
┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
│     Redis       │ │     MinIO       │ │  Elasticsearch  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Module Level (Core API)

```
┌─────────────────────────────────────────────────────────┐
│                    Core API                              │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  AuthModule    │  │ MasterDataModule│  │ AdmissionsModule│
└────────────────┘  └─────────────────┘  └────────┬────────┘
                                                   │
        ┌──────────────────────────────────────────┘
        │
┌───────▼────────┐  ┌────────▼────────┐  ┌─────────────────┐
│ WorkflowModule │  │  FormsModule    │  │   FeeModule      │
└────────────────┘  └─────────────────┘  └─────────────────┘
```

## Circular Dependencies

### Potential Circular Dependencies

1. **WorkflowModule ↔ ResourceReservationModule**
   - Workflow uses ResourceReservation for holds
   - ResourceReservation may trigger workflows
   - **Resolution**: Use events/queues to break circular dependency

2. **NotificationModule ↔ AuthModule**
   - Auth uses Notification for OTP
   - Notification uses Auth for user context
   - **Resolution**: Auth has integrated mail/sms, not using NotificationModule

3. **DocumentsModule ↔ CertificateGenerator**
   - Documents uses CertificateGenerator for PDF generation
   - CertificateGenerator uses Documents for templates
   - **Resolution**: Queue-based processing breaks circular dependency

## Startup Order

### Docker Compose Startup Order

```
1. PostgreSQL (database)
2. Redis (cache/queue)
3. MinIO (storage)
4. Elasticsearch (search)
5. Core API (depends on 1-4)
6. CBE Engine (depends on 1, 2)
7. Notification Worker (depends on 2)
8. Certificate Generator (depends on 1, 3, 2)
9. Admin Portal (depends on 5)
10. Nginx (depends on 5, 6, 9)
```

### PM2 Startup Order

```
1. Core API (primary API)
2. CBE Engine (exam engine)
3. Notification Worker (background jobs)
4. Certificate Generator (background jobs)
```

## Runtime Dependencies

### Request Flow Dependencies

```
User Request
    ↓
Admin Portal (React)
    ↓
HTTP Request
    ↓
Nginx (reverse proxy)
    ↓
Core API (NestJS)
    ↓
Controller
    ↓
Service
    ↓
PrismaService (database)
    ↓
PostgreSQL
    ↓
Response
    ↓
RedisService (cache)
    ↓
MinioService (storage)
    ↓
NotificationModule (async)
    ↓
Redis Queue
    ↓
Notification Worker
    ↓
External Service (email/SMS)
```

## Data Flow Dependencies

### Student Registration Flow

```
Registration Form
    ↓
AuthModule (register)
    ↓
PrismaService (create user)
    ↓
PostgreSQL (store user)
    ↓
RedisService (store OTP)
    ↓
MailService (send email OTP)
    ↓
SmsService (send mobile OTP)
    ↓
User verifies OTP
    ↓
AuthModule (activate user)
    ↓
PrismaService (update user)
    ↓
PostgreSQL (update user)
```

### Exam Flow

```
Student starts exam
    ↓
ExamTakePage (React)
    ↓
WebSocket connection
    ↓
CBE Engine (NestJS)
    ↓
ExamPaper (Prisma)
    ↓
PostgreSQL (get paper)
    ↓
Student answers
    ↓
CBE Engine (store answers)
    ↓
Redis (session state)
    ↓
Proctoring events
    ↓
MinioService (upload snapshots)
    ↓
MinIO (store snapshots)
    ↓
Exam submission
    ↓
Core API (auto-grade)
    ↓
PrismaService (update attempt)
    ↓
PostgreSQL (store results)
```

## Dependency Management

### npm Workspaces

The monorepo uses npm workspaces:

```json
{
  "workspaces": [
    "apps/*",
    "web/*",
    "libs/*"
  ]
}
```

### Shared Dependencies

Common dependencies are managed at root level:

```json
{
  "devDependencies": {
    "typescript": "^6.0.0",
    "@types/node": "^20.0.0",
    "turbo": "^2.0.0"
  }
}
```

### Service-Specific Dependencies

Each service has its own package.json:

```json
{
  "dependencies": {
    "@nestjs/common": "^10.0.0",
    "@nestjs/core": "^10.0.0",
    "prisma": "^5.0.0"
  }
}
```

## Dependency Updates

### Update Strategy

1. **Security updates**: Update immediately
2. **Major updates**: Test thoroughly before updating
3. **Minor updates**: Update monthly
4. **Patch updates**: Update weekly

### Update Commands

```bash
# Check for outdated packages
npm outdated

# Update all packages
npm update

# Update specific package
npm update package-name

# Audit for vulnerabilities
npm audit
npm audit fix
```

## Dependency Security

### Vulnerability Scanning

```bash
# Run npm audit
npm audit

# Fix vulnerabilities
npm audit fix

# Force fix (may break changes)
npm audit fix --force
```

### Snyk Integration

```bash
# Install Snyk
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor for vulnerabilities
snyk monitor
```

## Known Limitations

1. **No Dependency Visualization**: No dependency graph visualization tool
2. **No Dependency Locking**: No lock file for shared dependencies
3. **No Dependency Version Constraints**: Loose version constraints
4. **No Dependency Health Monitoring**: No monitoring for dependency health
5. **No Dependency Rollback**: No automated rollback mechanism

## Future Enhancements

1. **Add Dependency Visualization**: Use tools like Madge or Depcheck
2. **Add Dependency Locking**: Use npm-lockfile or pnpm
3. **Add Version Constraints**: Use strict version constraints
4. **Add Dependency Health Monitoring**: Monitor dependency health
5. **Add Dependency Rollback**: Automated rollback mechanism
6. **Add Dependency Updates**: Automated dependency updates (Dependabot)
7. **Add Dependency Scanning**: Continuous vulnerability scanning
8. **Add Dependency Documentation**: Document each dependency's purpose
