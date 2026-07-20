# 06-Authentication

## Purpose

This folder provides comprehensive documentation about the authentication system of the University ERP. It explains how authentication works, JWT tokens, refresh tokens, and authentication flows.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses JWT-based authentication. Understanding authentication is critical for:
- Implementing secure authentication
- Managing user sessions
- Protecting routes
- Implementing token refresh
- Debugging authentication issues

Without understanding authentication, developers may struggle with security or may introduce authentication bugs.

## Where This Is Used

- **Onboarding**: New developers learn authentication
- **Feature Development**: Implementing authentication
- **Code Reviews**: Reviewing authentication code
- **Security**: Implementing security measures
- **Debugging**: Debugging authentication issues

## Dependencies

### Authentication Dependencies

**Confirmed by Code**: Authentication depends on:

- **JWT**: JSON Web Tokens
- **Passport.js**: Authentication middleware
- **bcrypt**: Password hashing
- **Prisma**: User data storage
- **Redis**: Token blacklisting (optional)

## Internal Architecture

### Authentication Architecture

**Confirmed by Code**: Authentication follows JWT-based flow.

```
┌─────────────────────────────────────────────────────────┐
│              Authentication Flow                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Login        │  │  Token Issue    │  │  Token Refresh │
│  (Credentials)│  │  (JWT)          │  │  (Refresh Token)│
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Authentication Flow

**Confirmed by Code**: Authentication implemented in auth module.

**Login Endpoint**:
```typescript
@UseGuards(AuthGuard('local'))
@Throttle({ default: { limit: 5, ttl: 60000 } })
@Post('login')
login(@Request() req, @Body() _dto: LoginDto) {
  return this.authService.login(req.user);
}
```

**What This Does**:
- **AuthGuard('local')**: Uses Passport local strategy
- **Throttle**: Rate limits login attempts
- **login()**: Generates JWT tokens
- **req.user**: User from Passport local strategy

**AuthService.login()**:
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
- **accessToken**: Short-lived access token (15 minutes)
- **refreshToken**: Long-lived refresh token (7 days)
- **Save Refresh Token**: Stores refresh token in database
- **Return**: Returns tokens and user data

### JWT Guard

**Confirmed by Code**: JWT guard validates access tokens.

**GlobalJwtAuthGuard**:
```typescript
@Injectable()
export class GlobalJwtAuthGuard extends AuthGuard('jwt') {
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
- **@Public Decorator**: Checks for public routes
- **Bypass**: Bypasses JWT validation for public routes
- **Default**: Validates JWT for all other routes

### Token Refresh

**Confirmed by Code**: Refresh token endpoint updates access token.

**Refresh Endpoint**:
```typescript
@Post('refresh')
async refresh(@Body() dto: RefreshTokenDto) {
  return this.authService.refresh(dto.refreshToken);
}
```

**AuthService.refresh()**:
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
- **Return**: Returns new access token and user data

### Logout

**Confirmed by Code**: Logout endpoint invalidates refresh token.

**Logout Endpoint**:
```typescript
@Post('logout')
async logout(@Body() dto: RefreshTokenDto) {
  return this.authService.logout(dto.refreshToken);
}
```

**AuthService.logout()**:
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
- **Prevent Refresh**: Prevents token refresh after logout

## Database Interactions

### Authentication-Database Flow

**Confirmed by Code**: Authentication interacts with database.

**Flow**:
```
Login → Validate Credentials → Generate Tokens → Save Refresh Token → Database
```

## Redis Interactions

### Authentication-Redis Flow

**Confirmed by Code**: Token blacklisting uses Redis.

**Flow**:
```
Logout → Add Token to Blacklist → Redis
```

## Queue Interactions

### Authentication-Queue Flow

**Confirmed by Code**: Authentication doesn't directly interact with queues.

**Flow**:
```
Authentication → No queue interaction
```

## Worker Interactions

### Authentication-Worker Flow

**Confirmed by Code**: Workers don't use authentication.

**Flow**:
```
Worker → No authentication (internal service)
```

## Business Rules

### Authentication Rules

**Confirmed by Code**: Authentication follows these rules:

1. **JWT Tokens**: Use JWT for authentication
2. **Access Token**: Short-lived access token (15 minutes)
3. **Refresh Token**: Long-lived refresh token (7 days)
4. **Password Hashing**: Hash passwords with bcrypt
5. **Rate Limiting**: Rate limit login attempts

### Token Rules

**Confirmed by Code**: Token rules:

1. **Access Token**: 15 minutes expiry
2. **Refresh Token**: 7 days expiry
3. **Token Storage**: Store refresh token in database
4. **Token Blacklist**: Blacklist revoked tokens
5. **Token Refresh**: Refresh access token before expiry

## Security

### Authentication Security

**Confirmed by Code**: Security measures for authentication:

1. **Password Hashing**: Hash passwords with bcrypt
2. **JWT Secret**: Use strong JWT secret
3. **HTTPS**: Use HTTPS in production
4. **Token Expiry**: Short access token expiry
5. **Rate Limiting**: Rate limit login attempts

## Performance Considerations

### Authentication Performance

**Confirmed by Code**: Performance considerations:

1. **Token Validation**: Fast token validation
2. **Database Queries**: Optimize user lookup
3. **Caching**: Cache user data if needed
4. **Token Size**: Keep token payload small
5. **Refresh Strategy**: Efficient token refresh

## Common Mistakes

### Mistake 1: Not Hashing Passwords

**Symptom**: Plain text passwords in database

**Cause**: Not hashing passwords

**Fix**:
```typescript
// Hash password before storage
const hashedPassword = await bcrypt.hash(password, 10);
```

### Mistake 2: Not Rate Limiting Login

**Symptom**: Brute force attacks

**Cause**: Not rate limiting login

**Fix**:
```typescript
// Add rate limiting
@Throttle({ default: { limit: 5, ttl: 60000 } })
```

### Mistake 3: Not Invalidating Refresh Tokens

**Symptom**: Tokens work after logout

**Cause**: Not invalidating refresh tokens

**Fix**:
```typescript
// Delete refresh token on logout
await this.prisma.refreshToken.deleteMany({
  where: { token: refreshToken },
});
```

## Debugging Guide

### Authentication Debugging

**Issue**: Authentication failing

**Investigation**:
1. Check JWT secret
2. Check token expiry
3. Check refresh token
4. Check user data
5. Check guard logic

**Tools**:
- JWT decoder
- Authentication logs
- Database logs
- Token inspector

## Future Enhancements

### Multi-Factor Authentication

**Status**: Not implemented

**Proposal**: Add MFA:
- TOTP-based MFA
- SMS-based MFA
- Email-based MFA
- Better security
- Required for sensitive operations

### OAuth Integration

**Status**: Not implemented

**Proposal**: Add OAuth integration:
- Google OAuth
- Microsoft OAuth
- SSO support
- Better UX
- Reduced password management

## Production Considerations

### Production Authentication

**Production Deployment**:
- Use strong JWT secret
- Use HTTPS
- Configure rate limiting
- Monitor authentication attempts
- Implement token blacklisting

### Authentication Monitoring

**Monitoring Metrics**:
- Login success rate
- Login failure rate
- Token refresh rate
- Token expiry rate
- Authentication errors

## Example Requests

### Login Example

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

### Authentication Response

**Response**: Authentication successful

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGc...",
    "refreshToken": "eyJhbGc...",
    "user": {
      "id": "user-id",
      "email": "admin@university.edu",
      "role": "SUPERADMIN"
    }
  }
}
```

## Sequence Diagrams

### Authentication Flow

```
User → Login Request → Validate Credentials → Generate JWT → Return Tokens → Store Tokens
```

### Token Refresh Flow

```
Client → Refresh Token Request → Validate Refresh Token → Generate New Access Token → Return New Access Token
```

## Architecture Diagrams

### Authentication Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Client                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Login Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Passport Local Strategy                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  JWT Service                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Tokens                                     │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does JWT authentication work?

**Answer**: JWT authentication via:
- User logs in with credentials
- Server validates credentials
- Server generates JWT token
- Client stores token
- Client sends token with requests
- Server validates token

### Q2: How do you handle token refresh?

**Answer**: Token refresh via:
- Refresh token stored in database
- Client sends refresh token
- Server validates refresh token
- Server generates new access token
- Client uses new access token

### Q3: How do you secure JWT tokens?

**Answer**: JWT security via:
- Use strong JWT secret
- Use HTTPS
- Short access token expiry
- Refresh token rotation
- Token blacklisting on logout

## Exercises

### Exercise 1: Implement Login

**Task**: Implement login endpoint.

**Steps**:
1. Create login DTO
2. Implement local strategy
3. Generate JWT tokens
4. Save refresh token
5. Test login

**Verification**:
- Login implemented
- Tokens generated
- Refresh token saved
- Tests pass

### Exercise 2: Implement Token Refresh

**Task**: Implement token refresh.

**Steps**:
1. Create refresh DTO
2. Validate refresh token
3. Generate new access token
4. Return new token
5. Test refresh

**Verification**:
- Refresh implemented
- Token validated
- New token generated
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

### Scenario 2: Refresh Token Stolen

**Situation**: Refresh token stolen

**Response**:
1. User reports stolen token
2. Invalidate refresh token
3. Force re-authentication
4. Monitor for suspicious activity
5. Implement MFA

## Navigation

**Next Section**: [01-JWT-Tokens](./01-JWT-Tokens.md)

**Previous Section**: [05-Database](../05-Database/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [07-Authorization](../07-Authorization/README.md) - Authorization details
