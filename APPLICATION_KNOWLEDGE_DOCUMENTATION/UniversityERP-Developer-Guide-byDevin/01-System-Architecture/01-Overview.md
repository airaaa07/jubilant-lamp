# System Architecture Overview

## Overview

This document provides a comprehensive overview of the University ERP system architecture. It details the high-level design, technology choices, architectural patterns, and system components.

## Architecture Summary

**Confirmed by Code**: The University ERP follows a microservices-inspired monorepo architecture with clear separation of concerns.

**Architecture Type:**
- **Pattern**: Modular Monolith with Microservices-ready design
- **Style**: Layered Architecture with Domain-Driven Design principles
- **Deployment**: Containerized with Docker, orchestrated with Kubernetes
- **Communication**: REST API with WebSocket for real-time features

## High-Level Architecture

**System Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  Admin Portal (React)    Student Portal (React)                │
│  - Staff Management      - Student Dashboard                   │
│  - Course Management     - Attendance View                     │
│  - Exam Management       - Results View                        │
│  - Fee Management       - Fee Payment                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway / Load Balancer                 │
├─────────────────────────────────────────────────────────────────┤
│  Nginx / Kong                                                    │
│  - Request Routing                                               │
│  - SSL Termination                                               │
│  - Rate Limiting                                                 │
│  - Authentication                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                           │
├─────────────────────────────────────────────────────────────────┤
│  Core API (NestJS)                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Auth Module  │  │ User Module  │  │ Student Mod  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Course Mod   │  │ Attendance   │  │ Exam Module  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Fee Module   │  │ Library Mod  │  │ Hostel Mod   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Transport    │  │ Workflow     │  │ CBE Engine   │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Layer                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ PostgreSQL   │  │ Redis        │  │ MinIO        │           │
│  │ - Primary DB │  │ - Cache      │  │ - Files      │           │
│  │ - Relations  │  │ - Queue      │  │ - Documents  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Infrastructure Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  Docker / Kubernetes                                             │
│  - Container Orchestration                                      │
│  - Service Discovery                                             │
│  - Auto Scaling                                                  │
│  - Health Checks                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend Technologies

**Confirmed by Code**: The backend uses modern, production-ready technologies.

**Core Technologies:**
- **Framework**: NestJS (Node.js framework)
- **Language**: TypeScript
- **Runtime**: Node.js 18+ (LTS)
- **Database**: PostgreSQL 14+
- **ORM**: Prisma
- **Cache**: Redis 7+
- **Queue**: Bull (Redis-based)
- **Storage**: MinIO (S3-compatible)
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: class-validator
- **Logging**: Winston
- **Testing**: Jest, Supertest

**Why These Technologies:**

**NestJS:**
- Provides a robust architecture out of the box
- Built-in dependency injection
- Modular structure
- Excellent TypeScript support
- Large ecosystem and community
- Easy to test

**TypeScript:**
- Type safety
- Better developer experience
- Catch errors at compile time
- Better IDE support
- Self-documenting code

**PostgreSQL:**
- ACID compliance
- Advanced features (JSON, arrays, etc.)
- Excellent performance
- Strong community support
- Full-text search capabilities

**Prisma:**
- Type-safe database access
- Auto-generated TypeScript types
- Excellent developer experience
- Migration management
- Query builder

**Redis:**
- In-memory for high performance
- Support for multiple data structures
- Built-in persistence options
- Pub/Sub messaging
- Transaction support

### Frontend Technologies

**Confirmed by Code**: The frontend uses modern React-based technologies.

**Core Technologies:**
- **Framework**: React 18+
- **Language**: TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: React Context, React Query
- **Routing**: React Router
- **HTTP Client**: Axios
- **Forms**: React Hook Form
- **Validation**: Zod
- **Testing**: React Testing Library, Playwright
- **UI Components**: Custom components with shadcn/ui patterns

**Why These Technologies:**

**React:**
- Component-based architecture
- Large ecosystem
- Excellent performance
- Strong community
- Easy to learn and use

**Vite:**
- Fast development server
- Instant HMR
- Optimized builds
- Modern tooling

**Tailwind CSS:**
- Utility-first CSS
- Highly customizable
- Small bundle size
- Easy to maintain
- Consistent design

**React Query:**
- Server state management
- Caching and synchronization
- Background updates
- Optimistic updates
- Excellent TypeScript support

### DevOps Technologies

**Confirmed by Code**: The project uses containerization and orchestration.

**Core Technologies:**
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana
- **Logging**: Winston, ELK Stack
- **Reverse Proxy**: Nginx
- **Load Balancer**: Nginx, HAProxy

## Architectural Patterns

### Layered Architecture

**Confirmed by Code**: The system follows a layered architecture pattern.

**Layers:**

