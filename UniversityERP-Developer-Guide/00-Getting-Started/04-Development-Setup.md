# Development Setup

## Purpose

This document provides detailed instructions for setting up a complete development environment for the University ERP system. This includes IDE configuration, tooling setup, and development workflow.

## Why This Document Exists

**Confirmed by Code**: The University ERP is a complex monorepo with multiple services. A proper development environment requires:
- IDE configuration for TypeScript and NestJS
- Git workflow setup
- Debugging configuration
- Linting and formatting setup
- Hot-reload configuration

Without proper setup, development will be inefficient and error-prone.

## Where This Is Used

- **Onboarding**: New developers set up their IDE
- **Environment Reset**: Re-configure after IDE changes
- **Team Standardization**: Ensure consistent development environment
- **Troubleshooting**: IDE-related issues

## Prerequisites

**Required**: Complete [02-Installation.md](./02-Installation.md) before proceeding.

**Verification**:
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Docker services running
- [ ] Database migrated
- [ ] Database seeded

## IDE Setup

### VS Code (Recommended)

**Confirmed by Code**: Project uses TypeScript, NestJS, React.

**Installation**:
1. Download VS Code from https://code.visualstudio.com/
2. Install recommended extensions

**Recommended Extensions**:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "prisma.prisma",
    "ms-azuretools.vscode-docker",
    "eamodio.gitlens",
    "Vue.volar",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "firsttris.vscode-jest-runner",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

**Extension Details**:

1. **ESLint** (dbaeumer.vscode-eslint)
   - Purpose: JavaScript/TypeScript linting
   - Why: Enforces code quality and consistency
   - Configuration: .eslintrc.js in project root

2. **Prettier** (esbenp.prettier-vscode)
   - Purpose: Code formatting
   - Why: Consistent code style across team
   - Configuration: .prettierrc in project root

3. **Prisma** (prisma.prisma)
   - Purpose: Prisma schema highlighting and autocomplete
   - Why: Better database schema editing experience
   - Configuration: Auto-detects schema.prisma

4. **Docker** (ms-azuretools.vscode-docker)
   - Purpose: Docker container management
   - Why: Easy Docker service management
   - Configuration: Auto-detects docker-compose.yml

5. **GitLens** (eamodio.gitlens)
   - Purpose: Git supercharged
   - Why: Better Git integration and blame
   - Configuration: Works out of the box

6. **Volar** (Vue.volar)
   - Purpose: Vue 3 language support
   - Why: Better Vue/React support (React uses similar features)
   - Configuration: Auto-detects Vue/React files

7. **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
   - Purpose: Tailwind CSS autocomplete
   - Why: Better CSS class completion
   - Configuration: Auto-detects tailwind.config.js

8. **TypeScript** (ms-vscode.vscode-typescript-next)
   - Purpose: Latest TypeScript features
   - Why: Better TypeScript support
   - Configuration: Uses workspace TypeScript version

9. **Jest Runner** (firsttris.vscode-jest-runner)
   - Purpose: Run Jest tests from VS Code
   - Why: Easy test execution
   - Configuration: Auto-detects Jest config

10. **Code Spell Checker** (streetsidesoftware.code-spell-checker)
    - Purpose: Spell checking in code
    - Why: Catch typos in comments and strings
    - Configuration: Add technical terms to ignore

**VS Code Settings**:

Create `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "files.eol": "\n",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true,
    "**/.turbo": true
  }
}
```

**VS Code Workspace Settings**:

Create `.vscode/settings.json` in project root:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "eslint.workingDirectories": [
    { "directory": "apps/core-api", "changeProcessCWD": true },
    { "directory": "web/admin-portal", "changeProcessCWD": true }
  ]
}
```

**VS Code Launch Configuration**:

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Core API",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start:debug"],
      "cwd": "${workspaceFolder}/apps/core-api",
      "console": "integratedTerminal",
      "restart": true,
      "protocol": "inspector"
    },
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Admin Portal",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/web/admin-portal/src"
    }
  ]
}
```

### WebStorm (Alternative)

**Installation**:
1. Download WebStorm from https://www.jetbrains.com/webstorm/
2. Install Node.js plugin
3. Configure Node.js interpreter

**Configuration**:
- Set Node.js interpreter to project's Node.js version
- Enable ESLint
- Enable Prettier
- Configure TypeScript service
- Configure Jest

## Git Workflow Setup

### Git Configuration

**Confirmed by Code**: Repository uses Git for version control.

