# Security Model

## Purpose

This document explains the security model used in the University ERP system. It details authentication, authorization, data security, and security best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP handles sensitive data including student information, academic records, and financial data. Understanding the security model is critical for:
- Implementing secure features
- Preventing security vulnerabilities
- Protecting sensitive data
- Ensuring compliance
- Troubleshooting security issues

Without understanding the security model, developers may introduce security vulnerabilities or expose sensitive data.

## Where This Is Used

- **Onboarding**: New developers learn security practices
- **Feature Development**: Implementing secure features
- **Security Reviews**: Evaluating security implications
- **Compliance**: Ensuring regulatory compliance
- **Troubleshooting**: Debugging security issues

## Dependencies

### Security Dependencies

**Confirmed by Code**: The security model depends on:

- **Authentication**: JWT tokens, Passport.js
- **Authorization**: Role-based and scope-based access control
- **Encryption**: bcrypt for password hashing
- **Validation**: Zod for input validation
- **Guards**: NestJS guards for route protection
- **Pipes**: NestJS pipes for data validation

## Internal Architecture

### Security Layers

**Confirmed by Code**: The system has multiple security layers:

```
┌─────────────────────────────────────────────────────────┐
│                  Security Layers                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Network Layer │  │  Application    │  │   Data Layer    │
│  (HTTPS, CORS) │  │  (Auth, Guards) │  │ (Encryption,    │
│               │  │                 │  │  Validation)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Authentication Architecture

**Confirmed by Code**: JWT-based authentication with refresh tokens.

**Flow**:
1. User submits credentials
2. Server validates credentials
3. Server generates access token (15 min)
4. Server generates refresh token (7 days)
5. Server stores refresh token in database and Redis
6. Server returns tokens to client
7. Client stores tokens
8. Client sends access token in Authorization header
9. Server validates token on each request
10. Client uses refresh token to get new access token

### Authorization Architecture

**Confirmed by Code**: Role-based and scope-based authorization.

**Roles**:
- SUPERADMIN: Full system access
- UNIVERSITY_ADMIN: University-level access
- INSTITUTE_ADMIN: Institute-level access
- DEPARTMENT_ADMIN: Department-level access
- STAFF: Staff-level access
- STUDENT: Student-level access

**Scopes**:
- Module-level access (e.g., 'university', 'admissions', 'academic')
- Fine-grained access control

## Code Walkthrough

### Authentication Implementation

**Confirmed by Code**: Authentication is implemented in AuthModule.

**Login Flow**:
```typescript
@Injectable()
export class AuthService {
  async login(dto: LoginDto) {
    // Validate credentials
    const user = await this.validateUser(dto.email, dto.password);
    
    // Generate tokens
    const accessToken = this.jwtService.sign({
      sub: user.id,
      email: user.email,
      role: user.role,
      scope: user.scope,
      universityId: user.universityId,
      instituteId: user.instituteId,
    }, { expiresIn: '15m' });

    const refreshToken = this.jwtService.sign({
      sub: user.id,
    }, { expiresIn: '7d' });

    // Store refresh token
    await this.prisma.refreshToken.create({
      data: {
        token: refreshToken,
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
      },
    });

    // Cache refresh token
    await this.redis.setex(`refresh:${user.id}`, 7 * 24 * 60 * 60, refreshToken);

    return { accessToken, refreshToken, user };
  }
}
```

### Guard Implementation

**Confirmed by Code**: Guards protect routes.

**Global JWT Guard**:
```typescript
@Injectable()
export class GlobalJwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(
      'isPublic',
      [context.getHandler(), context.getClass()]
    );

    if (isPublic) {
      return true;
    }

    return super.canActivate(context);
  }
}
```

**Scope Guard**:
```typescript
@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScope = this.reflector.get('scope', context.getHandler());
    
    if (!requiredScope) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    // SUPERADMIN has access to all scopes
    if (user.role === 'SUPERADMIN') {
      return true;
    }

    // Check if user has required scope
    return user.scope === requiredScope;
  }
}
```

### Password Hashing

**Confirmed by Code**: Passwords are hashed with bcrypt.

**Implementation**:
```typescript
import bcrypt from 'bcrypt';

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 10);
}

async function comparePassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

### Input Validation

**Confirmed by Code**: Inputs are validated with Zod.

**Implementation**:
```typescript
import { z } from 'zod';

const LoginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodSchema) {}

  transform(value: any) {
    return this.schema.parse(value);
  }
}
```

## Database Interactions

### Password Storage

**Confirmed by Code**: Passwords are hashed before storage.

**Flow**:
1. User submits password
2. Password is hashed with bcrypt
3. Hashed password is stored in database
4. Original password is never stored

### Refresh Token Storage

**Confirmed by Code**: Refresh tokens are stored in database and Redis.

**Flow**:
1. Refresh token generated
2. Stored in RefreshToken table
3. Cached in Redis
4. Used for token refresh
5. Deleted on logout

## Redis Interactions

### Token Caching

**Confirmed by Code**: Refresh tokens are cached in Redis.

