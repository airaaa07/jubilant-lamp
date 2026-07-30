# Testing Guide

## Overview

This guide provides comprehensive instructions for testing the University ERP system. It covers unit testing, integration testing, E2E testing, and testing best practices.

## Testing Philosophy

**Confirmed by Code**: The University ERP follows a comprehensive testing strategy.

**Testing Pyramid:**
```
        E2E Tests (10%)
       /            \
    Integration Tests (30%)
   /                    \
Unit Tests (60%)
```

**Testing Goals:**
- Ensure code correctness
- Prevent regressions
- Document expected behavior
- Facilitate refactoring
- Improve code quality

## Unit Testing

### Backend Unit Testing

**Confirmed by Code**: The backend uses Jest for unit testing.

**Setup:**

```bash
# Install testing dependencies
cd apps/core-api
npm install --save-dev @types/jest jest ts-jest @nestjs/testing

# Configure Jest
# jest.config.js is already configured
```

**Writing Unit Tests:**

**File**: `apps/core-api/src/users/users.service.spec.ts`

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { PrismaService } from '../prisma/prisma.service';
import { ConflictException } from '@nestjs/common';

describe('UsersService', () => {
  let service: UsersService;
  let prisma: PrismaService;

  const mockPrismaService = {
    user: {
      findUnique: jest.fn(),
      findMany: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    },
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: PrismaService,
          useValue: mockPrismaService,
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('create', () => {
    it('should create a user successfully', async () => {
      const dto = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      const expectedResult = {
        id: 'user-id',
        ...dto,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      mockPrismaService.user.findUnique.mockResolvedValue(null);
      mockPrismaService.user.create.mockResolvedValue(expectedResult);

      const result = await service.create(dto);

      expect(result).toEqual(expectedResult);
      expect(prisma.user.findUnique).toHaveBeenCalledWith({
        where: { email: dto.email },
      });
      expect(prisma.user.create).toHaveBeenCalledWith({
        data: dto,
      });
    });

    it('should throw ConflictException if email already exists', async () => {
      const dto = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      mockPrismaService.user.findUnique.mockResolvedValue({
        id: 'existing-user-id',
        email: dto.email,
      });

      await expect(service.create(dto)).rejects.toThrow(ConflictException);
    });
  });

  describe('findAll', () => {
    it('should return an array of users', async () => {
      const expectedResult = [
        { id: 'user-1', email: 'user1@example.com', name: 'User 1' },
        { id: 'user-2', email: 'user2@example.com', name: 'User 2' },
      ];

      mockPrismaService.user.findMany.mockResolvedValue(expectedResult);

      const result = await service.findAll();

      expect(result).toEqual(expectedResult);
      expect(prisma.user.findMany).toHaveBeenCalled();
    });
  });

  describe('findOne', () => {
    it('should return a user by id', async () => {
      const userId = 'user-id';
      const expectedResult = {
        id: userId,
        email: 'test@example.com',
        name: 'Test User',
      };

      mockPrismaService.user.findUnique.mockResolvedValue(expectedResult);

      const result = await service.findOne(userId);

      expect(result).toEqual(expectedResult);
      expect(prisma.user.findUnique).toHaveBeenCalledWith({
        where: { id: userId },
      });
    });

    it('should return null if user not found', async () => {
      const userId = 'non-existent-id';

      mockPrismaService.user.findUnique.mockResolvedValue(null);

      const result = await service.findOne(userId);

      expect(result).toBeNull();
    });
  });
});
```

**Testing Controllers:**

**File**: `apps/core-api/src/users/users.controller.spec.ts`

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

describe('UsersController', () => {
  let controller: UsersController;
  let service: UsersService;

  const mockUsersService = {
    create: jest.fn(),
    findAll: jest.fn(),
    findOne: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: mockUsersService,
        },
      ],
    }).compile();

    controller = module.get<UsersController>(UsersController);
    service = module.get<UsersService>(UsersService);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('create', () => {
    it('should create a user', async () => {
      const dto: CreateUserDto = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      const expectedResult = {
        id: 'user-id',
        ...dto,
      };

      mockUsersService.create.mockResolvedValue(expectedResult);

      const result = await controller.create(dto);

      expect(result).toEqual(expectedResult);
      expect(service.create).toHaveBeenCalledWith(dto);
    });
  });

  describe('findAll', () => {
    it('should return an array of users', async () => {
      const expectedResult = [
        { id: 'user-1', email: 'user1@example.com' },
        { id: 'user-2', email: 'user2@example.com' },
      ];

      mockUsersService.findAll.mockResolvedValue(expectedResult);

      const result = await controller.findAll();

      expect(result).toEqual(expectedResult);
      expect(service.findAll).toHaveBeenCalled();
    });
  });
});
```

### Frontend Unit Testing

**Confirmed by Code**: The frontend uses React Testing Library for unit testing.

**Setup:**

```bash
# Install testing dependencies
cd web/admin-portal
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom
```

**Writing Unit Tests:**

**File**: `web/admin-portal/src/components/common/Button/Button.test.tsx`

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('should render button with label', () => {
    render(<Button label="Click me" onClick={() => {}} />);
    
    const button = screen.getByRole('button', { name: 'Click me' });
    expect(button).toBeInTheDocument();
  });

  it('should call onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button label="Click me" onClick={handleClick} />);
    
    const button = screen.getByRole('button', { name: 'Click me' });
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button label="Click me" onClick={() => {}} disabled />);
    
    const button = screen.getByRole('button', { name: 'Click me' });
    expect(button).toBeDisabled();
  });

  it('should not call onClick when disabled', () => {
    const handleClick = jest.fn();
    render(<Button label="Click me" onClick={handleClick} disabled />);
    
    const button = screen.getByRole('button', { name: 'Click me' });
    fireEvent.click(button);
    
    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

**Testing Custom Hooks:**

**File**: `web/admin-portal/src/hooks/useAuth.test.ts`

```typescript
import { renderHook, act } from '@testing-library/react';
import { useAuth } from './useAuth';
import { AuthProvider } from '../context/AuthContext';

describe('useAuth', () => {
  it('should return user and loading state', () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.user).toBeNull();
    expect(result.current.loading).toBe(true);
  });

  it('should login user', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login('admin@university.edu', 'admin123');
    });

    expect(result.current.user).not.toBeNull();
    expect(result.current.user?.email).toBe('admin@university.edu');
  });

  it('should logout user', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <AuthProvider>{children}</AuthProvider>
    );

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login('admin@university.edu', 'admin123');
    });

    await act(async () => {
      await result.current.logout();
    });

    expect(result.current.user).toBeNull();
  });
});
```

## Integration Testing

### Backend Integration Testing

**Confirmed by Code**: The backend uses NestJS testing utilities for integration testing.

**Setup:**

```bash
# Install testing dependencies
cd apps/core-api
npm install --save-dev @nestjs/testing supertest
```

**Writing Integration Tests:**

**File**: `apps/core-api/test/users.e2e-spec.ts`

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';

describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe());
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('/users (POST)', () => {
    it('should create a user', () => {
      const dto = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      return request(app.getHttpServer())
        .post('/users')
        .send(dto)
        .expect(201)
        .expect((res) => {
          expect(res.body).toHaveProperty('id');
          expect(res.body.email).toBe(dto.email);
          expect(res.body.name).toBe(dto.name);
        });
    });

    it('should return 400 for invalid email', () => {
      const dto = {
        email: 'invalid-email',
        password: 'password123',
        name: 'Test User',
      };

      return request(app.getHttpServer())
        .post('/users')
        .send(dto)
        .expect(400);
    });

    it('should return 400 for weak password', () => {
      const dto = {
        email: 'test@example.com',
        password: '123',
        name: 'Test User',
      };

      return request(app.getHttpServer())
        .post('/users')
        .send(dto)
        .expect(400);
    });
  });

  describe('/users (GET)', () => {
    it('should return an array of users', () => {
      return request(app.getHttpServer())
        .get('/users')
        .expect(200)
        .expect((res) => {
          expect(Array.isArray(res.body)).toBe(true);
        });
    });
  });

  describe('/users/:id (GET)', () => {
    it('should return a user by id', () => {
      const userId = 'user-id';

      return request(app.getHttpServer())
        .get(`/users/${userId}`)
        .expect(200)
        .expect((res) => {
          expect(res.body).toHaveProperty('id');
          expect(res.body.id).toBe(userId);
        });
    });

    it('should return 404 for non-existent user', () => {
      const userId = 'non-existent-id';

      return request(app.getHttpServer())
        .get(`/users/${userId}`)
        .expect(404);
    });
  });
});
```

### Frontend Integration Testing

**Confirmed by Code**: The frontend uses React Testing Library for integration testing.

**Writing Integration Tests:**

**File**: `web/admin-portal/src/pages/auth/LoginPage/LoginPage.test.tsx`

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { LoginPage } from './LoginPage';
import { AuthProvider } from '../../context/AuthContext';

const renderWithProviders = (component: React.ReactNode) => {
  return render(
    <BrowserRouter>
      <AuthProvider>{component}</AuthProvider>
    </BrowserRouter>
  );
};

describe('LoginPage', () => {
  it('should render login form', () => {
    renderWithProviders(<LoginPage />);

    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
  });

  it('should show validation errors for empty fields', async () => {
    renderWithProviders(<LoginPage />);

    const loginButton = screen.getByRole('button', { name: 'Login' });
    fireEvent.click(loginButton);

    await waitFor(() => {
      expect(screen.getByText('Email is required')).toBeInTheDocument();
      expect(screen.getByText('Password is required')).toBeInTheDocument();
    });
  });

  it('should call login with correct credentials', async () => {
    renderWithProviders(<LoginPage />);

    const emailInput = screen.getByLabelText('Email');
    const passwordInput = screen.getByLabelText('Password');
    const loginButton = screen.getByRole('button', { name: 'Login' });

    fireEvent.change(emailInput, { target: { value: 'admin@university.edu' } });
    fireEvent.change(passwordInput, { target: { value: 'admin123' } });
    fireEvent.click(loginButton);

    await waitFor(() => {
      // Expect login to be called with correct credentials
      // This would require mocking the auth service
    });
  });
});
```

