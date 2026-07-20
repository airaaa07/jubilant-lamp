# University ERP - Repository Structure

## Root Directory Structure

```
/home/admin/UniversityERP/
├── .claude/                    # Claude Code configuration
├── .dockerignore              # Docker build exclusions
├── .env                      # Environment variables (not committed)
├── .env.example              # Environment variable template
├── .git/                     # Git repository
├── .githooks/                # Git hooks for memory sync
├── .gitignore                # Git exclusions
├── .turbo/                   # Turbo build cache
├── README.md                 # Git hooks documentation
├── apps/                     # Backend services (NestJS)
├── deploy/                   # Deployment scripts
├── docker/                   # Docker configuration files
├── docker-compose.yml        # Docker services definition
├── docker-volumes/          # Docker volume mounts
├── docs/                     # Documentation (this directory)
├── dumps/                    # Database dumps
├── ecosystem.native.config.js # PM2 configuration
├── libs/                     # Shared libraries (empty)
├── mobile/                   # Mobile app (placeholder)
├── node_modules/             # npm dependencies
├── package.json              # Root package.json (workspaces)
├── package-lock.json         # npm lock file
├── scripts/                  # Utility scripts
├── start.sh                  # Startup script
├── status.sh                 # Status check script
├── stop.sh                   # Shutdown script
├── tsconfig.base.json        # Base TypeScript configuration
├── turbo.json                # Turbo build configuration
└── vault.env.json            # Vault secrets configuration
```

## Apps Directory (Backend Services)

```
apps/
├── core-api/                 # Main NestJS API server (port 3000)
│   ├── .turbo/              # Turbo cache
│   ├── Dockerfile           # Docker image definition
│   ├── dist/                # Compiled JavaScript
│   ├── jest.config.js       # Jest test configuration
│   ├── nest-cli.json        # NestJS CLI configuration
│   ├── node_modules/        # Dependencies
│   ├── package.json         # Dependencies and scripts
│   ├── prisma/              # Database schema and migrations
│   ├── scripts/             # Utility scripts
│   ├── src/                 # Source code
│   ├── tsconfig.build.json  # Build TypeScript config
│   ├── tsconfig.build.tsbuildinfo # Build cache
│   ├── tsconfig.json        # TypeScript config
│   └── webpack.config.js    # Webpack configuration
│
├── cbe-engine/               # Computer-Based Exam engine (port 3001)
│   ├── Dockerfile           # Docker image definition
│   ├── node_modules/        # Dependencies
│   ├── package.json         # Dependencies and scripts
│   └── src/                 # Source code
│
├── cert-generator/          # Certificate generator (port 3003)
│   ├── Dockerfile           # Docker image definition
│   ├── node_modules/        # Dependencies
│   ├── package.json         # Dependencies and scripts
│   └── src/                 # Source code
│
└── notification-worker/     # Notification worker (port 3002)
    ├── Dockerfile           # Docker image definition
    ├── node_modules/        # Dependencies
    ├── package.json         # Dependencies and scripts
    └── src/                 # Source code
```

## Web Directory (Frontend)

```
web/
├── admin-portal/            # React admin interface (port 5173)
│   ├── node_modules/        # Dependencies
│   ├── package.json         # Dependencies and scripts
│   └── src/                 # Source code
│
└── student-portal/          # Student portal (placeholder)
    ├── .gitkeep             # Placeholder file
    ├── node_modules/        # Dependencies
    └── src/                 # Source code (empty)
```

## Core API Source Structure

