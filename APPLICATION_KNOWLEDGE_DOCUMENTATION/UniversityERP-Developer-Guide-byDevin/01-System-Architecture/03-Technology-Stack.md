# Technology Stack

## Purpose

This document provides a comprehensive overview of the technology stack used in the University ERP system. It explains the choice of each technology, its purpose, and how it fits into the overall architecture.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses a diverse technology stack including NestJS, React, PostgreSQL, Redis, MinIO, and more. Understanding the technology stack is critical for:
- Making informed technical decisions
- Understanding system capabilities and limitations
- Troubleshooting technology-specific issues
- Planning for upgrades and migrations
- Evaluating alternative technologies

Without understanding the technology stack, developers may misuse technologies or make incompatible choices.

## Where This Is Used

- **Onboarding**: New developers learn the technologies
- **Architecture Reviews**: Evaluating technology choices
- **Technical Planning**: Planning new features
- **Troubleshooting**: Technology-specific debugging
- **Upgrade Planning**: Planning technology upgrades

## Dependencies

### Technology Dependencies

**Confirmed by Code**: The technology stack has these dependencies:

**Backend**:
- NestJS depends on Node.js and TypeScript
- Prisma depends on PostgreSQL
- Bull depends on Redis
- MinIO SDK depends on MinIO server

**Frontend**:
- React depends on Node.js and TypeScript
- Vite depends on Node.js
- React Query depends on React
- Tailwind CSS depends on PostCSS

**Infrastructure**:
- Docker depends on OS kernel
- Docker Compose depends on Docker
- PostgreSQL depends on OS
- Redis depends on OS

## Internal Architecture

### Technology Stack Overview

**Confirmed by Code**: The system uses the following technology stack:

```
Backend:
├── Node.js 18.x
├── TypeScript 6.x
├── NestJS 10.x
├── Prisma 5.x
├── PostgreSQL 16.x
├── Redis 7.x
├── Bull 4.x
└── MinIO SDK 7.x

Frontend:
├── Node.js 18.x
├── TypeScript 6.x
├── React 19.x
├── Vite 5.x
├── React Query
├── Tailwind CSS 3.x
└── React Router 6.x

Infrastructure:
├── Docker 20.x
├── Docker Compose 2.x
├── PostgreSQL 16.x (Docker)
├── Redis 7.x (Docker)
├── MinIO 7.x (Docker)
├── Elasticsearch 8.13.0 (Docker)
└── Nginx (Docker)
```

## Code Walkthrough

### Backend Technologies

#### Node.js

**Confirmed by Code**: Node.js 18.x is used as the runtime.

**Purpose**: JavaScript runtime for backend services.

**Why Node.js**:
- Non-blocking I/O
- Event-driven architecture
- Large ecosystem (npm)
- TypeScript support
- Scalable
- Fast development

**Usage**:
```typescript
// apps/core-api/src/main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
```

#### TypeScript

**Confirmed by Code**: TypeScript 6.x is used for type safety.

**Purpose**: Static typing for JavaScript.

**Why TypeScript**:
- Type safety
- Better IDE support
- Catch errors at compile time
- Self-documenting code
- Refactoring confidence
- Better collaboration

**Usage**:
```typescript
interface User {
  id: string;
  email: string;
  role: 'ADMIN' | 'STAFF' | 'STUDENT';
}

async function getUser(id: string): Promise<User> {
  return prisma.user.findUnique({ where: { id } });
}
```

#### NestJS

**Confirmed by Code**: NestJS 10.x is the backend framework.

**Purpose**: Framework for building efficient Node.js applications.

**Why NestJS**:
- Built-in dependency injection
- Modular architecture
- TypeScript support
- Easy testing
- Scalable
- Large ecosystem
- Similar to Angular (familiarity)

**Usage**:
```typescript
@Module({
  imports: [ConfigModule, PrismaModule],
  controllers: [AuthController],
  providers: [AuthService],
})
export class AuthModule {}
```

#### Prisma

**Confirmed by Code**: Prisma 5.x is the ORM.

**Purpose**: Database ORM and query builder.

**Why Prisma**:
- Type-safe database access
- Auto-generated types
- Migration management
- Excellent TypeScript support
- Easy to use
- Great documentation

**Usage**:
```typescript
const user = await prisma.user.findUnique({
  where: { email: 'test@example.com' },
  include: { institute: true },
});
```

### Frontend Technologies

#### React

**Confirmed by Code**: React 19.x is the frontend framework.

**Purpose**: UI library for building user interfaces.

**Why React**:
- Component-based architecture
- Virtual DOM for performance
- Large ecosystem
- TypeScript support
- Hooks for state management
- Server components (React 19)

