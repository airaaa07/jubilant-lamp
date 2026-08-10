# Docker

## Purpose

This document explains Docker in the University ERP system. It details how Docker is used for containerization, Docker configuration, and best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Docker for containerization. Understanding Docker is critical for:
- Containerizing applications
- Local development
- Production deployment
- Debugging Docker issues
- Optimizing Docker images

Without understanding Docker, developers may struggle with containerization or may introduce Docker-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn Docker
- **Feature Development**: Containerizing applications
- **Code Reviews**: Reviewing Docker configurations
- **Local Development**: Running applications locally
- **Production**: Deploying to production

## Dependencies

### Docker Dependencies

**Confirmed by Code**: Docker depends on:

- **Docker Engine**: Docker runtime
- **Docker Compose**: Multi-container orchestration
- **Node.js**: Application runtime
- **Nginx**: Web server for frontend

## Internal Architecture

### Docker Architecture

**Confirmed by Code**: Docker follows container-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Docker Engine                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Docker Images                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  Admin Portal  │  │  PostgreSQL     │
│  Image        │  │  Image         │  │  Image          │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Docker Containers                             │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Dockerfile (Core API)

**Confirmed by Code**: Dockerfile for backend API.

**Dockerfile**:
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["node", "dist/main"]
```

**What This Does**:
- **Multi-stage Build**: Optimizes image size
- **Builder Stage**: Builds application with dev dependencies
- **Production Stage**: Production image with only production dependencies
- **COPY**: Copies build output
- **CMD**: Runs application

### Dockerfile (Admin Portal)

**Confirmed by Code**: Dockerfile for frontend.

**Dockerfile**:
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**What This Does**:
- **Build Stage**: Builds React app
- **Nginx**: Serves static files
- **nginx.conf**: Nginx configuration
- **Static Files**: Copies build output to nginx

### Docker Compose

**Confirmed by Code**: Docker Compose for local development.

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  core-api:
    build:
      context: ./apps/core-api
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - JWT_SECRET=dev-secret
    depends_on:
      - postgres
      - redis

  admin-portal:
    build:
      context: ./web/admin-portal
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - core-api

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=university_erp
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

**What This Does**:
- **core-api**: Backend API service
- **admin-portal**: Frontend admin portal
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **volumes**: Persistent data storage

## Database Interactions

### Docker-Database Flow

**Confirmed by Code**: Database runs in Docker container.

**Flow**:
```
Docker Compose → PostgreSQL Container → Database
```

## Redis Interactions

### Docker-Redis Flow

**Confirmed by Code**: Redis runs in Docker container.

**Flow**:
```
Docker Compose → Redis Container → Cache
```

## Queue Interactions

### Docker-Queue Flow

**Confirmed by Code**: Queue runs in same container as API.

**Flow**:
```
Docker Compose → Core API Container → Bull Queue
```

## Worker Interactions

### Docker-Worker Flow

**Confirmed by Code**: Workers run in same container as API.

**Flow**:
```
Docker Compose → Core API Container → Workers
```

## Business Rules

### Docker Rules

**Confirmed by Code**: Docker follows these rules:

1. **Multi-stage Build**: Use multi-stage builds
2. **Alpine Images**: Use Alpine images for smaller size
3. **Environment Variables**: Configuration via environment variables
4. **Volumes**: Use volumes for persistent storage
5. **Networks**: Use Docker networks for communication

### Docker Compose Rules

**Confirmed by Code**: Docker Compose rules:

1. **Service Definition**: Define all services
2. **Dependencies**: Define service dependencies
3. **Environment**: Configure environment variables
4. **Volumes**: Define volumes for persistence
5. **Ports**: Expose necessary ports

## Security

### Docker Security

**Confirmed by Code**: Security considerations for Docker:

1. **Base Images**: Use official base images
2. **Updates**: Keep base images updated
3. **Secrets**: Don't commit secrets
4. **User**: Run as non-root user
5. **Networks**: Use private networks

## Performance Considerations

### Docker Performance

**Confirmed by Code**: Performance considerations:

1. **Image Size**: Keep image size small
2. **Layers**: Minimize layers
3. **Caching**: Use build cache
4. **Resource Limits**: Set resource limits
5. **Multi-stage Builds**: Use multi-stage builds

## Common Mistakes

### Mistake 1: Not Using Multi-stage Builds

**Symptom**: Large image size

**Cause**: Not using multi-stage builds

**Fix**:
```dockerfile
# Use multi-stage build
FROM node:20-alpine AS builder
# build stage

