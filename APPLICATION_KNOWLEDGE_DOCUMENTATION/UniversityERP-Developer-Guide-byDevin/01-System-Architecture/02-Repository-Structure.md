# Repository Structure

## Purpose

This document provides a detailed explanation of the University ERP repository structure. It explains the organization of files and directories, the purpose of each folder, and the naming conventions used.

## Why This Document Exists

**Confirmed by Code**: The University ERP is a monorepo with multiple services and a complex directory structure. Understanding the repository structure is critical for:
- Navigating the codebase efficiently
- Finding specific files quickly
- Understanding the project organization
- Adding new features in the correct location
- Following the established patterns

Without understanding the repository structure, developers may place files in wrong locations or break established patterns.

## Where This Is Used

- **Onboarding**: New developers learn the structure
- **Navigation**: Finding files during development
- **Code Reviews**: Ensuring files are in correct locations
- **Refactoring**: Moving files to correct locations
- **Architecture Decisions**: Understanding the organization rationale

## Dependencies

### Repository Dependencies

**Confirmed by Code**: The repository uses npm workspaces for monorepo management.

**Workspace Configuration**:
```json
{
  "workspaces": [
    "apps/*",
    "web/*",
    "libs/*"
  ]
}
```

### Directory Dependencies

**Confirmed by Code**: The directory structure follows a specific pattern:
- `apps/` - Backend services
- `web/` - Frontend applications
- `libs/` - Shared libraries
- `docker-volumes/` - Docker data persistence
- `deploy/` - Deployment configurations

## Internal Architecture

### Root Directory Structure

**Confirmed by Code**: The root directory contains the following structure:

```
UniversityERP/
├── apps/                          # Backend services
│   ├── core-api/                  # Main NestJS backend
│   ├── cbe-engine/                # Computer-Based Exam engine
│   ├── notification-worker/        # Background notification worker
│   └── cert-generator/            # Certificate generation worker
├── web/                           # Frontend applications
│   └── admin-portal/              # React admin portal
├── libs/                          # Shared libraries (currently empty)
├── docker-volumes/                # Docker data persistence
│   ├── postgres/                  # PostgreSQL data
│   ├── redis/                     # Redis data
│   ├── minio/                     # MinIO data
│   ├── elasticsearch/             # Elasticsearch data
│   └── nginx/                     # Nginx logs
├── deploy/                        # Deployment configurations
│   ├── native/                    # Native deployment scripts
│   └── docker/                    # Docker deployment configs
├── docker/                        # Docker configurations
│   └── nginx/                     # Nginx configuration
├── docs/                          # Documentation
├── scripts/                       # Utility scripts
├── .env.example                   # Environment variables template
├── .env.native                    # Native deployment environment
├── .gitignore                     # Git ignore rules
├── docker-compose.yml             # Docker Compose configuration
├── package.json                   # Root package.json
├── pnpm-workspace.yaml            # pnpm workspace config (if using pnpm)
├── turbo.json                     # Turborepo configuration
└── tsconfig.json                  # Root TypeScript config
```

## Code Walkthrough

### Root Files

**Confirmed by Code**: The root directory contains configuration files.

#### package.json

**Purpose**: Root package.json for monorepo management.

**Key Sections**:
```json
{
  "name": "university-erp",
  "private": true,
  "workspaces": [
    "apps/*",
    "web/*",
    "libs/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "format": "turbo run format",
    "test": "turbo run test"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^6.0.0"
  }
}
```

**What It Does**:
- Defines workspace directories
- Defines root-level scripts
- Defines shared dev dependencies

#### turbo.json

**Purpose**: Turborepo configuration for build optimization.

**Confirmed by Code**: turbo.json exists in root.

**Configuration**:
```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    }
  }
}
```

**What It Does**:
- Defines build pipeline
- Defines dependencies between packages
- Defines cache strategy
- Defines outputs to cache

#### docker-compose.yml

**Purpose**: Docker Compose configuration for infrastructure services.

**Confirmed by Code**: docker-compose.yml exists in root.

**Services**:
- PostgreSQL
- Redis
- MinIO
- Elasticsearch
- Nginx (optional)

**What It Does**:
- Defines infrastructure services
- Defines service dependencies
- Defines volume mounts
- Defines network configuration

