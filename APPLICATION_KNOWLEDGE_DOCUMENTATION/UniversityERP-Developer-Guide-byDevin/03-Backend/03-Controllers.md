# Controllers

## Purpose

This document explains the controller pattern used in the University ERP backend. It details how controllers handle HTTP requests, route definitions, and request/response handling.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend uses NestJS controllers for HTTP handling. Understanding controllers is critical for:
- Creating API endpoints
- Handling HTTP requests
- Implementing route logic
- Validating requests
- Formatting responses

Without understanding controllers, developers may struggle to create or modify API endpoints.

## Where This Is Used

- **Onboarding**: New developers learn controller pattern
- **Feature Development**: Creating API endpoints
- **Code Reviews**: Reviewing controller code
- **Debugging**: Debugging HTTP issues
- **API Development**: Developing REST APIs

## Dependencies

### Controller Dependencies

**Confirmed by Code**: Controllers depend on:

- **NestJS Controller Decorator**: Route definition
- **Services**: Business logic
- **DTOs**: Data transfer objects
- **Guards**: Route protection
- **Pipes**: Request validation

## Internal Architecture

### Controller Architecture

**Confirmed by Code**: Controllers follow RESTful conventions.

```
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  HTTP Methods │  │  Parameters    │  │  Body          │
│  (GET, POST)  │  │  (@Param, @Query)│  │  (@Body)       │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Service Layer                             │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Controller Definition

**Confirmed by Code**: Controllers defined with @Controller decorator.

**Basic Controller**:
```typescript
@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  findAll() {
    return this.usersService.findAll();
  }
}
```

**What This Does**:
- **@Controller**: Defines route prefix ('/users')
- **constructor**: Injects UsersService
- **@Get**: Defines GET endpoint for '/users'
- **findAll()**: Delegates to service

### HTTP Methods

**Confirmed by Code**: Controllers support all HTTP methods.

**GET Request**:
```typescript
@Get()
findAll() {
  return this.usersService.findAll();
}

@Get(':id')
findOne(@Param('id') id: string) {
  return this.usersService.findOne(id);
}
```

**POST Request**:
```typescript
@Post()
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

**PATCH Request**:
```typescript
@Patch(':id')
update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
  return this.usersService.update(id, dto);
}
```

**DELETE Request**:
```typescript
@Delete(':id')
remove(@Param('id') id: string) {
  return this.usersService.remove(id);
}
```

### Parameters

**Confirmed by Code**: Controllers extract parameters from requests.

**Route Parameters**:
```typescript
@Get(':id')
findOne(@Param('id') id: string) {
  return this.usersService.findOne(id);
}
```

**Query Parameters**:
```typescript
@Get()
findAll(@Query() query: QueryUserDto) {
  return this.usersService.findAll(query);
}
```

**Request Body**:
```typescript
@Post()
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

**Headers**:
```typescript
@Get()
findAll(@Headers() headers: Record<string, string>) {
  console.log(headers);
  return this.usersService.findAll();
}
```

### Custom Decorators

**Confirmed by Code**: Custom decorators for common operations.

**CurrentUser Decorator**:
```typescript
export const CurrentUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return data ? request.user?.[data] : request.user;
  },
);
```

**Usage**:
```typescript
@Get('profile')
getProfile(@CurrentUser() user: JwtPayload) {
  return this.usersService.getProfile(user.id);
}
```

### Guards

**Confirmed by Code**: Guards protect routes.

**Applying Guards**:
```typescript
@Controller('users')
@UseGuards(GlobalJwtAuthGuard, ScopeGuard)
export class UsersController {
  @Get()
  @Scope('users')
  findAll() {
    return this.usersService.findAll();
  }

  @Get('public')
  @Public()
  publicData() {
    return { message: 'Public data' };
  }
}
```

**What This Does**:
- **@UseGuards**: Applies guards to all routes
- **@Scope**: Sets required scope for route
- **@Public**: Marks route as public (no auth)

### Pipes

**Confirmed by Code**: Pipes validate and transform data.

**Applying Pipes**:
```typescript
@Post()
@UsePipes(new ZodValidationPipe(CreateUserSchema))
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

**Global Pipe**:
```typescript
// In main.ts
app.useGlobalPipes(new ValidationPipe());
```

### Response Formatting

**Confirmed by Code**: Controllers format responses consistently.

