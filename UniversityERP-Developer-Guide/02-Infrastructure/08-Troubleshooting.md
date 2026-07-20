# Infrastructure Troubleshooting

## Purpose

This document provides a comprehensive guide for troubleshooting infrastructure issues in the University ERP system. It details common issues, their causes, and solutions.

## Why This Document Exists

**Confirmed by Code**: The University ERP infrastructure can encounter various issues. Understanding troubleshooting is critical for:
- Resolving issues quickly
- Minimizing downtime
- Identifying root causes
- Preventing recurrence
- Documenting solutions

Without proper troubleshooting knowledge, issues may take longer to resolve or may be resolved incorrectly.

## Where This Is Used

- **Operations**: Daily troubleshooting of infrastructure
- **Support**: Resolving user-reported issues
- **Maintenance**: Preventive troubleshooting
- **Documentation**: Documenting known issues and solutions
- **Training**: Training team on troubleshooting

## Dependencies

### Troubleshooting Dependencies

**Confirmed by Code**: Troubleshooting depends on:

- **Docker**: Container management
- **System Logs**: System and application logs
- **Monitoring Tools**: Metrics and alerts
- **Debugging Tools**: Debugging commands
- **Documentation**: Known issues and solutions

## Internal Architecture

### Troubleshooting Flow

**Confirmed by Code**: Troubleshooting follows a systematic approach.

```
┌─────────────────────────────────────────────────────────┐
│              Troubleshooting Flow                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Identify     │  │  Diagnose       │  │  Resolve       │
│  Issue        │  │  Root Cause     │  │  Issue         │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Verify       │  │  Document      │  │  Prevent       │
│  Resolution   │  │  Solution      │  │  Recurrence    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Docker Issues

#### Issue: Container Won't Start

**Symptom**:
```bash
docker-compose up -d
# Container shows "Exited" or "Restarting"
```

**Possible Causes**:
- Port conflict
- Volume permission issue
- Invalid configuration
- Resource limits

**Investigation**:
```bash
# Check container status
docker-compose ps

# Check container logs
docker-compose logs <service>

# Check Docker events
docker events
```

**Solutions**:

**Solution 1: Check Port Conflict**
```bash
# Find process using port
lsof -i :5432

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5433:5432"
```

**Solution 2: Fix Volume Permissions**
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./docker-volumes/

# Or run Docker with correct user
```

**Solution 3: Check Configuration**
```bash
# Validate docker-compose.yml
docker-compose config

# Check for syntax errors
```

#### Issue: Container Keeps Restarting

**Symptom**:
```bash
docker-compose ps
# Container shows "Restarting" with increasing restart count
```

**Possible Causes**:
- Application crash
- Database connection failure
- Invalid environment variables
- Resource exhaustion

**Investigation**:
```bash
# Check container logs
docker-compose logs -f <service>

# Check resource usage
docker stats <service>
```

**Solutions**:

**Solution 1: Check Application Logs**
```bash
# View logs to identify crash reason
docker-compose logs <service>
```

**Solution 2: Check Database Connection**
```bash
# Test database connection
docker-compose exec postgres pg_isready

# Check DATABASE_URL
cat .env | grep DATABASE_URL
```

**Solution 3: Check Environment Variables**
```bash
# Verify environment variables
docker-compose exec <service> env
```

### Database Issues

#### Issue: PostgreSQL Connection Failed

**Symptom**:
```bash
# Application logs
Error: Can't reach database server
```

**Possible Causes**:
- PostgreSQL not running
- Invalid DATABASE_URL
- Network issue
- Firewall blocking

**Investigation**:
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Test connection
docker-compose exec postgres pg_isready

# Check DATABASE_URL
cat .env | grep DATABASE_URL
```

**Solutions**:

**Solution 1: Start PostgreSQL**
```bash
docker-compose up -d postgres

# Wait for it to be ready
docker-compose exec postgres pg_isready
```

**Solution 2: Fix DATABASE_URL**
```bash
# Edit .env
# Should be: postgresql://postgres:postgres@localhost:5432/university_erp
```

**Solution 3: Check Network**
```bash
# Test network connectivity
docker-compose exec core-api ping postgres
```

#### Issue: Database Migration Failed

**Symptom**:
```bash
npx prisma migrate dev
# Error: Migration failed
```

**Possible Causes**:
- Schema conflict
- Migration conflict
- Database lock
- Permission issues

**Investigation**:
```bash
# Check migration status
npx prisma migrate status

