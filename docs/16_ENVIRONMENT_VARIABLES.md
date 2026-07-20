# University ERP - Environment Variables

## Overview

This document provides a complete reference of all environment variables used in the University ERP system.

## Environment Variables Reference

### Database

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DATABASE_URL` | string | - | PostgreSQL connection string |
| `POSTGRES_USER` | string | postgres | PostgreSQL username |
| `POSTGRES_PASSWORD` | string | postgres | PostgreSQL password |
| `POSTGRES_DB` | string | university_erp | PostgreSQL database name |

**Example**:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=university_erp
```

### Redis

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `REDIS_HOST` | string | localhost | Redis server host |
| `REDIS_PORT` | number | 6379 | Redis server port |

**Example**:
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
```

### MinIO

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MINIO_ENDPOINT` | string | http://minio:9000 | MinIO server endpoint |
| `MINIO_ACCESS_KEY` | string | minioadmin | MinIO access key |
| `MINIO_SECRET_KEY` | string | minioadmin | MinIO secret key |
| `MINIO_BUCKET` | string | university-erp-docs | Default documents bucket |
| `MINIO_EXAM_BUCKET` | string | university-erp-exams | Exam artefacts bucket |

**Example**:
```bash
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams
```

### Azure Blob (Optional)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `AZURE_STORAGE_CONNECTION_STRING` | string | - | Azure Blob connection string |

**Example**:
```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
```

**Note**: When set, Azure Blob is used instead of MinIO.

### JWT Authentication

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `JWT_SECRET` | string | - | JWT signing secret (required) |
| `JWT_EXPIRY` | string | 15m | Access token expiry |
| `JWT_REFRESH_EXPIRY` | string | 7d | Refresh token expiry |

**Example**:
```bash
JWT_SECRET=your-super-secret-key-change-in-production
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
```

### SMTP / Email

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `SMTP_HOST` | string | - | SMTP server host |
| `SMTP_PORT` | number | 587 | SMTP server port |
| `SMTP_SECURE` | boolean | false | Use SSL/TLS |
| `SMTP_USER` | string | - | SMTP username |
| `SMTP_PASSWORD` | string | - | SMTP password |
| `SMTP_FROM` | string | - | Default from address |

**Example**:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu
```

### Elasticsearch

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ELASTICSEARCH_NODE` | string | http://localhost:9200 | Elasticsearch node URL |

**Example**:
```bash
ELASTICSEARCH_NODE=http://localhost:9200
```

### Application

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `APP_URL` | string | http://localhost:5173 | Frontend application URL |
| `API_URL` | string | http://localhost:3000 | Backend API URL |
| `NODE_ENV` | string | development | Node environment (development/production) |
| `PORT` | number | 3000 | API server port |

**Example**:
```bash
APP_URL=http://localhost:5173
API_URL=http://localhost:3000
NODE_ENV=development
PORT=3000
```

### University

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `UNIVERSITY_ID` | string | - | Default university ID |
| `INSTITUTE_ID` | string | - | Default institute ID |

**Example**:
```bash
UNIVERSITY_ID=default-university-id
INSTITUTE_ID=default-institute-id
```

### Vault (Secret Management)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VAULT_ENABLED` | boolean | false | Enable vault integration |
| `VAULT_PROVIDER` | string | aws | Vault provider (aws/azure/google) |
| `VAULT_REGION` | string | us-east-1 | AWS region (for AWS) |
| `VAULT_SECRET_NAME` | string | university-erp-secrets | Secret name in vault |

**Example**:
```bash
VAULT_ENABLED=false
VAULT_PROVIDER=aws
VAULT_REGION=us-east-1
VAULT_SECRET_NAME=university-erp-secrets
```

### Service-Specific Ports

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CORE_API_PORT` | number | 3000 | Core API port |
| `CBE_ENGINE_PORT` | number | 3001 | CBE Engine port |
| `NOTIFICATION_WORKER_PORT` | number | 3002 | Notification Worker port |
| `CERT_GENERATOR_PORT` | number | 3003 | Certificate Generator port |

**Example**:
```bash
CORE_API_PORT=3000
CBE_ENGINE_PORT=3001
NOTIFICATION_WORKER_PORT=3002
CERT_GENERATOR_PORT=3003
```

### Frontend

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `VITE_API_URL` | string | http://localhost:3000/api | API URL for frontend |

**Example**:
```bash
VITE_API_URL=http://localhost:3000/api
```

### Docker Compose Services

#### PostgreSQL

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `POSTGRES_USER` | string | postgres | PostgreSQL username |
| `POSTGRES_PASSWORD` | string | postgres | PostgreSQL password |
| `POSTGRES_DB` | string | university_erp | PostgreSQL database name |

#### Redis

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| (No specific env vars) | - | - | Uses default Redis configuration |

#### MinIO

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `MINIO_ROOT_USER` | string | minioadmin | MinIO root user |
| `MINIO_ROOT_PASSWORD` | string | minioadmin | MinIO root password |

#### Elasticsearch

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `discovery.type` | string | single-node | Discovery type |
| `xpack.security.enabled` | boolean | false | Security enabled |
| `ES_JAVA_OPTS` | string | -Xms512m -Xmx512m | Java heap options |

## Environment File Templates

### .env.example

```bash
# Database
DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=university_erp

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MinIO
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams

# Azure Blob (optional)
AZURE_STORAGE_CONNECTION_STRING=

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu

# Elasticsearch
ELASTICSEARCH_NODE=http://localhost:9200

