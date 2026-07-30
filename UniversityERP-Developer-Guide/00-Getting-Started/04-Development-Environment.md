# Development Environment Setup

## Overview

This guide provides comprehensive instructions for setting up a complete development environment for the University ERP system. It covers IDE configuration, development tools, debugging setup, and productivity enhancements.

## IDE Setup

### Visual Studio Code

**Recommended IDE**: Visual Studio Code with extensions

**Install VS Code:**
```bash
# Download from https://code.visualstudio.com/
# Or install via package manager

# macOS
brew install --cask visual-studio-code

# Linux (Ubuntu)
sudo snap install code --classic

# Windows
# Download installer from website
```

### Recommended Extensions

**Essential Extensions:**

1. **ESLint**
   - Extension ID: `dbaeumer.vscode-eslint`
   - Purpose: JavaScript/TypeScript linting
   - Install: `code --install-extension dbaeumer.vscode-eslint`

2. **Prettier**
   - Extension ID: `esbenp.prettier-vscode`
   - Purpose: Code formatting
   - Install: `code --install-extension esbenp.prettier-vscode`

3. **Prisma**
   - Extension ID: `Prisma.prisma`
   - Purpose: Prisma ORM support
   - Install: `code --install-extension Prisma.prisma`

4. **Docker**
   - Extension ID: `ms-azuretools.vscode-docker`
   - Purpose: Docker support
   - Install: `code --install-extension ms-azuretools.vscode-docker`

5. **GitLens**
   - Extension ID: `eamodio.gitlens`
   - Purpose: Git supercharged
   - Install: `code --install-extension eamodio.gitlens`

6. **TypeScript Importer**
   - Extension ID: `pmneo.tsimporter`
   - Purpose: Auto import TypeScript modules
   - Install: `code --install-extension pmneo.tsimporter`

7. **Auto Rename Tag**
   - Extension ID: `formulahendry.auto-rename-tag`
   - Purpose: Auto rename paired HTML/XML tag
   - Install: `code --install-extension formulahendry.auto-rename-tag`

8. **Path Intellisense**
   - Extension ID: `christian-kohler.path-intellisense`
   - Purpose: Autocomplete filenames
   - Install: `code --install-extension christian-kohler.path-intellisense`

9. **NestJS Snippets**
   - Extension ID: `ambar.nestjs-snippets`
   - Purpose: NestJS code snippets
   - Install: `code --install-extension ambar.nestjs-snippets`

10. **TODO Highlight**
    - Extension ID: `wayou.vscode-todo-highlight`
    - Purpose: Highlight TODO comments
    - Install: `code --install-extension wayou.vscode-todo-highlight`

**Install All Extensions:**

```bash
# Create script to install all extensions
cat > install-extensions.sh << 'EOF'
#!/bin/bash
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension Prisma.prisma
code --install-extension ms-azuretools.vscode-docker
code --install-extension eamodio.gitlens
code --install-extension pmneo.tsimporter
code --install-extension formulahendry.auto-rename-tag
code --install-extension christian-kohler.path-intellisense
code --install-extension ambar.nestjs-snippets
code --install-extension wayou.vscode-todo-highlight
EOF

# Make script executable
chmod +x install-extensions.sh

# Run script
./install-extensions.sh
```

### VS Code Configuration

