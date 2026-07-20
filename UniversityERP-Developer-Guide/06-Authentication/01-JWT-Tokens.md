# JWT Tokens

## Purpose

This document explains JWT (JSON Web Tokens) used in the University ERP authentication system. It details JWT structure, token generation, token validation, and token security.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses JWT for authentication. Understanding JWT is critical for:
- Generating secure tokens
- Validating tokens
- Understanding token structure
- Debugging token issues
- Implementing token security

Without understanding JWT, developers may struggle with authentication or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn JWT
- **Feature Development**: Implementing JWT-based auth
- **Code Reviews**: Reviewing JWT code
- **Security**: Implementing JWT security
- **Debugging**: Debugging JWT issues

## Dependencies

### JWT Dependencies

**Confirmed by Code**: JWT depends on:

- **@nestjs/jwt**: JWT library for NestJS
- **Passport JWT**: Passport JWT strategy
- **bcrypt**: Password hashing
- **Prisma**: User data storage

## Internal Architecture

### JWT Architecture

**Confirmed by Code**: JWT follows standard structure.

```
┌─────────────────────────────────────────────────────────┐
│              JWT Structure                                │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Header       │  │  Payload        │  │  Signature     │
│  (Algorithm)  │  │  (Data)         │  │  (Security)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### JWT Structure

**Confirmed by Code**: JWT has three parts.

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**What This Does**:
- **alg**: Algorithm used (HS256)
- **typ**: Token type (JWT)
- **Base64 Encoded**: Header is base64 encoded

**Payload**:
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "role": "STUDENT",
  "universityId": "uni-id",
  "instituteId": "inst-id",
  "iat": 1234567890,
  "exp": 1234567890
}
```

**What This Does**:
- **sub**: Subject (user ID)
- **email**: User email
- **role**: User role
- **universityId**: University ID
- **instituteId**: Institute ID
- **iat**: Issued at timestamp
- **exp**: Expiration timestamp

**Signature**:
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

**What This Does**:
- **HMACSHA256**: HMAC with SHA-256
- **Header + Payload**: Concatenated header and payload
- **Secret**: JWT secret key
- **Base64 Encoded**: Signature is base64 encoded

### JWT Generation

**Confirmed by Code**: JWT generated with JwtService.

**Generate Access Token**:
```typescript
const payload = {
  sub: user.id,
  email: user.email,
  role: user.role,
  universityId: user.universityId,
  instituteId: user.instituteId,
};

const accessToken = this.jwtService.sign(payload);
```

**What This Does**:
- **Payload**: JWT payload with user data
- **sign()**: Signs payload with secret
- **Default Expiry**: 15 minutes (default)
- **Returns**: JWT token string

**Generate Refresh Token**:
```typescript
const refreshToken = this.jwtService.sign(payload, {
  expiresIn: this.configService.get('JWT_REFRESH_EXPIRY', '7d'),
});
```

**What This Does**:
- **Payload**: Same payload as access token
- **expiresIn**: Custom expiry (7 days)
- **sign()**: Signs payload with secret
- **Returns**: JWT token string

### JWT Validation

**Confirmed by Code**: JWT validated with Passport JWT strategy.

**JWT Strategy**:
```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    private configService: ConfigService,
    private prisma: PrismaService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: configService.get<string>('JWT_SECRET'),
    });
  }

  async validate(payload: any) {
    const user = await this.prisma.user.findUnique({
      where: { id: payload.sub },
    });

    if (!user) {
      throw new UnauthorizedException();
    }

    return user;
  }
}
```

**What This Does**:
- **jwtFromRequest**: Extracts token from Authorization header
- **ignoreExpiration**: Don't ignore token expiry
- **secretOrKey**: JWT secret key
- **validate()**: Validates payload and returns user

### JWT Configuration

**Confirmed by Code**: JWT configured in environment variables.

**Environment Variables**:
```bash
JWT_SECRET=your-secret-key
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
```

**What This Does**:
- **JWT_SECRET**: Secret key for signing tokens
- **JWT_EXPIRY**: Access token expiry
- **JWT_REFRESH_EXPIRY**: Refresh token expiry

## Database Interactions

### JWT-Database Flow

**Confirmed by Code**: JWT payload validated against database.

**Flow**:
```
JWT Token → Validate Payload → Check User in Database → User Validated
```

## Redis Interactions

### JWT-Redis Flow

**Confirmed by Code**: Revoked tokens stored in Redis.

**Flow**:
```
Logout → Add Token to Blacklist → Redis
```

## Queue Interactions

### JWT-Queue Flow

**Confirmed by Code**: JWT doesn't interact with queues.

**Flow**:
```
JWT → No queue interaction
```

## Worker Interactions

### JWT-Worker Flow

**Confirmed by Code**: Workers don't use JWT.

**Flow**:
```
Worker → No JWT (internal service)
```

## Business Rules

### JWT Rules

**Confirmed by Code**: JWT follows these rules:

1. **Access Token**: Short-lived (15 minutes)
2. **Refresh Token**: Long-lived (7 days)
3. **Secret**: Use strong secret key
4. **Payload**: Keep payload minimal
5. **Validation**: Validate every request

### Payload Rules

