# Master Data Module

## Purpose

This document explains the Master Data module of the University ERP system. It details the management of universities, institutes, departments, and other master data entities.

## Why This Document Exists

**Confirmed by Code**: The Master Data module manages core organizational data. Understanding this module is critical for:
- Managing universities, institutes, departments
- Setting up organizational hierarchy
- Managing master data configurations
- Implementing multi-tenancy
- Debugging master data issues

Without understanding the Master Data module, developers may struggle with organizational setup or may introduce data inconsistencies.

## Where This Is Used

- **Onboarding**: New developers learn master data module
- **Feature Development**: Implementing master data features
- **Code Reviews**: Reviewing master data code
- **Multi-Tenancy**: Managing multi-tenancy
- **Organization Setup**: Setting up organizations

## Dependencies

### Master Data Module Dependencies

**Confirmed by Code**: Master data module depends on:

- **PrismaModule**: Master data storage
- **AuthModule**: Authentication and authorization
- **GlobalJwtAuthGuard**: Route protection
- **ScopeGuard**: Scope-based access control

## Internal Architecture

### Master Data Module Architecture

**Confirmed by Code**: Master data module follows standard NestJS architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Master Data Module                           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Controllers  │  │  Services       │  │  DTOs          │
│  (Routes)     │  │  (Logic)        │  │  (Validation)   │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### University Controller

**Confirmed by Code**: University controller manages universities.

**UniversityController**:
```typescript
@Controller('universities')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UniversityController {
  constructor(private universityService: UniversityService) {}

  @Get()
  @Scope('master-data')
  findAll() {
    return this.universityService.findAll();
  }

  @Get(':id')
  @Scope('master-data')
  findOne(@Param('id') id: string) {
    return this.universityService.findOne(id);
  }

  @Post()
  @Scope('master-data')
  create(@Body() dto: CreateUniversityDto) {
    return this.universityService.create(dto);
  }

  @Patch(':id')
  @Scope('master-data')
  update(@Param('id') id: string, @Body() dto: UpdateUniversityDto) {
    return this.universityService.update(id, dto);
  }

  @Delete(':id')
  @Scope('master-data')
  remove(@Param('id') id: string) {
    return this.universityService.remove(id);
  }
}
```

**What This Does**:
- **findAll**: Get all universities
- **findOne**: Get university by ID
- **create**: Create new university
- **update**: Update university
- **remove**: Delete university

### Institute Controller

**Confirmed by Code**: Institute controller manages institutes.

**InstituteController**:
```typescript
@Controller('institutes')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class InstituteController {
  constructor(private instituteService: InstituteService) {}

  @Get()
  @Scope('master-data')
  findAll(@Query('universityId') universityId?: string) {
    return this.instituteService.findAll(universityId);
  }

  @Get(':id')
  @Scope('master-data')
  findOne(@Param('id') id: string) {
    return this.instituteService.findOne(id);
  }

  @Post()
  @Scope('master-data')
  create(@Body() dto: CreateInstituteDto) {
    return this.instituteService.create(dto);
  }

  @Patch(':id')
  @Scope('master-data')
  update(@Param('id') id: string, @Body() dto: UpdateInstituteDto) {
    return this.instituteService.update(id, dto);
  }

  @Delete(':id')
  @Scope('master-data')
  remove(@Param('id') id: string) {
    return this.instituteService.remove(id);
  }
}
```

**What This Does**:
- **findAll**: Get all institutes (optionally filtered by university)
- **findOne**: Get institute by ID
- **create**: Create new institute
- **update**: Update institute
- **remove**: Delete institute

### Department Controller

**Confirmed by Code**: Department controller manages departments.

**DepartmentController**:
```typescript
@Controller('departments')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class DepartmentController {
  constructor(private departmentService: DepartmentService) {}

  @Get()
  @Scope('master-data')
  findAll(@Query('instituteId') instituteId?: string) {
    return this.departmentService.findAll(instituteId);
  }

  @Get(':id')
  @Scope('master-data')
  findOne(@Param('id') id: string) {
    return this.departmentService.findOne(id);
  }

  @Post()
  @Scope('master-data')
  create(@Body() dto: CreateDepartmentDto) {
    return this.departmentService.create(dto);
  }

  @Patch(':id')
  @Scope('master-data')
  update(@Param('id') id: string, @Body() dto: UpdateDepartmentDto) {
    return this.departmentService.update(id, dto);
  }

  @Delete(':id')
  @Scope('master-data')
  remove(@Param('id') id: string) {
    return this.departmentService.remove(id);
  }
}
```

**What This Does**:
- **findAll**: Get all departments (optionally filtered by institute)
- **findOne**: Get department by ID
- **create**: Create new department
- **update**: Update department
- **remove**: Delete department

## Database Interactions

### Master Data-Database Flow

**Confirmed by Code**: Master data module interacts with database.

**Flow**:
```
Master Data Service → Prisma → University/Institute/Department Tables
```

## Redis Interactions

### Master Data-Redis Flow

**Confirmed by Code**: Master data can be cached in Redis.

