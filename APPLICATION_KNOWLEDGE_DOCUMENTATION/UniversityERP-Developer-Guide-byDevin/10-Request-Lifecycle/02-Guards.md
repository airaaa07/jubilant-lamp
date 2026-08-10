# Guards

## Purpose

This document explains guards in the University ERP system. It details how guards work, how to create custom guards, and how guards fit into the request lifecycle.

## Why This Document Exists

**Confirmed by Code**: Guards are used for authentication and authorization. Understanding guards is critical for:
- Implementing authentication
- Implementing authorization
- Protecting routes
- Debugging auth issues
- Creating custom guards

Without understanding guards, developers may struggle with security or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn guards
- **Feature Development**: Implementing guards
- **Code Reviews**: Reviewing guard code
- **Security**: Implementing security measures
- **Route Protection**: Protecting routes

## Dependencies

### Guards Dependencies

**Confirmed by Code**: Guards depend on:

- **NestJS**: Framework for guards
- **Passport.js**: Authentication strategies
- **Reflector**: Metadata reflection
- **AuthModule**: Authentication service

## Internal Architecture

### Guards Architecture

**Confirmed by Code**: Guards execute after middleware.

```
┌─────────────────────────────────────────────────────────┐
│              Middleware                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Guards                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Interceptors                                 │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Guard Implementation

**Confirmed by Code**: Guards implement CanActivate interface.

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
- **AuthGuard('jwt')**: Extends Passport JWT strategy
- **@Public Decorator**: Checks for public routes
- **Bypass**: Bypasses JWT validation for public routes
- **Default**: Validates JWT for all other routes

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

    if (user.role === 'SUPERADMIN') {
      return true;
    }

    return user.scope === requiredScope;
  }
}
```

**What This Does**:
- **@Scope Decorator**: Checks for @Scope decorator
- **SUPERADMIN**: SUPERADMIN has access to all scopes
- **Scope Check**: Checks if user has required scope
- **Access Control**: Enforces module-level access

**RolesGuard**:
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

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

**What This Does**:
- **@Roles Decorator**: Checks for @Roles decorator
- **requiredRoles**: Required roles for access
- **user.role**: User's role
- **some()**: Checks if user has any required role

### Guard Usage

**Confirmed by Code**: Guards applied at controller or method level.

**Controller-Level Guards**:
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

**What This Does**:
- **@UseGuards**: Applies guards to controller
- **GlobalJwtAuthGuard**: Validates JWT
- **ScopeGuard**: Checks scope
- **@Scope**: Method-level scope

**Method-Level Guards**:
```typescript
@Controller('users')
export class UsersController {
  @Get()
  @UseGuards(GlobalJwtAuthGuard)
  findAll() {
    return this.usersService.findAll();
  }

  @Post()
  @UseGuards(GlobalJwtAuthGuard, RolesGuard)
  @Roles('ADMIN')
  create() {
    return this.usersService.create();
  }
}
```

**What This Does**:
- **@UseGuards**: Applies guards to method
- **@Roles**: Method-level roles
- **Different Guards**: Different guards for different methods

## Database Interactions

### Guards-Database Flow

**Confirmed by Code**: Guards may interact with database for validation.

**Flow**:
```
Guard → Service → Database → Validation Result
```

## Redis Interactions

### Guards-Redis Flow

**Confirmed by Code**: Guards can use Redis for caching.

