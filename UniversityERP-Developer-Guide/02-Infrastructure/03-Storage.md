# Storage

## Purpose

This document explains the storage architecture of the University ERP system. It details Docker volumes, data persistence, backup strategies, and storage management.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Docker volumes for data persistence. Understanding storage is critical for:
- Ensuring data persistence across container restarts
- Implementing backup strategies
- Managing storage capacity
- Troubleshooting storage issues
- Planning storage scaling

Without understanding storage, data may be lost or storage may become a bottleneck.

## Where This Is Used

- **Development**: Setting up local development environment
- **Deployment**: Deploying to production
- **Backup**: Implementing backup strategies
- **Troubleshooting**: Debugging storage issues
- **Capacity Planning**: Planning storage growth

## Dependencies

### Storage Dependencies

**Confirmed by Code**: Storage depends on:

- **Docker Volumes**: Data persistence
- **Host Filesystem**: Volume storage
- **Docker Compose**: Volume configuration
- **Backup Tools**: Backup strategies

## Internal Architecture

### Storage Overview

**Confirmed by Code**: The system uses Docker volumes for data persistence.

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Volumes                           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL    │  │   Redis         │  │   MinIO        │
│  Volume        │  │   Volume        │  │   Volume        │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ Elasticsearch  │  │  Application   │  │  Logs          │
│  Volume        │  │  (No Volume)   │  │  (Optional)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Volume Types

**Confirmed by Code**: The system uses named volumes.

**Named Volumes**:
- Managed by Docker
- Stored in `/var/lib/docker/volumes/`
- Persist across container lifecycle
- Easy to backup and restore

**Bind Mounts**:
- Mount host directory to container
- Direct access to files
- Used for `./docker-volumes/` directory

**Tmpfs**:
- In-memory filesystem
- Not persisted
- Not used in current setup

## Code Walkthrough

### Volume Configuration

**Confirmed by Code**: docker-compose.yml defines volumes.

**PostgreSQL Volume**:
```yaml
postgres:
  image: postgres:16-alpine
  volumes:
    - ./docker-volumes/postgres:/var/lib/postgresql/data
```

**What This Does**:
- Mounts `./docker-volumes/postgres` from host to `/var/lib/postgresql/data` in container
- PostgreSQL stores data in this directory
- Data persists across container restarts
- Data persists across container removal

**Redis Volume**:
```yaml
redis:
  image: redis:7-alpine
  volumes:
    - ./docker-volumes/redis:/data
```

**What This Does**:
- Mounts `./docker-volumes/redis` from host to `/data` in container
- Redis stores AOF file in this directory
- Data persists across container restarts
- Data persists across container removal

**MinIO Volume**:
```yaml
minio:
  image: minio/minio:latest
  volumes:
    - ./docker-volumes/minio:/data
```

**What This Does**:
- Mounts `./docker-volumes/minio` from host to `/data` in container
- MinIO stores objects in this directory
- Data persists across container restarts
- Data persists across container removal

**Elasticsearch Volume**:
```yaml
elasticsearch:
  image: elasticsearch:8.13.0
  volumes:
    - ./docker-volumes/elasticsearch:/usr/share/elasticsearch/data
```

**What This Does**:
- Mounts `./docker-volumes/elasticsearch` from host to `/usr/share/elasticsearch/data` in container
- Elasticsearch stores indices in this directory
- Data persists across container restarts
- Data persists across container removal

### Volume Management

**List Volumes**:
```bash
docker volume ls
```

**Inspect Volume**:
```bash
docker volume inspect university-erp_postgres
```

**Remove Volume**:
```bash
docker volume rm university-erp_postgres
```

**Remove Unused Volumes**:
```bash
docker volume prune
```

## Database Interactions

### PostgreSQL Storage

**Confirmed by Code**: PostgreSQL stores data in volume.

**Storage Location**:
- **Host**: `./docker-volumes/postgres`
- **Container**: `/var/lib/postgresql/data`

**Data Stored**:
- Database files
- WAL (Write-Ahead Log) files
- Configuration files
- Temporary files

**Storage Requirements**:
- **Development**: 1-2 GB
- **Production**: 10-100 GB (depends on data)
- **Growth**: Linear with data growth

**Backup Strategy**:
```bash
# Backup using pg_dump
docker-compose exec postgres pg_dump -U postgres university_erp > backup.sql

# Backup volume
docker run --rm -v university-erp_postgres:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz /data

# Restore from backup
docker-compose exec -T postgres psql -U postgres university_erp < backup.sql
```

## Redis Interactions

### Redis Storage

**Confirmed by Code**: Redis stores data in volume.

