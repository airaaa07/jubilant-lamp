# Infrastructure Monitoring

## Purpose

This document explains the monitoring strategy for the University ERP infrastructure. It details how to monitor Docker services, resource usage, and system health.

## Why This Document Exists

**Confirmed by Code**: The University ERP infrastructure requires monitoring for reliability. Understanding infrastructure monitoring is critical for:
- Detecting issues early
- Ensuring system reliability
- Optimizing performance
- Planning capacity
- Troubleshooting issues

Without proper monitoring, issues may go undetected until they cause outages.

## Where This Is Used

- **Operations**: Daily monitoring of infrastructure
- **Alerting**: Alerting on issues
- **Performance**: Optimizing performance
- **Capacity Planning**: Planning for growth
- **Troubleshooting**: Debugging issues

## Dependencies

### Monitoring Dependencies

**Confirmed by Code**: Monitoring depends on:

- **Docker**: Container metrics
- **System**: Host metrics
- **Services**: Service-specific metrics
- **Logs**: Application logs
- **Alerting**: Alerting tools

## Internal Architecture

### Monitoring Architecture

**Confirmed by Code**: Monitoring at multiple layers.

```
┌─────────────────────────────────────────────────────────┐
│              Monitoring Layers                            │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Container    │  │  Service       │  │  Application   │
│  Metrics      │  │  Metrics       │  │  Metrics       │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Logs         │  │  Alerts        │  │  Dashboards    │
│  (Collection) │  │  (Notification)│  │  (Visualization)│
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Docker Monitoring

**Confirmed by Code**: Docker provides built-in monitoring.

**Container Stats**:
```bash
# View real-time stats
docker stats

# View stats for specific container
docker stats university-erp-postgres

# View stats with no stream
docker stats --no-stream
```

**Output**:
```
CONTAINER ID   NAME                      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
abc123         university-erp-postgres    5.2%      512Mi / 2Gi          25.6%     1.2GB / 500MB
def456         university-erp-redis       2.1%      256Mi / 512Mi        50.0%     500MB / 200MB
```

**What This Does**:
- Shows CPU usage percentage
- Shows memory usage and limit
- Shows memory usage percentage
- Shows network I/O
- Shows block I/O

### Service Monitoring

**Confirmed by Code**: Services provide health checks.

**PostgreSQL Health**:
```bash
# Check PostgreSQL health
docker-compose exec postgres pg_isready

# Check PostgreSQL connections
docker-compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

**Redis Health**:
```bash
# Check Redis health
docker-compose exec redis redis-cli ping

# Check Redis memory
docker-compose exec redis redis-cli INFO memory
```

**MinIO Health**:
```bash
# Check MinIO health
curl http://localhost:9000/minio/health/live
```

### System Monitoring

**Confirmed by Code**: System monitoring via system tools.

**CPU Monitoring**:
```bash
# Check CPU usage
top
htop

# Check CPU stats
mpstat
```

**Memory Monitoring**:
```bash
# Check memory usage
free -h

# Check memory stats
vmstat
```

**Disk Monitoring**:
```bash
# Check disk usage
df -h

# Check disk I/O
iostat
```

**Network Monitoring**:
```bash
# Check network connections
netstat -tulpn

# Check network stats
iftop
```

## Database Interactions

### PostgreSQL Monitoring

**Confirmed by Code**: PostgreSQL provides monitoring queries.

**Connection Monitoring**:
```sql
-- Check active connections
SELECT count(*) FROM pg_stat_activity;

-- Check connection details
SELECT * FROM pg_stat_activity;
```

**Query Monitoring**:
```sql
-- Check slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**Table Monitoring**:
```sql
-- Check table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Redis Interactions

### Redis Monitoring

**Confirmed by Code**: Redis provides INFO commands.

**General Info**:
```bash
docker-compose exec redis redis-cli INFO
```

**Memory Info**:
```bash
docker-compose exec redis redis-cli INFO memory
```