**Create `.vscode/settings.json`:**

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
    "**/.turbo": true,
    "**/coverage": true
  },
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/.next/**": true,
    "**/.turbo/**": true
  },
  "eslint.workingDirectories": [
    { "directory": "apps/core-api", "changeProcessCWD": true },
    { "directory": "web/admin-portal", "changeProcessCWD": true }
  ],
  "prisma.showPrismaStudioNotification": false
}
```

**Create `.vscode/launch.json`:**

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
      "sourceMaps": true,
      "outFiles": ["${workspaceFolder}/apps/core-api/dist/**/*.js"],
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Admin Portal",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/web/admin-portal/src",
      "sourceMaps": true
    }
  ]
}
```

**Create `.vscode/tasks.json`:**

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Core API",
      "type": "shell",
      "command": "npm",
      "args": ["run", "start:dev"],
      "options": {
        "cwd": "${workspaceFolder}/apps/core-api"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start Admin Portal",
      "type": "shell",
      "command": "npm",
      "args": ["run", "dev"],
      "options": {
        "cwd": "${workspaceFolder}/web/admin-portal"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      },
      "isBackground": true,
      "problemMatcher": []
    },
    {
      "label": "Start Docker Services",
      "type": "shell",
      "command": "docker-compose",
      "args": ["up", "-d"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Run Database Migrations",
      "type": "shell",
      "command": "npx",
      "args": ["prisma", "migrate", "dev"],
      "options": {
        "cwd": "${workspaceFolder}/apps/core-api"
      },
      "group": "build",
      "presentation": {
        "reveal": "always"
      }
    }
  ]
}
```

## Git Configuration

### Git Setup

**Configure Git:**

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set default push behavior
git config --global push.autoSetupRemote true

# Enable credential helper
git config --global credential.helper store

# Set line endings to LF (recommended for cross-platform)
git config --global core.autocrlf input
```

### Git Hooks

**Install Husky for Git hooks:**

```bash
# Install Husky
npm install --save-dev husky

# Initialize Husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint"

# Add commit-msg hook
npx husky add .husky/commit-msg 'npx commitlint --edit $1'
```

**Create `.husky/pre-commit`:**

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint
npm run type-check
```

**Create `.husky/commit-msg`:**

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx commitlint --edit $1
```

### Git Ignore

**Create `.gitignore`:**

```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output/

# Production
dist/
build/
.next/
.turbo/

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env
.env*.local
.env.development
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
Thumbs.db

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Prisma
prisma/migrations/**/migration.sql

# Docker
docker-compose.override.yml
```

## Development Tools

### API Testing Tools

**Postman:**

```bash
# Download Postman from https://www.postman.com/downloads/
# Or install via Snap (Linux)
sudo snap install postman
```

**Insomnia:**

```bash
# Download Insomnia from https://insomnia.rest/download
# Or install via Snap (Linux)
sudo snap install insomnia
```

### Database Tools

**DBeaver:**

```bash
# Download DBeaver from https://dbeaver.io/download/
# Or install via package manager

# macOS
brew install --cask dbeaver-community

# Linux (Ubuntu)
sudo snap install dbeaver-ce

# Windows
# Download installer from website
```

**pgAdmin:**

```bash
# Download pgAdmin from https://www.pgadmin.org/download/
# Or install via package manager

# macOS
brew install --cask pgadmin4

# Linux (Ubuntu)
sudo apt install pgadmin4

# Windows
# Download installer from website
```

### Redis Tools

**Redis Commander:**

```bash
# Install Redis Commander
npm install -g redis-commander

# Start Redis Commander
redis-commander

# Access at http://localhost:8081
```

**Another Redis Desktop Manager:**

```bash
# Download from https://github.com/qishibo/AnotherRedisDesktopManager/releases
# Install based on your OS
```

### Docker Tools

**Docker Desktop:**

```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
# Install based on your OS
```

## Debugging Setup

### Backend Debugging

**Debug NestJS Application:**

1. Open VS Code
2. Press `F5` or go to Run and Debug
3. Select "Debug Core API"
4. Set breakpoints in your code
5. Start debugging

**Debug with Chrome DevTools:**

```bash
# Start with debug mode
cd apps/core-api
npm run start:debug
```

**Debug with Node Inspector:**

```bash
# Install node inspector
npm install -g node-inspector

# Start with inspect flag
node --inspect-brk dist/main.js
```

### Frontend Debugging

**Debug React Application:**

1. Open VS Code
2. Press `F5` or go to Run and Debug
3. Select "Debug Admin Portal"
4. Set breakpoints in your code
5. Start debugging

**Debug with Chrome DevTools:**

```bash
# Start dev server
cd web/admin-portal
npm run dev

