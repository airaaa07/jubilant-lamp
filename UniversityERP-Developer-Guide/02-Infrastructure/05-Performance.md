# Infrastructure Performance

## Purpose

This document explains the performance considerations and optimizations for the University ERP infrastructure. It details how to optimize Docker services, networking, storage, and overall infrastructure performance.

## Why This Document Exists

**Confirmed by Code**: The University ERP infrastructure performance is critical for application performance. Understanding infrastructure performance is critical for:
- Optimizing application performance
- Identifying bottlenecks
- Planning capacity
- Reducing costs
- Improving user experience

Without understanding infrastructure performance, the application may be slow or unresponsive.

## Where This Is Used

- **Development**: Optimizing local development environment
- **Deployment**: Optimizing production deployment
- **Performance Tuning**: Tuning infrastructure for performance
- **Capacity Planning**: Planning for growth
- **Cost Optimization**: Reducing infrastructure costs

## Dependencies

### Performance Dependencies

**Confirmed by Code**: Infrastructure performance depends on:

- **Hardware**: CPU, RAM, Disk, Network
- **Docker**: Container overhead
- **Services**: PostgreSQL, Redis, MinIO, Elasticsearch
- **Networking**: Network latency, bandwidth
- **Storage**: Disk IOPS, throughput

## Internal Architecture

### Performance Layers

**Confirmed by Code**: Performance considerations at multiple layers.

```
┌─────────────────────────────────────────────────────────┐
│              Performance Layers                           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Hardware     │  │  Docker         │  │  Services      │
│  (CPU, RAM)   │  │  (Overhead)     │  │  (Config)      │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Networking   │  │  Storage       │  │  Application   │
│  (Latency)    │  │  (IOPS)        │  │  (Optimization) │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Docker Performance

**Confirmed by Code**: Docker configuration affects performance.

**Resource Limits**:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

**What This Does**:
- Limits CPU to 2 cores
- Limits memory to 2GB
- Reserves 1 CPU core
- Reserves 1GB memory
- Prevents resource starvation

**Performance Impact**:
- Prevents one service from consuming all resources
- Ensures predictable performance
- Enables better resource utilization

### PostgreSQL Performance

**Confirmed by Code**: PostgreSQL configuration affects performance.

**Configuration**:
```yaml
services:
  postgres:
    image: postgres:16-alpine
    command:
      - postgres
      - -c
      - shared_buffers=256MB
      - -c
      - effective_cache_size=1GB
      - -c
      - maintenance_work_mem=64MB
      - -c
      - checkpoint_completion_target=0.9
      - -c
      - wal_buffers=16MB
      - -c
      - default_statistics_target=100
      - -c
      - random_page_cost=1.1
      - -c
      - effective_io_concurrency=200
      - -c
      - work_mem=1310kB
      - -c
      - min_wal_size=1GB
      - -c
      - max_wal_size=4GB
```

**What This Does**:
- **shared_buffers**: Memory for shared data buffers
- **effective_cache_size**: Memory available for disk caching
- **maintenance_work_mem**: Memory for maintenance operations
- **work_mem**: Memory for sorting and hashing
- **wal_buffers**: Memory for WAL (Write-Ahead Log)

**Performance Impact**:
- Better query performance
- Reduced disk I/O
- Faster operations

### Redis Performance

**Confirmed by Code**: Redis configuration affects performance.

**Configuration**:
```yaml
services:
  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

**What This Does**:
- **maxmemory**: Maximum memory Redis can use
- **maxmemory-policy**: Policy for key eviction when memory is full

**Eviction Policies**:
- **noeviction**: Don't evict any keys
- **allkeys-lru**: Evict least recently used keys
- **volatile-lru**: Evict least recently used keys with expiry
- **allkeys-random**: Evict random keys
- **volatile-random**: Evict random keys with expiry

**Performance Impact**:
- Prevents out-of-memory errors
- Ensures cache stays within limits
- Optimizes cache hit rate

### MinIO Performance

**Confirmed by Code**: MinIO configuration affects performance.

**Configuration**:
```yaml
services:
  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_CACHE_DRIVES: /data
      MINIO_CACHE_EXPIRY: 90
      MINIO_CACHE_QUOTA: 80
```

**What This Does**:
- **MINIO_CACHE_DRIVES**: Cache drive location
- **MINIO_CACHE_EXPIRY**: Cache expiry in days
- **MINIO_CACHE_QUOTA**: Cache quota percentage

**Performance Impact**:
- Faster object retrieval
- Reduced disk I/O
- Better performance for frequently accessed objects

## Database Interactions

### PostgreSQL Connection Pooling

**Confirmed by Code**: Connection pooling affects performance.

