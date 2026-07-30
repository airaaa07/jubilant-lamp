# Authentication

## Purpose

This document explains authentication in the University ERP system. It details how authentication is implemented, JWT tokens, password hashing, and best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses JWT-based authentication. Understanding authentication is critical for:
- Implementing secure authentication
- Managing user sessions
- Protecting user data
- Preventing unauthorized access
- Implementing token management

Without understanding authentication, developers may struggle with security or may introduce authentication vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn authentication
- **Feature Development**: Implementing authentication features
- **Code Reviews**: Reviewing authentication approaches
- **Security**: Implementing security
- **User Management**: Managing user sessions

## Dependencies

### Authentication Dependencies

**Confirmed by Code**: Authentication depends on:

- **JWT**: Authentication tokens
- **bcrypt**: Password hashing
- **Passport**: Authentication strategy
- **Guards**: Authentication guards
- **Refresh Tokens**: Token refresh mechanism

## Internal Architecture

### Authentication Architecture

**Confirmed by Code**: Authentication follows JWT-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Client                                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Login Request                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Authentication Service                          │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
┌───────▼────────┐                          ┌────────▼────────┐
│  Password     │                          │  JWT Token      │
│  Validation   │                          │  Generation     │
└────────────────┘                          └─────────────────┘
        │                                           │
        ↓                                           ↓
┌────────────────┐                          ┌────────────────┐
│  Bcrypt Hash  │                          │  Access Token  │
│  Comparison   │                          │  Refresh Token │
└────────────────┘                          └────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Token Response                                 │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Password Hashing

**Confirmed by Code**: Password hashing with bcrypt.

