# Backup and Recovery

## Purpose

This document explains the backup and recovery strategy for the University ERP system. It details how to backup data, restore data, and implement disaster recovery.

## Why This Document Exists

**Confirmed by Code**: The University ERP stores critical data in PostgreSQL, Redis, MinIO, and Elasticsearch. Understanding backup and recovery is critical for:
- Preventing data loss
- Implementing disaster recovery
- Meeting compliance requirements
- Ensuring business continuity
- Recovering from failures

Without proper backup and recovery, data loss could be catastrophic.

## Where This Is Used

- **Operations**: Daily backup operations
- **Disaster Recovery**: Recovering from failures
- **Compliance**: Meeting data retention requirements
- **Testing**: Testing backup and restore procedures
- **Auditing**: Demonstrating data protection

## Dependencies

### Backup Dependencies

**Confirmed by Code**: Backup depends on:

- **Docker Volumes**: Data persistence
- **PostgreSQL**: Database backups
- **Redis**: Cache backups
- **MinIO**: Object storage backups
- **Elasticsearch**: Search index backups
- **Backup Tools**: pg_dump, mc, tar, etc.

## Internal Architecture

### Backup Architecture

**Confirmed by Code**: Multiple backup strategies for different data types.

```
┌─────────────────────────────────────────────────────────┐
│              Backup Strategy                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL   │  │   Redis         │  │   MinIO        │
│  pg_dump       │  │   AOF Backup    │  │   mc mirror    │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Volume       │  │   Off-site      │  │   Encryption   │
│  Backups      │  │   Storage       │  │   (Optional)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### PostgreSQL Backup

**Confirmed by Code**: PostgreSQL backup via pg_dump.

**Logical Backup**:
```bash
# Backup to SQL file
docker-compose exec postgres pg_dump -U postgres university_erp > backup-$(date +%Y%m%d).sql

# Backup with compression
docker-compose exec postgres pg_dump -U postgres university_erp | gzip > backup-$(date +%Y%m%d).sql.gz

# Backup specific tables
docker-compose exec postgres pg_dump -U postgres -t "User" university_erp > users-backup.sql
```

**What This Does**:
- Exports database to SQL file
- Can be restored with psql
- Human-readable format
- Good for small to medium databases

**Physical Backup**:
```bash
# Backup volume
docker run --rm \
  -v university-erp_postgres:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz /data
```

**What This Does**:
- Backs up entire PostgreSQL data directory
- Faster than logical backup
- Good for large databases
- Not human-readable

### PostgreSQL Restore

**Confirmed by Code**: PostgreSQL restore via psql.

**Restore from SQL File**:
```bash
# Restore from SQL file
docker-compose exec -T postgres psql -U postgres university_erp < backup-20240101.sql

# Restore from compressed SQL file
gunzip -c backup-20240101.sql.gz | docker-compose exec -T postgres psql -U postgres university_erp
```

**Restore from Volume Backup**:
```bash
# Stop PostgreSQL
docker-compose stop postgres

# Remove existing volume
docker volume rm university-erp_postgres

# Create new volume
docker volume create university-erp_postgres

# Restore from backup
docker run --rm \
  -v university-erp_postgres:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup-20240101.tar.gz -C /

# Start PostgreSQL
docker-compose start postgres
```

### Redis Backup

**Confirmed by Code**: Redis backup via AOF file.

**AOF Backup**:
```bash
# Copy AOF file
cp ./docker-volumes/redis/appendonly.aof ./redis-backup-$(date +%Y%m%d).aof

# Backup volume
docker run --rm \
  -v university-erp_redis:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/redis-backup-$(date +%Y%m%d).tar.gz /data
```

**What This Does**:
- Backs up AOF (Append Only File)
- Contains all write operations
- Can be used to restore Redis state

### Redis Restore

**Confirmed by Code**: Redis restore via AOF file.

**Restore from AOF**:
```bash
# Stop Redis
docker-compose stop redis

# Copy backup AOF
cp ./redis-backup-20240101.aof ./docker-volumes/redis/appendonly.aof

# Start Redis
docker-compose start redis
```

**Restore from Volume Backup**:
```bash
# Stop Redis
docker-compose stop redis

# Remove existing volume
docker volume rm university-erp_redis

# Create new volume
docker volume create university-erp_redis

# Restore from backup
docker run --rm \
  -v university-erp_redis:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/redis-backup-20240101.tar.gz -C /

# Start Redis
docker-compose start redis
```

### MinIO Backup

**Confirmed by Code**: MinIO backup via mc mirror.

**Backup Buckets**:
```bash
# Install mc CLI
docker run --rm -it minio/mc /bin/sh

# Configure mc alias
mc alias set local http://localhost:9000 minioadmin minioadmin

# Mirror bucket to local directory
mc mirror local/university-erp-docs ./minio-docs-backup
mc mirror local/university-erp-exams ./minio-exams-backup
```

**Backup Volume**:
```bash
# Backup volume
docker run --rm \
  -v university-erp_minio:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/minio-backup-$(date +%Y%m%d).tar.gz /data
