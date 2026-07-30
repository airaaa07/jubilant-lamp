# Contributing Guide

## Overview

This guide provides comprehensive instructions for contributing to the University ERP project. It covers the contribution workflow, coding standards, testing requirements, and pull request process.

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Read the [Installation Guide](./01-Installation.md)
- Read the [Development Environment Setup](./04-Development-Environment.md)
- Read the [Project Structure](./05-Project-Structure.md)
- Set up your local development environment
- Familiarized yourself with the codebase

### Contribution Workflow

**Confirmed by Code**: The project uses Git for version control with a feature branch workflow.

**Workflow Steps:**

1. **Fork the Repository**
   ```bash
   # Fork the repository on GitHub
   # Clone your fork
   git clone https://github.com/your-username/UniversityERP.git
   cd UniversityERP
   ```

2. **Add Upstream Remote**
   ```bash
   # Add upstream remote
   git remote add upstream https://github.com/original-org/UniversityERP.git
   
   # Verify remotes
   git remote -v
   ```

3. **Create Feature Branch**
   ```bash
   # Sync with upstream
   git fetch upstream
   git checkout main
   git merge upstream/main
   
   # Create feature branch
   git checkout -b feature/your-feature-name
   ```

4. **Make Changes**
   ```bash
   # Make your changes
   # Follow coding standards
   # Write tests
   # Update documentation
   ```

5. **Commit Changes**
   ```bash
   # Stage changes
   git add .
   
   # Commit with conventional commit message
   git commit -m "feat: add user authentication"
   ```

6. **Push Changes**
   ```bash
   # Push to your fork
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in PR template
   - Submit PR

## Coding Standards

### TypeScript Standards

**Confirmed by Code**: The project uses TypeScript with strict type checking.

**TypeScript Configuration:**

```typescript
// Use strict type checking
// Enable all strict type checking options
// Use explicit types for function parameters
// Use explicit return types for functions

// Good
function calculateTotal(price: number, quantity: number): number {
  return price * quantity;
}

// Bad
function calculateTotal(price, quantity) {
  return price * quantity;
}
```

**TypeScript Best Practices:**

1. **Use Interfaces for Object Shapes**
   ```typescript
   // Good
   interface User {
     id: string;
     name: string;
     email: string;
   }
   
   // Bad
   type User = {
     id: string;
     name: string;
     email: string;
   };
   ```

2. **Use Type Aliases for Union Types**
   ```typescript
   // Good
   type Status = 'pending' | 'approved' | 'rejected';
   
   // Bad
   interface Status {
     value: 'pending' | 'approved' | 'rejected';
   }
   ```

3. **Use Enums for Fixed Sets**
   ```typescript
   // Good
   enum Role {
     ADMIN = 'ADMIN',
     STAFF = 'STAFF',
     STUDENT = 'STUDENT',
   }
   
   // Bad
   const Role = {
     ADMIN: 'ADMIN',
     STAFF: 'STAFF',
     STUDENT: 'STUDENT',
   };
   ```

### NestJS Standards

**Confirmed by Code**: The backend uses NestJS framework.

**NestJS Best Practices:**

1. **Module Organization**
   ```typescript
   // Each feature should be in its own module
   // Module should contain: controller, service, dto, entity
   
   @Module({
     imports: [PrismaModule],
     controllers: [UsersController],
     providers: [UsersService],
     exports: [UsersService],
   })
   export class UsersModule {}
   ```

2. **DTO Validation**
   ```typescript
   // Use class-validator for DTO validation
   import { IsEmail, IsNotEmpty, MinLength } from 'class-validator';
   
   export class CreateUserDto {
     @IsEmail()
     email: string;
     
     @IsNotEmpty()
     @MinLength(8)
     password: string;
   }
   ```

3. **Service Layer**
   ```typescript
   // Business logic should be in service layer
   // Controllers should only handle HTTP concerns
   @Injectable()
   export class UsersService {
     constructor(private prisma: PrismaService) {}
     
     async create(dto: CreateUserDto): Promise<User> {
       // Business logic here
       return this.prisma.user.create({ data: dto });
     }
   }
   ```

### React Standards

**Confirmed by Code**: The frontend uses React with TypeScript.

**React Best Practices:**

1. **Component Structure**
   ```typescript
   // Use functional components with hooks
   // Use TypeScript for props
   // Keep components small and focused
   
   interface ButtonProps {
     label: string;
     onClick: () => void;
     disabled?: boolean;
   }
   
   export const Button: React.FC<ButtonProps> = ({
     label,
     onClick,
     disabled = false,
   }) => {
     return (
       <button onClick={onClick} disabled={disabled}>
         {label}
       </button>
     );
   };
   ```

2. **Custom Hooks**
   ```typescript
   // Use custom hooks for reusable logic
   // Prefix hooks with "use"
   // Return consistent structure
   
   export const useAuth = () => {
     const [user, setUser] = useState<User | null>(null);
     const [loading, setLoading] = useState(true);
     
     useEffect(() => {
       // Fetch user
     }, []);
     
     return { user, loading };
   };
   ```

3. **State Management**
   ```typescript
   // Use Context API for global state
   // Use local state for component-specific state
   // Use Redux/Zustand for complex state
   
   // Good: Context for auth
   const AuthContext = createContext<AuthContextType | null>(null);
   
   // Good: Local state for form
   const [formData, setFormData] = useState<FormData>({});
   ```

### Code Style

**ESLint Configuration:**

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:prettier/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "no-console": "warn"
  }
}
```

