# Multi-Tenancy Model

## Purpose

This document explains the multi-tenancy model used in the University ERP system. It details the hierarchy, data scoping, access control, and implementation patterns.

## Why This Document Exists

**Confirmed by Code**: The University ERP is designed as a multi-tenant system supporting multiple universities, institutes, and departments. Understanding the multi-tenancy model is critical for:
- Implementing correct data scoping
- Ensuring data isolation between tenants
- Implementing proper access control
- Designing tenant-specific features
- Troubleshooting tenant-related issues

Without understanding the multi-tenancy model, developers may accidentally expose data across tenants or implement incorrect access control.

## Where This Is Used

- **Onboarding**: New developers learn the multi-tenancy model
- **Feature Development**: Implementing tenant-specific features
- **Security Reviews**: Ensuring proper data isolation
- **Data Migration**: Migrating tenant data
- **Troubleshooting**: Debugging tenant-related issues

## Dependencies

### Multi-Tenancy Dependencies

**Confirmed by Code**: The multi-tenancy model depends on:

- **Database Schema**: University, Institute, Department tables
- **Authentication**: JWT payload includes universityId and instituteId
- **Authorization**: Scope guards enforce tenant access
- **Data Scoping**: Services filter data by tenant

## Internal Architecture

### Tenant Hierarchy

**Confirmed by Code**: The system uses a hierarchical multi-tenancy model.

```
University (Top-level tenant)
    ↓
Institute (Second-level tenant)
    ↓
Department (Third-level tenant)
```

### Hierarchy Details

**University**:
- **Purpose**: Top-level tenant representing a university
- **Scope**: All data belongs to a university
- **Access**: University-level administrators have access to all institutes
- **Database Table**: `University`

**Institute**:
- **Purpose**: Second-level tenant representing a campus or college within a university
- **Scope**: Data belongs to an institute within a university
- **Access**: Institute-level administrators have access to their institute only
- **Database Table**: `Institute`
- **Foreign Key**: `universityId` references `University`

**Department**:
- **Purpose**: Third-level tenant representing an academic department
- **Scope**: Data belongs to a department within an institute
- **Access**: Department-level administrators have access to their department only
- **Database Table**: `Department`
- **Foreign Key**: `instituteId` references `Institute`

## Code Walkthrough

### Database Schema

**Confirmed by Code**: The database schema defines the tenant hierarchy.

```prisma
// apps/core-api/prisma/schema.prisma

model University {
  id          String   @id @default(cuid())
  name        String
  shortName   String
  domain      String?
  logoUrl     String?
  config      Json?
  institutes  Institute[]
  users       User[]
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model Institute {
  id           String      @id @default(cuid())
  universityId String
  university   University  @relation(fields: [universityId], references: [id])
  name         String
  shortName    String
  address      String?
  city         String?
  state        String?
  country      String?
  pincode      String?
  phone        String?
  email        String?
  config       Json?
  departments  Department[]
  users        User[]
  createdAt    DateTime    @default(now())
  updatedAt    DateTime    @updatedAt
}

model Department {
  id          String   @id @default(cuid())
  instituteId String
  institute   Institute @relation(fields: [instituteId], references: [id])
  name        String
  code        String
  hodId       String?
  config      Json?
  staff       Staff[]
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
```

### User-Tenant Association

**Confirmed by Code**: Users are associated with tenants through foreign keys.

```prisma
model User {
  id           String   @id @default(cuid())
  universityId String
  university   University @relation(fields: [universityId], references: [id])
  instituteId  String?
  institute   Institute?  @relation(fields: [instituteId], references: [id])
  email        String   @unique
  role         UserRole
  scope        String?
  // ... other fields
}
```

### JWT Payload

**Confirmed by Code**: JWT payload includes tenant information.

```typescript
interface JwtPayload {
  sub: string;        // User ID
  email: string;
  role: UserRole;
  scope: string;
  universityId: string;
  instituteId?: string;
}
```

## Database Interactions

### Data Scoping

**Confirmed by Code**: Services scope data by tenant.

**Example**:
```typescript
// Wrong: Returns all users (security issue)
const users = await prisma.user.findMany();

// Correct: Returns users scoped to tenant
const users = await prisma.user.findMany({
  where: {
    universityId: user.universityId,
    instituteId: user.instituteId,
  },
});
```

### Tenant Filtering

**Confirmed by Code**: Services filter data based on user's tenant.

**Pattern**:
```typescript
@Injectable()
export class UniversityService {
  async findAll(query: QueryUniversityDto, user: JwtPayload) {
    // SUPERADMIN can see all universities
    if (user.role === 'SUPERADMIN') {
      return this.prisma.university.findMany();
    }

    // Other users can only see their university
    return this.prisma.university.findMany({
      where: { id: user.universityId },
    });
  }
}
```

