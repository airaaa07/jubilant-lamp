# 02-Infrastructure

## Purpose

This folder provides comprehensive documentation about the infrastructure of the University ERP system. It explains the Docker Compose setup, native deployment, networking, storage, and all infrastructure components.

## Why This Folder Exists

**Confirmed by Code**: The University ERP infrastructure includes Docker services, databases, caches, object storage, and more. Understanding the infrastructure is critical for:
- Setting up the development environment
- Deploying to production
- Troubleshooting infrastructure issues
- Scaling the infrastructure
- Managing infrastructure costs

Without understanding the infrastructure, developers may struggle with setup, deployment, or troubleshooting.

## Where This Is Used

- **Onboarding**: New developers learn infrastructure setup
- **Development**: Setting up local development environment
- **Deployment**: Deploying to production
- **Troubleshooting**: Debugging infrastructure issues
- **Scaling**: Planning infrastructure scaling

## Dependencies

### Infrastructure Dependencies

**Confirmed by Code**: The infrastructure depends on:

- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL**: Relational database
- **Redis**: In-memory data store
- **MinIO**: Object storage
- **Elasticsearch**: Search engine
- **Nginx**: Reverse proxy and load balancer

## Internal Architecture

### Infrastructure Overview

**Confirmed by Code**: The infrastructure consists of multiple services.

```
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure                            │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Application   │  │  Data Layer     │  │  Storage Layer  │
│  Services     │  │                 │  │                 │
│  (Core API,   │  │  PostgreSQL     │  │  MinIO         │
│   CBE Engine, │  │  Redis          │  │                 │
│   Workers)    │  │  Elasticsearch  │  │                 │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Docker Compose Architecture

**Confirmed by Code**: docker-compose.yml defines all infrastructure services.

**Services**:
- **PostgreSQL**: Relational database
- **Redis**: In-memory data store and queue backend
- **MinIO**: Object storage (S3-compatible)
- **Elasticsearch**: Search engine
- **Nginx**: Reverse proxy and load balancer (optional)

## Code Walkthrough

### Docker Compose Configuration

**Confirmed by Code**: docker-compose.yml in project root.

**PostgreSQL Service**:
```yaml
postgres:
  image: postgres:16-alpine
  container_name: university-erp-postgres
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: university_erp
  volumes:
    - ./docker-volumes/postgres:/var/lib/postgresql/data
  ports:
    - "5432:5432"
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**What This Does**:
- Runs PostgreSQL 16 Alpine image
- Sets database credentials
- Mounts volume for data persistence
- Exposes port 5432
- Configures health check

**Redis Service**:
```yaml
redis:
  image: redis:7-alpine
  container_name: university-erp-redis
  command: redis-server --appendonly yes
  volumes:
    - ./docker-volumes/redis:/data
  ports:
    - "6379:6379"
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**What This Does**:
- Runs Redis 7 Alpine image
- Enables AOF persistence
- Mounts volume for data persistence
- Exposes port 6379
- Configures health check

**MinIO Service**:
```yaml
minio:
  image: minio/minio:latest
  container_name: university-erp-minio
  command: server /data --console-address ":9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  volumes:
    - ./docker-volumes/minio:/data
  ports:
    - "9000:9000"
    - "9001:9001"
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**What This Does**:
- Runs MinIO latest image
- Configures MinIO server and console
- Sets MinIO credentials
- Mounts volume for data persistence
- Exposes ports 9000 (API) and 9001 (Console)
- Configures health check

**Elasticsearch Service**:
```yaml
elasticsearch:
  image: elasticsearch:8.13.0
  container_name: university-erp-elasticsearch
  environment:
    - discovery.type=single-node
    - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    - xpack.security.enabled=false
  volumes:
    - ./docker-volumes/elasticsearch:/usr/share/elasticsearch/data
  ports:
    - "9200:9200"
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
    interval: 10s
    timeout: 5s
    retries: 5
```

**What This Does**:
- Runs Elasticsearch 8.13.0
- Configures single-node discovery
- Sets JVM memory options
- Disables security (development only)
- Mounts volume for data persistence
- Exposes port 9200
- Configures health check

## Database Interactions

### PostgreSQL Infrastructure

**Confirmed by Code**: PostgreSQL is the primary database.

**Connection**:
```bash
# From host
docker-compose exec postgres psql -U postgres -d university_erp

# From application
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
```

**Backup**:
```bash
# Backup
docker-compose exec postgres pg_dump -U postgres university_erp > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres university_erp < backup.sql
```

**Volume**:
- **Location**: `./docker-volumes/postgres`
- **Purpose**: Data persistence
- **Backup**: Should be backed up regularly

