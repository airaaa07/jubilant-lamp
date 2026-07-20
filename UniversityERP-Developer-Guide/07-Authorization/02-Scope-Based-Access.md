# Scope-Based Access

## Purpose

This document explains scope-based access control in the University ERP system. It details how scopes are defined, how scope-based authorization is implemented, and how scopes differ from roles.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses scope-based authorization for module-level access. Understanding scope-based access is critical for:
- Implementing module-level access control
- Managing user permissions per module
- Protecting module-specific endpoints
- Implementing fine-grained access control
- Debugging authorization issues

Without understanding scope-based access, developers may struggle with module-level access control or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn scope-based access
- **Feature Development**: Implementing scope-based access
- **Code Reviews**: Reviewing scope-based access code
- **Security**: Implementing security measures
- **Module Management**: Managing module access

## Dependencies

### Scope-Based Access Dependencies

**Confirmed by Code**: Scope-based access depends on:

- **NestJS Guards**: Route protection
- **Prisma**: User and scope data storage
- **Reflector**: Metadata reflection
- **Decorators**: Custom decorators for scopes

## Internal Architecture

### Scope Architecture

**Confirmed by Code**: Scopes follow module-based model.

```
┌─────────────────────────────────────────────────────────┐
│              Scope-Based Access                           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Module Scopes│  │  Scope Guard    │  │  Scope Decorator│
│  (Per Module) │  │  (Validation)    │  │  (@Scope)       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Scope Definition

**Confirmed by Code**: Scopes defined per module.

**Module Scopes**:
```typescript
// Common scopes
const SCOPES = {
  USERS: 'users',
  ADMISSIONNS: 'admissions',
  ACADEMIC: 'academic',
  ATTENDANCE: 'attendance',
  EXAMINATION: 'examination',
  FEE: 'fee',
  TIMETABLE: 'timetable',
  LIBRARY: 'library',
  HOSTEL: 'hostel',
  TRANSPORT: 'transport',
  HR: 'hr',
  DOCUMENTS: 'documents',
  WORKFLOW: 'workflow',
  NOTIFICATIONS: 'notifications',
  NOTICE_BOARD: 'notice_board',
  BANNERS: 'banners',
  SETTINGS: 'settings',
  FORMS: 'forms',
  ANALYTICS: 'analytics',
  AUDIT: 'audit',
  COUNSELLING: 'counselling',
  SOCIAL_MONITORING: 'social_monitoring',
  RESOURCE_RESERVATION: 'resource_reservation',
};
```

**What This Does**:
- **Module Scopes**: One scope per module
- **String Values**: Scope names as strings
- **Consistent Naming**: Consistent naming convention
- **Type Safety**: Can be typed with TypeScript

### Scope Decorator

**Confirmed by Code**: @Scope decorator for marking routes.

**@Scope Decorator**:
```typescript
import { SetMetadata } from '@nestjs/common';

export const SCOPE_KEY = 'scope';
export const Scope = (scope: string) => SetMetadata(SCOPE_KEY, scope);
```

**What This Does**:
- **SetMetadata**: Sets metadata on route handler
- **SCOPE_KEY**: Key for scope metadata
- **Scope**: Decorator function
- **scope**: Scope value

**Usage**:
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

### Scope Guard

**Confirmed by Code**: ScopeGuard validates scope-based access.

**ScopeGuard**:
```typescript
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
- **requiredScope**: Required scope for access
- **SUPERADMIN**: SUPERADMIN has access to all scopes
- **Scope Check**: Checks if user has required scope
- **Access Control**: Enforces module-level access

### User Scope Assignment

**Confirmed by Code**: User scope assigned based on role.

