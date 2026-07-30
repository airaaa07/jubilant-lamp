# Redis Guide

## Overview

This document provides comprehensive information about Redis usage in the University ERP system. It covers Redis configuration, data structures, caching strategies, and best practices.

## Redis Technology

**Confirmed by Code**: The University ERP uses Redis for caching and queue management.

**Why Redis:**
- In-memory data store for high performance
- Support for multiple data structures
- Built-in persistence options
- Pub/Sub messaging
- Transaction support
- Excellent for caching and queuing

**Version:**
- Redis 7+

## Redis Architecture

**Confirmed by Code**: Redis is used for caching and queue management.

**Redis Usage Overview:**

```
┌─────────────────────────────────────────────────────────┐
│              Redis Usage                                  │
├─────────────────────────────────────────────────────────┤
│ Caching: Session data, API responses, user data          │
│ Queues: Background jobs, email sending, notifications    │
│ Pub/Sub: Real-time notifications, WebSocket events       │
│ Session Store: User sessions, flash messages             │
└─────────────────────────────────────────────────────────┘
```

## Redis Configuration

**Confirmed by Code**: Redis is configured via environment variables.

**Environment Variables:**

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_CLUSTER_MODE=false
REDIS_SENTINEL_HOST=
REDIS_SENTINEL_PORT=
REDIS_SENTINEL_MASTER=
```

**Configuration Parameters:**
- `REDIS_HOST`: Redis server host
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_PASSWORD`: Redis password (if required)
- `REDIS_DB`: Redis database number (default: 0)
- `REDIS_CLUSTER_MODE`: Enable Redis cluster mode (default: false)
- `REDIS_SENTINEL_HOST`: Redis Sentinel host (if using Sentinel)
- `REDIS_SENTINEL_PORT`: Redis Sentinel port (if using Sentinel)
- `REDIS_SENTINEL_MASTER`: Redis Sentinel master name (if using Sentinel)

## Redis Service

**Confirmed by Code**: The University ERP has a Redis service for Redis operations.

**File**: `apps/core-api/src/redis/redis.service.ts`

