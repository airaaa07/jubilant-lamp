# University ERP - Authentication

## Overview

The system uses **JWT (JSON Web Tokens)** for authentication with **Passport.js** as the authentication framework. Authentication is fail-closed by default, with a global JWT guard protecting all routes unless explicitly marked as public.

## Technology Stack

- **Passport 0.6.x**: Authentication middleware
- **@nestjs/passport**: NestJS Passport integration
- **@nestjs/jwt**: JWT token handling
- **bcrypt 5.x**: Password hashing
- **Passport-JWT**: JWT strategy for Passport
- **Passport-Local**: Local strategy for username/password

## Architecture

```
┌─────────────┐
│   Client    │
│             │
│  React App  │
└──────┬──────┘
       │
       │ 1. Login (email/password)
       ↓
┌─────────────┐
│   API       │
│             │
│  Controller │
└──────┬──────┘
       │
       │ 2. LocalAuthGuard
       ↓
┌─────────────┐
│   Passport  │
│             │
│ LocalStrategy│
└──────┬──────┘
       │
       │ 3. Validate credentials
       ↓
┌─────────────┐
│   Service   │
│             │
│ AuthService │
└──────┬──────┘
       │
       │ 4. Generate JWT
       ↓
┌─────────────┐
│   Response  │
│             │
│  JWT Token  │
└──────┬──────┘
       │
       │ 5. Store token
       ↓
┌─────────────┐
│  LocalStorage│
└─────────────┘
```

## JWT Token Structure

### Access Token

- **Purpose**: Short-lived token for API access
- **Expiry**: 15 minutes (configurable via JWT_EXPIRY)
- **Payload**: User ID, email, role, scope, universityId, instituteId

```typescript
{
  sub: userId,
  email: user.email,
  role: user.role,
  scope: user.scope,
  universityId: user.universityId,
  instituteId: user.instituteId,
  iat: issuedAt,
  exp: expiresAt
}
```

### Refresh Token

- **Purpose**: Long-lived token for refreshing access tokens
- **Expiry**: 7 days (configurable via JWT_REFRESH_EXPIRY)
- **Storage**: Database (RefreshToken table) + Redis

## Authentication Flow

### Login Flow

#### 1. User Submits Credentials

```
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password"
}
```

#### 2. LocalAuthGuard Validation

```typescript
// apps/core-api/src/modules/auth/guards/local.guard.ts
@UseGuards(AuthGuard('local'))
@Post('login')
login(@Request() req, @Body() _dto: LoginDto) {
  return this.authService.login(req.user);
}
```

#### 3. Passport Local Strategy

```typescript
// apps/core-api/src/modules/auth/strategies/local.strategy.ts
@Injectable()
export class LocalStrategy extends PassportStrategy(Strategy, 'local') {
  constructor(private authService: AuthService) {
    super({
      usernameField: 'email',
      passwordField: 'password',
    });
  }

  async validate(email: string, password: string): Promise<any> {
    const user = await this.authService.validateUser(email, password);
    if (!user) {
      throw new UnauthorizedException();
    }
    return user;
  }
}
```

#### 4. Service Validation

```typescript
// apps/core-api/src/modules/auth/auth.service.ts
async validateUser(email: string, password: string): Promise<any> {
  const user = await this.prisma.user.findUnique({
    where: { email },
  });

  if (!user) {
    return null;
  }

  const isPasswordValid = await bcrypt.compare(password, user.passwordHash);
  if (!isPasswordValid) {
    return null;
  }

  return user;
}
```

#### 5. Token Generation

```typescript
async login(user: any) {
  const payload = {
    sub: user.id,
    email: user.email,
    role: user.role,
    scope: user.scope,
    universityId: user.universityId,
    instituteId: user.instituteId,
  };

  const accessToken = this.jwtService.sign(payload, {
    expiresIn: this.configService.get('JWT_EXPIRY', '15m'),
  });

  const refreshToken = this.jwtService.sign(payload, {
    expiresIn: this.configService.get('JWT_REFRESH_EXPIRY', '7d'),
  });

  // Store refresh token in database
  await this.prisma.refreshToken.create({
    data: {
      userId: user.id,
      token: refreshToken,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    },
  });

  // Store in Redis for quick access
  await this.redis.setex(
    `refresh:${user.id}`,
    7 * 24 * 60 * 60,
    refreshToken
  );

  return {
    accessToken,
    refreshToken,
    user,
  };
}
```

#### 6. Client Storage

```typescript
// Frontend
localStorage.setItem('accessToken', accessToken);
localStorage.setItem('refreshToken', refreshToken);
```

### Token Refresh Flow

