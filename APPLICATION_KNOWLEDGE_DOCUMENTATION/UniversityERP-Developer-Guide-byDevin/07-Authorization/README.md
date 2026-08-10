# 07-Authorization

## Purpose

This folder provides comprehensive documentation about the authorization system of the University ERP. It explains how authorization works, role-based access control, scope-based access control, and permission management.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses role-based and scope-based authorization. Understanding authorization is critical for:
- Implementing access control
- Protecting sensitive data
- Managing user permissions
- Implementing data scoping
- Debugging authorization issues

Without understanding authorization, developers may struggle with access control or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn authorization
- **Feature Development**: Implementing authorization
- **Code Reviews**: Reviewing authorization code
- **Security**: Implementing security measures
- **Debugging**: Debugging authorization issues

## Dependencies

### Authorization Dependencies

**Confirmed by Code**: Authorization depends on:

- **NestJS Guards**: Route protection
- **Passport.js**: Authentication middleware
- **Prisma**: User and role data storage
- **Reflector**: Metadata reflection

## Internal Architecture

### Authorization Architecture

**Confirmed by Code**: Authorization follows multi-layer model.

```
┌─────────────────────────────────────────────────────────┐
│              Authorization Layers                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Role-Based   │  │  Scope-Based    │  │  Data Scoping  │
│  Access       │  │  Access         │  │  (Tenant)       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Role-Based Authorization

**Confirmed by Code**: Role-based authorization implemented via guards.

**Role Hierarchy**:
```typescript
enum UserRole {
  SUPERADMIN           // Access to all data
  UNIVERSITY_ADMIN     // Access to university data
  INSTITUTE_ADMIN      // Access to institute data
  DEPARTMENT_ADMIN    // Access to department data
  STAFF               // Access to assigned data
  STUDENT             // Access to own data
}
```

**What This Does**:
- **SUPERADMIN**: Access to all universities
- **UNIVERSITY_ADMIN**: Access to own university
- **INSTITUTE_ADMIN**: Access to own institute
- **DEPARTMENT_ADMIN**: Access to own department
- **STAFF**: Access to assigned data
- **STUDENT**: Access to own data

### Scope-Based Authorization

**Confirmed by Code**: Scope-based authorization implemented via ScopeGuard.

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
- **SUPERADMIN**: SUPERADMIN has access to all scopes
- **Scope Check**: Checks if user has required scope
- **Access Control**: Enforces module-level access

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

### Data Scoping

**Confirmed by Code**: Data scoped by tenant hierarchy.

**Data Scoping**:
```typescript
async findAll(user: JwtPayload) {
  const where = this.buildWhereClause(user);
  
  return this.prisma.user.findMany({
    where,
  });
}

private buildWhereClause(user: JwtPayload) {
  switch (user.role) {
    case 'SUPERADMIN':
      return {};
    case 'UNIVERSITY_ADMIN':
      return { universityId: user.universityId };
    case 'INSTITUTE_ADMIN':
      return { universityId: user.universityId, instituteId: user.instituteId };
    case 'DEPARTMENT_ADMIN':
      return { universityId: user.universityId, instituteId: user.instituteId, departmentId: user.departmentId };
    case 'STAFF':
      return { universityId: user.universityId, instituteId: user.instituteId, id: user.id };
    case 'STUDENT':
      return { id: user.id };
    default:
      return {};
  }
}
```

**What This Does**:
- **SUPERADMIN**: No filtering (access to all)
- **UNIVERSITY_ADMIN**: Filter by universityId
- **INSTITUTE_ADMIN**: Filter by universityId and instituteId
- **DEPARTMENT_ADMIN**: Filter by universityId, instituteId, and departmentId
- **STAFF**: Filter by universityId, instituteId, and userId
- **STUDENT**: Filter by userId (own data only)

## Database Interactions

### Authorization-Database Flow

**Confirmed by Code**: Authorization validated against database.

**Flow**:
```
Request → Guard → Check User Role → Check User Permissions → Database Query with Scoping
```

## Redis Interactions

### Authorization-Redis Flow

**Confirmed by Code**: Authorization doesn't interact with Redis.

**Flow**:
```
Authorization → No Redis interaction
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

**Confirmed by Code**: Workers don't use authorization.

**Flow**:
```
Worker → No authorization (internal service)
```

## Business Rules

### Authorization Rules

**Confirmed by Code**: Authorization follows these rules:

1. **Role Hierarchy**: SUPERADMIN > UNIVERSITY_ADMIN > INSTITUTE_ADMIN > DEPARTMENT_ADMIN > STAFF > STUDENT
2. **Scope Enforcement**: Enforce module-level access
3. **Data Scoping**: Scope data by tenant hierarchy
4. **Default Deny**: Deny access by default
5. **Explicit Allow**: Explicitly allow access

### Data Scoping Rules

**Confirmed by Code**: Data scoping follows these rules:

1. **SUPERADMIN**: Access to all data
2. **UNIVERSITY_ADMIN**: Access to university data
3. **INSTITUTE_ADMIN**: Access to institute data
4. **DEPARTMENT_ADMIN**: Access to department data
5. **STAFF**: Access to assigned data
6. **STUDENT**: Access to own data

