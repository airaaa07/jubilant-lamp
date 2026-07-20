# University ERP - Learning Guide

## Overview

This guide provides a structured learning path for developers new to the University ERP codebase. It covers the essential concepts, tools, and workflows needed to contribute effectively.

## Prerequisites

### Required Knowledge

- **JavaScript/TypeScript**: Intermediate level
- **React**: Basic understanding of hooks, components, state management
- **NestJS**: Basic understanding of modules, controllers, services
- **SQL**: Basic understanding of relational databases
- **Git**: Basic understanding of version control

### Required Tools

- **Node.js 18+**: JavaScript runtime
- **npm 9+**: Package manager
- **Docker**: Container platform
- **Docker Compose**: Multi-container orchestration
- **VS Code**: Recommended IDE
- **Git**: Version control

## Learning Path

### Phase 1: Setup and Overview (1-2 days)

#### Day 1: Environment Setup

**Objectives**:
- Set up development environment
- Run the application locally
- Understand the project structure

**Tasks**:
1. Clone the repository
2. Install dependencies (`npm install`)
3. Start Docker services (`docker-compose up -d`)
4. Run database migrations (`cd apps/core-api && npx prisma migrate dev`)
5. Seed the database (`cd apps/core-api && npx prisma db seed`)
6. Start the core API (`cd apps/core-api && npm run start:dev`)
7. Start the admin portal (`cd web/admin-portal && npm run dev`)
8. Access the application at http://localhost:5173

**Resources**:
- [00_PROJECT_INDEX.md](00_PROJECT_INDEX.md)
- [01_SYSTEM_OVERVIEW.md](01_SYSTEM_OVERVIEW.md)
- [02_REPOSITORY_STRUCTURE.md](02_REPOSITORY_STRUCTURE.md)

#### Day 2: Architecture Overview

**Objectives**:
- Understand the system architecture
- Learn about the technology stack
- Explore the database schema

**Tasks**:
1. Read the system overview documentation
2. Review the technology stack
3. Explore the Prisma schema
4. Understand the multi-tenancy model
5. Review the API endpoints

**Resources**:
- [01_SYSTEM_OVERVIEW.md](01_SYSTEM_OVERVIEW.md)
- [03_BACKEND_ARCHITECTURE.md](03_BACKEND_ARCHITECTURE.md)
- [04_FRONTEND_ARCHITECTURE.md](04_FRONTEND_ARCHITECTURE.md)
- [05_DATABASE.md](05_DATABASE.md)
- [06_API_REFERENCE.md](06_API_REFERENCE.md)

### Phase 2: Backend Development (3-5 days)

#### Day 3: NestJS Basics

**Objectives**:
- Understand NestJS fundamentals
- Learn about modules, controllers, services
- Practice creating a simple module

**Tasks**:
1. Read the backend architecture documentation
2. Explore existing modules (e.g., auth, master-data)
3. Understand the controller pattern
4. Understand the service pattern
5. Understand DTOs and validation
6. Create a simple test endpoint

**Resources**:
- [03_BACKEND_ARCHITECTURE.md](03_BACKEND_ARCHITECTURE.md)
- NestJS Documentation: https://docs.nestjs.com

#### Day 4: Database Operations

**Objectives**:
- Learn Prisma ORM
- Understand database relationships
- Practice database operations

**Tasks**:
1. Read the database documentation
2. Explore the Prisma schema
3. Understand the audit middleware
4. Practice CRUD operations
5. Understand transactions
6. Explore the seed scripts

**Resources**:
- [05_DATABASE.md](05_DATABASE.md)
- Prisma Documentation: https://www.prisma.io/docs

#### Day 5: Authentication & Authorization

**Objectives**:
- Understand JWT authentication
- Learn about guards and decorators
- Practice implementing protected routes

**Tasks**:
1. Read the authentication documentation
2. Explore the auth module
3. Understand the JWT strategy
4. Understand the scope guard
5. Practice creating protected endpoints
6. Test authentication flow

**Resources**:
- [12_AUTHENTICATION.md](12_AUTHENTICATION.md)
- apps/core-api/src/modules/auth/