**Configuration**:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp?connection_limit=10&pool_timeout=20
```

**What This Does**:
- **connection_limit**: Maximum number of connections in pool
- **pool_timeout**: Timeout for getting connection from pool

**Performance Impact**:
- Reuses connections
- Reduces connection overhead
- Better performance under load

### PostgreSQL Indexing

**Confirmed by Code**: Indexes affect query performance.

**Example**:
```prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  @@index([email])
}
```

**What This Does**:
- Creates index on email column
- Speeds up queries filtering by email
- Slows down writes (index maintenance)

**Performance Impact**:
- Faster reads
- Slower writes
- Trade-off between read and write performance

## Redis Interactions

### Redis Caching Strategy

**Confirmed by Code**: Caching strategy affects performance.

**Pattern**:
```typescript
async getData(id: string) {
  const cacheKey = `data:${id}`;
  const cached = await this.redis.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const data = await this.prisma.data.findUnique({ where: { id } });
  await this.redis.setex(cacheKey, 300, JSON.stringify(data));
  
  return data;
}
```

**What This Does**:
- Checks cache first
- Returns cached data if available
- Queries database on cache miss
- Stores result in cache with TTL

**Performance Impact**:
- Reduced database load
- Faster response times
- Better performance under load

### Redis Pipeline

**Confirmed by Code**: Redis pipeline affects performance.

**Pattern**:
```typescript
const pipeline = this.redis.pipeline();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.set('key3', 'value3');
await pipeline.exec();
```

**What This Does**:
- Batches multiple Redis commands
- Reduces network round trips
- Improves throughput

**Performance Impact**:
- Reduced network latency
- Higher throughput
- Better performance for bulk operations

## Queue Interactions

### Bull Queue Performance

**Confirmed by Code**: Queue configuration affects performance.

**Configuration**:
```typescript
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT),
    maxRetriesPerRequest: 3,
    retryStrategy: (times) => Math.min(times * 50, 2000),
  },
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 100,
    removeOnFail: 50,
  },
});
```

**What This Does**:
- **maxRetriesPerRequest**: Max retries for Redis commands
- **retryStrategy**: Retry strategy for failed jobs
- **attempts**: Number of retry attempts
- **backoff**: Backoff strategy for retries
- **removeOnComplete**: Remove completed jobs after N
- **removeOnFail**: Remove failed jobs after N

**Performance Impact**:
- Better error handling
- Reduced queue backlog
- Better performance under load

## Worker Interactions

### Worker Performance

**Confirmed by Code**: Worker configuration affects performance.

**Configuration**:
```yaml
services:
  notification-worker:
    deploy:
      replicas: 3
    environment:
      - CONCURRENCY=10
```

**What This Does**:
- **replicas**: Number of worker instances
- **CONCURRENCY**: Number of concurrent jobs per worker

**Performance Impact**:
- Higher throughput
- Better job processing
- Reduced queue backlog

## Business Rules

### Performance Rules

**Confirmed by Code**: Performance follows these rules:

1. **Resource Limits**: Set resource limits for all services
2. **Connection Pooling**: Use connection paging for databases
3. **Caching**: Cache frequently accessed data
4. **Indexing**: Add indexes for frequently queried columns
5. **Monitoring**: Monitor performance metrics

### Optimization Rules

**Confirmed by Code**: Optimization follows these rules:

1. **Profile First**: Profile before optimizing
2. **Optimize Bottlenecks**: Focus on bottlenecks
3. **Measure Impact**: Measure before and after
4. **Trade-offs**: Consider trade-offs
5. **Monitor**: Monitor after optimization

## Security

### Performance Security

**Confirmed by Code**: Security considerations for performance:

1. **No Security Trade-offs**: Don't compromise security for performance
2. **Secure Caching**: Cache sensitive data carefully
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Resource Limits**: Prevent resource exhaustion attacks

## Performance Considerations

### Hardware Requirements

**Confirmed by Code**: Hardware affects performance.

**Development**:
- **CPU**: 4 cores
- **RAM**: 8GB
- **Disk**: SSD, 50GB
- **Network**: 100Mbps

**Production**:
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Disk**: SSD, 200GB+
- **Network**: 1Gbps+

### Docker Overhead

**Confirmed by Code**: Docker has performance overhead.

**Overhead**:
- **CPU**: 1-2% overhead
- **Memory**: 50-100MB per container
- **Network**: Minimal overhead
- **Disk**: Minimal overhead

**Mitigation**:
- Use lightweight images (Alpine)
- Limit container resources
- Use host networking if needed

## Common Mistakes

### Mistake 1: Not Setting Resource Limits

**Symptom**: One service consuming all resources

**Cause**: Not setting resource limits

**Fix**:
```yaml
services:
  postgres:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

### Mistake 2: Not Using Connection Pooling

**Symptom**: Database connection errors under load

**Cause**: Not using connection pooling

