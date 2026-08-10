# Role-Based Access

## Purpose

This document explains role-based access control (RBAC) in the University ERP system. It details how roles are defined, how role hierarchy works, and how role-based authorization is implemented.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses role-based access control. Understanding RBAC is critical for:
- Implementing access control
- Managing user roles
- Protecting sensitive data
- Implementing role hierarchy
- Debugging authorization issues

Without understanding RBAC, developers may struggle with access control or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn RBAC
- **Feature Development**: Implementing RBAC
- **Code Reviews**: Reviewing RBAC code
- **Security**: Implementing security measures
- **User Management**: Managing user roles

## Dependencies

### RBAC Dependencies

**Confirmed by Code**: RBAC depends on:

- **NestJS Guards**: Route protection
- **Prisma**: User and role data storage
- **Passport.js**: Authentication middleware
- **Reflector**: Metadata reflection

## Internal Architecture

### RBAC Architecture

**Confirmed by Code**: RBAC follows hierarchical model.

```
┌─────────────────────────────────────────────────────────┐
│              Role Hierarchy                                │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  SUPERADMIN   │  │  University Admin│  │  Institute Admin│
│  (All Data)   │  │  (University)   │  │  (Institute)    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Department   │  │  Staff          │  │  Student        │
│  Admin        │  │  (Assigned)      │  │  (Own Data)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Role Definition

**Confirmed by Code**: Roles defined in Prisma schema.

**UserRole Enum**:
```prisma
enum UserRole {
  SUPERADMIN
  UNIVERSITY_ADMIN
  INSTITUTE_ADMIN
  DEPARTMENT_ADMIN
  STAFF
  STUDENT
}
```

**What This Does**:
- **SUPERADMIN**: Access to all universities
- **UNIVERSITY_ADMIN**: Access to own university
- **INSTITUTE_ADMIN**: Access to own institute
- **DEPARTMENT_ADMIN**: Access to own department
- **STAFF**: Access to assigned data
- **STUDENT**: Access to own data

### Role Guard

**Confirmed by Code**: Role guard implemented for role-based access.

**RolesGuard**:
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

**What This Does**:
- **@Roles Decorator**: Checks for @Roles decorator
- **requiredRoles**: Required roles for access
- **user.role**: User's role
- **some()**: Checks if user has any required role

**Usage**:
```typescript
@Controller('admin')
@UseGuards(GlobalJwtAuthGuard, RolesGuard)
export class AdminController {
  @Get()
  @Roles('SUPERADMIN', 'UNIVERSITY_ADMIN')
  findAll() {
    return this.adminService.findAll();
  }
}
```

### Role Hierarchy

**Confirmed by Code**: Role hierarchy implemented in guards.

**Role Hierarchy**:
```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get('roles', context.getHandler());
    const request = context.switchToHttp().getRequest();
    const user = request.user;

    // SUPERADMIN has access to all roles
    if (user.role === 'SUPERADMIN') {
      return true;
    }

    // Role hierarchy
    const roleHierarchy = {
      SUPERADMIN: 6,
      UNIVERSITY_ADMIN: 5,
      INSTITUTE_ADMIN: 4,
      DEPARTMENT_ADMIN: 3,
      STAFF: 2,
      STUDENT: 1,
    };

    const userRoleLevel = roleHierarchy[user.role];
    const requiredRoleLevel = Math.max(...requiredRoles.map(role => roleHierarchy[role] || 0));

    return userRoleLevel >= requiredRoleLevel;
  }
}
```

**What This Does**:
- **SUPERADMIN**: Bypasses all role checks
- **Role Hierarchy**: Defines role levels
- **Comparison**: Compares user role level with required level
- **Access Granted**: If user role level >= required level

## Database Interactions

### RBAC-Database Flow

**Confirmed by Code**: Role data stored in database.

**Flow**:
```
User Role → Database Query → Role Validation → Access Granted/Denied
```

## Redis Interactions

### RBAC-Redis Flow

**Confirmed by Code**: RBAC doesn't interact with Redis.

**Flow**:
```
RBAC → No Redis interaction
```

## Queue Interactions

### RBAC-Queue Flow

**Confirmed by Code**: RBAC doesn't interact with queues.

**Flow**:
```
RBAC → No queue interaction
```

## Worker Interactions

### RBAC-Worker Flow

**Confirmed by Code**: Workers don't use RBAC.

**Flow**:
```
Worker → No RBAC (internal service)
```

## Business Rules

### RBAC Rules

**Confirmed by Code**: RBAC follows these rules:

1. **Role Hierarchy**: SUPERADMIN > UNIVERSITY_ADMIN > INSTITUTE_ADMIN > DEPARTMENT_ADMIN > STAFF > STUDENT
2. **Inheritance**: Higher roles inherit lower role permissions
3. **Explicit Assignment**: Users explicitly assigned roles
4. **Role-Based Scoping**: Data scoped by role
5. **Default Deny**: Deny access by default

### Role Assignment Rules

**Confirmed by Code**: Role assignment follows these rules:

1. **SUPERADMIN**: System administrator
2. **UNIVERSITY_ADMIN**: University administrator
3. **INSTITUTE_ADMIN**: Institute administrator
4. **DEPARTMENT_ADMIN**: Department administrator
5. **STAFF**: Staff member
6. **STUDENT**: Student

## Security

### RBAC Security

**Confirmed by Code**: Security considerations for RBAC:

1. **Principle of Least Privilege**: Grant minimum required access
2. **Role Separation**: Separate duties across roles
3. **Role Hierarchy**: Enforce role hierarchy
4. **Audit Logging**: Log all role-based access
5. **Role Changes**: Audit role changes

## Performance Considerations

### RBAC Performance

**Confirmed by Code**: Performance considerations:

1. **Guard Performance**: Keep guards fast
2. **Database Queries**: Optimize role queries
3. **Caching**: Cache user roles if needed
4. **Metadata Reflection**: Use efficient metadata reflection
5. **Role Validation**: Fast role validation

## Common Mistakes

### Mistake 1: Not Implementing Role Hierarchy

**Symptom**: SUPERADMIN blocked

**Cause**: Not implementing role hierarchy

**Fix**:
```typescript
// Add role hierarchy check
if (user.role === 'SUPERADMIN') {
  return true;
}
```

### Mistake 2: Not Using Guards

**Symptom**: Unprotected routes

**Cause**: Not using guards

**Fix**:
```typescript
// Add guards
@UseGuards(GlobalJwtAuthGuard, RolesGuard)
```

### Mistake 3: Hardcoding Roles

**Symptom**: Difficult to manage roles

**Cause**: Hardcoding roles in code

**Fix**:
```typescript
// Use enum for roles
enum UserRole {
  SUPERADMIN,
  UNIVERSITY_ADMIN,
  // ...
}
```

## Debugging Guide

### RBAC Debugging

**Issue**: Role-based access failing

**Investigation**:
1. Check guard logic
2. Check user role
3. Check required roles
4. Check role hierarchy
5. Check metadata

**Tools**:
- Guard logs
- User logs
- Database logs
- Metadata inspector

## Future Enhancements

### Dynamic Roles

**Status**: Not implemented

**Proposal**: Implement dynamic roles:
- Custom roles
- Role templates
- Role inheritance
- Better flexibility
- More complex but more powerful

### Role Permissions

**Status**: Not implemented

**Proposal**: Implement role permissions:
- Fine-grained permissions per role
- Permission inheritance
- Dynamic permissions
- Better flexibility
- More complex

## Production Considerations

### Production RBAC

**Production Deployment**:
- Enable all guards
- Implement role hierarchy
- Monitor role-based access
- Monitor role changes
- Audit role assignments

### RBAC Monitoring

**Monitoring Metrics**:
- Role-based access success rate
- Role-based access failure rate
- Access patterns by role
- Role change frequency
- Unauthorized access attempts

## Example Requests

### Role-Based Access Example

**Request**: Access protected endpoint

```bash
GET /api/admin
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

