# Data Scoping

## Purpose

This document explains data scoping in the University ERP system. It details how data is scoped by tenant hierarchy, how data isolation is implemented, and how multi-tenancy is handled.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses data scoping for multi-tenancy. Understanding data scoping is critical for:
- Implementing data isolation
- Preventing data leaks
- Managing multi-tenancy
- Implementing tenant hierarchy
- Debugging data access issues

Without understanding data scoping, developers may struggle with data isolation or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn data scoping
- **Feature Development**: Implementing data scoping
- **Code Reviews**: Reviewing data scoping code
- **Security**: Implementing security measures
- **Multi-Tenancy**: Managing multi-tenancy

## Dependencies

### Data Scoping Dependencies

**Confirmed by Code**: Data scoping depends on:

- **Prisma**: Database queries with scoping
- **NestJS Guards**: Route protection
- **JWT**: User context from JWT
- **TypeScript**: Type-safe scoping

## Internal Architecture

### Data Scoping Architecture

**Confirmed by Code**: Data scoping follows tenant hierarchy.

```
┌─────────────────────────────────────────────────────────┐
│              Tenant Hierarchy                              │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  University   │  │  Institute      │  │  Department     │
│  (Top Level)  │  │  (Middle Level) │  │  (Low Level)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Tenant Hierarchy

**Confirmed by Code**: Tenant hierarchy defined in database.

**Hierarchy Structure**:
```prisma
model University {
  id          String       @id @default(cuid())
  name        String
  institutes  Institute[]
}

model Institute {
  id           String       @id @default(cuid())
  name         String
  universityId String
  university   University   @relation(fields: [universityId], references: [id])
  departments  Department[]
}

model Department {
  id           String      @id @default(cuid())
  name         String
  instituteId  String
  institute    Institute   @relation(fields: [instituteId], references: [id])
  users        User[]
}
```

**What This Does**:
- **University**: Top-level tenant
- **Institute**: Middle-level tenant (belongs to University)
- **Department**: Low-level tenant (belongs to Institute)
- **Hierarchy**: University → Institute → Department

### Data Scoping Implementation

**Confirmed by Code**: Data scoped by user role and tenant.

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
      return { 
        universityId: user.universityId,
        instituteId: user.instituteId,
      };
    case 'DEPARTMENT_ADMIN':
      return { 
        universityId: user.universityId,
        instituteId: user.instituteId,
        departmentId: user.departmentId,
      };
    case 'STAFF':
      return { 
        universityId: user.universityId,
        instituteId: user.instituteId,
        id: user.id,
      };
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

### Prisma Middleware for Data Scoping

**Status**: Not implemented

**Proposal**: Prisma middleware for automatic data scoping.

**Prisma Middleware**:
```typescript
prisma.$use(async (params, next) => {
  const user = getCurrentUser();
  
  if (user && user.role !== 'SUPERADMIN') {
    // Add data scoping to where clause
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = {
        ...params.args.where,
        ...buildWhereClause(user),
      };
    }
  }
  
  return next(params);
});
```

**What This Does**:
- **Middleware**: Intercepts Prisma queries
- **User Context**: Gets current user
- **SUPERADMIN**: Bypasses scoping
- **Auto Scope**: Automatically adds scoping to queries
- **Transparent**: Transparent to application code

## Database Interactions

### Data Scoping-Database Flow

**Confirmed by Code**: Data scoped in database queries.

**Flow**:
```
User Request → Build Where Clause → Database Query with Scoping → Filtered Results
```

## Redis Interactions

### Data Scoping-Redis Flow

**Confirmed by Code**: Data scoping doesn't interact with Redis.

**Flow**:
```
Data Scoping → No Redis interaction
```

## Queue Interactions

### Data Scoping-Queue Flow

**Confirmed by Code**: Data scoping doesn't interact with queues.

**Flow**:
```
Data Scoping → No queue interaction
```

## Worker Interactions

### Data Scoping-Worker Flow

**Confirmed by Code**: Workers don't use data scoping.

**Flow**:
```
Worker → No data scoping (internal service)
```

## Business Rules

### Data Scoping Rules

**Confirmed by Code**: Data scoping follows these rules:

1. **Tenant Hierarchy**: University → Institute → Department
2. **Role-Based Scoping**: Data scoped by user role
3. **SUPERADMIN**: No scoping (access to all)
4. **Default Deny**: Deny access by default
5. **Explicit Allow**: Explicitly allow access

### Scoping Rules by Role

**Confirmed by Code**: Scoping rules by role:

1. **SUPERADMIN**: No filtering
2. **UNIVERSITY_ADMIN**: Filter by universityId
3. **INSTITUTE_ADMIN**: Filter by universityId and instituteId
4. **DEPARTMENT_ADMIN**: Filter by universityId, instituteId, and departmentId
5. **STAFF**: Filter by universityId, instituteId, and userId
6. **STUDENT**: Filter by userId

## Security

### Data Scoping Security

**Confirmed by Code**: Security considerations for data scoping:

1. **Data Isolation**: Ensure data isolation between tenants
2. **Default Deny**: Deny access by default
3. **Explicit Scoping**: Explicitly scope all queries
4. **Audit Logging**: Log all data access
5. **Scoping Validation**: Validate scoping logic

## Performance Considerations

### Data Scoping Performance

**Confirmed by Code**: Performance considerations:

1. **Indexing**: Index foreign keys for scoping
2. **Query Optimization**: Optimize scoped queries
3. **Caching**: Cache scoped results if needed
4. **Middleware Overhead**: Consider middleware overhead
5. **Query Complexity**: Keep scoping simple

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

### Mistake 2: Incorrect Scoping Logic

**Symptom**: Data not properly scoped

**Cause**: Incorrect scoping logic

**Fix**:
```typescript
// Fix scoping logic
case 'INSTITUTE_ADMIN':
  return { 
    universityId: user.universityId,
    instituteId: user.instituteId,
  };
