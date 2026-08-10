# Session Management

## Purpose

This document explains session management in the University ERP authentication system. It details how sessions are managed, token refresh, and session invalidation.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses JWT-based session management. Understanding session management is critical for:
- Managing user sessions
- Implementing token refresh
- Invalidating sessions
- Preventing session hijacking
- Debugging session issues

Without understanding session management, developers may struggle with session security or may introduce session vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn session management
- **Feature Development**: Implementing session management
- **Code Reviews**: Reviewing session management code
- **Security**: Implementing session security
- **Debugging**: Debugging session issues

## Dependencies

### Session Management Dependencies

**Confirmed by Code**: Session management depends on:

- **JWT**: JSON Web Tokens
- **Prisma**: Refresh token storage
- **Redis**: Token blacklisting (optional)
- **Passport.js**: Authentication middleware

## Internal Architecture

### Session Architecture

**Confirmed by Code**: Session follows JWT-based model.

```
┌─────────────────────────────────────────────────────────┐
│              Session Management                           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Token Issue  │  │  Token Refresh  │  │  Session       │
│  (JWT)        │  │  (Refresh Token)│  │  Invalidation  │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Session Creation

**Confirmed by Code**: Session created on login.

**Login Flow**:
```typescript
async login(user: any) {
  const payload = {
    sub: user.id,
    email: user.email,
    role: user.role,
    universityId: user.universityId,
    instituteId: user.instituteId,
  };

  const accessToken = this.jwtService.sign(payload);
  const refreshToken = this.jwtService.sign(payload, {
    expiresIn: this.configService.get('JWT_REFRESH_EXPIRY', '7d'),
  });

  // Save refresh token
  await this.prisma.refreshToken.create({
    data: {
      token: refreshToken,
      userId: user.id,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    },
  });

  return {
    accessToken,
    refreshToken,
    user: {
      id: user.id,
      email: user.email,
      role: user.role,
      universityId: user.universityId,
      instituteId: user.instituteId,
    },
  };
}
```

**What This Does**:
- **Payload**: JWT payload with user data
- **Access Token**: Short-lived access token
- **Refresh Token**: Long-lived refresh token
- **Save Refresh Token**: Stores refresh token in database
- **Session Created**: User session created

### Token Refresh

**Confirmed by Code**: Session refreshed with refresh token.

**Refresh Flow**:
```typescript
async refresh(refreshToken: string) {
  try {
    const payload = this.jwtService.verify(refreshToken);
    
    const storedToken = await this.prisma.refreshToken.findUnique({
      where: { token: refreshToken },
    });

    if (!storedToken || storedToken.expiresAt < new Date()) {
      throw new UnauthorizedException('Invalid refresh token');
    }

    const user = await this.prisma.user.findUnique({
      where: { id: payload.sub },
    });

    if (!user) {
      throw new UnauthorizedException('User not found');
    }

    const newPayload = {
      sub: user.id,
      email: user.email,
      role: user.role,
      universityId: user.universityId,
      instituteId: user.instituteId,
    };

    const newAccessToken = this.jwtService.sign(newPayload);

    return {
      accessToken: newAccessToken,
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        universityId: user.universityId,
        instituteId: user.instituteId,
      },
    };
  } catch (error) {
    throw new UnauthorizedException('Invalid refresh token');
  }
}
```

**What This Does**:
- **Verify**: Verifies refresh token
- **Check Stored Token**: Checks if token exists in database
- **Check Expiry**: Checks if token is expired
- **Generate New Access Token**: Generates new access token
- **Session Refreshed**: User session refreshed

### Session Invalidation

**Confirmed by Code**: Session invalidated on logout.

**Logout Flow**:
```typescript
async logout(refreshToken: string) {
  await this.prisma.refreshToken.deleteMany({
    where: { token: refreshToken },
  });

  return { success: true };
}
```

**What This Does**:
- **Delete Refresh Token**: Deletes refresh token from database
- **Session Invalidated**: User session invalidated
- **Prevent Refresh**: Prevents token refresh after logout

### Token Blacklisting

**Status**: Not implemented

**Proposal**: Token blacklisting for revoked tokens.

**Token Blacklisting**:
```typescript
async blacklistToken(token: string) {
  const decoded = this.jwtService.decode(token);
  const ttl = decoded.exp - Math.floor(Date.now() / 1000);
  
  await this.redis.setex(`blacklist:${token}`, ttl, '1');
}