FROM node:20-alpine
# production stage
COPY --from=builder /app/dist ./dist
```

### Mistake 2: Not Using Volumes

**Symptom**: Data loss on restart

**Cause**: Not using volumes

**Fix**:
```yaml
# Use volumes
volumes:
  - postgres-data:/var/lib/postgresql/data
```

### Mistake 3: Committing Secrets

**Symptom**: Security vulnerability

**Cause**: Committing secrets to Dockerfile

**Fix**:
```dockerfile
# Use environment variables
ENV JWT_SECRET=${JWT_SECRET}
```

## Debugging Guide

### Docker Debugging

**Issue**: Container not starting

**Investigation**:
1. Check container logs
2. Check Dockerfile
3. Check environment variables
4. Check dependencies
5. Check networking

**Tools**:
- Docker logs
- Docker ps
- Docker inspect
- Docker exec

## Future Enhancements

### Docker Buildx

**Status**: Not implemented

**Proposal**: Implement Docker Buildx:
- Multi-platform builds
- Better caching
- Faster builds
- More complex
- Better for production

### Docker Scout

**Status**: Not implemented

**Proposal**: Implement Docker Scout:
- Security scanning
- Vulnerability detection
- Better security
- More complex
- Better for production

## Production Considerations

### Production Docker

**Production Deployment**:
- Use multi-stage builds
- Use official base images
- Set resource limits
- Use secrets manager
- Monitor containers

### Docker Monitoring

**Monitoring Metrics**:
- Container resource usage
- Container uptime
- Image size
- Build time
- Container count

## Example Requests

### Docker Example

**Build Image**:
```bash
docker build -t university-erp-core-api .
```

**Run Container**:
```bash
docker run -p 3000:3000 university-erp-core-api
```

## Example Responses

### Docker Response

**Response**: Container running

```bash
Container started on port 3000
```

## Sequence Diagrams

### Docker Flow

```
Docker Build → Docker Image → Docker Run → Docker Container → Application Running
```

## Architecture Diagrams

### Docker Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Docker Engine                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Docker Images                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  Admin Portal  │  │  PostgreSQL     │
│  Image        │  │  Image         │  │  Image          │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How is Docker used in the system?

**Answer**: Docker via:
- Containerizing applications
- Local development with Docker Compose
- Production deployment
- Multi-stage builds
- Volume management

### Q2: How do you optimize Docker images?

**Answer**: Optimize images via:
- Multi-stage builds
- Alpine base images
- Minimize layers
- Use build cache
- Remove unnecessary files

### Q3: How do you handle persistent data in Docker?

**Answer**: Persistent data via:
- Docker volumes
- Volume mounts
- Named volumes
- Bind mounts
- Backup strategies

## Exercises

### Exercise 1: Create Dockerfile

**Task**: Create a Dockerfile for the application.

**Steps**:
1. Create multi-stage Dockerfile
2. Build application
3. Copy production dependencies
4. Set up command
5. Test Docker build

**Verification**:
- Dockerfile created
- Build works
- Image runs
- Tests pass

### Exercise 2: Create Docker Compose

**Task**: Create Docker Compose for local development.

**Steps**:
1. Define services
2. Configure environment variables
3. Set up volumes
4. Configure networking
5. Test Docker Compose

**Verification**:
- Docker Compose created
- Services defined
- Environment configured
- Volumes configured
- Tests pass

## Real Production Scenarios

### Scenario 1: Container Not Starting

**Situation**: Container not starting

**Response**:
1. Check container logs
2. Check Dockerfile
3. Check environment variables
4. Fix issue
5. Restart container

### Scenario 2: Large Image Size

**Situation**: Large Docker image

**Response**:
1. Check Dockerfile
2. Use multi-stage build
3. Use Alpine images
4. Remove unnecessary files
5. Rebuild image

## Navigation

**Next Section**: [02-Kubernetes](./02-Kubernetes.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [17-Production](../17-Production/README.md) - Production details