```
apps/core-api/src/
├── app.module.ts            # Root NestJS module
├── main.ts                  # Application bootstrap
│
├── common/                  # Shared utilities and decorators
│   ├── __tests__/          # Common tests
│   ├── context/            # Request context (async local storage)
│   ├── decorators/         # Custom decorators (@Public, @Scope, etc.)
│   ├── filters/            # Exception filters
│   ├── guards/             # Auth guards (JWT, Scope)
│   ├── index.ts            # Common exports
│   ├── middleware/         # Express middleware
│   ├── password-policy.ts  # Password validation rules
│   ├── pipes/              # Custom pipes (Zod validation)
│   ├── profile-completeness.ts # Profile completeness logic
│   ├── social-links.ts     # Social link validation
│   └── utils/              # Utility functions
│
├── database/                # Database configuration
│   ├── __tests__/          # Database tests
│   ├── audit-middleware.ts # Prisma audit middleware
│   ├── database.module.ts  # Database module
│   └── prisma.service.ts   # Prisma client wrapper
│
├── health/                  # Health check endpoints
│   └── health.module.ts    # Health module
│
├── infrastructure/          # Infrastructure services
│   ├── minio/              # Object storage (MinIO/Azure)
│   │   ├── minio.module.ts
│   │   └── minio.service.ts
│   ├── redis/              # Redis client
│   │   ├── redis.module.ts
│   │   └── redis.service.ts
│   └── vault/              # Secret management
│       ├── vault.bootstrap.ts
│       └── vault.service.ts
│
├── modules/                 # Feature modules (36 modules)
│   ├── academic/           # Academic operations
│   ├── admissions/         # Admissions management
│   ├── analytics/          # Analytics and reporting
│   ├── attendance/         # Attendance tracking
│   ├── audit/              # Audit log viewer
│   ├── auth/               # Authentication
│   ├── banners/            # Login banners
│   ├── branding/           # University branding
│   ├── counselling/        # Student counselling
│   ├── directory/          # Staff/student directory
│   ├── documents/          # Document generation
│   ├── examination/        # Examination management
│   ├── fee/                # Fee management
│   ├── forms/              # Dynamic forms
│   ├── hostel/             # Hostel management
│   ├── hr/                 # HR management
│   ├── id-format/          # ID format configuration
│   ├── library/            # Library management
│   ├── master-data/        # Master data management
│   ├── notice-board/       # Notice board
│   ├── notifications/      # Notifications
│   ├── onboarding/         # Student onboarding
│   ├── parent-portal/      # Parent portal features
│   ├── question-bank/      # Question bank
│   ├── resource-optimisation/ # Resource optimization
│   ├── resource-reservation/ # Resource booking
│   ├── roles/              # Role management
│   ├── settings/           # System settings
│   ├── social-monitoring/   # Social media monitoring
│   ├── staff-subject/      # Staff-subject mapping
│   ├── student-profile/    # Student profiles
│   ├── timetable/          # Timetable management
│   ├── transport/          # Transport management
│   ├── upload/             # File upload handling
│   ├── users/              # User management
│   └── workflow/           # Workflow engine
│
└── types/                   # TypeScript type definitions
    └── index.ts            # Shared types
```

## Admin Portal Source Structure

```
web/admin-portal/src/
├── App.tsx                  # Root React component
├── App.css                  # Global styles
├── index.css                # Base styles
├── main.tsx                 # React entry point
│
├── api/                     # API client layer
│   ├── auth.ts             # Authentication API
│   ├── axios.ts            # Axios configuration
│   └── modules.ts          # Module-specific API calls
│
├── auth/                    # Authentication context
│   ├── AuthContext.tsx     # Auth provider
│   ├── ProtectedRoute.tsx   # Route protection
│   ├── StudentStatusContext.tsx # Student status
│   └── useAuth.ts          # Auth hook
│
├── components/              # Reusable components
│   ├── AdmissionApplyModal.tsx
│   ├── ApplicantCard.tsx
│   ├── ApplicationFeeModal.tsx
│   ├── Badge.tsx
│   ├── BannerHost.tsx
│   ├── CanvasDocumentDesigner.tsx
│   ├── ConfirmDialog.tsx
│   ├── DateInput.tsx
│   ├── DateTimeInput.tsx
│   ├── DrillModal.tsx
│   ├── ErrorBoundary.tsx
│   ├── ExecDashboard.tsx
│   ├── Folder.tsx
│   ├── FormField.tsx
│   ├── HelpDrawer.tsx
│   ├── InstanceDrawer.tsx
│   ├── Modal.tsx
│   ├── NotEnrolledNotice.tsx
│   ├── NotificationBell.tsx
│   ├── PageHeader.tsx
│   ├── Pagination.tsx
│   ├── PersonalDashboard.tsx
│   ├── ProgramLabelDetailModal.tsx
│   ├── ReadOnlyFormView.tsx
│   ├── RichContent.tsx
│   ├── SearchBar.tsx
│   ├── SearchSelect.tsx
│   ├── Spinner.tsx
│   ├── StreamLabelDetailModal.tsx
│   ├── SystemStatus.tsx
│   ├── Table.tsx
│   ├── Tabs.tsx
│   ├── WorkflowProgress.tsx
│   └── canvas/             # Canvas-related components
│
├── config/                  # Configuration
│   ├── appTitle.ts         # App title management
│   └── ...
│
├── help/                    # Help documentation
│   └── (32 help files)
│
├── layouts/                 # Layout components
│   └── AdminLayout.tsx     # Main admin layout
│
├── lib/                     # Utility libraries
│   ├── appTitle.ts         # Title utilities
│   └── ...
│
├── pages/                   # Page components (41 pages)
│   ├── AdmissionsPage.tsx
│   ├── AnalyticsPage.tsx
│   ├── AttendancePage.tsx
│   ├── AuditLogPage.tsx
│   ├── BannersPage.tsx
│   ├── CounsellingAdminPage.tsx
│   ├── CounsellingDeskPage.tsx
│   ├── DashboardPage.tsx
│   ├── DirectoryPage.tsx
│   ├── DocumentsPage.tsx
│   ├── ExamItemAnalysisPage.tsx
│   ├── ExamMonitorPage.tsx
│   ├── ExamTakePage.tsx
│   ├── ExaminationsPage.tsx
│   ├── FeesPage.tsx
│   ├── ForgotPasswordPage.tsx
│   ├── FormsPage.tsx
│   ├── HRPage.tsx
│   ├── HelpCenterPage.tsx
│   ├── HostelPage.tsx
│   ├── IdFormatsPage.tsx
│   ├── LeaveRequestsPage.tsx
│   ├── LibraryPage.tsx
│   ├── LoginPage.tsx
│   ├── MasterDataPage.tsx
│   ├── MeritListPage.tsx
│   ├── MyInvigilationPage.tsx
│   ├── MyTasksPage.tsx
│   ├── NoticeBoardPage.tsx
│   ├── OnboardStudentsPage.tsx
│   ├── ProgramFeeManager.tsx
│   ├── RegisterPage.tsx
│   ├── ResetPasswordPage.tsx
│   ├── ResourceFeeManager.tsx
│   ├── SettingsPage.tsx
│   ├── SetupAccountPage.tsx
│   ├── StartAdmissionsPage.tsx
│   ├── StudentApplicationsPage.tsx
│   ├── StudentProfilePage.tsx
│   ├── TimetablePage.tsx
│   ├── TransportPage.tsx
│   ├── UserManagementPage.tsx
│   ├── WorkflowDesignerPage.tsx
│   └── WorkflowMonitorPage.tsx
│
├── theme/                   # Theme configuration
│   └── ThemeContext.tsx    # Theme provider
│
└── utils/                   # Utility functions
    └── ...
```

