# Prerequisites

## Purpose

This document details all prerequisites required to work with the University ERP system. Understanding these prerequisites ensures you have the correct versions and configurations before attempting installation.

## Why This Document Exists

**Confirmed by Code**: The University ERP has specific version requirements for Node.js, Docker, and other tools. Using incorrect versions will cause:
- Installation failures
- Runtime errors
- Compatibility issues
- Unpredictable behavior

This document exists to prevent these issues by clearly stating all requirements.

## Where This Is Used

- **Onboarding**: New developers verify their environment
- **CI/CD**: Ensures build agents have correct versions
- **Troubleshooting**: First step when issues occur
- **Documentation**: Reference for system requirements

## System Requirements

### Operating System

**Confirmed by Code**: The system is designed to run on:

- **Linux**: Primary development and production platform
- **macOS**: Supported for development
- **Windows**: Supported for development (via WSL2 recommended)

**Inferred**: Windows support via WSL2 is recommended because:
- Docker Desktop works better on WSL2
- Node.js tooling is more native on Linux
- Shell scripts are designed for Unix-like systems

### Hardware Requirements

**Inferred** (based on typical needs for this stack):

**Minimum**:
- **CPU**: 4 cores (Intel i5/AMD Ryzen 5 or equivalent)
- **RAM**: 8GB
- **Disk**: 50GB free space
- **Network**: Stable internet connection for dependencies

**Recommended**:
- **CPU**: 8 cores (Intel i7/AMD Ryzen 7 or equivalent)
- **RAM**: 16GB
- **Disk**: 100GB free space (SSD recommended)
- **Network**: High-speed internet for faster dependency downloads

**Why These Requirements**:
- Docker services (PostgreSQL, Redis, MinIO, Elasticsearch) consume RAM
- Node.js and npm processes consume CPU and RAM
- node_modules for monorepo can be large (2-5GB)
- Docker volumes for database and cache consume disk space

## Software Requirements

### Node.js

**Confirmed by Code**:
- **Version**: 18.x or higher
- **Source**: apps/core-api/package.json (engines field not visible, but inferred from dependencies)

**Verification**:
```bash
node --version
# Expected output: v18.x.x or higher
```

**Why Node.js 18+**:
- NestJS 10.x requires Node.js 18+
- React 19 requires Node.js 18+
- Prisma 5.x requires Node.js 18+
- Modern JavaScript features (ES2022) support

**Installation**:
- **Linux**: Use nvm (Node Version Manager)
- **macOS**: Use nvm or Homebrew
- **Windows**: Use nvm-windows or official installer

**Using nvm (Recommended)**:
```bash
# Install nvm (Linux/macOS)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js 18
nvm install 18
nvm use 18
nvm alias default 18
```

### npm

**Confirmed by Code**:
- **Version**: 9.x or higher
- **Source**: package-lock.json format (lockfileVersion 3 requires npm 9+)

**Verification**:
```bash
npm --version
# Expected output: 9.x.x or higher
```

**Why npm 9+**:
- npm workspaces require npm 7+ (9+ recommended)
- package-lock.json v3 requires npm 9+
- Better dependency resolution
- Faster installation

**Installation**: npm is bundled with Node.js

### Docker

**Confirmed by Code**:
- **Version**: 20.x or higher
- **Source**: docker-compose.yml uses Docker Compose v2 syntax

**Verification**:
```bash
docker --version
# Expected output: Docker version 20.x.x or higher
```

**Why Docker 20+**:
- Docker Compose v2 integration
- Better performance
- Improved security features
- Better Windows support

**Installation**:
- **Linux**: Follow official Docker installation guide
- **macOS**: Install Docker Desktop
- **Windows**: Install Docker Desktop (WSL2 backend recommended)

**Docker Desktop Configuration**:
- Enable WSL2 integration (Windows)
- Allocate at least 4GB RAM to Docker
- Enable file sharing for project directory

### Docker Compose

**Confirmed by Code**:
- **Version**: 2.x or higher
- **Source**: docker-compose.yml uses Compose file format v3.8

**Verification**:
```bash
docker-compose --version
# Expected output: Docker Compose version v2.x.x or higher
```

**Why Docker Compose 2+**:
- Integrated with Docker CLI
- Better performance
- Improved watch mode
- Better health check support

**Installation**: Included with Docker Desktop

### Git

**Confirmed by Code**:
- **Version**: 2.x or higher
- **Source**: .git directory exists in repository

**Verification**:
```bash
git --version
# Expected output: git version 2.x.x or higher
```

**Why Git 2+**:
- Version control for the project
- Branching and merging
- Collaboration features
- CI/CD integration

**Installation**:
- **Linux**: `sudo apt install git` or equivalent
- **macOS**: Included with Xcode Command Line Tools
- **Windows**: Install Git for Windows