#### 1. Client Sends Refresh Token

```
POST /api/auth/refresh
{
  "refreshToken": "eyJhbGc..."
}
```

#### 2. Service Validation

```typescript
async refreshToken(refreshToken: string) {
  try {
    const payload = this.jwtService.verify(refreshToken);
    
    // Check if token exists in database
    const storedToken = await this.prisma.refreshToken.findUnique({
      where: { token: refreshToken },
    });

    if (!storedToken) {
      throw new UnauthorizedException('Invalid refresh token');
    }

    // Check if expired
    if (storedToken.expiresAt < new Date()) {
      throw new UnauthorizedException('Refresh token expired');
    }

    // Generate new access token
    const newAccessToken = this.jwtService.sign(
      {
        sub: payload.sub,
        email: payload.email,
        role: payload.role,
        scope: payload.scope,
        universityId: payload.universityId,
        instituteId: payload.instituteId,
      },
      { expiresIn: this.configService.get('JWT_EXPIRY', '15m') }
    );

    return { accessToken: newAccessToken };
  } catch (error) {
    throw new UnauthorizedException('Invalid refresh token');
  }
}
```

### Protected Request Flow

#### 1. Client Sends Request with Token

```
GET /api/users
Authorization: Bearer eyJhbGc...
```

#### 2. Global JWT Guard

```typescript
// apps/core-api/src/common/guards/global-jwt.guard.ts
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

#### 3. JWT Strategy Validation

```typescript
// apps/core-api/src/modules/auth/strategies/jwt.strategy.ts
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy, 'jwt') {
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
      include: {
        university: true,
        institute: true,
      },
    });

    if (!user) {
      throw new UnauthorizedException();
    }

    return {
      userId: user.id,
      email: user.email,
      role: user.role,
      scope: user.scope,
      universityId: user.universityId,
      instituteId: user.instituteId,
    };
  }
}
```

#### 4. User Injection

```typescript
// apps/core-api/src/common/decorators/current-user.decorator.ts
export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return data ? request.user?.[data] : request.user;
  },
);

// Usage in controller
@Get()
async findAll(@CurrentUser() user: JwtPayload) {
  return this.service.findAll(user);
}
```

## Guards

### GlobalJwtAuthGuard

- **Purpose**: Fail-closed JWT authentication
- **Behavior**: Requires valid JWT unless route marked @Public
- **Location**: `apps/core-api/src/common/guards/global-jwt.guard.ts`

### JwtAuthGuard

- **Purpose**: Always-enforce JWT (ignores @Public)
- **Usage**: For routes that must be authenticated even in @Public controllers
- **Location**: `apps/core-api/src/modules/auth/guards/jwt.guard.ts`

### ScopeGuard

- **Purpose**: Module-level authorization
- **Behavior**: Checks user has required scope
- **Location**: `apps/core-api/src/modules/auth/guards/scope.guard.ts`

```typescript
@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScope = this.reflector.get<string>(
      'scope',
      context.getHandler()
    );

    if (!requiredScope) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    return user.scope === requiredScope || user.role === 'SUPERADMIN';
  }
}
```

## Decorators

### @Public()

- **Purpose**: Exempt route from global JWT guard
- **Usage**: On controller methods that should be publicly accessible
- **Location**: `apps/core-api/src/common/decorators/public.decorator.ts`

```typescript
export const Public = () => SetMetadata('isPublic', true);

// Usage
@Public()
@Post('register')
async register(@Body() dto: RegisterDto) {
  return this.authService.register(dto);
}
```

### @Scope(scope: string)

- **Purpose**: Require specific module scope
- **Usage**: On controllers or methods
- **Location**: `apps/core-api/src/common/decorators/scope.decorator.ts`

```typescript
export const Scope = (scope: string) => SetMetadata('scope', scope);

// Usage
@Scope('university')
@Controller('master-data/universities')
export class UniversityController {
  // ...
}
```

### @CurrentUser()

- **Purpose**: Inject authenticated user payload
- **Usage**: In controller methods
- **Location**: `apps/core-api/src/common/decorators/current-user.decorator.ts`

```typescript
@Get()
async findAll(@CurrentUser() user: JwtPayload) {
  return this.service.findAll(user);
}
```

## Password Management

### Password Hashing

```typescript
async hashPassword(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(10);
  return bcrypt.hash(password, salt);
}
```

### Password Validation

```typescript
async validatePassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

### Password Policy