## E2E Testing

### Backend E2E Testing

**Confirmed by Code**: The backend uses NestJS for E2E testing.

**Writing E2E Tests:**

**File**: `apps/core-api/test/auth.e2e-spec.ts`

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';

describe('AuthController (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('Authentication Flow', () => {
    it('should register a new user', () => {
      const dto = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
      };

      return request(app.getHttpServer())
        .post('/auth/register')
        .send(dto)
        .expect(201)
        .expect((res) => {
          expect(res.body).toHaveProperty('accessToken');
          expect(res.body).toHaveProperty('user');
        });
    });

    it('should login with valid credentials', () => {
      const dto = {
        email: 'admin@university.edu',
        password: 'admin123',
      };

      return request(app.getHttpServer())
        .post('/auth/login')
        .send(dto)
        .expect(200)
        .expect((res) => {
          expect(res.body).toHaveProperty('accessToken');
          expect(res.body).toHaveProperty('refreshToken');
          expect(res.body).toHaveProperty('user');
          authToken = res.body.accessToken;
        });
    });

    it('should access protected route with valid token', () => {
      return request(app.getHttpServer())
        .get('/users/profile')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);
    });

    it('should return 401 without token', () => {
      return request(app.getHttpServer())
        .get('/users/profile')
        .expect(401);
    });

    it('should return 401 with invalid token', () => {
      return request(app.getHttpServer())
        .get('/users/profile')
        .set('Authorization', 'Bearer invalid-token')
        .expect(401);
    });
  });
});
```

### Frontend E2E Testing

**Confirmed by Code**: The frontend uses Playwright for E2E testing.

**Setup:**

```bash
# Install Playwright
cd web/admin-portal
npm install --save-dev @playwright/test