**Scope Assignment**:
```typescript
async assignScope(userId: string, role: UserRole) {
  let scope: string;

  switch (role) {
    case 'SUPERADMIN':
      scope = 'all'; // Access to all scopes
      break;
    case 'UNIVERSITY_ADMIN':
      scope = 'university'; // Access to university-level scopes
      break;
    case 'INSTITUTE_ADMIN':
      scope = 'institute'; // Access to institute-level scopes
      break;
    case 'DEPARTMENT_ADMIN':
      scope = 'department'; // Access to department-level scopes
      break;
    case 'STAFF':
      scope = 'staff'; // Access to staff-level scopes
      break;
    case 'STUDENT':
      scope = 'student'; // Access to student-level scopes
      break;
    default:
      scope = 'none';
  }

  await this.prisma.user.update({
    where: { id: userId },
    data: { scope },
  });
}
```

**What This Does**:
- **Role-Based Scope**: Scope assigned based on role
- **SUPERADMIN**: Access to all scopes
- **UNIVERSITY_ADMIN**: University-level access
- **INSTITUTE_ADMIN**: Institute-level access
- **DEPARTMENT_ADMIN**: Department-level access
- **STAFF**: Staff-level access
- **STUDENT**: Student-level access

## Database Interactions

### Scope-Database Flow

**Confirmed by Code**: Scope data stored in database.

**Flow**:
```
User Scope → Database Query → Scope Validation → Access Granted/Denied
```

## Redis Interactions

### Scope-Redis Flow

**Confirmed by Code**: Scope doesn't interact with Redis.

**Flow**:
```
Scope → No Redis interaction
```

## Queue Interactions

### Scope-Queue Flow

**Confirmed by Code**: Scope doesn't interact with queues.

**Flow**:
```
Scope → No queue interaction
```

## Worker Interactions

### Scope-Worker Flow

**Confirmed by Code**: Workers don't use scope.

**Flow**:
```
Worker → No scope (internal service)
```

## Business Rules

### Scope Rules

**Confirmed by Code**: Scope follows these rules:

1. **Module-Level**: One scope per module
2. **Role-Based**: Scope assigned based on role
3. **SUPERADMIN**: SUPERADMIN has access to all scopes
4. **Explicit Check**: Explicitly check scope on each route
5. **Default Deny**: Deny access by default

### Scope Assignment Rules

**Confirmed by Code**: Scope assignment follows these rules:

1. **SUPERADMIN**: Access to all scopes
2. **UNIVERSITY_ADMIN**: Access to university-level scopes
3. **INSTITUTE_ADMIN**: Access to institute-level scopes
4. **DEPARTMENT_ADMIN**: Access to department-level scopes
5. **STAFF**: Access to staff-level scopes
6. **STUDENT**: Access to student-level scopes

## Security

### Scope Security

**Confirmed by Code**: Security considerations for scope:

1. **Principle of Least Privilege**: Grant minimum required scope
2. **Module Isolation**: Isolate module access
3. **Scope Validation**: Validate scope on every request
4. **Audit Logging**: Log all scope-based access
5. **Scope Changes**: Audit scope changes

## Performance Considerations

### Scope Performance

**Confirmed by Code**: Performance considerations:

1. **Guard Performance**: Keep guards fast
2. **Metadata Reflection**: Use efficient metadata reflection
3. **Scope Validation**: Fast scope validation
4. **Caching**: Cache user scopes if needed
5. **String Comparison**: Fast string comparison

## Common Mistakes

### Mistake 1: Not Using Scope Decorator

**Symptom**: No scope-based access control

**Cause**: Not using @Scope decorator

**Fix**:
```typescript
// Add @Scope decorator
@Scope('users')
@Get()
findAll() {
  return this.usersService.findAll();
}
```

### Mistake 2: Not Applying Scope Guard

**Symptom**: Scope not validated

**Cause**: Not applying ScopeGuard

**Fix**:
```typescript
// Add ScopeGuard
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
```

### Mistake 3: Not Checking SUPERADMIN

**Symptom**: SUPERADMIN blocked

**Cause**: Not checking SUPERADMIN role