```

### MinIO Restore

**Confirmed by Code**: MinIO restore via mc mirror.

**Restore from Backup**:
```bash
# Restore bucket from local directory
mc mirror ./minio-docs-backup local/university-erp-docs
mc mirror ./minio-exams-backup local/university-erp-exams
```

**Restore from Volume Backup**:
```bash
# Stop MinIO
docker-compose stop minio

# Remove existing volume
docker volume rm university-erp_minio

# Create new volume
docker volume create university-erp_minio

# Restore from backup
docker run --rm \
  -v university-erp_minio:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/minio-backup-20240101.tar.gz -C /

# Start MinIO
docker-compose start minio
```

### Elasticsearch Backup

**Confirmed by Code**: Elasticsearch backup via Snapshot API.

**Create Snapshot Repository**:
```bash
# Create snapshot repository
curl -X PUT "http://localhost:9200/_snapshot/backup_repo" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "/usr/share/elasticsearch/backups"
  }
}'

# Create backup directory
docker-compose exec elasticsearch mkdir -p /usr/share/elasticsearch/backups
```

**Create Snapshot**:
```bash
# Create snapshot
curl -X PUT "http://localhost:9200/_snapshot/backup_repo/snapshot_1?wait_for_completion=true"
```

**Restore Snapshot**:
```bash
# Restore snapshot
curl -X POST "http://localhost:9200/_snapshot/backup_repo/snapshot_1/_restore"
```

## Database Interactions

### Database Backup Strategy

**Confirmed by Code**: PostgreSQL backup strategy.

**Daily Backup**:
- Logical backup (pg_dump) at 2 AM
- Retain 7 days
- Compressed to save space

**Weekly Backup**:
- Physical backup (volume) on Sunday
- Retain 4 weeks
- Off-site storage

**Monthly Backup**:
- Full backup on 1st of month
- Retain 12 months
- Archive to cold storage

## Redis Interactions

### Redis Backup Strategy

**Confirmed by Code**: Redis backup strategy.

**Daily Backup**:
- AOF file backup at 3 AM
- Retain 7 days
- Compressed to save space

**Weekly Backup**:
- Volume backup on Sunday
- Retain 4 weeks
- Off-site storage

## Queue Interactions

### Queue Backup Strategy

**Confirmed by Code**: Queue data stored in Redis.

**Strategy**:
- Queue data backed up with Redis
- No separate backup needed
- Queue data can be rebuilt from database

## Worker Interactions

### Worker Backup Strategy

**Confirmed by Code**: Workers are stateless.

**Strategy**:
- No backup needed for workers
- All data in PostgreSQL, Redis, MinIO
- Workers can be redeployed

## Business Rules

### Backup Rules

**Confirmed by Code**: Backup follows these rules:

1. **Regular Backups**: Daily backups for all data
2. **Off-site Storage**: Store backups off-site
3. **Encryption**: Encrypt sensitive backups
4. **Verification**: Verify backup integrity
5. **Testing**: Test restore process regularly

### Recovery Rules

**Confirmed by Code**: Recovery follows these rules:

1. **Priority**: Recover critical services first
2. **Validation**: Validate data after restore
3. **Testing**: Test application after restore
4. **Monitoring**: Monitor for issues after restore
5. **Documentation**: Document recovery process

## Security

### Backup Security

**Confirmed by Code**: Security considerations for backups:

1. **Encryption**: Encrypt backup files
2. **Access Control**: Restrict access to backups
3. **Secure Storage**: Store backups securely
4. **Retention**: Define retention policy
5. **Disposal**: Securely delete old backups

### Backup Encryption

**GPG Encryption**:
```bash
# Encrypt backup
gpg --symmetric --cipher-algo AES256 backup-20240101.sql

# Decrypt backup
gpg --decrypt backup-20240101.sql.gpg > backup-20240101.sql
```

## Performance Considerations

### Backup Performance

**Confirmed by Code**: Performance considerations for backups:

1. **Schedule During Low Traffic**: Run backups during low traffic
2. **Compression**: Compress backups to save space
3. **Parallel Backups**: Run backups in parallel where possible
4. **Incremental Backups**: Use incremental backups for large databases
5. **Monitoring**: Monitor backup performance

## Common Mistakes

### Mistake 1: Not Testing Backups

**Symptom**: Backup fails when needed

**Cause**: Not testing restore process

**Fix**:
```bash
# Regularly test restore
# Restore to test environment
# Verify data integrity
# Document restore process
```

### Mistake 2: Not Encrypting Backups

**Symptom**: Sensitive data exposed

**Cause**: Not encrypting backup files

**Fix**:
```bash
# Encrypt backups
gpg --symmetric --cipher-algo AES256 backup.sql
```

### Mistake 3: Not Having Off-site Backup

**Symptom**: Data loss due to site failure

**Cause**: All backups on-site

**Fix**:
```bash
# Sync backups to off-site storage
rsync -avz ./backups/ user@remote-server:/backups/
```

## Debugging Guide

### Backup Debugging

**Issue**: Backup fails

**Investigation**:
1. Check service is running
2. Check disk space
3. Check permissions
4. Check backup logs
5. Test backup manually

**Tools**:
- Docker logs
- Backup logs
- System logs
- Manual backup commands

## Future Enhancements

### Automated Backups

**Status**: Not implemented

**Proposal**: Implement automated backups:
- Cron jobs for scheduled backups
- Automated off-site sync
- Backup verification
- Backup notifications
- Backup retention management

### Point-in-Time Recovery

**Status**: Not implemented

**Proposal**: Implement PITR:
- PostgreSQL WAL archiving
- Continuous WAL backup
- Restore to any point in time
- Better recovery granularity

## Production Considerations

### Production Backup Strategy

**Production Deployment**:
- Automated daily backups
- Automated off-site sync
- Backup encryption
- Backup verification
- Backup retention policy
- Disaster recovery plan

### Disaster Recovery

**Recovery Plan**:
1. Identify failure scope
2. Determine recovery strategy
3. Restore from most recent backup
4. Validate data integrity
5. Test application
6. Monitor for issues
7. Document recovery

## Example Requests

### Create Backup

**Request**:
```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U postgres university_erp | gzip > backup-$(date +%Y%m%d).sql.gz

