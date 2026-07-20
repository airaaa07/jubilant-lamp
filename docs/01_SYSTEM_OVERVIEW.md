# University ERP - System Overview

## Purpose

University ERP is a comprehensive university management system designed to handle all aspects of university operations including:

- Student lifecycle management (admissions, enrollment, academics)
- Staff and faculty management
- Financial operations (fees, payments, scholarships)
- Infrastructure management (hostel, transport, library)
- Examination system (computer-based exams with proctoring)
- Document generation and management
- Workflow-based approval processes
- Communication (notifications, notices, counselling)

## Architecture Type

**Monolithic Microservices**: The system uses a monorepo structure with multiple independent services that share code through a workspace configuration:

- **core-api**: Main REST API server (NestJS)
- **cbe-engine**: Real-time exam engine with WebSockets (NestJS)
- **notification-worker**: Background email/SMS worker (NestJS)
- **cert-generator**: Certificate generation service (NestJS)
- **admin-portal**: React admin interface

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Nginx (Port 80)                          │
│                    Reverse Proxy / Load Balancer                  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Admin Portal  │  │    Core API     │  │   CBE Engine    │
│  (React/Vite)  │  │   (NestJS)      │  │  (NestJS/WS)    │
│   Port 5173    │  │    Port 3000    │  │    Port 3001    │
└────────────────┘  └─────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ Notification   │  │ Cert Generator  │  │  PostgreSQL     │
│   Worker       │  │   (Puppeteer)   │  │    Port 5432    │
│   Port 3002    │  │    Port 3003    │  └─────────────────┘
└────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│     Redis      │  │     MinIO       │  │  Elasticsearch  │
│   Port 6379    │  │   Port 9000     │  │    Port 9200    │
└────────────────┘  └─────────────────┘  └─────────────────┘
```

## Multi-Tenancy Model

The system supports **university-level multi-tenancy**:

1. **University**: Top-level entity (e.g., "State University")
2. **Institute**: Individual colleges under a university (e.g., "Engineering College")
3. **Department**: Academic departments within institutes

Each university can have multiple institutes, and each institute has its own departments, students, staff, and configuration while sharing the same database.

## Key Design Patterns

### 1. Module-Based Architecture

The backend is organized into 36 independent NestJS modules, each with:
- Controller (API endpoints)
- Service (business logic)
- DTOs (data validation)
- Guards (authorization)

### 2. Versioned Academic Configuration

Academic rules (grading, attendance, passing criteria) are versioned using:
- **StreamLabel**: Versioned academic program rules
- **SubjectLabel**: Versioned subject-specific rules

Once a batch/term is frozen, it uses the frozen version of these rules, ensuring consistency even if rules change later.

### 3. Generic Workflow Engine

A configurable workflow system handles approval processes:
- WorkflowDefinition: State machine configuration
- WorkflowInstance: Running workflow instances
- WorkflowTask: Per-actor tasks
- WorkflowReservation: Resource holds (seats, hostel, transport)

### 4. Audit Trail

Automatic audit logging via Prisma middleware:
- Field-level change tracking
- Actor attribution (who made the change)
- Sensitive field redaction
- Configurable model denylist

### 5. Role-Based Access Control (RBAC)

- **Application Roles**: High-level roles (Student, TeachingFaculty, AdminStaff, etc.)
- **Scope Roles**: Module-specific permissions
- **Multi-Role Assignment**: Users can hold multiple roles with different scopes

## Data Flow Patterns

### Request Flow

```
React Component
    ↓
API Call (axios)
    ↓
Controller (NestJS)
    ↓
Guard (JWT + Scope)
    ↓
DTO Validation (Zod)
    ↓
Service (Business Logic)
    ↓
Repository (Prisma)
    ↓
Database (PostgreSQL)
    ↓
Response
```

### Background Job Flow

```
Service
    ↓
Queue Job (Bull)
    ↓
Redis Queue
    ↓
Worker Process
    ↓
External Service (Email/SMS)
    ↓
Completion Callback
```

### Exam Flow (CBE)

```
React Exam Interface
    ↓
WebSocket Connection (CBE Engine)
    ↓
Real-time Events (answers, proctoring)
    ↓
Exam Attempt Recording
    ↓
Auto-grading
    ↓
