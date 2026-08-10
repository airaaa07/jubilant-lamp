# Academic Module

## Purpose

This document explains the Academic module of the University ERP system. It details courses, batches, sections, subjects, and academic program management.

## Why This Document Exists

**Confirmed by Code**: The Academic module manages academic programs. Understanding this module is critical for:
- Managing courses and programs
- Managing batches and sections
- Managing subjects and enrollments
- Implementing academic workflows
- Debugging academic issues

Without understanding the Academic module, developers may struggle with academic features or may introduce bugs.

## Where This Is Used

- **Onboarding**: New developers learn academic module
- **Feature Development**: Implementing academic features
- **Code Reviews**: Reviewing academic code
- **Academic Management**: Managing academic programs
- **Enrollment**: Managing student enrollments

## Dependencies

### Academic Module Dependencies

**Confirmed by Code**: Academic module depends on:

- **PrismaModule**: Academic data storage
- **AuthModule**: Authentication and authorization
- **MasterDataModule**: Department data
- **AdmissionsModule**: Student data
- **WorkflowModule**: Academic workflows

## Internal Architecture

### Academic Module Architecture

**Confirmed by Code**: Academic module follows standard NestJS architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Academic Module                              │
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

### Course Controller

**Confirmed by Code**: Course controller manages courses.

**CourseController**:
```typescript
@Controller('courses')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class CourseController {
  constructor(private courseService: CourseService) {}

  @Get()
  @Scope('academic')
  findAll(@Query('universityId') universityId?: string) {
    return this.courseService.findAll(universityId);
  }

  @Get(':id')
  @Scope('academic')
  findOne(@Param('id') id: string) {
    return this.courseService.findOne(id);
  }

  @Post()
  @Scope('academic')
  create(@Body() dto: CreateCourseDto) {
    return this.courseService.create(dto);
  }

  @Patch(':id')
  @Scope('academic')
  update(@Param('id') id: string, @Body() dto: UpdateCourseDto) {
    return this.courseService.update(id, dto);
  }

  @Delete(':id')
  @Scope('academic')
  remove(@Param('id') id: string) {
    return this.courseService.remove(id);
  }
}
```

**What This Does**:
- **findAll**: Get all courses (optionally filtered by university)
- **findOne**: Get course by ID
- **create**: Create new course
- **update**: Update course
- **remove**: Delete course

### Batch Controller

**Confirmed by Code**: Batch controller manages batches.

**BatchController**:
```typescript
@Controller('batches')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class BatchController {
  constructor(private batchService: BatchService) {}

  @Get()
  @Scope('academic')
  findAll(@Query('courseId') courseId?: string) {
    return this.batchService.findAll(courseId);
  }

  @Get(':id')
  @Scope('academic')
  findOne(@Param('id') id: string) {
    return this.batchService.findOne(id);
  }

  @Post()
  @Scope('academic')
  create(@Body() dto: CreateBatchDto) {
    return this.batchService.create(dto);
  }

  @Patch(':id')
  @Scope('academic')
  update(@Param('id') id: string, @Body() dto: UpdateBatchDto) {
    return this.batchService.update(id, dto);
  }

  @Delete(':id')
  @Scope('academic')
  remove(@Param('id') id: string) {
    return this.batchService.remove(id);
  }
}
```

**What This Does**:
- **findAll**: Get all batches (optionally filtered by course)
- **findOne**: Get batch by ID
- **create**: Create new batch
- **update**: Update batch
- **remove**: Delete batch

### Subject Controller

**Confirmed by Code**: Subject controller manages subjects.

**SubjectController**:
```typescript
@Controller('subjects')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class SubjectController {
  constructor(private subjectService: SubjectService) {}

  @Get()
  @Scope('academic')
  findAll(@Query('courseId') courseId?: string) {
    return this.subjectService.findAll(courseId);
  }

  @Get(':id')
  @Scope('academic')
  findOne(@Param('id') id: string) {
    return this.subjectService.findOne(id);
  }

  @Post()
  @Scope('academic')
  create(@Body() dto: CreateSubjectDto) {
    return this.subjectService.create(dto);
  }

  @Patch(':id')
  @Scope('academic')
  update(@Param('id') id: string, @Body() dto: UpdateSubjectDto) {
    return this.subjectService.update(id, dto);
  }

  @Delete(':id')
  @Scope('academic')
  remove(@Param('id') id: string) {
    return this.subjectService.remove(id);
  }
}
```

**What This Does**:
- **findAll**: Get all subjects (optionally filtered by course)
- **findOne**: Get subject by ID
- **create**: Create new subject
- **update**: Update subject
- **remove**: Delete subject

## Database Interactions

### Academic-Database Flow

**Confirmed by Code**: Academic module interacts with database.

**Flow**:
```
Academic Service → Prisma → Course/Batch/Section/Subject Tables
```

## Redis Interactions

### Academic-Redis Flow

**Confirmed by Code**: Academic module can use Redis for caching.

