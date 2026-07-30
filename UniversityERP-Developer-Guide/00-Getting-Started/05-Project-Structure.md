# Project Structure

## Overview

This document provides a comprehensive overview of the University ERP project structure. It details the organization of the monorepo, the relationship between different applications, and the purpose of each directory and file.

## Monorepo Architecture

**Confirmed by Code**: The University ERP uses a monorepo architecture with Turborepo for build orchestration.

**Monorepo Structure:**
```
UniversityERP/
├── apps/                    # Application packages
│   ├── core-api/           # Core NestJS API application
│   └── cbe-engine/         # CBE (Curriculum Based Education) Engine
├── web/                     # Web applications
│   ├── admin-portal/       # React admin portal
│   └── student-portal/     # React student portal
├── libs/                    # Shared libraries
│   ├── common/             # Common utilities and types
│   ├── ui/                 # Shared UI components
│   └── config/             # Shared configuration
├── docker/                  # Docker configurations
│   ├── core-api/           # Core API Dockerfile
│   ├── admin-portal/       # Admin portal Dockerfile
│   └── postgres/           # PostgreSQL configuration
├── docs/                    # Documentation
├── scripts/                 # Build and deployment scripts
├── docker-compose.yml      # Docker Compose configuration
├── package.json            # Root package.json
├── turbo.json              # Turborepo configuration
└── tsconfig.json           # Root TypeScript configuration
```

## Directory Structure Details

### apps/ Directory

**Purpose**: Contains all application packages.

**Structure**:
```
apps/
├── core-api/
│   ├── src/
│   │   ├── auth/           # Authentication module
│   │   ├── users/          # Users module
│   │   ├── students/       # Students module
│   │   ├── courses/        # Courses module
│   │   ├── attendance/     # Attendance module
│   │   ├── exams/          # Exams module
│   │   ├── fees/           # Fees module
│   │   ├── library/        # Library module
│   │   ├── hostel/         # Hostel module
│   │   ├── transport/      # Transport module
│   │   ├── workflow/       # Workflow module
│   │   ├── common/         # Common utilities
│   │   ├── config/         # Configuration
│   │   ├── prisma/         # Prisma schema and migrations
│   │   ├── main.ts         # Application entry point
│   │   └── app.module.ts   # Root module
│   ├── test/               # Test files
│   ├── prisma/             # Prisma schema
│   │   ├── schema.prisma   # Database schema
│   │   └── seed.ts         # Database seed
│   ├── Dockerfile          # Docker configuration
│   ├── package.json        # Dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   ├── nest-cli.json       # NestJS CLI configuration
│   └── .env                # Environment variables
└── cbe-engine/
    ├── src/
    │   ├── engine/         # CBE engine logic
    │   ├── rules/          # CBE rules
    │   ├── calculations/    # CBE calculations
    │   └── main.ts         # Entry point
    ├── test/
    ├── package.json
    └── tsconfig.json
```

**core-api Structure Details:**

**Confirmed by Code**: The core-api follows NestJS module architecture.

**Module Structure**:
```
src/
├── auth/                   # Authentication module
│   ├── auth.controller.ts
│   ├── auth.service.ts
│   ├── auth.module.ts
│   ├── guards/
│   │   ├── jwt-auth.guard.ts
│   │   └── local-auth.guard.ts
│   ├── strategies/
│   │   ├── jwt.strategy.ts
│   │   └── local.strategy.ts
│   └── dto/
│       ├── login.dto.ts
│       └── register.dto.ts
├── users/                  # Users module
│   ├── users.controller.ts
│   ├── users.service.ts
│   ├── users.module.ts
│   └── dto/
│       ├── create-user.dto.ts
│       └── update-user.dto.ts
├── students/               # Students module
│   ├── students.controller.ts
│   ├── students.service.ts
│   ├── students.module.ts
│   └── dto/
├── courses/                # Courses module
│   ├── courses.controller.ts
│   ├── courses.service.ts
│   ├── courses.module.ts
│   └── dto/
├── attendance/             # Attendance module
│   ├── attendance.controller.ts
│   ├── attendance.service.ts
│   ├── attendance.module.ts
│   └── dto/
├── exams/                  # Exams module
│   ├── exams.controller.ts
│   ├── exams.service.ts
│   ├── exams.module.ts
│   └── dto/
├── fees/                   # Fees module
│   ├── fees.controller.ts
│   ├── fees.service.ts
│   ├── fees.module.ts
│   └── dto/
├── library/                # Library module
│   ├── library.controller.ts
│   ├── library.service.ts
│   ├── library.module.ts
│   └── dto/
├── hostel/                 # Hostel module
│   ├── hostel.controller.ts
│   ├── hostel.service.ts
│   ├── hostel.module.ts
│   └── dto/
├── transport/              # Transport module
│   ├── transport.controller.ts
│   ├── transport.service.ts
│   ├── transport.module.ts
│   └── dto/
├── workflow/               # Workflow module
│   ├── workflow.controller.ts
│   ├── workflow.service.ts
│   ├── workflow.module.ts
│   └── dto/
├── common/                 # Common utilities
│   ├── decorators/
│   ├── filters/
│   ├── interceptors/
│   ├── pipes/
│   └── guards/
├── config/                 # Configuration
│   ├── database.config.ts
│   ├── redis.config.ts
│   └── minio.config.ts
├── prisma/                 # Prisma service
│   └── prisma.service.ts
├── main.ts                 # Application entry point
└── app.module.ts           # Root module
```

 web/ Directory