**Standard Response**:
```typescript
@Get()
async findAll() {
  const users = await this.usersService.findAll();
  return {
    success: true,
    data: users,
  };
}
```

**Error Response**:
```typescript
@Get()
async findAll() {
  try {
    const users = await this.usersService.findAll();
    return {
      success: true,
      data: users,
    };
  } catch (error) {
    throw new BadRequestException('Failed to fetch users');
  }
}
```

## Database Interactions

### Controller-Service-Database Flow

**Confirmed by Code**: Controllers delegate to services which interact with database.

**Flow**:
```
Controller → Service → Prisma → Database
```

**Example**:
```typescript
// Controller
@Get(':id')
findOne(@Param('id') id: string) {
  return this.usersService.findOne(id);
}

// Service
async findOne(id: string) {
  return this.prisma.user.findUnique({ where: { id } });
}
```

## Redis Interactions

### Controller-Service-Redis Flow

**Confirmed by Code**: Controllers delegate to services which interact with Redis.

**Flow**:
```
Controller → Service → Redis
```

**Example**:
```typescript
// Controller
@Get(':id')
findOne(@Param('id') id: string) {
  return this.usersService.findOne(id);
}

// Service
async findOne(id: string) {
  const cacheKey = `user:${id}`;
  const cached = await this.redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const user = await this.prisma.user.findUnique({ where: { id } });
  await this.redis.setex(cacheKey, 300, JSON.stringify(user));
  
  return user;
}
```

## Queue Interactions

### Controller-Service-Queue Flow

**Confirmed by Code**: Controllers delegate to services which submit to queues.

**Flow**:
```
Controller → Service → Queue
```

**Example**:
```typescript
// Controller
@Post('send-email')
sendEmail(@Body() dto: EmailDto) {
  return this.notificationService.sendEmail(dto);
}

// Service
async sendEmail(dto: EmailDto) {
  await this.notificationQueue.add('email', dto);
  return { success: true, message: 'Email queued' };
}
```

## Worker Interactions

### Controllers and Workers

**Confirmed by Code**: Controllers don't directly interact with workers.

**Flow**:
```
Controller → Service → Queue → Worker
```

**Example**:
```typescript
// Controller
@Post('send-email')
sendEmail(@Body() dto: EmailDto) {
  return this.notificationService.sendEmail(dto);
}

// Service
async sendEmail(dto: EmailDto) {
  await this.notificationQueue.add('email', dto);
}

// Worker (separate service)
@Processor('notifications')
export class NotificationProcessor {
  @Process('email')
  async handleEmail(job: Job) {
    await this.mailService.sendEmail(job.data);
  }
}
```

## Business Rules

### Controller Rules

**Confirmed by Code**: Controllers follow these rules:

1. **Thin Controllers**: Controllers should be thin
2. **Delegation**: Delegate to services for business logic
3. **Validation**: Validate all inputs
4. **Formatting**: Format responses consistently
5. **Error Handling**: Handle errors appropriately

### RESTful Rules

**Confirmed by Code**: Controllers follow RESTful conventions:

1. **GET**: Retrieve data
2. **POST**: Create data
3. **PATCH**: Update data (partial)
4. **PUT**: Update data (full)
5. **DELETE**: Delete data

## Security

### Controller Security

**Confirmed by Code**: Security measures in controllers:

1. **Guards**: Apply guards for authentication/authorization
2. **Validation**: Validate all inputs
3. **Sanitization**: Sanitize outputs
4. **Rate Limiting**: Apply rate limiting where appropriate
5. **Scope Enforcement**: Enforce scope-based access

## Performance Considerations

### Controller Performance

**Confirmed by Code**: Performance considerations for controllers:

1. **Pagination**: Paginate large datasets
2. **Select Fields**: Select only needed fields
3. **Caching**: Cache frequently accessed data
4. **Async Operations**: Use async/await
5. **Connection Pooling**: Reuse database connections

## Common Mistakes

### Mistake 1: Business Logic in Controller

**Symptom**: Controller has complex logic

**Cause**: Business logic in controller

**Fix**:
```typescript
// Wrong
@Controller('users')
export class UsersController {
  @Get()
  async findAll() {
    const users = await this.prisma.user.findMany();
    return users.filter(u => u.active);
  }
}

// Correct
@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  findAll() {
    return this.usersService.findAll();
  }
}
```