#### .env.example

**Purpose**: Template for environment variables.

**Confirmed by Code**: .env.example exists in root.

**Variables**:
- DATABASE_URL
- REDIS_HOST, REDIS_PORT
- MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
- JWT_SECRET, JWT_EXPIRY, JWT_REFRESH_EXPIRY
- SMTP configuration
- ELASTICSEARCH_NODE

**What It Does**:
- Documents required environment variables
- Provides default values
- Serves as template for .env file

## Database Interactions

### No Direct Database Interactions

**Confirmed by Code**: The root directory does not contain database interaction code. All database interactions are in individual services.

## Redis Interactions

### No Direct Redis Interactions

**Confirmed by Code**: The root directory does not contain Redis interaction code. All Redis interactions are in individual services.

## Queue Interactions

### No Direct Queue Interactions

**Confirmed by Code**: The root directory does not contain queue interaction code. All queue interactions are in individual services.

## Worker Interactions

### No Direct Worker Interactions

**Confirmed by Code**: The root directory does not contain worker code. All workers are in the apps/ directory.

## Business Rules

### File Organization Rules

**Confirmed by Code**: The repository follows these organization rules:

1. **Backend Services**: All backend services in `apps/`
2. **Frontend Applications**: All frontend apps in `web/`
3. **Shared Code**: All shared code in `libs/`
4. **Docker Configs**: Docker configs in `docker/`
5. **Deployment Configs**: Deployment configs in `deploy/`
6. **Documentation**: Documentation in `docs/`
7. **Scripts**: Utility scripts in `scripts/`

### Naming Conventions

**Confirmed by Code**: The repository follows these naming conventions:

1. **Directory Names**: kebab-case (e.g., `core-api`, `admin-portal`)
2. **File Names**: kebab-case (e.g., `auth.controller.ts`, `auth.service.ts`)
3. **Class Names**: PascalCase (e.g., `AuthService`, `AuthController`)
4. **Interface Names**: PascalCase with `I` prefix (e.g., `IUserService`)
5. **Type Names**: PascalCase (e.g., `UserDto`, `LoginDto`)
6. **Constant Names**: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)
7. **Private Methods**: camelCase with underscore prefix (e.g., `_validateUser`)
8. **Public Methods**: camelCase (e.g., `validateUser`)

## Security

### .gitignore

**Confirmed by Code**: .gitignore exists in root.

**Ignored Files**:
- `node_modules/`
- `dist/`
- `.env`
- `.env.local`
- `.env.*.local`
- `coverage/`
- `.turbo/`
- `docker-volumes/`
- `*.log`

**What It Does**:
- Prevents committing sensitive files
- Prevents committing build artifacts
- Prevents committing environment-specific files

### Environment Variables

**Confirmed by Code**: Environment variables are in .env file (not committed).

**Sensitive Variables**:
- DATABASE_URL
- JWT_SECRET
- SMTP_PASSWORD
- MINIO_SECRET_KEY
- AZURE_STORAGE_CONNECTION_STRING

**What It Does**:
- Keeps sensitive data out of version control
- Allows environment-specific configuration
- Enables secure secret management

## Performance Considerations

### Build Performance

**Confirmed by Code**: Turborepo optimizes build performance.

**Optimizations**:
- Parallel builds
- Build caching
- Incremental builds
- Dependency-aware builds

### Monorepo Performance

**Confirmed by Code**: npm workspaces manage monorepo dependencies.

**Optimizations**:
- Shared dependencies
- Hoisted node_modules
- Efficient dependency resolution

## Common Mistakes

### Mistake 1: Placing Files in Wrong Directory

**Symptom**: Code not found or not working

**Cause**: File placed in wrong directory

**Fix**:
- Backend code goes in `apps/`
- Frontend code goes in `web/`
- Shared code goes in `libs/`

### Mistake 2: Not Following Naming Conventions

**Symptom**: Code style inconsistent

**Cause**: Not following naming conventions

**Fix**:
- Use kebab-case for file names
- Use PascalCase for class names
- Use camelCase for method names

### Mistake 3: Committing .env File

**Symptom**: Sensitive data in version control

**Cause**: .env file committed

