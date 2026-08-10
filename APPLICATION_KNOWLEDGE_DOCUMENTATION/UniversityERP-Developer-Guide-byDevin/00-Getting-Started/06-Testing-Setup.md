# Testing Setup

## Purpose

This document provides detailed instructions for setting up the testing framework for the University ERP system. This includes unit tests, integration tests, and E2E tests.

## Why This Document Exists

**Confirmed by Code**: The project uses Jest for testing. Proper testing setup ensures:
- Code quality
- Bug prevention
- Refactoring confidence
- Documentation through tests

Without proper testing setup, code quality will degrade over time.

## Where This Is Used

- **Development**: Running tests during development
- **CI/CD**: Automated testing in pipelines
- **Code Review**: Ensuring changes don't break existing functionality
- **Refactoring**: Confidence when refactoring code

## Prerequisites

**Required**:
- Complete [02-Installation.md](./02-Installation.md)
- Complete [04-Development-Setup.md](./04-Development-Setup.md)

**Verification**:
- [ ] Dependencies installed
- [ ] Database running
- [ ] Jest installed

## Testing Framework

### Jest

**Confirmed by Code**: Jest is configured in the project.

**Package**: `jest` in devDependencies

**Configuration**: `jest.config.js` in each package

**Why Jest**:
- Zero configuration
- Built-in assertions
- Mocking support
- Snapshot testing
- Code coverage
- Parallel test execution

### Test Structure

**Confirmed by Code**: Test files follow naming convention.

**Convention**: `*.spec.ts` or `*.test.ts`

**Example Structure**:
```
apps/core-api/src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.service.spec.ts  # Unit test
│   │   └── auth.controller.spec.ts  # Controller test
```

## Unit Testing

### Setting Up Unit Tests

**Confirmed by Code**: Jest is configured for unit tests.

**Action**:
```bash
cd apps/core-api

# Run unit tests
npm test

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage
```

### Writing Unit Tests

**Service Test Example**:

```typescript
// auth.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { AuthService } from './auth.service';
import { PrismaService } from '../database/prisma.service';
import { JwtService } from '@nestjs/jwt';

describe('AuthService', () => {
  let service: AuthService;
  let prisma: PrismaService;
  let jwtService: JwtService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        {
          provide: PrismaService,
          useValue: {
            user: {
              findUnique: jest.fn(),
              create: jest.fn(),
              update: jest.fn(),
            },
          },
        },
        {
          provide: JwtService,
          useValue: {
            sign: jest.fn(),
            verify: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<AuthService>(AuthService);
    prisma = module.get<PrismaService>(PrismaService);
    jwtService = module.get<JwtService>(JwtService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('validateUser', () => {
    it('should return user if credentials are valid', async () => {
      const mockUser = {
        id: 'user-id',
        email: 'test@example.com',
        passwordHash: 'hashed-password',
      };

      jest.spyOn(prisma.user, 'findUnique').mockResolvedValue(mockUser as any);
      jest.spyOn(bcrypt, 'compare').mockResolvedValue(true as any);

      const result = await service.validateUser('test@example.com', 'password');

      expect(result).toEqual(mockUser);
    });

    it('should return null if user not found', async () => {
      jest.spyOn(prisma.user, 'findUnique').mockResolvedValue(null);

      const result = await service.validateUser('test@example.com', 'password');

      expect(result).toBeNull();
    });
  });
});
```

### Controller Test Example

```typescript
// auth.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';

describe('AuthController', () => {
  let controller: AuthController;
  let service: AuthService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AuthController],
      providers: [
        {
          provide: AuthService,
          useValue: {
            login: jest.fn(),
            register: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<AuthController>(AuthController);
    service = module.get<AuthService>(AuthService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('login', () => {
    it('should return access token and refresh token', async () => {
      const mockUser = { id: 'user-id', email: 'test@example.com' };
      const mockTokens = {
        accessToken: 'access-token',
        refreshToken: 'refresh-token',
      };

      jest.spyOn(service, 'login').mockResolvedValue({
        ...mockTokens,
        user: mockUser,
      } as any);

      const result = await controller.login({ user: mockUser } as any);

      expect(result).toEqual({
        ...mockTokens,
        user: mockUser,
      });
    });
  });
});
```