## Redis Interactions

### Redis Infrastructure

**Confirmed by Code**: Redis is used for caching and queues.

**Connection**:
```bash
# From host
docker-compose exec redis redis-cli

# From application
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Persistence**:
- **Mode**: AOF (Append Only File)
- **Volume**: `./docker-volumes/redis`
- **Purpose**: Data persistence

**Monitoring**:
```bash
# Monitor commands
docker-compose exec redis redis-cli monitor

# Check memory
docker-compose exec redis redis-cli INFO memory
```

## Queue Interactions

### Bull Queue Infrastructure

**Confirmed by Code**: Bull queues use Redis as backend.

**Configuration**:
```typescript
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});
```

**Monitoring**:
```bash
# Check queue status
docker-compose exec redis redis-cli KEYS "bull:*"
```

## Worker Interactions

### Worker Infrastructure

**Confirmed by Code**: Workers are separate services.

**Notification Worker**:
```yaml
notification-worker:
  build:
    context: ./apps/notification-worker
    dockerfile: Dockerfile
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
    - REDIS_HOST=redis
    - REDIS_PORT=6379
  depends_on:
    - postgres
    - redis
```

**Certificate Generator**:
```yaml
cert-generator:
  build:
    context: ./apps/cert-generator
    dockerfile: Dockerfile
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
    - REDIS_HOST=redis
    - REDIS_PORT=6379
    - MINIO_ENDPOINT=minio:9000
  depends_on:
    - postgres
    - redis
    - minio
```

## Business Rules

### Infrastructure Rules

**Confirmed by Code**: Infrastructure follows these rules:

1. **Data Persistence**: All data services use volumes
2. **Health Checks**: All services have health checks
3. **Networking**: Services communicate via Docker network
4. **Environment Variables**: Configuration via environment variables
5. **Resource Limits**: Configure resource limits in production

### Volume Rules

**Confirmed by Code**: Volumes are used for data persistence.

**Volumes**:
- `./docker-volumes/postgres`: PostgreSQL data
- `./docker-volumes/redis`: Redis data
- `./docker-volumes/minio`: MinIO data
- `./docker-volumes/elasticsearch`: Elasticsearch data

**Backup Strategy**:
- Regular backups of all volumes
- Off-site backup storage
- Backup encryption
- Backup verification

## Security

### Infrastructure Security

**Confirmed by Code**: Security considerations for infrastructure:

1. **Default Credentials**: Change default credentials in production
2. **Network Isolation**: Use private networks
3. **Firewall**: Restrict exposed ports
4. **TLS**: Enable TLS for all services
5. **Secrets Management**: Use secrets manager in production

## Performance Considerations

### Infrastructure Performance

**Confirmed by Code**: Performance considerations for infrastructure:

1. **Resource Allocation**: Allocate sufficient resources
2. **Connection Pooling**: Configure connection pools
3. **Caching**: Configure Redis caching
4. **Indexing**: Configure database indexes
5. **Load Balancing**: Use load balancer for scaling

## Common Mistakes

### Mistake 1: Not Using Volumes

**Symptom**: Data lost on container restart

**Cause**: Not using volumes for data persistence

**Fix**:
```yaml
# Wrong
postgres:
  image: postgres:16-alpine

# Correct
postgres:
  image: postgres:16-alpine
  volumes:
    - ./docker-volumes/postgres:/var/lib/postgresql/data
```

### Mistake 2: Not Configuring Health Checks

**Symptom**: Unhealthy services not detected

**Cause**: Not configuring health checks

**Fix**:
```yaml
# Add health check
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Mistake 3: Exposing All Ports

**Symptom**: Security risk

**Cause**: Exposing all ports to host

**Fix**:
```yaml
# Only expose necessary ports
ports:
  - "5432:5432"  # PostgreSQL
  - "6379:6379"  # Redis
```

## Debugging Guide

### Infrastructure Debugging

**Issue**: Service not starting

**Investigation**:
1. Check service logs: `docker-compose logs <service>`
2. Check service status: `docker-compose ps`
3. Check resource usage: `docker stats`
4. Check network: `docker network inspect`
5. Check volumes: `docker volume ls`

**Tools**:
- Docker logs
- Docker stats
- Docker inspect
- Service-specific tools (psql, redis-cli)

## Future Enhancements

### Kubernetes Deployment

**Status**: Not implemented

**Proposal**: Deploy on Kubernetes:
- Helm charts for deployment
- ConfigMaps for configuration
- Secrets for sensitive data
- Persistent volumes for data
- Horizontal Pod Autoscaler

### Managed Services

**Status**: Not implemented

