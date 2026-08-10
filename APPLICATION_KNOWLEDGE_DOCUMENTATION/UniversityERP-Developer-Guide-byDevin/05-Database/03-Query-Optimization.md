# Query Optimization

## Purpose

This document explains query optimization strategies for the University ERP database. It details how to optimize database queries, use indexes effectively, and improve query performance.

## Why This Document Exists

**Confirmed by Code**: The University ERP database requires optimization for performance. Understanding query optimization is critical for:
- Improving query performance
- Reducing database load
- Scaling the application
- Debugging slow queries
- Optimizing resource usage

Without understanding query optimization, developers may struggle with performance issues or may introduce inefficient queries.

## Where This Is Used

- **Onboarding**: New developers learn query optimization
- **Feature Development**: Writing optimized queries
- **Code Reviews**: Reviewing query performance
- **Performance Tuning**: Optimizing slow queries
- **Debugging**: Debugging performance issues

## Dependencies

### Query Optimization Dependencies

**Confirmed by Code**: Query optimization depends on:

- **PostgreSQL 16**: Relational database with query optimizer
- **Prisma 5.x**: ORM for database access
- **EXPLAIN ANALYZE**: Query analysis tool
- **Indexes**: Database indexes for performance

## Internal Architecture

### Query Optimization Architecture

**Confirmed by Code**: Query optimization at multiple levels.

```
┌─────────────────────────────────────────────────────────┐
│              Query Optimization Layers                     │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Indexes      │  │  Query Plans    │  │  Caching       │
│  (Performance)│  │  (Analysis)     │  │  (Redis)       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Index Usage

**Confirmed by Code**: Indexes defined in Prisma schema.

**Creating Indexes**:
```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  universityId  String
  instituteId   String?
  
  @@index([email])
  @@index([universityId])
  @@index([instituteId])
  @@index([universityId, instituteId])
}
```

**What This Does**:
- **@@index**: Creates index on column
- **email**: Index on email for fast lookup
- **universityId**: Index on universityId for filtering
- **instituteId**: Index on instituteId for filtering
- **Composite**: Composite index on universityId + instituteId

**Index Types**:
```prisma
// B-tree index (default)
@@index([email])

// Unique index
@@unique([email])

// Composite index
@@index([universityId, instituteId])

// Partial index (not supported in Prisma, use raw SQL)
// CREATE INDEX index_name ON table (column) WHERE condition
```

### Query Optimization

**Confirmed by Code**: Queries optimized with Prisma.

**Select Specific Fields**:
```typescript
// Bad - selects all fields
const users = await prisma.user.findMany();

// Good - selects only needed fields
const users = await prisma.user.findMany({
  select: { id: true, email: true, name: true },
});
```

**What This Does**:
- **select**: Specifies fields to select
- **Performance**: Reduces data transfer
- **Memory**: Reduces memory usage

**Pagination**:
```typescript
// Bad - no pagination
const users = await prisma.user.findMany();

// Good - with pagination
const users = await prisma.user.findMany({
  skip: 0,
  take: 10,
});
```

**What This Does**:
- **skip**: Skips N records
- **take**: Takes N records
- **Performance**: Limits result size
- **Memory**: Reduces memory usage

**Where Clause Optimization**:
```typescript
// Bad - function on column
const users = await prisma.user.findMany({
  where: {
    email: { contains: user.email.toLowerCase() },
  },
});

// Good - function on value
const users = await prisma.user.findMany({
  where: {
    email: { contains: user.email, mode: 'insensitive' },
  },
});
```

**What This Does**:
- **mode: 'insensitive'**: Case-insensitive search
- **Index Usage**: Allows index usage
- **Performance**: Better query performance

**Eager Loading**:
```typescript
// Bad - N+1 query problem
const users = await prisma.user.findMany();
for (const user of users) {
  const university = await prisma.university.findUnique({
    where: { id: user.universityId },
  });
}