# Check database logs
docker-compose logs postgres
```

**Solutions**:

**Solution 1: Resolve Conflict**
```bash
# Check migration files
ls prisma/migrations/

# Manually resolve conflict in migration SQL
```

**Solution 2: Reset Database**
```bash
# WARNING: Deletes all data
npx prisma migrate reset
```

### Redis Issues

#### Issue: Redis Connection Failed

**Symptom**:
```bash
# Application logs
Error: Redis connection failed
```

**Possible Causes**:
- Redis not running
- Invalid REDIS_HOST/PORT
- Network issue
- Firewall blocking

**Investigation**:
```bash
# Check Redis status
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli ping

# Check environment variables
cat .env | grep REDIS
```

**Solutions**:

**Solution 1: Start Redis**
```bash
docker-compose up -d redis
```

**Solution 2: Fix Environment Variables**
```bash
# Edit .env
REDIS_HOST=localhost
REDIS_PORT=6379
```

**Solution 3: Test Connection**
```bash
docker-compose exec redis redis-cli ping
# Should return PONG
```

#### Issue: Redis Memory Full

**Symptom**:
```bash
# Application logs
Error: OOM command not allowed
```

**Possible Causes**:
- Redis maxmemory reached
- No eviction policy set

**Investigation**:
```bash
# Check Redis memory
docker-compose exec redis redis-cli INFO memory
```

**Solutions**:

**Solution 1: Clear Redis**
```bash
# WARNING: Deletes all data
docker-compose exec redis redis-cli FLUSHALL
```

**Solution 2: Set Eviction Policy**
```bash
# Edit docker-compose.yml
command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

# Restart Redis
docker-compose restart redis
```

### MinIO Issues

#### Issue: MinIO Connection Failed

**Symptom**:
```bash
# Application logs
Error: MinIO connection failed
```

**Possible Causes**:
- MinIO not running
- Invalid MINIO_ENDPOINT
- Invalid credentials
- Network issue

**Investigation**:
```bash
# Check MinIO status
docker-compose ps minio

# Test connection
curl http://localhost:9000/minio/health/live

# Check environment variables
cat .env | grep MINIO
```

**Solutions**:

**Solution 1: Start MinIO**
```bash
docker-compose up -d minio
```

**Solution 2: Fix Environment Variables**
```bash
# Edit .env
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

**Solution 3: Test Connection**
```bash
curl http://localhost:9000/minio/health/live
```

#### Issue: MinIO Bucket Not Found

**Symptom**:
```bash
# Application logs
Error: Bucket not found
```

**Possible Causes**:
- Bucket not created
- Incorrect bucket name
- Permission issues

**Investigation**:
```bash
# List buckets
docker-compose exec minio mc ls local
```

**Solutions**:

**Solution 1: Create Bucket**
```bash
docker-compose exec minio mc mb local/university-erp-docs
docker-compose exec minio mc mb local/university-erp-exams
```

**Solution 2: Fix Bucket Name**
```bash
# Edit .env
MINIO_BUCKET=university-erp-docs
MINIO_EXAM_BUCKET=university-erp-exams
```

### Elasticsearch Issues

#### Issue: Elasticsearch Connection Failed

**Symptom**:
```bash
# Application logs
Error: Elasticsearch connection failed
```

**Possible Causes**:
- Elasticsearch not running
- Invalid ELASTICSEARCH_NODE
- Network issue
- Firewall blocking

**Investigation**:
```bash
# Check Elasticsearch status
docker-compose ps elasticsearch

# Test connection
curl http://localhost:9200/_cluster/health

# Check environment variables
cat .env | grep ELASTICSEARCH
```

**Solutions**:

**Solution 1: Start Elasticsearch**
```bash
docker-compose up -d elasticsearch
```

**Solution 2: Fix Environment Variables**
```bash
# Edit .env
ELASTICSEARCH_NODE=http://localhost:9200
```