async isTokenBlacklisted(token: string): Promise<boolean> {
  const isBlacklisted = await this.redis.get(`blacklist:${token}`);
  return !!isBlacklisted;
}
```

**What This Does**:
- **blacklistToken**: Adds token to blacklist
- **TTL**: Sets TTL based on token expiry
- **isTokenBlacklisted**: Checks if token is blacklisted
- **Prevent Usage**: Prevents blacklisted token usage

## Database Interactions

### Session-Database Flow

**Confirmed by Code**: Session data stored in database.

**Flow**:
```
Login → Generate Tokens → Save Refresh Token → Database
```

## Redis Interactions

### Session-Redis Flow

**Confirmed by Code**: Token blacklisting uses Redis.

**Flow**:
```
Logout → Add Token to Blacklist → Redis
```

## Queue Interactions

### Session-Queue Flow

**Confirmed by Code**: Session doesn't interact with queues.

**Flow**:
```
Session → No queue interaction
```

## Worker Interactions

### Session-Worker Flow

**Confirmed by Code**: Workers don't manage sessions.

**Flow**:
```
Worker → No session interaction
```

## Business Rules

### Session Rules

**Confirmed by Code**: Session follows these rules:

1. **Access Token**: Short-lived (15 minutes)
2. **Refresh Token**: Long-lived (7 days)
3. **Token Storage**: Store refresh token in database
4. **Token Invalidation**: Invalidate tokens on logout
5. **Token Blacklisting**: Blacklist revoked tokens

### Token Refresh Rules

**Confirmed by Code**: Token refresh rules:

1. **Validate**: Validate refresh token before use
2. **Check Expiry**: Check refresh token expiry
3. **Generate New**: Generate new access token
4. **Keep Refresh**: Keep refresh token valid
5. **Rotate**: Consider rotating refresh tokens

## Security

### Session Security

**Confirmed by Code**: Security considerations for sessions:

1. **Short Access Token**: Short access token expiry
2. **Refresh Token Storage**: Store refresh token securely
3. **Token Blacklisting**: Blacklist revoked tokens
4. **HTTPS**: Use HTTPS in production
5. **Token Validation**: Validate every request

## Performance Considerations

### Session Performance

**Confirmed by Code**: Performance considerations:

1. **Token Validation**: Fast token validation
2. **Database Queries**: Optimize refresh token lookup
3. **Caching**: Cache user data if needed
4. **Token Size**: Keep token payload small
5. **Refresh Strategy**: Efficient token refresh

## Common Mistakes

### Mistake 1: Not Invalidating Refresh Tokens

**Symptom**: Tokens work after logout

**Cause**: Not invalidating refresh tokens

**Fix**:
```typescript
// Delete refresh token on logout
await this.prisma.refreshToken.deleteMany({
  where: { token: refreshToken },
});
```

### Mistake 2: Not Checking Token Expiry

**Symptom**: Expired tokens accepted

**Cause**: Not checking token expiry

**Fix**:
```typescript
// Check expiry before using token
if (storedToken.expiresAt < new Date()) {
  throw new UnauthorizedException('Invalid refresh token');
}
```

### Mistake 3: Not Blacklisting Revoked Tokens

**Symptom**: Revoked tokens still work

**Cause**: Not blacklisting revoked tokens

**Fix**:
```typescript
// Blacklist revoked tokens
await this.redis.setex(`blacklist:${token}`, ttl, '1');
```

## Debugging Guide

### Session Debugging

**Issue**: Session not working

**Investigation**:
1. Check token generation
2. Check token validation
3. Check refresh token storage
4. Check token expiry
5. Check session invalidation

**Tools**:
- JWT decoder
- Authentication logs
- Database logs
- Redis logs (if using blacklisting)

## Future Enhancements

### Session Timeout

**Status**: Not implemented

**Proposal**: Implement session timeout:
- Inactivity timeout
- Absolute timeout
- Configurable timeout
- Better security
- User inconvenience

### Concurrent Sessions

**Status**: Not implemented

**Proposal**: Implement concurrent session management:
- Limit concurrent sessions
- Session list
- Session termination
- Better security
- User control

## Production Considerations

### Production Sessions

**Production Deployment**:
- Implement token blacklisting
- Monitor session activity
- Implement session timeout
- Monitor token refresh rate
- Monitor invalid sessions

### Session Monitoring

**Monitoring Metrics**:
- Active sessions
- Session duration
- Token refresh rate
- Token invalidation rate
- Session errors

## Example Requests

### Session Refresh Example

**Request**: Refresh session

```bash
POST /api/auth/refresh
Content-Type: application/json

