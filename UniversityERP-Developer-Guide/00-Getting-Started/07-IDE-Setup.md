# IDE Setup

## Purpose

This document provides detailed instructions for setting up Integrated Development Environments (IDEs) for the University ERP system. This includes VS Code, WebStorm, and other popular IDEs.

## Why This Document Exists

**Confirmed by Code**: The University ERP is a complex TypeScript monorepo with NestJS backend and React frontend. Proper IDE setup is critical for:
- Type safety and autocomplete
- Debugging capabilities
- Code formatting and linting
- Git integration
- Productivity

Without proper IDE setup, development will be inefficient and error-prone.

## Where This Is Used

- **Onboarding**: New developers set up their IDE
- **Environment Reset**: Re-configure after IDE changes
- **Team Standardization**: Ensure consistent development environment
- **Troubleshooting**: IDE-related issues

## VS Code Setup

### Installation

**Download**: https://code.visualstudio.com/

**Install**:
- Download installer for your OS
- Run installer
- Follow installation wizard

### Recommended Extensions

**Confirmed by Code**: Project uses TypeScript, NestJS, React, Prisma, Docker.

**Install Extensions**:
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search and install each extension

**Extension List**:

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
    "streetsidesoftware.code-spell-checker",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense",
    "usernamehw.errorlens",
    "wix.vscode-import-cost",
    "oderwat.indent-rainbow",
    "visualstudioexptteam.vscodeintellicode"
  ]
}
```

**Extension Details**:

1. **ESLint** (dbaeumer.vscode-eslint)
   - **Purpose**: JavaScript/TypeScript linting
   - **Why**: Enforces code quality and consistency
   - **Configuration**: Auto-detects .eslintrc.js

2. **Prettier** (esbenp.prettier-vscode)
   - **Purpose**: Code formatting
   - **Why**: Consistent code style across team
   - **Configuration**: Auto-detects .prettierrc

3. **Prisma** (prisma.prisma)
   - **Purpose**: Prisma schema highlighting and autocomplete
   - **Why**: Better database schema editing experience
   - **Configuration**: Auto-detects schema.prisma

4. **Docker** (ms-azuretools.vscode-docker)
   - **Purpose**: Docker container management
   - **Why**: Easy Docker service management
   - **Configuration**: Auto-detects docker-compose.yml

5. **GitLens** (eamodio.gitlens)
   - **Purpose**: Git supercharged
   - **Why**: Better Git integration and blame
   - **Configuration**: Works out of the box

6. **Volar** (Vue.volar)
   - **Purpose**: Vue 3 language support
   - **Why**: Better Vue/React support
   - **Configuration**: Auto-detects Vue/React files

7. **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
   - **Purpose**: Tailwind CSS autocomplete
   - **Why**: Better CSS class completion
   - **Configuration**: Auto-detects tailwind.config.js

8. **TypeScript** (ms-vscode.vscode-typescript-next)
   - **Purpose**: Latest TypeScript features
   - **Why**: Better TypeScript support
   - **Configuration**: Uses workspace TypeScript version

9. **Jest Runner** (firsttris.vscode-jest-runner)
   - **Purpose**: Run Jest tests from VS Code
   - **Why**: Easy test execution
   - **Configuration**: Auto-detects Jest config

10. **Code Spell Checker** (streetsidesoftware.code-spell-checker)
    - **Purpose**: Spell checking in code
    - **Why**: Catch typos in comments and strings
    - **Configuration**: Add technical terms to ignore

### VS Code Settings

**Workspace Settings**:

Create `.vscode/settings.json` in project root:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "typescript.preferences.importModuleSpecifier": "relative",
  "files.eol": "\n",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true,
    "**/.turbo": true,
    "**/coverage": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true,
    "**/.turbo": true,
    "**/coverage": true
  },
  "eslint.workingDirectories": [
    { "directory": "apps/core-api", "changeProcessCWD": true },
    { "directory": "web/admin-portal", "changeProcessCWD": true }
  ],
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ]
}
```

**User Settings** (optional):

```json
{
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.rulers": [80, 120],
  "editor.minimap.enabled": false,
  "editor.wordWrap": "on",
  "terminal.integrated.fontSize": 14,
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "git.enableSmartCommit": true,
  "git.autofetch": true
}
```

### VS Code Launch Configuration