# Application
APP_URL=http://localhost:5173
API_URL=http://localhost:3000
NODE_ENV=deeployment
PORT=3000

# University
UNIVERSITY_ID=
INSTITUTE_ID=

# Vault
VAULT_ENABLED=false
VAULT_PROVIDER=aws
VAULT_REGION=us-east-1
VAULT_SECRET_NAME=university-erp-secrets
```

### .env (Development)

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=university_erp

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MinIO
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams

# JWT
JWT_SECRET=dev-secret-key-do-not-use-in-production
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu

# Elasticsearch
ELASTICSEARCH_NODE=http://localhost:9200

# Application
APP_URL=http://localhost:5173
API_URL=http://localhost:3000
NODE_ENV=development
PORT=3000

# University
UNIVERSITY_ID=
INSTITUTE_ID=
```

### .env.production (Production)

```bash
# Database
DATABASE_URL=postgresql://prod-user:prod-pass@prod-db:5432/university_erp
POSTGRES_USER=prod-user
POSTGRES_PASSWORD=prod-pass
POSTGRES_DB=university_erp

# Redis
REDIS_HOST=prod-redis
REDIS_PORT=6379

# MinIO
MINIO_ENDPOINT=https://minio.example.com
MINIO_ACCESS_KEY=prod-access-key
MINIO_SECRET_KEY=prod-secret-key
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams

# JWT
JWT_SECRET=<strong-random-secret>
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# SMTP
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=apikey
SMTP_PASSWORD=<sendgrid-api-key>
SMTP_FROM=noreply@university.edu

# Elasticsearch
ELASTICSEARCH_NODE=http://elasticsearch:9200

# Application
APP_URL=https://erp.university.edu
API_URL=https://api.university.edu
NODE_ENV=production
PORT=3000

# University
UNIVERSITY_ID=<university-id>
INSTITUTE_ID=<institute-id>

# Vault
VAULT_ENABLED=true
VAULT_PROVIDER=aws
VAULT_REGION=us-east-1
VAULT_SECRET_NAME=university-erp-secrets
```

## Security Best Practices

### 1. Never Commit .env Files

```gitignore
# .gitignore
.env
.env.local
.env.*.local
```

### 2. Use Strong Secrets

```bash
# Generate strong secret
JWT_SECRET=$(openssl rand -base64 32)
```

### 3. Use Vault for Production

```bash
VAULT_ENABLED=true
VAULT_PROVIDER=aws
VAULT_REGION=us-east-1
VAULT_SECRET_NAME=university-erp-secrets
```

### 4. Rotate Secrets Regularly

- Rotate JWT_SECRET monthly
- Rotate database passwords quarterly
- Rotate API keys as needed

### 5. Use Environment-Specific Files

```bash
# Development
.env

# Staging
.env.staging

# Production
.env.production
```

## Configuration Validation

### Required Variables

The following variables are required for the application to start:

- `DATABASE_URL`
- `JWT_SECRET`

### Optional Variables

The following variables have defaults:

- `REDIS_HOST` (default: localhost)
- `REDIS_PORT` (default: 6379)
- `JWT_EXPIRY` (default: 15m)
- `JWT_REFRESH_EXPIRY` (default: 7d)
- `PORT` (default: 3000)
- `NODE_ENV` (default: development)

## Troubleshooting

### Database Connection Failed

**Error**: `Can't reach database server`

**Solution**: Check `DATABASE_URL` is correct and PostgreSQL is running.

### Redis Connection Failed

**Error**: `Redis connection failed`

**Solution**: Check `REDIS_HOST` and `REDIS_PORT` are correct and Redis is running.

### MinIO Connection Failed

**Error**: `MinIO connection failed`

**Solution**: Check `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, and `MINIO_SECRET_KEY` are correct.

### JWT Secret Missing

**Error**: `JWT_SECRET is required`

**Solution**: Set `JWT_SECRET` environment variable.

### SMTP Authentication Failed

**Error**: `SMTP authentication failed`

**Solution**: Check `SMTP_USER` and `SMTP_PASSWORD` are correct.

## Environment Variable Access in Code

### Using ConfigService

```typescript
@Injectable()
export class MyService {
  constructor(private configService: ConfigService) {}

  getDatabaseUrl(): string {
    return this.configService.get<string>('DATABASE_URL');
  }

  getJwtSecret(): string {
    return this.configService.get<string>('JWT_SECRET');
  }

  getPort(): number {
    return this.configService.get<number>('PORT', 3000);
  }
}
```

### Direct Access

```typescript
const databaseUrl = process.env.DATABASE_URL;
const jwtSecret = process.env.JWT_SECRET;
```

## Environment-Specific Behavior

### Development

- Detailed logging enabled
- Swagger documentation enabled
- Hot reload enabled
- Error stack traces shown

### Production

- Minimal logging
- Swagger documentation disabled
- Hot reload disabled
- Error messages sanitized

## Known Limitations

1. **No Configuration Validation**: No runtime validation of environment variables
2. **No Type Safety**: Environment variables are strings, no type checking
3. **No Documentation in Code**: No inline documentation for variables
4. **No Environment-Specific Defaults**: No different defaults per environment

## Future Enhancements

1. **Add Validation**: Add Joi schema validation
2. **Add Type Safety**: Use typed configuration
3. **Add Documentation**: Add inline documentation
4. **Add Environment-Specific Defaults**: Different defaults per environment
5. **Add Configuration UI**: UI for managing environment variables
6. **Add Configuration Encryption**: Encrypt sensitive values at rest
7. **Add Configuration Rotation**: Automated secret rotation