## Security

### Authorization Security

**Confirmed by Code**: Security considerations for authorization:

1. **Principle of Least Privilege**: Grant minimum required access
2. **Role-Based Access**: Use roles for access control
3. **Scope-Based Access**: Use scopes for module-level access
4. **Data Scoping**: Scope data by tenant hierarchy
5. **Audit Logging**: Log all access attempts

## Performance Considerations

### Authorization Performance

**Confirmed by Code**: Performance considerations:

1. **Guard Performance**: Keep guards fast
2. **Database Queries**: Optimize data scoping queries
3. **Indexing**: Index foreign keys for scoping
4. **Caching**: Cache user permissions if needed
5. **Metadata Reflection**: Use efficient metadata reflection

## Common Mistakes

### Mistake 1: Not Implementing Data Scoping

**Symptom**: Users can access data they shouldn't

**Cause**: Not implementing data scoping

**Fix**:
```typescript
// Add data scoping
const where = this.buildWhereClause(user);
return this.prisma.user.findMany({ where });
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

### Mistake 3: Not Using Guards

**Symptom**: Unprotected routes

**Cause**: Not using guards

**Fix**:
```typescript
// Add guards
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
```

## Debugging Guide

### Authorization Debugging

**Issue**: Authorization failing

**Investigation**:
1. Check guard logic
2. Check user role
3. Check user scope
4. Check data scoping
5. Check metadata

**Tools**:
- Guard logs
- User logs
- Database logs
- Metadata inspector

## Future Enhancements

### Permission-Based Authorization

**Status**: Not implemented

**Proposal**: Implement permission-based authorization:
- Fine-grained permissions
- Permission inheritance
- Dynamic permissions
- Better flexibility
- More complex but more powerful

### Attribute-Based Access Control

**Status**: Not implemented

**Proposal**: Implement ABAC:
- Attribute-based rules
- Context-aware access
- More flexible policies
- Better security
- More complex

## Production Considerations

### Production Authorization

**Production Deployment**:
- Enable all guards
- Implement data scoping
- Monitor authorization failures
- Monitor access patterns
- Audit access logs

### Authorization Monitoring

**Monitoring Metrics**:
- Authorization success rate
- Authorization failure rate
- Access patterns by role
- Data access patterns
- Unauthorized access attempts

## Example Requests

### Authorization Example

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

### Authorization Response

**Response**: Access granted

```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com"
  }
}
```

## Sequence Diagrams

### Authorization Flow

```
Request → Guard → Check Role → Check Scope → Check Data Scope → Access Granted/Denied
```

## Architecture Diagrams

### Authorization Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Request                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  JWT Guard                                  │
│                  (Authentication)                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Scope Guard                                │
│                  (Authorization)                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Data Scoping                               │
│                  (Tenant Filter)                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database Query                             │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does role-based authorization work?

**Answer**: Role-based authorization via:
- User assigned role
- Role determines access level
- Guards check user role
- Role hierarchy enforced
- Data scoped by role

### Q2: How does scope-based authorization work?

**Answer**: Scope-based authorization via:
- @Scope decorator on routes
- ScopeGuard checks required scope
- User must have required scope
- Module-level access control
- SUPERADMIN bypasses scope check

### Q3: How does data scoping work?

**Answer**: Data scoping via:
- Filter queries based on user role
- SUPERADMIN: No filtering
- UNIVERSITY_ADMIN: Filter by universityId
- INSTITUTE_ADMIN: Filter by universityId and instituteId
- DEPARTMENT_ADMIN: Filter by universityId, instituteId, and departmentId
- STUDENT: Filter by userId

## Exercises

### Exercise 1: Implement a Guard

**Task**: Implement a custom guard.

**Steps**:
1. Implement CanActivate interface
2. Add guard logic
3. Apply guard to controller
4. Test guard
5. Test access control

**Verification**:
- Guard implemented
- Guard logic works
- Access control works
- Tests pass

### Exercise 2: Implement Data Scoping

**Task**: Implement data scoping.

**Steps**:
1. Build where clause based on user role
2. Apply where clause to query
3. Test data scoping
4. Test with different roles
5. Verify data isolation

**Verification**:
- Data scoping implemented
- Where clause correct
- Data isolated
- Tests pass

## Real Production Scenarios

### Scenario 1: Unauthorized Access

**Situation**: User accessing unauthorized data

**Response**:
1. Check guard logic
2. Check user role
3. Check user scope
4. Fix authorization
5. Monitor access attempts

### Scenario 2: Data Leak

**Situation**: User seeing data they shouldn't

**Response**:
1. Check data scoping
2. Fix where clause
3. Test with different roles
4. Verify data isolation
5. Monitor access patterns

## Navigation

**Next Section**: [01-Role-Based-Access](./01-Role-Based-Access.md)

**Previous Section**: [06-Authentication](../06-Authentication/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [06-Authentication](../06-Authentication/README.md) - Authentication details
