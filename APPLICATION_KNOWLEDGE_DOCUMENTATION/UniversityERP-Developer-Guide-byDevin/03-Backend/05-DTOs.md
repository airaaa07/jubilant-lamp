# DTOs (Data Transfer Objects)

## Purpose

This document explains the DTO (Data Transfer Object) pattern used in the University ERP backend. It details how DTOs are used for validation, data transfer, and API contracts.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses DTOs for request/response validation. Understanding DTOs is critical for:
- Validating incoming requests
- Defining API contracts
- Type-safe data transfer
- Documenting API endpoints
- Preventing invalid data

Without understanding DTOs, developers may struggle with validation or API contract issues.

## Where This Is Used

- **Onboarding**: New developers learn DTO pattern
- **Feature Development**: Creating DTOs for endpoints
- **Code Reviews**: Reviewing DTO definitions
- **API Documentation**: Documenting API contracts
- **Validation**: Validating request data

## Dependencies

### DTO Dependencies

**Confirmed by Code**: DTOs depend on:

- **Zod**: Schema validation library
- **class-validator**: Validation decorators
- **class-transformer**: Data transformation
- **TypeScript**: Type definitions

## Internal Architecture

### DTO Architecture

**Confirmed by Code**: DTOs follow a standard pattern.

```
┌─────────────────────────────────────────────────────────┐
│                  DTO Structure                              │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Create DTO   │  │  Update DTO    │  │  Query DTO     │
│  (Input)      │  │  (Input)       │  │  (Input)       │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Response DTO │  │  List DTO      │  │  Pagination    │
│  (Output)     │  │  (Output)      │  │  DTO           │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### DTO Definition

**Confirmed by Code**: DTOs defined with Zod schemas.

**Create DTO**:
```typescript
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  role: z.enum(['STUDENT', 'STAFF', 'ADMIN']),
  universityId: z.string().cuid(),
  instituteId: z.string().cuid().optional(),
});

export type CreateUserDto = z.infer<typeof CreateUserSchema>;
```

**What This Does**:
- **z.object**: Defines object schema
- **z.string().email()**: Validates email format
- **z.string().min()**: Validates minimum length
- **z.enum()**: Validates enum values
- **z.cuid()**: Validates CUID format
- **z.infer**: Infers TypeScript type from schema

**Update DTO**:
```typescript
export const UpdateUserSchema = z.object({
  email: z.string().email('Invalid email format').optional(),
  name: z.string().min(2, 'Name must be at least 2 characters').optional(),
  role: z.enum(['STUDENT', 'STAFF', 'ADMIN']).optional(),
}).partial();

export type UpdateUserDto = z.infer<typeof UpdateUserSchema>;
```

**What This Does**:
- **.optional()**: Makes field optional
- **.partial()**: Makes all fields optional

**Query DTO**:
```typescript
export const QueryUserSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(10),
  search: z.string().optional(),
  role: z.enum(['STUDENT', 'STAFF', 'ADMIN']).optional(),
});

export type QueryUserDto = z.infer<typeof QueryUserSchema>;
```

**What This Does**:
- **z.coerce.number()**: Coerces string to number
- **.int()**: Validates integer
- **.positive()**: Validates positive number
- **.max()**: Validates maximum value
- **.default()**: Sets default value

### DTO Validation

**Confirmed by Code**: DTOs validated with ZodValidationPipe.

**ZodValidationPipe**:
```typescript
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';
import { ZodSchema } from 'zod';

@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodSchema) {}

  transform(value: any) {
    try {
      return this.schema.parse(value);
    } catch (error) {
      throw new BadRequestException('Validation failed');
    }
  }
}
```

**Usage in Controller**:
```typescript
@Post()
@UsePipes(new ZodValidationPipe(CreateUserSchema))
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

**What This Does**:
- Validates request body against schema
- Throws BadRequestException if validation fails
- Returns validated data

### DTO Nesting

**Confirmed by Code**: DTOs can be nested for complex structures.