**Usage**:
```typescript
function UserProfile({ userId }: { userId: string }) {
  const { data: user } = useQuery(['user', userId], () => fetchUser(userId));

  if (!user) return <div>Loading...</div>;

  return <div>{user.name}</div>;
}
```

#### Vite

**Confirmed by Code**: Vite 5.x is the build tool.

**Purpose**: Fast build tool for frontend.

**Why Vite**:
- Fast HMR (Hot Module Replacement)
- Fast cold start
- ES modules support
- Great DX (Developer Experience)
- Plugin ecosystem
- Optimized builds

**Usage**:
```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
```

#### React Query

**Confirmed by Code**: React Query is used for server state management.

**Purpose**: Data fetching and caching library.

**Why React Query**:
- Automatic caching
- Automatic refetching
- Optimistic updates
- Pagination
- Infinite queries
- Type-safe

**Usage**:
```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
});
```

#### Tailwind CSS

**Confirmed by Code**: Tailwind CSS 3.x is used for styling.

**Purpose**: Utility-first CSS framework.

**Why Tailwind CSS**:
- No custom CSS files
- Consistent design system
- Responsive design
- Dark mode support
- Purges unused CSS
- Fast development

**Usage**:
```typescript
<div className="flex items-center justify-center p-4 bg-blue-500 text-white rounded">
  <span className="text-lg font-bold">Hello</span>
</div>
```

### Infrastructure Technologies

#### Docker

**Confirmed by Code**: Docker 20.x is used for containerization.

**Purpose**: Container platform for applications.

**Why Docker**:
- Consistent environments
- Easy deployment
- Resource isolation
- Scalability
- Microservices support
- Great DX

**Usage**:
```yaml
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["node", "dist/main.js"]
```

#### Docker Compose

**Confirmed by Code**: Docker Compose 2.x is used for multi-container orchestration.

**Purpose**: Define and run multi-container applications.

**Why Docker Compose**:
- Easy local development
- Multi-service orchestration
- Volume management
- Network management
- Simple configuration

**Usage**:
```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: postgres
```

#### PostgreSQL

**Confirmed by Code**: PostgreSQL 16.x is the database.

**Purpose**: Relational database.

**Why PostgreSQL**:
- ACID compliance
- Advanced features (JSONB, arrays)
- Excellent performance
- Great tooling
- Open source
- Reliable

**Usage**:
```sql
SELECT u.*, i.name as institute_name
FROM "User" u
JOIN "Institute" i ON u."instituteId" = i.id
WHERE u.email = 'test@example.com';
```

#### Redis

**Confirmed by Code**: Redis 7.x is used for caching and queues.

**Purpose**: In-memory data store.

**Why Redis**:
- Fast in-memory operations
- Data structures (strings, lists, sets, hashes)
- Pub/sub support
- Persistence options
- Great for caching
- Queue backend (Bull)

**Usage**:
```typescript
await redis.setex('user:123', 300, JSON.stringify(user));
const user = JSON.parse(await redis.get('user:123'));
```

#### MinIO

**Confirmed by Code**: MinIO 7.x is used for object storage.

**Purpose**: S3-compatible object storage.

**Why MinIO**:
- S3-compatible API
- Self-hosted
- Great performance
- Easy to use
- Cost-effective
- Supports Azure Blob fallback

**Usage**:
```typescript
await minioService.upload('file.pdf', buffer, 'application/pdf');
const url = await minioService.getPresignedUrl('file.pdf');
```

## Database Interactions

### PostgreSQL via Prisma

**Confirmed by Code**: All database operations use Prisma.

**Connection**: Prisma Client connects to PostgreSQL.

**Operations**:
- Query: `prisma.user.findMany()`
- Create: `prisma.user.create()`
- Update: `prisma.user.update()`
- Delete: `prisma.user.delete()`
- Transaction: `prisma.$transaction()`

## Redis Interactions

### Redis via ioredis

**Confirmed by Code**: RedisService wraps ioredis client.

**Connection**: RedisService connects to Redis.

**Operations**:
- Set: `redis.set(key, value)`
- Get: `redis.get(key)`
- Delete: `redis.del(key)`
- Set with expiry: `redis.setex(key, ttl, value)`
- Hash operations: `redis.hset()`, `redis.hget()`

## Queue Interactions

### Bull via Redis

**Confirmed by Code**: Bull queues use Redis as backend.

**Connection**: Bull connects to Redis.

**Operations**:
- Add job: `queue.add(jobType, data)`
- Process job: `@Processor(queueName)`
- Retry logic: Built-in with exponential backoff
- Dead letter queue: For failed jobs