# Open Chrome DevTools
# Press F12 in Chrome
# Go to Sources tab
# Set breakpoints
```

### Database Debugging

**Debug with Prisma Studio:**

```bash
cd apps/core-api
npx prisma studio
```

**Debug with DBeaver:**

1. Open DBeaver
2. Create new connection
3. Select PostgreSQL
4. Enter connection details:
   - Host: localhost
   - Port: 5432
   - Database: university_erp
   - Username: postgres
   - Password: postgres
5. Connect and explore database

### Redis Debugging

**Debug with Redis CLI:**

```bash
# Connect to Redis
redis-cli

# Monitor commands
MONITOR

# Check keys
KEYS *

# Check value
GET key_name

# Exit
exit
```

**Debug with Redis Commander:**

```bash
# Start Redis Commander
redis-commander

# Access at http://localhost:8081
```

## Productivity Enhancements

### Shell Aliases

**Create shell aliases for common commands:**

```bash
# Add to ~/.bashrc or ~/.zshrc

# University ERP aliases
alias uerp-start='cd ~/UniversityERP && docker-compose up -d'
alias uerp-stop='cd ~/UniversityERP && docker-compose down'
alias uerp-logs='cd ~/UniversityERP && docker-compose logs -f'
alias uerp-api='cd ~/UniversityERP/apps/core-api && npm run start:dev'
alias uerp-portal='cd ~/UniversityERP/web/admin-portal && npm run dev'
alias uerp-migrate='cd ~/UniversityERP/apps/core-api && npx prisma migrate dev'
alias uerp-seed='cd ~/UniversityERP/apps/core-api && npx prisma db seed'
alias uerp-studio='cd ~/UniversityERP/apps/core-api && npx prisma studio'
alias uerp-test='cd ~/UniversityERP && npm test'
alias uerp-lint='cd ~/UniversityERP && npm run lint'
alias uerp-build='cd ~/UniversityERP && npm run build'

# Reload shell
source ~/.bashrc
# or
source ~/.zshrc
```

### NPM Scripts

**Add useful npm scripts to `package.json`:**

```json
{
  "scripts": {
    "dev": "concurrently \"npm run dev:api\" \"npm run dev:portal\"",
    "dev:api": "npm run start:dev --workspace=apps/core-api",
    "dev:portal": "npm run dev --workspace=web/admin-portal",
    "dev:all": "concurrently \"npm run dev:api\" \"npm run dev:portal\" \"npm run dev:worker\"",
    "lint": "turbo run lint",
    "lint:fix": "turbo run lint:fix",
    "type-check": "turbo run type-check",
    "test": "turbo run test",
    "test:watch": "turbo run test:watch",
    "test:coverage": "turbo run test:coverage",
    "clean": "turbo run clean && rm -rf node_modules",
    "clean:install": "npm run clean && npm install",
    "db:migrate": "npx prisma migrate dev --workspace=apps/core-api",
    "db:seed": "npx prisma db seed --workspace=apps/core-api",
    "db:reset": "npx prisma migrate reset --workspace=apps/core-api",
    "db:studio": "npx prisma studio --workspace=apps/core-api"
  }
}
```

### VS Code Workspaces

**Create VS Code workspace:**

**File**: `UniversityERP.code-workspace`

```json
{
  "folders": [
    {
      "path": "./apps/core-api",
      "name": "Core API"
    },
    {
      "path": "./web/admin-portal",
      "name": "Admin Portal"
    },
    {
      "path": "./libs",
      "name": "Shared Libraries"
    }
  ],
  "settings": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "typescript.tsdk": "node_modules/typescript/lib"
  }
}
```

## Environment-Specific Configuration

### Development Environment

**Development `.env` configuration:**

```env
# Database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/university_erp?schema=public"

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT
JWT_SECRET=dev-secret-key-change-in-production
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=7d

# MinIO
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_USE_SSL=false

# App
PORT=3000
NODE_ENV=development

# CORS
CORS_ORIGIN=http://localhost:5173

# Logging
LOG_LEVEL=debug

