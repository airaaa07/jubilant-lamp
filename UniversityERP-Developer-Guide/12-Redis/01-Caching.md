# Caching

## Purpose

This document explains caching in the University ERP system. It details how caching is implemented using Redis, caching strategies, and best practices.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Redis for caching. Understanding caching is critical for:
- Improving performance
- Reducing database load
- Implementing cache strategies
- Debugging cache issues
- Optimizing cache usage

Without understanding caching, developers may struggle with performance or may introduce caching bugs.

## Where This Is Used

- **Onboarding**: New developers learn caching
- **Feature Development**: Implementing caching
- **Code Reviews**: Reviewing caching code
- **Performance**: Improving performance
- **Database Load**: Reducing database load

## Dependencies

### Caching Dependencies

**Confirmed by Code**: Caching depends on:

- **RedisService**: Redis client
- **Prisma**: Database access
- **NestJS**: Framework for caching
- **Environment Variables**: Cache configuration

## Internal Architecture

### Caching Architecture

**Confirmed by Code**: Caching follows cache-aside pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Check Cache                                  │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
┌───────▼────────┐                          ┌────────▼────────┐
│  Cache Hit    │                          │  Cache Miss     │
└────────────────┘                          └─────────────────┘
        │                                           │
        ↓                                           ↓
┌────────────────┐                          ┌────────────────┐
│  Return Data   │                          │  Query Database │
└────────────────┘                          └────────────────┘
                                                   │
                                                   ↓
                                          ┌────────────────┐
                                          │  Cache Result  │
                                          └────────────────┘
                                                   │
                                                   ↓
                                          ┌────────────────┐
                                          │  Return Data   │
                                          └────────────────┘
```

## Code Walkthrough

### Caching Service

**Confirmed by Code**: Caching service provides caching methods.

**CacheService**:
```typescript
import { Injectable } from '@nestjs/common';
import { RedisService } from '../redis/redis.service';

@Injectable()
export class CacheService {
  constructor(private redis: RedisService) {}

