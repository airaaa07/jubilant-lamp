# Deployment Model

## Purpose

This document explains the deployment model of the University ERP system. It details the deployment strategies, environments, and deployment processes.

## Why This Document Exists

**Confirmed by Code**: The University ERP has multiple deployment options including Docker Compose and native deployment with PM2. Understanding the deployment model is critical for:
- Deploying the system to production
- Managing multiple environments
- Automating deployments
- Rolling back deployments
- Troubleshooting deployment issues

Without understanding the deployment model, deployments may fail or cause downtime.

## Where This Is Used

- **Deployment**: Deploying to production
- **Environment Management**: Managing dev/staging/production
- **CI/CD**: Automating deployments
- **Troubleshooting**: Debugging deployment issues
- **Disaster Recovery**: Recovering from failures

## Dependencies

### Deployment Dependencies

**Confirmed by Code**: Deployment depends on:

- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PM2**: Process manager for native deployment
- **Nginx**: Reverse proxy and load balancer
- **Environment Variables**: Configuration management
- **Scripts**: Deployment scripts

## Internal Architecture

### Deployment Strategies

**Confirmed by Code**: Multiple deployment strategies are supported.

```
┌─────────────────────────────────────────────────────────┐
│                  Deployment Strategies                     │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│   Docker       │  │   Native        │  │   Cloud         │
│   Compose      │  │   (PM2)         │  │   (AWS/Azure)   │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Docker Compose Deployment

**Confirmed by Code**: Docker Compose is used for local development and simple deployments.

**Architecture**:
- All services in Docker containers
- Docker Compose for orchestration
- Docker volumes for data persistence
- Docker networks for communication

**Pros**:
- Simple to deploy
- Consistent environments
- Easy to scale
- Good for small to medium deployments

**Cons**:
- Limited to single host
- Manual scaling
- Limited high availability

### Native Deployment

**Confirmed by Code**: Native deployment with PM2 is supported.

**Architecture**:
- Services run natively on OS
- PM2 for process management
- Systemd for service management
- Native database and cache

**Pros**:
- Better performance
- More control
- Can use existing infrastructure
- Lower overhead

**Cons**:
- More complex setup
- Environment inconsistencies
- Harder to scale

### Cloud Deployment

**Status**: Not fully implemented

**Proposal**: Cloud deployment on AWS or Azure.

**Architecture**:
- Container orchestration (Kubernetes)
- Managed services (RDS, ElastiCache)
- Load balancer (ALB/NLB)
- Auto-scaling groups
- CI/CD pipelines

**Pros**:
- Scalability
- High availability
- Managed services
- Better monitoring

**Cons**:
- Higher cost
- Complexity
- Vendor lock-in

## Code Walkthrough

### Docker Compose Configuration

**Confirmed by Code**: docker-compose.yml defines all services.

**Configuration**:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: university_erp
    volumes:
      - ./docker-volumes/postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - ./docker-volumes/redis:/data
    ports:
      - "6379:6379"

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - ./docker-volumes/minio:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  elasticsearch:
    image: elasticsearch:8.13.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - ./docker-volumes/elasticsearch:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

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
    depends_on:
      - postgres
      - redis
```

**What This Does**:
- Defines all infrastructure services
- Defines application services
- Configures networking
- Configures volumes
- Configures environment variables

### PM2 Configuration

**Confirmed by Code**: ecosystem.native.config.js defines PM2 configuration.

**Configuration**:
```javascript
module.exports = {
  apps: [
    {
      name: 'core-api',
      script: 'apps/core-api/dist/main.js',
      instances: 2,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'development',
        PORT: 3000,
      },
      env_production: {
        NODE_ENV: 'production',
        PORT: 3000,
      },
    },
    {
      name: 'cbe-engine',
      script: 'apps/cbe-engine/dist/main.js',
      instances: 1,
      env: {
        NODE_ENV: 'development',
        PORT: 3001,
      },
    },
    {
      name: 'notification-worker',
      script: 'apps/notification-worker/dist/main.js',
      instances: 2,
      env: {
        NODE_ENV: 'development',
        PORT: 3002,
      },
    },
    {
      name: 'cert-generator',
      script: 'apps/cert-generator/dist/main.js',
      instances: 1,
      env: {
        NODE_ENV: 'development',
        PORT: 3003,
      },
    },
  ],
};
```

**What This Does**:
- Defines application processes
- Configures cluster mode
- Configures environment variables
- Configures instances
- Enables auto-restart