**Stats Info**:
```bash
docker-compose exec redis redis-cli INFO stats
```

**Key Space Info**:
```bash
docker-compose exec redis redis-cli INFO keyspace
```

## Queue Interactions

### Queue Monitoring

**Confirmed by Code**: Bull queues provide monitoring.

**Queue Stats**:
```typescript
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT),
  },
});

// Get queue stats
const stats = await queue.getJobCounts();
console.log(stats); // { waiting: 10, active: 2, completed: 100, failed: 5 }
```

**Job Monitoring**:
```typescript
// Get waiting jobs
const waiting = await queue.getWaiting();

// Get active jobs
const active = await queue.getActive();

// Get failed jobs
const failed = await queue.getFailed();
```

## Worker Interactions

### Worker Monitoring

**Confirmed by Code**: Workers can be monitored via logs.

**Worker Logs**:
```bash
# View worker logs
docker-compose logs -f notification-worker
```

**Worker Status**:
```bash
# Check worker process
docker-compose exec notification-worker ps aux
```

## Business Rules

### Monitoring Rules

**Confirmed by Code**: Monitoring follows these rules:

1. **Continuous Monitoring**: Monitor continuously
2. **Alert on Thresholds**: Alert when metrics exceed thresholds
3. **Log Everything**: Log all relevant events
4. **Retain Logs**: Retain logs for analysis
5. **Regular Review**: Review metrics regularly

### Alerting Rules

**Confirmed by Code**: Alerting follows these rules:

1. **Critical Alerts**: Immediate notification for critical issues
2. **Warning Alerts**: Notification for warning issues
3. **Info Alerts**: Notification for informational events
4. **Escalation**: Escalate critical alerts
5. **Acknowledgment**: Require acknowledgment for critical alerts

## Security

### Monitoring Security

**Confirmed by Code**: Security considerations for monitoring:

1. **Secure Logs**: Don't log sensitive data
2. **Secure Access**: Restrict access to monitoring tools
3. **Secure Storage**: Secure storage for logs and metrics
4. **Secure Transmission**: Encrypt monitoring data in transit
5. **Audit Access**: Audit access to monitoring data

## Performance Considerations

### Monitoring Performance

**Confirmed by Code**: Performance considerations for monitoring:

1. **Sampling**: Sample metrics to reduce overhead
2. **Async Logging**: Use async logging to reduce overhead
3. **Batch Processing**: Batch log entries
4. **Compression**: Compress logs and metrics
5. **Retention**: Define retention policy

## Common Mistakes

### Mistake 1: Not Monitoring Critical Services

**Symptom**: Issues go undetected

**Cause**: Not monitoring critical services

**Fix**:
```bash
# Monitor all critical services
docker-compose ps
docker stats
```

### Mistake 2: Not Setting Up Alerts

**Symptom**: Issues detected too late

**Cause**: Not setting up alerts

**Fix**:
```bash
# Set up alerts for critical metrics
# Use monitoring tools (Prometheus, Grafana)
# Configure alerting rules
```

### Mistake 3: Not Retaining Logs

**Symptom**: Cannot debug past issues

**Cause**: Not retaining logs

**Fix**:
```bash
# Configure log rotation
# Retain logs for sufficient time
# Archive old logs
```

## Debugging Guide

### Monitoring Debugging

**Issue**: Monitoring not working

**Investigation**:
1. Check monitoring tool is running
2. Check configuration
3. Check network connectivity
4. Check permissions
5. Check logs

**Tools**:
- Docker logs
- System logs
- Monitoring tool logs
- Network tools

## Future Enhancements

### Prometheus Integration

**Status**: Not implemented

**Proposal**: Implement Prometheus monitoring:
- Prometheus for metrics collection
- Grafana for visualization
- Alertmanager for alerting
- Custom dashboards
- Alerting rules

### APM Integration

**Status**: Not implemented

**Proposal**: Implement APM monitoring:
- New Relic or Datadog
- Application performance monitoring
- Distributed tracing
- Error tracking
- Performance profiling

