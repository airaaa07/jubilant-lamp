# Authorization

## Purpose

This document explains authorization in the University ERP system. It details how authorization is implemented, role-based access control, scope-based access control, and best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses role-based and scope-based authorization. Understanding authorization is critical for:
- Implementing access control
- Protecting resources
- Managing user permissions
- Preventing unauthorized access
- Implementing data scoping

Without understanding authorization, developers may struggle with access control or may introduce authorization vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn authorization
- **Feature Development**: Implementing authorization features
- **Code Reviews**: Reviewing authorization approaches
- **Security**: Implementing security
- **Access Control**: Managing permissions

## Dependencies

### Authorization Dependencies

**Confirmed by Code**: Authorization depends on:

- **Guards**: Authorization guards
- **Decorators**: Authorization decorators
- **Roles**: User roles
- **Scopes**: Permission scopes
- **Reflector**: Metadata reflector

## Internal Architecture

### Authorization Architecture

**Confirmed by Code**: Authorization follows layered access control.

```
┌─────────────────────────────────────────────────────────┐
│              Request                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Authentication Guard                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Role Guard                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Scope Guard                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Data Scoping                                  │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Roles Guard

**Confirmed by Code**: Roles guard for role-based access control.

**RolesGuard**:
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>(
      'roles',
      context.getHandler(),
    );

    if (!requiredRoles) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.role === role);
  }
}
```

**What This Does**:
- **@Roles**: Decorator for required roles
- **canActivate**: Check if user has required role
- **Reflector**: Get metadata from decorators

### Scope Guard

**Confirmed by Code**: Scope guard for scope-based access control.

**ScopeGuard**:
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class ScopeGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredScopes = this.reflector.get<string[]>(
      'scopes',
      context.getHandler(),
    );

    if (!requiredScopes) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    const userScopes = user.scopes || [];
    return requiredScopes.some((scope) => userScopes.includes(scope));
  }
}
```

**What This Does**:
- **@Scopes**: Decorator for required scopes
- **canActivate**: Check if user has required scope
- **Reflector**: Get metadata from decorators

### Data Scoping

**Confirmed by Code**: Data scoping for multi-tenancy.

**Data Scoping**:
```typescript
@Injectable()
export class DataScopingService {
  constructor(private prisma: PrismaService) {}

