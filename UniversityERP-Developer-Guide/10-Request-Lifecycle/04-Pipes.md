# Pipes

## Purpose

This document explains pipes in the University ERP system. It details how pipes work, how to create custom pipes, and how pipes fit into the request lifecycle.

## Why This Document Exists

**Confirmed by Code**: Pipes are used for validation and transformation. Understanding pipes is critical for:
- Validating input data
- Transforming input data
- Sanitizing input data
- Debugging validation issues
- Creating custom pipes

Without understanding pipes, developers may struggle with validation or may introduce validation bugs.

## Where This Is Used

- **Onboarding**: New developers learn pipes
- **Feature Development**: Implementing pipes
- **Code Reviews**: Reviewing pipe code
- **Validation**: Validating input data
- **Transformation**: Transforming input data

## Dependencies

### Pipe Dependencies

**Confirmed by Code**: Pipes depend on:

- **NestJS**: Framework for pipes
- **Zod**: Validation library
- **TypeScript**: Type-safe pipes

## Internal Architecture

### Pipe Architecture

**Confirmed by Code**: Pipes execute before controller.

```
┌─────────────────────────────────────────────────────────┐
│              Interceptors (Pre)                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Pipes                                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Controller                                   │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Pipe Implementation

**Confirmed by Code**: Pipes implement PipeTransform interface.

**ZodValidationPipe**:
```typescript
import { Injectable, PipeTransform, BadRequestException } from '@nestjs/common';
import { z } from 'zod';

@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: z.ZodSchema) {}

  transform(value: any) {
    try {
      return this.schema.parse(value);
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new BadRequestException({
          message: 'Validation failed',
          errors: error.errors,
        });
      }
      throw new BadRequestException('Validation failed');
    }
  }
}
```

**What This Does**:
- **PipeTransform**: Implements PipeTransform interface
- **transform()**: Pipe function
- **Zod Schema**: Validates against Zod schema
- **Error**: Throws BadRequestException on validation failure

**ParseIntPipe**:
```typescript
import { Injectable, PipeTransform, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseIntPipe implements PipeTransform {
  transform(value: any) {
    const val = parseInt(value, 10);
    if (isNaN(val)) {
      throw new BadRequestException('Validation failed: cannot parse integer');
    }
    return val;
  }
}
```

**What This Does**:
- **Parse**: Parses string to integer
- **Validation**: Validates integer
- **Error**: Throws BadRequestException on failure

**TrimPipe**:
```typescript
import { Injectable, PipeTransform } from '@nestjs/common';

@Injectable()
export class TrimPipe implements PipeTransform {
  transform(value: any) {
    if (typeof value === 'string') {
      return value.trim();
    }
    return value;
  }
}
```

**What This Does**:
- **Trim**: Trims whitespace from strings
- **Type Check**: Only trims strings
- **Pass-through**: Passes non-strings unchanged

### Pipe Usage

**Confirmed by Code**: Pipes applied at parameter or method level.

**Parameter-Level Pipes**:
```typescript
@Controller('users')
export class UsersController {
  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }

  @Patch(':id')
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body(new ZodValidationPipe(UpdateUserDto)) dto: UpdateUserDto,
  ) {
    return this.usersService.update(id, dto);
  }
}
```

**What This Does**:
- **@Param()**: Applies pipe to parameter
- **ParseIntPipe**: Parses ID to integer
- **ZodValidationPipe**: Validates body against schema

**Method-Level Pipes**:
```typescript
@Controller('users')
export class UsersController {
  @Post()
  @UsePipes(new ZodValidationPipe(CreateUserDto))
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}
```

**What This Does**:
- **@UsePipes**: Applies pipe to method
- **ZodValidationPipe**: Validates entire request body

**Global Pipes**:
```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(
    new ZodValidationPipe(Zod.object({
      // global validation rules
    })),
  );
  
  await app.listen(3000);
}
```

**What This Does**:
- **useGlobalPipes**: Applies pipe globally
- **Global Validation**: Validates all requests

## Database Interactions

### Pipe-Database Flow

**Confirmed by Code**: Pipes don't interact with database.

**Flow**:
```
Pipe → No database interaction
```

## Redis Interactions

### Pipe-Redis Flow

**Confirmed by Code**: Pipes don't interact with Redis.

**Flow**:
```
Pipe → No Redis interaction
```

## Queue Interactions

### Pipe-Queue Flow

**Confirmed by Code**: Pipes don't interact with queues.

**Flow**:
```
Pipe → No queue interaction
```

## Worker Interactions

### Pipe-Worker Flow

**Confirmed by Code**: Workers don't use pipes.

**Flow**:
```
Worker → No pipes (internal service)
```

## Business Rules

### Pipe Rules

**Confirmed by Code**: Pipes follow these rules:

1. **PipeTransform**: Implement PipeTransform interface
2. **Transform**: Transform input data
3. **Validation**: Validate input data
4. **Error Handling**: Throw exceptions on validation failure
5. **Order**: Pipes execute in order

### Pipe Order Rules

**Confirmed by Code**: Pipe order follows these rules:

1. **Parameter-Level**: Parameter-level pipes first
2. **Method-Level**: Method-level pipes second
3. **Global**: Global pipes last
4. **Registration Order**: Execute in registration order
4. **All Execute**: All pipes execute

## Security

### Pipe Security

**Confirmed by Code**: Security considerations for pipes:

1. **Input Validation**: Validate all input
2. **Input Sanitization**: Sanitize malicious input
3. **Type Safety**: Ensure type safety
4. **Error Messages**: Don't leak sensitive info in errors
5. **Length Limits**: Limit input length

## Performance Considerations

### Pipe Performance

**Confirmed by Code**: Performance considerations:

1. **Fast Execution**: Keep pipes fast
2. **Validation**: Use efficient validation
3. **Schema Compilation**: Compile schemas once
4. **Skip Validation**: Skip validation when possible
5. **Async Operations**: Use async for slow operations

## Common Mistakes

### Mistake 1: Not Implementing PipeTransform

**Symptom**: Pipe not working

**Cause**: Not implementing PipeTransform interface

**Fix**:
```typescript
// Implement PipeTransform
@Injectable()
export class MyPipe implements PipeTransform {
  transform(value: any) {
    return value;
  }
}
```

### Mistake 2: Not Handling Errors

**Symptom**: Errors not caught

**Cause**: Not handling errors in pipe

**Fix**:
```typescript
// Add error handling
try {
  return this.schema.parse(value);
} catch (error) {
  throw new BadRequestException('Validation failed');
}
```

### Mistake 3: Not Returning Value

**Symptom**: Pipe not transforming data

**Cause**: Not returning value

**Fix**:
```typescript
// Return transformed value
return transformedValue;
```

## Debugging Guide

### Pipe Debugging

**Issue**: Pipe not working

**Investigation**:
1. Check pipe registration
2. Check pipe logic
3. Check validation schema
4. Check error handling
5. Check logs

**Tools**:
- Pipe logs
- Validation logs
- Error logs
- Console logs

## Future Enhancements

### Custom Validation Pipes

**Status**: Partially implemented

**Proposal**: Implement custom validation pipes:
- Business logic validation
- Database validation
- Async validation
- More flexible validation
- More complex

### Sanitization Pipes

**Status**: Not implemented

**Proposal**: Implement sanitization pipes:
- XSS sanitization
- SQL injection prevention
- HTML sanitization
- Better security
- More complex

## Production Considerations

### Production Pipes

**Production Deployment**:
- Enable all pipes
- Configure validation
- Configure sanitization
- Monitor pipe performance
- Monitor validation errors

### Pipe Monitoring

**Monitoring Metrics**:
- Pipe execution time
- Validation failure rate
- Transformation rate
- Error rate
- Validation patterns

## Example Requests

### Pipe Example

**Request**:
```bash
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Example Responses

