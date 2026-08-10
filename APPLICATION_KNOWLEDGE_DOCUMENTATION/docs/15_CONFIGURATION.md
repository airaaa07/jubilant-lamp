# University ERP - Configuration

## Overview

The system uses **NestJS ConfigModule** for configuration management, with environment variables as the primary configuration source. Configuration is loaded at application startup and is available throughout the application via dependency injection.

## Configuration Architecture

```
┌─────────────────┐
│  Environment    │
│   Variables     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  ConfigModule   │
│                 │
│  NestJS Config  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  ConfigService  │
│                 │
│  DI Injection   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Services       │
│                 │
│  Usage          │
└─────────────────┘
```

## ConfigModule Setup

### Core API

```typescript
// apps/core-api/src/app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: ['.env', '.env.native'],
    }),
    // ... other modules
  ],
})
export class AppModule {}
```

### Other Services

All other services (cbe-engine, cert-generator, notification-worker) use the same pattern:

```typescript
@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true })],
})
export class AppModule {}
```

## Configuration Categories

### 1. Database Configuration

```typescript
DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=university_erp
```

### 2. Redis Configuration

```typescript
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 3. MinIO Configuration

```typescript
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams
```

### 4. Azure Blob Configuration (Optional)

```typescript
AZURE_STORAGE_CONNECTION_STRING=<connection-string>
```

### 5. JWT Configuration

```typescript
JWT_SECRET=your-secret-key
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
```

### 6. SMTP Configuration

```typescript
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@university.edu
```

### 7. Elasticsearch Configuration

```typescript
ELASTICSEARCH_NODE=http://localhost:9200
```

### 8. Application Configuration

```typescript
APP_URL=http://localhost:5173
API_URL=http://localhost:3000
NODE_ENV=development
PORT=3000
```

### 9. University Configuration

```typescript
UNIVERSITY_ID=<default-university-id>
INSTITUTE_ID=<default-institute-id>
```

### 10. Vault Configuration (Optional)

```typescript
VAULT_ENABLED=false
VAULT_PROVIDER=aws|azure|google
VAULT_REGION=us-east-1
VAULT_SECRET_NAME=university-erp-secrets
```

## Configuration Access

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

### Default Values

```typescript
const port = this.configService.get<number>('PORT', 3000);
const redisHost = this.configService.get<string>('REDIS_HOST', 'localhost');
```

## Configuration Files

### .env

Local development environment file (not committed):

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp
REDIS_HOST=localhost
REDIS_PORT=6379
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
JWT_SECRET=dev-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### .env.example

Template for environment variables (committed):

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
NODE_ENV=development
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

### .env.native

Native deployment environment file:

```bash
# Production values
DATABASE_URL=postgresql://prod-user:prod-pass@prod-db:5432/university_erp
REDIS_HOST=prod-redis
MINIO_ENDPOINT=https://minio.example.com
JWT_SECRET=<production-secret>
# ... other production values
```

## Vault Integration

### Vault Bootstrap

```typescript
// apps/core-api/src/infrastructure/vault/vault.bootstrap.ts
export async function bootstrapVault(configService: ConfigService) {
  const enabled = configService.get<boolean>('VAULT_ENABLED', false);

  if (!enabled) {
    return;
  }

  const provider = configService.get<string>('VAULT_PROVIDER');
  const region = configService.get<string>('VAULT_REGION');
  const secretName = configService.get<string>('VAULT_SECRET_NAME');

  switch (provider) {
    case 'aws':
      return bootstrapAwsVault(region, secretName);
    case 'azure':
      return bootstrapAzureVault(secretName);
    case 'google':
      return bootstrapGoogleVault(secretName);
    default:
      throw new Error(`Unknown vault provider: ${provider}`);
  }
}
```

### AWS Secrets Manager

```typescript
async function bootstrapAwsVault(region: string, secretName: string) {
  const client = new SecretsManagerClient({ region });
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);
  const secrets = JSON.parse(response.SecretString || '{}');

  // Merge secrets into environment
  Object.assign(process.env, secrets);
}
```

### Azure Key Vault

```typescript
async function bootstrapAzureVault(secretName: string) {
  const credential = new DefaultAzureCredential();
  const client = new SecretClient(
    `https://${vaultName}.vault.azure.net`,
    credential
  );
  const secret = await client.getSecret(secretName);
  const secrets = JSON.parse(secret.value || '{}');

  Object.assign(process.env, secrets);
}
```

### Google Secret Manager

```typescript
async function bootstrapGoogleVault(secretName: string) {
  const client = new SecretManagerServiceClient();
  const [version] = await client.accessSecretVersion({
    name: secretName,
  });
  const secrets = JSON.parse(version.payload?.data?.toString() || '{}');

  Object.assign(process.env, secrets);
}
```

## Configuration Validation

### Joi Schema (Potential)

```typescript
import * as Joi from 'joi';

