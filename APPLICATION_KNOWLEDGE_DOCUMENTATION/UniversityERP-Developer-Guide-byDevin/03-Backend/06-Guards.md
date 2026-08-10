# Guards

## Purpose

This document explains the guard pattern used in the University ERP backend. It details how guards protect routes, implement authentication and authorization, and enforce access control.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS guards for route protection. Understanding guards is critical for:
- Implementing authentication
- Implementing authorization
- Protecting sensitive routes
- Enforcing access control
- Securing the application

Without understanding guards, developers may struggle to implement security correctly.

## Where This Is Used

- **Onboarding**: New developers learn guard pattern
- **Feature Development**: Implementing route protection
- **Code Reviews**: Reviewing guard implementation
- **Security**: Implementing security measures
- **Access Control**: Enforcing access control

## Dependencies

### Guard Dependencies

**Confirmed by Code**: Guards depend on:

- **NestJS Guards**: Guard interface
- **Passport.js**: Authentication strategies
- **JWT**: JSON Web Tokens
- **Reflector**: Metadata reflection
- **ExecutionContext**: Execution context

## Internal Architecture

### Guard Architecture

**Confirmed by Code**: Guards follow a layered architecture.

```
┌─────────────────────────────────────────────────────────┐
│                  Guard Layers                              │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Global JWT   │  │  Scope Guard    │  │  Role Guard    │
│  Guard        │  │                │  │                │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Route Access Decision                      │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Guard Definition

**Confirmed by Code**: Guards implement CanActivate interface.

**Basic Guard**:
```typescript
import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';

@Injectable()
export class MyGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    return request.user?.role === 'ADMIN';
  }
}
```

**What This Does**:
- **CanActivate**: Interface for guard
- **ExecutionContext**: Provides request context
- **switchToHttp()**: Switches to HTTP context
- **getRequest()**: Gets request object
- **Returns**: Boolean indicating access granted/denied

### Global JWT Guard

**Confirmed by Code**: Global JWT guard protects all routes by default.

**GlobalJwtAuthGuard**:
```typescript
import { Injectable, ExecutionContext } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Reflector } from '@nestjs/core';

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
- **Extends AuthGuard**: Extends Passport JWT guard
- **Reflector**: Reflects metadata from decorators
- **@Public Decorator**: Checks for @Public decorator
- **Bypass**: Bypasses JWT validation for public routes
- **Default**: Validates JWT for all other routes

**Usage in main.ts**:
```typescript
app.useGlobalGuards(new GlobalJwtAuthGuard());
```

### Scope Guard

**Confirmed by Code**: Scope guard enforces module-level access.

**ScopeGuard**:
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

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

**What This Does**:
- **@Scope Decorator**: Checks for @Scope decorator
- **SUPERADMIN**: SUPERADMIN has access to all scopes
- **Scope Check**: Checks if user has required scope
- **Access Control**: Enforces module-level access

**Usage in Controller**:
```typescript
@Controller('users')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UsersController {
  @Get()
  @Scope('users')
  findAll() {
    return this.usersService.findAll();
  }
}
```

### Role Guard

**Status**: Not implemented

**Proposal**: Role guard for role-based access.

**RoleGuard**:
```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get('roles', context.getHandler());
    
    if (!requiredRoles) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    return requiredRoles.some((role) => user.role === role);
  }
}
```

### Custom Decorators

**Confirmed by Code**: Custom decorators for guard metadata.

**@Public Decorator**:
```typescript
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

**Usage**:
```typescript
@Public()
@Post('register')
register(@Body() dto: RegisterDto) {
  return this.authService.register(dto);
}
```

**@Scope Decorator**:
```typescript
import { SetMetadata } from '@nestjs/common';