**Purpose**: Contains all web application packages.

**Structure**:
```
web/
├── admin-portal/
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   │   ├── common/     # Common components
│   │   │   ├── layout/     # Layout components
│   │   │   └── forms/      # Form components
│   │   ├── pages/          # Page components
│   │   │   ├── auth/       # Auth pages
│   │   │   ├── dashboard/  # Dashboard pages
│   │   │   ├── students/   # Student pages
│   │   │   ├── courses/    # Course pages
│   │   │   ├── attendance/ # Attendance pages
│   │   │   ├── exams/      # Exam pages
│   │   │   ├── fees/       # Fee pages
│   │   │   ├── library/    # Library pages
│   │   │   ├── hostel/     # Hostel pages
│   │   │   └── transport/  # Transport pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── context/        # React context
│   │   ├── services/       # API services
│   │   ├── utils/          # Utility functions
│   │   ├── types/          # TypeScript types
│   │   ├── constants/      # Constants
│   │   ├── App.tsx         # Root component
│   │   └── main.tsx        # Entry point
│   ├── public/             # Static assets
│   ├── index.html          # HTML template
│   ├── vite.config.ts      # Vite configuration
│   ├── tsconfig.json       # TypeScript configuration
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   ├── package.json        # Dependencies
│   └── .env                # Environment variables
└── student-portal/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── hooks/
    │   ├── context/
    │   ├── services/
    │   ├── utils/
    │   ├── types/
    │   ├── constants/
    │   ├── App.tsx
    │   └── main.tsx
    ├── public/
    ├── index.html
    ├── vite.config.ts
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── package.json
    └── .env
```

**admin-portal Structure Details:**

**Confirmed by Code**: The admin-portal follows React component architecture.