**Fix**:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp?connection_limit=10
```

### Mistake 3: Not Caching

**Symptom**: Slow API responses

**Cause**: Not caching frequently accessed data

**Fix**:
```typescript
// Add caching
const cached = await this.redis.get(cacheKey);
if (cached) return JSON.parse(cached);
```

## Debugging Guide

### Performance Debugging

**Issue**: Slow performance

**Investigation**:
1. Check resource usage: `docker stats`
2. Check database performance: `docker-compose exec postgres pg_stat_activity`
3. Check cache hit rate: `docker-compose exec redis redis-cli INFO stats`
4. Check network latency: `ping`
5. Check disk I/O: `iostat`

**Tools**:
- Docker stats
- PostgreSQL EXPLAIN ANALYZE
- Redis INFO commands
- System monitoring tools

## Future Enhancements

### Performance Monitoring

**Status**: Not implemented

**Proposal**: Implement performance monitoring:
- Prometheus for metrics collection
- Grafana for visualization
- APM tools (New Relic, Datadog)
- Custom dashboards
- Alerting on thresholds

### Auto-scaling

**Status**: Not implemented

**Proposal**: Implement auto-scaling:
- Kubernetes HPA
- Docker Swarm scaling
- Auto-scale based on metrics
- Scale up/down based on load
- Cost optimization

## Production Considerations

### Production Performance

**Production Deployment**:
- Use managed services (AWS RDS, ElastiCache, S3)
- Configure appropriate resource limits
- Enable connection pooling
- Configure caching
- Monitor performance metrics
- Implement alerting

### Performance Monitoring

**Monitoring Metrics**:
- CPU usage
- Memory usage
- Disk I/O
- Network latency
- Database query performance
- Cache hit rate
- Queue backlog
- Response times

## Example Requests

### Check Resource Usage

**Request**:
```bash
docker stats
```

**Response**:
```
CONTAINER ID   NAME                      CPU %     MEM USAGE / LIMIT
abc123         university-erp-postgres    5.2%      512Mi / 2Gi
def456         university-erp-redis       2.1%      256Mi / 512Mi
```

### Check Database Performance

**Request**:
```bash
docker-compose exec postgres pg_stat_activity
```

**Response**:
```
datid | datname | pid  | state
-------+---------+------+--------
12345 | university_erp | 123 | active
```

## Example Responses

### Performance Metrics

**Request**: Get performance metrics

**Response**:
```json
{
  "cpu_usage": "5.2%",
  "memory_usage": "512Mi / 2Gi",
  "disk_iops": 1000,
  "network_latency": "1ms",
  "cache_hit_rate": "90%",
  "query_time_avg": "50ms"
}
```

## Sequence Diagrams

### Performance Optimization Flow

```
Performance Issue
        ↓
    Identify Bottleneck
        ↓
    Profile System
        ↓
    Identify Root Cause
        ↓
    Implement Optimization
        ↓
    Measure Impact
        ↓
    Monitor Performance
```

## Architecture Diagrams

### Performance Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Hardware Layer                            │
│  CPU: 8 cores, RAM: 16GB, Disk: SSD 200GB               │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Docker Layer                             │
│  Resource limits, connection pooling, caching           │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Service Layer                            │
│  PostgreSQL, Redis, MinIO, Elasticsearch                │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                         │
│  Core API, CBE Engine, Workers                         │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you optimize PostgreSQL performance?

**Answer**: PostgreSQL optimization via:
- Connection pooling
- Indexing frequently queried columns
- Tuning configuration parameters (shared_buffers, work_mem)
- Using EXPLAIN ANALYZE to identify slow queries
- Partitioning large tables
- Using read replicas

### Q2: How do you optimize Redis performance?

**Answer**: Redis optimization via:
- Setting maxmemory and eviction policy
- Using Redis pipeline for bulk operations
- Using Redis clustering for horizontal scaling
- Monitoring cache hit rate
- Optimizing cache key design

### Q3: How do you monitor infrastructure performance?

**Answer**: Monitoring via:
- Docker stats for container metrics
- PostgreSQL pg_stat_activity for database metrics
- Redis INFO commands for cache metrics
- System monitoring tools (top, iostat)
- Future: Prometheus + Grafana

## Exercises

### Exercise 1: Optimize PostgreSQL

**Task**: Optimize PostgreSQL performance.

**Steps**:
1. Check slow queries
2. Add indexes
3. Tune configuration
4. Test performance
5. Measure impact

**Verification**:
- Queries faster
- Performance improved
- Metrics better

### Exercise 2: Optimize Redis

**Task**: Optimize Redis performance.

**Steps**:
1. Check cache hit rate
2. Optimize cache keys
3. Configure eviction policy
4. Use pipeline for bulk ops
5. Test performance

**Verification**:
- Cache hit rate improved
- Performance improved
- Metrics better

## Real Production Scenarios

### Scenario 1: Database Slow Under Load

**Situation**: PostgreSQL slow under high load

**Response**:
1. Check connection pool size
2. Check slow queries
3. Add indexes
4. Tune configuration
5. Add read replicas
6. Monitor performance

### Scenario 2: Cache Miss Rate High

**Situation**: Redis cache miss rate high

**Response**:
1. Check cache key design
2. Check TTL values
3. Check cache size
4. Adjust eviction policy
5. Increase cache size
6. Monitor hit rate

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [04-Environment-Variables](./04-Environment-Variables.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [18-Performance](../18-Performance/README.md) - Performance guide
- [17-Production](../17-Production/README.md) - Production guide