**Flow**:
```
Guard → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Guards-Queue Flow

**Confirmed by Code**: Guards don't interact with queues.

**Flow**:
```
Guard → No queue interaction
```

## Worker Interactions

### Guards-Worker Flow

**Confirmed by Code**: Workers don't use guards.

**Flow**:
```
Worker → No guards (internal service)
```

## Business Rules

### Guard Rules

**Confirmed by Code**: Guards follow these rules:

1. **CanActivate**: Implement CanActivate interface
2. **Return Boolean**: Return true/false
3. **Async**: Can be async
4. **Metadata**: Use reflector for metadata
5. **Order**: Guards execute in order

### Guard Order Rules

**Confirmed by Code**: Guard order follows these rules:

1. **Authentication First**: Authentication guards first
2. **Authorization Second**: Authorization guards second
3. **Custom Guards**: Custom guards after
4. **Method-Level**: Method-level guards override controller-level
5. **All Must Pass**: All guards must pass

## Security

### Guard Security

**Confirmed by Code**: Security considerations for guards:

1. **Authentication**: Validate authentication
2. **Authorization**: Validate authorization
3. **Role-Based**: Role-based access control
4. **Scope-Based**: Scope-based access control
5. **Data Scoping**: Data scoped by tenant hierarchy

## Performance Considerations

### Guard Performance

**Confirmed by Code**: Performance considerations:

1. **Fast Execution**: Keep guards fast
2. **Caching**: Cache guard results
3. **Database Queries**: Optimize database queries
4. **Metadata Reflection**: Use efficient metadata reflection
5. **Early Return**: Return early on failure

## Common Mistakes

### Mistake 1: Not Returning Boolean

**Symptom**: Guard not working

**Cause**: Not returning boolean

**Fix**:
```typescript
// Return boolean
return true; // or false
```

### Mistake 2: Not Using Reflector

**Symptom**: Metadata not accessible

**Cause**: Not using reflector

**Fix**:
```typescript
// Use reflector
const isPublic = this.reflector.get('isPublic', context.getHandler());
```

### Mistake 3: Not Handling Async

**Symptom**: Guard not working with async operations

**Cause**: Not handling async

**Fix**:
```typescript
// Make guard async
async canActivate(context: ExecutionContext): Promise<boolean> {
  const result = await someAsyncOperation();
  return result;
}
```

## Debugging Guide

### Guard Debugging

**Issue**: Guard not working

**Investigation**:
1. Check guard registration
2. Check guard logic
3. Check metadata
4. Check user data
5. Check logs

**Tools**:
- Guard logs
- Authentication logs
- Metadata inspector
- Console logs

## Future Enhancements

### Dynamic Guards

**Status**: Not implemented

**Proposal**: Implement dynamic guards:
- Guards based on database configuration
- Dynamic role-based guards
- Dynamic scope-based guards
- More flexibility
- More complex

### Permission Guards

**Status**: Not implemented

**Proposal**: Implement permission guards:
- Fine-grained permissions
- Permission-based access control
- Dynamic permissions
- Better security
- More complex

## Production Considerations

### Production Guards

**Production Deployment**:
- Enable all guards
- Configure authentication
- Configure authorization
- Monitor guard performance
- Monitor guard failures

### Guard Monitoring

**Monitoring Metrics**:
- Guard success rate
- Guard failure rate
- Guard execution time
- Authentication failure rate
- Authorization failure rate

## Example Requests

### Guard Example

**Request**:
```bash
GET /api/users
Authorization: Bearer <token>
```

## Example Responses

### Guard Response

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
    "code": 401,
    "message": "Unauthorized"
  }
}
```

## Sequence Diagrams

### Guard Flow

```
Request → Middleware → Guard 1 → Guard 2 → Guard 3 → Interceptors → Controller
```

## Architecture Diagrams

### Guard Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Middleware                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Guard 1 (Auth)                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Guard 2 (Scope)                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Guard 3 (Role)                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Interceptors                                 │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do guards work in NestJS?

**Answer**: Guards via:
- Implement CanActivate interface
- Return true/false
- Execute after middleware
- Can access request context
- Can use metadata

### Q2: How do you create a custom guard?

**Answer**: Custom guard via:
- Implement CanActivate interface
- Add guard logic
- Use reflector for metadata
- Return boolean
- Register guard

### Q3: What is the difference between guards and middleware?

**Answer**: Guards vs Middleware:
- Guards: NestJS-level, executes after middleware
- Middleware: Express-level, executes before guards
- Guards: Can access NestJS context
- Middleware: Can modify request/response
- Guards: Better for auth/authz
- Middleware: Better for preprocessing

## Exercises

### Exercise 1: Create a Guard

**Task**: Create a custom guard.

**Steps**:
1. Implement CanActivate interface
2. Add guard logic
3. Use reflector for metadata
4. Register guard
5. Test guard

**Verification**:
- Guard created
- Logic works
- Metadata works
- Guard registered
- Tests pass

### Exercise 2: Create a Role-Based Guard

**Task**: Create a role-based guard.

**Steps**:
1. Implement CanActivate interface
2. Add role check logic
3. Use @Roles decorator
4. Test guard
5. Test with different roles

**Verification**:
- Guard created
- Role check works
- Decorator works
- Guard works
- Tests pass

## Real Production Scenarios

### Scenario 1: Guard Not Working

**Situation**: Guard not protecting route

**Response**:
1. Check guard registration
2. Check guard logic
3. Check metadata
4. Fix guard
5. Test guard

### Scenario 2: Guard Blocking Valid User

**Situation**: Guard blocking valid user

**Response**:
1. Check guard logic
2. Check user data
3. Check metadata
4. Fix guard
5. Test guard

## Navigation

**Next Section**: [03-Interceptors](./03-Interceptors.md)

**Previous Section**: [01-Middleware](./01-Middleware.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/06-Guards](../03-Backend/06-Guards.md) - Guards details