**Action**:
```bash
# Configure Git user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Configure line endings
git config --global core.autocrlf input  # Linux/macOS
git config --global core.autocrlf true   # Windows

# Configure default branch
git config --global init.defaultBranch main

# Configure rebase
git config --global pull.rebase true
```

### Git Hooks

**Status**: Not implemented

**Proposal**: Use Husky for Git hooks:

```bash
npm install husky --save-dev
npx husky install
npx husky add .husky/pre-commit "npm run lint"
npx husky add .husky/pre-commit "npm run format:check"
```

### Git Branching Strategy

**Recommended**: Git Flow or GitHub Flow

**GitHub Flow** (simpler):
- `main`: Production branch
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `hotfix/*`: Hotfix branches

**Example**:
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
# Merge to develop
```

## Linting and Formatting

### ESLint

**Confirmed by Code**: ESLint is configured in project.

**Configuration**: `.eslintrc.js` in project root

**Run Linting**:
```bash
# Lint all files
npm run lint

# Lint specific package
cd apps/core-api
npm run lint

# Fix linting issues
npm run lint:fix
```

**ESLint Rules**:
- TypeScript strict mode
- NestJS specific rules
- React specific rules
- Import order rules

### Prettier

**Confirmed by Code**: Prettier is configured in project.

**Configuration**: `.prettierrc` in project root

**Run Formatting**:
```bash
# Format all files
npm run format

# Format specific package
cd apps/core-api
npm run format

# Check formatting
npm run format:check
```

**Prettier Rules**:
- Single quotes
- 2 space indentation
- Trailing commas
- Semicolons

## Debugging Setup

### Backend Debugging

**Confirmed by Code**: NestJS supports debugging.

**VS Code Debugging**:
1. Open `.vscode/launch.json` (created above)
2. Select "Debug Core API" configuration
3. Press F5 to start debugging
4. Set breakpoints in code
5. Make requests to API
6. Debug execution

**Chrome DevTools Debugging**:
```bash
# Start with debug mode
cd apps/core-api
npm run start:debug
```

Then open Chrome DevTools and connect to Node.js debugger.

### Frontend Debugging

**Confirmed by Code**: React/Vite supports debugging.

**VS Code Debugging**:
1. Open `.vscode/launch.json` (created above)
2. Select "Debug Admin Portal" configuration
3. Press F5 to start debugging
4. Set breakpoints in code
5. Interact with application
6. Debug execution

**Chrome DevTools**:
1. Open http://localhost:5173
2. Press F12 to open DevTools
3. Use Sources panel for debugging
4. Use React DevTools for React debugging

### Database Debugging

**Tools**:
- **DBeaver**: GUI for database
- **pgAdmin**: PostgreSQL GUI
- **Command line**: psql

**Connect to Database**:
```bash
# Using Docker exec
docker-compose exec postgres psql -U postgres -d university_erp

# Using local client
psql -h localhost -U postgres -d university_erp
```

**Common Queries**:
```sql
-- List tables
\dt

-- Describe table
\d "User"

-- Run query
SELECT * FROM "User" LIMIT 10;

-- Exit
\q
```

### Redis Debugging

**Tools**:
- **Redis Commander**: GUI for Redis
- **Command line**: redis-cli

**Connect to Redis**:
```bash
# Using Docker exec
docker-compose exec redis redis-cli

# Using local client
redis-cli -h localhost -p 6379
```

**Common Commands**:
```bash
# Ping
PING

# Get value
GET key

# Set value
SET key value

# List keys
KEYS *

# Flush all (WARNING: deletes all data)
FLUSHALL