**Implementation**:
```typescript
// Store refresh token
await this.redis.setex(`refresh:${userId}`, 7 * 24 * 60 * 60, refreshToken);

// Retrieve refresh token
const refreshToken = await this.redis.get(`refresh:${userId}`);

// Delete refresh token
await this.redis.del(`refresh:${userId}`);
```

### Session Management

**Confirmed by Code**: Sessions are managed in Redis.

**Implementation**:
```typescript
// Store session
await this.redis.setex(`session:${userId}`, 15 * 60, JSON.stringify(sessionData));

// Retrieve session
const session = await this.redis.get(`session:${userId}`);

// Delete session
await this.redis.del(`session:${userId}`);
```

## Queue Interactions

### Security in Queues

**Confirmed by Code**: Jobs include security context.

**Implementation**:
```typescript
await this.notificationQueue.add('email', {
  userId: user.id,
  universityId: user.universityId,
  instituteId: user.instituteId,
  to: user.email,
  subject: 'Notification',
  body: 'Message',
});
```

## Worker Interactions

### Secure Job Processing

**Confirmed by Code**: Workers process jobs with security context.

**Implementation**:
```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { userId, universityId, instituteId, to, subject, body } = job.data;
    
    // Process with security context
    // Validate user has access to send notification
    // Log audit trail
  }
}
```

## Business Rules

### Authentication Rules

**Confirmed by Code**: Authentication follows these rules:

1. **All routes protected by default**: Unless marked as public
2. **JWT tokens expire**: Access tokens expire in 15 minutes
3. **Refresh tokens expire**: Refresh tokens expire in 7 days
4. **Passwords hashed**: Passwords are hashed with bcrypt
5. **Rate limiting**: Login limited to 5 attempts per minute

### Authorization Rules

**Confirmed by Code**: Authorization follows these rules:

1. **Role-based access**: Users have roles (SUPERADMIN, ADMIN, STAFF, STUDENT)
2. **Scope-based access**: Users have scopes for module access
3. **Tenant scoping**: Data scoped to user's tenant
4. **Fail-closed**: Access denied by default
5. **Explicit grants**: Access must be explicitly granted

### Data Security Rules

**Confirmed by Code**: Data security follows these rules:

1. **Sensitive data encrypted**: Passwords, tokens encrypted
2. **Input validation**: All inputs validated
3. **Output encoding**: All outputs encoded
4. **Audit logging**: All access logged
5. **Data isolation**: Tenant data isolated

## Security

### Authentication Security

**Confirmed by Code**: Authentication security measures:

1. **JWT tokens**: Signed with secret key
2. **Token expiration**: Short-lived access tokens
3. **Refresh tokens**: Long-lived refresh tokens
4. **Token rotation**: Refresh tokens rotated on use
5. **Token revocation**: Tokens can be revoked

### Authorization Security

**Confirmed by Code**: Authorization security measures:

1. **Fail-closed**: Access denied by default
2. **Role hierarchy**: SUPERADMIN > UNIVERSITY_ADMIN > INSTITUTE_ADMIN > DEPARTMENT_ADMIN
3. **Scope enforcement**: Module-level access control
4. **Tenant isolation**: Data isolated by tenant
5. **Audit logging**: All access logged

### Data Security

**Confirmed by Code**: Data security measures:

1. **Password hashing**: bcrypt with salt rounds
2. **Secret management**: Secrets in environment variables
3. **Encryption at rest**: Database encryption (if configured)
4. **Encryption in transit**: HTTPS/TLS
5. **Data masking**: Sensitive data masked in logs

## Performance Considerations

### Security Performance

**Confirmed by Code**: Security performance considerations:

1. **Token validation**: Fast JWT validation
2. **Password hashing**: bcrypt is slow by design
3. **Rate limiting**: Redis-based rate limiting
4. **Cache-based auth**: Session data cached
5. **Guard efficiency**: Guards are lightweight

## Common Mistakes

### Mistake 1: Not Protecting Routes

**Symptom**: Unprotected routes accessible

**Cause**: Not using guards

**Fix**:
```typescript
// Wrong
@Controller('users')
export class UserController {
  @Get()
  async findAll() {
    return this.userService.findAll();
  }
}

// Correct
@Controller('users')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UserController {
  @Get()
  @Scope('users')
  async findAll() {
    return this.userService.findAll();
  }
}
```

### Mistake 2: Storing Passwords in Plain Text

**Symptom**: Passwords not hashed

**Cause**: Not hashing passwords

**Fix**:
```typescript
// Wrong
await prisma.user.create({
  data: { email, password },
});

// Correct
const hashedPassword = await bcrypt.hash(password, 10);
await prisma.user.create({
  data: { email, passwordHash: hashedPassword },
});
```

### Mistake 3: Not Validating Inputs

**Symptom**: Invalid data accepted

**Cause**: Not validating inputs

**Fix**:
```typescript
// Wrong
@Post('register')
async register(@Body() dto: any) {
  return this.authService.register(dto);
}

// Correct
@Post('register')
async register(@Body(new ZodValidationPipe(RegisterSchema)) dto: RegisterDto) {
  return this.authService.register(dto);
}
```

## Debugging Guide

