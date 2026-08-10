# 12-Redis

## Purpose

This folder provides comprehensive documentation about Redis in the University ERP system. It details how Redis is used for caching, queue storage, session management, and other use cases.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses Redis for multiple purposes. Understanding Redis is critical for:
- Implementing caching
- Managing queues
- Storing sessions
- Improving performance
- Debugging Redis issues

Without understanding Redis, developers may struggle with caching or may introduce Redis-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn Redis
- **Feature Development**: Implementing Redis features
- **Code Reviews**: Reviewing Redis code
- **Caching**: Implementing caching
- **Queues**: Managing queue storage

## Dependencies

### Redis Dependencies

**Confirmed by Code**: Redis depends on:

- **ioredis**: Redis client for Node.js
- **NestJS**: Framework for Redis integration
- **Bull**: Queue library using Redis
- **Environment Variables**: Redis configuration

## Internal Architecture

### Redis Architecture

**Confirmed by Code**: Redis follows client-server architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Redis Client (ioredis)                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Redis Server                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Cache        │  │  Queue Storage  │  │  Session        │
│  (Key-Value)  │  │  (Bull)         │  │  (Session Data) │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Redis Service

**Confirmed by Code**: Redis service provides Redis client.

**RedisService**:
```typescript
import { Injectable, OnModuleDestroy } from '@nestjs/common';
import Redis from 'ioredis';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class RedisService extends Redis implements OnModuleDestroy {
  constructor(private configService: ConfigService) {
    super({
      host: configService.get('REDIS_HOST', 'localhost'),
      port: configService.get('REDIS_PORT', 6379),
      password: configService.get('REDIS_PASSWORD'),
      db: configService.get('REDIS_DB', 0),
    });
  }

  async onModuleDestroy() {
    await this.quit();
  }
}
```

**What This Does**:
- **ioredis**: Extends ioredis Redis client
- **Configuration**: Configures from environment variables
- **OnModuleDestroy**: Gracefully closes connection on shutdown

### Redis Module

**Confirmed by Code**: Redis module provides Redis integration.

**RedisModule**:
```typescript
import { Module, Global } from '@nestjs/common';
import { RedisService } from './redis.service';

@Global()
@Module({
  providers: [RedisService],
  exports: [RedisService],
})
export class RedisModule {}
```

**What This Does**:
- **@Global**: Makes module global
- **Providers**: Provides RedisService
- **Exports**: Exports RedisService for other modules

## Database Interactions

### Redis-Database Flow

**Confirmed by Code**: Redis doesn't interact with database directly.

**Flow**:
```
Redis → No database interaction
```

## Redis Interactions

### Redis-Redis Flow

**Confirmed by Code**: Redis interacts with Redis server.

**Flow**:
```
Application → Redis Client → Redis Server
```

## Queue Interactions

### Redis-Queue Flow

**Confirmed by Code**: Redis used for queue storage by Bull.

**Flow**:
```
Bull Queue → Redis Server → Bull Worker
```

## Worker Interactions

### Redis-Worker Flow

**Confirmed by Code**: Workers use Redis for queue storage.

**Flow**:
```
Worker → Redis Queue → Process Job
```

## Business Rules

### Redis Rules

**Confirmed by Code**: Redis follows these rules:

1. **Key-Value**: Redis is key-value store
2. **TTL**: Keys can have TTL (time to live)
3. **Data Types**: Supports multiple data types
4. **Persistence**: Can persist to disk
5. **Replication**: Supports replication

### Caching Rules

**Confirmed by Code**: Caching follows these rules:

1. **Cache Aside**: Cache-aside pattern
2. **TTL**: Set appropriate TTL
3. **Invalidation**: Invalidate on data change
4. **Cache Miss**: Handle cache miss
5. **Cache Hit**: Return cached data

## Security

### Redis Security

**Confirmed by Code**: Security considerations for Redis:

1. **Password**: Use Redis password
2. **Network**: Use private network or VPN
3. **Encryption**: Use TLS in production
4. **Access Control**: Restrict Redis access
5. **Sensitive Data**: Don't store sensitive data

## Performance Considerations

### Redis Performance

**Confirmed by Code**: Performance considerations:

1. **In-Memory**: Redis is in-memory, fast
2. **Connection Pooling**: Use connection pooling
3. **Pipeline**: Use pipeline for multiple commands
4. **Memory Usage**: Monitor memory usage
5. **Eviction Policy**: Configure eviction policy

## Common Mistakes