### Mistake 2: Not Validating Input

**Symptom**: Invalid data in database

**Cause**: Not validating input

**Fix**:
```typescript
// Add validation pipe
@Post()
@UsePipes(new ZodValidationPipe(CreateUserSchema))
create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

### Mistake 3: Not Handling Errors

**Symptom**: Unhandled errors

**Cause**: Not handling errors

**Fix**:
```typescript
// Add error handling
@Get()
async findAll() {
  try {
    return await this.usersService.findAll();
  } catch (error) {
    throw new BadRequestException('Failed to fetch users');
  }
}
```

## Debugging Guide

### Controller Debugging

**Issue**: Controller not working

**Investigation**:
1. Check route definition
2. Check parameter extraction
3. Check service call
4. Check response format
5. Check logs

**Tools**:
- NestJS debugger
- Postman/curl for testing
- Application logs
- Network tools

## Future Enhancements

### GraphQL Resolvers

**Status**: Not implemented

**Proposal**: Add GraphQL resolvers:
- Replace REST with GraphQL
- Flexible queries
- Reduced over-fetching
- Better for frontend

### OpenAPI Specification

**Status**: Not implemented

**Proposal**: Add OpenAPI spec:
- Auto-generate API documentation
- Swagger UI
- API testing
- Client generation

## Production Considerations

### Production Controllers

**Production Deployment**:
- Enable response compression
- Enable CORS properly
- Configure rate limiting
- Configure logging
- Configure monitoring

### Controller Monitoring

**Monitoring Metrics**:
- Request rate per endpoint
- Response time per endpoint
- Error rate per endpoint
- Request size
- Response size

## Example Requests

### Controller Example

**Request**:
```bash
GET /api/users?page=1&limit=10
Authorization: Bearer <token>
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": "user-id",
      "email": "user@example.com"
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 10
  }
}
```

## Example Responses

### Controller Response

**Response**: Controller response

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

### Request Flow

```
Client → HTTP Request → Guard → Pipe → Controller → Service → Database
                                                              ↓
                                                          Response
                                                              ↓
                                                          Controller
                                                              ↓
                                                          Client
```

## Architecture Diagrams

### Controller Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HTTP Request                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Guard                                    │
│                  (Authentication/Authorization)             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Pipe                                     │
│                  (Validation/Transformation)                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Controller                               │
│                  (HTTP Handler)                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Service                                  │
│                  (Business Logic)                         │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the role of a controller in NestJS?

**Answer**: Controller role:
- Handle HTTP requests
- Extract parameters from requests
- Delegate to services for business logic
- Format responses
- Apply guards and pipes

### Q2: How do you handle different HTTP methods in controllers?

**Answer**: HTTP methods via decorators:
- @Get() for GET requests
- @Post() for POST requests
- @Patch() for PATCH requests
- @Put() for PUT requests
- @Delete() for DELETE requests

### Q3: How do you validate request data in controllers?

**Answer**: Validation via:
- Validation pipes
- DTOs with validation decorators
- Zod schemas
- Custom validation logic
- Global validation pipe

## Exercises

### Exercise 1: Create a Controller

**Task**: Create a new controller.

**Steps**:
1. Generate controller with NestJS CLI
2. Define routes
3. Add parameter extraction
4. Add validation
5. Test endpoints

**Verification**:
- Controller created
- Routes work
- Validation works
- Endpoints tested

### Exercise 2: Add Custom Decorator

**Task**: Create a custom decorator.

**Steps**:
1. Create decorator function
2. Extract data from context
3. Return extracted data
4. Apply decorator to controller
5. Test decorator

**Verification**:
- Decorator created
- Decorator works
- Data extracted correctly

## Real Production Scenarios

### Scenario 1: Slow Endpoint

**Situation**: Controller endpoint slow

**Response**:
1. Identify slow endpoint
2. Check service logic
3. Add caching
4. Optimize queries
5. Monitor performance

### Scenario 2: Validation Error

**Situation**: Validation not working

**Response**:
1. Check validation pipe
2. Check DTO definition
3. Check validation rules
4. Fix validation
5. Test validation

## Navigation

**Next Section**: [04-Services](./04-Services.md)

**Previous Section**: [02-Module-System](./02-Module-System.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [02-Module-System](./02-Module-System.md) - Module system
- [12-API-Reference](../01-System-Architecture/12-API-Reference.md) - API reference