**Solution 3: Test Connection**
```bash
curl http://localhost:9200/_cluster/health
```

## Database Interactions

### Database Troubleshooting

**Confirmed by Code**: Database issues can be troubleshooted via logs and commands.

**Slow Queries**:
```sql
-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**Connection Issues**:
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check connection details
SELECT * FROM pg_stat_activity;
```

**Lock Issues**:
```sql
-- Check locks
SELECT * FROM pg_locks;

-- Check blocking queries
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';
```

## Redis Interactions

### Redis Troubleshooting

**Confirmed by Code**: Redis issues can be troubleshooted via commands.

**Memory Issues**:
```bash
# Check memory usage
docker-compose exec redis redis-cli INFO memory

# Check memory fragmentation
docker-compose exec redis redis-cli MEMORY STATS
```

**Connection Issues**:
```bash
# Check connections
docker-compose exec redis redis-cli CLIENT LIST

# Check slowlog
docker-compose exec redis redis-cli SLOWLOG GET
```

## Queue Interactions

### Queue Troubleshooting

**Confirmed by Code**: Queue issues can be troubleshooted via Bull commands.

**Job Stuck**:
```typescript
// Check job status
const job = await queue.getJob(jobId);
console.log(job);

// Retry job
await job.retry();
```

**Queue Backlog**:
```typescript
// Check queue stats
const stats = await queue.getJobCounts();
console.log(stats);
```

## Worker Interactions

### Worker Troubleshooting

**Confirmed by Code**: Worker issues can be troubleshooted via logs.

**Worker Not Processing**:
```bash
# Check worker logs
docker-compose logs -f notification-worker

# Check worker status
docker-compose exec notification-worker ps aux
```

## Business Rules

### Troubleshooting Rules

**Confirmed by Code**: Troubleshooting follows these rules:

1. **Systematic Approach**: Follow systematic troubleshooting process
2. **Check Logs First**: Always check logs first
3. **Reproduce Issue**: Try to reproduce the issue
4. **Isolate Problem**: Isolate the problem to a component
5. **Test Solution**: Test solution before implementing

### Documentation Rules

**Confirmed by Code**: Documentation follows these rules:

1. **Document Issue**: Document the issue
2. **Document Root Cause**: Document the root cause
3. **Document Solution**: Document the solution
4. **Document Prevention**: Document how to prevent recurrence
5. **Share Knowledge**: Share knowledge with team

## Security

### Troubleshooting Security

**Confirmed by Code**: Security considerations for troubleshooting:

1. **No Data Exposure**: Don't expose sensitive data during troubleshooting
2. **Secure Access**: Restrict access to troubleshooting tools
3. **Audit Logs**: Audit troubleshooting activities
4. **Secure Disposal**: Securely dispose of troubleshooting data

## Performance Considerations

### Troubleshooting Performance

**Confirmed by Code**: Performance considerations for troubleshooting:

1. **Minimize Impact**: Minimize impact on production
2. **Use Read-Only**: Use read-only operations where possible
3. **Sample Data**: Use sample data for testing
4. **Monitor Impact**: Monitor impact of troubleshooting

## Common Mistakes

### Mistake 1: Not Checking Logs

**Symptom**: Issue not resolved

**Cause**: Not checking logs

**Fix**:
```bash
# Always check logs first
docker-compose logs <service>
```

### Mistake 2: Not Reproducing Issue

**Symptom**: Solution doesn't work

**Cause**: Not reproducing issue

**Fix**:
```bash
# Reproduce issue before fixing
# Test fix before implementing
```

### Mistake 3: Not Documenting Solution

**Symptom**: Same issue occurs again

**Cause**: Not documenting solution

**Fix**:
```bash
# Document solution
# Share with team
# Add to knowledge base
```

## Debugging Guide

### Systematic Troubleshooting

**Issue**: Infrastructure not working

**Investigation**:
1. Check service status: `docker-compose ps`
2. Check service logs: `docker-compose logs <service>`
3. Check resource usage: `docker stats`
4. Check network connectivity: `ping`
5. Check configuration: `docker-compose config`

**Tools**:
- Docker commands
- System commands
- Service-specific tools
- Monitoring tools

## Future Enhancements

