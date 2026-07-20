# Docker Services

## Purpose

This document provides detailed information about each Docker service used in the University ERP system. It explains the configuration, purpose, and management of each service.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses multiple Docker services for infrastructure. Understanding each service is critical for:
- Managing infrastructure
- Troubleshooting service issues
- Configuring services correctly
- Optimizing service performance
- Scaling services appropriately

Without understanding each Docker service, infrastructure management becomes difficult.

## Where This Is Used

- **Development**: Setting up local development environment
- **Deployment**: Deploying to production
- **Troubleshooting**: Debugging service issues
- **Configuration**: Configuring service parameters
- **Scaling**: Planning service scaling

## Dependencies

### Docker Service Dependencies

**Confirmed by Code**: Docker services depend on:

- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration
- **Docker Networks**: Service communication
- **Docker Volumes**: Data persistence

## Internal Architecture

### Service Overview

**Confirmed by Code**: The system uses these Docker services:

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Services                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL    │  │   Redis         │  │   MinIO        │
│  Port: 5432    │  │   Port: 6379    │  │   Port: 9000    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ Elasticsearch  │  │   Nginx         │  │   Application   │
│  Port: 9200    │  │   Port: 80/443  │  │   Services      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### PostgreSQL Service

**Confirmed by Code**: PostgreSQL service in docker-compose.yml.

**Configuration**:
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
  restart: unless-stopped
```

**Purpose**: Relational database for the application.

**Configuration Details**:
- **Image**: postgres:16-alpine (lightweight PostgreSQL 16)
- **Container Name**: university-erp-postgres
- **Environment Variables**:
  - `POSTGRES_USER`: Database user (postgres)
  - `POSTGRES_PASSWORD`: Database password (postgres)
  - `POSTGRES_DB`: Database name (university_erp)
- **Volumes**: `./docker-volumes/postgres:/var/lib/postgresql/data` (data persistence)
- **Ports**: `5432:5432` (host:container)
- **Health Check**: Checks if PostgreSQL is ready
- **Restart Policy**: unless-stopped (auto-restart unless stopped manually)

**Management Commands**:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Stop PostgreSQL
docker-compose stop postgres

# Restart PostgreSQL
docker-compose restart postgres

# View logs
docker-compose logs -f postgres

# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d university_erp

# Backup database
docker-compose exec postgres pg_dump -U postgres university_erp > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres university_erp < backup.sql
```

### Redis Service

**Confirmed by Code**: Redis service in docker-compose.yml.

**Configuration**:
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
  restart: unless-stopped
```

**Purpose**: In-memory data store for caching and queue backend.

**Configuration Details**:
- **Image**: redis:7-alpine (lightweight Redis 7)
- **Container Name**: university-erp-redis
- **Command**: `redis-server --appendonly yes` (enables AOF persistence)
- **Volumes**: `./docker-volumes/redis:/data` (data persistence)
- **Ports**: `6379:6379` (host:container)
- **Health Check**: Pings Redis to check if it's responding
- **Restart Policy**: unless-stopped

**Management Commands**:
```bash
# Start Redis
docker-compose up -d redis

# Stop Redis
docker-compose stop redis

# Restart Redis
docker-compose restart redis

# View logs
docker-compose logs -f redis

# Connect to Redis
docker-compose exec redis redis-cli

# Monitor Redis commands
docker-compose exec redis redis-cli monitor

# Check Redis memory
docker-compose exec redis redis-cli INFO memory

# Flush all data (WARNING: deletes all data)
docker-compose exec redis redis-cli FLUSHALL
```

### MinIO Service

**Confirmed by Code**: MinIO service in docker-compose.yml.

**Configuration**:
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
  restart: unless-stopped
```

**Purpose**: S3-compatible object storage for files and documents.