**Backend Debugging**:

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
      "protocol": "inspector",
      "env": {
        "NODE_ENV": "development"
      }
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Debug CBE Engine",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start:debug"],
      "cwd": "${workspaceFolder}/apps/cbe-engine",
      "console": "integratedTerminal",
      "restart": true,
      "protocol": "inspector"
    },
    {
      "type": "chrome",
      "request": "launch",
      "name": "Debug Admin Portal",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/web/admin-portal/src",
      "sourceMaps": true,
      "sourceMapPathOverrides": {
        "webpack:///./src/*": "${webRoot}/*"
      }
    }
  ]
}
```

### VS Code Tasks

**Create `.vscode/tasks.json`**:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Core API",
      "type": "npm",
      "script": "start:dev",
      "path": "apps/core-api",
      "problemMatcher": [],
      "isBackground": true,
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start Admin Portal",
      "type": "npm",
      "script": "dev",
      "path": "web/admin-portal",
      "problemMatcher": [],
      "isBackground": true,
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    },
    {
      "label": "Start Docker Services",
      "type": "shell",
      "command": "docker-compose",
      "args": ["up", "-d"],
      "problemMatcher": [],
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Run Migrations",
      "type": "shell",
      "command": "npx",
      "args": ["prisma", "migrate", "dev"],
      "options": {
        "cwd": "${workspaceFolder}/apps/core-api"
      },
      "problemMatcher": []
    },
    {
      "label": "Seed Database",
      "type": "shell",
      "command": "npx",
      "args": ["prisma", "db", "seed"],
      "options": {
        "cwd": "${workspaceFolder}/apps/core-api"
      },
      "problemMatcher": []
    }
  ]
}
```

### VS Code Keybindings

**Create `.vscode/keybindings.json`**:

```json
{
  "keybindings": [
    {
      "key": "ctrl+shift+t",
      "command": "workbench.action.tasks.runTask",
      "args": "Start Core API"
    },
    {
      "key": "ctrl+shift+p",
      "command": "workbench.action.tasks.runTask",
      "args": "Start Admin Portal"
    },
    {
      "key": "ctrl+shift+d",
      "command": "workbench.action.tasks.runTask",
      "args": "Start Docker Services"
    }
  ]
}
```

## WebStorm Setup

### Installation

**Download**: https://www.jetbrains.com/webstorm/

**Install**:
- Download installer for your OS
- Run installer
- Follow installation wizard
- Activate license

### Configuration

**Node.js Configuration**:
1. Open Settings (Ctrl+Alt+S)
2. Go to Languages & Frameworks > Node.js
3. Set Node interpreter to project's Node.js version
4. Enable coding assistance for Node.js

**TypeScript Configuration**:
1. Open Settings
2. Go to Languages & Frameworks > TypeScript
3. Set TypeScript version to workspace version
4. Enable TypeScript service

**ESLint Configuration**:
1. Open Settings
2. Go to Languages & Frameworks > JavaScript > Code Quality Tools > ESLint
3. Enable ESLint
4. Set ESLint package to workspace
5. Enable auto-run on save

**Prettier Configuration**:
1. Open Settings
2. Go to Languages & Frameworks > JavaScript > Prettier
3. Enable Prettier
4. Set Prettier package to workspace
5. Enable run on save for files

### WebStorm Plugins

**Recommended Plugins**:
1. **Prisma** - Prisma support
2. **Docker** - Docker support
3. **Tailwind CSS** - Tailwind CSS support
4. **GitToolBox** - Enhanced Git integration
5. **Rainbow Brackets** - Color-coded brackets

### WebStorm Debugging

**Backend Debugging**:
1. Open Run/Debug Configurations
2. Add new Node.js configuration
3. Set working directory to `apps/core-api`
4. Set Node parameters to `node --inspect`
5. Set JavaScript file to `dist/main.js`
6. Set environment variables

**Frontend Debugging**:
1. Open Run/Debug Configurations
2. Add new JavaScript Debug configuration
3. Set URL to `http://localhost:5173`
4. Set directory to `web/admin-portal`

## Other IDEs

### Sublime Text

**Extensions**:
- SublimeLinter
- SublimeLinter-eslint
- TypeScript Syntax
- Dockerfile Syntax Highlighting
- GitGutter

### Vim/Neovim

**Plugins** (using vim-plug):
```vim
Plug 'neoclide/coc.nvim'
Plug 'prisma/vim-prisma'
Plug 'pangloss/vim-javascript'
Plug 'leafgarland/typescript-vim'
Plug 'peitalin/vim-jsx-typescript'
Plug 'vim-airline/vim-airline'
Plug 'scrooloose/nerdtree'
Plug 'tpope/vim-fugitive'
```

### Emacs

**Packages**:
- typescript-mode
- eslint-mode
- prettier-js-mode
- dockerfile-mode
- magit (Git)

## IDE-Specific Features

### VS Code Features

**Multi-root Workspaces**:
- Open multiple folders as workspace
- Each folder can have its own settings
- Useful for monorepo

**Remote Development**:
- SSH into remote server
- Develop in container
- Develop in WSL

**Integrated Terminal**:
- Multiple terminals
- Split terminals
- Terminal profiles

**Source Control**:
- Git integration
- Branch management
- Merge conflicts
- Blame annotations

### WebStorm Features

**Smart Code Completion**:
- Context-aware suggestions
- Chain completion
- Live templates

**Refactoring**:
- Rename
- Extract method
- Inline variable
- Move file