```typescript
// apps/core-api/src/common/password-policy.ts
export const passwordPolicy = {
  minLength: 8,
  requireUppercase: true,
  requireLowercase: true,
  requireNumber: true,
  requireSpecialChar: true,
  preventCommonPatterns: true,
};

export function validatePassword(password: string): boolean {
  if (password.length < passwordPolicy.minLength) return false;
  if (passwordPolicy.requireUppercase && !/[A-Z]/.test(password)) return false;
  if (passwordPolicy.requireLowercase && !/[a-z]/.test(password)) return false;
  if (passwordPolicy.requireNumber && !/[0-9]/.test(password)) return false;
  if (passwordPolicy.requireSpecialChar && !/[^A-Za-z0-9]/.test(password)) return false;
  if (passwordPolicy.preventCommonPatterns && isCommonPassword(password)) return false;
  return true;
}
```

### Password History

```typescript
async checkPasswordHistory(userId: string, newPassword: string): Promise<boolean> {
  const history = await this.prisma.passwordHistory.findMany({
    where: { userId },
    orderBy: { createdAt: 'desc' },
    take: 5,
  });

  for (const entry of history) {
    const isSame = await bcrypt.compare(newPassword, entry.passwordHash);
    if (isSame) {
      throw new BadRequestException('Cannot reuse recent passwords');
    }
  }

  return true;
}
```

## OTP System

### Mobile OTP

```typescript
async sendRegistrationOtp(phone: string) {
  const code = generateOtp(); // 6-digit code
  const codeHash = await bcrypt.hash(code, 10);

  await this.prisma.mobileOtp.upsert({
    where: {
      phone_purpose: { phone, purpose: 'registration' },
    },
    create: {
      universityId: user.universityId,
      phone,
      purpose: 'registration',
      codeHash,
      expiresAt: new Date(Date.now() + 10 * 60 * 1000),
    },
    update: {
      codeHash,
      expiresAt: new Date(Date.now() + 10 * 60 * 1000),
      attempts: 0,
    },
  });

  await this.smsService.sendOtp(phone, code);
}
```

### Email OTP

```typescript
async sendRegistrationEmailOtp(email: string) {
  const code = generateOtp();
  const codeHash = await bcrypt.hash(code, 10);

  await this.prisma.emailOtp.upsert({
    where: { email },
    create: {
      email,
      codeHash,
      expiresAt: new Date(Date.now() + 10 * 60 * 1000),
    },
    update: {
      codeHash,
      expiresAt: new Date(Date.now() + 10 * 60 * 1000),
    },
  });

  await this.mailService.sendOtpEmail(email, code);
}
```

## CAPTCHA

### SVG CAPTCHA

```typescript
async generateCaptcha() {
  const captcha = svgCaptcha.create({
    size: 6,
    noise: 2,
    color: true,
    background: '#f0f0f0',
  });

  const token = this.jwtService.sign(
    { text: captcha.text },
    { expiresIn: '5m' }
  );

  return {
    svg: captcha.data,
    token,
  };
}
```

## Environment Variables

```bash
JWT_SECRET=your-secret-key
JWT_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
```

## Security Considerations

### Secret Key

- **JWT_SECRET**: Must be kept secret
- **Generation**: Use strong random string
- **Rotation**: Rotate periodically in production

### Token Expiry

- **Access Token**: Short-lived (15 min) to limit exposure
- **Refresh Token**: Longer-lived (7 days) for convenience
- **Revocation**: Delete refresh token on logout

### HTTPS

- **Production**: Always use HTTPS
- **Development**: HTTP acceptable locally

### Token Storage

- **Frontend**: Store in localStorage (or httpOnly cookie for more security)
- **Backend**: Store refresh token in database + Redis

### Rate Limiting

- **Login**: 5 attempts per minute
- **OTP Send**: 3 attempts per minute
- **OTP Verify**: 10 attempts per minute

## Logout Flow

```typescript
async logout(userId: string) {
  // Delete refresh token from database
  await this.prisma.refreshToken.deleteMany({
    where: { userId },
  });

  // Delete from Redis
  await this.redis.del(`refresh:${userId}`);

  return { success: true };
}
```

## Known Limitations

1. **No Multi-Factor Authentication**: Only password-based auth
2. **No OAuth/Social Login**: No Google/Facebook login
3. **No Session Management**: No active session tracking
4. **No Device Fingerprinting**: No device tracking
5. **No IP Whitelisting**: No IP-based restrictions

## Future Enhancements

1. **MFA**: Add multi-factor authentication
2. **OAuth**: Add social login options
3. **Session Management**: Track active sessions
4. **Device Fingerprinting**: Track devices
5. **IP Whitelisting**: Add IP-based restrictions
6. **Password Expiry**: Enforce password rotation
7. **Account Lockout**: Lock after failed attempts
8. **Audit Logging**: Log all auth events