**Prettier Configuration:**

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

## Testing Standards

### Unit Testing

**Confirmed by Code**: The project uses Jest for unit testing.

**Unit Testing Best Practices:**

1. **Test Structure**
   ```typescript
   // Arrange, Act, Assert pattern
   describe('UsersService', () => {
     describe('create', () => {
       it('should create a user', async () => {
         // Arrange
         const dto: CreateUserDto = {
           email: 'test@example.com',
           password: 'password123',
           name: 'Test User',
         };
         
         // Act
         const result = await usersService.create(dto);
         
         // Assert
         expect(result).toBeDefined();
         expect(result.email).toBe(dto.email);
       });
     });
   });
   ```

2. **Mocking**
   ```typescript
   // Mock external dependencies
   jest.mock('@prisma/client');
   
   describe('UsersService', () => {
     let service: UsersService;
     let prisma: PrismaService;
     
     beforeEach(() => {
       prisma = new PrismaService();
       service = new UsersService(prisma);
     });
     
     afterEach(() => {
       jest.clearAllMocks();
     });
   });
   ```

### Integration Testing

**Integration Testing Best Practices:**

```typescript
// Use test database for integration tests
// Clean up after each test
// Test actual database operations

describe('UsersController (e2e)', () => {
  let app: INestApplication;
  
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
  
  it('/users (POST)', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ email: 'test@example.com', password: 'password123' })
      .expect(201);
  });
});
```

### E2E Testing

**E2E Testing Best Practices:**

```typescript
// Use Playwright or Cypress for E2E testing
// Test critical user flows
// Keep tests independent

import { test, expect } from '@playwright/test';

test('user login flow', async ({ page }) => {
  await page.goto('http://localhost:5173/login');
  await page.fill('input[name="email"]', 'admin@university.edu');
  await page.fill('input[name="password"]', 'admin123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('http://localhost:5173/dashboard');
});
```

## Documentation Standards

### Code Documentation

**JSDoc Comments:**

```typescript
/**
 * Creates a new user
 * @param dto - User creation data
 * @returns Created user
 * @throws ConflictException if email already exists
 */
async create(dto: CreateUserDto): Promise<User> {
  const existingUser = await this.prisma.user.findUnique({
    where: { email: dto.email },
  });
  
  if (existingUser) {
    throw new ConflictException('Email already exists');
  }
  
  return this.prisma.user.create({ data: dto });
}
```

### README Standards

**Module README:**