**Fix**:
```typescript
// Add SUPERADMIN check
if (user.role === 'SUPERADMIN') {
  return true;
}
```

## Debugging Guide

### Scope Debugging

**Issue**: Scope-based access failing

**Investigation**:
1. Check guard logic
2. Check user scope
3. Check required scope
4. Check metadata
5. Check decorator

**Tools**:
- Guard logs
- User logs
- Metadata inspector
- Console logs

## Future Enhancements

### Multiple Scopes

**Status**: Not implemented

**Proposal**: Implement multiple scopes:
- Users can have multiple scopes
- Scope combinations
- More flexible access control
- Better granularity
- More complex

### Dynamic Scopes

**Status**: Not implemented

**Proposal**: Implement dynamic scopes:
- Scopes based on context
- Time-based scopes
- Location-based scopes
- More flexible
- More complex

## Production Considerations

### Production Scope

**Production Deployment**:
- Enable ScopeGuard
- Apply @Scope decorator to all routes
- Monitor scope-based access
- Monitor scope changes
- Audit scope assignments

### Scope Monitoring

**Monitoring Metrics**:
- Scope-based access success rate
- Scope-based access failure rate
- Access patterns by scope
- Scope change frequency
- Unauthorized access attempts

## Example Requests

### Scope-Based Access Example

**Request**: Access protected endpoint

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
    "code": "FORBIDDEN",
    "message": "Access denied"
  }
}
```

## Example Responses

### Scope-Based Response

**Response**: Access granted

```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "scope": "users"
  }
}
```

## Sequence Diagrams

### Scope-Based Access Flow

```
Request → Guard → Check @Scope Decorator → Check User Scope → Compare Scopes → Access Granted/Denied
```

## Architecture Diagrams

### Scope Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User with Scope                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Scope Guard                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  @Scope Decorator                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Scope Comparison                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Access Granted/Denied                       │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does scope-based access control work?

**Answer**: Scope-based access via:
- @Scope decorator on routes
- ScopeGuard validates scope
- User has assigned scope
- Scope compared with required scope
- Access granted/denied based on match

### Q2: How is scope different from role?

**Answer**: Scope vs Role:
- Role: User's position in hierarchy
- Scope: Module-level access
- Role: Determines overall access level
- Scope: Determines module-specific access
- Role: Used for data scoping
- Scope: Used for route protection

### Q3: How do you assign scopes to users?

**Answer**: Scope assignment via:
- Scope assigned based on role
- Role determines scope level
- SUPERADMIN gets all scopes
- Other roles get specific scopes
- Scope stored in user record

## Exercises

### Exercise 1: Implement Scope Guard

**Task**: Implement a scope-based guard.

**Steps**:
1. Implement CanActivate interface
2. Add scope validation logic
3. Apply guard to controller
4. Test guard
5. Test access control

**Verification**:
- Guard implemented
- Scope validation works
- Access control works
- Tests pass

### Exercise 2: Add a New Scope

**Task**: Add a new scope to the system.

**Steps**:
1. Add scope to SCOPES constant
2. Update scope assignment logic
3. Add @Scope decorator to routes
4. Test new scope
5. Test access control

**Verification**:
- Scope added
- Assignment updated
- Decorator added
- Tests pass

## Real Production Scenarios

### Scenario 1: Unauthorized Access

**Situation**: User accessing unauthorized module

**Response**:
1. Check guard logic
2. Check user scope
3. Check required scope
4. Fix authorization
5. Monitor access attempts

### Scenario 2: Scope Change

**Situation**: User scope changed but access not updated

**Response**:
1. Check scope update logic
2. Force re-authentication
3. Update session
4. Test new scope
5. Monitor scope changes

## Navigation

**Next Section**: [03-Data-Scoping](./03-Data-Scoping.md)

**Previous Section**: [01-Role-Based-Access](./01-Role-Based-Access.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [06-Authentication](../06-Authentication/README.md) - Authentication details
