# University ERP - Complete Project Guide

## 🏗️ Project Architecture

This is a **monorepo** University ERP system with the following components:

### Core Components
- **`apps/core-api/`** - NestJS backend API (Port 3000)
- **`web/admin-portal/`** - React frontend admin portal (Port 5173)
- **`apps/cbe-engine/`** - Computer-based exam engine (Port 3001)
- **`apps/notification-worker/`** - Background notification service (Port 3002)
- **`apps/cert-generator/`** - Certificate generation service (Port 3003)

### Infrastructure Services (Docker)
- **PostgreSQL 16** - Database (Port 5432)
- **Redis 7** - Caching & sessions (Port 6379)
- **MinIO** - Object storage for files (Port 9000, Console: 9001)
- **Elasticsearch 8** - Search engine (Port 9200)
- **Nginx** - Reverse proxy (Port 80)

---

## 🚀 How to Start the Project

### Prerequisites
- **Node 20** installed
- **Docker & Docker Compose** installed
- **PostgreSQL 16 client tools** (`pg_dump`, `pg_restore`, `psql`)
- **PM2** globally installed (`npm i -g pm2`)

### Step 1: Environment Setup
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and fill in the required values:
# - POSTGRES_PASSWORD
# - MINIO_ROOT_USER & MINIO_ROOT_PASSWORD
# - MINIO_ACCESS_KEY & MINIO_SECRET_KEY
# - JWT_SECRET (generate with: openssl rand -hex 32)
# - UNIVERSITY_ID
```

### Step 2: Start Infrastructure Services
```bash
# Start Docker containers (PostgreSQL, Redis, MinIO, Elasticsearch)
docker compose up -d postgres redis minio elasticsearch

# Wait for services to be healthy (check with docker compose ps)
```

### Step 3: Install Dependencies
```bash
# Install root dependencies
npm install

# Install core-api dependencies
cd apps/core-api && npm install && cd ../..

# Install admin-portal dependencies
cd web/admin-portal && npm install && cd ../..
```

### Step 4: Database Setup
```bash
cd apps/core-api

# Option A: Fresh database with seed data
npx prisma db push --skip-generate
npx prisma generate
npx ts-node prisma/seed.ts              # university + super admin
node prisma/seed-settings.js            # settings + module access
node prisma/seed-subset/seed-subset.js  # curated data subset

# Option B: Restore from existing dump
# Use scripts/clone/clone-restore.sh as documented in docs/CLONE.md

cd ../..
```

### Step 5: Quick Start (Automated)
```bash
# Use the provided startup script
./start.sh

# This will:
# 1. Start Docker infrastructure
# 2. Start nginx
# 3. Start worker services (cbe-engine, notification-worker, cert-generator)
# 4. Start core-api via PM2
# 5. Start admin-portal via PM2
```

### Step 6: Manual Start (Alternative)
```bash
# Start core-api
cd apps/core-api
npm run build
pm2 start dist/main.js --name core-api
cd ../..

# Start admin-portal
cd web/admin-portal
pm2 start "npm run dev -- --host 0.0.0.0" --name admin-portal
cd ../..
```

---

## 📊 How to View Logs

### PM2 Logs (Application Services)
```bash
# View all logs
pm2 logs

# View specific service logs
pm2 logs core-api
pm2 logs admin-portal

# View logs in real-time with lines limit
pm2 logs --lines 100

# Clear logs
pm2 flush
```

### Docker Logs (Infrastructure Services)
```bash
# View all Docker logs
docker compose logs -f

# View specific service logs
docker compose logs -f postgres
docker compose logs -f redis
docker compose logs -f minio
docker compose logs -f elasticsearch

# View last 100 lines
docker compose logs --tail=100 postgres
```

### Log File Locations
- **Core API**: `/var/log/university-erp/core-api-error.log` & `/var/log/university-erp/core-api-out.log`
- **Admin Portal**: `/var/log/university-erp/portal-error.log` & `/var/log/university-erp/portal-out.log`
- **Nginx**: `./docker-volumes/nginx/logs/`

---

## 🔍 How to Check Status

### Quick Status Check
```bash
./status.sh
```

This shows:
- Docker container status
- PM2 process status
- Health checks for all services

### Manual Status Checks
```bash
# Docker containers
docker compose ps