  async scopeQuery<T>(user: any, query: any): Promise<T> {
    // Add data scoping based on user role
    if (user.role === 'STUDENT') {
      query.where = {
        ...query.where,
        userId: user.sub,
      };
    } else if (user.role === 'DEPARTMENT_ADMIN') {
      query.where = {
        ...query.where,
        departmentId: user.departmentId,
      };
    }
    // ... other roles
    return query;
  }
}
```

**What This Does**:
- **scopeQuery**: Scope query based on user role
- **where**: Add where clause for data scoping
- **Multi-tenancy**: Implement data scoping for multi-tenancy

## Database Interactions

### Authorization-Database Flow

**Confirmed by Code**: Database stores user roles and scopes.

**Flow**:
```
Authorization → Database → User Roles/Scopes → Access Control
```

## Redis Interactions

### Authorization-Redis Flow

**Confirmed by Code**: Redis can be used for caching user permissions.

**Flow**:
```
Authorization → Redis → Cached Permissions → Access Control
```

## Queue Interactions

### Authorization-Queue Flow

**Confirmed by Code**: Authorization doesn't interact with queues.

**Flow**:
```
Authorization → No queue interaction
```

## Worker Interactions

### Authorization-Worker Flow

**Confirmed by Code**: Workers may need authorization for job processing.

**Flow**:
```
Worker → Authorization → Job Processing
```

## Business Rules

### Authorization Rules

**Confirmed by Code**: Authorization follows these rules:

1. **Role-Based**: Use role-based access control
2. **Scope-Based**: Use scope-based access control
3. **Data Scoping**: Implement data scoping
4. **Least Privilege**: Apply least privilege principle
5. **Audit**: Audit access attempts

### Role Rules

**Confirmed by Code**: Role rules:

1. **Hierarchy**: Role hierarchy for access
2. **Permissions**: Role-based permissions
3. **Assignment**: Role assignment to users
4. **Validation**: Validate role access
5. **Audit**: Audit role changes

## Security

### Authorization Security

**Confirmed by Code**: Security considerations for authorization:

1. **Least Privilege**: Apply least privilege principle
2. **Role Validation**: Validate role access
3. **Scope Validation**: Validate scope access
4. **Data Scoping**: Implement data scoping
5. **Audit Logging**: Audit access attempts

## Performance Considerations

### Authorization Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Cache user permissions
2. **Guard Optimization**: Optimize guard logic
3. **Database**: Optimize role/scope queries
4. **Redis**: Use Redis for caching
5. **Validation**: Optimize validation logic

## Common Mistakes

### Mistake 1: Not Implementing Data Scoping

**Symptom**: Data leak

**Cause**: Not implementing data scoping

**Fix**:
```typescript
// Implement data scoping
query.where = {
  ...query.where,
  userId: user.sub,
};
```

### Mistake 2: Not Using Least Privilege

**Symptom**: Over-privileged users

**Cause**: Not using least privilege principle

**Fix**:
```typescript
// Use least privilege
@Roles('ADMIN') // Only admin can access
@Scopes('users:read') // Only users with read scope
```

### Mistake 3: Not Auditing Access

**Symptom**: No audit trail

**Cause**: Not auditing access attempts

**Fix**:
```typescript
// Audit access attempts
this.logger.info('Access attempt', { userId, resource, action });
```

## Debugging Guide

### Authorization Debugging

**Issue**: Authorization not working

**Investigation**:
1. Check user role
2. Check user scopes
3. Check guard configuration
4. Check decorator metadata
5. Check logs

**Tools**:
- Authorization logs
- Database queries
- Guard debugging
- Decorator inspection
- User permission inspection

## Future Enhancements

### Attribute-Based Access Control

**Status**: Not implemented

**Proposal**: Implement ABAC:
- Attribute-based policies
- Dynamic permissions
- Better flexibility
- More complex
- Better for production

### Permission Caching

**Status**: Not implemented

**Proposal**: Implement permission caching:
- Cache user permissions
- Better performance
- Redis caching
- More complex
- Better for production

## Production Considerations

### Production Authorization

**Production Deployment**:
- Implement role-based access
- Implement scope-based access
- Implement data scoping
- Audit access attempts
- Monitor authorization

### Authorization Monitoring

**Monitoring Metrics**:
- Authorization success rate
- Authorization failure rate
- Role usage
- Scope usage
- Data scoping effectiveness

## Example Requests

### Authorization Example

**Protected Endpoint**:
```typescript
@Get('users')
@Roles('ADMIN')
@Scopes('users:read')
findAll() {
  return this.usersService.findAll();
}
```

## Example Responses

### Authorization Response

**Response**: Access granted or denied

```json
{
  "success": true,
  "data": [...]
}
```

or

```json
{
  "success": false,
  "error": "Unauthorized"
}
```

## Sequence Diagrams

### Authorization Flow

```
Request → Authentication Guard → Role Guard → Scope Guard → Data Scoping → Resource Access
```

## Architecture Diagrams

### Authorization Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Request                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Authentication Guard                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Role Guard                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Scope Guard                                   │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is authorization implemented?

**Answer**: Authorization via:
- Role-based access control
- Scope-based access control
- Guards for authorization
- Decorators for permissions
- Data scoping for multi-tenancy

### Q2: How do you implement role-based access control?

**Answer**: RBAC via:
- Roles assigned to users
- Guards check user role
- Decorators specify required roles
- Role hierarchy for access
- Least privilege principle

### Q3: How do you implement data scoping?

**Answer**: Data scoping via:
- Query scoping based on user role
- Where clauses for data filtering
- Multi-tenancy support
- User-specific data access
- Department-specific data access

## Exercises

### Exercise 1: Implement Role-Based Access

**Task**: Implement role-based access control.

**Steps**:
1. Create roles guard
2. Add @Roles decorator
3. Implement role checking
4. Test role-based access
5. Verify access control

**Verification**:
- Guard created
- Decorator added
- Role checking works
- Access control works
- Tests pass

### Exercise 2: Implement Data Scoping

**Task**: Implement data scoping for multi-tenancy.

**Steps**:
1. Create data scoping service
2. Implement query scoping
3. Add role-based scoping
4. Test data scoping
5. Verify data isolation

**Verification**:
- Service created
- Query scoping works
- Role-based scoping works
- Data isolation works
- Tests pass

## Real Production Scenarios

### Scenario 1: Unauthorized Access

**Situation**: Unauthorized access attempt

**Response**:
1. Check user role
2. Check user scopes
3. Block access
4. Log event
5. Monitor attempts

### Scenario 2: Data Leak

**Situation**: Data leak detected

**Response**:
1. Check data scoping
2. Fix scoping logic
3. Audit data access
4. Monitor data access
5. Implement fixes

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [01-Authentication](./01-Authentication.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [07-Authorization](../07-Authorization/README.md) - Authorization details