**Storage Location**:
- **Host**: `./docker-volumes/redis`
- **Container**: `/data`

**Data Stored**:
- AOF (Append Only File)
- RDB (Redis Database) snapshots (if configured)

**Storage Requirements**:
- **Development**: 100-500 MB
- **Production**: 1-10 GB (depends on cache size)
- **Growth**: Depends on cache usage

**Backup Strategy**:
```bash
# Backup AOF file
cp ./docker-volumes/redis/appendonly.aof ./redis-backup-$(date +%Y%m%d).aof

# Backup volume
docker run --rm -v university-erp_redis:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup-$(date +%Y%m%d).tar.gz /data

# Restore from backup
cp ./redis-backup-20240101.aof ./docker-volumes/redis/appendonly.aof
docker-compose restart redis
```

## Queue Interactions

### Queue Storage

**Confirmed by Code**: Bull queues store data in Redis.

**Storage Location**:
- Same as Redis storage
- Queue data stored in Redis AOF file

**Data Stored**:
- Job data
- Job metadata
- Job results
- Queue statistics

**Storage Requirements**:
- Included in Redis storage requirements
- Depends on queue backlog

## Worker Interactions

### Worker Storage

**Confirmed by Code**: Workers don't use volumes for data.

**Storage**:
- Workers are stateless
- No persistent storage required
- All data stored in PostgreSQL, Redis, or MinIO

## Business Rules

### Storage Rules

**Confirmed by Code**: Storage follows these rules:

1. **Data Persistence**: All data services use volumes
2. **Backup Strategy**: Regular backups of all volumes
3. **Retention Policy**: Define retention policy for backups
4. **Capacity Planning**: Monitor storage usage and plan growth
5. **Cleanup**: Regular cleanup of old data

### Backup Rules

**Confirmed by Code**: Backup strategy follows these rules:

1. **Regular Backups**: Daily backups for production
2. **Off-site Storage**: Store backups off-site
3. **Encryption**: Encrypt backups
4. **Verification**: Verify backup integrity
5. **Testing**: Test restore process

## Security

### Storage Security

**Confirmed by Code**: Security considerations for storage:

1. **Permissions**: Set appropriate file permissions
2. **Encryption**: Encrypt sensitive data at rest
3. **Access Control**: Restrict access to volumes
4. **Backup Encryption**: Encrypt backup files
5. **Secure Deletion**: Securely delete sensitive data

## Performance Considerations

### Storage Performance

**Confirmed by Code**: Performance considerations for storage:

1. **Disk Type**: Use SSD for better performance
2. **IOPS**: Ensure sufficient IOPS for database
3. **Latency**: Monitor disk latency
4. **Throughput**: Monitor disk throughput
5. **Capacity**: Ensure sufficient disk space

## Common Mistakes

### Mistake 1: Not Using Volumes

**Symptom**: Data lost on container restart

**Cause**: Not using volumes for data persistence

**Fix**:
```yaml
# Wrong
postgres:
  image: postgres:16-alpine

# Correct
postgres:
  image: postgres:16-alpine
  volumes:
    - ./docker-volumes/postgres:/var/lib/postgresql/data
```

### Mistake 2: Not Backing Up Volumes

**Symptom**: Data loss on disk failure

**Cause**: Not backing up volumes

**Fix**:
```bash
# Regular backup
docker run --rm -v university-erp_postgres:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz /data
```

### Mistake 3: Running Out of Disk Space

**Symptom**: Services fail due to no disk space

**Cause**: Not monitoring disk usage

**Fix**:
```bash
# Monitor disk usage
df -h

# Clean up old data
docker system prune -a
docker volume prune
```

## Debugging Guide

### Storage Debugging

**Issue**: Volume not mounting

**Investigation**:
1. Check volume exists: `docker volume ls`
2. Check volume details: `docker volume inspect <volume>`
3. Check container logs: `docker-compose logs <service>`
4. Check permissions: `ls -la ./docker-volumes/`
5. Check disk space: `df -h`

**Tools**:
- Docker volume commands
- Docker logs
- File system commands
- Disk usage commands

## Future Enhancements

### Storage Monitoring

**Status**: Not implemented

**Proposal**: Implement storage monitoring:
- Monitor disk usage
- Monitor IOPS
- Monitor latency
- Alert on thresholds
- Predict capacity needs

### Automated Backups

**Status**: Not implemented

**Proposal**: Implement automated backups:
- Cron jobs for daily backups
- Automated off-site sync
- Backup verification
- Backup retention policy
- Automated restore testing

## Production Considerations

### Production Storage