**Confirmed by Code**: Payload rules:

1. **sub**: Subject (user ID)
2. **Email**: User email
3. **Role**: User role
4. **University ID**: University ID
5. **Institute ID**: Institute ID

## Security

### JWT Security

**Confirmed by Code**: Security considerations for JWT:

1. **Secret Key**: Use strong secret key
2. **HTTPS**: Use HTTPS in production
3. **Expiry**: Short access token expiry
4. **Blacklisting**: Blacklist revoked tokens
5. **Rotation**: Rotate refresh tokens

## Performance Considerations

### JWT Performance

**Confirmed by Code**: Performance considerations:

1. **Validation**: Fast token validation
2. **Payload Size**: Keep payload small
3. **Signature**: Efficient signature verification
4. **Caching**: Cache user data if needed
5. **Refresh**: Efficient token refresh

## Common Mistakes

### Mistake 1: Weak Secret Key

**Symptom**: Tokens easily forged

**Cause**: Using weak secret key

**Fix**:
```bash
# Use strong secret key
JWT_SECRET=$(openssl rand -base64 32)
```

### Mistake 2: Long Access Token Expiry

**Symptom**: Security risk if token stolen

**Cause**: Long access token expiry

**Fix**:
```bash
# Use short expiry
JWT_EXPIRY=15m
```

### Mistake 3: Sensitive Data in Payload

**Symptom**: Sensitive data exposed in token

**Cause**: Including sensitive data in payload

**Fix**:
```typescript
// Keep payload minimal
const payload = {
  sub: user.id,
  email: user.email,
  role: user.role,
};
```

## Debugging Guide

### JWT Debugging

**Issue**: JWT validation failing

**Investigation**:
1. Decode JWT token
2. Check payload
3. Check expiry
4. Check secret key
5. Check token format

**Tools**:
- JWT decoder (jwt.io)
- Authentication logs
- Token inspector
- Console logs

## Future Enhancements

### Token Rotation

**Status**: Not implemented

**Proposal**: Implement token rotation:
- Rotate refresh tokens on use
- One-time use refresh tokens
- Better security
- Prevent token replay
- Reduced attack surface

### Token Binding

**Status**: Not implemented

**Proposal**: Implement token binding:
- Bind token to device/IP
- Prevent token theft
- Better security
- User inconvenience
- Configurable binding

## Production Considerations

### Production JWT

**Production Deployment**:
- Use strong secret key
- Use HTTPS
- Short access token expiry
- Implement token blacklisting
- Monitor token usage

### JWT Monitoring

**Monitoring Metrics**:
- Token validation success rate
- Token validation failure rate
- Token refresh rate
- Token expiry rate
- Token usage patterns

## Example Requests

### JWT Generation Example

**Request**: Generate JWT

```typescript
const token = this.jwtService.sign(payload);
```

## Example Responses

### JWT Response

**Response**: JWT token

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

## Sequence Diagrams

### JWT Flow

```
Login → Validate Credentials → Generate JWT → Return JWT → Client Stores JWT → Client Sends JWT → Validate JWT → Access Granted
```

## Architecture Diagrams

### JWT Architecture

```
┌─────────────────────────────────────────────────────────┐
│              JWT Token                                    │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Header       │  │  Payload        │  │  Signature     │
│  (Base64)     │  │  (Base64)       │  │  (Base64)      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What is JWT and how does it work?

**Answer**: JWT is:
- JSON Web Token
- Self-contained token
- Three parts: header, payload, signature
- Signed with secret key
- Stateless authentication

### Q2: How do you secure JWT tokens?

**Answer**: JWT security via:
- Use strong secret key
- Use HTTPS
- Short access token expiry
- Token blacklisting
- Refresh token rotation

### Q3: What is the difference between access token and refresh token?

**Answer**: Access vs Refresh token:
- Access token: Short-lived (15 minutes), used for API calls
- Refresh token: Long-lived (7 days), used to get new access token
- Access token: Contains user data
- Refresh token: Stored in database
- Access token: Validated on every request

## Exercises

### Exercise 1: Generate JWT

**Task**: Generate a JWT token.

**Steps**:
1. Create payload
2. Sign with secret
3. Set expiry
4. Return token
5. Test token

**Verification**:
- Token generated
- Payload correct
- Signature valid
- Expiry set
- Tests pass

### Exercise 2: Validate JWT

**Task**: Validate a JWT token.

**Steps**:
1. Extract token
2. Verify signature
3. Check expiry
4. Extract payload
5. Return user

**Verification**:
- Token validated
- Signature verified
- Expiry checked
- Payload extracted
- Tests pass

## Real Production Scenarios

### Scenario 1: Token Expiry

**Situation**: Access token expired

**Response**:
1. Client detects 401 error
2. Client uses refresh token
3. Client gets new access token
4. Client retries request
5. User continues seamlessly

### Scenario 2: Token Stolen

**Situation**: Access token stolen

**Response**:
1. Invalidate token
2. Blacklist token
3. Force re-authentication
4. Monitor for suspicious activity
5. Implement MFA

## Navigation

**Next Section**: [02-Password-Hashing](./02-Password-Hashing.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [07-Authorization](../07-Authorization/README.md) - Authorization details
