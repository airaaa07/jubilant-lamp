# University ERP - Redis

## Overview

**Redis 7** is used in the system for multiple purposes:

- **Session Storage**: JWT refresh tokens
- **Caching**: Application data caching
- **Queue Backend**: Bull job queues
- **Pub/Sub**: Real-time notifications (potential)

## Technology Stack

- **Redis 7.x**: In-memory data store
- **ioredis 5.x**: Redis client for Node.js
- **Bull 4.x**: Queue library using Redis

## Architecture

```
┌─────────────────┐
│   Core API      │
│                 │
│  RedisService   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│     Redis       │
│                 │
│  In-Memory DB   │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌────────┐
│ Cache  │ │ Queues │
└────────┘ └────────┘
```

## Redis Service

### Location

- **Module**: `apps/core-api/src/infrastructure/redis/`
- **Service**: `RedisService`
- **Module**: `RedisModule` (global)

### Service Implementation

```typescript
// apps/core-api/src/infrastructure/redis/redis.service.ts
@Injectable()
export class RedisService extends Redis implements OnModuleDestroy {
  constructor(configService: ConfigService) {
    super({
      host: configService.get<string>('REDIS_HOST', 'localhost'),
      port: configService.get<number>('REDIS_PORT', 6379),
    });
  }

  async onModuleDestroy() {
    await this.quit();
  }
}
```

### Environment Variables

```bash
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Docker Configuration

```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - ./docker-volumes/redis:/data
  command: redis-server --appendonly yes
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 30s
    timeout: 20s
    retries: 3
```

## Usage Patterns

### Session Storage

JWT refresh tokens are stored in Redis:

```typescript
// In auth service
await redisService.setex(
  `refresh:${userId}`,
  7 * 24 * 60 * 60, // 7 days in seconds
  refreshToken
);

// Verify refresh token
const storedToken = await redisService.get(`refresh:${userId}`);
```

### Caching

Frequently accessed data is cached:

```typescript
// Cache university data
const cacheKey = `university:${universityId}`;
const cached = await redisService.get(cacheKey);

if (cached) {
  return JSON.parse(cached);
}

const university = await prisma.university.findUnique({
  where: { id: universityId },
});

await redisService.setex(
  cacheKey,
  300, // 5 minutes
  JSON.stringify(university)
);

return university;
```

### Cache Invalidation

Cache is invalidated on data updates:

```typescript
// Update university
await prisma.university.update({
  where: { id: universityId },
  data: updateData,
});