export const SCOPE_KEY = 'scope';
export const Scope = (scope: string) => SetMetadata(SCOPE_KEY, scope);
```

**Usage**:
```typescript
@Scope('users')
@Get()
findAll() {
  return this.usersService.findAll();
}
```

**@CurrentUser Decorator**:
```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return data ? request.user?.[data] : request.user;
  },
);
```

**Usage**:
```typescript
@Get('profile')
getProfile(@CurrentUser() user: JwtPayload) {
  return this.usersService.getProfile(user.id);
}
```

## Database Interactions

### Guard-Database Flow

**Confirmed by Code**: Guards don't directly interact with database.

**Flow**:
```
Request → Guard → JWT Validation → User Extraction → Service → Database
```

**Example**:
```typescript
// Guard validates JWT
// User extracted from JWT
// User passed to service
// Service uses user data for database queries
```

## Redis Interactions

### Guard-Redis Flow

**Confirmed by Code**: Guards may check Redis for token validity.

**Token Blacklist**:
```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private redis: RedisService) {
    super();
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const result = await super.canActivate(context);
    
    if (!result) {
      return false;
    }

    const request = context.switchToHttp().getRequest();
    const token = request.headers.authorization?.replace('Bearer ', '');
    
    const isBlacklisted = await this.redis.get(`blacklist:${token}`);
    
    if (isBlacklisted) {
      return false;
    }
    
    return true;
  }
}
```

## Queue Interactions

### Guard-Queue Flow

**Confirmed by Code**: Guards don't directly interact with queues.

**Flow**:
```
Request → Guard → Service → Queue
```

## Worker Interactions

### Guard-Worker Flow

**Confirmed by Code**: Workers don't use guards.

**Flow**:
```
Worker processes job directly without guards
```

## Business Rules

### Guard Rules

**Confirmed by Code**: Guards follow these rules:

1. **Default Protection**: All routes protected by default
2. **Public Routes**: Explicitly marked as public
3. **Scope Enforcement**: Module-level access enforced
4. **Role Hierarchy**: SUPERADMIN has access to all
5. **Fail-Closed**: Access denied by default

### Access Control Rules

**Confirmed by Code**: Access control follows these rules:

1. **SUPERADMIN**: Access to all data
2. **UNIVERSITY_ADMIN**: Access to university data
3. **INSTITUTE_ADMIN**: Access to institute data
4. **DEPARTMENT_ADMIN**: Access to department data
5. **STAFF**: Access to assigned data
6. **STUDENT**: Access to own data

## Security

### Guard Security

**Confirmed by Code**: Security measures in guards:

1. **JWT Validation**: Validate JWT signature and expiry
2. **Token Blacklist**: Blacklist revoked tokens
3. **Scope Enforcement**: Enforce module-level access
4. **Role Enforcement**: Enforce role-based access
5. **Audit Logging**: Log all access attempts

## Performance Considerations

### Guard Performance

**Confirmed by Code**: Performance considerations for guards:

1. **Fast Validation**: Keep guard validation fast
2. **Caching**: Cache user permissions
3. **Metadata Reflection**: Use efficient metadata reflection
4. **Guard Order**: Order guards efficiently
5. **Early Return**: Return early on failure

## Common Mistakes

### Mistake 1: Not Protecting Routes

**Symptom**: Unprotected routes accessible

**Cause**: Not applying guards

**Fix**:
```typescript
// Wrong
@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    return this.usersService.findAll();
  }
}