### Mocking Dependencies

**Mocking Prisma**:
```typescript
{
  provide: PrismaService,
  useValue: {
    user: {
      findUnique: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      findMany: jest.fn(),
    },
  },
}
```

**Mocking External Services**:
```typescript
{
  provide: MinioService,
  useValue: {
    upload: jest.fn(),
    download: jest.fn(),
    delete: jest.fn(),
  },
}
```

## Integration Testing

### Setting Up Integration Tests

**Status**: Not fully implemented

**Proposal**: Use NestJS testing utilities for integration tests:

```typescript
// auth.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../app.module';

describe('AuthController (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/auth/login (POST)', () => {
    return request(app.getHttpServer())
      .post('/auth/login')
      .send({ email: 'test@example.com', password: 'password' })
      .expect(201)
      .expect((res) => {
        expect(res.body).toHaveProperty('accessToken');
        expect(res.body).toHaveProperty('refreshToken');
      });
  });

  afterAll(async () => {
    await app.close();
  });
});
```

### Test Database

**Status**: Not implemented

**Proposal**: Use separate test database:

```bash
# Add to .env.test
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp_test
```

**Setup**:
```typescript
// test setup
beforeAll(async () => {
  // Run migrations on test database
  await exec('npx prisma migrate deploy');
});

afterAll(async () => {
  // Clean up test database
  await exec('npx prisma migrate reset --force');
});
```

## E2E Testing

### Setting Up E2E Tests

**Status**: Not implemented

**Proposal**: Use Playwright for E2E tests:

```bash
npm install -D @playwright/test
npx playwright install
```

**Configuration**: `playwright.config.ts`

**Example Test**:
```typescript
// login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('http://localhost:5173/login');
  
  await page.fill('input[name="email"]', 'admin@university.edu');
  await page.fill('input[name="password"]', 'admin123');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('http://localhost:5173/dashboard');
});
```

### Running E2E Tests

```bash
# Run E2E tests
npx playwright test

# Run in headed mode
npx playwright test --headed

# Run specific test
npx playwright test login.spec.ts
```

## Test Coverage

### Generating Coverage Report

**Confirmed by Code**: Jest supports coverage.

**Action**:
```bash
cd apps/core-api

# Generate coverage report
npm test -- --coverage

# Open coverage report
open coverage/index.html
```

**Coverage Thresholds**:

**Status**: Not configured

**Proposal**: Add coverage thresholds to jest.config.js:

```javascript
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

### Coverage Report

**Output**: `coverage/` directory

**Files**:
- `index.html` - HTML report
- `lcov.info` - LCOV format
- `clover.xml` - Clover XML format

## Testing Best Practices

### Unit Test Best Practices

1. **Test One Thing**: Each test should test one specific behavior
2. **Arrange-Act-Assert**: Structure tests clearly
3. **Descriptive Names**: Use descriptive test names
4. **Independent Tests**: Tests should not depend on each other
5. **Mock External Dependencies**: Mock databases, APIs, etc.
6. **Test Edge Cases**: Test null, undefined, empty arrays, etc.
7. **Keep Tests Fast**: Unit tests should be fast
8. **Avoid Implementation Details**: Test behavior, not implementation

### Integration Test Best Practices

1. **Test Real Interactions**: Test real database, Redis, etc.
2. **Use Test Database**: Don't use production database
3. **Clean Up**: Clean up after each test
4. **Test Happy Path**: Test successful scenarios
5. **Test Error Paths**: Test error scenarios
6. **Test Performance**: Test response times
7. **Test Security**: Test authentication, authorization

### E2E Test Best Practices

1. **Test User Flows**: Test complete user journeys
2. **Test Critical Paths**: Test most important features
3. **Test Cross-Browser**: Test in multiple browsers
4. **Test Mobile**: Test on mobile devices
5. **Test Slow Networks**: Test with slow network simulation
6. **Test Accessibility**: Test with screen readers

## Common Testing Patterns

### Testing Controllers

```typescript
describe('MyController', () => {
  let controller: MyController;
  let service: MyService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      controllers: [MyController],
      providers: [
        {
          provide: MyService,
          useValue: {
            method: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get(MyController);
    service = module.get(MyService);
  });

  it('should call service method', async () => {
    jest.spyOn(service, 'method').mockResolvedValue('result');
    
    await controller.method();
    
    expect(service.method).toHaveBeenCalled();
  });
});
```

### Testing Services

```typescript
describe('MyService', () => {
  let service: MyService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        MyService,
        {
          provide: PrismaService,
          useValue: {
            model: {
              findMany: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get(MyService);
    prisma = module.get(PrismaService);
  });

  it('should return data from database', async () => {
    const mockData = [{ id: '1', name: 'Test' }];
    jest.spyOn(prisma.model, 'findMany').mockResolvedValue(mockData);
    
    const result = await service.findAll();
    
    expect(result).toEqual(mockData);
  });
});
```

### Testing Guards

```typescript
describe('MyGuard', () => {
  let guard: MyGuard;
  let reflector: Reflector;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        MyGuard,
        {
          provide: Reflector,
          useValue: {
            get: jest.fn(),
          },
        },
      ],
    }).compile();

    guard = module.get(MyGuard);
    reflector = module.get(Reflector);
  });

  it('should allow access if public', () => {
    jest.spyOn(reflector, 'get').mockReturnValue(true);
    
    const context = createMock<ExecutionContext>();
    const result = guard.canActivate(context);
    
    expect(result).toBe(true);
  });
});
```

## Running Tests

### Run All Tests

```bash
# Run all tests in all packages
npm test

# Run all tests in specific package
cd apps/core-api
npm test
```

### Run Specific Test

```bash
# Run specific test file
npm test -- auth.service.spec.ts

# Run specific test
npm test -- -t "should return user if credentials are valid"
```

### Run Tests in Watch Mode

```bash
# Watch mode
npm test -- --watch

# Watch mode with coverage
npm test -- --watch --coverage
```

### Run Tests with Coverage

```bash
# Generate coverage
npm test -- --coverage

# Coverage with threshold
npm test -- --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

## CI/CD Integration

### GitHub Actions

**Status**: Not implemented

**Proposal**: Add GitHub Actions workflow:

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Run migrations
        run: |
          cd apps/core-api
          npx prisma migrate deploy
      
      - name: Run tests
        run: npm test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Common Issues

### Issue 1: Tests Timeout

**Symptom**: Tests timeout after 5000ms

**Cause**: Async operations not awaited

**Fix**:
```typescript
// Wrong
it('should return user', () => {
  service.getUser();
});

// Correct
it('should return user', async () => {
  await service.getUser();
});
```

### Issue 2: Mock Not Working

**Symptom**: Mock function not being called

**Cause**: Mock not set up correctly

**Fix**:
```typescript
// Wrong
jest.spyOn(service, 'method');

// Correct
jest.spyOn(service, 'method').mockResolvedValue('result');
```

### Issue 3: Test Database Not Clean

**Symptom**: Tests affect each other

**Cause**: Database not cleaned between tests

**Fix**:
```typescript
beforeEach(async () => {
  // Clean database
  await prisma.user.deleteMany();
  await prisma.institute.deleteMany();
});
```

### Issue 4: Coverage Low

**Symptom**: Low test coverage

**Cause**: Not enough tests

**Fix**:
- Add more tests
- Test edge cases
- Test error paths
- Test all branches

## Future Enhancements

### Visual Regression Testing

**Status**: Not implemented

**Proposal**: Use Percy or Chromatic for visual regression testing

### Performance Testing

**Status**: Not implemented

**Proposal**: Use k6 or Artillery for performance testing

### Load Testing

**Status**: Not implemented

**Proposal**: Use k6 or Artillery for load testing

## Related Documentation

- [04-Development-Setup.md](./04-Development-Setup.md) - Development setup
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
- [17-Production](../17-Production/README.md) - Production guide