// Invalidate cache
await redisService.del(`university:${universityId}`);
```

### Queue Backend

Bull queues use Redis as backend:

```typescript
// Queue configuration
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT),
  },
});
```

## Common Operations

### Set Value

```typescript
await redisService.set('key', 'value');
```

### Set with Expiry

```typescript
await redisService.setex('key', 3600, 'value'); // 1 hour
```

### Get Value

```typescript
const value = await redisService.get('key');
```

### Delete Value

```typescript
await redisService.del('key');
```

### Set Hash

```typescript
await redisService.hset('user:123', {
  name: 'John',
  email: 'john@example.com',
});
```

### Get Hash

```typescript
const user = await redisService.hgetall('user:123');
```

### Delete Hash

```typescript
await redisService.del('user:123');
```

### Set List

```typescript
await redisService.lpush('notifications', JSON.stringify(notification));
```

### Get List

```typescript
const notifications = await redisService.lrange('notifications', 0, -1);
```

### Set Set

```typescript
await redisService.sadd('online-users', userId);
```

### Check Set Membership

```typescript
const isOnline = await redisService.sismember('online-users', userId);
```

## Cache Strategies

### Cache-Aside

```typescript
async getUser(userId: string) {
  const cacheKey = `user:${userId}`;
  const cached = await redisService.get(cacheKey);

  if (cached) {
    return JSON.parse(cached);
  }

  const user = await prisma.user.findUnique({
    where: { id: userId },
  });

  if (user) {
    await redisService.setex(cacheKey, 300, JSON.stringify(user));
  }

  return user;
}
```

### Write-Through

```typescript
async updateUser(userId: string, data: any) {
  const user = await prisma.user.update({
    where: { id: userId },
    data,
  });

  await redisService.setex(
    `user:${userId}`,
    300,
    JSON.stringify(user)
  );

  return user;
}
```

### Write-Behind

```typescript
async updateUser(userId: string, data: any) {
  // Update cache immediately
  await redisService.setex(
    `user:${userId}`,
    300,
    JSON.stringify(data)
  );

  // Update database asynchronously
  setImmediate(async () => {
    await prisma.user.update({
      where: { id: userId },
      data,
    });
  });
}
```

## Cache Keys

### Naming Convention

```
{entity}:{id}
{entity}:{id}:{field}
{entity}:{id}:{relation}:{id}
```

### Examples

```
university:123
institute:456
user:789
user:789:profile
batch:101:students
exam:202:attempts
```

## Cache Expiry

### Common TTL Values

- **User data**: 5 minutes (300s)
- **Master data**: 1 hour (3600s)
- **Configuration**: 10 minutes (600s)
- **Session tokens**: 7 days (604800s)
- **OTP codes**: 10 minutes (600s)

## Redis Data Structures

### Strings

- **Use case**: Simple key-value pairs
- **Example**: Cache university data

### Hashes

- **Use case**: Object-like data
- **Example**: User profile data

### Lists

- **Use case**: Ordered collections
- **Example**: Notification queue

### Sets

- **Use case**: Unique collections
- **Example**: Online users

### Sorted Sets

- **Use case**: Ranked collections
- **Example**: Leaderboards (not currently used)

## Performance Considerations

### Memory Usage

Monitor Redis memory usage:

```bash
redis-cli INFO memory
```

### Eviction Policy

Configure eviction policy in redis.conf:

```
maxmemory 256mb
maxmemory-policy allkeys-lru
```

### Connection Pooling

ioredis handles connection pooling automatically.

### Pipeline Operations

Batch multiple operations:

```typescript
const pipeline = redisService.pipeline();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.set('key3', 'value3');
await pipeline.exec();
```

## Monitoring

### Health Check

```typescript
async healthCheck(): Promise<boolean> {
  try {
    await redisService.ping();
    return true;
  } catch (error) {
    return false;
  }
}
```

### Metrics

- **Memory usage**: Used memory vs max memory
- **Hit rate**: Cache hit / (cache hit + cache miss)
- **Connections**: Number of active connections
- **Operations per second**: OPS metric

### Commands

```bash
# Get info
redis-cli INFO

# Monitor commands
redis-cli MONITOR

# Slow log
redis-cli SLOWLOG GET 10
```

## Backup Strategy

### RDB Snapshots

Redis automatically creates RDB snapshots:

```
save 900 1
save 300 10
save 60 10000
```

### AOF (Append Only File)

Enable AOF for durability:

```
appendonly yes
appendfsync everysec
```

### Docker Volume Backup

```bash
# Backup Redis data
docker run --rm -v docker-volumes_redis:/data -v $(pwd):/backup \
  alpine tar czf /backup/redis-backup.tar.gz /data
```

## Security Considerations

### Authentication

Configure Redis password in redis.conf:

```
requirepass yourpassword
```

### TLS/SSL

Enable TLS for secure connections:

```
tls-port 6379
port 0
tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
```

### Network Isolation

- Bind to localhost in development
- Use firewall rules in production
- Don't expose Redis to public internet

## Known Limitations

1. **No Redis Cluster**: Single Redis instance
2. **No Sentinel**: No high availability
3. **No Persistence**: AOF not enabled by default
4. **No Encryption**: No TLS in development
5. **Limited Monitoring**: No Redis Exporter configured

## Future Enhancements

1. **Redis Cluster**: Add clustering for scalability
2. **Sentinel**: Add high availability
3. **AOF Persistence**: Enable AOF for durability
4. **TLS Encryption**: Enable TLS in production
5. **Redis Exporter**: Add Prometheus metrics
6. **Cache Warming**: Warm cache on startup
7. **Cache Partitioning**: Partition cache by entity type
8. **Pub/Sub**: Use for real-time notifications