1. **Presentation Layer**
   - Controllers (NestJS)
   - Components (React)
   - DTOs (Data Transfer Objects)

2. **Business Logic Layer**
   - Services (NestJS)
   - Hooks (React)
   - Domain logic

3. **Data Access Layer**
   - Prisma ORM
   - Repository pattern
   - Data models

4. **Infrastructure Layer**
   - Database connections
   - External services
   - File storage

**Benefits:**
- Separation of concerns
- Easy to test
- Easy to maintain
- Scalable

### Modular Architecture

**Confirmed by Code**: The system is organized into modules.

**Module Structure:**

```
apps/core-api/src/
├── auth/              # Authentication module
├── users/             # Users module
├── students/          # Students module
├── courses/           # Courses module
├── attendance/        # Attendance module
├── exams/             # Exams module
├── fees/              # Fees module
├── library/           # Library module
├── hostel/            # Hostel module
├── transport/         # Transport module
├── workflow/          # Workflow module
└── common/            # Common utilities
```

**Module Benefits:**
- Clear boundaries
- Easy to understand
- Easy to test
- Easy to scale
- Team collaboration

### Repository Pattern

**Confirmed by Code**: The system uses the repository pattern for data access.

**Repository Implementation:**

```typescript
@Injectable()
export class UserRepository {
  constructor(private prisma: PrismaService) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async create(data: CreateUserDto): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserDto): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<User> {
    return this.prisma.user.delete({
      where: { id },
    });
  }
}
```

**Benefits:**
- Abstraction over data access
- Easy to test
- Easy to swap data source
- Centralized query logic

### Dependency Injection

**Confirmed by Code**: NestJS uses dependency injection extensively.

**DI Example:**

```typescript
@Module({
  imports: [PrismaModule],
  controllers: [UsersController],
  providers: [UsersService, UserRepository],
  exports: [UsersService],
})
export class UsersModule {}

@Injectable()
export class UsersService {
  constructor(
    private userRepository: UserRepository,
    private cacheService: CacheService,
  ) {}
}
```

**Benefits:**
- Loose coupling
- Easy to test
- Easy to maintain
- Clear dependencies

## Communication Patterns

### REST API

**Confirmed by Code**: The system uses REST API for communication.

**API Design:**
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes
- JSON format
- Versioning

**Example Endpoints:**
```
GET    /api/users         - List users
GET    /api/users/:id     - Get user
POST   /api/users         - Create user
PUT    /api/users/:id     - Update user
DELETE /api/users/:id     - Delete user
```

### WebSocket

**Confirmed by Code**: The system uses WebSocket for real-time features.

**WebSocket Use Cases:**
- Real-time notifications
- Live attendance updates
- Real-time exam results
- Live chat

**WebSocket Implementation:**

```typescript
@WebSocketGateway()
export class NotificationsGateway {
  @WebSocketServer()
  server: Server;

  @SubscribeMessage('subscribe')
  handleSubscribe(client: Socket, userId: string) {
    client.join(`user:${userId}`);
  }

  sendNotification(userId: string, notification: any) {
    this.server.to(`user:${userId}`).emit('notification', notification);
  }
}
```

### Event-Driven Architecture

**Confirmed by Code**: The system uses events for decoupled communication.

**Event Implementation:**

```typescript
@Injectable()
export class EventService {
  private eventEmitter = new EventEmitter2();

  emit(event: string, data: any) {
    this.eventEmitter.emit(event, data);
  }

  on(event: string, handler: (data: any) => void) {
    this.eventEmitter.on(event, handler);
  }
}

// Usage
eventService.emit('user.created', { userId: 'user-1' });

eventService.on('user.created', (data) => {
  // Handle user created event
});
```

## Data Flow

### Request Flow

**Confirmed by Code**: The request flow follows a clear pattern.

**Request Flow Diagram:**

```
Client Request
    │
    ▼
API Gateway / Load Balancer
    │
    ▼
Authentication Guard
    │
    ▼
Validation Pipe
    │
    ▼
Controller
    │
    ▼
Service (Business Logic)
    │
    ├─► Cache (Redis)
    │
    ├─► Database (PostgreSQL)
    │
    └─► Queue (Bull)
    │
    ▼
Response
    │
    ▼
Client
```

### Data Flow Example

**User Registration Flow:**

```
1. Client sends POST /api/auth/register
   │
   ▼
2. API Gateway routes request
   │
   ▼
3. Validation pipe validates DTO
   │
   ▼
4. Auth controller receives request
   │
   ▼
5. Auth service checks if user exists
   │
   ├─► Cache: Check if email exists
   │
   └─► Database: Query user by email
   │
   ▼
6. If user exists, return error
   │
   ▼
7. If not, hash password
   │
   ▼
8. Create user in database
   │
   ▼
9. Cache user data
   │
   ▼
10. Queue welcome email
   │
   ▼
11. Generate JWT tokens
   │
   ▼
12. Return response with tokens
   │
   ▼
13. Client stores tokens
```