// Good - eager loading
const users = await prisma.user.findMany({
  include: { university: true },
});
```

**What This Does**:
- **include**: Eager loads relations
- **Single Query**: Single query instead of N+1
- **Performance**: Much better performance

### EXPLAIN ANALYZE

**Confirmed by Code**: Queries analyzed with EXPLAIN ANALYZE.

**Using EXPLAIN ANALYZE**:
```sql
EXPLAIN ANALYZE
SELECT * FROM "User" WHERE "universityId" = 'uni-id';
```

**Output**:
```
Index Scan using User_universityId_idx on "User"  (cost=0.28..8.30 rows=1 width=200) (actual time=0.015..0.016 rows=1 loops=1)
  Index Cond: ("universityId" = 'uni-id'::text)
Planning Time: 0.092 ms
Execution Time: 0.031 ms
```

**What This Does**:
- **Index Scan**: Shows index usage
- **Cost**: Estimated query cost
- **Rows**: Estimated row count
- **Actual Time**: Actual execution time
- **Planning Time**: Query planning time

**Interpreting Results**:
- **Seq Scan**: Full table scan (bad)
- **Index Scan**: Index used (good)
- **High Cost**: Expensive query
- **High Actual Time**: Slow query
- **Planning Time**: Query planning overhead

## Database Interactions

### Query-Database Flow

**Confirmed by Code**: Queries executed via Prisma.

**Flow**:
```
Prisma Query → PostgreSQL Query Planner → Database → Results
```

## Redis Interactions

### Query-Redis Flow

**Confirmed by Code**: Query results cached in Redis.

**Flow**:
```
Query → Check Redis Cache → Cache Hit → Return
                              ↓
                         Cache Miss → Query Database → Cache Result → Return