# Exit
EXIT
```

## Hot Reload Configuration

### Backend Hot Reload

**Confirmed by Code**: NestJS has hot-reload enabled.

**Configuration**: `start:dev` script in package.json

**How It Works**:
- File changes trigger rebuild
- Server restarts automatically
- Maintains state where possible

**Usage**:
```bash
cd apps/core-api
npm run start:dev
```

### Frontend Hot Reload

**Confirmed by Code**: Vite has hot-reload enabled.

**Configuration**: Vite default behavior

**How It Works**:
- File changes trigger rebuild
- Browser updates automatically
- Maintains component state

**Usage**:
```bash
cd web/admin-portal
npm run dev
```

## Testing Setup

### Jest Configuration

**Confirmed by Code**: Jest is configured for testing.

**Run Tests**:
```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- auth.service.spec.ts
```

**Test Structure**:
```
apps/core-api/src/
├── modules/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   └── auth.service.spec.ts  # Test file
```

### E2E Testing

**Status**: Not implemented

**Proposal**: Use Playwright or Cypress for E2E testing:

```bash
npm install -D @playwright/test
npx playwright install
```

## Development Workflow

### Typical Development Day

1. **Start Services**:
   ```bash
   docker-compose up -d
   ```

2. **Pull Latest Changes**:
   ```bash
   git pull origin main
   npm install
   ```

3. **Run Migrations** (if needed):
   ```bash
   cd apps/core-api
   npx prisma migrate dev
   cd ../..
   ```

4. **Start Backend**:
   ```bash
   cd apps/core-api
   npm run start:dev
   ```

5. **Start Frontend** (new terminal):
   ```bash
   cd web/admin-portal
   npm run dev
   ```

6. **Develop**:
   - Make changes
   - Hot-reload applies changes
   - Debug as needed

7. **Test**:
   ```bash
   npm test
   ```

8. **Lint and Format**:
   ```bash
   npm run lint
   npm run format
   ```

9. **Commit**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

10. **Stop Services**:
    ```bash
    docker-compose down
    ```

### Code Review Process

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Make Changes**:
   - Write code
   - Write tests
   - Update documentation

3. **Run Checks**:
   ```bash
   npm run lint
   npm run format
   npm test
   npm run build
   ```

4. **Commit**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push**:
   ```bash
   git push origin feature/new-feature
   ```

6. **Create Pull Request**:
   - Describe changes
   - Link to issue
   - Request review

7. **Address Feedback**:
   - Make changes
   - Re-run checks
   - Push updates

8. **Merge**:
   - Merge to main/develop
   - Delete feature branch

## Performance Optimization

### Build Performance

**Turbo** (Confirmed by Code):
- Monorepo build system
- Caches build artifacts
- Parallel builds

**Usage**:
```bash
# Build all packages
npm run build

# Build specific package
npm run build -- --filter=core-api
```

### Development Performance

**Tips**:
- Use SSD for faster file operations
- Allocate sufficient RAM to Docker
- Close unused applications
- Use hot-reload instead of full rebuilds

## Common Issues

### Issue 1: VS Code Not Using Workspace TypeScript

**Symptom**: TypeScript errors despite correct code

**Cause**: VS Code using global TypeScript instead of workspace

**Fix**:
```json
// .vscode/settings.json
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

### Issue 2: Hot Reload Not Working

**Symptom**: Changes not reflected without manual restart

**Cause**: File watcher limits or configuration issues

**Fix**:
```bash
# Increase file watcher limits (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Restart services
```

### Issue 3: Linting Errors on Save

**Symptom**: ESLint errors on every save

**Cause**: ESLint configuration or code style issues

**Fix**:
```bash
# Auto-fix linting issues
npm run lint:fix

# Check ESLint configuration
cat .eslintrc.js
```

### Issue 4: Debugging Breakpoints Not Hit

**Symptom**: Breakpoints not triggering during debugging

**Cause**: Incorrect source map configuration

**Fix**:
```bash
# Ensure source maps are enabled
# Check tsconfig.json for "sourceMap": true

# Rebuild
npm run build
```

## Future Enhancements

### Pre-commit Hooks

**Status**: Not implemented

**Proposal**: Use Husky for pre-commit hooks:
- Run linting
- Run formatting check
- Run tests
- Prevent bad commits

### Commit Linting

**Status**: Not implemented

**Proposal**: Use commitlint for commit message linting:
- Enforce conventional commits
- Consistent commit messages
- Better changelog generation

### Automated Testing

**Status**: Not implemented

**Proposal**: Run tests automatically on:
- Pre-commit
- Pre-push
- CI/CD pipeline

## Production Considerations

### Development vs Production

**Development**:
- Hot-reload enabled
- Source maps enabled
- Detailed logging
- Swagger docs enabled
- Debugging enabled

**Production**:
- No hot-reload
- No source maps
- Minimal logging
- Swagger docs disabled
- Debugging disabled

### Production Build

```bash
# Build for production
npm run build

# Start production server
cd apps/core-api
npm run start:prod
```

## Related Documentation

- [01-Prerequisites.md](./01-Prerequisites.md) - Prerequisites
- [02-Installation.md](./02-Installation.md) - Installation
- [05-Database-Setup.md](./05-Database-Setup.md) - Database setup
- [06-Testing-Setup.md](./06-Testing-Setup.md) - Testing setup
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