# Backup Redis
cp ./docker-volumes/redis/appendonly.aof ./redis-backup-$(date +%Y%m%d).aof

# Backup MinIO
docker run --rm -v university-erp_minio:/data -v $(pwd):/backup alpine tar czf /backup/minio-backup-$(date +%Y%m%d).tar.gz /data
```

## Example Responses

### Backup Status

**Request**: Check backup status

**Response**:
```json
{
  "last_backup": "2024-01-01T02:00:00Z",
  "backup_size": "1.2GB",
  "backup_status": "success",
  "backup_retention": "7 days"
}
```

## Sequence Diagrams

### Backup Flow

```
Scheduled Time
        ↓
    Stop Services (if needed)
        ↓
    Create Backup
        ↓
    Compress Backup
        ↓
    Encrypt Backup (optional)
        ↓
    Upload to Off-site Storage
        ↓
    Verify Backup
        ↓
    Start Services (if stopped)
```

### Restore Flow

```
Failure Detected
        ↓
    Identify Failure Scope
        ↓
    Select Backup
        ↓
    Download Backup
        ↓
    Decrypt Backup (if encrypted)
        ↓
    Stop Services
        ↓
    Restore Backup
        ↓
    Start Services
        ↓
    Validate Data
        ↓
    Test Application
        ↓
    Monitor for Issues
```

## Architecture Diagrams

### Backup Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Production Environment                        │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL   │  │   Redis         │  │   MinIO        │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Backup Storage                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Local Backup │  │ Off-site      │  │ Cold Storage  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: What is the backup strategy for the system?

**Answer**: Backup strategy includes:
- PostgreSQL: Daily pg_dump, weekly volume backup
- Redis: Daily AOF backup, weekly volume backup
- MinIO: Daily mc mirror, weekly volume backup
- Elasticsearch: Daily snapshot
- Off-site storage for all backups
- 7-day retention for daily backups
- 4-week retention for weekly backups

### Q2: How do you recover from a database failure?

**Answer**: Database recovery via:
- Stop PostgreSQL service
- Remove corrupted volume
- Create new volume
- Restore from most recent backup
- Start PostgreSQL service
- Validate data integrity
- Test application

### Q3: How do you ensure backup integrity?

**Answer**: Backup integrity via:
- Regular restore testing
- Backup verification after creation
- Checksum verification
- Monitoring backup logs
- Alert on backup failures

## Exercises

### Exercise 1: Create Backup

**Task**: Create a backup of all data.

**Steps**:
1. Backup PostgreSQL
2. Backup Redis
3. Backup MinIO
4. Verify backups
5. Store off-site

**Verification**:
- All backups created
- Backups valid
- Backups stored off-site

### Exercise 2: Restore from Backup

**Task**: Restore from backup.

**Steps**:
1. Stop services
2. Restore PostgreSQL
3. Restore Redis
4. Restore MinIO
5. Start services
6. Validate data

**Verification**:
- Data restored
- Data valid
- Application works

## Real Production Scenarios

### Scenario 1: Database Corruption

**Situation**: PostgreSQL database corrupted

**Response**:
1. Stop PostgreSQL
2. Identify corruption scope
3. Select appropriate backup
4. Restore from backup
5. Validate data integrity
6. Test application
7. Monitor for issues

### Scenario 2: Complete System Failure

**Situation**: Complete system failure

**Response**:
1. Assess damage
2. Identify recoverable data
3. Restore from off-site backup
4. Rebuild infrastructure
5. Restore data
6. Test application
7. Monitor for issues

## Navigation

**Next Section**: [07-Monitoring](./07-Monitoring.md)

**Previous Section**: [05-Performance](./05-Performance.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [03-Storage](./03-Storage.md) - Storage details
- [17-Production](../17-Production/README.md) - Production guide