# PM2 processes
pm2 list

# Health checks
curl http://localhost:3000/api/health        # Core API
curl http://localhost/api/health               # Nginx proxy
curl http://localhost:9000/minio/health/live   # MinIO
curl http://localhost:9200/_cluster/health     # Elasticsearch
```

---

## 🗄️ Database Structure & Communication

### Database Technology
- **PostgreSQL 16** as the primary database
- **Prisma ORM** for database access and migrations
- **Connection string**: `postgresql://erp_user:PASSWORD@postgres:5432/university_erp`

### Prisma Schema Location
- **Schema file**: `apps/core-api/prisma/schema.prisma`
- **Migrations**: `apps/core-api/prisma/migrations/`
- **Seed files**: `apps/core-api/prisma/seed-*.js`

### Key Database Models
- `University` - Top-level university entity
- `Institute` - Colleges/institutes under university
- `User` - System users with roles
- `Department` - Academic departments
- `Student` - Student profiles
- `FeeHead`, `FeeDemand` - Fee management
- `Question` - Exam question bank
- And many more (see schema.prisma)

### Backend Database Connection
**File**: `apps/core-api/src/database/prisma.service.ts`

```typescript
// PrismaService is a @Global() module available throughout the app
// It connects using DATABASE_URL from .env
// Includes audit middleware for tracking changes
```

### Database Operations Flow
1. **API Request** → NestJS Controller
2. **Controller** → Service (business logic)
3. **Service** → PrismaService (database access)
4. **PrismaService** → PostgreSQL (via Prisma Client)
5. **Response** → JSON back to frontend

---

## 🔌 Backend Architecture (core-api)

### Technology Stack
- **Framework**: NestJS (Node.js framework)
- **Language**: TypeScript
- **ORM**: Prisma
- **Authentication**: JWT (Passport.js)
- **Validation**: class-validator & Zod
- **API Documentation**: Swagger (dev only)

### Directory Structure
```
apps/core-api/src/
├── main.ts                 # Application entry point
├── app.module.ts           # Root module with all imports
├── common/                 # Shared utilities (guards, filters, decorators)
├── database/               # Prisma service & database module
├── health/                 # Health check endpoints
├── infrastructure/         # External services (Redis, MinIO, Vault)
├── modules/                # Feature modules (37 modules)
│   ├── auth/              # Authentication & authorization
│   ├── master-data/       # University, institute, department management
│   ├── admissions/        # Student admissions
│   ├── attendance/        # Attendance tracking
│   ├── fee/               # Fee management
│   ├── examination/       # Exams & assessments
│   ├── timetable/         # Class scheduling
│   ├── library/           # Library management
│   ├── hostel/            # Hostel management
│   ├── transport/         # Transport management
│   ├── hr/                # HR & staff management
│   ├── workflow/          # Workflow engine
│   └── [30 more modules...]
└── types/                  # TypeScript type definitions
```

### Key Backend Files
- **`main.ts`** - Bootstrap, CORS, middleware setup, Swagger docs
- **`app.module.ts`** - Root module with all 37 feature modules imported
- **`database/prisma.service.ts`** - Prisma client with audit middleware
- **`common/guards/global-jwt.guard.ts`** - Global JWT authentication
- **`common/filters/http-exception.filter.ts`** - Global error handling

### API Endpoints Structure
- **Base URL**: `http://localhost:3000/api`
- **Authentication**: Bearer JWT token in Authorization header
- **Public routes**: `/api/auth/login`, `/api/auth/forgot-password`, etc.
- **Protected routes**: All other routes require valid JWT
- **API Docs**: `http://localhost:3000/api/docs` (development only)

### Example API Flow
```
Frontend Request → Vite Proxy → Core API → Prisma → PostgreSQL
                    (port 5173)   (port 3000)
```

---

## 🎨 Frontend Architecture (admin-portal)

### Technology Stack
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite
- **Routing**: React Router v7
- **State Management**: @tanstack/react-query (server state)
- **Forms**: react-hook-form + Zod validation
- **UI Components**: Headless UI + Tailwind CSS
- **Rich Text**: Tiptap editor
- **Charts**: Recharts
- **PDF Generation**: jsPDF + jsPDF-autotable
- **Excel**: ExcelJS