### Phase 3: Frontend Development (3-5 days)

#### Day 6: React Basics

**Objectives**:
- Understand React 19 features
- Learn about React Router
- Practice creating components

**Tasks**:
1. Read the frontend architecture documentation
2. Explore the admin portal structure
3. Understand the routing setup
4. Understand lazy loading
5. Create a simple component
6. Practice using TailwindCSS

**Resources**:
- [04_FRONTEND_ARCHITECTURE.md](04_FRONTEND_ARCHITECTURE.md)
- React Documentation: https://react.dev

#### Day 7: State Management

**Objectives**:
- Learn React Query for server state
- Understand React Context for client state
- Practice state management patterns

**Tasks**:
1. Explore the auth context
2. Understand React Query usage
3. Practice using useQuery and useMutation
4. Understand the API client layer
5. Practice caching and invalidation

**Resources**:
- web/admin-portal/src/auth/
- web/admin-portal/src/api/
- TanStack Query Documentation: https://tanstack.com/query/latest

#### Day 8: Forms and Validation

**Objectives**:
- Learn react-hook-form
- Understand Zod validation
- Practice form handling

**Tasks**:
1. Explore existing forms
2. Understand react-hook-form pattern
3. Understand Zod schema validation
4. Practice creating a form
5. Implement form validation

**Resources**:
- React Hook Form Documentation: https://react-hook-form.com
- Zod Documentation: https://zod.dev

### Phase 4: Advanced Topics (5-7 days)

#### Day 9: Workflow Engine

**Objectives**:
- Understand the workflow engine
- Learn about workflow definitions
- Practice creating workflows

**Tasks**:
1. Read the feature flows documentation
2. Explore the workflow module
3. Understand workflow definitions
4. Understand workflow instances
5. Practice creating a simple workflow
6. Test workflow execution

**Resources**:
- [07_FEATURE_FLOWS.md](07_FEATURE_FLOWS.md)
- apps/core-api/src/modules/workflow/

#### Day 10: Background Jobs

**Objectives**:
- Understand Bull queues
- Learn about worker services
- Practice creating background jobs

**Tasks**:
1. Read the workers and queues documentation
2. Explore the notification worker
3. Explore the certificate generator
4. Understand queue configuration
5. Practice adding a job to queue
6. Test job processing

**Resources**:
- [08_WORKERS_AND_QUEUES.md](08_WORKERS_AND_QUEUES.md)
- Bull Documentation: https://docs.bullmq.io/

#### Day 11: Storage and File Handling

**Objectives**:
- Understand MinIO integration
- Learn about file uploads
- Practice file handling

**Tasks**:
1. Read the storage documentation
2. Explore the MinIO service
3. Understand file upload flow
4. Practice uploading files
5. Practice generating presigned URLs

**Resources**:
- [09_STORAGE_AND_MINIO.md](09_STORAGE_AND_MINIO.md)
- apps/core-api/src/infrastructure/minio/

#### Day 12: Caching and Performance

**Objectives**:
- Understand Redis caching
- Learn about caching strategies
- Practice implementing caching

**Tasks**:
1. Read the Redis documentation
2. Explore the Redis service
3. Understand cache patterns
4. Practice caching database queries
5. Practice cache invalidation

**Resources**:
- [10_REDIS.md](10_REDIS.md)
- apps/core-api/src/infrastructure/redis/

#### Day 13: Testing

**Objectives**:
- Understand testing strategy
- Learn about Jest
- Practice writing tests

**Tasks**:
1. Explore existing tests
2. Understand Jest configuration
3. Practice writing unit tests
4. Practice writing integration tests
5. Run tests and fix failures

**Resources**:
- Jest Documentation: https://jestjs.io/

### Phase 5: Specialized Modules (3-5 days)

#### Day 14: Examination System

**Objectives**:
- Understand the CBE engine
- Learn about WebSocket communication
- Explore exam flow

**Tasks**:
1. Read the feature flows documentation (exam flow)
2. Explore the examination module
3. Explore the CBE engine
4. Understand WebSocket communication
5. Test exam interface

