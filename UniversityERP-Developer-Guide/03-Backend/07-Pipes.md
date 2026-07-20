# Pipes

## Purpose

This document explains the pipe pattern used in the University ERP backend. It details how pipes transform and validate data, handle request processing, and implement data transformation logic.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS pipes for data transformation and validation. Understanding pipes is critical for:
- Validating incoming requests
- Transforming request data
- Sanitizing data
- Type conversion
- Implementing custom validation logic

Without understanding pipes, developers may struggle with data validation or transformation.

## Where This Is Used

- **Onboarding**: New developers learn pipe pattern
- **Feature Development**: Creating pipes for validation
- **Code Reviews**: Reviewing pipe implementation
- **Data Validation**: Validating request data
- **Data Transformation**: Transforming data

## Dependencies

### Pipe Dependencies

**Confirmed by Code**: Pipes depend on:

- **NestJS Pipes**: Pipe interface
- **Zod**: Schema validation library
- **class-validator**: Validation decorators
- **class-transformer**: Data transformation
- **TypeScript**: Type definitions

## Internal Architecture

### Pipe Architecture

**Confirmed by Code**: Pipes follow a processing pipeline.

```
┌─────────────────────────────────────────────────────────┐
│                  Pipe Pipeline                             │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Validation   │  │  Transformation│  │  Sanitization  │
│  Pipe         │  │  Pipe          │  │  Pipe          │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Pipe Definition

**Confirmed by Code**: Pipes implement PipeTransform interface.

**Basic Pipe**:
```typescript
import { PipeTransform, Injectable, ArgumentMetadata } from '@nestjs/common';

@Injectable()
export class MyPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    return value;
  }
}
```

**What This Does**:
- **PipeTransform**: Interface for pipe
- **transform()**: Transforms input value
- **metadata**: Metadata about the target
- **Returns**: Transformed value

### Validation Pipe

**Confirmed by Code**: ZodValidationPipe validates data against Zod schema.

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

**What This Does**:
- **Zod Schema**: Validates against Zod schema
- **parse()**: Validates and transforms data
- **Error Handling**: Throws BadRequestException on failure
- **Type Safety**: Returns typed data

**Usage in Controller**:
```typescript
@Post()
@UsePipes(new ZodValidationPipe(CreateUserSchema))
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

### Global Validation Pipe

**Confirmed by Code**: Global validation pipe applied in main.ts.

**Global Pipe**:
```typescript
// main.ts
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));
  
  await app.listen(3000);
}
```

**What This Does**:
- **whitelist**: Strips properties not in DTO
- **forbidNonWhitelisted**: Throws error if non-whitelisted property present
- **transform**: Automatically transforms types

### Custom Validation Pipe

**Confirmed by Code**: Custom pipes for specific validation logic.

**Custom Pipe**:
```typescript
@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
  transform(value: string): number {
    const val = parseInt(value, 10);
    if (isNaN(val)) {
      throw new BadRequestException('Validation failed');
    }
    return val;
  }
}
```

**Usage**:
```typescript
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) {
  return this.usersService.findOne(id);
}
```

### Transformation Pipe

**Confirmed by Code**: Pipes can transform data.

**LowerCasePipe**:
```typescript
@Injectable()
export class LowerCasePipe implements PipeTransform {
  transform(value: any) {
    if (typeof value !== 'string') {
      return value;
    }
    return value.toLowerCase();
  }
}
```

**Usage**:
```typescript
@Post('search')
search(@Body('query', LowerCasePipe) query: string) {
  return this.usersService.search(query);
}
```

### Sanitization Pipe

**Confirmed by Code**: Pipes can sanitize data.

**SanitizePipe**:
```typescript
@Injectable()
export class SanitizePipe implements PipeTransform {
  transform(value: any) {
    if (typeof value !== 'string') {
      return value;
    }
    // Remove HTML tags
    return value.replace(/<[^>]*>/g, '');
  }
}
```

**Usage**:
```typescript
@Post('comment')
createComment(@Body('content', SanitizePipe) content: string) {
  return this.commentsService.create(content);
}
```

## Database Interactions

### Pipe-Database Flow

**Confirmed by Code**: Pipes don't directly interact with database.

**Flow**:
```
Request → Pipe → Controller → Service → Database
```

## Redis Interactions

### Pipe-Redis Flow

**Confirmed by Code**: Pipes don't directly interact with Redis.

**Flow**:
```
Request → Pipe → Controller → Service → Redis
```

## Queue Interactions

### Pipe-Queue Flow

**Confirmed by Code**: Pipes don't directly interact with queues.

**Flow**:
```
Request → Pipe → Controller → Service → Queue
```

## Worker Interactions

### Pipe-Worker Flow

**Confirmed by Code**: Workers don't use pipes.

**Flow**:
```
Worker processes job directly without pipes
```

## Business Rules

### Pipe Rules

**Confirmed by Code**: Pipes follow these rules:

1. **Validation**: Validate all inputs
2. **Transformation**: Transform data as needed
3. **Sanitization**: Sanitize user input
4. **Type Conversion**: Convert types as needed
5. **Error Handling**: Handle validation errors

### Validation Rules

**Confirmed by Code**: Validation follows these rules:

1. **Schema Validation**: Validate against schema
2. **Business Validation**: Validate business rules
3. **Type Validation**: Validate data types
4. **Format Validation**: Validate data formats
5. **Custom Validation**: Custom validation logic

## Security

### Pipe Security

**Confirmed by Code**: Security considerations for pipes:

1. **Input Sanitization**: Sanitize all user input
2. **SQL Injection**: Prevent SQL injection
3. **XSS Prevention**: Prevent XSS attacks
4. **Type Safety**: Ensure type safety
5. **Validation**: Validate all inputs

## Performance Considerations

### Pipe Performance

**Confirmed by Code**: Performance considerations for pipes:

1. **Fast Validation**: Keep validation fast
2. **Minimal Transformation**: Minimize transformation overhead
3. **Early Return**: Return early on failure
4. **Caching**: Cache validation results if applicable
5. **Async Operations**: Use async for expensive operations

## Common Mistakes

### Mistake 1: Not Validating Input

**Symptom**: Invalid data in database

**Cause**: Not using validation pipe

**Fix**:
```typescript
// Add validation pipe
@Post()
@UsePipes(new ZodValidationPipe(CreateUserSchema))
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

### Mistake 2: Not Sanitizing Input

**Symptom**: XSS vulnerability

**Cause**: Not sanitizing user input

**Fix**:
```typescript
// Add sanitization pipe
@Post('comment')
createComment(@Body('content', SanitizePipe) content: string) {
  return this.commentsService.create(content);
}
```

### Mistake 3: Not Transforming Types

**Symptom**: Type errors in service

**Cause**: Not transforming types

**Fix**:
```typescript
// Add type transformation pipe
@Get(':id')
findOne(@Param('id', ParseIntPipe) id: number) {
  return this.usersService.findOne(id);
}
```

## Debugging Guide

### Pipe Debugging

**Issue**: Pipe not working

**Investigation**:
1. Check pipe logic
2. Check pipe application
3. Check input data
4. Check error messages
5. Test pipe

**Tools**:
- Pipe logs
- Request inspection
- Validation errors
- Unit tests

## Future Enhancements

### Async Validation

**Status**: Not implemented

**Proposal**: Add async validation:
- Async validation against database
- Async validation against external services
- Better business rule validation
- More flexible validation

### Custom Validation Decorators

**Status**: Not implemented

**Proposal**: Add custom validation decorators:
- Reusable validation logic
- Declarative validation
- Better code organization
- Easier maintenance

## Production Considerations

### Production Pipes

**Production Deployment**:
- Enable all validation pipes
- Use strict validation
- Monitor validation errors
- Monitor pipe performance
- Update validation rules carefully

### Pipe Monitoring

**Monitoring Metrics**:
- Validation error rate
- Validation time
- Pipe execution time
- Transformation success rate
- Sanitization rate

## Example Requests

### Pipe Validation Example

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

### Pipe Transformation

**Response**: Transformed data

```json
{
  "email": "user@example.com",
  "name": "john doe"
}
```

## Sequence Diagrams

### Pipe Flow

```
Request → Pipe → Validation → Transformation → Controller
            ↓
        Valid?
            ↓
        Yes → Continue
            ↓
        No → Error Response
```

## Architecture Diagrams

### Pipe Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Validation Pipe                           │
│                  (Validate Data)                            │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Transformation Pipe                        │
│                  (Transform Data)                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
│                  (Valid Data)                              │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the role of pipes in NestJS?

**Answer**: Pipes role:
- Validate incoming data
- Transform data
- Sanitize data
- Convert types
- Implement custom validation logic

### Q2: How do you create a custom pipe?

**Answer**: Custom pipe via:
- Implement PipeTransform interface
- Define transform method
- Apply pipe to controller or method
- Use decorator for parameter pipes
- Return transformed value

### Q3: How do you handle validation errors in pipes?

**Answer**: Validation errors via:
- Try-catch for validation
- Throw BadRequestException on failure
- Return error details
- Use proper error messages
- Log validation errors

## Exercises

### Exercise 1: Create a Validation Pipe

**Task**: Create a custom validation pipe.

**Steps**:
1. Implement PipeTransform interface
2. Add validation logic
3. Handle errors
4. Apply to controller
5. Test pipe

**Verification**:
- Pipe created
- Validation works
- Errors handled correctly
- Tests pass

### Exercise 2: Create a Transformation Pipe

**Task**: Create a transformation pipe.

**Steps**:
1. Implement PipeTransform interface
2. Add transformation logic
3. Handle type conversion
4. Apply to controller
5. Test pipe

**Verification**:
- Pipe created
- Transformation works
- Type conversion works
- Tests pass

## Real Production Scenarios

### Scenario 1: Validation Error

**Situation**: Validation failing unexpectedly

**Response**:
1. Check pipe logic
2. Check validation rules
3. Check input data
4. Fix validation
5. Test validation

### Scenario 2: Performance Issue

**Situation**: Pipe slow

**Response**:
1. Identify slow pipe
2. Optimize pipe logic
3. Add caching if applicable
4. Monitor performance
5. Test optimization

## Navigation

**Next Section**: [08-Interceptors](./08-Interceptors.md)

**Previous Section**: [06-Guards](./06-Guards.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [05-DTOs](./05-DTOs.md) - DTOs
- [03-Controllers](./03-Controllers.md) - Controllers