**Configuration Details**:
- **Image**: minio/minio:latest
- **Container Name**: university-erp-minio
- **Command**: `server /data --console-address ":9001"` (starts MinIO server and console)
- **Environment Variables**:
  - `MINIO_ROOT_USER`: MinIO access key (minioadmin)
  - `MINIO_ROOT_PASSWORD`: MinIO secret key (minioadmin)
- **Volumes**: `./docker-volumes/minio:/data` (data persistence)
- **Ports**:
  - `9000:9000` (MinIO API)
  - `9001:9001` (MinIO Console)
- **Health Check**: Checks MinIO health endpoint
- **Restart Policy**: unless-stopped

**Management Commands**:
```bash
# Start MinIO
docker-compose up -d minio

# Stop MinIO
docker-compose stop minio

# Restart MinIO
docker-compose restart minio

# View logs
docker-compose logs -f minio

# Access MinIO Console
# Open browser to http://localhost:9001
# Login with minioadmin/minioadmin

# Create bucket using mc CLI
docker-compose exec minio mc alias set local http://localhost:9000 minioadmin minioadmin
docker-compose exec minio mc mb local/university-erp-docs
docker-compose exec minio mc mb local/university-erp-exams

# List buckets
docker-compose exec minio mc ls local

# Upload file
docker-compose exec minio mc cp /path/to/file local/university-erp-docs/

# Download file
docker-compose exec minio mc cp local/university-erp-docs/file /path/to/destination
```

### Elasticsearch Service

**Confirmed by Code**: Elasticsearch service in docker-compose.yml.

**Configuration**:
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
  restart: unless-stopped
```

**Purpose**: Search engine for full-text search and analytics.

**Configuration Details**:
- **Image**: elasticsearch:8.13.0
- **Container Name**: university-erp-elasticsearch
- **Environment Variables**:
  - `discovery.type=single-node`: Single-node discovery (development)
  - `ES_JAVA_OPTS=-Xms512m -Xmx512m`: JVM memory settings
  - `xpack.security.enabled=false`: Disable security (development only)
- **Volumes**: `./docker-volumes/elasticsearch:/usr/share/elasticsearch/data` (data persistence)
- **Ports**: `9200:9200` (Elasticsearch API)
- **Health Check**: Checks cluster health
- **Restart Policy**: unless-stopped

**Management Commands**:
```bash
# Start Elasticsearch
docker-compose up -d elasticsearch

# Stop Elasticsearch
docker-compose stop elasticsearch

# Restart Elasticsearch
docker-compose restart elasticsearch

# View logs
docker-compose logs -f elasticsearch

# Check cluster health
curl http://localhost:9200/_cluster/health

# Check node info
curl http://localhost:9200/_nodes

# List indices
curl http://localhost:9200/_cat/indices?v

# Create index
curl -X PUT http://localhost:9200/my-index

# Delete index
curl -X DELETE http://localhost:9200/my-index
```

### Nginx Service

**Status**: Optional service (not in docker-compose.yml)

**Purpose**: Reverse proxy and load balancer.

**Configuration**:
```yaml
nginx:
  image: nginx:alpine
  container_name: university-erp-nginx
  volumes:
    - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
    - ./docker/nginx/ssl:/etc/nginx/ssl
  ports:
    - "80:80"
    - "443:443"
  depends_on:
    - core-api
    - admin-portal
  restart: unless-stopped
```

**Configuration Details**:
- **Image**: nginx:alpine
- **Container Name**: university-erp-nginx
- **Volumes**:
  - `./docker/nginx/nginx.conf:/etc/nginx/nginx.conf` (Nginx configuration)
  - `./docker/nginx/ssl:/etc/nginx/ssl` (SSL certificates)
- **Ports**:
  - `80:80` (HTTP)
  - `443:443` (HTTPS)
- **Depends On**: core-api, admin-portal
- **Restart Policy**: unless-stopped

**Management Commands**:
```bash
# Start Nginx
docker-compose up -d nginx

# Stop Nginx
docker-compose stop nginx

# Restart Nginx
docker-compose restart nginx