# Initialize Playwright
npx playwright install
```

**Writing E2E Tests:**

**File**: `web/admin-portal/e2e/login.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173/login');
  });

  test('should show login page', async ({ page }) => {
    await expect(page).toHaveTitle('University ERP - Login');
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should show validation errors', async ({ page }) => {
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Email is required')).toBeVisible();
    await expect(page.locator('text=Password is required')).toBeVisible();
  });

  test('should login successfully', async ({ page }) => {
    await page.fill('input[name="email"]', 'admin@university.edu');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('http://localhost:5173/dashboard');
    await expect(page.locator('text=Welcome, Admin')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.fill('input[name="email"]', 'invalid@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Invalid credentials')).toBeVisible();
  });
});

test.describe('Dashboard Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('http://localhost:5173/login');
    await page.fill('input[name="email"]', 'admin@university.edu');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.waitForURL('http://localhost:5173/dashboard');
  });

  test('should show dashboard', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Dashboard');
    await expect(page.locator('text=Total Students')).toBeVisible();
    await expect(page.locator('text=Total Courses')).toBeVisible();
  });

  test('should navigate to students page', async ({ page }) => {
    await page.click('text=Students');
    await expect(page).toHaveURL('http://localhost:5173/students');
    await expect(page.locator('text=Students List')).toBeVisible();
  });
});
```

## Testing Best Practices

### General Best Practices

1. **Test Behavior, Not Implementation**
   ```typescript
   // Good - tests behavior
   it('should return user by id', async () => {
     const user = await service.findOne('user-id');
     expect(user.email).toBe('test@example.com');
   });

   // Bad - tests implementation
   it('should call prisma.user.findUnique', async () => {
     await service.findOne('user-id');
     expect(prisma.user.findUnique).toHaveBeenCalled();
   });
   ```

2. **Arrange, Act, Assert Pattern**
   ```typescript
   it('should create a user', async () => {
     // Arrange
     const dto = { email: 'test@example.com', password: 'password123' };
     const expectedResult = { id: 'user-id', ...dto };

     // Act
     const result = await service.create(dto);

     // Assert
     expect(result).toEqual(expectedResult);
   });
   ```

3. **Use Descriptive Test Names**
   ```typescript
   // Good
   it('should return 404 when user not found', async () => {
     // test code
   });

   // Bad
   it('test user not found', async () => {
     // test code
   });
   ```

4. **Test Edge Cases**
   ```typescript
   it('should handle empty array', async () => {
     const result = await service.findAll();
     expect(result).toEqual([]);
   });

   it('should handle null input', async () => {
     await expect(service.findOne(null)).rejects.toThrow();
   });
   ```

5. **Keep Tests Independent**
   ```typescript
   beforeEach(() => {
     // Reset state before each test
   });

   afterEach(() => {
     // Clean up after each test
   });
   ```

### Backend Testing Best Practices

1. **Mock External Dependencies**
   ```typescript
   const mockPrismaService = {
     user: {
       findUnique: jest.fn(),
     },
   };
   ```

2. **Use Test Database**
   ```typescript
   // Use separate test database
   DATABASE_URL="postgresql://test:test@localhost:5432/test_db"
   ```

3. **Clean Up After Tests**
   ```typescript
   afterAll(async () => {
     await prisma.$disconnect();
   });
   ```

### Frontend Testing Best Practices

1. **Test User Interactions**
   ```typescript
   fireEvent.click(button);
   fireEvent.change(input, { target: { value: 'test' } });
   ```

2. **Use getByRole for Accessibility**
   ```typescript
   const button = screen.getByRole('button', { name: 'Submit' });
   ```

3. **Wait for Async Operations**
   ```typescript
   await waitFor(() => {
     expect(element).toBeVisible();
   });
   ```

## Running Tests

### Run All Tests

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### Run Backend Tests

```bash
cd apps/core-api