# Email (optional - use mailhog for development)
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=noreply@university.edu
```

### Staging Environment

**Staging `.env.staging` configuration:**

```env
# Database
DATABASE_URL="postgresql://user:password@staging-db.example.com:5432/university_erp_staging?schema=public"

# Redis
REDIS_HOST=staging-redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=staging-redis-password

# JWT
JWT_SECRET=staging-secret-key
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=7d

# MinIO
MINIO_ENDPOINT=staging-minio.example.com
MINIO_PORT=9000
MINIO_ACCESS_KEY=staging-access-key
MINIO_SECRET_KEY=staging-secret-key
MINIO_USE_SSL=true

# App
PORT=3000
NODE_ENV=staging

# CORS
CORS_ORIGIN=https://staging.university.edu

# Logging
LOG_LEVEL=info

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=staging@example.com
SMTP_PASSWORD=staging-password
SMTP_FROM=noreply@university.edu
```

### Production Environment

**Production `.env.production` configuration:**

```env
# Database
DATABASE_URL="postgresql://user:password@prod-db.example.com:5432/university_erp?schema=public&connection_limit=20&pool_timeout=30"

# Redis
REDIS_HOST=prod-redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=prod-redis-password
REDIS_CLUSTER_MODE=true

# JWT
JWT_SECRET=prod-secret-key-use-strong-random-string
JWT_EXPIRES_IN=1h
REFRESH_TOKEN_EXPIRES_IN=7d

# MinIO
MINIO_ENDPOINT=prod-minio.example.com
MINIO_PORT=9000
MINIO_ACCESS_KEY=prod-access-key
MINIO_SECRET_KEY=prod-secret-key
MINIO_USE_SSL=true

# App
PORT=3000
NODE_ENV=production

# CORS
CORS_ORIGIN=https://university.edu

# Logging
LOG_LEVEL=error

# Email
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=prod@example.com
SMTP_PASSWORD=prod-password
SMTP_FROM=noreply@university.edu
```

## Verification

### Verify Development Environment

**Verify all tools are installed:**

```bash
# Verify Node.js
node --version

# Verify npm
npm --version

# Verify Docker
docker --version

# Verify Docker Compose
docker-compose --version

# Verify Git
git --version

# Verify VS Code extensions
code --list-extensions

# Verify Redis CLI
redis-cli --version

# Verify Prisma
npx prisma --version
```

### Verify Development Setup

**Verify development setup:**

```bash
# Start Docker services
docker-compose up -d

# Verify services are running
docker-compose ps

# Run database migrations
cd apps/core-api
npx prisma migrate dev

# Seed database
npx prisma db seed

# Start Core API
npm run start:dev

# Start Admin Portal (new terminal)
cd ../../web/admin-portal
npm run dev

# Test API
curl http://localhost:3000/health

# Test Frontend
# Open http://localhost:5173 in browser
```

## Troubleshooting

### Common Issues

**Issue: VS Code extensions not working**

**Solution:**
```bash
# Reload VS Code
# Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux)
# Type "Reload Window"
# Press Enter
```

**Issue: Git hooks not running**

**Solution:**
```bash
# Reinstall Husky
npm install --save-dev husky
npx husky install

# Make hooks executable
chmod +x .husky/pre-commit
chmod +x .husky/commit-msg
```

**Issue: Docker services not starting**

**Solution:**
```bash
# Restart Docker
# Linux
sudo systemctl restart docker

# macOS/Windows
# Restart Docker Desktop

# Re-start services
docker-compose down
docker-compose up -d
```

## Next Steps

After setting up the development environment:

1. **Explore the Codebase**: Start exploring the codebase
2. **Read Architecture Documentation**: Understand the system architecture
3. **Start Development**: Start building features
4. **Contribute**: Contribute to the project

## Additional Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Git Documentation](https://git-scm.com/doc)
- [Docker Documentation](https://docs.docker.com/)
- [NestJS Documentation](https://docs.nestjs.com/)
- [React Documentation](https://react.dev/)
- [Prisma Documentation](https://www.prisma.io/docs)
