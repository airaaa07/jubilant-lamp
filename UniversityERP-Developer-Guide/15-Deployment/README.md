# 15-Deployment

## Purpose

This folder provides comprehensive documentation about deployment in the University ERP system. It details how the system is deployed, deployment strategies, CI/CD pipelines, and production considerations.

## Why This Folder Exists

**Confirmed by Code**: The University ERP requires proper deployment. Understanding deployment is critical for:
- Deploying the system to production
- Setting up CI/CD pipelines
- Managing environments
- Debugging deployment issues
- Optimizing deployment process

Without understanding deployment, developers may struggle with production deployment or may introduce deployment-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn deployment
- **Feature Development**: Preparing for deployment
- **Code Reviews**: Reviewing deployment configurations
- **Production**: Deploying to production
- **CI/CD**: Setting up pipelines

## Dependencies

### Deployment Dependencies

**Confirmed by Code**: Deployment depends on:

- **Docker**: Containerization
- **Docker Compose**: Local development
- **Kubernetes**: Production orchestration
- **GitHub Actions**: CI/CD pipeline
- **Environment Variables**: Configuration

## Internal Architecture

### Deployment Architecture

**Confirmed by Code**: Deployment follows container-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Source Code                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              CI/CD Pipeline                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Docker Build                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Container Registry                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                           │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  Admin Portal  │  │  Database      │
│  (Backend)    │  │  (Frontend)     │  │  (PostgreSQL)   │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Docker Configuration

**Confirmed by Code**: Docker configuration for containerization.

**Dockerfile (Core API)**:
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
- **Builder Stage**: Builds application
- **Production Stage**: Production image
- **Dependencies**: Installs production dependencies
- **CMD**: Runs application

**Dockerfile (Admin Portal)**:
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
- **Static Files**: Copies build output

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

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio-data:/data

volumes:
  postgres-data:
  redis-data:
  minio-data:
```

**What This Does**:
- **core-api**: Backend API service
- **admin-portal**: Frontend admin portal
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **minio**: MinIO object storage
- **Volumes**: Persistent data storage

## Database Interactions

### Deployment-Database Flow

**Confirmed by Code**: Database deployed as container.

**Flow**:
```
Deployment → PostgreSQL Container → Database
```

## Redis Interactions

### Deployment-Redis Flow

**Confirmed by Code**: Redis deployed as container.

**Flow**:
```
Deployment → Redis Container → Cache
```

## Queue Interactions

### Deployment-Queue Flow

**Confirmed by Code**: Queue runs in same container as API.

**Flow**:
```
Deployment → Core API Container → Bull Queue
```

## Worker Interactions

### Deployment-Worker Flow

**Confirmed by Code**: Workers run in same container as API.

**Flow**:
```
Deployment → Core API Container → Workers
```

## Business Rules

### Deployment Rules

**Confirmed by Code**: Deployment follows these rules:

1. **Containerization**: All services containerized
2. **Environment Variables**: Configuration via environment variables
3. **Health Checks**: Health checks for all services
4. **Resource Limits**: Resource limits configured
5. **Persistent Storage**: Persistent storage for data

### CI/CD Rules

**Confirmed by Code**: CI/CD rules:

1. **Automated Testing**: Run tests before deployment
2. **Automated Building**: Build containers automatically
3. **Automated Deployment**: Deploy automatically on merge
4. **Rollback**: Ability to rollback
5. **Monitoring**: Monitor deployment

## Security

### Deployment Security

**Confirmed by Code**: Security considerations for deployment:

1. **Secrets Management**: Use secrets manager
2. **Environment Variables**: Don't commit secrets
3. **Network Security**: Use private networks
4. **TLS/SSL**: Use TLS in production
5. **Access Control**: Restrict access

## Performance Considerations

### Deployment Performance

**Confirmed by Code**: Performance considerations:

1. **Resource Limits**: Configure resource limits
2. **Horizontal Scaling**: Scale horizontally
3. **Load Balancing**: Use load balancer
4. **Caching**: Use caching
5. **CDN**: Use CDN for static assets

## Common Mistakes

### Mistake 1: Not Setting Resource Limits

**Symptom**: Resource exhaustion

**Cause**: Not setting resource limits

**Fix**:
```yaml
# Set resource limits
resources:
  limits:
    memory: "512Mi"
    cpu: "500m"
  requests:
    memory: "256Mi"
    cpu: "250m"
```

### Mistake 2: Not Using Persistent Storage

**Symptom**: Data loss on restart

**Cause**: Not using persistent storage

**Fix**:
```yaml
# Use persistent storage
volumes:
  - postgres-data:/var/lib/postgresql/data
```

### Mistake 3: Committing Secrets

**Symptom**: Security vulnerability

**Cause**: Committing secrets to repository

**Fix**:
```yaml
# Use environment variables
environment:
  - JWT_SECRET=${JWT_SECRET}
```

## Debugging Guide

### Deployment Debugging

**Issue**: Deployment failed

**Investigation**:
1. Check deployment logs
2. Check container logs
3. Check resource limits
4. Check configuration
5. Check network

**Tools**:
- kubectl logs
- Docker logs
- Deployment logs
- Monitoring tools

## Future Enhancements

### Kubernetes Helm Charts

**Status**: Not implemented

**Proposal**: Implement Helm charts:
- Easier deployment
- Version management
- Better configuration management
- More complex
- Better for production

### GitOps

**Status**: Not implemented

**Proposal**: Implement GitOps:
- Automated deployment
- Git-based configuration
- Better visibility
- More complex
- Better for production

## Production Considerations

### Production Deployment

**Production Deployment**:
- Use Kubernetes
- Configure resource limits
- Use secrets manager
- Enable monitoring
- Enable logging

### Deployment Monitoring

**Monitoring Metrics**:
- Deployment success rate
- Deployment duration
- Resource usage
- Error rate
- Uptime

## Example Requests

### Deployment Example

**Deploy to Kubernetes**:
```bash
kubectl apply -f k8s/
```

## Example Responses

### Deployment Response

**Response**: Deployment successful

```bash
deployment.apps/core-api created
service/core-api created
```

## Sequence Diagrams

### Deployment Flow

```
Code Push → CI/CD Pipeline → Build → Test → Deploy → Monitor
```

## Architecture Diagrams

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Source Code                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              CI/CD Pipeline                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Docker Build                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Container Registry                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                           │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is the system deployed?

**Answer**: System deployment via:
- Docker containerization
- Kubernetes orchestration
- CI/CD pipeline
- Environment configuration
- Monitoring and logging

### Q2: How do you set up CI/CD?

**Answer**: CI/CD setup via:
- GitHub Actions for CI/CD
- Automated testing
- Automated building
- Automated deployment
- Rollback capability

### Q3: How do you handle secrets in production?

**Answer**: Secrets handling via:
- Secrets manager (AWS Secrets Manager, etc.)
- Environment variables
- Not committing secrets
- Access control
- Rotation policies

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

### Scenario 1: Deployment Failed

**Situation**: Deployment failed

**Response**:
1. Check deployment logs
2. Check container logs
3. Check configuration
4. Fix issue
5. Redeploy

### Scenario 2: High Resource Usage

**Situation**: High resource usage

**Response**:
1. Check resource limits
2. Optimize application
3. Scale horizontally
4. Monitor resources
5. Adjust limits

## Navigation

**Next Section**: [01-Docker](./01-Docker.md)

**Previous Section**: [14-WebSockets](../14-WebSockets/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [17-Production](../17-Production/README.md) - Production details