```markdown
# Users Module

## Purpose
Manages user accounts and authentication.

## API Endpoints
- POST /users - Create user
- GET /users - List users
- GET /users/:id - Get user
- PUT /users/:id - Update user
- DELETE /users/:id - Delete user

## Usage
\`\`\`typescript
import { UsersService } from './users.service';

const usersService = new UsersService(prisma);
const user = await usersService.create(dto);
\`\`\`
```

## Commit Message Standards

**Conventional Commits:**

```bash
# Format: <type>(<scope>): <subject>

# Types
feat: New feature
fix: Bug fix
docs: Documentation changes
style: Code style changes (formatting, etc.)
refactor: Code refactoring
test: Test changes
chore: Build process or auxiliary tool changes

# Examples
feat(auth): add JWT authentication
fix(users): fix email validation bug
docs(readme): update installation instructions
style(format): format code with prettier
refactor(auth): simplify auth logic
test(users): add user service tests
chore(deps): update dependencies
```

## Pull Request Standards

### PR Template

**Title:** `[type]: brief description`

**Description:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] All tests passing

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed the code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings generated
- [ ] Added/updated tests
- [ ] All tests passing
```

### PR Review Process

**Review Checklist:**

1. **Code Quality**
   - Code is readable and maintainable
   - Follows coding standards
   - No code duplication
   - Proper error handling

2. **Testing**
   - Tests are comprehensive
   - Tests are passing
   - Edge cases are covered
   - No flaky tests

3. **Documentation**
   - Code is documented
   - README is updated
   - API documentation is updated
   - Changes are reflected in docs

4. **Performance**
   - No performance regression
   - Efficient algorithms
   - Proper caching
   - Database optimization

5. **Security**
   - No security vulnerabilities
   - Proper input validation
   - Proper authentication/authorization
   - No sensitive data in code

## Code Review Guidelines

### Giving Feedback

**Constructive Feedback:**

```markdown
## Feedback

### Positive
- Good implementation of X
- Clean code structure
- Comprehensive tests

### Suggestions
- Consider using Y instead of X for better performance
- Add error handling for edge case Z
- Extract this logic into a separate function

### Issues
- Bug in line 123: null reference possible
- Missing validation for user input
- Security issue: SQL injection vulnerability
```

### Receiving Feedback

**Handling Feedback:**

1. **Listen and Understand**
   - Read feedback carefully
   - Ask clarifying questions if needed
   - Understand the context

2. **Respond Politely**
   - Acknowledge feedback
   - Explain your reasoning if you disagree
   - Be open to suggestions

3. **Make Changes**
   - Implement requested changes
   - Update tests
   - Update documentation

4. **Follow Up**
   - Notify reviewer of changes
   - Request re-review
   - Close discussion when resolved

## Release Process

### Versioning

**Semantic Versioning:**

```bash
# Format: MAJOR.MINOR.PATCH

# MAJOR: Breaking changes
# MINOR: New features (backwards compatible)
# PATCH: Bug fixes (backwards compatible)

# Examples
1.0.0 -> 1.0.1 (Bug fix)
1.0.1 -> 1.1.0 (New feature)
1.1.0 -> 2.0.0 (Breaking change)
```

### Changelog

**Changelog Format:**

```markdown
# Changelog

## [1.0.0] - 2024-01-01

### Added
- User authentication
- User management
- Role-based access control

### Changed
- Updated dependencies
- Improved performance

### Fixed
- Fixed email validation bug
- Fixed memory leak

### Removed
- Removed deprecated API endpoints
```

## Getting Help

### Resources

- [Project README](../../README.md)
- [Documentation](../README.md)
- [Issues](https://github.com/org/UniversityERP/issues)
- [Discussions](https://github.com/org/UniversityERP/discussions)

### Contact

- **Maintainers**: List of maintainers
- **Email**: dev@university.edu
- **Slack**: #university-erp-dev

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project website

## License

By contributing, you agree that your contributions will be licensed under the project's license.