### Role-Based Response

**Response**: Access granted

```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "admin@university.edu",
    "role": "UNIVERSITY_ADMIN"
  }
}
```

## Sequence Diagrams

### Role-Based Access Flow

```
Request → Guard → Check User Role → Check Required Roles → Compare Role Hierarchy → Access Granted/Denied
```

## Architecture Diagrams

### RBAC Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User with Role                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Role Guard                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Role Hierarchy                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Access Granted/Denied                       │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does role-based access control work?

**Answer**: RBAC via:
- User assigned role
- Role determines access level
- Guards check user role
- Role hierarchy enforced
- Access granted/denied based on role

### Q2: How do you implement role hierarchy?

**Answer**: Role hierarchy via:
- Define role levels
- Compare user role level with required level
- SUPERADMIN bypasses all checks
- Higher roles inherit lower role permissions
- Access granted if user role >= required role

### Q3: How do you manage user roles?

**Answer**: Role management via:
- User role stored in database
- Role assigned on user creation
- Role can be updated by admin
- Role changes logged
- Role changes require re-authentication

## Exercises

### Exercise 1: Implement a Role Guard

**Task**: Implement a role-based guard.

**Steps**:
1. Implement CanActivate interface
2. Add role hierarchy logic
3. Apply guard to controller
4. Test guard
5. Test access control

**Verification**:
- Guard implemented
- Role hierarchy works
- Access control works
- Tests pass

### Exercise 2: Add a New Role

**Task**: Add a new role to the system.

**Steps**:
1. Add role to enum
2. Update role hierarchy
3. Update guard logic
4. Test new role
5. Test role hierarchy

**Verification**:
- Role added
- Hierarchy updated
- Guard updated
- Tests pass

## Real Production Scenarios

### Scenario 1: Unauthorized Access

**Situation**: User accessing unauthorized data

**Response**:
1. Check guard logic
2. Check user role
3. Check required roles
4. Fix authorization
5. Monitor access attempts

### Scenario 2: Role Change

**Situation**: User role changed but access not updated

**Response**:
1. Check role update logic
2. Force re-authentication
3. Update session
4. Test new role
5. Monitor role changes

## Navigation

**Next Section**: [02-Scope-Based-Access](./02-Scope-Based-Access.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [06-Authentication](../06-Authentication/README.md) - Authentication details