**Nested DTO**:
```typescript
export const CreateUserWithProfileSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  profile: z.object({
    firstName: z.string(),
    lastName: z.string(),
    dateOfBirth: z.coerce.date(),
  }),
});

export type CreateUserWithProfileDto = z.infer<typeof CreateUserWithProfileSchema>;
```

**What This Does**:
- Defines nested object structure
- Validates nested data
- Type-safe nested access

### DTO Arrays

**Confirmed by Code**: DTOs can define array structures.

**Array DTO**:
```typescript
export const CreateUsersSchema = z.object({
  users: z.array(CreateUserSchema),
});

export type CreateUsersDto = z.infer<typeof CreateUsersSchema>;
```

**What This Does**:
- Defines array of objects
- Validates array of DTOs
- Type-safe array access

## Database Interactions

### DTO-Database Mapping

**Confirmed by Code**: DTOs map to database models.

**Mapping**:
```typescript
// DTO
export const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string(),
});

// Service
async create(dto: CreateUserDto) {
  const hashedPassword = await bcrypt.hash(dto.password, 10);
  
  return this.prisma.user.create({
    data: {
      email: dto.email,
      passwordHash: hashedPassword,
      name: dto.name,
    },
  });
}
```

**What This Does**:
- Maps DTO fields to database fields
- Transforms data (e.g., password hashing)
- Creates database record

## Redis Interactions

### DTO-Cache Mapping

**Confirmed by Code**: DTOs used for cache serialization.

**Serialization**:
```typescript
async getUniversity(id: string) {
  const cacheKey = `university:${id}`;
  const cached = await this.redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const university = await this.prisma.university.findUnique({
    where: { id },
  });
  
  await this.redis.setex(cacheKey, 300, JSON.stringify(university));
  
  return university;
}
```

**What This Does**:
- Serializes DTO to JSON for cache
- Deserializes JSON from cache
- Type-safe cache access

## Queue Interactions

### DTO-Queue Mapping

**Confirmed by Code**: DTOs used for job data.

**Job Data**:
```typescript
// DTO
export const SendEmailSchema = z.object({
  to: z.string().email(),
  subject: z.string(),
  body: z.string(),
});

// Service
async sendEmail(dto: SendEmailDto) {
  await this.notificationQueue.add('email', dto);
}
```

**What This Does**:
- Validates DTO before queue
- Serializes DTO for queue
- Type-safe queue data

## Worker Interactions

### DTO-Worker Mapping

**Confirmed by Code**: Workers receive DTO data.

**Job Processing**:
```typescript
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    const { to, subject, body } = job.data;
    await this.mailService.sendEmail({ to, subject, body });
  }
}
```

**What This Does**:
- Deserializes DTO from job
- Type-safe job data access
- Processes job data

## Business Rules

### DTO Rules

**Confirmed by Code**: DTOs follow these rules:

1. **Validation**: All inputs validated
2. **Type Safety**: All DTOs typed
3. **Documentation**: DTOs document API contracts
4. **Consistency**: Consistent naming conventions
5. **Separation**: Separate DTOs for create, update, query

### Validation Rules

**Confirmed by Code**: Validation follows these rules:

1. **Required Fields**: Mark required fields
2. **Optional Fields**: Mark optional fields
3. **Type Validation**: Validate field types
4. **Format Validation**: Validate field formats
5. **Business Validation**: Validate business rules

## Security

### DTO Security

**Confirmed by Code**: Security considerations for DTOs:

1. **Input Validation**: Validate all inputs
2. **Output Sanitization**: Sanitize outputs
3. **Sensitive Data**: Don't include sensitive data in DTOs
4. **Password Fields**: Never return password fields
5. **PII**: Protect personally identifiable information

## Performance Considerations

### DTO Performance

**Confirmed by Code**: Performance considerations for DTOs:

1. **Validation Speed**: Keep validation fast
2. **Schema Size**: Keep schemas focused
3. **Nesting Depth**: Limit nesting depth
4. **Array Size**: Limit array sizes
5. **Coercion**: Use coercion for type conversion

## Common Mistakes

### Mistake 1: Not Validating Input

**Symptom**: Invalid data in database

**Cause**: Not validating input with DTO