// Correct
@Controller('users')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UsersController {
  @Get()
  @Scope('users')
  findAll() {
    return this.usersService.findAll();
  }
}
```

### Mistake 2: Not Checking Role Hierarchy

**Symptom**: SUPERADMIN blocked

**Cause**: Not checking role hierarchy

**Fix**:
```typescript
// Add role hierarchy check
if (user.role === 'SUPERADMIN') {
  return true;
}
```

### Mistake 3: Not Implementing Public Routes

**Symptom**: Public routes require authentication

**Cause**: Not implementing @Public decorator

**Fix**:
```typescript
// Add @Public decorator
@Public()
@Post('register')
register(@Body() dto: RegisterDto) {
  return this.authService.register(dto);
}
```

## Debugging Guide

### Guard Debugging

**Issue**: Guard blocking access

**Investigation**:
1. Check guard logic
2. Check JWT token
3. Check user permissions
4. Check scope/role
5. Check metadata

**Tools**:
- JWT decoder
- Guard logs
- User logs
- Metadata inspector

## Future Enhancements

### Role Guard

**Status**: Not implemented

**Proposal**: Implement role guard:
- Role-based access control
- Multiple roles support
- Role hierarchy
- Custom role logic

### Permission Guard

**Status**: Not implemented

**Proposal**: Implement permission guard:
- Fine-grained permissions
- Permission-based access
- Dynamic permissions
- Permission inheritance

## Production Considerations

### Production Guards

**Production Deployment**:
- Enable all guards
- Use strong JWT secrets
- Implement token blacklist
- Monitor guard performance
- Monitor access attempts

### Guard Monitoring

**Monitoring Metrics**:
- Guard execution time
- Access denied rate
- Access granted rate
- JWT validation failures
- Scope violations

## Example Requests

### Guarded Request

**Request**:
```bash
GET /api/users
Authorization: Bearer <token>
```

**Response** (Authorized):
```json
{
  "success": true,
  "data": [...]
}
```

**Response** (Unauthorized):
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Unauthorized"
  }
}
```

## Example Responses

### Guard Decision

**Response**: Guard decision

```json
{
  "access": "granted",
  "reason": "User has required scope"
}
```

## Sequence Diagrams

### Guard Flow

```
Request → Global JWT Guard → Scope Guard → Controller
              ↓                    ↓
          JWT Validation      Scope Check
              ↓                    ↓
          User Extraction      Access Decision
```

## Architecture Diagrams

### Guard Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Global JWT Guard                          │
│                  (Authentication)                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Scope Guard                               │
│                  (Authorization)                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do guards work in NestJS?

**Answer**: Guards in NestJS:
- Implement CanActivate interface
- Return boolean for access decision
- Can access request context
- Can use metadata from decorators
- Applied to controllers or methods

### Q2: How do you implement public routes?

**Answer**: Public routes via:
- @Public decorator to mark routes as public
- Global guard checks for @Public decorator
- Bypasses JWT validation for public routes
- Used for login, register, etc.

### Q3: How do you implement scope-based access control?

**Answer**: Scope-based access via:
- @Scope decorator to set required scope
- Scope guard checks user scope
- SUPERADMIN has access to all scopes
- Module-level access control
- Fine-grained access control

## Exercises

### Exercise 1: Create a Custom Guard

**Task**: Create a custom guard.

**Steps**:
1. Implement CanActivate interface
2. Add guard logic
3. Apply guard to controller
4. Test guard
5. Test access control

**Verification**:
- Guard created
- Guard logic works
- Access control works
- Tests pass

### Exercise 2: Create a Custom Decorator

**Task**: Create a custom decorator.

**Steps**:
1. Create decorator function
2. Set metadata
3. Use in guard
4. Apply to controller
5. Test decorator

**Verification**:
- Decorator created
- Metadata set correctly
- Guard uses metadata
- Works correctly

## Real Production Scenarios

### Scenario 1: Unauthorized Access

**Situation**: User accessing unauthorized data

**Response**:
1. Check guard logic
2. Check user permissions
3. Check scope/role
4. Fix guard logic
5. Monitor access attempts

### Scenario 2: Guard Performance Issue

**Situation**: Guard slow

**Response**:
1. Identify slow guard
2. Optimize guard logic
3. Add caching
4. Monitor performance
5. Test optimization

## Navigation

**Next Section**: [07-Pipes](./07-Pipes.md)

**Previous Section**: [05-DTOs](./05-DTOs.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [07-Authorization](../07-Authorization/README.md) - Authorization details