**Code Analysis**:
- Inspections
- Quick fixes
- Code cleanup

**Database Tools**:
- Database console
- SQL editor
- Data viewer

## Common IDE Issues

### Issue 1: TypeScript Errors Despite Correct Code

**Symptom**: TypeScript shows errors but code is correct

**Cause**: IDE using global TypeScript instead of workspace

**VS Code Fix**:
```json
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

**WebStorm Fix**:
- Settings > Languages & Frameworks > TypeScript
- Set TypeScript version to workspace

### Issue 2: ESLint Not Working

**Symptom**: ESLint not showing errors or not auto-fixing

**Cause**: ESLint extension not configured

**VS Code Fix**:
```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.workingDirectories": [
    { "directory": "apps/core-api", "changeProcessCWD": true },
    { "directory": "web/admin-portal", "changeProcessCWD": true }
  ]
}
```

**WebStorm Fix**:
- Settings > Languages & Frameworks > JavaScript > Code Quality Tools > ESLint
- Enable ESLint
- Set ESLint package to workspace

### Issue 3: Prettier Not Formatting

**Symptom**: Prettier not formatting on save

**Cause**: Prettier extension not configured

**VS Code Fix**:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

**WebStorm Fix**:
- Settings > Languages & Frameworks > JavaScript > Prettier
- Enable Prettier
- Set Prettier package to workspace
- Enable run on save

### Issue 4: Debugging Breakpoints Not Hit

**Symptom**: Breakpoints not triggering during debugging

**Cause**: Source maps not configured or incorrect

**VS Code Fix**:
```json
{
  "sourceMaps": true,
  "sourceMapPathOverrides": {
    "webpack:///./src/*": "${webRoot}/*"
  }
}
```

**WebStorm Fix**:
- Ensure source maps are enabled in tsconfig.json
- Rebuild project
- Restart debug session

## Productivity Tips

### VS Code Tips

**Multi-cursor Editing**:
- Alt + Click: Add cursor
- Ctrl + D: Select next occurrence
- Ctrl + Shift + L: Select all occurrences

**Quick Navigation**:
- Ctrl + P: Quick open file
- Ctrl + Shift + O: Go to symbol
- Ctrl + G: Go to line
- Ctrl + Shift + F: Search in files

**Code Snippets**:
- Create custom snippets in .vscode/snippets.json
- Use Emmet abbreviations for HTML/CSS

**Integrated Terminal**:
- Ctrl + `: Toggle terminal
- Ctrl + Shift + `: Create new terminal
- Split terminal for multiple commands

### WebStorm Tips

**Live Templates**:
- Settings > Editor > Live Templates
- Create custom templates
- Use abbreviations for common patterns

**Code Folding**:
- Ctrl + .: Fold code
- Ctrl + Shift + .: Unfold code
- Custom folding regions

**Structural Search and Replace**:
- Edit > Find > Replace Structurally
- Search and replace code patterns

**Database Tools**:
- View > Tool Windows > Database
- Connect to database
- Run SQL queries

## IDE Extensions for Specific Technologies

### Prisma

**VS Code Extension**: prisma.prisma

**Features**:
- Schema highlighting
- Autocomplete
- Go to definition
- Format schema

### Docker

**VS Code Extension**: ms-azuretools.vscode-docker

**Features**:
- Docker file syntax highlighting
- Docker Compose validation
- Container management
- Image management

### Tailwind CSS

**VS Code Extension**: bradlc.vscode-tailwindcss

**Features**:
- Class autocomplete
- Hover information
- Linting
- Go to definition

### Jest

**VS Code Extension**: firsttris.vscode-jest-runner

**Features**:
- Run tests from editor
- Debug tests
- Test coverage
- Test results

## IDE Customization

### VS Code Themes

**Recommended Themes**:
- One Dark Pro
- Dracula Official
- GitHub Dark
- Catppuccin

**Install**:
- Extensions > Themes
- Search and install
- Set in Settings > Color Theme

### VS Code Icons

**Recommended Icon Themes**:
- Material Icon Theme
- Material Design Icons
- File Icons

**Install**:
- Extensions > Icon Themes
- Search and install
- Set in Settings > File Icon Theme

### WebStorm Themes

**Recommended Themes**:
- Darcula
- One Dark
- Solarized Dark

**Install**:
- Settings > Appearance & Behavior > Appearance
- Select theme

## Future Enhancements

### AI-Assisted Development

**Status**: Not implemented

**Proposal**: Add AI extensions:
- GitHub Copilot
- Tabnine
- Codeium

### Code Review Integration

**Status**: Not implemented

**Proposal**: Add code review extensions:
- GitHub Pull Requests
- GitLab Merge Requests

## Related Documentation

- [04-Development-Setup.md](./04-Development-Setup.md) - Development setup
- [06-Testing-Setup.md](./06-Testing-Setup.md) - Testing setup
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