## Database Interactions

### Database Deployment

**Confirmed by Code**: Database deployment strategies.

**Docker Deployment**:
- PostgreSQL in Docker container
- Volume for data persistence
- Environment variables for configuration

**Native Deployment**:
- PostgreSQL installed on host
- Systemd for service management
- Configuration files in /etc/postgresql

**Cloud Deployment**:
- Managed PostgreSQL (AWS RDS, Azure Database)
- Automated backups
- High availability
- Read replicas

## Redis Interactions

### Redis Deployment

**Confirmed by Code**: Redis deployment strategies.

**Docker Deployment**:
- Redis in Docker container
- Volume for data persistence
- AOF persistence enabled

**Native Deployment**:
- Redis installed on host
- Systemd for service management
- Configuration files in /etc/redis

**Cloud Deployment**:
- Managed Redis (ElastiCache, Azure Cache)
- Clustering
- High availability
- Automatic failover

## Queue Interactions

### Queue Deployment

**Confirmed by Code**: Bull queues use Redis as backend.

**Deployment Considerations**:
- Redis must be deployed before workers
- Workers must connect to same Redis
- Queue data persists in Redis
- Dead letter queue for failed jobs

## Worker Interactions

### Worker Deployment

**Confirmed by Code**: Workers deployed as separate services.

**Docker Deployment**:
- Workers in Docker containers
- Separate services in docker-compose.yml
- Can scale independently

**Native Deployment**:
- Workers as PM2 processes
- Separate apps in ecosystem config
- Can scale independently

**Cloud Deployment**:
- Workers as separate services
- Auto-scaling groups
- Load balanced

## Business Rules

### Deployment Rules

**Confirmed by Code**: Deployment follows these rules:

1. **Environment-Specific Config**: Different configs for dev/staging/prod
2. **Database Migrations**: Run migrations before deployment
3. **Health Checks**: Verify health after deployment
4. **Rollback**: Ability to rollback on failure
5. **Zero Downtime**: Minimize downtime during deployment

### Environment Rules

**Confirmed by Code**: Environment-specific rules:

1. **Development**: Docker Compose, hot-reload, detailed logging
2. **Staging**: Docker Compose, production-like, testing
3. **Production**: Native or cloud, optimized, minimal logging

## Security

### Deployment Security

**Confirmed by Code**: Security considerations for deployment:

1. **Secrets Management**: Use secrets manager in production
2. **HTTPS**: Enable HTTPS in production
3. **Firewall**: Restrict access to necessary ports
4. **Network Isolation**: Use private networks
5. **Container Security**: Use minimal images, scan for vulnerabilities

## Performance Considerations

### Deployment Performance

**Confirmed by Code**: Performance considerations for deployment:

1. **Resource Allocation**: Allocate sufficient resources
2. **Connection Pooling**: Configure connection pools
3. **Caching**: Configure Redis caching
4. **Load Balancing**: Use load balancer for scaling
5. **Monitoring**: Monitor performance metrics

## Common Mistakes

### Mistake 1: Not Running Migrations

**Symptom**: Deployment fails with database errors

**Cause**: Migrations not run before deployment

**Fix**:
```bash
# Always run migrations before deployment
cd apps/core-api
npx prisma migrate deploy
```

### Mistake 2: Wrong Environment Variables

**Symptom**: Application fails to start

**Cause**: Wrong environment variables for environment

**Fix**:
```bash
# Use correct environment file
cp .env.production .env
# Verify variables
```

### Mistake 3: Not Scaling Workers

**Symptom**: Background jobs delayed

**Cause**: Insufficient worker capacity

**Fix**:
```yaml
# Scale workers in docker-compose.yml
notification-worker:
  deploy:
    replicas: 3
```

## Debugging Guide

### Deployment Debugging

**Issue**: Deployment fails

**Investigation**:
1. Check deployment logs
2. Check environment variables
3. Check database connection
4. Check service health
5. Check resource usage

**Tools**:
- Docker logs
- PM2 logs
- Application logs
- System logs

## Future Enhancements

### Kubernetes Deployment

**Status**: Not implemented

**Proposal**: Deploy on Kubernetes:
- Helm charts for deployment
- ConfigMaps for configuration
- Secrets for sensitive data
- Ingress for routing
- HPA for auto-scaling

### CI/CD Pipeline

**Status**: Not implemented