### Directory Structure
```
web/admin-portal/src/
├── main.tsx                # React entry point
├── App.tsx                 # Root component with routing
├── api/                    # API client & endpoints
│   ├── axios.ts           # Axios instance with interceptors
│   ├── auth.ts            # Authentication API calls
│   └── modules.ts         # All module-specific API calls (146KB)
├── auth/                   # Authentication context & hooks
│   ├── AuthContext.tsx    # Auth state management
│   ├── useAuth.ts         # Auth hook
│   └── ProtectedRoute.tsx # Route protection component
├── components/             # Reusable UI components
├── pages/                  # Page components (43 pages)
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx
│   ├── MasterDataPage.tsx
│   ├── AdmissionsPage.tsx
│   └── [40 more pages...]
├── layouts/                # Layout components
│   └── AdminLayout.tsx    # Main admin layout with sidebar
├── lib/                    # Utility functions
│   ├── format.ts          # Date/number formatting
│   ├── excel.ts           # Excel export utilities
│   └── [PDF generation files]
├── config/                 # Configuration files
├── help/                   # Help center content
└── theme/                  # Theme context
```

### Key Frontend Files
- **`vite.config.ts`** - Vite configuration with API proxy
- **`src/api/axios.ts`** - Axios instance with auth interceptors & token refresh
- **`src/api/modules.ts`** - All API endpoint definitions (auto-generated from backend)
- **`src/App.tsx`** - React Router setup with all routes
- **`src/auth/AuthContext.tsx`** - Authentication state management

### API Communication
**File**: `web/admin-portal/src/api/axios.ts`

```typescript
// Axios instance configuration
const api = axios.create({ baseURL: '/api' })

// Request interceptor: Adds JWT token to every request
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('accessToken')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor: Handles 401 errors & token refresh
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    // Auto-refresh token on 401
    // Queue concurrent requests during refresh
    // Redirect to login on refresh failure
  }
)
```

### Frontend-Backend Communication Flow
```
User Action → React Component → API Call (axios) → Vite Proxy → Core API → Prisma → PostgreSQL
                                            ↓
                                    Response → React Query Cache → Component Re-render
```

### Vite Proxy Configuration
**File**: `web/admin-portal/vite.config.ts`
```typescript
server: {
  port: 5173,
  host: '0.0.0.0',
  proxy: {
    '/api': {
      target: 'http://localhost:3000',  // Forwards to core-api
      changeOrigin: true,
    }
  }
}
```

### Authentication Flow
1. **Login**: User enters credentials → `/api/auth/login` → Returns JWT tokens
2. **Token Storage**: 
   - `accessToken` → `sessionStorage` (short-lived, 15min)
   - `refreshToken` → `localStorage` (long-lived, 7 days)
3. **API Calls**: Axios interceptor adds `Authorization: Bearer {token}` header
4. **Token Refresh**: On 401 error, auto-refresh using refresh token
5. **Logout**: Clear tokens, redirect to login

---

## 🛠️ Development Workflow

### Making Backend Changes
```bash
# 1. Edit code in apps/core-api/src/
# 2. If schema changes: Edit apps/core-api/prisma/schema.prisma
# 3. Generate Prisma client
cd apps/core-api
npx prisma generate

# 4. Create migration (if schema changed)
npx prisma migrate dev --name migration_name

# 5. Build and restart
npm run build
pm2 restart core-api
```

### Making Frontend Changes
```bash
# 1. Edit code in web/admin-portal/src/
# 2. Vite hot-reloads automatically in dev mode
# 3. For production build:
cd web/admin-portal
npm run build
pm2 restart admin-portal
```

### Adding New API Endpoints
1. **Backend**: Create controller/service in appropriate module
2. **Frontend**: Add API call in `web/admin-portal/src/api/modules.ts`
3. **TypeScript**: Ensure types match between frontend and backend

---

## 📁 Important File Locations

### Configuration
- `.env` - Environment variables (gitignored)
- `.env.example` - Environment template
- `docker-compose.yml` - Docker services definition
- `package.json` - Root package.json
- `turbo.json` - Turborepo configuration