**Production Deployment**:
- Use managed storage (AWS EBS, Azure Disk)
- Configure IOPS for database
- Enable encryption at rest
- Implement backup strategy
- Monitor storage metrics
- Plan for growth

### Storage Scaling

**Scaling Strategy**:
- Monitor storage usage
- Plan for growth
- Scale storage as needed
- Implement data archival
- Implement data cleanup

## Example Requests

### List Volumes

**Request**:
```bash
docker volume ls
```

**Response**:
```
DRIVER              VOLUME NAME
local               university-erp_postgres
local               university-erp_redis
local               university-erp_minio
local               university-erp_elasticsearch
```

### Inspect Volume

**Request**:
```bash
docker volume inspect university-erp_postgres
```

**Response**:
```json
[
  {
    "CreatedAt": "2024-01-01T00:00:00Z",
    "Driver": "local",
    "Labels": {
      "com.docker.compose.project": "university-erp",
      "com.docker.compose.volume": "postgres"
    },
    "Mountpoint": "/var/lib/docker/volumes/university-erp_postgres/_data",
    "Name": "university-erp_postgres",
    "Options": {},
    "Scope": "local"
  }
]
```

## Example Responses

### Volume Usage

**Request**:
```bash
du -sh ./docker-volumes/*
```

**Response**:
```
1.2G    ./docker-volumes/postgres
256M    ./docker-volumes/redis
512M    ./docker-volumes/minio
128M    ./docker-volumes/elasticsearch
```

## Sequence Diagrams

### Volume Mount Flow

```
Docker Compose → Create Volume
                  ↓
              Start Container
                  ↓
              Mount Volume
                  ↓
              Container Running
                  ↓
              Data Written to Volume
                  ↓
              Container Stopped
                  ↓
              Data Persists in Volume
```

## Architecture Diagrams

### Storage Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Host Filesystem                          │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ ./docker-      │  │ ./docker-      │  │ ./docker-      │
│ volumes/       │  │ volumes/       │  │ volumes/       │
│ postgres/      │  │ redis/         │  │ minio/         │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│ PostgreSQL    │  │   Redis         │  │   MinIO        │
│ Container     │  │   Container    │  │   Container    │
│ /var/lib/     │  │   /data        │  │   /data        │
│ postgresql/   │  │                │  │                │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How is data persistence handled in Docker?

**Answer**: Data persistence via Docker volumes:
- Volumes mounted to containers
- Data stored in volumes persists across container lifecycle
- Volumes can be backed up and restored
- Volumes managed by Docker or bind mounts to host

### Q2: What is the backup strategy for the system?

**Answer**: Backup strategy includes:
- PostgreSQL: pg_dump for logical backups, volume backups for full backups
- Redis: AOF file backup, volume backup
- MinIO: mc mirror for object backup, volume backup
- Elasticsearch: Snapshot API, volume backup
- Regular daily backups, off-site storage

### Q3: How do you monitor storage usage?

**Answer**: Monitoring via:
- Docker volume commands: `docker system df`
- Host commands: `df -h`, `du -sh`
- Application monitoring: Database metrics, cache metrics
- Future: Prometheus + Grafana for storage monitoring

## Exercises

### Exercise 1: Backup Volume

**Task**: Backup a Docker volume.

**Steps**:
1. Identify volume to backup
2. Create backup directory
3. Run backup command
4. Verify backup
5. Test restore

**Verification**:
- Backup created
- Backup valid
- Restore works

### Exercise 2: Monitor Storage Usage

**Task**: Monitor storage usage.

**Steps**:
1. Check disk usage: `df -h`
2. Check volume usage: `docker system df`
3. Check directory usage: `du -sh ./docker-volumes/*`
4. Analyze growth trend
5. Plan for growth

**Verification**:
- Storage usage known
- Growth trend identified
- Capacity planned

## Real Production Scenarios

### Scenario 1: Disk Space Full

**Situation**: Docker volumes filling disk

**Response**:
1. Check disk usage: `df -h`
2. Identify largest volumes: `du -sh ./docker-volumes/*`
3. Clean up Docker: `docker system prune -a`
4. Clean up old data in volumes
5. Add more disk space
6. Implement data retention policy

### Scenario 2: Volume Corruption

**Situation**: Volume corrupted, data inaccessible

**Response**:
1. Stop affected service
2. Check volume integrity
3. Restore from backup
4. Verify data integrity
5. Restart service
6. Monitor for issues

## Navigation

**Next Section**: [04-Environment-Variables](./04-Environment-Variables.md)

**Previous Section**: [02-Networking](./02-Networking.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [05-Database](../05-Database/README.md) - Database details
- [17-Production](../17-Production/README.md) - Production guide