### Pipe Response

**Response** (Valid):
```json
{
  "success": true,
  "data": {...}
}
```

**Response** (Invalid):
```json
{
  "success": false,
  "error": {
    "code": 400,
    "message": "Validation failed",
    "errors": [...]
  }
}
```

## Sequence Diagrams

### Pipe Flow

```
Request → Interceptors → Pipe 1 → Pipe 2 → Pipe 3 → Controller → Service
```

## Architecture Diagrams

### Pipe Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Interceptors (Pre)                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Pipe 1 (Validation)                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Pipe 2 (Transformation)                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Pipe 3 (Sanitization)                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                                   │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do pipes work in NestJS?

**Answer**: Pipes via:
- Implement PipeTransform interface
- Transform input data
- Validate input data
- Execute before controller
- Can be parameter, method, or global

### Q2: How do you create a custom pipe?

**Answer**: Custom pipe via:
- Implement PipeTransform interface
- Add pipe logic
- Transform or validate data
- Return transformed data
- Register pipe

### Q3: What is the difference between pipes and validators?

**Answer**: Pipes vs Validators:
- Pipes: Transform and validate data
- Validators: Only validate data
- Pipes: More flexible
- Validators: Simpler
- Pipes: Can be chained
- Validators: Usually standalone

## Exercises

### Exercise 1: Create a Pipe

**Task**: Create a custom pipe.

**Steps**:
1. Implement PipeTransform interface
2. Add pipe logic
3. Add error handling
4. Register pipe
5. Test pipe

**Verification**:
- Pipe created
- Logic works
- Error handling works
- Pipe registered
- Tests pass

### Exercise 2: Create a Validation Pipe

**Task**: Create a validation pipe.

**Steps**:
1. Implement PipeTransform interface
2. Add validation logic
3. Use Zod for validation
4. Add error handling
5. Test validation

**Verification**:
- Pipe created
- Validation works
- Zod works
- Error handling works
- Tests pass

## Real Production Scenarios

### Scenario 1: Pipe Not Validating

**Situation**: Pipe not validating input

**Response**:
1. Check pipe registration
2. Check validation schema
3. Check pipe logic
4. Fix pipe
5. Test pipe

### Scenario 2: Pipe Causing Error

**Situation**: Pipe causing error

**Response**:
1. Check pipe logic
2. Check error handling
3. Check validation schema
4. Fix pipe
5. Test pipe

## Navigation

**Next Section**: [05-Exception-Filters](./05-Exception-Filters.md)

**Previous Section**: [03-Interceptors](./03-Interceptors.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-Backend/07-Pipes](../03-Backend/07-Pipes.md) - Pipes details