### Backend
- `apps/core-api/src/main.ts` - Backend entry point
- `apps/core-api/src/app.module.ts` - Root module
- `apps/core-api/prisma/schema.prisma` - Database schema
- `apps/core-api/package.json` - Backend dependencies

### Frontend
- `web/admin-portal/src/main.tsx` - Frontend entry point
- `web/admin-portal/src/App.tsx` - Root component with routes
- `web/admin-portal/vite.config.ts` - Vite configuration
- `web/admin-portal/package.json` - Frontend dependencies

### Scripts
- `start.sh` - Start all services
- `stop.sh` - Stop all services
- `status.sh` - Check service status
- `scripts/setup-hooks.sh` - Git hooks setup
- `scripts/sync-memory.sh` - Memory sync for Claude

### PM2 Configuration
- `ecosystem.native.config.js` - PM2 process configuration

---

## 🔐 Security Features

### Backend Security
- **Helmet.js** - Security headers
- **CORS** - Configured for frontend origin
- **Rate Limiting** - 300 requests/minute per IP (ThrottlerGuard)
- **JWT Authentication** - All routes protected by default
- **Password Hashing** - bcrypt for user passwords
- **Audit Logging** - All database changes tracked
- **Input Validation** - class-validator & Zod

### Frontend Security
- **Token Storage** - Access token in sessionStorage, refresh in localStorage
- **Auto Token Refresh** - Transparent token refresh on expiry
- **Route Protection** - ProtectedRoute component for authenticated routes
- **Error Boundaries** - Graceful error handling

---

## 📝 Common Tasks

### View Database Contents
```bash
# Connect to PostgreSQL
docker exec -it erp-postgres psql -U erp_user -d university_erp

# List tables
\dt

# Query data
SELECT * FROM users LIMIT 10;
```

### Reset Database
```bash
cd apps/core-api
# Drop all tables and recreate
npx prisma db push --force-reset
# Re-seed
npx ts-node prisma/seed.ts
```

### Check API Documentation
```bash
# In development, visit:
http://localhost:3000/api/docs
```

### Generate Prisma Client
```bash
cd apps/core-api
npx prisma generate
```

### Run Database Migrations
```bash
cd apps/core-api
# Development
npx prisma migrate dev

# Production
npx prisma migrate deploy
```

---

## 🐛 Troubleshooting

### Core API Not Starting
```bash
# Check logs
pm2 logs core-api

# Check database connection
docker compose ps postgres
curl http://localhost:5432

# Verify .env DATABASE_URL is correct
```

### Frontend Not Connecting to API
```bash
# Check if core-api is running
curl http://localhost:3000/api/health

# Check Vite proxy configuration in vite.config.ts
# Verify CORS settings in core-api/src/main.ts
```

### Database Connection Issues
```bash
# Check PostgreSQL container
docker compose logs postgres

# Verify DATABASE_URL in .env
# Ensure PostgreSQL is healthy
docker compose ps
```

### Port Already in Use
```bash
# Check what's using the port
lsof -i :3000  # core-api
lsof -i :5173  # admin-portal
lsof -i :5432  # postgres

# Kill process if needed
kill -9 <PID>
```

---

## 📚 Additional Documentation

- **`README.md`** - Git hooks and memory sync documentation
- **`docs/CLONE.md`** - How to clone a University ERP instance
- **`docs/memory/`** - Extensive module documentation and plans
- **`apps/core-api/prisma/MIGRATIONS.md`** - Database migration history

---

## 🎯 Quick Reference

### Service URLs
- **Core API**: http://localhost:3000/api
- **Admin Portal**: http://localhost:5173
- **MinIO Console**: http://localhost:9001
- **API Docs**: http://localhost:3000/api/docs (dev only)

### Key Commands
```bash
./start.sh              # Start all services
./stop.sh               # Stop all services
./status.sh             # Check status
pm2 logs                # View application logs
docker compose logs -f  # View infrastructure logs
```

### Module Count
- **Backend Modules**: 37 feature modules
- **Frontend Pages**: 43 page components
- **Database Models**: 100+ Prisma models

---

This guide covers everything you need to understand and work with the University ERP system. For specific module details, refer to the documentation in `docs/memory/`.