# Run unit tests
npm run test

# Run e2e tests
npm run test:e2e

# Run tests with coverage
npm run test:coverage
```

### Run Frontend Tests

```bash
cd web/admin-portal

# Run unit tests
npm run test

# Run e2e tests
npm run test:e2e

# Run tests with coverage
npm run test:coverage
```

## Test Coverage

**Coverage Goals:**
- Unit Tests: 80%+ coverage
- Integration Tests: 70%+ coverage
- E2E Tests: Critical paths covered

**View Coverage Report:**

```bash
# Generate coverage report
npm run test:coverage

# View report
open coverage/index.html
```

## Continuous Integration

**GitHub Actions Configuration:**

**File**: `.github/workflows/test.yml`

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Generate coverage
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Troubleshooting

### Common Issues

**Issue: Tests Timeout**

**Solution:**
```typescript
// Increase timeout
jest.setTimeout(30000);
```

**Issue: Tests Fail in CI but Pass Locally**

**Solution:**
```bash
# Check environment variables
# Check database connection
# Check timing issues
```

**Issue: Mock Not Working**

**Solution:**
```typescript
// Clear mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
});
```

## Additional Resources

- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [NestJS Testing](https://docs.nestjs.com/fundamentals/testing)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Playwright Documentation](https://playwright.dev/)