**Git Configuration**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.autocrlf input  # Linux/macOS
git config --global core.autocrlf true   # Windows
```

### PostgreSQL Client

**Confirmed by Code**:
- **Version**: 16.x or higher (matches Docker image version)
- **Source**: docker-compose.yml uses postgres:16-alpine

**Verification**:
```bash
psql --version
# Expected output: psql (PostgreSQL) 16.x or higher
```

**Why PostgreSQL Client**:
- Direct database access for debugging
- Running SQL queries manually
- Database administration
- Migration verification

**Installation**:
- **Linux**: `sudo apt install postgresql-client`
- **macOS**: `brew install postgresql`
- **Windows**: Download from PostgreSQL website

**Alternative**: Use Docker exec instead of local client:
```bash
docker-compose exec postgres psql -U postgres -d university_erp
```

### Redis CLI

**Confirmed by Code**:
- **Version**: 7.x or higher (matches Docker image version)
- **Source**: docker-compose.yml uses redis:7-alpine

**Verification**:
```bash
redis-cli --version
# Expected output: redis-cli 7.x.x
```

**Why Redis CLI**:
- Direct Redis access for debugging
- Inspecting cache data
- Manual cache invalidation
- Queue inspection

**Installation**:
- **Linux**: `sudo apt install redis-tools`
- **macOS**: `brew install redis`
- **Windows**: Download from Redis website

**Alternative**: Use Docker exec instead of local client:
```bash
docker-compose exec redis redis-cli
```

## Optional Tools

### VS Code

**Recommended**: Visual Studio Code

**Extensions Recommended**:
- ESLint
- Prettier
- Prisma
- Docker
- GitLens
- TypeScript Vue Plugin (Volar)
- Tailwind CSS IntelliSense

**Why VS Code**:
- Excellent TypeScript support
- Great debugging capabilities
- Large extension ecosystem
- Integrated terminal
- Git integration

### Postman

**Recommended**: For API testing

**Why Postman**:
- Easy API testing
- Request collection management
- Environment variables
- Automated testing

**Alternative**: Use curl, Insomnia, or HTTPie

### DBeaver

**Recommended**: For database management

**Why DBeaver**:
- Multi-database support
- Visual query builder
- ER diagrams
- Data export/import

**Alternative**: pgAdmin, TablePlus, or command line

## Network Requirements

### Internet Connection

**Required**: Stable internet connection for:

- Downloading npm packages (2-5GB)
- Pulling Docker images (2-5GB)
- Accessing npm registry
- Accessing GitHub
- Accessing documentation

**Bandwidth**:
- **Minimum**: 10 Mbps
- **Recommended**: 50 Mbps or higher

### Firewall

**Required Ports**:
- **3000**: Core API
- **3001**: CBE Engine
- **3002**: Notification Worker
- **3003**: Certificate Generator
- **5173**: Admin Portal
- **5432**: PostgreSQL
- **6379**: Redis
- **9000**: MinIO API
- **9001**: MinIO Console
- **9200**: Elasticsearch

**Firewall Configuration**:
- Allow outbound connections to npm registry
- Allow outbound connections to Docker registry
- Allow inbound connections to application ports (for local testing)
- Allow Docker container networking

## Account Requirements

### GitHub

**Required**: GitHub account for:

- Cloning repository
- Creating pull requests
- Issue tracking
- CI/CD integration

### Docker Hub

**Optional**: Docker Hub account for:

- Pulling public images
- Pushing custom images (if needed)
- Accessing private images

### npm Registry

**Required**: npm registry access for:

- Installing dependencies
- Publishing packages (if needed)

## Environment-Specific Requirements

### Development

**Additional Requirements**:
- Hot-reload tools (included with NestJS and Vite)
- Source map support (included)
- Debugging tools (VS Code debugger)

### Staging

**Additional Requirements**:
- Staging server access
- Staging database access
- Staging Redis access
- CI/CD pipeline access

### Production

**Additional Requirements**:
- Production server access
- Production database access
- Production Redis access
- Secrets management access (AWS Secrets Manager, Azure Key Vault, etc.)
- Monitoring tools access
- Logging tools access

## Verification Checklist

Before proceeding with installation, verify:

- [ ] Node.js 18.x or higher installed
- [ ] npm 9.x or higher installed
- [ ] Docker 20.x or higher installed
- [ ] Docker Compose 2.x or higher installed
- [ ] Git 2.x or higher installed
- [ ] PostgreSQL client installed (optional)
- [ ] Redis CLI installed (optional)
- [ ] VS Code installed (recommended)
- [ ] Internet connection stable
- [ ] Firewall allows required ports
- [ ] GitHub account created
- [ ] Docker Hub account created (optional)

## Common Issues

### Issue 1: Node.js Version Too Old

**Symptom**: Installation fails with "unsupported Node.js version" error

**Cause**: Node.js version is older than 18.x

**Fix**: Install Node.js 18.x using nvm:
```bash
nvm install 18
nvm use 18
```

### Issue 2: Docker Not Running

**Symptom**: `docker ps` fails with "Cannot connect to Docker daemon"

**Cause**: Docker daemon not running

**Fix**: Start Docker Desktop or Docker daemon:
```bash
# Linux
sudo systemctl start docker