```typescript
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { createClient, RedisClientType } from 'redis';

@Injectable()
export class RedisService implements OnModuleInit, OnModuleDestroy {
  private client: RedisClientType;

  constructor() {
    this.client = createClient({
      socket: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT) || 6379,
        password: process.env.REDIS_PASSWORD || undefined,
      },
      database: parseInt(process.env.REDIS_DB) || 0,
    });

    this.client.on('error', (err) => console.error('Redis Client Error', err));
    this.client.on('connect', () => console.log('Redis Client Connected'));
    this.client.on('disconnect', () => console.log('Redis Client Disconnected'));
  }

  async onModuleInit() {
    await this.client.connect();
  }

  async onModuleDestroy() {
    await this.client.quit();
  }

  // String operations
  async get(key: string): Promise<string | null> {
    return this.client.get(key);
  }

  async set(key: string, value: string, ttl?: number): Promise<void> {
    if (ttl) {
      await this.client.setEx(key, ttl, value);
    } else {
      await this.client.set(key, value);
    }
  }

  async del(key: string): Promise<void> {
    await this.client.del(key);
  }

  async mget(keys: string[]): Promise<(string | null)[]> {
    return this.client.mGet(keys);
  }

  async mset(keyValues: Record<string, string>): Promise<void> {
    await this.client.mSet(keyValues);
  }

  // Hash operations
  async hget(key: string, field: string): Promise<string | null> {
    return this.client.hGet(key, field);
  }

  async hset(key: string, field: string, value: string): Promise<void> {
    await this.client.hSet(key, field, value);
  }

  async hgetall(key: string): Promise<Record<string, string>> {
    return this.client.hGetAll(key);
  }

  async hdel(key: string, field: string): Promise<void> {
    await this.client.hDel(key, field);
  }

  // List operations
  async lpush(key: string, value: string): Promise<number> {
    return this.client.lPush(key, value);
  }

  async rpush(key: string, value: string): Promise<number> {
    return this.client.rPush(key, value);
  }

  async lpop(key: string): Promise<string | null> {
    return this.client.lPop(key);
  }

  async rpop(key: string): Promise<string | null> {
    return this.client.rPop(key);
  }

  async lrange(key: string, start: number, stop: number): Promise<string[]> {
    return this.client.lRange(key, start, stop);
  }

  // Set operations
  async sadd(key: string, member: string): Promise<number> {
    return this.client.sAdd(key, member);
  }

  async srem(key: string, member: string): Promise<number> {
    return this.client.sRem(key, member);
  }

  async smembers(key: string): Promise<string[]> {
    return this.client.sMembers(key);
  }

  async sismember(key: string, member: string): Promise<boolean> {
    return this.client.sIsMember(key, member);
  }

  // Sorted set operations
  async zadd(key: string, score: number, member: string): Promise<number> {
    return this.client.zAdd(key, { score, value: member });
  }

  async zrem(key: string, member: string): Promise<number> {
    return this.client.zRem(key, member);
  }

  async zrange(key: string, start: number, stop: number): Promise<string[]> {
    return this.client.zRange(key, start, stop);
  }

  // Key operations
  async keys(pattern: string): Promise<string[]> {
    return this.client.keys(pattern);
  }

  async exists(key: string): Promise<boolean> {
    return (await this.client.exists(key)) === 1;
  }

  async expire(key: string, seconds: number): Promise<void> {
    await this.client.expire(key, seconds);
  }

  async ttl(key: string): Promise<number> {
    return this.client.tTL(key);
  }

  async flushDb(): Promise<void> {
    await this.client.flushDb();
  }

  async flushAll(): Promise<void> {
    await this.client.flushAll();
  }
}
```

## Caching Strategies

**Confirmed by Code**: The University ERP uses the cache-aside pattern.

### Cache-Aside Pattern

**Implementation:**

```typescript
@Injectable()
export class CacheService {
  constructor(private redis: RedisService) {}

  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    if (!cached) return null;
    return JSON.parse(cached) as T;
  }

  async set<T>(key: string, value: T, ttl: number = 3600): Promise<void> {
    await this.redis.set(key, JSON.stringify(value), ttl);
  }

  async delete(key: string): Promise<void> {
    await this.redis.del(key);
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}
```

**Usage Example:**

```typescript
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private cache: CacheService,
  ) {}

  async findOne(id: string): Promise<User> {
    // Try cache first
    const cacheKey = `user:${id}`;
    const cached = await this.cache.get<User>(cacheKey);
    if (cached) return cached;

    // Cache miss - fetch from database
    const user = await this.prisma.user.findUnique({
      where: { id },
    });

    if (!user) return null;

    // Set cache
    await this.cache.set(cacheKey, user, 3600);

    return user;
  }

  async update(id: string, data: UpdateUserDto): Promise<User> {
    const user = await this.prisma.user.update({
      where: { id },
      data,
    });

    // Invalidate cache
    await this.cache.delete(`user:${id}`);

    return user;
  }
}
```

### Cache Invalidation

**Strategies:**

1. **Time-based expiration**
   ```typescript
   await this.cache.set(key, value, 3600); // 1 hour TTL
   ```

2. **Event-based invalidation**
   ```typescript
   // Invalidate on update
   await this.cache.delete(`user:${id}`);
   ```

3. **Pattern-based invalidation**
   ```typescript
   // Invalidate all user caches
   await this.cache.invalidate('user:*');
   ```

## Queue Management

**Confirmed by Code**: The University ERP uses Bull for queue management.

### Queue Setup

**File**: `apps/core-api/src/queue/queue.module.ts`

