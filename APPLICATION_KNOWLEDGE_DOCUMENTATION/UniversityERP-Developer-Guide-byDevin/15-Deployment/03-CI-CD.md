# CI/CD

## Purpose

This document explains CI/CD in the University ERP system. It details how CI/CD pipelines are implemented, automated testing, building, and deployment.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses CI/CD for automation. Understanding CI/CD is critical for:
- Automating builds and tests
- Automating deployments
- Ensuring code quality
- Debugging CI/CD issues
- Optimizing CI/CD pipelines

Without understanding CI/CD, developers may struggle with automation or may introduce CI/CD-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn CI/CD
- **Feature Development**: Preparing for deployment
- **Code Reviews**: Reviewing CI/CD configurations
- **Automation**: Automating builds and deployments
- **Quality**: Ensuring code quality

## Dependencies

### CI/CD Dependencies

**Confirmed by Code**: CI/CD depends on:

- **GitHub Actions**: CI/CD platform
- **Docker**: Containerization
- **Kubernetes**: Deployment target
- **Testing Frameworks**: Jest, etc.

## Internal Architecture

### CI/CD Architecture

**Confirmed by Code**: CI/CD follows pipeline-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Code Push                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions Trigger                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Install Dependencies                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Run Tests                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Build Docker Images                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Push to Registry                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Deploy to Kubernetes                           │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### GitHub Actions Workflow

**Confirmed by Code**: GitHub Actions workflow for CI/CD.

**.github/workflows/ci-cd.yml**:
```yaml
name: CI/CD Pipeline

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
        image: postgres:16-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: university_erp_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: apps/core-api/package-lock.json
    
    - name: Install Dependencies
      run: |
        cd apps/core-api
        npm ci
    
    - name: Run Tests
      run: |
        cd apps/core-api
        npm run test
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/university_erp_test
        REDIS_HOST: localhost
        REDIS_PORT: 6379
        JWT_SECRET: test-secret
    
    - name: Build
      run: |
        cd apps/core-api
        npm run build

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and Push Core API
      uses: docker/build-push-action@v4
      with:
        context: ./apps/core-api
        push: true
        tags: university-erp/core-api:latest, university-erp/core-api:${{ github.sha }}
        cache-from: type=registry,ref=university-erp/core-api:latest
        cache-to: type=inline
    
    - name: Build and Push Admin Portal
      uses: docker/build-push-action@v4
      with:
        context: ./web/admin-portal
        push: true
        tags: university-erp/admin-portal:latest, university-erp/admin-portal:${{ github.sha }}
        cache-from: type=registry,ref=university-erp/admin-portal:latest
        cache-to: type=inline

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
    
    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/core-api core-api=university-erp/core-api:${{ github.sha }}
        kubectl set image deployment/admin-portal admin-portal=university-erp/admin-portal:${{ github.sha }}
        kubectl rollout status deployment/core-api
        kubectl rollout status deployment/admin-portal
```

**What This Does**:
- **test**: Runs tests with PostgreSQL and Redis services
- **build-and-push**: Builds and pushes Docker images
- **deploy**: Deploys to Kubernetes
- **needs**: Job dependencies
- **if**: Conditional execution

## Database Interactions

### CI/CD-Database Flow

**Confirmed by Code**: CI/CD uses PostgreSQL service for testing.

**Flow**:
```
CI/CD → PostgreSQL Service → Test Database
```

## Redis Interactions

### CI/CD-Redis Flow

**Confirmed by Code**: CI/CD uses Redis service for testing.

**Flow**:
```
CI/CD → Redis Service → Test Cache
```

## Queue Interactions

### CI/CD-Queue Flow

**Confirmed by Error**: CI/CD doesn't interact with queues directly.

**Flow**:
```
CI/CD → No queue interaction
```

## Worker Interactions

### CI/CD-Worker Flow

**Confirmed by Code**: CI/CD doesn't interact with workers directly.

**Flow**:
```
CI/CD → No worker interaction
```

## Business Rules

### CI/CD Rules

**Confirmed by Code**: CI/CD follows these rules:

1. **Automated Testing**: Run tests on every push
2. **Automated Building**: Build images on main branch
3. **Automated Deployment**: Deploy on main branch
4. **Dependency Caching**: Cache dependencies for speed
5. **Service Dependencies**: Use services for dependencies

### Pipeline Rules

**Confirmed by Code**: Pipeline rules:

1. **Job Dependencies**: Jobs depend on previous jobs
2. **Conditional Execution**: Execute based on conditions
3. **Secrets**: Use secrets for sensitive data
4. **Caching**: Use caching for speed
5. **Parallel Execution**: Run jobs in parallel when possible

## Security

### CI/CD Security