### Mistake 1: Not Setting TTL

**Symptom**: Memory leak

**Cause**: Not setting TTL on keys

**Fix**:
```typescript
// Set TTL
await this.redis.setex(key, 3600, value);
```

### Mistake 2: Not Handling Connection Errors

**Symptom**: Application crashes

**Cause**: Not handling Redis connection errors

**Fix**:
```typescript
// Add error handling
try {
  await this.redis.get(key);
} catch (error) {
  // Handle error
  return null;
}
```

### Mistake 3: Storing Large Objects

**Symptom**: Slow performance

**Cause**: Storing large objects in Redis

**Fix**:
```typescript
// Store only necessary data
const cachedData = {
  id: data.id,
  name: data.name,
  // Don't store large nested objects
};
```

## Debugging Guide

### Redis Debugging

**Issue**: Redis not working

**Investigation**:
1. Check Redis connection
2. Check Redis server status
3. Check Redis configuration
4. Check Redis logs
5. Check application logs

**Tools**:
- Redis CLI
- Redis logs
- Application logs
- Redis monitoring tools

## Future Enhancements

### Redis Cluster

**Status**: Not implemented

**Proposal**: Implement Redis cluster:
- High availability
- Automatic failover
- Better scalability
- More complex
- Better for production

### Redis Sentinel

**Status**: Not implemented

**Proposal**: Implement Redis sentinel:
- High availability
- Automatic failover
- Monitoring
- Better reliability
- More complex

## Production Considerations

### Production Redis

**Production Deployment**:
- Use Redis password
- Use TLS encryption
- Configure persistence
- Configure replication
- Monitor Redis performance

### Redis Monitoring

**Monitoring Metrics**:
- Memory usage
- Hit rate
- Miss rate
- Connection count
- Command rate

## Example Requests

### Redis Example

**Set Value**:
```typescript
await this.redis.set('key', 'value');
await this.redis.setex('key', 3600, 'value');
```

**Get Value**:
```typescript
const value = await this.redis.get('key');
```

## Example Responses

### Redis Response

**Response**: Value retrieved

```typescript
const value = await this.redis.get('key');
// value = 'value'
```

## Sequence Diagrams

### Redis Flow

```
Application → Redis Client → Redis Server → Response
```

## Architecture Diagrams

### Redis Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Application                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Redis Client                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Redis Server                               │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Cache        │  │  Queue Storage  │  │  Session        │
│  (Key-Value)  │  │  (Bull)         │  │  (Session Data) │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How is Redis used in the system?

**Answer**: Redis via:
- Caching frequently accessed data
- Queue storage for Bull
- Session management
- Token blacklisting
- Real-time data

### Q2: How do you implement caching with Redis?

**Answer**: Caching via:
- Cache-aside pattern
- Check cache first
- Return cached data if hit
- Query database if miss
- Cache database result

### Q3: How do you handle cache invalidation?

**Answer**: Cache invalidation via:
- Delete key on data change
- Set TTL for automatic expiration
- Use cache tags for group invalidation
- Use pub/sub for cache invalidation
- Monitor cache hit rate

## Exercises

### Exercise 1: Implement Caching

**Task**: Implement caching with Redis.

**Steps**:
1. Check cache first
2. Return cached data if hit
3. Query database if miss
4. Cache database result
5. Set TTL

**Verification**:
- Caching implemented
- Cache hit works
- Cache miss works
- TTL set
- Tests pass

### Exercise 2: Implement Token Blacklisting

**Task**: Implement token blacklisting with Redis.

**Steps**:
1. Add token to blacklist on logout
2. Set TTL based on token expiry
3. Check blacklist on token validation
4. Remove expired tokens
5. Test blacklisting

**Verification**:
- Blacklisting implemented
- Token added to blacklist
- TTL set correctly
- Check works
- Tests pass

## Real Production Scenarios

### Scenario 1: Redis Connection Failed

**Situation**: Redis connection failed

**Response**:
1. Check Redis server status
2. Check network connectivity
3. Check Redis configuration
4. Fix connection
5. Test Redis

### Scenario 2: Memory Leak

**Situation**: Redis memory leak

**Response**:
1. Check memory usage
2. Check TTL settings
3. Check key patterns
4. Fix TTL
5. Monitor memory

## Navigation

**Next Section**: [01-Caching](./01-Caching.md)

**Previous Section**: [11-Workers](../11-Workers/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [11-Workers](../11-Workers/README.md) - Workers details