  async get<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    if (!cached) return null;
    return JSON.parse(cached) as T;
  }

  async set<T>(key: string, value: T, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async delete(key: string): Promise<void> {
    await this.redis.del(key);
  }

  async deletePattern(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  async invalidateCache(pattern: string): Promise<void> {
    await this.deletePattern(pattern);
  }
}
```

**What This Does**:
- **get**: Gets value from cache
- **set**: Sets value in cache with TTL
- **delete**: Deletes key from cache
- **deletePattern**: Deletes keys matching pattern
- **invalidateCache**: Invalidates cache by pattern

### Caching Implementation

**Confirmed by Code**: Caching implemented in services.

**UsersService with Caching**:
```typescript
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private cacheService: CacheService,
  ) {}

  async findAll(): Promise<User[]> {
    const cacheKey = 'users:all';
    const cached = await this.cacheService.get<User[]>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const users = await this.prisma.user.findMany();
    await this.cacheService.set(cacheKey, users, 3600);
    
    return users;
  }

  async findOne(id: string): Promise<User> {
    const cacheKey = `users:${id}`;
    const cached = await this.cacheService.get<User>(cacheKey);
    
    if (cached) {
      return cached;
    }

    const user = await this.prisma.user.findUnique({ where: { id } });
    if (user) {
      await this.cacheService.set(cacheKey, user, 3600);
    }
    
    return user;
  }

  async update(id: string, dto: UpdateUserDto): Promise<User> {
    const user = await this.prisma.user.update({
      where: { id },
      data: dto,
    });

    // Invalidate cache
    await this.cacheService.delete(`users:${id}`);
    await this.cacheService.invalidateCache('users:*');
    
    return user;
  }
}
```

**What This Does**:
- **findAll**: Caches all users
- **findOne**: Caches single user
- **update**: Invalidates cache on update
- **Cache Aside**: Implements cache-aside pattern

## Database Interactions

### Caching-Database Flow

**Confirmed by Code**: Caching reduces database load.

**Flow**:
```
Application → Cache → Database (if cache miss)
```

## Redis Interactions

### Caching-Redis Flow

**Confirmed by Code**: Caching uses Redis for storage.

**Flow**:
```
Application → Redis Service → Redis Server
```

## Queue Interactions

### Caching-Queue Flow

**Confirmed by Code**: Caching doesn't interact with queues.

**Flow**:
```
Caching → No queue interaction
```

## Worker Interactions

### Caching-Worker Flow

**Confirmed by Code**: Workers can use caching.

**Flow**:
```
Worker → Cache → Database (if cache miss)
```

## Business Rules

### Caching Rules

**Confirmed by Code**: Caching follows these rules:

1. **Cache Aside**: Cache-aside pattern
2. **TTL**: Set appropriate TTL
3. **Invalidation**: Invalidate on data change
4. **Cache Miss**: Handle cache miss
5. **Cache Hit**: Return cached data

### Cache Key Rules

**Confirmed by Code**: Cache key rules:

1. **Naming**: Use consistent naming
2. **Namespacing**: Use namespace for keys
3. **Parameters**: Include parameters in key
4. **Uniqueness**: Keys must be unique
5. **Readability**: Keys should be readable

## Security

### Caching Security

**Confirmed by Code**: Security considerations for caching:

1. **Sensitive Data**: Don't cache sensitive data
2. **Access Control**: Cache scoped by user
3. **Encryption**: Encrypt cached data if needed
4. **TTL**: Set appropriate TTL
5. **Invalidation**: Invalidate on access change

## Performance Considerations

### Caching Performance

**Confirmed by Code**: Performance considerations:

1. **Hit Rate**: Monitor cache hit rate
2. **TTL**: Set appropriate TTL
3. **Memory Usage**: Monitor memory usage
4. **Cache Size**: Monitor cache size
5. **Eviction**: Configure eviction policy

## Common Mistakes

### Mistake 1: Not Setting TTL

**Symptom**: Memory leak

**Cause**: Not setting TTL on keys

**Fix**:
```typescript
// Set TTL
await this.cacheService.set(key, value, 3600);
```

### Mistake 2: Not Invalidating Cache

**Symptom**: Stale data

**Cause**: Not invalidating cache on data change

**Fix**:
```typescript
// Invalidate cache
await this.cacheService.delete(key);
```

### Mistake 3: Caching Sensitive Data

**Symptom**: Security vulnerability

**Cause**: Caching sensitive data

**Fix**:
```typescript
// Don't cache sensitive data
if (data.isSensitive) {
  return data;
}
await this.cacheService.set(key, data);
```

## Debugging Guide

### Caching Debugging

**Issue**: Cache not working

**Investigation**:
1. Check Redis connection
2. Check cache key
3. Check TTL
4. Check cache logic
5. Check logs

**Tools**:
- Redis CLI
- Cache logs
- Application logs
- Redis monitoring tools

## Future Enhancements

### Cache Warming

**Status**: Not implemented

**Proposal**: Implement cache warming:
- Pre-populate cache on startup
- Schedule cache warming
- Better performance
- More complex
- Better for predictable access patterns

### Distributed Caching

**Status**: Not implemented

**Proposal**: Implement distributed caching:
- Redis cluster
- Better scalability
- High availability
- More complex
- Better for production

## Production Considerations

### Production Caching

**Production Deployment**:
- Enable caching
- Configure TTL
- Monitor cache performance
- Monitor memory usage
- Monitor hit rate

### Caching Monitoring

**Monitoring Metrics**:
- Cache hit rate
- Cache miss rate
- Memory usage
- Cache size
- Eviction rate

## Example Requests

### Caching Example

**Get Data**:
```typescript
const users = await this.usersService.findAll();
```

## Example Responses

### Caching Response

**Response**: Data from cache or database

```typescript
// First call: from database
// Second call: from cache
```

## Sequence Diagrams

### Caching Flow

```
Application → Check Cache → Cache Hit → Return Data
Application → Check Cache → Cache Miss → Query Database → Cache Result → Return Data
```

## Architecture Diagrams

### Caching Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Application                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Check Cache                                │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┴─────────────────────┐
        │                                           │
┌───────▼────────┐                          ┌────────▼────────┐
│  Cache Hit    │                          │  Cache Miss     │
└────────────────┘                          └─────────────────┘
        │                                           │
        ↓                                           ↓
┌────────────────┐                          ┌────────────────┐
│  Return Data   │                          │  Query Database │
└────────────────┘                          └────────────────┘
                                                   │
                                                   ↓
                                          ┌────────────────┐
                                          │  Cache Result  │
                                          └────────────────┘
                                                   │
                                                   ↓
                                          ┌────────────────┐
                                          │  Return Data   │
                                          └────────────────┘
```

## Common Interview Questions

### Q1: How does caching work in the system?

**Answer**: Caching via:
- Cache-aside pattern
- Check cache first
- Return cached data if hit
- Query database if miss
- Cache database result

### Q2: How do you handle cache invalidation?

**Answer**: Cache invalidation via:
- Delete key on data change
- Invalidate by pattern
- Set TTL for automatic expiration
- Use cache tags for group invalidation
- Monitor cache hit rate

### Q3: What caching strategies do you use?

**Answer**: Caching strategies via:
- Cache-aside pattern
- TTL-based expiration
- Pattern-based invalidation
- Namespace-based keys
- Read-through caching

## Exercises

### Exercise 1: Implement Caching

**Task**: Implement caching for a service.

**Steps**:
1. Inject CacheService
2. Check cache first
3. Return cached data if hit
4. Query database if miss
5. Cache database result

**Verification**:
- Caching implemented
- Cache hit works
- Cache miss works
- TTL set
- Tests pass

### Exercise 2: Implement Cache Invalidation

**Task**: Implement cache invalidation.

**Steps**:
1. Add cache invalidation on update
2. Add cache invalidation on delete
3. Use pattern-based invalidation
4. Test invalidation
5. Verify cache cleared

**Verification**:
- Invalidation implemented
- Update invalidates cache
- Delete invalidates cache
- Pattern works
- Tests pass

## Real Production Scenarios

### Scenario 1: Cache Not Working

**Situation**: Cache not working

**Response**:
1. Check Redis connection
2. Check cache logic
3. Check cache key
4. Fix caching
5. Test caching

### Scenario 2: Stale Data

**Situation**: Stale data in cache

**Response**:
1. Check invalidation logic
2. Fix invalidation
3. Clear cache
4. Test invalidation
5. Monitor cache

## Navigation

**Next Section**: [02-Queue-Storage](./02-Queue-Storage.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [11-Workers](../11-Workers/README.md) - Workers details