{
  "refreshToken": "eyJhbGc..."
}
```

**Response**:
```json
{
  "accessToken": "eyJhbGc...",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "role": "STUDENT"
  }
}
```

## Example Responses

### Session Response

**Response**: Session refreshed

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGc...",
    "user": {
      "id": "user-id",
      "email": "user@example.com",
      "role": "STUDENT"
    }
  }
}
```

## Sequence Diagrams

### Session Creation Flow

```
User → Login → Validate Credentials → Generate Tokens → Save Refresh Token → Return Tokens → User Stores Tokens
```

### Token Refresh Flow

```
Client → Refresh Token Request → Validate Refresh Token → Generate New Access Token → Return New Access Token
```

## Architecture Diagrams

### Session Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Access Token (15 min)                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Refresh Token (7 days)                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database (Refresh Token Storage)            │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you manage sessions with JWT?

**Answer**: JWT session management via:
- Access token for API calls (short-lived)
- Refresh token for token refresh (long-lived)
- Store refresh token in database
- Invalidate refresh token on logout
- Blacklist revoked tokens

### Q2: How do you handle session expiry?

**Answer**: Session expiry via:
- Access token expires in 15 minutes
- Refresh token expires in 7 days
- Client uses refresh token to get new access token
- User must re-authenticate if refresh token expires
- Implement session timeout if needed

### Q3: How do you invalidate sessions?

**Answer**: Session invalidation via:
- Delete refresh token on logout
- Blacklist revoked tokens
- Invalidate all user sessions
- Invalidate specific session
- Monitor invalid sessions

## Exercises

### Exercise 1: Implement Session Creation

**Task**: Implement session creation on login.

**Steps**:
1. Validate credentials
2. Generate access token
3. Generate refresh token
4. Save refresh token
5. Return tokens

**Verification**:
- Session created
- Tokens generated
- Refresh token saved
- Tests pass

### Exercise 2: Implement Session Invalidation

**Task**: Implement session invalidation on logout.

**Steps**:
1. Get refresh token
2. Delete refresh token from database
3. Blacklist access token
4. Return success
5. Test invalidation

**Verification**:
- Session invalidated
- Refresh token deleted
- Access token blacklisted
- Tests pass

## Real Production Scenarios

### Scenario 1: Session Hijacking

**Situation**: Access token stolen

**Response**:
1. Invalidate access token
2. Blacklist token
3. Force re-authentication
4. Monitor for suspicious activity
5. Implement MFA

### Scenario 2: Session Expiry

**Situation**: Access token expired

**Response**:
1. Client detects 401 error
2. Client uses refresh token
3. Client gets new access token
4. Client retries request
5. User continues seamlessly

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [02-Password-Hashing](./02-Password-Hashing.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [07-Authorization](../07-Authorization/README.md) - Authorization details