**Resources**:
- [07_FEATURE_FLOWS.md](07_FEATURE_FLOWS.md)
- apps/core-api/src/modules/examination/
- apps/cbe-engine/

#### Day 15: Fee Management

**Objectives**:
- Understand the fee module
- Learn about payment integration
- Explore fee structures

**Tasks**:
1. Explore the fee module
2. Understand fee heads
3. Understand fee structures
4. Understand payment flow
5. Explore Razorpay integration

**Resources**:
- apps/core-api/src/modules/fee/

#### Day 16: Document Generation

**Objectives**:
- Understand document templates
- Learn about certificate generation
- Practice document generation

**Tasks**:
1. Read the certificate engine documentation
2. Explore the documents module
3. Understand document templates
4. Practice generating a certificate
5. Test certificate generation

**Resources**:
- [14_CERTIFICATE_ENGINE.md](14_CERTIFICATE_ENGINE.md)
- apps/core-api/src/modules/documents/
- apps/cert-generator/

### Phase 6: Deployment and Operations (2-3 days)

#### Day 17: Docker and Deployment

**Objectives**:
- Understand Docker configuration
- Learn about deployment strategies
- Practice deployment

**Tasks**:
1. Read the infrastructure documentation
2. Explore docker-compose.yml
3. Understand Dockerfile patterns
4. Practice building Docker images
5. Practice deploying with Docker Compose

**Resources**:
- [17_INFRASTRUCTURE.md](17_INFRASTRUCTURE.md)
- Docker Documentation: https://docs.docker.com/

#### Day 18: Monitoring and Debugging

**Objectives**:
- Understand monitoring tools
- Learn debugging techniques
- Practice troubleshooting

**Tasks**:
1. Explore health check endpoints
2. Understand logging
3. Practice debugging with VS Code
4. Practice debugging with Chrome DevTools
5. Troubleshoot common issues

**Resources**:
- [19_REQUEST_LIFECYCLES.md](19_REQUEST_LIFECYCLES.md)

### Phase 7: Contribution (Ongoing)

#### Day 19+: Contributing

**Objectives**:
- Understand contribution guidelines
- Practice making contributions
- Learn code review process

**Tasks**:
1. Understand Git workflow
2. Create a feature branch
3. Make a small change
4. Write tests
5. Submit pull request
6. Participate in code review

## Common Tasks

### Adding a New API Endpoint

1. **Create DTO** in `apps/core-api/src/modules/[module]/dto/`
2. **Add method** to controller
3. **Add method** to service
4. **Add validation** with Zod
5. **Add guards** if needed
6. **Test endpoint**

### Adding a New Frontend Page

1. **Create component** in `web/admin-portal/src/pages/`
2. **Add route** in `App.tsx`
3. **Create API methods** in `web/admin-portal/src/api/`
4. **Add navigation** if needed
5. **Test page**

### Adding a New Database Model

1. **Add model** to `apps/core-api/prisma/schema.prisma`
2. **Run migration** (`npx prisma migrate dev`)
3. **Update seed** if needed
4. **Run seed** (`npx prisma db seed`)
5. **Test model**

### Adding a New Workflow

1. **Create workflow definition** in database
2. **Configure states and transitions**
3. **Add workflow logic** in service
4. **Test workflow execution**
5. **Add notifications**

## Troubleshooting

### Common Issues

#### Database Connection Failed

**Symptoms**: Application fails to start with database error

**Solutions**:
1. Check PostgreSQL is running (`docker-compose ps postgres`)
2. Check DATABASE_URL is correct
3. Check database credentials
4. Restart PostgreSQL service

#### Redis Connection Failed

**Symptoms**: Cache/queue operations fail

**Solutions**:
1. Check Redis is running (`docker-compose ps redis`)
2. Check REDIS_HOST and REDIS_PORT
3. Test Redis connection (`docker-compose exec redis redis-cli ping`)

#### MinIO Connection Failed

**Symptoms**: File upload fails

**Solutions**:
1. Check MinIO is running (`docker-compose ps minio`)
2. Check MINIO_ENDPOINT is correct
3. Check MinIO credentials
4. Test MinIO health (`curl http://localhost:9000/minio/health/live`)

#### Build Errors