# macOS/Windows
# Start Docker Desktop application
```

### Issue 3: Docker Permission Denied

**Symptom**: `docker ps` fails with "permission denied"

**Cause**: User not in docker group

**Fix**: Add user to docker group:
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

### Issue 4: Git Not Configured

**Symptom**: Git commits fail with "user.name not configured"

**Cause**: Git user.name and user.email not set

**Fix**: Configure Git:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Issue 5: Port Already in Use

**Symptom**: Service fails to start with "port already in use" error

**Cause**: Another process using the same port

**Fix**: Stop conflicting process or change port in .env file:
```bash
# Find process using port
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :3000  # Core API

# Kill process
kill -9 <PID>
```

## Next Steps

After verifying all prerequisites:

1. Proceed to [02-Installation.md](./02-Installation.md)
2. Follow the installation guide
3. Verify your setup
4. Proceed to System Architecture documentation

## Additional Resources

### Node.js
- Official website: https://nodejs.org/
- nvm documentation: https://github.com/nvm-sh/nvm

### Docker
- Official website: https://www.docker.com/
- Docker documentation: https://docs.docker.com/

### Git
- Official website: https://git-scm.com/
- Pro Git book: https://git-scm.com/book

### PostgreSQL
- Official website: https://www.postgresql.org/
- Documentation: https://www.postgresql.org/docs/

### Redis
- Official website: https://redis.io/
- Documentation: https://redis.io/docs/

## Troubleshooting

### General Troubleshooting Steps

1. **Check versions**: Verify all tools are at correct versions
2. **Check logs**: Look at error messages for clues
3. **Check permissions**: Verify user has necessary permissions
4. **Check network**: Verify internet connection and firewall
5. **Restart services**: Restart Docker, Node.js, etc.
6. **Reinstall**: Reinstall problematic tool if needed

### Getting Help

If you encounter issues not covered here:

1. Check official documentation for each tool
2. Search for error messages online
3. Ask team members for help
4. Create an issue in the repository

## Version Compatibility Matrix

| Tool | Minimum | Recommended | Notes |
|------|---------|-------------|-------|
| Node.js | 18.x | 18 LTS | Use LTS version for stability |
| npm | 9.x | Latest 9.x | Bundled with Node.js |
| Docker | 20.x | Latest 20.x | Docker Desktop recommended |
| Docker Compose | 2.x | Latest 2.x | Included with Docker Desktop |
| Git | 2.x | Latest 2.x | Any 2.x version works |
| PostgreSQL Client | 16.x | 16.x | Matches Docker image |
| Redis CLI | 7.x | 7.x | Matches Docker image |

## Security Considerations

### Tool Security

- **Keep tools updated**: Regularly update Node.js, Docker, Git
- **Use official sources**: Download from official websites
- **Verify checksums**: Verify downloads if possible
- **Use secure connections**: When downloading tools

### Account Security

- **Use strong passwords**: For GitHub, Docker Hub accounts
- **Enable 2FA**: For GitHub account
- **Use SSH keys**: For Git authentication
- **Rotate credentials**: Regularly rotate passwords and tokens

## Performance Considerations

### Tool Performance

- **Use SSD**: For faster Docker operations
- **Allocate RAM**: Give Docker at least 4GB RAM
- **Use nvm cache**: nvm caches Node.js versions for faster switching
- **Use npm cache**: npm caches packages for faster reinstalls

### Network Performance

- **Use wired connection**: More stable than Wi-Fi
- **Use CDN**: npm registry uses CDN for faster downloads
- **Use mirror**: Use npm mirror if in region with slow access

## Future Enhancements

### Automated Prerequisite Check

**Status**: Not implemented

**Proposal**: Create a script that automatically checks all prerequisites:

```bash
./check-prerequisites.sh
```

This script would:
- Check all tool versions
- Check Docker status
- Check network connectivity
- Report any issues
- Provide fix suggestions

### Docker Image Pre-pull

**Status**: Not implemented

**Proposal**: Pre-pull all Docker images during setup to avoid delays:

```bash
docker pull postgres:16-alpine
docker pull redis:7-alpine
docker pull minio/minio:latest
docker pull elasticsearch:8.13.0
```

## Production Considerations

### Production Prerequisites

In addition to development prerequisites, production requires:

- **Server access**: SSH access to production servers
- **Monitoring tools**: Prometheus, Grafana, or similar
- **Logging tools**: ELK stack, Loki, or similar
- **Secrets management**: AWS Secrets Manager, Azure Key Vault, or similar
- **CI/CD**: GitHub Actions, GitLab CI, or similar
- **Load balancer**: Nginx, HAProxy, or cloud load balancer
- **CDN**: CloudFront, Cloudflare, or similar (optional)

### Production Tool Versions

Production may use different versions for stability:

- **Node.js**: Use LTS version (18.x LTS)
- **Docker**: Use stable release
- **PostgreSQL**: Use stable release (16.x)
- **Redis**: Use stable release (7.x)

## Related Documentation

- [02-Installation.md](./02-Installation.md) - Installation guide
- [03-Quick-Start.md](./03-Quick-Start.md) - Quick start guide
- [04-Development-Setup.md](./04-Development-Setup.md) - Development setup
- [08-Common-Issues.md](./08-Common-Issues.md) - Common issues and solutions