**Flow**:
```
Academic Service → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Academic-Queue Flow

**Confirmed by Code**: Academic module doesn't directly interact with queues.

**Flow**:
```
Academic → No queue interaction
```

## Worker Interactions

### Academic-Worker Flow

**Confirmed by Code**: Workers don't use academic module.

**Flow**:
```
Worker → No academic interaction
```

## Business Rules

### Academic Rules

**Confirmed by Code**: Academic follows these rules:

1. **Course Structure**: Courses belong to universities and departments
2. **Batch Structure**: Batches belong to courses
3. **Section Structure**: Sections belong to batches
4. **Subject Structure**: Subjects belong to courses
5. **Enrollment**: Students enroll in subjects

### Validation Rules

**Confirmed by Code**: Validation follows these rules:

1. **Required Fields**: Name, code required
2. **Unique Codes**: Codes must be unique within university
3. **Parent Exists**: Parent must exist
4. **Credits**: Credits must be positive
5. **Capacity**: Capacity must be positive

## Security

### Academic Security

**Confirmed by Code**: Security considerations for academic:

1. **Scope Enforcement**: Enforce academic scope
2. **Data Scoping**: Scope data by tenant hierarchy
3. **Audit Logging**: Log all academic changes
4. **Access Control**: Restrict access to authorized users
5. **Validation**: Validate all inputs

## Performance Considerations

### Academic Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Cache academic data
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
const course = await this.prisma.course.findUnique({
  where: { id: dto.courseId },
});

if (!course) {
  throw new NotFoundException('Course not found');
}
```

### Mistake 2: Not Implementing Data Scoping

**Symptom**: Users can access data they shouldn't

**Cause**: Not implementing data scoping

**Fix**:
```typescript
// Add data scoping
const where = this.buildWhereClause(user);
return this.prisma.course.findMany({ where });
```

### Mistake 3: Not Caching Academic Data

**Symptom**: Slow academic data queries

**Cause**: Not caching academic data

**Fix**:
```typescript
// Add caching
const cached = await this.redis.get(cacheKey);
if (cached) return JSON.parse(cached);

const data = await this.prisma.course.findMany();
await this.redis.setex(cacheKey, 3600, JSON.stringify(data));
return data;
```

## Debugging Guide

### Academic Debugging

**Issue**: Academic data not loading

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

### Subject Pooling

**Status**: Not implemented

**Proposal**: Implement subject pooling:
- Students choose from subject pools
- Elective subjects
- Credit-based selection
- Better flexibility
- More complex

### Academic Calendar

**Status**: Not implemented

**Proposal**: Implement academic calendar:
- Academic year management
- Semester management
- Holiday management
- Better scheduling
- More complex

## Production Considerations

### Production Academic

**Production Deployment**:
- Enable caching
- Implement data scoping
- Monitor academic changes
- Monitor access patterns
- Audit all changes

### Academic Monitoring

**Monitoring Metrics**:
- Academic data access rate
- Academic data change rate
- Cache hit rate
- Query performance
- Access patterns

## Example Requests

### Academic Example

**Request**: Get courses

```bash
GET /api/courses
Authorization: Bearer <token>
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "course-id",
      "name": "Computer Science",
      "code": "CS",
      "credits": 120
    }
  ]
}
```

## Example Responses

### Academic Response

**Response**: Academic data retrieved

```json
{
  "success": true,
  "data": {
    "id": "course-id",
    "name": "Computer Science",
    "code": "CS",
    "credits": 120,
    "batches": [...]
  }
}
```

## Sequence Diagrams

### Academic Flow

```
Request → Guard → Service → Database → Response
```

## Architecture Diagrams

### Academic Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Academic Controller                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Academic Service                          │
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

### Q1: How is the academic structure organized?

**Answer**: Academic structure via:
- Course (top level)
- Batch (belongs to course)
- Section (belongs to batch)
- Subject (belongs to course)
- Foreign key relationships

### Q2: How do you implement data scoping for academic data?

**Answer**: Data scoping via:
- Filter by user role
- SUPERADMIN: No filtering
- UNIVERSITY_ADMIN: Filter by universityId
- INSTITUTE_ADMIN: Filter by universityId and instituteId
- DEPARTMENT_ADMIN: Filter by universityId, instituteId, and departmentId

### Q3: How do you handle subject enrollment?

**Answer**: Subject enrollment via:
- Students enroll in subjects
- Subject pools for electives
- Credit-based selection
- Enrollment validation
- Capacity limits

## Exercises

### Exercise 1: Add a New Academic Entity

**Task**: Add a new academic entity.

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

### Exercise 2: Add Caching to Academic Data

**Task**: Add caching to academic data queries.

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

### Scenario 1: Academic Data Not Loading

**Situation**: Academic data not loading

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

**Next Section**: [05-Attendance-Module](./05-Attendance-Module.md)

**Previous Section**: [03-Admissions-Module](./03-Admissions-Module.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [05-Database](../05-Database/README.md) - Database details