**Symptoms**: TypeScript compilation errors

**Solutions**:
1. Check TypeScript version
2. Clear node_modules and reinstall
3. Clear Turbo cache (`rm -rf .turbo`)
4. Check for circular dependencies

#### Frontend Build Errors

**Symptoms**: Vite build fails

**Solutions**:
1. Check Node.js version
2. Clear node_modules and reinstall
3. Check environment variables
4. Check for missing dependencies

## Best Practices

### Backend

1. **Use DTOs** for request/response validation
2. **Use services** for business logic
3. **Use transactions** for multi-step operations
4. **Handle errors** gracefully
5. **Add logging** for debugging
6. **Write tests** for critical paths
7. **Use guards** for authorization
8. **Use caching** for frequently accessed data

### Frontend

1. **Use React Query** for server state
2. **Use React Context** for global state
3. **Lazy load** pages for performance
4. **Handle errors** gracefully
5. **Add loading states** for async operations
6. **Use TypeScript** for type safety
7. **Follow naming conventions**
8. **Keep components small**

### Database

1. **Use indexes** for frequently queried fields
2. **Use transactions** for related operations
3. **Use migrations** for schema changes
4. **Seed data** for development
5. **Backup data** regularly
6. **Monitor performance** of slow queries

### Git

1. **Use feature branches** for new work
2. **Write descriptive commit messages**
3. **Keep commits small** and focused
4. **Rebase** before merging
5. **Resolve conflicts** carefully
6. **Never commit** sensitive data

## Resources

### Documentation

- [Project Index](00_PROJECT_INDEX.md)
- [System Overview](01_SYSTEM_OVERVIEW.md)
- [Repository Structure](02_REPOSITORY_STRUCTURE.md)
- [Backend Architecture](03_BACKEND_ARCHITECTURE.md)
- [Frontend Architecture](04_FRONTEND_ARCHITECTURE.md)
- [Database](05_DATABASE.md)
- [API Reference](06_API_REFERENCE.md)
- [Feature Flows](07_FEATURE_FLOWS.md)
- [Workers and Queues](08_WORKERS_AND_QUEUES.md)
- [Storage and MinIO](09_STORAGE_AND_MINIO.md)
- [Redis](10_REDIS.md)
- [Elasticsearch](11_ELASTICSEARCH.md)
- [Authentication](12_AUTHENTICATION.md)
- [Email and SMTP](13_EMAIL_AND_SMTP.md)
- [Certificate Engine](14_CERTIFICATE_ENGINE.md)
- [Configuration](15_CONFIGURATION.md)
- [Environment Variables](16_ENVIRONMENT_VARIABLES.md)
- [Infrastructure](17_INFRASTRUCTURE.md)
- [Dependency Graph](18_DEPENDENCY_GRAPH.md)
- [Request Lifecycles](19_REQUEST_LIFECYCLES.md)
- [Unknowns and Open Questions](21_UNKNOWNS_AND_OPEN_QUESTIONS.md)

### External Resources

- NestJS: https://docs.nestjs.com
- React: https://react.dev
- Prisma: https://www.prisma.io/docs
- TypeScript: https://www.typescriptlang.org/docs
- Docker: https://docs.docker.com
- Redis: https://redis.io/docs
- MinIO: https://min.io/docs
- Bull: https://docs.bullmq.io/

## Getting Help

### Internal Resources

1. **Documentation**: Check the docs/ directory
2. **Code Comments**: Read inline code comments
3. **Existing Code**: Review similar implementations
4. **Team**: Ask team members for guidance

### External Resources

1. **Stack Overflow**: Search for similar issues
2. **GitHub Issues**: Check repository issues
3. **Documentation**: Read official documentation
4. **Community**: Join relevant communities

## Next Steps

After completing this learning path:

1. **Pick a small task** to work on
2. **Create a feature branch**
3. **Implement the task**
4. **Write tests**
5. **Submit for review**
6. **Iterate based on feedback**

## Continuous Learning

- **Stay updated** with new versions of dependencies
- **Read documentation** regularly
- **Practice** regularly
- **Ask questions** when stuck
- **Share knowledge** with team