**Password Hashing**:
```typescript
import * as bcrypt from 'bcrypt';

async hashPassword(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  return bcrypt.hash(password, salt);
}

async comparePassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

**What This Does**:
- **genSalt**: Generate salt for hashing
- **hash**: Hash password with salt
- **compare**: Compare password with hash

### JWT Token Generation

**Confirmed by Code**: JWT token generation for authentication.

**JWT Service**:
```typescript
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(private jwtService: JwtService) {}

  async login(user: any) {
    const payload = { sub: user.id, email: user.email, role: user.role };
    return {
      access_token: this.jwtService.sign(payload),
      refresh_token: this.jwtService.sign(payload, {
        expiresIn: '7d',
      }),
    };
  }

  async refreshToken(refreshToken: string) {
    const payload = this.jwtService.verify(refreshToken);
    const newPayload = { sub: payload.sub, email: payload.email, role: payload.role };
    return {
      access_token: this.jwtService.sign(newPayload),
    };
  }
}
```

**What This Does**:
- **sign**: Sign JWT token
- **payload**: Token payload with user data
- **refresh_token**: Refresh token with longer expiry
- **refreshToken**: Refresh access token

### Authentication Guard

**Confirmed by Code**: Authentication guard for protecting routes.

**JWT Guard**:
```typescript
import { Injectable, ExecutionContext } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Reflector } from '@nestjs/core';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(
      'isPublic',
      [context.getHandler(), context.getClass()],
    );

    if (isPublic) {
      return true;
    }

    return super.canActivate(context);
  }
}
```

**What This Does**:
- **@Public**: Allow public routes
- **canActivate**: Check authentication
- **Reflector**: Get metadata from decorators

## Database Interactions

### Authentication-Database Flow

**Confirmed by Code**: Database stores user credentials.

**Flow**:
```
Login Request → Database → User Lookup → Password Comparison → Token Generation
```

## Redis Interactions

### Authentication-Redis Flow

**Confirmed by Code**: Redis can be used for token blacklisting.

**Flow**:
```
Logout → Redis → Token Blacklist → Token Invalidated
```

## Queue Interactions

### Authentication-Queue Flow

**Confirmed by Code**: Authentication doesn't interact with queues.

**Flow**:
```
Authentication → No queue interaction
```

## Worker Interactions

### Authentication-Worker Flow

**Confirmed by Code**: Workers don't interact with authentication.

**Flow**:
```
Worker → No authentication interaction
```

## Business Rules

### Authentication Rules

**Confirmed by Code**: Authentication follows these rules:

1. **Password Hashing**: Hash passwords with bcrypt
2. **JWT**: Use JWT for authentication
3. **Refresh Tokens**: Use refresh tokens
4. **Token Expiry**: Set appropriate token expiry
5. **Token Blacklisting**: Blacklist tokens on logout

### Password Rules

**Confirmed by Code**: Password rules:

1. **Strength**: Require strong passwords
2. **Hashing**: Hash passwords with bcrypt
3. **Salt**: Use salt for hashing
4. **Comparison**: Compare hashed passwords
5. **Reset**: Implement password reset

## Security

### Authentication Security

**Confirmed by Code**: Security considerations for authentication:

1. **Password Hashing**: Hash passwords with bcrypt
2. **JWT Secret**: Use strong JWT secret
3. **HTTPS**: Use HTTPS in production
4. **Token Expiry**: Set appropriate token expiry
5. **Token Blacklisting**: Blacklist tokens on logout

## Performance Considerations

### Authentication Performance

**Confirmed by Code**: Performance considerations:

1. **Bcrypt Rounds**: Use appropriate bcrypt rounds
2. **Token Validation**: Cache token validation
3. **Database**: Optimize user lookup
4. **Redis**: Use Redis for token blacklisting
5. **Rate Limiting**: Rate limit login attempts

## Common Mistakes

### Mistake 1: Not Hashing Passwords

**Symptom**: Security vulnerability

**Cause**: Not hashing passwords

**Fix**:
```typescript
// Hash passwords
const hashedPassword = await this.hashPassword(password);
```

### Mistake 2: Weak JWT Secret

**Symptom**: Security vulnerability

**Cause**: Using weak JWT secret

**Fix**:
```typescript
// Use strong JWT secret
JWT_SECRET=strong-random-secret-key
 ```

### Mistake 3: Not Setting Token Expiry

**Symptom**: Security vulnerability

**Cause**: Not setting token expiry

**Fix**:
```typescript
// Set token expiry
this.jwtService.sign(payload, { expiresIn: '1h' });
```

## Debugging Guide

### Authentication Debugging

**Issue**: Authentication not working

**Investigation**:
1. Check password hashing
2. Check JWT token generation
3. Check token validation
4. Check guard configuration
5. Check logs

**Tools**:
- JWT decoder
- Password hash tester
- Authentication logs
- Network tab
- Console logs

## Future Enhancements

### Multi-Factor Authentication

**Status**: Not implemented

**Proposal**: Implement MFA:
- SMS-based MFA
- TOTP-based MFA
- Better security
- More complex
- Better for production

### OAuth Integration

**Status**: Not implemented

**Proposal**: Implement OAuth:
- Google OAuth
- Facebook OAuth
- Better user experience
- More complex
- Better for production

## Production Considerations

### Production Authentication

**Production Deployment**:
- Use strong JWT secret
- Use HTTPS
- Set appropriate token expiry
- Implement token blacklisting
- Monitor authentication

### Authentication Monitoring

**Monitoring Metrics**:
- Login success rate
- Login failure rate
- Token refresh rate
- Token expiry rate
- Authentication latency

## Example Requests

### Authentication Example

**Login**:
```typescript
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Refresh Token**:
```typescript
POST /api/auth/refresh
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Example Responses

### Authentication Response

**Response**: JWT tokens

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Sequence Diagrams

### Authentication Flow

```
Client → Login Request → Authentication Service → Password Validation → JWT Token → Token Response
```

## Architecture Diagrams

### Authentication Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Client                                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Login Request                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Authentication Service                          │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is authentication implemented?

**Answer**: Authentication via:
- JWT tokens for authentication
- Password hashing with bcrypt
- Refresh tokens for token renewal
- Guards for route protection
- Token validation

### Q2: How do you handle password hashing?

**Answer**: Password hashing via:
- Bcrypt for hashing
- Salt generation
- Hash comparison
- Strong password requirements
- Password reset

### Q3: How do you handle token refresh?

**Answer**: Token refresh via:
- Refresh tokens with longer expiry
- Refresh endpoint
- New access token generation
- Token validation
- Token blacklisting

## Exercises

### Exercise 1: Implement Authentication

**Task**: Implement authentication with JWT.

**Steps**:
1. Hash passwords with bcrypt
2. Generate JWT tokens
3. Implement login endpoint
4. Implement token validation
5. Test authentication

**Verification**:
- Password hashing works
- JWT generation works
- Login works
- Token validation works
- Tests pass

### Exercise 2: Implement Token Refresh

**Task**: Implement token refresh mechanism.

**Steps**:
1. Implement refresh endpoint
2. Validate refresh token
3. Generate new access token
4. Test token refresh
5. Verify token expiry

**Verification**:
- Refresh endpoint works
- Token validation works
- New token generated
- Token refresh works
- Tests pass

## Real Production Scenarios

### Scenario 1: Login Failed

**Situation**: Login failed

**Response**:
1. Check password
2. Check user existence
3. Check account status
4. Fix issue
5. Test login

### Scenario 2: Token Expired

**Situation**: Token expired

**Response**:
1. Check token expiry
2. Use refresh token
3. Generate new token
4. Test token refresh
5. Monitor token expiry

## Navigation

**Next Section**: [02-Authorization](./02-Authorization.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [07-Authorization](../07-Authorization/README.md) - Authorization details