**Component Structure**:
```
src/
├── components/
│   ├── common/
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Modal/
│   │   ├── Table/
│   │   ├── Card/
│   │   ├── Badge/
│   │   ├── Avatar/
│   │   └── Spinner/
│   ├── layout/
│   │   ├── Header/
│   │   ├── Sidebar/
│   │   ├── Footer/
│   │   └── Layout/
│   └── forms/
│       ├── LoginForm/
│       ├── UserForm/
│       ├── StudentForm/
│       └── CourseForm/
├── pages/
│   ├── auth/
│   │   ├── LoginPage/
│   │   ├── RegisterPage/
│   │   └── ForgotPasswordPage/
│   ├── dashboard/
│   │   ├── DashboardPage/
│   │   ├── AnalyticsPage/
│   │   └── ReportsPage/
│   ├── students/
│   │   ├── StudentsListPage/
│   │   ├── StudentDetailPage/
│   │   ├── StudentCreatePage/
│   │   └── StudentEditPage/
│   ├── courses/
│   │   ├── CoursesListPage/
│   │   ├── CourseDetailPage/
│   │   ├── CourseCreatePage/
│   │   └── CourseEditPage/
│   ├── attendance/
│   │   ├── AttendanceListPage/
│   │   ├── AttendanceMarkPage/
│   │   └── AttendanceReportPage/
│   ├── exams/
│   │   ├── ExamsListPage/
│   │   ├── ExamDetailPage/
│   │   ├── ExamCreatePage/
│   │   └── ExamEditPage/
│   ├── fees/
│   │   ├── FeesListPage/
│   │   ├── FeeDetailPage/
│   │   ├── FeeCreatePage/
│   │   └── FeeEditPage/
│   ├── library/
│   │   ├── BooksListPage/
│   │   ├── BookDetailPage/
│   │   ├── BookIssuePage/
│   │   └── BookReturnPage/
│   ├── hostel/
│   │   ├── HostelsListPage/
│   │   ├── HostelDetailPage/
│   │   ├── RoomAllocationPage/
│   │   └── RoomVacancyPage/
│   └── transport/
│       ├── RoutesListPage/
│       ├── RouteDetailPage/
│       ├── PassIssuePage/
│       └── PassRenewalPage/
├── hooks/
│   ├── useAuth.ts
│   ├── useUsers.ts
│   ├── useStudents.ts
│   ├── useCourses.ts
│   ├── useAttendance.ts
│   ├── useExams.ts
│   ├── useFees.ts
│   ├── useLibrary.ts
│   ├── useHostel.ts
│   └── useTransport.ts
├── context/
│   ├── AuthContext.tsx
│   ├── ThemeContext.tsx
│   └── NotificationContext.tsx
├── services/
│   ├── api.ts
│   ├── auth.ts
│   ├── users.ts
│   ├── students.ts
│   ├── courses.ts
│   ├── attendance.ts
│   ├── exams.ts
│   ├── fees.ts
│   ├── library.ts
│   ├── hostel.ts
│   └── transport.ts
├── utils/
│   ├── formatters.ts
│   ├── validators.ts
│   ├── helpers.ts
│   └── constants.ts
├── types/
│   ├── auth.ts
│   ├── user.ts
│   ├── student.ts
│   ├── course.ts
│   ├── attendance.ts
│   ├── exam.ts
│   ├── fee.ts
│   ├── library.ts
│   ├── hostel.ts
│   └── transport.ts
├── constants/
│   ├── routes.ts
│   ├── permissions.ts
│   └── config.ts
├── App.tsx
└── main.tsx
```

### libs/ Directory

**Purpose**: Contains shared libraries used across applications.

**Structure**:
```
libs/
├── common/
│   ├── src/
│   │   ├── types/          # Shared TypeScript types
│   │   ├── utils/          # Shared utility functions
│   │   ├── constants/      # Shared constants
│   │   ├── validators/     # Shared validators
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
├── ui/
│   ├── src/
│   │   ├── components/     # Shared UI components
│   │   ├── styles/         # Shared styles
│   │   ├── themes/         # Shared themes
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
└── config/
    ├── src/
    │   ├── database/       # Database configuration
    │   ├── redis/          # Redis configuration
    │   ├── minio/          # MinIO configuration
    │   └── index.ts
    ├── package.json
    └── tsconfig.json
```

### docker/ Directory

**Purpose**: Contains Docker configurations for different services.

**Structure**:
```
docker/
├── core-api/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
├── admin-portal/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
├── student-portal/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   └── .dockerignore
├── postgres/
│   ├── Dockerfile
│   └── init.sql
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

### docs/ Directory

**Purpose**: Contains project documentation.

**Structure**:
```
docs/
├── api/                    # API documentation
├── architecture/           # Architecture documentation
├── deployment/             # Deployment documentation
├── development/            # Development documentation
└── user/                   # User documentation
```

### scripts/ Directory

**Purpose**: Contains build and deployment scripts.

**Structure**:
```
scripts/
├── build.sh                # Build script
├── deploy.sh               # Deployment script
├── test.sh                 # Test script
├── lint.sh                 # Lint script
└── migrate.sh              # Database migration script
```

## Key Configuration Files

### Root Configuration Files

**package.json**:
```json
{
  "name": "university-erp",
  "version": "1.0.0",
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
    "test": "turbo run test",
    "clean": "turbo run clean"
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "typescript": "^5.0.0"
  },
  "packageManager": "npm@9.0.0"
}
```

**turbo.json**:
```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
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

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    container_name: university-erp-db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: university_erp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: university-erp-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio:latest
    container_name: university-erp-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

### Core API Configuration Files

**nest-cli.json**:
```json
{
  "$schema": "https://json.schemastore.org/nest-cli",
  "collection": "@nestjs/schematics",
  "sourceRoot": "src",
  "compilerOptions": {
    "deleteOutDir": true,
    "webpack": true,
    "tsConfigPath": "tsconfig.json"
  }
}
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "module": "commonjs",
    "declaration": true,
    "removeComments": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "allowSyntheticDefaultImports": true,
    "target": "ES2021",
    "sourceMap": true,
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": true,
    "skipLibCheck": true,
    "strictNullChecks": false,
    "noImplicitAny": false,
    "strictBindCallApply": false,
    "forceConsistentCasingInFileNames": false,
    "noFallthroughCasesInSwitch": false
  }
}
```