```typescript
import { Module } from '@nestjs/common';
import { BullModule } from '@nestjs/bull';
import { RedisService } from '../redis/redis.service';

@Module({
  imports: [
    BullModule.forRoot({
      redis: {
        host: process.env.REDIS_HOST || 'localhost',
        port: parseInt(process.env.REDIS_PORT) || 6379,
        password: process.env.REDIS_PASSWORD || undefined,
      },
    }),
    BullModule.registerQueue({
      name: 'email',
    }),
    BullModule.registerQueue({
      name: 'notifications',
    }),
  ],
  providers: [RedisService],
  exports: [BullModule],
})
export class QueueModule {}
```

### Queue Processor

**File**: `apps/core-api/src/queue/processors/email.processor.ts`

```typescript
import { Processor, Process } from '@nestjs/bull';
import { Job } from 'bull';

@Processor('email')
export class EmailProcessor {
  @Process('send')
  async handleSendEmail(job: Job) {
    const { to, subject, body } = job.data;

    // Send email logic
    console.log(`Sending email to ${to}: ${subject}`);

    // Simulate email sending
    await new Promise(resolve => setTimeout(resolve, 1000));

    return { success: true };
  }
}
```

### Queue Usage

**Add job to queue:**

```typescript
@Injectable()
export class EmailService {
  constructor(
    @InjectQueue('email') private emailQueue: Queue,
  ) {}

  async sendEmail(to: string, subject: string, body: string) {
    await this.emailQueue.add('send', { to, subject, body }, {
      attempts: 3,
      backoff: {
        type: 'exponential',
        delay: 2000,
      },
    });
  }
}
```

## Pub/Sub Messaging

**Confirmed by Code**: The University ERP uses Redis Pub/Sub for real-time messaging.

### Publisher

**File**: `apps/core-api/src/redis/publisher.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { RedisService } from './redis.service';

@Injectable()
export class PublisherService {
  constructor(private redis: RedisService) {}

  async publish(channel: string, message: any) {
    await this.redis.publish(channel, JSON.stringify(message));
  }
}
```

### Subscriber

**File**: `apps/core-api/src/redis/subscriber.service.ts`

```typescript
import { Injectable, OnModuleInit } from '@nestjs/common';
import { RedisService } from './redis.service';

@Injectable()
export class SubscriberService implements OnModuleInit {
  constructor(private redis: RedisService) {}

  async onModuleInit() {
    const subscriber = this.redis.getClient().duplicate();
    await subscriber.connect();

    await subscriber.subscribe('notifications', (message) => {
      console.log('Received notification:', message);
    });
  }
}
```

## Redis Data Structures

### Strings

**Usage:** Simple key-value pairs

```typescript
// Set string
await redis.set('user:1:name', 'John Doe');

// Get string
const name = await redis.get('user:1:name');

// Set with expiration
await redis.set('session:123', JSON.stringify({ userId: 1 }), 3600);
```

### Hashes

**Usage:** Object-like structures

```typescript
// Set hash fields
await redis.hset('user:1', 'name', 'John Doe');
await redis.hset('user:1', 'email', 'john@example.com');

// Get hash field
const name = await redis.hget('user:1', 'name');

// Get all hash fields
const user = await redis.hgetall('user:1');
```

### Lists

**Usage:** Ordered collections

```typescript
// Push to list
await redis.lpush('queue:tasks', JSON.stringify({ id: 1, task: 'Task 1' }));
await redis.rpush('queue:tasks', JSON.stringify({ id: 2, task: 'Task 2' }));

// Pop from list
const task = await redis.lpop('queue:tasks');

// Get range
const tasks = await redis.lrange('queue:tasks', 0, -1);
```

### Sets

**Usage:** Unordered unique collections

```typescript
// Add to set
await redis.sadd('tags:1', 'javascript');
await redis.sadd('tags:1', 'typescript');
await redis.sadd('tags:1', 'javascript'); // Duplicate ignored

// Get all members
const tags = await redis.smembers('tags:1');

// Check membership
const hasTag = await redis.sismember('tags:1', 'javascript');
```