### Security Debugging

**Issue**: Authentication failing

**Investigation**:
1. Check JWT secret
2. Check token expiration
3. Check token payload
4. Check guard logic
5. Check user permissions

**Tools**:
- JWT decoder
- Guard logs
- Service logs

## Future Enhancements

### Multi-Factor Authentication

**Status**: Not implemented

**Proposal**: Implement MFA:
- TOTP-based MFA
- SMS-based MFA
- Email-based MFA
- Recovery codes

### OAuth Integration

**Status**: Not implemented

**Proposal**: Implement OAuth:
- Google OAuth
- Microsoft OAuth
- SAML SSO
- LDAP integration

## Production Considerations

### Security Hardening

**Production Security**:
- Use strong secrets
- Enable HTTPS
- Enable rate limiting
- Enable CORS properly
- Use secure cookies
- Enable HSTS
- Use CSP headers

### Secret Management

**Production Secrets**:
- Use secrets manager (AWS Secrets Manager, Azure Key Vault)
- Rotate secrets regularly
- Never commit secrets
- Use environment-specific secrets
- Audit secret access

## Example Requests

### Authentication Example

**Request**:
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@university.edu",
  "password": "password"
}
```

**Response**:
```json
{
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "user": {
    "id": "user-id",
    "email": "admin@university.edu",
    "role": "SUPERADMIN"
  }
}
```

## Example Responses

### Authorization Example

**Request**:
```bash
GET /api/master-data/universities
Authorization: Bearer <token>
```

**Response** (SUPERADMIN):
```json
{
  "success": true,
  "data": [
    { "id": "uni-1", "name": "University A" },
    { "id": "uni-2", "name": "University B" }
  ]
}
```

**Response** (Other Role):
```json
{
  "success": true,
  "data": [
    { "id": "uni-1", "name": "University A" }
  ]
}
```

## Sequence Diagrams

### Authentication Flow

```
User → Login Form → API Request
                      ↓
                  Local Strategy
                      ↓
                  Validate Credentials
                      ↓
                  Generate JWT Tokens
                      ↓
                  Store Refresh Token
                      ↓
                  Return Tokens
                      ↓
                  Client Stores Tokens
```

### Authorization Flow

```
Request → JWT Guard → Validate Token
                      ↓
                  Extract User
                      ↓
                  Scope Guard → Check Scope
                      ↓
                  Controller → Service
                      ↓
                  Return Response
```

## Architecture Diagrams

### Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Security Architecture                     │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ Authentication │  │ Authorization  │  │   Data Security │
│  (JWT, OAuth)  │  │  (RBAC, ABAC)   │  │ (Encryption,    │
│               │  │                 │  │  Validation)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How does authentication work in the system?

**Answer**: Authentication uses JWT:
- User submits credentials
- Server validates credentials
- Server generates access token (15 min) and refresh token (7 days)
- Client stores tokens
- Client sends access token in Authorization header
- Server validates token on each request
- Client uses refresh token to get new access token

### Q2: How does authorization work in the system?

**Answer**: Authorization uses role-based and scope-based access:
- Users have roles (SUPERADMIN, ADMIN, STAFF, STUDENT)
- Users have scopes for module access
- Guards enforce access control
- Data is scoped to user's tenant
- SUPERADMIN has access to all data

### Q3: How do you secure sensitive data?

**Answer**: Sensitive data is secured via:
- Passwords hashed with bcrypt
- Secrets stored in environment variables
- Data encrypted at rest (if configured)
- Data encrypted in transit (HTTPS/TLS)
- Sensitive data masked in logs
- Audit logging for all access

## Exercises

### Exercise 1: Implement Secure Route

**Task**: Implement a secure route with authentication and authorization.

**Steps**:
1. Create controller
2. Add guards
3. Add scope decorator
4. Test authentication
5. Test authorization

**Verification**:
- Unauthenticated requests rejected
- Unauthorized requests rejected
- Authorized requests succeed

### Exercise 2: Implement Password Reset

**Task**: Implement secure password reset flow.

**Steps**:
1. Generate reset token
2. Send email with reset link
3. Validate reset token
4. Update password
5. Invalidate reset token

**Verification**:
- Reset token expires
- Reset token single-use
- Password hashed
- Old tokens invalidated

## Real Production Scenarios

### Scenario 1: Security Breach

**Situation**: Security breach detected

**Response**:
1. Identify breach scope
2. Revoke all tokens
3. Force password reset
4. Rotate secrets
5. Audit logs
6. Notify users
7. Implement fixes

### Scenario 2: Unauthorized Access

**Situation**: Unauthorized access attempt detected

**Response**:
1. Block IP address
2. Revoke user tokens
3. Investigate logs
4. Notify security team
5. Implement additional controls
6. Monitor for recurrence

## Navigation

**Next Section**: [08-Scalability-Model](./08-Scalability-Model.md)

**Previous Section**: [06-Data-Flow-Patterns](./06-Data-Flow-Patterns.md)

**Related Documentation**:
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [07-Authorization](../07-Authorization/README.md) - Authorization details
- [19-Security](../19-Security/README.md) - Security details