**Confirmed by Code**: Security considerations for CI/CD:

1. **Secrets**: Use GitHub secrets
2. **Access Control**: Restrict access to secrets
3. **Token Security**: Use secure tokens
4. **Dependency Scanning**: Scan dependencies for vulnerabilities
5. **Image Scanning**: Scan images for vulnerabilities

## Performance Considerations

### CI/CD Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Use caching for speed
2. **Parallel Jobs**: Run jobs in parallel
3. **Service Health**: Use health checks
4. **Build Cache**: Use build cache
5. **Dependency Cache**: Cache dependencies

## Common Mistakes

### Mistake 1: Not Using Caching

**Symptom**: Slow pipeline

**Cause**: Not using caching

**Fix**:
```yaml
# Use caching
- name: Setup Node.js
  uses: actions/setup-node@v3
  with:
    node-version: '20'
    cache: 'npm'
```

### Mistake 2: Not Setting Up Services

**Symptom**: Tests failing

**Cause**: Not setting up service dependencies

**Fix**:
```yaml
# Set up services
services:
  postgres:
    image: postgres:16-alpine
    # configuration
```

### Mistake 3: Committing Secrets

**Symptom**: Security vulnerability

**Cause**: Committing secrets to workflow

**Fix**:
```yaml
# Use secrets
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

## Debugging Guide

### CI/CD Debugging

**Issue**: Pipeline failed

**Investigation**:
1. Check pipeline logs
2. Check job status
3. Check service health
4. Check configuration
5. Check secrets

**Tools**:
- GitHub Actions logs
- GitHub Actions UI
- Local testing
- Debugging workflows

## Future Enhancements

### Dependency Scanning

**Status**: Not implemented

**Proposal**: Implement dependency scanning:
- Scan dependencies for vulnerabilities
- Security alerts
- Better security
- More complex
- Better for production

### Automated Rollback

**Status**: Not implemented

**Proposal**: Implement automated rollback:
- Rollback on failure
- Health checks
- Better reliability
- More complex
- Better for production

## Production Considerations

### Production CI/CD

**Production Deployment**:
- Use secrets for sensitive data
- Enable dependency scanning
- Enable image scanning
- Monitor pipeline performance
- Monitor deployment success rate

### CI/CD Monitoring

**Monitoring Metrics**:
- Pipeline success rate
- Pipeline duration
- Job duration
- Resource usage
- Deployment frequency

## Example Requests

### CI/CD Example

**Trigger Pipeline**:
```bash
git push origin main
```

## Example Responses

### CI/CD Response

**Response**: Pipeline successful

```bash
Pipeline completed successfully
```

## Sequence Diagrams

### CI/CD Flow

```
Code Push → Trigger → Install Dependencies → Run Tests → Build → Push → Deploy
```

## Architecture Diagrams

### CI/CD Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Code Push                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions Trigger                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Install Dependencies                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Run Tests                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Build Docker Images                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Push to Registry                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Deploy to Kubernetes                           │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is CI/CD implemented?

**Answer**: CI/CD via:
- GitHub Actions for automation
- Automated testing
- Automated building
- Automated deployment
- Pipeline dependencies

### Q2: How do you handle secrets in CI/CD?

**Answer**: Secrets handling via:
- GitHub secrets
- Environment variables
- Access control
- Token rotation
- Secret encryption

### Q3: How do you optimize CI/CD performance?

**Answer**: Optimize CI/CD via:
- Dependency caching
- Build caching
- Parallel job execution
- Service health checks
- Pipeline optimization

## Exercises

### Exercise 1: Create CI/CD Pipeline

**Task**: Create a CI/CD pipeline.

**Steps**:
1. Create workflow file
2. Add test job
3. Add build job
4. Add deploy job
5. Test pipeline

**Verification**:
- Workflow created
- Test job works
- Build job works
- Deploy job works
- Tests pass

### Exercise 2: Add Caching

**Task**: Add caching to CI/CD pipeline.

**Steps**:
1. Add dependency caching
2. Add build caching
3. Configure cache keys
4. Test caching
5. Verify speed improvement

**Verification**:
- Caching added
- Dependency caching works
- Build caching works
- Speed improved
- Tests pass

## Real Production Scenarios

### Scenario 1: Pipeline Failed

**Situation**: Pipeline failed

**Response**:
1. Check pipeline logs
2. Check job status
3. Check configuration
4. Fix issue
5. Rerun pipeline

### Scenario 2: Slow Pipeline

**Situation**: Pipeline slow

**Response**:
1. Check caching
2. Optimize jobs
3. Add parallel execution
4. Optimize services
5. Monitor performance

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [02-Kubernetes](./02-Kubernetes.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [17-Production](../17-Production/README.md) - Production details