**Flow**:
```
Master Data Service → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Master Data-Queue Flow

**Confirmed by Code**: Master data doesn't interact with queues.

**Flow**:
```
Master Data → No queue interaction
```

## Worker Interactions

### Master Data-Worker Flow

**Confirmed by Code**: Workers don't use master data module.

**Flow**:
```
Worker → No master data interaction
```

## Business Rules

### Master Data Rules

**Confirmed by Code**: Master data follows these rules:

1. **Hierarchy**: University → Institute → Department
2. **Uniqueness**: University names must be unique
3. **Relationships**: Institutes belong to universities
4. **Relationships**: Departments belong to institutes
5. **Scoping**: Data scoped by user role

### Validation Rules

**Confirmed by Code**: Validation follows these rules:

1. **Required Fields**: Name is required
2. **Unique Names**: Names must be unique within parent
3. **Parent Exists**: Parent must exist
4. **Active Status**: Active/inactive status
5. **Code Format**: Code must follow format

## Security

### Master Data Security

**Confirmed by Code**: Security considerations for master data:

1. **Scope Enforcement**: Enforce master-data scope
2. **Data Scoping**: Scope data by tenant hierarchy
3. **Audit Logging**: Log all master data changes
4. **Access Control**: Restrict access to authorized users
5. **Validation**: Validate all inputs

## Performance Considerations

### Master Data Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Cache master data in Redis
2. **Indexing**: Index foreign keys
3. **Query Optimization**: Optimize queries
4. **Lazy Loading**: Lazy load related data
5. **Pagination**: Paginate large datasets

## Common Mistakes

### Mistake 1: Not Checking Parent Existence

**Symptom**: Invalid parent reference

**Cause**: Not checking parent existence

**Fix**:
```typescript
// Check parent existence
const university = await this.prisma.university.findUnique({
  where: { id: dto.universityId },
});

if (!university) {
  throw new NotFoundException('University not found');
}
```

### Mistake 2: Not Implementing Data Scoping

**Symptom**: Users can access data they shouldn't

**Cause**: Not implementing data scoping

**Fix**:
```typescript
// Add data scoping
const where = this.buildWhereClause(user);
return this.prisma.university.findMany({ where });
```

### Mistake 3: Not Caching Master Data

**Symptom**: Slow master data queries

**Cause**: Not caching master data

**Fix**:
```typescript
// Add caching
const cached = await this.redis.get(cacheKey);
if (cached) return JSON.parse(cached);

const data = await this.prisma.university.findMany();
await this.redis.setex(cacheKey, 3600, JSON.stringify(data));
return data;
```

## Debugging Guide

### Master Data Debugging

**Issue**: Master data not loading

**Investigation**:
1. Check database connection
2. Check query logic
3. Check data scoping
4. Check cache
5. Check logs

**Tools**:
- Prisma logs
- Database logs
- Redis logs
- Service logs

## Future Enhancements

### Master Data Versioning

**Status**: Not implemented

**Proposal**: Implement master data versioning:
- Track changes to master data
- Version history
- Rollback capability
- Better audit trail
- More complex

### Master Data Import/Export

**Status**: Not implemented

**Proposal**: Implement import/export:
- Bulk import master data
- Bulk export master data
- Excel/CSV support
- Validation
- Better UX

## Production Considerations

### Production Master Data

**Production Deployment**:
- Enable caching
- Implement data scoping
- Monitor master data changes
- Monitor access patterns
- Audit all changes

### Master Data Monitoring

**Monitoring Metrics**:
- Master data access rate
- Master data change rate
- Cache hit rate
- Query performance
- Access patterns

## Example Requests

### Master Data Example

**Request**: Get universities

```bash
GET /api/universities
Authorization: Bearer <token>
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "uni-id",
      "name": "University of Technology",
      "code": "UT"
    }
  ]
}
```

## Example Responses

### Master Data Response

**Response**: Master data retrieved

```json
{
  "success": true,
  "data": {
    "id": "uni-id",
    "name": "University of Technology",
    "code": "UT",
    "institutes": [...]
  }
}
```

## Sequence Diagrams

### Master Data Flow

```
Request → Guard → Service → Database → Response
```

## Architecture Diagrams

### Master Data Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Master Data Controller                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Master Data Service                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Prisma                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database                                   │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is the organizational hierarchy structured?

**Answer**: Hierarchy via:
- University (top level)
- Institute (belongs to university)
- Department (belongs to institute)
- Foreign key relationships
- Multi-tenancy support

### Q2: How do you implement data scoping for master data?

**Answer**: Data scoping via:
- Filter by user role
- SUPERADMIN: No filtering
- UNIVERSITY_ADMIN: Filter by universityId
- INSTITUTE_ADMIN: Filter by universityId and instituteId
- DEPARTMENT_ADMIN: Filter by universityId, instituteId, and departmentId

### Q3: How do you cache master data?

**Answer**: Caching via:
- Redis cache
- Cache key based on query
- TTL-based expiration
- Cache invalidation on update
- Cache-aside pattern

## Exercises

### Exercise 1: Add a New Master Data Entity

**Task**: Add a new master data entity.

**Steps**:
1. Add model to Prisma schema
2. Generate migration
3. Create controller
4. Create service
5. Test CRUD operations

**Verification**:
- Model added
- Migration applied
- Controller works
- Service works
- Tests pass

### Exercise 2: Add Caching to Master Data

**Task**: Add caching to master data queries.

**Steps**:
1. Inject RedisService
2. Add cache check
3. Add cache set
4. Add cache invalidation
5. Test caching

**Verification**:
- Caching implemented
- Cache hit works
- Cache miss works
- Cache invalidation works
- Tests pass

## Real Production Scenarios

### Scenario 1: Master Data Not Loading

**Situation**: Master data not loading

**Response**:
1. Check database connection
2. Check query logic
3. Check data scoping
4. Fix query
5. Test query

### Scenario 2: Cache Invalidation Issue

**Situation**: Stale data in cache

**Response**:
1. Check cache invalidation logic
2. Fix invalidation
3. Clear cache
4. Test cache
5. Monitor cache

## Navigation

**Next Section**: [03-Admissions-Module](./03-Admissions-Module.md)

**Previous Section**: [01-Auth-Module](./01-Auth-Module.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [05-Database](../05-Database/README.md) - Database details
