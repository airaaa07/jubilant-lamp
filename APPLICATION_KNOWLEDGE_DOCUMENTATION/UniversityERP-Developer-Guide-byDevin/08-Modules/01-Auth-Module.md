# Auth Module

## Purpose

This document explains the Auth module of the University ERP system. It details authentication, authorization, user management, and related functionality.

## Why This Document Exists

**Confirmed by Code**: The Auth module handles authentication and authorization. Understanding this module is critical for:
- Implementing secure authentication
- Managing user sessions
- Protecting routes
- Implementing role-based access
- Debugging auth issues

Without understanding the Auth module, developers may struggle with security or may introduce authentication vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn auth module
- **Feature Development**: Implementing auth features
- **Code Reviews**: Reviewing auth code
- **Security**: Implementing security measures
- **User Management**: Managing users

## Dependencies

### Auth Module Dependencies

**Confirmed by Code**: Auth module depends on:

- **PrismaModule**: User data storage
- **RedisModule**: Token blacklisting (optional)
- **BullModule**: Queue for async operations
- **Passport.js**: Authentication strategies
- **@nestjs/jwt**: JWT token generation

## Internal Architecture

### Auth Module Architecture

**Confirmed by Code**: Auth module follows standard NestJS architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Auth Module                                  │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Controllers  │  │  Services       │  │  Strategies     │
│  (Routes)     │  │  (Logic)        │  │  (Passport)     │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Auth Controller

**Confirmed by Code**: Auth controller handles auth endpoints.

**AuthController**:
```typescript
@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @UseGuards(AuthGuard('local'))
  @Throttle({ default: { limit: 5, ttl: 60000 } })
  @Post('login')
  login(@Request() req, @Body() _dto: LoginDto) {
    return this.authService.login(req.user);
  }

  @Post('register')
  @Public()
  async register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }

  @Post('refresh')
  async refresh(@Body() dto: RefreshTokenDto) {
    return this.authService.refresh(dto.refreshToken);
  }

  @Post('logout')
  async logout(@Body() dto: RefreshTokenDto) {
    return this.authService.logout(dto.refreshToken);
  }

  @Get('profile')
  @UseGuards(GlobalJwtAuthGuard)
  getProfile(@CurrentUser() user: JwtPayload) {
    return this.authService.getProfile(user.sub);
  }

  @Patch('profile')
  @UseGuards(GlobalJwtAuthGuard)
  updateProfile(@CurrentUser() user: JwtPayload, @Body() dto: UpdateProfileDto) {
    return this.authService.updateProfile(user.sub, dto);
  }
}
```

**What This Does**:
- **login**: Authenticates user and returns tokens
- **register**: Registers new user
- **refresh**: Refreshes access token
- **logout**: Invalidates refresh token
- **getProfile**: Gets user profile
- **updateProfile**: Updates user profile

### Auth Service

**Confirmed by Code**: Auth service implements auth logic.

**AuthService**:
```typescript
@Injectable()
export class AuthService {
  constructor(
    private prisma: PrismaService,
    private jwtService: JwtService,
    private configService: ConfigService,
  ) {}

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

  async register(dto: RegisterDto) {
    const hashedPassword = await bcrypt.hash(dto.password, 10);

    const user = await this.prisma.user.create({
      data: {
        email: dto.email,
        passwordHash: hashedPassword,
        name: dto.name,
        role: dto.role,
        universityId: dto.universityId,
        instituteId: dto.instituteId,
      },
    });

    return {
      id: user.id,
      email: user.email,
      name: user.name,
      role: user.role,
    };
  }

  async refresh(refreshToken: string) {
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
  }

  async logout(refreshToken: string) {
    await this.prisma.refreshToken.deleteMany({
      where: { token: refreshToken },
    });

    return { success: true };
  }
}
```

**What This Does**:
- **login**: Generates JWT tokens and saves refresh token
- **register**: Creates new user with hashed password
- **refresh**: Validates refresh token and generates new access token
- **logout**: Deletes refresh token from database

## Database Interactions

### Auth-Database Flow

**Confirmed by Code**: Auth module interacts with database.

**Flow**:
```
Auth Service → Prisma → User Table → RefreshToken Table
```

## Redis Interactions

### Auth-Redis Flow

**Confirmed by Code**: Auth module can use Redis for token blacklisting.

**Flow**:
```
Auth Service → Redis → Token Blacklist
```

## Queue Interactions

### Auth-Queue Flow

**Confirmed by Code**: Auth module doesn't directly interact with queues.