**Fix**:
```typescript
// Add validation
export const CreateUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});
```

### Mistake 2: Not Using Coercion

**Symptom**: Type errors in validation

**Cause**: Not coercing string to number

**Fix**:
```typescript
// Add coercion
export const QueryUserSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(10),
});
```

### Mistake 3: Too Much Validation

**Symptom**: Validation slow

**Cause**: Too much validation logic

**Fix**:
```typescript
// Keep validation focused
// Move complex validation to service
export const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2),
});
```

## Debugging Guide

### DTO Debugging

**Issue**: Validation failing

**Investigation**:
1. Check DTO schema
2. Check validation rules
3. Check input data
4. Check error messages
5. Test with valid data

**Tools**:
- Zod validation
- Controller logs
- Request inspection
- Postman testing

## Future Enhancements

### Auto-Generated DTOs

**Status**: Not implemented

**Proposal**: Auto-generate DTOs from Prisma:
- Generate DTOs from Prisma schema
- Auto-update on schema changes
- Type-safe DTOs
- Less manual work

### OpenAPI Integration

**Status**: Not implemented

**Proposal**: Integrate with OpenAPI:
- Auto-generate OpenAPI spec from DTOs
- Document API contracts
- Generate client SDKs
- Better API documentation

## Production Considerations

### Production DTOs

**Production Deployment**:
- Keep validation strict
- Monitor validation errors
- Update DTOs carefully
- Version DTOs for breaking changes
- Document DTO changes

### DTO Monitoring

**Monitoring Metrics**:
- Validation error rate
- Validation time
- DTO usage statistics
- Breaking change detection

## Example Requests

### DTO Validation Example

**Request**:
```bash
POST /api/users
Content-Type: application/json

{
  "email": "invalid-email",
  "password": "short"
}
```

**Response**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  }
}
```

## Example Responses

### Valid DTO Example

**Request**:
```bash
POST /api/users
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

## Sequence Diagrams

### DTO Validation Flow

```
Request → DTO Validation → Controller → Service → Database
            ↓
        Valid?
            ↓
        Yes → Continue
            ↓
        No → Error Response
```

## Architecture Diagrams

### DTO Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Validation Pipe                           │
│                  (DTO Validation)                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
│                  (Valid Data)                              │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the purpose of DTOs?

**Answer**: DTO purpose:
- Validate incoming requests
- Define API contracts
- Type-safe data transfer
- Document API endpoints
- Prevent invalid data

### Q2: How do you validate DTOs in NestJS?

**Answer**: DTO validation via:
- Zod schemas for validation
- Validation pipes to apply validation
- Custom validation logic
- Type-safe validation
- Error handling

### Q3: How do you handle nested DTOs?

**Answer**: Nested DTOs via:
- Zod object nesting
- Nested validation
- Type-safe nested access
- Recursive validation
- Complex structure support

## Exercises

### Exercise 1: Create a DTO

**Task**: Create a new DTO.

**Steps**:
1. Define Zod schema
2. Infer TypeScript type
3. Add validation rules
4. Test validation
5. Use in controller

**Verification**:
- DTO created
- Validation works
- Type-safe
- Used correctly

### Exercise 2: Add Complex Validation

**Task**: Add complex validation to DTO.

**Steps**:
1. Add custom validation
2. Add conditional validation
3. Add array validation
4. Test validation
5. Handle errors

**Verification**:
- Complex validation works
- Errors handled correctly
- Validation fast enough

## Real Production Scenarios

### Scenario 1: Validation Error

**Situation**: DTO validation failing

**Response**:
1. Check DTO schema
2. Check validation rules
3. Check input data
4. Fix validation
5. Test validation

### Scenario 2: Breaking Change

**Situation**: DTO change breaks API

**Response**:
1. Identify breaking change
2. Version DTO
3. Update documentation
4. Communicate change
5. Monitor impact

## Navigation

**Next Section**: [06-Guards](./06-Guards.md)

**Previous Section**: [04-Services](./04-Services.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [03-Controllers](./03-Controllers.md) - Controllers
- [12-API-Reference](../01-System-Architecture/12-API-Reference.md) - API reference