## Redis Interactions

### Tenant-Specific Caching

**Confirmed by Code**: Cache keys include tenant information.

**Pattern**:
```typescript
const cacheKey = `university:${user.universityId}:${universityId}`;
const cached = await this.redis.get(cacheKey);
```

## Queue Interactions

### Tenant-Specific Jobs

**Confirmed by Code**: Jobs include tenant context.

**Pattern**:
```typescript
await this.notificationQueue.add('email', {
  to: user.email,
  universityId: user.universityId,
  instituteId: user.instituteId,
  subject: 'Notification',
  body: 'Message',
});
```

## Worker Interactions

### Tenant Context in Workers

**Confirmed by Code**: Workers process jobs with tenant context.

**Pattern**:
```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { universityId, instituteId, to, subject, body } = job.data;
    // Process email with tenant context
  }
}
```

## Business Rules

### Data Scoping Rules

**Confirmed by Code**: The system follows these data scoping rules:

1. **University-Level Data**: Scoped to universityId
2. **Institute-Level Data**: Scoped to instituteId
3. **Department-Level Data**: Scoped to departmentId
4. **User Data**: Scoped to user's universityId and instituteId
5. **SUPERADMIN**: Can access all data
6. **Other Roles**: Can only access their tenant data

### Access Control Rules

**Confirmed by Code**: The system follows these access control rules:

1. **SUPERADMIN**: Can access all universities, institutes, departments
2. **UNIVERSITY_ADMIN**: Can access their university and all institutes
3. **INSTITUTE_ADMIN**: Can access their institute and all departments
4. **DEPARTMENT_ADMIN**: Can access their department only
5. **STAFF**: Can access their department data
6. **STUDENT**: Can access their own data

### Configuration Rules

**Confirmed by Code**: Configuration is hierarchical:

1. **University Config**: Applies to entire university
2. **Institute Config**: Overrides university config for institute
3. **Department Config**: Overrides institute config for department

## Security

### Data Isolation

**Confirmed by Code**: Data is isolated at the database level.

**Mechanism**:
- Foreign key constraints enforce relationships
- WHERE clauses filter by tenant
- Scope guards enforce access control

### Cross-Tenant Access Prevention

**Confirmed by Code**: Cross-tenant access is prevented by:

1. **Database Queries**: Always filter by tenant
2. **API Guards**: Scope guards enforce tenant access
3. **JWT Validation**: JWT includes tenant information
4. **Audit Logging**: All access is logged

## Performance Considerations

### Query Performance

**Confirmed by Code**: Tenant filtering affects query performance.

**Optimizations**:
- Indexes on universityId and instituteId
- Partitioning by universityId (future enhancement)
- Query optimization for tenant filtering

### Caching Strategy

**Confirmed by Code**: Caching is tenant-specific.

**Strategy**:
- Cache keys include tenant information
- Cache invalidation is tenant-specific
- No cross-tenant cache pollution

## Common Mistakes

### Mistake 1: Not Filtering by Tenant

**Symptom**: Users see data from other tenants

**Cause**: Not filtering queries by tenant

**Fix**:
```typescript
// Wrong
const data = await prisma.model.findMany();

// Correct
const data = await prisma.model.findMany({
  where: {
    universityId: user.universityId,
    instituteId: user.instituteId,
  },
});
```

### Mistake 2: Hardcoding Tenant ID

**Symptom**: Code not working for other tenants

**Cause**: Hardcoding tenant ID instead of using user's tenant

**Fix**:
```typescript
// Wrong
const universityId = 'university-123';

// Correct
const universityId = user.universityId;
```

### Mistake 3: Not Checking Tenant Access

**Symptom**: Unauthorized access to tenant data

**Cause**: Not checking user's tenant access

**Fix**:
```typescript
// Check if user has access to tenant
if (user.universityId !== targetUniversityId && user.role !== 'SUPERADMIN') {
  throw new ForbiddenException('Access denied');
}
```

## Debugging Guide

### Tenant-Related Debugging

**Issue**: User sees data from wrong tenant

**Investigation**:
1. Check JWT payload
2. Check database query
3. Check scope guard
4. Check service logic

**Tools**:
- JWT decoder
- Database query logs
- Service logs

## Future Enhancements

### Row-Level Security

**Status**: Not implemented

**Proposal**: Implement row-level security in PostgreSQL:
- Database-level tenant filtering
- Automatic data isolation
- Better performance

### Tenant Isolation

**Status**: Not implemented

**Proposal**: Implement tenant isolation:
- Separate database per tenant
- Separate schema per tenant
- Better data isolation
- Better performance

