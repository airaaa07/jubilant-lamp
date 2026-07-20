# Environment Variables

## Purpose

This document provides a comprehensive reference for all environment variables used in the University ERP system. It explains the purpose, default values, and configuration of each variable.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses environment variables for configuration. Understanding environment variables is critical for:
- Configuring the application correctly
- Managing different environments (dev, staging, prod)
- Securing sensitive data
- Troubleshooting configuration issues
- Deploying to production

Without understanding environment variables, the application may not work correctly or may expose sensitive data.

## Where This Is Used

- **Development**: Setting up local development environment
- **Deployment**: Deploying to different environments
- **Configuration**: Configuring application behavior
- **Security**: Managing secrets
- **Troubleshooting**: Debugging configuration issues

## Dependencies

### Environment Variable Dependencies

**Confirmed by Code**: Environment variables depend on:

- **.env File**: Local environment configuration
- **Docker Compose**: Service environment variables
- **NestJS ConfigModule**: Configuration loading
- **Process Environment**: Runtime environment

## Internal Architecture

### Environment Variable Categories

**Confirmed by Code**: Environment variables are organized by category.

```
┌─────────────────────────────────────────────────────────┐
│              Environment Variables                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Database      │  │  Redis          │  │  MinIO         │
│  Variables    │  │  Variables      │  │  Variables     │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  JWT           │  │  SMTP           │  │  Application   │
│  Variables    │  │  Variables      │  │  Variables     │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Environment Variable Configuration

**Confirmed by Code**: .env.example provides template.

**.env.example**:
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# MinIO
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams

# Azure Blob Storage (optional)
AZURE_STORAGE_CONNECTION_STRING=
AZURE_STORAGE_CONTAINER_NAME=

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
SMTP_FROM=noreply@university.edu

# Elasticsearch
ELASTICSEARCH_NODE=http://localhost:9200

# Application
PORT=3000
NODE_ENV=development

# Vault (optional)
VAULT_ADDR=
VAULT_TOKEN=
```

### NestJS Configuration

**Confirmed by Code**: NestJS ConfigModule loads environment variables.

**Configuration**:
```typescript
// apps/core-api/src/app.module.ts
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
  ],
})
export class AppModule {}
```

**What This Does**:
- Loads environment variables from .env file
- Makes variables available via ConfigService
- Global configuration for all modules

### Accessing Environment Variables

**Confirmed by Code**: Services access variables via ConfigService.

**Example**:
```typescript
@Injectable()
export class MyService {
  constructor(private configService: ConfigService) {}

  getDatabaseUrl(): string {
    return this.configService.get<string>('DATABASE_URL');
  }

  getPort(): number {
    return this.configService.get<number>('PORT', 3000);
  }
}
```

## Database Interactions

### Database Environment Variables

**Confirmed by Code**: PostgreSQL connection via DATABASE_URL.

**Variables**:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
```

**Components**:
- **Protocol**: postgresql://
- **User**: postgres
- **Password**: postgres
- **Host**: localhost
- **Port**: 5432
- **Database**: university_erp

**Connection Options** (optional):
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp?connection_limit=10&pool_timeout=20
```

**Docker Compose**:
```yaml
services:
  core-api:
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
```

## Redis Interactions

### Redis Environment Variables

**Confirmed by Code**: Redis connection via REDIS_HOST and REDIS_PORT.

**Variables**:
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Optional Variables**:
```bash
REDIS_PASSWORD=your-password
REDIS_DB=0
```

**Docker Compose**:
```yaml
services:
  core-api:
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
```

## Queue Interactions

### Queue Environment Variables

**Confirmed by Code**: Bull queues use Redis environment variables.

**Configuration**:
```typescript
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
    password: process.env.REDIS_PASSWORD,
  },
});
```

## Worker Interactions

### Worker Environment Variables

**Confirmed by Code**: Workers use same environment variables as API.

**Variables**:
```bash
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
REDIS_HOST=redis
REDIS_PORT=6379
MINIO_ENDPOINT=http://minio:9000
```

## Business Rules

### Environment Variable Rules

**Confirmed by Code**: Environment variables follow these rules:

1. **.env File**: Never commit .env file
2. **.env.example**: Commit .env.example as template
3. **Defaults**: Provide sensible defaults
4. **Validation**: Validate required variables
5. **Documentation**: Document all variables

### Security Rules

**Confirmed by Code**: Security considerations for environment variables:

1. **No Secrets in Code**: Never hardcode secrets
2. **Environment-Specific**: Different variables for different environments
3. **Secrets Manager**: Use secrets manager in production
4. **Access Control**: Restrict access to .env file
5. **Rotation**: Rotate secrets regularly

## Security

### Environment Variable Security

**Confirmed by Code**: Security best practices:

1. **Never Commit .env**: Add .env to .gitignore
2. **Use Strong Secrets**: Use strong random secrets
3. **Rotate Secrets**: Rotate secrets regularly
4. **Use Secrets Manager**: Use AWS Secrets Manager or Azure Key Vault in production
5. **Limit Access**: Restrict access to environment variables

### Secrets Management

**Development**:
- Use .env file
- Never commit .env
- Share .env.example

**Staging**:
- Use .env.staging file
- Use secrets manager if available
- Rotate secrets regularly

**Production**:
- Use secrets manager (AWS Secrets Manager, Azure Key Vault)
- Never store secrets in code
- Rotate secrets regularly
- Audit secret access

## Performance Considerations

### Environment Variable Performance