## Prisma Directory Structure

```
apps/core-api/prisma/
├── MIGRATIONS.md            # Migration documentation
├── _migrations_archive_pre_baseline/ # Archived migrations
├── migrations/              # Database migrations
├── schema.prisma            # Database schema (2999 lines)
├── clean-stale-registrations.js
├── fix-admission-cascade-fields.js
├── fix-allocation-student-keys.js
├── fix-scholarship-field.js
├── patch-admission-application-fee-gate.js
├── patch-admission-assign-application-no.js
├── patch-admission-forms-remove-inform-payment.js
├── patch-admission-meritlist.js
├── patch-admission-send-back.js
├── patch-admission-strict-payment-gate.js
├── patch-alumni-doc-charge-gate.js
├── rename-stream-labels.js
├── seed-admission-approvers.js
├── seed-admission-coursetypes.js
├── seed-admission-forms.js
├── seed-alumni-and-deletion.js
├── seed-alumni-fee-head.js
├── seed-application-approver-roles.js
├── seed-catalog.js
├── seed-config.js
├── seed-defaults.js
├── seed-document-templates.js
├── seed-fix-stream-codes.js
├── seed-form-workflow-folders.js
├── seed-hostel-transport.ts
├── seed-institute-data.ts
├── seed-notice-board.js
├── seed-program-fee-head.js
├── seed-question-bank-disciplines.js
├── seed-question-bank-medical.js
├── seed-question-bank-technology.js
├── seed-question-bank.js
├── seed-reassessment-supplementary-fee-heads.js
├── seed-registration-forms.js
├── seed-roles.js
├── seed-scholarship-head.js
├── seed-settings.js
├── seed-subset/             # Subset seed files
├── seed-superadmin.js
├── seed-testing-institute.js
├── seed-workflow-admission.js
├── seed-workflow-document-request.js
├── seed-workflow-leave.js
├── seed-workflow-reservations.js
├── seed-workflow-start-admissions.js
└── seed.ts                  # Seed entry point
```

## Docker Directory Structure

```
docker/
├── nginx/
│   └── nginx.conf          # Nginx configuration
└── postgres/
    └── init.sql            # PostgreSQL initialization
```

## Scripts Directory Structure

```
scripts/
└── (utility scripts for deployment and maintenance)
```

## Deploy Directory Structure

```
deploy/
└── (deployment configuration and scripts)
```

## Key File Purposes

### Root Configuration Files