**Proposal**: Use managed services:
- AWS RDS for PostgreSQL
- AWS ElastiCache for Redis
- AWS S3 for object storage
- AWS Elasticsearch for search

## Production Considerations

### Production Infrastructure

**Production Deployment**:
- Use managed services
- Enable TLS/SSL
- Configure resource limits
- Implement monitoring
- Implement logging
- Implement backup strategy
- Implement disaster recovery

### Infrastructure Monitoring

**Monitoring Metrics**:
- CPU usage
- Memory usage
- Disk usage
- Network traffic
- Database connections
- Cache hit rate
- Queue backlog

## Example Requests

### Start Infrastructure

**Request**:
```bash
docker-compose up -d
```

**Response**:
```
Creating network "university-erp_default"
Creating volume "university-erp_postgres"
Creating volume "university-erp_redis"
Creating volume "university-erp_minio"
Creating volume "university-erp_elasticsearch"
Creating postgres ... done
Creating redis ... done
Creating minio ... done
Creating elasticsearch ... done
```

### Stop Infrastructure

**Request**:
```bash
docker-compose down
```

**Response**:
```
Stopping postgres ... done
Stopping redis ... done
Stopping minio ... done
Stopping elasticsearch ... done
Removing postgres ... done
Removing redis ... done
Removing minio ... done
Removing elasticsearch ... done
```

## Example Responses

### Service Status

**Request**:
```bash
docker-compose ps
```

**Response**:
```
NAME                          STATUS
university-erp-postgres       Up (healthy)
university-erp-redis          Up (healthy)
university-erp-minio          Up (healthy)
university-erp-elasticsearch  Up (healthy)
```

## Sequence Diagrams

### Infrastructure Startup

```
Docker Compose → Start Services
                     ↓
                 Start PostgreSQL
                     ↓
                 Start Redis
                     ↓
                 Start MinIO
                     ↓
                 Start Elasticsearch
                     ↓
                 Wait for Health Checks
                     ↓
                 Services Ready
```

## Architecture Diagrams

### Infrastructure Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Host                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  CBE Engine    │  │  Workers        │
│  (Container)   │  │  (Container)   │  │  (Containers)   │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL    │  │   Redis         │  │   MinIO        │
│  (Container)   │  │   (Container)   │  │   (Container)   │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Docker Volume│  │  Docker Volume  │  │  Docker Volume  │
│  (Postgres)   │  │  (Redis)       │  │  (MinIO)       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What infrastructure services does the system use?

**Answer**: The system uses:
- PostgreSQL for relational database
- Redis for caching and queue backend
- MinIO for object storage
- Elasticsearch for search
- Nginx for reverse proxy and load balancing

### Q2: How is data persistence handled?

**Answer**: Data persistence via Docker volumes:
- PostgreSQL data in `./docker-volumes/postgres`
- Redis data in `./docker-volumes/redis`
- MinIO data in `./docker-volumes/minio`
- Elasticsearch data in `./docker-volumes/elasticsearch`

### Q3: How do you backup the infrastructure?

**Answer**: Backup via:
- PostgreSQL: `pg_dump` command
- Redis: `SAVE` command or AOF file
- MinIO: `mc mirror` command
- Elasticsearch: Snapshot API
- Docker volumes: Copy volume directory

## Exercises

### Exercise 1: Start Infrastructure

**Task**: Start all infrastructure services.

**Steps**:
1. Navigate to project root
2. Run `docker-compose up -d`
3. Check service status
4. Verify health checks

**Verification**:
- All services running
- All services healthy
- Services accessible

### Exercise 2: Backup Database

**Task**: Backup PostgreSQL database.

**Steps**:
1. Run `pg_dump` command
2. Save to file
3. Verify backup
4. Test restore

**Verification**:
- Backup created
- Backup valid
- Restore works

## Real Production Scenarios

### Scenario 1: Database Failure

**Situation**: PostgreSQL container fails

**Response**:
1. Check logs
2. Restart container
3. If data corrupted, restore from backup
4. Verify data integrity
5. Monitor for recurrence

### Scenario 2: Disk Space Full

**Situation**: Docker volumes filling disk

**Response**:
1. Check disk usage
2. Clean up old data
3. Add more disk space
4. Implement log rotation
5. Implement data retention policy

## Navigation

**Next Section**: [01-Docker-Services](./01-Docker-Services.md)

**Previous Section**: [01-System-Architecture](../01-System-Architecture/README.md)

**Related Documentation**:
- [00-Getting-Started](../00-Getting-Started/README.md) - Getting started
- [15-Deployment](../15-Deployment/README.md) - Deployment details
- [17-Production](../17-Production/README.md) - Production guide