### Admin Portal Configuration Files

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
});
```

**tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## File Naming Conventions

### Backend File Naming

**Confirmed by Code**: Backend follows NestJS naming conventions.

**Conventions**:
- Controllers: `*.controller.ts`
- Services: `*.service.ts`
- Modules: `*.module.ts`
- DTOs: `*.dto.ts`
- Entities: `*.entity.ts`
- Guards: `*.guard.ts`
- Interceptors: `*.interceptor.ts`
- Pipes: `*.pipe.ts`
- Filters: `*.filter.ts`
- Decorators: `*.decorator.ts`

**Examples**:
- `auth.controller.ts`
- `auth.service.ts`
- `auth.module.ts`
- `login.dto.ts`
- `user.entity.ts`
- `jwt-auth.guard.ts`
- `logging.interceptor.ts`
- `validation.pipe.ts`
- `http-exception.filter.ts`
- `roles.decorator.ts`

### Frontend File Naming

**Confirmed by Code**: Frontend follows React naming conventions.

**Conventions**:
- Components: PascalCase with `/*` suffix
- Pages: PascalCase with `Page` suffix
- Hooks: camelCase with `use` prefix
- Context: PascalCase with `Context` suffix
- Services: camelCase with `.ts` extension
- Types: PascalCase with `.types.ts` extension
- Utils: camelCase with `.ts` extension

**Examples**:
- `Button/`
- `DashboardPage/`
- `useAuth.ts`
- `AuthContext.tsx`
- `auth.ts`
- `user.types.ts`
- `formatters.ts`

## Import Paths

### Backend Import Paths

**Confirmed by Code**: Backend uses relative imports for modules.

**Examples**:
```typescript
// Import from same module
import { AuthService } from './auth.service';

// Import from different module
import { UsersService } from '../users/users.service';

// Import from common
import { Logger } from '@nestjs/common';

// Import from shared library
import { User } from '@university-erp/common';
```

### Frontend Import Paths

**Confirmed by Code**: Frontend uses absolute imports with `@` alias.

**Examples**:
```typescript
// Import from components
import { Button } from '@/components/common/Button';

// Import from pages
import { DashboardPage } from '@/pages/dashboard/DashboardPage';

// Import from hooks
import { useAuth } from '@/hooks/useAuth';

// Import from services
import { authService } from '@/services/auth';

// Import from types
import { User } from '@/types/user';
```

## Module Dependencies

### Core API Module Dependencies

**Confirmed by Code**: Core API modules have specific dependencies.

**Module Dependency Graph**:
```
app.module.ts
├── auth.module
├── users.module
├── students.module
├── courses.module
├── attendance.module
├── exams.module
├── fees.module
├── library.module
├── hostel.module
├── transport.module
└── workflow.module
```

**Dependencies**:
- `auth.module` depends on `users.module`
- `students.module` depends on `courses.module`
- `attendance.module` depends on `students.module` and `courses.module`
- `exams.module` depends on `students.module` and `courses.module`
- `fees.module` depends on `students.module`
- `library.module` depends on `students.module`
- `hostel.module` depends on `students.module`
- `transport.module` depends on `students.module`
- `workflow.module` depends on all other modules

### Admin Portal Component Dependencies

**Confirmed by Code**: Admin portal components have specific dependencies.

**Component Dependency Graph**:
```
App.tsx
├── Layout/
│   ├── Header/
│   ├── Sidebar/
│   └── Footer/
├── Pages/
│   ├── Auth Pages/
│   ├── Dashboard Pages/
│   ├── Student Pages/
│   ├── Course Pages/
│   ├── Attendance Pages/
│   ├── Exam Pages/
│   ├── Fee Pages/
│   ├── Library Pages/
│   ├── Hostel Pages/
│   └── Transport Pages/
└── Components/
    ├── Common Components/
    ├── Layout Components/
    └── Form Components/
```

## Next Steps

After understanding the project structure:

1. **Explore the Codebase**: Start exploring specific modules
2. **Read Module Documentation**: Read module-specific documentation
3. **Start Development**: Start building features
4. **Contribute**: Contribute to the project

## Additional Resources

- [NestJS Documentation](https://docs.nestjs.com/)
- [React Documentation](https://react.dev/)
- [Turborepo Documentation](https://turbo.build/repo/docs)
- [Monorepo Best Practices](https://monorepo.tools/)