# Reload Nginx configuration
docker-compose exec nginx nginx -s reload

# Test Nginx configuration
docker-compose exec nginx nginx -t

# View logs
docker-compose logs -f nginx
```

## Database Interactions

### PostgreSQL Service Interactions

**Confirmed by Code**: Application connects to PostgreSQL via DATABASE_URL.

**Connection String**:
```
postgresql://postgres:postgres@localhost:5432/university_erp
```

**Connection from Application**:
```typescript
// apps/core-api/src/database/prisma.service.ts
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
});
```

## Redis Interactions

### Redis Service Interactions

**Confirmed by Code**: Application connects to Redis via REDIS_HOST and REDIS_PORT.

**Connection from Application**:
```typescript
// apps/core-api/src/infrastructure/redis/redis.service.ts
const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
});
```

## Queue Interactions

### Bull Queue Interactions

**Confirmed by Code**: Bull queues use Redis as backend.

**Connection from Application**:
```typescript
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});
```

## Worker Interactions

### Worker Service Interactions

**Confirmed by Code**: Workers connect to same Redis and PostgreSQL.

**Connection from Workers**:
```typescript
// Workers use same environment variables
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
REDIS_HOST=redis
REDIS_PORT=6379
```

## Business Rules

### Service Management Rules

**Confirmed by Code**: Service management follows these rules:

1. **Data Persistence**: All data services use volumes
2. **Health Checks**: All services have health checks
3. **Restart Policy**: Services auto-restart unless stopped
4. **Networking**: Services communicate via Docker network
5. **Environment Variables**: Configuration via environment variables

### Service Startup Order

**Confirmed by Code**: Services have dependencies defined.

**Startup Order**:
1. PostgreSQL (no dependencies)
2. Redis (no dependencies)
3. MinIO (no dependencies)
4. Elasticsearch (no dependencies)
5. Core API (depends on PostgreSQL, Redis)
6. CBE Engine (depends on PostgreSQL, Redis)
7. Notification Worker (depends on PostgreSQL, Redis)
8. Certificate Generator (depends on PostgreSQL, Redis, MinIO)
9. Nginx (depends on Core API, Admin Portal)

## Security

### Service Security

**Confirmed by Code**: Security considerations for services:

1. **Default Credentials**: Change default credentials in production
2. **Network Isolation**: Use private networks
3. **Firewall**: Restrict exposed ports
4. **TLS**: Enable TLS for all services
5. **Secrets Management**: Use secrets manager in production

## Performance Considerations

### Service Performance

**Confirmed by Code**: Performance considerations for services:

1. **Resource Limits**: Configure resource limits in production
2. **Connection Pooling**: Configure connection pools
3. **Caching**: Configure Redis caching
4. **Indexing**: Configure database indexes
5. **Load Balancing**: Use load balancer for scaling

## Common Mistakes

### Mistake 1: Not Configuring Health Checks

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

### Mistake 2: Not Using Volumes

**Symptom**: Data lost on container restart

**Cause**: Not using volumes for data persistence

**Fix**:
```yaml
# Add volume
volumes:
  - ./docker-volumes/postgres:/var/lib/postgresql/data
```

### Mistake 3: Exposing All Ports

**Symptom**: Security risk

**Cause**: Exposing all ports to host

**Fix**:
```yaml
# Only expose necessary ports
ports:
  - "5432:5432"