```

### Mistake 3: Not Indexing Foreign Keys

**Symptom**: Slow scoped queries

**Cause**: Not indexing foreign keys

**Fix**:
```prisma
// Add indexes
@@index([universityId])
@@index([instituteId])
@@index([departmentId])
```

## Debugging Guide

### Data Scoping Debugging

**Issue**: Data scoping not working

**Investigation**:
1. Check scoping logic
2. Check user role
3. Check user tenant IDs
4. Check query where clause
5. Test with different roles

**Tools**:
- Prisma logs
- Database logs
- Query inspector
- Console logs

## Future Enhancements

### Automatic Data Scoping

**Status**: Not implemented

**Proposal**: Implement automatic data scoping:
- Prisma middleware
- Automatic scoping
- Transparent to application
- Less boilerplate
- Better security

### Row-Level Security

**Status**: Not implemented

**Proposal**: Implement row-level security:
- Database-level security
- PostgreSQL RLS
- Better security
- Database-enforced
- More complex

## Production Considerations

### Production Data Scoping

**Production Deployment**:
- Implement data scoping on all queries
- Index foreign keys
- Monitor scoping performance
- Monitor data access patterns
- Audit data access

### Data Scoping Monitoring

**Monitoring Metrics**:
- Data access patterns by role
- Data access patterns by tenant
- Scoped query performance
- Data isolation violations
- Unauthorized data access attempts

## Example Requests

### Data Scoping Example

**Request**: Query with data scoping

```typescript
const users = await this.usersService.findAll(user);
```

**Response** (SUPERADMIN):
```json
{
  "data": [
    { "id": "user-1", "universityId": "uni-1" },
    { "id": "user-2", "universityId": "uni-2" }
  ]
}
```

**Response** (UNIVERSITY_ADMIN):
```json
{
  "data": [
    { "id": "user-1", "universityId": "uni-1" }
  ]
}
```

## Example Responses

### Data Scoping Response

**Response**: Scoped data

```json
{
  "success": true,
  "data": [
    {
      "id": "user-id",
      "email": "user@example.com",
      "universityId": "uni-id",
      "instituteId": "inst-id"
    }
  ]
}
```

## Sequence Diagrams

### Data Scoping Flow

```
Request → Get User Context → Build Where Clause → Database Query with Scoping → Filtered Results
```

## Architecture Diagrams

### Data Scoping Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User with Role and Tenant IDs               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Build Where Clause                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database Query                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Filtered Results                           │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does data scoping work?

**Answer**: Data scoping via:
- User role determines scoping level
- Where clause built based on role
- SUPERADMIN: No scoping
- Other roles: Filter by tenant IDs
- Data isolated by tenant hierarchy

### Q2: How do you implement multi-tenancy?

**Answer**: Multi-tenancy via:
- Tenant hierarchy (University → Institute → Department)
- Data scoped by tenant IDs
- User assigned to tenant
- Queries filtered by tenant
- Data isolation enforced

### Q3: How do you ensure data isolation?

**Answer**: Data isolation via:
- Data scoping on all queries
- Role-based scoping
- Tenant hierarchy enforcement
- Audit logging
- Regular security audits

## Exercises

### Exercise 1: Implement Data Scoping

**Task**: Implement data scoping for a query.

**Steps**:
1. Build where clause based on user role
2. Apply where clause to query
3. Test with different roles
4. Verify data isolation
5. Test with SUPERADMIN

**Verification**:
- Scoping implemented
- Where clause correct
- Data isolated
- Tests pass

### Exercise 2: Add a New Role to Scoping

**Task**: Add a new role to scoping logic.

**Steps**:
1. Add role to enum
2. Add scoping logic for new role
3. Test new role
4. Verify data isolation
5. Test with other roles

**Verification**:
- Role added
- Scoping logic added
- Data isolated
- Tests pass

## Real Production Scenarios

### Scenario 1: Data Leak

**Situation**: User seeing data they shouldn't

**Response**:
1. Check scoping logic
2. Fix where clause
3. Test with different roles
4. Verify data isolation
5. Monitor access patterns

### Scenario 2: Performance Issue

**Situation**: Scoped queries slow

**Response**:
1. Check query performance
2. Add missing indexes
3. Optimize scoping logic
4. Test performance
5. Monitor query performance

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [02-Scope-Based-Access](./02-Scope-Based-Access.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [05-Database](../05-Database/README.md) - Database details