**Confirmed by Code**: Performance considerations:

1. **Connection Pooling**: Configure connection limits in DATABASE_URL
2. **Cache TTL**: Configure cache TTL in environment variables
3. **Worker Count**: Configure worker count in environment variables
4. **Timeout Values**: Configure timeout values appropriately

## Common Mistakes

### Mistake 1: Committing .env File

**Symptom**: Secrets exposed in version control

**Cause**: .env file committed

**Fix**:
```bash
# Add .env to .gitignore
echo ".env" >> .gitignore

# Remove from git
git rm --cached .env
git commit -m "Remove .env from version control"
```

### Mistake 2: Using Default Secrets

**Symptom**: Security risk

**Cause**: Using default secrets in production

**Fix**:
```bash
# Change default secrets
JWT_SECRET=your-very-strong-random-secret-here
MINIO_SECRET_KEY=your-very-strong-secret-key-here
```

### Mistake 3: Not Validating Variables

**Symptom**: Application fails with undefined variable

**Cause**: Required variable not set

**Fix**:
```typescript
// Validate required variables
const requiredEnvVars = ['DATABASE_URL', 'REDIS_HOST', 'JWT_SECRET'];
requiredEnvVars.forEach((varName) => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});
```

## Debugging Guide

### Environment Variable Debugging

**Issue**: Application not loading environment variables

**Investigation**:
1. Check .env file exists
2. Check .env file location
3. Check variable spelling
4. Check ConfigModule configuration
5. Check environment variable access

**Tools**:
- `printenv` to list environment variables
- `echo $VAR_NAME` to check specific variable
- ConfigService to access variables
- Application logs to check loaded variables

## Future Enhancements

### Configuration Validation

**Status**: Not implemented

**Proposal**: Implement configuration validation:
- Validate required variables on startup
- Validate variable types
- Validate variable formats
- Provide helpful error messages

### Configuration Schema

**Status**: Not implemented

**Proposal**: Implement configuration schema:
- Define schema for environment variables
- Validate against schema
- Provide default values
- Document schema

## Production Considerations

### Production Environment Variables

**Production Deployment**:
- Use secrets manager
- Never commit secrets
- Use environment-specific files (.env.production)
- Rotate secrets regularly
- Audit secret access
- Monitor secret usage

### Environment-Specific Configuration

**Development**:
- Use .env file
- Use default values
- Enable debug logging
- Enable Swagger docs

**Staging**:
- Use .env.staging file
- Use production-like values
- Enable debug logging
- Enable Swagger docs

**Production**:
- Use secrets manager
- Use strong secrets
- Disable debug logging
- Disable Swagger docs

## Example Requests

### List Environment Variables

**Request**:
```bash
printenv | grep -E "(DATABASE|REDIS|JWT|MINIO)"
```

**Response**:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET=your-secret-key
MINIO_ENDPOINT=http://minio:9000
```

## Example Responses

### Configuration Validation

**Request**: Validate environment variables

**Response**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    "Using default JWT_SECRET in production is not recommended"
  ]
}
```

## Sequence Diagrams

### Environment Variable Loading

```
Application Start
        ↓
ConfigModule loads .env
        ↓
Variables available in process.env
        ↓
ConfigService provides variables
        ↓
Services use ConfigService
        ↓
Application configured
```

## Architecture Diagrams

### Environment Variable Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  .env File                                │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  ConfigModule                            │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Services     │  │  Controllers   │  │  Workers       │
│  (ConfigService)│  │  (ConfigService)│  │  (ConfigService)│
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How are environment variables managed in the system?

**Answer**: Environment variables via:
- .env file for local development
- .env.example as template
- ConfigModule loads variables
- ConfigService provides variables
- Secrets manager in production

### Q2: How do you secure sensitive environment variables?

**Answer**: Security via:
- Never commit .env file
- Use secrets manager in production
- Rotate secrets regularly
- Restrict access to secrets
- Audit secret access

### Q3: How do you handle environment-specific configuration?

**Answer**: Environment-specific via:
- .env file for development
- .env.staging for staging
- .env.production for production
- Secrets manager for production
- Different values per environment

## Exercises

### Exercise 1: Configure Environment Variables

**Task**: Configure environment variables for local development.

**Steps**:
1. Copy .env.example to .env
2. Set required variables
3. Set optional variables
4. Verify configuration
5. Start application

**Verification**:
- .env file created
- Variables set correctly
- Application starts successfully

### Exercise 2: Validate Environment Variables

**Task**: Validate environment variables.

**Steps**:
1. Check .env file exists
2. Check required variables are set
3. Check variable formats are correct
4. Check variable values are valid
5. Test application startup

**Verification**:
- All required variables set
- Formats correct
- Values valid
- Application starts

## Real Production Scenarios

### Scenario 1: Missing Environment Variable

**Situation**: Application fails to start due to missing variable

**Response**:
1. Check .env file
2. Check variable name spelling
3. Check variable is set
4. Add missing variable
5. Restart application

### Scenario 2: Wrong Environment Variable Value

**Situation**: Application connects to wrong database

**Response**:
1. Check DATABASE_URL
2. Check host, port, database name
3. Correct value
4. Restart application
5. Verify connection

## Navigation

**Next Section**: [05-Performance](./05-Performance.md)

**Previous Section**: [03-Storage](./03-Storage.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [15-Deployment](../15-Deployment/README.md) - Deployment details
- [17-Production](../17-Production/README.md) - Production guide