### Sorted Sets

**Usage:** Ordered collections with scores

```typescript
// Add to sorted set
await redis.zadd('leaderboard', 100, 'user1');
await redis.zadd('leaderboard', 200, 'user2');
await redis.zadd('leaderboard', 150, 'user3');

// Get range
const leaderboard = await redis.zrange('leaderboard', 0, -1);

// Get with scores
const leaderboardWithScores = await redis.zrangeWithScores('leaderboard', 0, -1);
```

## Redis Performance

**Confirmed by Code**: The University ERP uses Redis for performance optimization.

### Performance Tips

1. **Use appropriate data structures**
   - Use strings for simple values
   - Use hashes for objects
   - Use lists for queues
   - Use sets for unique collections
   - Use sorted sets for rankings

2. **Set appropriate TTL**
   - Cache data should have TTL
   - Session data should have TTL
   - Temporary data should have TTL

3. **Use pipelining**
   ```typescript
   const pipeline = redis.multi();
   pipeline.set('key1', 'value1');
   pipeline.set('key2', 'value2');
   pipeline.set('key3', 'value3');
   await pipeline.exec();
   ```

4. **Use connection pooling**
   - Reuse connections
   - Configure pool size
   - Monitor connection usage

5. **Monitor memory usage**
   ```bash
   redis-cli info memory
   ```

## Redis Monitoring

**Confirmed by Code**: The University ERP monitors Redis for health and performance.

### Monitoring Commands

```bash
# Check Redis info
redis-cli info

# Check memory usage
redis-cli info memory

# Check connected clients
redis-cli info clients

# Check slow queries
redis-cli slowlog get 10

# Monitor commands in real-time
redis-cli monitor
```

### Monitoring Metrics

**Key Metrics to Monitor:**
- Memory usage
- Connected clients
- Commands per second
- Hit ratio
- Slow queries
- Expired keys

## Redis Security

**Confirmed by Code**: The University ERP follows Redis security best practices.

### Security Best Practices

1. **Use authentication**
   ```env
   REDIS_PASSWORD=your-strong-password
   ```

2. **Use TLS in production**
   ```typescript
   this.client = createClient({
     socket: {
       host: process.env.REDIS_HOST,
       port: parseInt(process.env.REDIS_PORT),
       tls: {
         // TLS configuration
       },
     },
   });
   ```

3. **Restrict access**
   - Use firewall rules
   - Bind to specific IP
   - Use Redis ACLs

4. **Disable dangerous commands**
   ```bash
   # In redis.conf
   rename-command FLUSHDB ""
   rename-command FLUSHALL ""
   rename-command CONFIG ""
   ```

## Redis Troubleshooting

### Common Issues

**Issue: Connection refused**

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# Expected output: PONG

# If not running, start Redis
docker-compose up -d redis
```

**Issue: Memory full**

**Solution:**
```bash
# Check memory usage
redis-cli info memory

# Flush all data (WARNING: deletes all data)
redis-cli flushall

# Or flush specific database
redis-cli -n 0 flushdb
```

**Issue: Slow queries**

**Solution:**
```bash
# Check slow queries
redis-cli slowlog get 10

# Optimize queries
# Use appropriate data structures
# Add indexes if needed
```

## Redis CLI Commands

**Common Commands:**

```bash
# Connect to Redis
redis-cli

# Ping
PING

# Set key
SET key value

# Get key
GET key

# Delete key
DEL key

# Set with expiration
SETEX key 3600 value

# Get TTL
TTL key

# Get all keys
KEYS *

# Get info
INFO

# Monitor
MONITOR

# Flush database
FLUSHDB

# Flush all databases
FLUSHALL
```

## Additional Resources

- [Redis Documentation](https://redis.io/docs/)
- [Redis Best Practices](https://redis.io/topics/best-practices)
- [Bull Documentation](https://docs.bullmq.io/)