- **package.json**: Defines npm workspaces and root scripts
- **docker-compose.yml**: Defines all Docker services (infrastructure + apps)
- **turbo.json**: Turbo build system configuration for monorepo
- **tsconfig.base.json**: Base TypeScript configuration
- **.env.example**: Template for environment variables
- **start.sh**: Script to start all services
- **stop.sh**: Script to stop all services
- **status.sh**: Script to check service status

### Core API Configuration

- **nest-cli.json**: NestJS CLI configuration
- **jest.config.js**: Jest test configuration
- **webpack.config.js**: Webpack bundling configuration
- **tsconfig.build.json**: TypeScript build configuration

### Frontend Configuration

- **vite.config.js**: Vite build configuration (inferred from package.json)
- **tailwind.config.js**: TailwindCSS configuration (inferred)
- **postcss.config.js**: PostCSS configuration (inferred)

## Module Organization Pattern

Each NestJS module typically follows this structure:

```
modules/[module-name]/
├── [module-name].module.ts    # Module definition
├── [module-name].controller.ts # API endpoints
├── [module-name].service.ts    # Business logic
├── dto/                       # Data transfer objects
│   ├── [entity].dto.ts
│   └── [entity].schema.ts     # Zod validation schemas
└── (optional subdirectories)
```

## Naming Conventions

### Files

- **Controllers**: `[module].controller.ts`
- **Services**: `[module].service.ts`
- **Modules**: `[module].module.ts`
- **DTOs**: `[entity].dto.ts`
- **Schemas**: `[entity].schema.ts`
- **Guards**: `[purpose].guard.ts`
- **Pipes**: `[purpose].pipe.ts`

### Database

- **Tables**: snake_case (e.g., `user_roles`)
- **Models**: PascalCase (e.g., `UserRole`)
- **Columns**: snake_case (e.g., `created_at`)
- **Relations**: camelCase in Prisma (e.g., `userRoles`)

### API Routes

- **Pattern**: `/api/[module]/[resource]`
- **Plural**: Resource names are plural (e.g., `/api/users`)
- **Nested**: Related resources use nesting (e.g., `/api/users/:id/posts`)

## Environment-Specific Files

- **Development**: `.env` (not committed)
- **Example**: `.env.example` (committed template)
- **Native**: `.env.native` (native deployment)
- **Backup**: `.env.bak-*` (backups)

## Build Artifacts

- **dist/**: Compiled JavaScript (not committed)
- **node_modules/**: npm dependencies (not committed)
- **.turbo/**: Turbo build cache (not committed)
- **tsconfig.build.tsbuildinfo**: TypeScript build cache (not committed)

## Git Structure

- **.git/**: Git repository metadata
- **.githooks/**: Committed git hooks
- **.gitignore**: Git exclusions
- **.dockerignore**: Docker build exclusions

## Documentation Structure

```
docs/
├── 00_PROJECT_INDEX.md
├── 01_SYSTEM_OVERVIEW.md
├── 02_REPOSITORY_STRUCTURE.md
├── 03_BACKEND_ARCHITECTURE.md
├── 04_FRONTEND_ARCHITECTURE.md
├── 05_DATABASE.md
├── 06_API_REFERENCE.md
├── 07_FEATURE_FLOWS.md
├── 08_WORKERS_AND_QUEUES.md
├── 09_STORAGE_AND_MINIO.md
├── 10_REDIS.md
├── 11_ELASTICSEARCH.md
├── 12_AUTHENTICATION.md
├── 13_EMAIL_AND_SMTP.md
├── 14_CERTIFICATE_ENGINE.md
├── 15_CONFIGURATION.md
├── 16_ENVIRONMENT_VARIABLES.md
├── 17_INFRASTRUCTURE.md
├── 18_DEPENDENCY_GRAPH.md
├── 19_REQUEST_LIFECYCLES.md
├── 20_LEARNING_GUIDE.md
└── 21_UNKNOWNS_AND_OPEN_QUESTIONS.md
```

## Volume Mounts

```
docker-volumes/
├── postgres/               # PostgreSQL data
├── redis/                  # Redis data
├── minio/                  # MinIO data
├── elasticsearch/          # Elasticsearch data
└── nginx/                  # Nginx logs
```

## Important Notes

1. **Monorepo Structure**: Uses npm workspaces with Turbo for efficient builds
2. **Shared Code**: `libs/` directory exists but is empty (no shared packages currently)
3. **Placeholder Services**: `student-portal` and `mobile` are placeholders
4. **Database Migrations**: Extensive seed scripts for initial data
5. **Git Hooks**: Custom hooks for Claude Code memory sync
6. **Docker Profiles**: Core API has `docker-only` profile for containerized deployment
7. **PM2 Configuration**: Native deployment uses PM2 for process management