const validationSchema = Joi.object({
  DATABASE_URL: Joi.string().required(),
  REDIS_HOST: Joi.string().default('localhost'),
  REDIS_PORT: Joi.number().default(6379),
  JWT_SECRET: Joi.string().required(),
  JWT_EXPIRY: Joi.string().default('15m'),
  JWT_REFRESH_EXPIRY: Joi.string().default('7d'),
});

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      validationSchema,
    }),
  ],
})
export class AppModule {}
```

## Runtime Configuration

### Dynamic Configuration

Some configuration is stored in the database:

- **University Config**: University-level settings
- **Institute Config**: Institute-level settings
- **Attendance Config**: Attendance rules
- **Exam Config**: Exam rules
- **Library Config**: Library rules
- **Hostel Config**: Hostel rules
- **Transport Config**: Transport rules

### Configuration Access Pattern

```typescript
// Load from database
const config = await prisma.university.findUnique({
  where: { id: universityId },
  select: { config: true },
});

const settings = config.config as Record<string, any>;
```

## Configuration Security

### Sensitive Data

- **Never commit**: .env file
- **Never log**: Sensitive configuration values
- **Use vault**: For production secrets
- **Rotate secrets**: Regularly rotate secrets

### Environment-Specific Config

- **Development**: .env file
- **Staging**: Vault or .env.staging
- **Production**: Vault or .env.production

## Configuration Best Practices

### 1. Use Default Values

```typescript
const port = this.configService.get<number>('PORT', 3000);
```

### 2. Validate Configuration

```typescript
if (!this.configService.get('JWT_SECRET')) {
  throw new Error('JWT_SECRET is required');
}
```

### 3. Use Type Guards

```typescript
const port = this.configService.get<number>('PORT');
if (typeof port !== 'number') {
  throw new Error('PORT must be a number');
}
```

### 4. Document Required Variables

Maintain .env.example with all required variables.

### 5. Use Environment-Specific Files

```typescript
ConfigModule.forRoot({
  envFilePath: ['.env', `.env.${process.env.NODE_ENV}`],
})
```

## Configuration Hot Reload

### Development

NestJS watch mode automatically reloads on .env changes (not recommended).

### Production

Configuration changes require restart (no hot reload).

## Configuration Debugging

### Log Configuration

```typescript
bootstrap() {
  const config = this.app.get(ConfigService);
  this.logger.log('Database URL:', config.get('DATABASE_URL'));
  this.logger.log('Redis Host:', config.get('REDIS_HOST'));
}
```

### Configuration Endpoint

```typescript
@Get('config')
@UseGuards(JwtAuthGuard)
getConfig(@CurrentUser() user: JwtPayload) {
  if (user.role !== 'SUPERADMIN') {
    throw new ForbiddenException();
  }
  return {
    databaseUrl: this.configService.get('DATABASE_URL'),
    redisHost: this.configService.get('REDIS_HOST'),
    // ... other config (redact sensitive values)
  };
}
```

## Known Limitations

1. **No Configuration Validation**: No Joi schema validation
2. **No Hot Reload**: Configuration changes require restart
3. **No Configuration UI**: No UI for configuration management
4. **No Versioning**: No configuration versioning
5. **No Audit Trail**: No audit trail for configuration changes

## Future Enhancements

1. **Add Validation**: Add Joi schema validation
2. **Add Hot Reload**: Enable configuration hot reload
3. **Add Configuration UI**: Add UI for configuration management
4. **Add Versioning**: Add configuration versioning
5. **Add Audit Trail**: Log configuration changes
6. **Add Configuration History**: Track configuration history
7. **Add Configuration Rollback**: Rollback to previous configuration
8. **Add Configuration Encryption**: Encrypt sensitive configuration values
