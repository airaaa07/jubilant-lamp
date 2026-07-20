# University ERP - Infrastructure

## Overview

The system uses **Docker Compose** for local development and **PM2** for native deployment. Infrastructure services include PostgreSQL, Redis, MinIO, Elasticsearch, and Nginx.

## Technology Stack

- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PM2**: Process manager for native deployment
- **Nginx**: Reverse proxy and load balancer
- **PostgreSQL 16**: Database
- **Redis 7**: Cache and queue backend
- **MinIO**: Object storage
- **Elasticsearch 8.13**: Search engine

## Docker Compose Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Nginx (Port 80)                        │
│              Reverse Proxy / Load Balancer                │
└─────────────────────────────────────────────────────────┘
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

## Docker Compose Services

### Infrastructure Services

#### PostgreSQL

```yaml
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: university_erp
  ports:
    - "5432:5432"
  volumes:
    - ./docker-volumes/postgres:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 30s
    timeout: 20s
    retries: 3
```

**Configuration**:
- **Image**: postgres:16-alpine
- **Port**: 5432
- **Volume**: `docker-volumes/postgres`
- **Health Check**: pg_isready command

#### Redis

```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - ./docker-volumes/redis:/data
  command: redis-server --appendonly yes
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 30s
    timeout: 20s
    retries: 3
```

**Configuration**:
- **Image**: redis:7-alpine
- **Port**: 6379
- **Volume**: `docker-volumes/redis`
- **Persistence**: AOF enabled
- **Health Check**: redis-cli ping

#### MinIO

```yaml
minio:
  image: minio/minio:latest
  command: server /data --console-address ":9001"
  ports:
    - "9000:9000"
    - "9001:9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  volumes:
    - ./docker-volumes/minio:/data
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
    interval: 30s
    timeout: 20s
    retries: 3
```

**Configuration**:
- **Image**: minio/minio:latest
- **API Port**: 9000
- **Console Port**: 9001
- **Volume**: `docker-volumes/minio`
- **Health Check**: MinIO health endpoint

#### Elasticsearch

```yaml
elasticsearch:
  image: elasticsearch:8.13.0
  environment:
    - discovery.type=single-node
    - xpack.security.enabled=false
    - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
  ports:
    - "9200:9200"
  volumes:
    - ./docker-volumes/elasticsearch:/usr/share/elasticsearch/data
  healthcheck:
    test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
    interval: 30s
    timeout: 20s
    retries: 3
```

**Configuration**:
- **Image**: elasticsearch:8.13.0
- **Port**: 9200
- **Volume**: `docker-volumes/elasticsearch`
- **Discovery**: Single-node
- **Security**: Disabled
- **Java Heap**: 512MB

#### Nginx

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
  volumes:
    - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
    - ./docker-volumes/nginx:/var/log/nginx
  depends_on:
    - admin-portal
    - core-api
```

**Configuration**:
- **Image**: nginx:alpine
- **Port**: 80
- **Config**: `docker/nginx/nginx.conf`
- **Logs**: `docker-volumes/nginx`

### Application Services

#### Core API

```yaml
core-api:
  build:
    context: ./apps/core-api
    dockerfile: Dockerfile
  ports:
    - "3000:3000"
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy
    minio:
      condition: service_healthy
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
    - REDIS_HOST=redis
    - REDIS_PORT=6379
    - MINIO_ENDPOINT=http://minio:9000
    - MINIO_ACCESS_KEY=minioadmin
    - MINIO_SECRET_KEY=minioadmin
    - JWT_SECRET=dev-secret-key
  volumes:
    - ./apps/core-api:/app
    - /app/node_modules
```

**Configuration**:
- **Build**: From `apps/core-api/Dockerfile`
- **Port**: 3000
- **Depends On**: PostgreSQL, Redis, MinIO (with health checks)
- **Volumes**: Code mount for development

#### CBE Engine

```yaml
cbe-engine:
  build:
    context: ./apps/cbe-engine
    dockerfile: Dockerfile
  ports:
    - "3001:3001"
  depends_on:
    - postgres
    - redis
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
    - REDIS_HOST=redis
    - REDIS_PORT=6379
  volumes:
    - ./apps/cbe-engine:/app
    - /app/node_modules
```

**Configuration**:
- **Build**: From `apps/cbe-engine/Dockerfile`
- **Port**: 3001
- **Depends On**: PostgreSQL, Redis

#### Notification Worker

```yaml
notification-worker:
  build:
    context: ./apps/notification-worker
    dockerfile: Dockerfile
  ports:
    - "3002:3002"
  depends_on:
    - redis
  environment:
    - REDIS_HOST=redis
    - REDIS_PORT=6379
  volumes:
    - ./apps/notification-worker:/app
    - /app/node_modules
```

**Configuration**:
- **Build**: From `apps/notification-worker/Dockerfile`
- **Port**: 3002
- **Depends On**: Redis

#### Certificate Generator

```yaml
cert-generator:
  build:
    context: ./apps/cert-generator
    dockerfile: Dockerfile
  ports:
    - "3003:3003"
  depends_on:
    - postgres
    - minio
    - redis
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
    - MINIO_ENDPOINT=http://minio:9000
    - MINIO_ACCESS_KEY=minioadmin
    - MINIO_SECRET_KEY=minioadmin
    - REDIS_HOST=redis
    - REDIS_PORT=6379
  volumes:
    - ./apps/cert-generator:/app
    - /app/node_modules
```

**Configuration**:
- **Build**: From `apps/cert-generator/Dockerfile`
- **Port**: 3003
- **Depends On**: PostgreSQL, MinIO, Redis

#### Admin Portal

```yaml
admin-portal:
  build:
    context: ./web/admin-portal
    dockerfile: Dockerfile
  ports:
    - "5173:5173"
  environment:
    - VITE_API_URL=http://localhost:3000/api
  volumes:
    - ./web/admin-portal:/app
    - /app/node_modules