## Security Architecture

**Confirmed by Code**: The system implements comprehensive security measures.

### Security Layers

1. **Network Security**
   - TLS/SSL encryption
   - Firewall rules
   - DDoS protection

2. **Application Security**
   - JWT authentication
   - Role-based authorization
   - Input validation
   - Output encoding
   - CSRF protection
   - Rate limiting

3. **Data Security**
   - Encryption at rest
   - Encryption in transit
   - Data masking
   - Secure password hashing

4. **Infrastructure Security**
   - Container security
   - Secrets management
   - Access control
   - Audit logging

### Authentication Flow

**Confirmed by Code**: JWT-based authentication.

```
1. User logs in with credentials
   │
   ▼
2. Server validates credentials
   │
   ▼
3. Server generates JWT access token (expires in 1h)
   │
   ▼
4. Server generates JWT refresh token (expires in 7d)
   │
   ▼
5. Server returns both tokens
   │
   ▼
6. Client stores tokens securely
   │
   ▼
7. Client includes access token in requests
   │
   ▼
8. Server validates token on each request
   │
   ▼
9. If access token expires, use refresh token
   │
   ▼
10. Server issues new access token
```

## Scalability Architecture

**Confirmed by Code**: The system is designed for horizontal scaling.

### Scaling Strategies

1. **Horizontal Scaling**
   - Multiple API instances
   - Load balancing
   - Database read replicas
   - Redis clustering

2. **Vertical Scaling**
   - Increase server resources
   - Optimize database queries
   - Use caching
   - Optimize code

3. **Database Scaling**
   - Read replicas
   - Connection pooling
   - Query optimization
   - Indexing

4. **Cache Scaling**
   - Redis clustering
   - Distributed cache
   - Cache invalidation
   - Cache warming

## Monitoring Architecture

**Confirmed by Code**: The system uses comprehensive monitoring.

### Monitoring Components

1. **Application Monitoring**
   - Health checks
   - Performance metrics
   - Error tracking
   - Logging

2. **Infrastructure Monitoring**
   - Server metrics
   - Container metrics
   - Network metrics
   - Storage metrics

3. **Database Monitoring**
   - Query performance
   - Connection pool
   - Replication lag
   - Storage usage

4. **Cache Monitoring**
   - Hit ratio
   - Memory usage
   - Connection pool
   - Eviction rate

## Deployment Architecture

**Confirmed by Code**: The system uses containerized deployment.

### Deployment Environments

1. **Development**
   - Local Docker Compose
   - Hot reload
   - Debug mode
   - Mock services

2. **Staging**
   - Kubernetes cluster
   - Production-like configuration
   - Integration tests
   - Performance tests

3. **Production**
   - Kubernetes cluster
   - High availability
   - Auto-scaling
   - Monitoring and alerting

### Deployment Pipeline

```
1. Code commit
   │
   ▼
2. CI/CD pipeline triggers
   │
   ▼
3. Run tests
   │
   ▼
4. Build Docker images
   │
   ▼
5. Push to registry
   │
   ▼
6. Deploy to staging
   │
   ▼
7. Run integration tests
   │
   ▼
8. Manual approval
   │
   ▼
9. Deploy to production
   │
   ▼
10. Health checks
   │
   ▼
11. Monitor
```

## Architecture Principles

**Confirmed by Code**: The system follows key architectural principles.

### SOLID Principles

1. **Single Responsibility**
   - Each module has one responsibility
   - Each function does one thing

2. **Open/Closed**
   - Open for extension
   - Closed for modification

3. **Liskov Substitution**
   - Subtypes must be substitutable
   - Interface contracts

4. **Interface Segregation**
   - Small, focused interfaces
   - No fat interfaces

5. **Dependency Inversion**
   - Depend on abstractions
   - Not on concretions

### DRY Principle

**Don't Repeat Yourself:**
- Reusable components
- Shared libraries
- Common utilities
- DRY code

### KISS Principle

**Keep It Simple, Stupid:**
- Simple solutions
- Clear code
- Easy to understand
- Easy to maintain

### YAGNI Principle

**You Aren't Gonna Need It:**
- Build what you need
- Avoid over-engineering
- Don't predict future needs
- Refactor when needed

## Next Steps

After understanding the system architecture:

1. **Explore Modules**: Read about specific modules
2. **Read API Documentation**: Understand API design
3. **Read Database Guide**: Understand data model
4. **Read Deployment Guide**: Understand deployment

## Additional Resources

- [NestJS Architecture](https://docs.nestjs.com/first-steps)
- [React Architecture](https://react.dev/learn/thinking-in-react)
- [Microservices Patterns](https://microservices.io/patterns/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