## Worker Interactions

### Notification Worker

**Confirmed by Code**: Notification worker processes email/SMS jobs.

**Technology**: NestJS + Bull + Nodemailer

**Operations**:
- Process email jobs
- Process SMS jobs
- Retry on failure
- Log results

### Certificate Generator

**Confirmed by Code**: Certificate generator processes PDF generation jobs.

**Technology**: NestJS + Bull + Puppeteer + Handlebars

**Operations**:
- Process certificate jobs
- Generate PDF with Puppeteer
- Render templates with Handlebars
- Upload to MinIO
- Return URL

## Business Rules

### Technology Selection Rules

**Confirmed by Code**: Technology selection follows these rules:

1. **TypeScript Preferred**: All code uses TypeScript for type safety
2. **Framework Consistency**: Backend uses NestJS, frontend uses React
3. **ORM Preferred**: Use Prisma for database access
4. **Caching Required**: Use Redis for caching
5. **Containerization**: All services run in Docker
6. **Queue for Async**: Use Bull for background jobs

### Version Compatibility

**Confirmed by Code**: Versions are specified in package.json files.

**Compatibility Matrix**:
- Node.js 18+ required for NestJS 10
- TypeScript 6.x compatible with Node.js 18
- Prisma 5.x compatible with PostgreSQL 16
- React 19 compatible with TypeScript 6

## Security

### Technology Security

**Node.js Security**:
- Keep Node.js updated
- Use npm audit
- Use helmet for Express security
- Validate all inputs
- Sanitize outputs

**PostgreSQL Security**:
- Use strong passwords
- Enable SSL/TLS
- Use prepared statements (Prisma)
- Limit user permissions
- Regular backups

**Redis Security**:
- Use strong passwords
- Enable AUTH in production
- Use TLS in production
- Limit network access
- Regular backups

**Docker Security**:
- Use non-root user in containers
- Scan images for vulnerabilities
- Use minimal images
- Don't expose unnecessary ports
- Use secrets management

## Performance Considerations

### Technology Performance

**Node.js Performance**:
- Event-driven, non-blocking I/O
- Good for I/O-bound operations
- Can be CPU-intensive for heavy computation
- Use worker threads for CPU-bound tasks

**PostgreSQL Performance**:
- Excellent for relational data
- Indexes for fast queries
- Connection pooling
- Query optimization
- Partitioning for large tables

**Redis Performance**:
- In-memory, very fast
- Network latency is main bottleneck
- Use pipelining for multiple operations
- Use clustering for scalability

**React Performance**:
- Virtual DOM for efficient updates
- Code splitting for smaller bundles
- Memoization for expensive computations
- Lazy loading for components

## Common Mistakes

### Mistake 1: Not Using TypeScript Features

**Symptom**: Code not type-safe

**Cause**: Not using TypeScript features properly

**Fix**:
- Use interfaces for data structures
- Use type guards
- Use generics
- Enable strict mode in tsconfig.json

### Mistake 2: Not Using Caching

**Symptom**: Slow API responses

**Cause**: Not caching frequently accessed data

**Fix**:
- Use Redis for caching
- Cache database queries
- Cache API responses
- Set appropriate TTL

### Mistake 3: Not Using Transactions

**Symptom**: Data inconsistency

**Cause**: Not using Prisma transactions

**Fix**:
```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data });
  const profile = await tx.userProfile.create({ data });
});
```

## Debugging Guide

### Technology-Specific Debugging

**Node.js Debugging**:
```bash
# Start with debug flag
node --inspect dist/main.js

# Or use VS Code debugger
```

**TypeScript Debugging**:
```bash
# Source maps required
# Enable in tsconfig.json
"sourceMap": true
```

**Prisma Debugging**:
```bash
# Enable query logging
DATABASE_URL="postgresql://...?logging=true"

# Or use Prisma Client logging
const prisma = new PrismaClient({ log: ['query', 'info', 'warn', 'error'] });
```

**Redis Debugging**:
```bash
# Monitor commands
docker-compose exec redis redis-cli monitor

# Check memory
docker-compose exec redis redis-cli INFO memory
```

## Future Enhancements

### Technology Upgrades

**Planned Upgrades**:
- Node.js: Upgrade to LTS when available
- TypeScript: Upgrade to latest stable
- NestJS: Upgrade to latest stable
- Prisma: Upgrade to latest stable
- React: Upgrade to latest stable

### Alternative Technologies