## Production Considerations

### Production Monitoring

**Production Deployment**:
- Use managed monitoring (AWS CloudWatch, Azure Monitor)
- Configure alerting rules
- Set up dashboards
- Configure log aggregation
- Configure metrics retention
- Configure alerting escalation

### Monitoring Metrics

**Critical Metrics**:
- CPU usage > 80%
- Memory usage > 80%
- Disk usage > 80%
- Database connection pool > 80%
- Cache hit rate < 80%
- Error rate > 1%
- Response time > 1s

## Example Requests

### Check Container Stats

**Request**:
```bash
docker stats --no-stream
```

**Response**:
```
CONTAINER ID   NAME                      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
abc123         university-erp-postgres    5.2%      512Mi / 2Gi          25.6%     1.2GB / 500MB
def456         university-erp-redis       2.1%      256Mi / 512Mi        50.0%     500MB / 200MB
```

## Example Responses

### Service Health

**Request**: Check service health

**Response**:
```json
{
  "postgres": "healthy",
  "redis": "healthy",
  "minio": "healthy",
  "elasticsearch": "healthy"
}
```

## Sequence Diagrams

### Monitoring Flow

```
System Running
        ↓
    Collect Metrics
        ↓
    Store Metrics
        ↓
    Analyze Metrics
        ↓
    Check Thresholds
        ↓
    Alert if Threshold Exceeded
        ↓
    Visualize Metrics
```

## Architecture Diagrams

### Monitoring Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Infrastructure                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Docker       │  │  System        │  │  Services      │
│  Metrics      │  │  Metrics       │  │  Metrics       │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Monitoring Stack                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Prometheus   │  │  Grafana      │  │  Alertmanager │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you monitor Docker containers?

**Answer**: Docker container monitoring via:
- Docker stats for real-time metrics
- Docker logs for container logs
- Health checks for service health
- Custom monitoring tools (Prometheus, cAdvisor)
- Resource limits and usage

### Q2: What metrics do you monitor?

**Answer**: Critical metrics include:
- CPU usage
- Memory usage
- Disk usage and I/O
- Network I/O
- Database connections
- Cache hit rate
- Error rates
- Response times

### Q3: How do you set up alerts?

**Answer**: Alerting via:
- Configure alerting rules in monitoring tools
- Set thresholds for critical metrics
- Configure notification channels (email, Slack, PagerDuty)
- Configure escalation policies
- Require acknowledgment for critical alerts

## Exercises

### Exercise 1: Monitor Docker Containers

**Task**: Monitor Docker container metrics.

**Steps**:
1. Run docker stats
2. Analyze CPU usage
3. Analyze memory usage
4. Analyze network I/O
5. Identify bottlenecks

**Verification**:
- Metrics collected
- Bottlenecks identified
- Optimization plan created

### Exercise 2: Check Service Health

**Task**: Check health of all services.

**Steps**:
1. Check PostgreSQL health
2. Check Redis health
3. Check MinIO health
4. Check Elasticsearch health
5. Document health status

**Verification**:
- All services checked
- Health status documented
- Issues identified

## Real Production Scenarios

### Scenario 1: High CPU Usage

**Situation**: CPU usage > 80%

**Response**:
1. Identify container with high CPU
2. Check what process is using CPU
3. Optimize if possible
4. Scale if needed
5. Monitor for recurrence

### Scenario 2: High Memory Usage

**Situation**: Memory usage > 80%

**Response**:
1. Identify container with high memory
2. Check for memory leaks
3. Optimize if possible
4. Scale if needed
5. Monitor for recurrence

## Navigation

**Next Section**: [08-Troubleshooting](./08-Troubleshooting.md)

**Previous Section**: [06-Backup-and-Recovery](./06-Backup-and-Recovery.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [05-Performance](./05-Performance.md) - Performance details
- [17-Production](../17-Production/README.md) - Production guide