```

## Queue Interactions

### Query-Queue Flow

**Confirmed by Code**: Queries don't directly interact with queues.

**Flow**:
```
Query → Database (no queue interaction)
```

## Worker Interactions

### Query-Worker Flow

**Confirmed by Code**: Workers execute queries via Prisma.

**Flow**:
```
Worker → Prisma Query → Database
```

## Business Rules

### Query Optimization Rules

**Confirmed by Code**: Query optimization follows these rules:

1. **Indexes**: Index frequently queried columns
2. **Select Fields**: Select only needed fields
3. **Pagination**: Paginate large datasets
4. **Eager Loading**: Use include for relations
5. **Caching**: Cache frequently accessed data

### Index Rules

**Confirmed by Code**: Index rules:

1. **Foreign Keys**: Index all foreign keys
2. **Unique Columns**: Index unique columns
3. **Frequently Queried**: Index frequently queried columns
4. **Composite Indexes**: Use composite indexes for multi-column queries
5. **Avoid Over-Indexing**: Don't over-index (slows writes)

## Security

### Query Security

**Confirmed by Code**: Security considerations for queries:

1. **SQL Injection**: Prisma prevents SQL injection
2. **Data Access**: Implement row-level security
3. **Query Logging**: Log all queries
4. **Sensitive Data**: Don't log sensitive data
5. **Query Limits**: Limit query results

## Performance Considerations

### Query Performance

**Confirmed by Code**: Performance considerations:

1. **Indexes**: Use indexes for fast lookups
2. **Query Plans**: Analyze query plans
3. **Connection Pooling**: Use connection pooling
4. **Caching**: Cache frequently accessed data
5. **Query Optimization**: Optimize slow queries

## Common Mistakes

### Mistake 1: Not Using Indexes

**Symptom**: Slow queries

**Cause**: Not using indexes

**Fix**:
```prisma
// Add index
@@index([email])
@@index([universityId])
```

### Mistake 2: N+1 Query Problem

**Symptom**: Too many database queries

**Cause**: Not using eager loading

**Fix**:
```typescript
// Use include
const users = await prisma.user.findMany({
  include: { university: true },
});
```

### Mistake 3: Selecting All Fields

**Symptom**: Slow queries, high memory usage

**Cause**: Selecting all fields

**Fix**:
```typescript
// Select only needed fields
const users = await prisma.user.findMany({
  select: { id: true, email: true },
});
```

## Debugging Guide

### Query Debugging

**Issue**: Query slow

**Investigation**:
1. Run EXPLAIN ANALYZE
2. Check query plan
3. Check index usage
4. Optimize query
5. Add indexes if needed

**Tools**:
- EXPLAIN ANALYZE
- Prisma Studio
- Database logs
- Query profiler

## Future Enhancements

### Query Caching

**Status**: Not implemented

**Proposal**: Implement query caching:
- Cache query results
- Invalidate on data change
- Better performance
- Reduced database load
- TTL-based expiration

### Materialized Views

**Status**: Not implemented

**Proposal**: Implement materialized views:
- Pre-computed query results
- Faster complex queries
- Refresh on schedule
- Better performance
- Reduced query complexity

## Production Considerations

### Production Queries

**Production Deployment**:
- Analyze query plans
- Optimize slow queries
- Monitor query performance
- Set up query alerts
- Regular query optimization

### Query Monitoring

**Monitoring Metrics**:
- Query execution time
- Query frequency
- Slow query count
- Index usage
- Cache hit rate

## Example Requests

### Query Example

**Request**: Optimized query

```typescript
const users = await prisma.user.findMany({
  where: { universityId: universityId },
  select: { id: true, email: true, name: true },
  skip: 0,
  take: 10,
  include: { university: true },
});
```

## Example Responses

### Query Response

**Response**: Query results

```typescript
[
  {
    id: 'user-id',
    email: 'user@example.com',
    name: 'John Doe',
    university: { id: 'uni-id', name: 'University' }
  }
]
```

## Sequence Diagrams

### Query Flow

```
Prisma Query → PostgreSQL → Query Planner → Index Scan → Results
```

## Architecture Diagrams

### Query Optimization Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Prisma Query                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Query Planner                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Index Scan / Seq Scan                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Results                                      │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you optimize database queries?

**Answer**: Query optimization via:
- Add indexes for frequently queried columns
- Select only needed fields
- Use pagination for large datasets
- Use eager loading for relations
- Cache frequently accessed data

### Q2: How do you use EXPLAIN ANALYZE?

**Answer**: EXPLAIN ANALYZE via:
- Run EXPLAIN ANALYZE before query
- Analyze query plan
- Check for Seq Scan (bad)
- Check for Index Scan (good)
- Optimize based on results

### Q3: What is the N+1 query problem?

**Answer**: N+1 query problem:
- Query N records
- For each record, query related data
- Results in N+1 queries
- Solve with eager loading (include)
- Much better performance

## Exercises

### Exercise 1: Optimize a Query

**Task**: Optimize a slow query.

**Steps**:
1. Identify slow query
2. Run EXPLAIN ANALYZE
3. Check index usage
4. Add indexes
5. Test performance

**Verification**:
- Query optimized
- Indexes added
- Performance improved
- Tests pass

### Exercise 2: Fix N+1 Problem

**Task**: Fix N+1 query problem.

**Steps**:
1. Identify N+1 problem
2. Add eager loading
3. Test query
4. Verify single query
5. Test performance

**Verification**:
- N+1 problem fixed
- Eager loading works
- Single query
- Performance improved
- Tests pass

## Real Production Scenarios

### Scenario 1: Slow Query

**Situation**: Query slow in production

**Response**:
1. Identify slow query
2. Run EXPLAIN ANALYZE
3. Add missing indexes
4. Optimize query
5. Monitor performance

### Scenario 2: High Database Load

**Situation**: Database under high load

**Response**:
1. Identify frequent queries
2. Add caching
3. Optimize queries
4. Add read replicas
5. Monitor load

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [02-Migrations](./02-Migrations.md)

**Related Documentation**:
- [01-Prisma-Schema](./01-Prisma-Schema.md) - Prisma schema
- [02-Migrations](./02-Migrations.md) - Migrations
- [18-Performance](../18-Performance/README.md) - Performance guide