**Considered Alternatives**:
- **Backend**: Fastify (instead of Express/NestJS)
- **Database**: MongoDB (instead of PostgreSQL)
- **Queue**: RabbitMQ (instead of Bull/Redis)
- **Frontend**: Next.js (instead of Vite)
- **Styling**: CSS Modules (instead of Tailwind)

## Production Considerations

### Technology Production Configurations

**Node.js Production**:
- Use process manager (PM2, systemd)
- Enable cluster mode
- Set NODE_ENV=production
- Use production build
- Enable logging

**PostgreSQL Production**:
- Use managed service (AWS RDS, Azure Database)
- Enable automated backups
- Enable point-in-time recovery
- Use read replicas
- Monitor performance

**Redis Production**:
- Use managed service (ElastiCache, Azure Cache)
- Enable persistence (AOF)
- Use clustering
- Monitor memory usage
- Set eviction policy

**Docker Production**:
- Use minimal images
- Use non-root user
- Scan for vulnerabilities
- Use secrets management
- Enable logging

## Example Requests

### Technology Version Check

**Request**:
```bash
node --version
npm --version
tsc --version
```

**Response**:
```
v18.x.x
9.x.x
Version 6.x.x
```

## Example Responses

### Package Version Information

**Request**:
```bash
npm list nestjs
```

**Response**:
```
university-erp@1.0.0
└── nestjs@10.0.0
```

## Sequence Diagrams

### Technology Stack Flow

```
User → React (Frontend)
    ↓
Vite (Build Tool)
    ↓
Node.js (Runtime)
    ↓
NestJS (Backend Framework)
    ↓
Prisma (ORM)
    ↓
PostgreSQL (Database)
    ↓
Redis (Cache)
    ↓
MinIO (Storage)
```

## Architecture Diagrams

### Technology Stack Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   React 19   │  │   NestJS 10  │  │   Bull 4.x   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Runtime Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Node.js 18  │  │  TypeScript 6 │  │   Vite 5.x   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ PostgreSQL 16│  │   Redis 7.x  │  │   MinIO 7.x  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Docker 20  │  │Docker Compose│  │   Nginx      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: Why did you choose TypeScript over JavaScript?

**Answer**: TypeScript provides:
- Type safety at compile time
- Better IDE support with autocomplete
- Self-documenting code
- Easier refactoring
- Catches errors early
- Better collaboration

### Q2: Why did you choose NestJS over Express?

**Answer**: NestJS provides:
- Built-in dependency injection
- Modular architecture
- TypeScript support out of the box
- Easy testing
- Scalable structure
- Similar to Angular (familiarity)
- Large ecosystem

### Q3: Why did you choose Prisma over TypeORM?

**Answer**: Prisma provides:
- Auto-generated types
- Type-safe queries
- Migration management
- Great TypeScript support
- Easy to use
- Excellent documentation

### Q4: Why did you choose React over Vue or Angular?

**Answer**: React provides:
- Component-based architecture
- Virtual DOM for performance
- Large ecosystem
- TypeScript support
- Hooks for state management
- Server components (React 19)
- Flexibility

### Q5: Why did you choose PostgreSQL over MongoDB?

**Answer**: PostgreSQL provides:
- ACID compliance
- Relational data model
- Advanced features (JSONB, arrays)
- Excellent performance
- Great tooling
- Open source
- Reliable

## Exercises

### Exercise 1: Technology Research

**Task**: Research one technology in the stack and write a summary.

**Verification**:
- Understand the technology
- Understand its purpose
- Understand its alternatives
- Understand its pros and cons

### Exercise 2: Version Compatibility

**Task**: Check version compatibility between technologies.

**Verification**:
- Check Node.js version compatibility
- Check TypeScript version compatibility
- Check framework version compatibility
- Document any issues

## Real Production Scenarios

### Scenario 1: Technology Upgrade

**Situation**: Need to upgrade React to version 20

**Steps**:
1. Check breaking changes
2. Update package.json
3. Run tests
4. Fix breaking changes
5. Deploy to staging
6. Monitor for issues

### Scenario 2: Technology Migration

**Situation**: Need to migrate from Bull to RabbitMQ

**Steps**:
1. Research RabbitMQ
2. Plan migration
3. Implement RabbitMQ integration
4. Migrate existing jobs
5. Test thoroughly
6. Deploy to production

## Navigation

**Next Section**: [04-Multi-Tenancy-Model](./04-Multi-Tenancy-Model.md)

**Previous Section**: [02-Repository-Structure](./02-Repository-Structure.md)

**Related Documentation**:
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [04-Frontend](../04-Frontend/README.md) - Frontend architecture
- [05-Database](../05-Database/README.md) - Database details