**Proposal**: Implement CI/CD pipeline:
- GitHub Actions or GitLab CI
- Automated testing
- Automated deployment
- Rollback capability

## Production Considerations

### Production Deployment

**Production Deployment Process**:
1. Run tests
2. Build artifacts
3. Run migrations on staging
4. Deploy to staging
5. Test on staging
6. Run migrations on production
7. Deploy to production
8. Verify health
9. Monitor for issues

### Rollback Strategy

**Rollback Process**:
1. Identify issue
2. Stop new deployment
3. Revert to previous version
4. Run rollback migrations (if needed)
5. Verify health
6. Monitor for issues

## Example Requests

### Deploy with Docker Compose

**Request**:
```bash
docker-compose up -d
```

**Response**:
```
Creating network "university-erp_default"
Creating volume "university-erp_postgres"
Creating volume "university-erp_redis"
Creating postgres ... done
Creating redis ... done
Creating core-api ... done
```

### Deploy with PM2

**Request**:
```bash
pm2 start ecosystem.native.config.js --env production
```

**Response**:
```
[PM2] Starting applications in production mode...
[PM2] App [core-api] launched (2 instances)
[PM2] App [cbe-engine] launched (1 instance)
[PM2] App [notification-worker] launched (2 instances)
[PM2] App [cert-generator] launched (1 instance)
```

## Example Responses

### Health Check

**Request**:
```bash
curl http://localhost:3000/health
```

**Response**:
```json
{
  "status": "ok",
  "database": "connected",
  "redis": "connected",
  "minio": "connected",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Sequence Diagrams

### Deployment Flow

```
Developer → Build Artifacts
              ↓
          Run Tests
              ↓
          Run Migrations
              ↓
          Deploy Services
              ↓
          Verify Health
              ↓
          Monitor
```

### Rollback Flow

```
Issue Detected → Stop Deployment
                    ↓
                Revert Version
                    ↓
                Rollback Migrations
                    ↓
                Verify Health
                    ↓
                Monitor
```

## Architecture Diagrams

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Load Balancer (Nginx)                    │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API 1    │  │  Core API 2    │  │  Core API 3    │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ Notification  │  │ Cert Generator │  │  CBE Engine    │
│   Worker      │  │                │  │                │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ PostgreSQL    │  │   Redis         │  │   MinIO        │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What deployment strategies does the system support?

**Answer**: The system supports:
- Docker Compose for local and simple deployments
- Native deployment with PM2 for production
- Cloud deployment (AWS/Azure) for scalability
- Each strategy has pros and cons

### Q2: How do you handle database migrations during deployment?

**Answer**: Migrations are handled via:
- Prisma migrations
- Run migrations before deployment
- Test migrations on staging first
- Rollback capability if migration fails
- Zero-downtime deployment strategy

### Q3: How do you ensure zero downtime during deployment?

**Answer**: Zero downtime via:
- Load balancer with health checks
- Rolling updates (one instance at a time)
- Blue-green deployment
- Database migrations backward compatible
- Health checks before traffic routing

## Exercises

### Exercise 1: Deploy with Docker Compose

**Task**: Deploy the system using Docker Compose.

**Steps**:
1. Clone repository
2. Configure environment variables
3. Start Docker services
4. Run migrations
5. Seed database
6. Start application services
7. Verify health

**Verification**:
- All services running
- Health check passes
- Application accessible

### Exercise 2: Deploy with PM2

**Task**: Deploy the system using PM2.

**Steps**:
1. Install dependencies
2. Build application
3. Configure PM2
4. Start services with PM2
5. Verify health
6. Configure startup script

**Verification**:
- All services running
- PM2 status healthy
- Application accessible

## Real Production Scenarios

### Scenario 1: Deployment Failure

**Situation**: Deployment fails with database errors

**Response**:
1. Check deployment logs
2. Check database connection
3. Check migration status
4. Rollback if needed
4. Fix issue
5. Retry deployment

### Scenario 2: Performance Degradation After Deployment

**Situation**: Performance degraded after deployment

**Response**:
1. Monitor metrics
2. Identify bottleneck
3. Rollback if critical
4. Optimize if non-critical
5. Monitor after fix

## Navigation

**Next Section**: [10-Development-Workflow](./10-Development-Workflow.md)

**Previous Section**: [08-Scalability-Model](./08-Scalability-Model.md)

**Related Documentation**:
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [15-Deployment](../15-Deployment/README.md) - Deployment details
- [17-Production](../17-Production/README.md) - Production guide