Result Publication
```

## Technology Rationale

### NestJS for Backend

- **Modular architecture**: Clean separation of concerns
- **Dependency injection**: Easy testing and maintenance
- **TypeScript**: Type safety at compile time
- **Extensive ecosystem**: Guards, interceptors, schedulers

### React 19 for Frontend

- **Component-based**: Reusable UI components
- **Modern hooks**: useState, useEffect, useContext
- **Rich ecosystem**: React Query, TipTap, Recharts
- **Performance**: Vite for fast development and builds

### Prisma for Database

- **Type-safe**: Generated TypeScript types
- **Migrations**: Version-controlled schema changes
- **Relations**: Easy navigation of related data
- **Middleware**: Audit logging and hooks

### PostgreSQL for Database

- **ACID compliance**: Reliable transactions
- **JSON support**: Flexible configuration storage
- **Full-text search**: Built-in search capabilities
- **Mature ecosystem**: Tools and extensions

### Redis for Caching

- **In-memory**: Fast read/write operations
- **Session storage**: JWT refresh tokens
- **Pub/Sub**: Real-time notifications
- **Persistence**: Optional disk backup

### MinIO for Storage

- **S3-compatible**: Drop-in replacement for AWS S3
- **Self-hosted**: No external dependencies
- **Multi-bucket**: Separate document and exam storage
- **Azure fallback**: Cloud deployment support

### Bull for Queues

- **Redis-backed**: Leverages existing Redis
- **Reliable**: Job persistence and retries
- **Dashboard**: UI for monitoring queues
- **Scheduled jobs**: Cron-like functionality

## Security Model

### Authentication

- **JWT tokens**: Short-lived access tokens (15 min)
- **Refresh tokens**: Long-lived refresh tokens (7 days)
- **Password hashing**: bcrypt with salt
- **Account lockout**: Failed login tracking
- **Password policy**: Configurable complexity rules

### Authorization

- **Global JWT guard**: Fail-closed by default
- **Public decorator**: Opt-out for specific routes
- **Scope guard**: Module-level permissions
- **Role checks**: Service-level authorization

### Rate Limiting

- **Global default**: 300 requests/minute/IP
- **Sensitive routes**: Tighter limits (login: 5/min)
- **Per-route overrides**: @Throttle decorator

### Data Protection

- **Audit logging**: All writes tracked
- **Sensitive redaction**: Passwords, tokens redacted
- **Null byte stripping**: PostgreSQL compatibility
- **CORS**: Configured origin whitelist
- **Helmet**: Security headers

## Scalability Considerations

### Horizontal Scaling

- **Stateless API**: Core API can be scaled horizontally
- **Session storage**: Redis for shared sessions
- **Database connection pooling**: Prisma connection limits
- **Queue workers**: Multiple worker instances

### Vertical Scaling

- **Database indexing**: Strategic indexes on foreign keys
- **Query optimization**: Prisma query optimization
- **Caching**: Redis for frequently accessed data
- **Lazy loading**: React code splitting

### Performance Optimizations

- **React lazy loading**: Route-based code splitting
- **Image optimization**: MinIO presigned URLs
- **Database denormalization**: Cached computed fields
- **Batch operations**: Bulk inserts/updates

## Deployment Model

### Development

- **Docker Compose**: All services in containers
- **Hot reload**: NestJS watch mode, Vite HMR
- **Volume mounts**: Live code editing
- **Environment variables**: .env file

### Production

- **PM2**: Process management for core-api
- **Docker**: Containerized services
- **Azure Blob**: Cloud storage fallback
- **Health checks**: Service monitoring

### Infrastructure Services

- **PostgreSQL**: Primary database
- **Redis**: Cache and queue backend
- **MinIO**: Object storage
- **Elasticsearch**: Search engine
- **Nginx**: Reverse proxy

## Integration Points

### External Services

- **Email**: SMTP (Nodemailer)
- **SMS**: SMS gateway integration
- **Payment**: Razorpay integration
- **Cloud Storage**: Azure Blob (optional)
- **Secret Management**: AWS Secrets Manager, Azure Key Vault, Google Secret Manager

### Internal Services

- **CBE Engine**: WebSocket-based exam delivery
- **Notification Worker**: Async email/SMS sending
- **Certificate Generator**: PDF generation with Puppeteer
- **Core API**: Central business logic

## Monitoring and Observability

### Health Checks

- **Core API**: /health endpoint
- **Database**: Connection health
- **Redis**: Ping check
- **MinIO**: Bucket existence check
- **Elasticsearch**: Cluster health

### Logging

- **Application logs**: NestJS logger
- **Audit logs**: Database audit trail
- **Error tracking**: Global exception filter
- **Request context**: Per-request actor tracking

### Metrics

- **API performance**: Response times
- **Queue metrics**: Job processing stats
- **Database metrics**: Query performance
- **Cache hit rates**: Redis efficiency

## Development Workflow

### Code Organization

- **Monorepo**: Single repository for all services
- **Workspaces**: npm workspaces for shared packages
- **Turbo**: Build system for monorepo
- **TypeScript**: Strict type checking

### Testing Strategy

- **Unit tests**: Jest for services
- **Integration tests**: API endpoint tests
- **E2E tests**: (Not extensively implemented)
- **Manual testing**: QA through admin portal

### Deployment Pipeline

- **Build**: Docker image creation
- **Push**: Container registry
- **Deploy**: Docker Compose or Kubernetes
- **Migrate**: Prisma migrations
- **Seed**: Initial data seeding

## Known Limitations

1. **Student Portal**: Placeholder exists, not fully implemented
2. **Elasticsearch**: Configured but usage not deeply explored
3. **Worker Queues**: Minimal implementation in some workers
4. **Testing**: Limited automated test coverage
5. **Mobile**: No mobile app (web-only)

## Future Extensibility

The system is designed for:

- **New modules**: Easy addition of NestJS modules
- **Custom workflows**: Configurable workflow engine
- **Multi-tenant**: Additional universities/institutes
- **Plugin architecture**: Service-based design
- **API-first**: REST API for external integrations