```

## Debugging Guide

### Service Debugging

**Issue**: Service not starting

**Investigation**:
1. Check service logs: `docker-compose logs <service>`
2. Check service status: `docker-compose ps`
3. Check resource usage: `docker stats`
4. Check configuration: `docker-compose config`

**Tools**:
- Docker logs
- Docker stats
- Docker inspect
- Service-specific tools (psql, redis-cli)

## Future Enhancements

### Service Monitoring

**Status**: Not implemented

**Proposal**: Implement service monitoring:
- Prometheus for metrics collection
- Grafana for visualization
- Alerting for service failures
- Dashboard for service health

### Service Auto-Scaling

**Status**: Not implemented

**Proposal**: Implement auto-scaling:
- Kubernetes HPA
- Docker Swarm scaling
- Auto-scale based on metrics
- Scale up/down based on load

## Production Considerations

### Production Services

**Production Deployment**:
- Use managed services (AWS RDS, ElastiCache, S3)
- Configure resource limits
- Enable TLS/SSL
- Configure backups
- Configure monitoring
- Configure logging

### Service Backup

**Backup Strategy**:
- PostgreSQL: Automated daily backups
- Redis: AOF persistence + snapshots
- MinIO: Versioning + lifecycle policies
- Elasticsearch: Snapshots

## Example Requests

### Start All Services

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

### Service Startup

```
Docker Compose → Start PostgreSQL
                     ↓
                 Wait for Health Check
                     ↓
                 Start Redis
                     ↓
                 Wait for Health Check
                     ↓
                 Start MinIO
                     ↓
                 Wait for Health Check
                     ↓
                 Start Elasticsearch
                     ↓
                 Wait for Health Check
                     ↓
                 Start Application Services
```

## Architecture Diagrams

### Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Network                            │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL    │  │   Redis         │  │   MinIO        │
│  5432          │  │   6379          │  │   9000, 9001    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ Elasticsearch  │  │   Core API      │  │   Workers      │
│  9200          │  │   3000          │  │   3002, 3003    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What Docker services does the system use?

**Answer**: The system uses:
- PostgreSQL for relational database
- Redis for caching and queue backend
- MinIO for object storage
- Elasticsearch for search
- Nginx for reverse proxy and load balancing

### Q2: How is data persistence handled in Docker services?

**Answer**: Data persistence via Docker volumes:
- PostgreSQL: `./docker-volumes/postgres`
- Redis: `./docker-volumes/redis`
- MinIO: `./docker-volumes/minio`
- Elasticsearch: `./docker-volumes/elasticsearch`

### Q3: How do you monitor Docker services?

**Answer**: Monitoring via:
- Docker Compose: `docker-compose ps`
- Docker Logs: `docker-compose logs -f <service>`
- Docker Stats: `docker stats`
- Health Checks: Built-in health checks
- Future: Prometheus + Grafana

## Exercises

### Exercise 1: Manage PostgreSQL Service

**Task**: Start, stop, and restart PostgreSQL service.

**Steps**:
1. Start PostgreSQL
2. Check status
3. View logs
4. Stop PostgreSQL
5. Restart PostgreSQL
6. Verify connection

**Verification**:
- Service starts correctly
- Service stops correctly
- Service restarts correctly
- Connection works

### Exercise 2: Manage Redis Service

**Task**: Connect to Redis and perform operations.

**Steps**:
1. Start Redis
2. Connect to Redis CLI
3. Set a key
4. Get the key
5. Delete the key
6. Flush all data

**Verification**:
- Connection works
- Operations work
- Data persists

## Real Production Scenarios

### Scenario 1: PostgreSQL Container Fails

**Situation**: PostgreSQL container crashes

**Response**:
1. Check logs: `docker-compose logs postgres`
2. Restart container: `docker-compose restart postgres`
3. If data corrupted, restore from backup
4. Verify data integrity
5. Monitor for recurrence

### Scenario 2: Redis Memory Full

**Situation**: Redis runs out of memory

**Response**:
1. Check memory: `docker-compose exec redis redis-cli INFO memory`
2. Flush data if acceptable: `docker-compose exec redis redis-cli FLUSHALL`
3. Configure maxmemory in redis.conf
4. Configure eviction policy
5. Monitor memory usage

## Navigation

**Next Section**: [02-Networking](./02-Networking.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [00-Getting-Started](../00-Getting-Started/README.md) - Getting started
- [15-Deployment](../15-Deployment/README.md) - Deployment details
- [17-Production](../17-Production/README.md) - Production guide