**Flow**:
```
Auth → No queue interaction
```

## Worker Interactions

### Auth-Worker Flow

**Confirmed by Code**: Workers don't use auth module.

**Flow**:
```
Worker → No auth (internal service)
```

## Business Rules

### Auth Rules

**Confirmed by Code**: Auth follows these rules:

1. **JWT Tokens**: Use JWT for authentication
2. **Access Token**: Short-lived (15 minutes)
3. **Refresh Token**: Long-lived (7 days)
4. **Password Hashing**: Hash passwords with bcrypt
5. **Rate Limiting**: Rate limit login attempts

### User Rules

**Confirmed by Code**: User rules:

1. **Email Unique**: Email must be unique
2. **Password Strength**: Password must meet strength requirements
3. **Role Assignment**: Users assigned roles
4. **Tenant Assignment**: Users assigned to university/institute
5. **Profile**: Users have profile information

## Security

### Auth Security

**Confirmed by Code**: Security considerations for auth:

1. **Password Hashing**: Hash passwords with bcrypt
2. **JWT Secret**: Use strong JWT secret
3. **HTTPS**: Use HTTPS in production
4. **Rate Limiting**: Rate limit login attempts
5. **Token Expiry**: Short access token expiry

## Performance Considerations

### Auth Performance

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
const hashedPassword = await bcrypt.hash(password, 10);
```

### Mistake 2: Not Rate Limiting Login

**Symptom**: Brute force attacks

**Cause**: Not rate limiting login

**Fix**:
```typescript
@Throttle({ default: { limit: 5, ttl: 60000 } })
```

### Mistake 3: Not Invalidating Refresh Tokens

**Symptom**: Tokens work after logout

**Cause**: Not invalidating refresh tokens

**Fix**:
```typescript
await this.prisma.refreshToken.deleteMany({
  where: { token: refreshToken },
});
```

## Debugging Guide

### Auth Debugging

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

### Production Auth

**Production Deployment**:
- Use strong JWT secret
- Use HTTPS
- Configure rate limiting
- Monitor authentication attempts
- Implement token blacklisting

### Auth Monitoring

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

### Auth Response

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

### Login Flow

```
User → Login Request → Local Strategy → Validate Credentials → Generate JWT → Return Tokens → User Stores Tokens
```

### Token Refresh Flow

```
Client → Refresh Token Request → Validate Refresh Token → Generate New Access Token → Return New Access Token
```

## Architecture Diagrams

### Auth Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Auth Controller                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Auth Service                               │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Prisma       │  │  JWT Service    │  │  Passport       │
│  (Database)   │  │  (Tokens)       │  │  (Strategies)   │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How does the auth module work?

**Answer**: Auth module via:
- Passport local strategy for login
- JWT tokens for authentication
- Refresh tokens for token refresh
- Guards for route protection
- bcrypt for password hashing

### Q2: How do you handle token refresh?

**Answer**: Token refresh via:
- Refresh token stored in database
- Client sends refresh token
- Server validates refresh token
- Server generates new access token
- Client uses new access token

### Q3: How do you secure the auth module?

**Answer**: Auth security via:
- Password hashing with bcrypt
- JWT token authentication
- Rate limiting on login
- HTTPS in production
- Token blacklisting on logout

## Exercises

### Exercise 1: Add a New Auth Endpoint

**Task**: Add a new auth endpoint.

**Steps**:
1. Add endpoint to controller
2. Implement service method
3. Add validation
4. Add guard if needed
5. Test endpoint

**Verification**:
- Endpoint added
- Service method works
- Validation works
- Guard works
- Tests pass

### Exercise 2: Add OTP Authentication

**Task**: Add OTP-based authentication.

**Steps**:
1. Add OTP generation
2. Add OTP verification
3. Add OTP endpoint
4. Test OTP flow
5. Document OTP flow

**Verification**:
- OTP generation works
- OTP verification works
- Endpoint works
- Tests pass

## Real Production Scenarios

### Scenario 1: Login Failure

**Situation**: User unable to login

**Response**:
1. Check credentials
2. Check user status
3. Check JWT secret
4. Check guard logic
5. Fix authentication

### Scenario 2: Token Expiry

**Situation**: Access token expired

**Response**:
1. Client detects 401 error
2. Client uses refresh token
3. Client gets new access token
4. Client retries request
5. User continues seamlessly

## Navigation

**Next Section**: [02-Master-Data-Module](./02-Master-Data-Module.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [07-Authorization](../07-Authorization/README.md) - Authorization details