## Production Considerations

### Tenant Onboarding

**Process**:
1. Create University record
2. Create Institute records
3. Create Department records
4. Create admin users
5. Configure tenant settings
6. Seed tenant data

### Tenant Migration

**Process**:
1. Export tenant data
2. Import to new system
3. Verify data integrity
4. Update tenant configuration
5. Test tenant access
6. Notify tenant users

## Example Requests

### Get Universities

**Request**:
```bash
GET /api/master-data/universities
Authorization: Bearer <token>
```

**Response** (SUPERADMIN):
```json
{
  "success": true,
  "data": [
    { "id": "uni-1", "name": "University A" },
    { "id": "uni-2", "name": "University B" }
  ]
}
```

**Response** (Other Role):
```json
{
  "success": true,
  "data": [
    { "id": "uni-1", "name": "University A" }
  ]
}
```

## Example Responses

### Tenant-Scoped Data

**Request**:
```bash
GET /api/students
Authorization: Bearer <token>
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "student-1",
      "name": "John Doe",
      "universityId": "uni-1",
      "instituteId": "inst-1"
    }
  ],
  "meta": {
    "universityId": "uni-1",
    "instituteId": "inst-1"
  }
}
```

## Sequence Diagrams

### Tenant Data Access Flow

```
User → JWT (with tenant info)
    ↓
Scope Guard (validates tenant access)
    ↓
Service (filters by tenant)
    ↓
Prisma (queries with WHERE clause)
    ↓
PostgreSQL (returns tenant data)
    ↓
Response (tenant-scoped data)
```

## Architecture Diagrams

### Multi-Tenancy Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  University ERP System                    │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  University A   │  │  University B   │  │  University C   │
└────────────────┘  └────────────────┘  └────────────────┘
         │                     │                     │
    ┌────┴────┐           ┌────┴────┐           ┌────┴────┐
    ↓         ↓           ↓         ↓           ↓         ↓
┌──────┐ ┌──────┐     ┌──────┐ ┌──────┐     ┌──────┐ ┌──────┐
│Inst 1│ │Inst 2│     │Inst 1│ │Inst 2│     │Inst 1│ │Inst 2│
└──────┘ └──────┘     └──────┘ └──────┘     └──────┘ └──────┘
```

## Common Interview Questions

### Q1: How does the multi-tenancy model work?

**Answer**: The system uses a hierarchical multi-tenancy model:
- University is the top-level tenant
- Institute belongs to University
- Department belongs to Institute
- All data is scoped to user's tenant
- Access control is enforced via scope guards

### Q2: How do you ensure data isolation between tenants?

**Answer**: Data isolation is ensured via:
- Database queries filter by tenant (universityId, instituteId)
- Scope guards enforce tenant access
- JWT payload includes tenant information
- Audit logging tracks all access

### Q3: How do you handle tenant-specific configurations?

**Answer**: Tenant-specific configurations are handled via:
- University-level config in University table
- Institute-level config in Institute table
- Department-level config in Department table
- Hierarchical override (department > institute > university)

## Exercises

### Exercise 1: Implement Tenant Scoping

**Task**: Implement tenant scoping for a new service.

**Steps**:
1. Create service
2. Add tenant filtering to queries
3. Add scope guard
4. Test with different tenant users

**Verification**:
- Users only see their tenant data
- SUPERADMIN sees all data
- Access control works correctly

### Exercise 2: Add Tenant Configuration

**Task**: Add tenant-specific configuration.

**Steps**:
1. Add config field to table
2. Implement config retrieval
3. Implement config override logic
4. Test configuration hierarchy

**Verification**:
- University config applies
- Institute config overrides university
- Department config overrides institute

## Real Production Scenarios

### Scenario 1: Adding New University

**Situation**: Need to onboard a new university

**Steps**:
1. Create University record
2. Create Institute records
3. Create Department records
4. Create admin users
5. Configure university settings
6. Seed initial data
7. Verify access control

### Scenario 2: Tenant Data Migration

**Situation**: Need to migrate tenant data to new system

**Steps**:
1. Export tenant data from old system
2. Transform data to new schema
3. Import to new system
4. Verify data integrity
5. Update tenant configuration
6. Test tenant access
7. Notify tenant users

## Navigation

**Next Section**: [05-Design-Patterns](./05-Design-Patterns.md)

**Previous Section**: [03-Technology-Stack](./03-Technology-Stack.md)

**Related Documentation**:
- [06-Authentication](../06-Authentication/README.md) - Authentication details
- [07-Authorization](../07-Authorization/README.md) - Authorization details
- [05-Database](../05-Database/README.md) - Database details