**Fix**:
- Add .env to .gitignore
- Remove .env from git history
- Use .env.example as template

## Debugging Guide

### Repository-Level Debugging

**Issue**: Build fails

**Investigation**:
```bash
# Check turbo configuration
cat turbo.json

# Check workspace configuration
cat package.json

# Check dependencies
npm install

# Try building specific package
cd apps/core-api
npm run build
```

**Tools**:
- Turborepo logs
- npm logs
- TypeScript compiler logs

## Future Enhancements

### Shared Libraries

**Status**: libs/ directory exists but is empty

**Proposal**: Move shared code to libs/:
- Shared types
- Shared utilities
- Shared constants
- Shared validators

### Monorepo Tool

**Status**: Using npm workspaces

**Enhancement**: Consider using pnpm or Yarn for better performance:
- pnpm: Faster, uses hard links
- Yarn: Better workspace support

## Production Considerations

### Build Artifacts

**Production Build**:
- Build all packages: `npm run build`
- Output in `dist/` directories
- Deploy `dist/` directories

### Environment Files

**Production Environment**:
- Use `.env.production` for production
- Use secrets manager for sensitive values
- Never commit production .env file

## Example Requests

### Build All Packages

**Request**:
```bash
npm run build
```

**Response**:
```
• Packages in scope: core-api, cbe-engine, notification-worker, cert-generator, admin-portal
• Tasks: 5 successful, 0 total
```

## Example Responses

### Package Structure

**Request**:
```bash
ls apps/
```

**Response**:
```
core-api/
cbe-engine/
notification-worker/
cert-generator/
```

## Sequence Diagrams

### Build Flow

```
Developer → npm run build
    ↓
Turborepo
    ↓
Build dependency graph
    ↓
Build packages in parallel
    ↓
Cache build artifacts
    ↓
Return build status
```

## Architecture Diagrams

### Repository Structure Diagram

```
UniversityERP/
├── apps/
│   ├── core-api/
│   │   ├── src/
│   │   ├── prisma/
│   │   ├── test/
│   │   └── package.json
│   ├── cbe-engine/
│   ├── notification-worker/
│   └── cert-generator/
├── web/
│   └── admin-portal/
│       ├── src/
│       ├── public/
│       └── package.json
├── libs/
│   └── (empty)
├── docker-volumes/
├── deploy/
├── docker/
├── docs/
├── scripts/
└── Root files
```

## Common Interview Questions

### Q1: Why did you choose a monorepo structure?

**Answer**: Monorepo provides:
- Shared dependencies
- Consistent tooling
- Easy cross-package changes
- Simplified CI/CD
- Better code sharing
- Atomic commits

### Q2: Why did you choose Turborepo?

**Answer**: Turborepo provides:
- Fast builds with caching
- Parallel task execution
- Dependency-aware builds
- Remote caching
- Incremental builds
- Better developer experience

### Q3: How do you manage shared code?

**Answer**: Shared code is placed in `libs/` directory:
- Shared types
- Shared utilities
- Shared constants
- Shared validators
- Imported by packages via workspace

## Exercises

### Exercise 1: Navigate Repository

**Task**: Navigate to specific files:
- Auth controller
- User service
- Prisma schema
- Docker Compose file

**Verification**:
- Found auth.controller.ts
- Found user.service.ts
- Found schema.prisma
- Found docker-compose.yml

### Exercise 2: Create New Service

**Task**: Create a new service in apps/ directory

**Steps**:
1. Create directory: apps/new-service/
2. Create package.json
3. Create src/main.ts
4. Add to workspace
5. Test build

**Verification**:
- Service builds successfully
- Service can be imported
- Service runs correctly

## Real Production Scenarios

### Scenario 1: Adding New Backend Service

**Situation**: Need to add a new backend service

**Steps**:
1. Create directory in apps/
2. Initialize package.json
3. Add to workspace
4. Implement service
5. Add to docker-compose.yml
6. Test deployment

### Scenario 2: Adding Shared Library

**Situation**: Need to share code between services

**Steps**:
1. Create directory in libs/
2. Initialize package.json
3. Add to workspace
4. Implement shared code
5. Import in services
6. Test integration

## Navigation

**Next Section**: [03-Technology-Stack](./03-Technology-Stack.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