```

**Configuration**:
- **Build**: From `web/admin-portal/Dockerfile`
- **Port**: 5173
- **Volumes**: Code mount for development

## Docker Volumes

```
docker-volumes/
├── postgres/          # PostgreSQL data
├── redis/             # Redis data
├── minio/             # MinIO data
├── elasticsearch/     # Elasticsearch data
└── nginx/             # Nginx logs
```

## Nginx Configuration

### nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server core-api:3000;
    }

    upstream cbe {
        server cbe-engine:3001;
    }

    upstream frontend {
        server admin-portal:5173;
    }

    server {
        listen 80;
        server_name localhost;

        location /api/ {
            proxy_pass http://api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        location /cbe/ {
            proxy_pass http://cbe;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

## Native Deployment (PM2)

### PM2 Configuration

```javascript
// ecosystem.native.config.js
module.exports = {
  apps: [
    {
      name: 'core-api',
      script: 'apps/core-api/dist/main.js',
      instances: 2,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
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
        NODE_ENV: 'production',
        PORT: 3001,
      },
    },
    {
      name: 'notification-worker',
      script: 'apps/notification-worker/dist/main.js',
      instances: 2,
      env: {
        NODE_ENV: 'production',
        PORT: 3002,
      },
    },
    {
      name: 'cert-generator',
      script: 'apps/cert-generator/dist/main.js',
      instances: 1,
      env: {
        NODE_ENV: 'production',
        PORT: 3003,
      },
    },
  ],
};
```

### PM2 Commands

```bash
# Start all services
pm2 start ecosystem.native.config.js

# Stop all services
pm2 stop ecosystem.native.config.js

# Restart all services
pm2 restart ecosystem.native.config.js

# View logs
pm2 logs

# Monitor
pm2 monit

# Save process list
pm2 save

# Setup startup script
pm2 startup
```

## Startup Scripts

### start.sh

```bash
#!/bin/bash

# Start Docker Compose
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Run database migrations
cd apps/core-api
npx prisma migrate deploy

# Seed database
npx prisma db seed

echo "Services started successfully!"
```

### stop.sh

```bash
#!/bin/bash

# Stop Docker Compose
docker-compose down

echo "Services stopped successfully!"
```

### status.sh

```bash
#!/bin/bash

# Check Docker Compose status
docker-compose ps

# Check service health
echo "PostgreSQL:"
docker-compose exec postgres pg_isready

echo "Redis:"
docker-compose exec redis redis-cli ping

echo "MinIO:"
curl -f http://localhost:9000/minio/health/live

echo "Elasticsearch:"
curl -f http://localhost:9200/_cluster/health
```

## Dockerfile Patterns

### NestJS Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

### React Dockerfile

```dockerfile
FROM node:18-alpine as builder

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

## Deployment Strategies

### Development

- **Tool**: Docker Compose
- **Hot Reload**: Volume mounts for code
- **Database**: PostgreSQL in Docker
- **Storage**: MinIO in Docker
- **Cache**: Redis in Docker

### Staging

- **Tool**: Docker Compose or Kubernetes
- **Build**: Production builds
- **Database**: Managed PostgreSQL
- **Storage**: MinIO or Azure Blob
- **Cache**: Managed Redis

### Production

- **Tool**: PM2 or Kubernetes
- **Build**: Production builds
- **Database**: Managed PostgreSQL (AWS RDS, Azure Database)
- **Storage**: Azure Blob or AWS S3
- **Cache**: Managed Redis (ElastiCache, Azure Cache)
- **Load Balancer**: Nginx or Cloud Load Balancer

## Infrastructure Monitoring

### Health Checks

```bash
# Core API
curl http://localhost:3000/health

# PostgreSQL
docker-compose exec postgres pg_isready

# Redis
docker-compose exec redis redis-cli ping

# MinIO
curl http://localhost:9000/minio/health/live

# Elasticsearch
curl http://localhost:9200/_cluster/health
```

### Logs

```bash
# Docker Compose logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f core-api

# PM2 logs
pm2 logs

# Nginx logs
tail -f docker-volumes/nginx/access.log
tail -f docker-volumes/nginx/error.log
```

## Backup Strategy

### Database Backup

```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U postgres university_erp > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres university_erp < backup.sql
```

### Volume Backup

```bash
# Backup all volumes
docker run --rm \
  -v docker-volumes_postgres:/data/postgres \
  -v docker-volumes_redis:/data/redis \
  -v docker-volumes_minio:/data/minio \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d).tar.gz /data
```

## Scaling

### Horizontal Scaling

```bash
# Scale core-api
docker-compose up -d --scale core-api=3

# Scale notification-worker
docker-compose up -d --scale notification-worker=2
```

### Vertical Scaling

Increase resources in docker-compose.yml:

```yaml
services:
  core-api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

## Known Limitations

1. **No Kubernetes**: No Kubernetes configuration
2. **No CI/CD**: No automated deployment pipeline
3. **No Monitoring**: No Prometheus/Grafana
4. **No Log Aggregation**: No ELK stack
5. **No Auto-scaling**: No auto-scaling configuration

## Future Enhancements

1. **Add Kubernetes**: Add Kubernetes manifests
2. **Add CI/CD**: Add GitHub Actions or GitLab CI
3. **Add Monitoring**: Add Prometheus and Grafana
4. **Add Log Aggregation**: Add ELK or Loki
5. **Add Auto-scaling**: Add auto-scaling configuration
6. **Add CDN**: Add CloudFront or Cloudflare
7. **Add WAF**: Add Web Application Firewall
8. **Add DDoS Protection**: Add DDoS protection