### Automated Troubleshooting

**Status**: Not implemented

**Proposal**: Implement automated troubleshooting:
- Automated issue detection
- Automated root cause analysis
- Automated solution suggestion
- Automated issue resolution
- Automated documentation

### Self-Healing

**Status**: Not implemented

**Proposal**: Implement self-healing:
- Automatic restart on failure
- Automatic scaling on load
- Automatic failover
- Automatic recovery
- Automatic alerting

## Production Considerations

### Production Troubleshooting

**Production Deployment**:
- Use monitoring to detect issues early
- Use alerting to notify team
- Use runbooks for common issues
- Use post-mortem analysis
- Use continuous improvement

### Incident Response

**Incident Response Process**:
1. Detect incident
2. Assess impact
3. Mobilize team
4. Resolve incident
5. Communicate with stakeholders
6. Post-mortem analysis
7. Implement improvements

## Example Requests

### Diagnose Issue

**Request**: Diagnose infrastructure issue

**Steps**:
1. Check service status
2. Check logs
3. Check metrics
4. Identify root cause
5. Propose solution

## Example Responses

### Issue Resolution

**Response**: Issue resolved

```json
{
  "issue": "PostgreSQL connection failed",
  "root_cause": "PostgreSQL container not running",
  "solution": "Started PostgreSQL container",
  "status": "resolved"
}
```

## Sequence Diagrams

### Troubleshooting Flow

```
Issue Detected
        ↓
    Check Logs
        ↓
    Identify Component
        ↓
    Diagnose Root Cause
        ↓
    Implement Solution
        ↓
    Verify Resolution
        ↓
    Document Solution
```

## Architecture Diagrams

### Troubleshooting Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Issue Detection                              │
│  Monitoring, Alerts, User Reports                      │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Diagnosis                                    │
│  Logs, Metrics, Debugging Tools                        │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Resolution                                   │
│  Fixes, Workarounds, Escalations                       │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Verification                                  │
│  Testing, Monitoring, Validation                        │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you troubleshoot a Docker container that won't start?

**Answer**: Troubleshooting via:
- Check container status: `docker-compose ps`
- Check container logs: `docker-compose logs <service>`
- Check port conflicts: `lsof -i :port`
- Check volume permissions
- Check configuration: `docker-compose config`

### Q2: How do you troubleshoot a database connection issue?

**Answer**: Database troubleshooting via:
- Check database status: `docker-compose ps postgres`
- Test connection: `docker-compose exec postgres pg_isready`
- Check DATABASE_URL
- Check network connectivity
- Check firewall rules

### Q3: How do you troubleshoot a slow application?

**Answer**: Slow application troubleshooting via:
- Check resource usage: `docker stats`
- Check database queries: `EXPLAIN ANALYZE`
- Check cache hit rate
- Check network latency
- Profile application code

## Exercises

### Exercise 1: Troubleshoot Container Issue

**Task**: Troubleshoot a container that won't start.

**Steps**:
1. Check container status
2. Check container logs
3. Identify root cause
4. Implement solution
5. Verify resolution

**Verification**:
- Container starts
- Service healthy
- Issue resolved

### Exercise 2: Troubleshoot Database Issue

**Task**: Troubleshoot a database connection issue.

**Steps**:
1. Check database status
2. Test connection
3. Check configuration
4. Fix issue
5. Verify connection

**Verification**:
- Connection works
- Application connects
- Issue resolved

## Real Production Scenarios

### Scenario 1: Database Connection Pool Exhausted

**Situation**: Database connection pool exhausted

**Response**:
1. Check connection pool size
2. Check connection leaks
3. Increase pool size
4. Fix connection leaks
5. Monitor connections

### Scenario 2: Redis Out of Memory

**Situation**: Redis out of memory

**Response**:
1. Check Redis memory usage
2. Check cache hit rate
3. Adjust eviction policy
4. Increase memory limit
5. Monitor memory usage

## Navigation

**Next Section**: [09-Security](./09-Security.md)

**Previous Section**: [07-Monitoring](./07-Monitoring.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [07-Monitoring](./07-Monitoring.md) - Monitoring details
- [16-Debugging](../16-Debugging/README.md) - Debugging guide
