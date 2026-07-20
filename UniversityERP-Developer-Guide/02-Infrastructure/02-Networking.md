# Networking

## Purpose

This document explains the networking configuration of the University ERP system. It details how Docker services communicate, network isolation, port exposure, and security considerations.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Docker networking for service communication. Understanding networking is critical for:
- Configuring service communication
- Troubleshooting connectivity issues
- Securing service communication
- Planning network architecture
- Optimizing network performance

Without understanding networking, developers may struggle with service connectivity or security issues.

## Where This Is Used

- **Development**: Setting up local development environment
- **Deployment**: Deploying to production
- **Troubleshooting**: Debugging connectivity issues
- **Security**: Securing service communication
- **Performance**: Optimizing network performance

## Dependencies

### Networking Dependencies

**Confirmed by Code**: Networking depends on:

- **Docker Networks**: Service communication
- **Docker Compose**: Network configuration
- **Port Mapping**: Service exposure
- **DNS**: Service discovery
- **Firewall**: Network security

## Internal Architecture

### Network Architecture

**Confirmed by Code**: Docker Compose creates a default network.

```
┌─────────────────────────────────────────────────────────┐
│                  Docker Network                            │
│                  university-erp_default                    │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  PostgreSQL    │  │   Redis         │  │   MinIO        │
│  postgres      │  │   redis         │  │   minio        │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │   CBE Engine   │  │   Workers      │
│  core-api     │  │   cbe-engine    │  │   workers      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Network Types

**Confirmed by Code**: Docker supports multiple network types.

**Bridge Network** (Default):
- Used for service-to-service communication
- Services can communicate by container name
- Isolated from host network
- Default for Docker Compose

**Host Network**:
- Services use host network stack
- No network isolation
- Better performance
- Port conflicts possible

**Overlay Network**:
- Used for multi-host communication
- Swarm mode
- Not used in current setup

## Code Walkthrough

### Docker Compose Network Configuration

**Confirmed by Code**: Docker Compose creates default network.

**Default Network**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    # Docker Compose automatically adds to default network
    # Can communicate with other services by container name

  redis:
    image: redis:7-alpine
    # Can communicate with postgres as "postgres:5432"

  core-api:
    build: ./apps/core-api
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/university_erp
      REDIS_HOST: redis
      REDIS_PORT: 6379
```

**What This Does**:
- Creates default network named `university-erp_default`
- All services added to this network
- Services can communicate by container name
- DNS resolution enabled for service names

### Custom Network Configuration

**Status**: Not implemented

**Proposal**: Custom network configuration.

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

services:
  core-api:
    networks:
      - backend
  
  admin-portal:
    networks:
      - frontend
  
  nginx:
    networks:
      - frontend
      - backend
```

**What This Would Do**:
- Creates separate networks for frontend and backend
- Nginx connects both networks
- Better network isolation
- More secure architecture

### Port Mapping

**Confirmed by Code**: Services expose ports to host.

**Configuration**:
```yaml
services:
  postgres:
    ports:
      - "5432:5432"  # host:container

  redis:
    ports:
      - "6379:6379"

  core-api:
    ports:
      - "3000:3000"
```

**What This Does**:
- Maps container port to host port
- Allows external access to services
- Format: `host_port:container_port`
- Can map multiple ports: `"3000:3000", "3001:3001"`

### Service Discovery

**Confirmed by Code**: Services discover each other by container name.

**Example**:
```yaml
services:
  core-api:
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/university_erp
      # "postgres" is the container name of PostgreSQL service
```

**What This Does**:
- Docker provides DNS for service names
- Services can resolve container names to IP addresses
- No need to know IP addresses
- Simplifies configuration

## Database Interactions

### PostgreSQL Network Configuration

**Confirmed by Code**: Application connects to PostgreSQL via container name.

**Connection String**:
```
postgresql://postgres:postgres@postgres:5432/university_erp
```

**Network Flow**:
1. Core API container resolves `postgres` to PostgreSQL container IP
2. Core API connects to PostgreSQL on port 5432
3. Communication happens within Docker network
4. No host network involved

**From Host**:
```bash
# From host, use localhost
docker-compose exec postgres psql -U postgres -d university_erp

# Or connect via localhost
psql -h localhost -p 5432 -U postgres -d university_erp
```

## Redis Interactions

### Redis Network Configuration

**Confirmed by Code**: Application connects to Redis via container name.

**Connection**:
```typescript
const redis = new Redis({
  host: process.env.REDIS_HOST || 'redis',  // Container name
  port: parseInt(process.env.REDIS_PORT || '6379'),
});
```

**Network Flow**:
1. Application container resolves `redis` to Redis container IP
2. Application connects to Redis on port 6379
3. Communication happens within Docker network
4. No host network involved

**From Host**:
```bash
# From host, use localhost
docker-compose exec redis redis-cli

# Or connect via localhost
redis-cli -h localhost -p 6379
```

## Queue Interactions

### Bull Queue Network Configuration

**Confirmed by Code**: Bull queues use Redis as backend.

**Connection**:
```typescript
const queue = new Bull('notifications', {
  redis: {
    host: process.env.REDIS_HOST || 'redis',  // Container name
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});
```

**Network Flow**:
1. Core API resolves `redis` to Redis container IP
2. Core API connects to Redis on port 6379
3. Workers also resolve `redis` to same Redis container IP
4. All services communicate with same Redis instance

## Worker Interactions

### Worker Network Configuration

**Confirmed by Code**: Workers connect to same services as API.

**Connection**:
```yaml
services:
  notification-worker:
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/university_erp
      REDIS_HOST: redis
      REDIS_PORT: 6379
```

**Network Flow**:
1. Worker resolves `postgres` to PostgreSQL container IP
2. Worker resolves `redis` to Redis container IP
3. Worker connects to both services
4. Communication happens within Docker network

## Business Rules

### Networking Rules

**Confirmed by Code**: Networking follows these rules:

1. **Default Network**: All services in default network
2. **Service Discovery**: Use container names for communication
3. **Port Mapping**: Map only necessary ports to host
4. **Network Isolation**: Services isolated in Docker network
5. **DNS**: Docker provides DNS for service names

### Security Rules

**Confirmed by Code**: Security considerations for networking:

1. **Minimal Exposure**: Expose only necessary ports
2. **Network Isolation**: Use separate networks for different tiers
3. **TLS**: Enable TLS for all external communication
4. **Firewall**: Configure firewall rules
5. **Private Networks**: Use private networks for internal communication

## Security

### Network Security

**Confirmed by Code**: Security considerations for networking:

1. **Port Exposure**: Only expose necessary ports
2. **Network Isolation**: Services isolated in Docker network
3. **TLS**: Enable TLS for all external communication
4. **Firewall**: Configure firewall rules
5. **Service Discovery**: Use container names, not IPs

### Firewall Configuration

**Status**: Not implemented

**Proposal**: Configure firewall rules.

```bash
# Allow only necessary ports
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 22/tcp    # SSH
sudo ufw deny 5432/tcp   # PostgreSQL (internal only)
sudo ufw deny 6379/tcp   # Redis (internal only)
sudo ufw deny 9000/tcp   # MinIO (internal only)
sudo ufw enable
```

## Performance Considerations

### Network Performance

**Confirmed by Code**: Performance considerations for networking:

1. **Bridge Network**: Slight overhead compared to host network
2. **DNS Resolution**: Docker DNS adds slight overhead
3. **Network Isolation**: Security vs performance trade-off
4. **Connection Pooling**: Reuse connections to reduce overhead
5. **Keep-Alive**: Use keep-alive for persistent connections

## Common Mistakes

### Mistake 1: Using localhost for Inter-Service Communication

**Symptom**: Connection refused

**Cause**: Using localhost instead of container name

**Fix**:
```yaml
# Wrong
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_erp

# Correct
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/university_erp
```

### Mistake 2: Exposing All Ports

**Symptom**: Security risk

**Cause**: Exposing all ports to host

**Fix**:
```yaml
# Wrong
ports:
  - "5432:5432"
  - "6379:6379"
  - "9000:9000"

# Correct - only expose necessary ports
ports:
  - "3000:3000"  # Only API port
```

### Mistake 3: Not Configuring Network Isolation

**Symptom**: Security risk

**Cause**: All services in same network

**Fix**:
```yaml
# Create separate networks
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

services:
  core-api:
    networks:
      - backend
  
  admin-portal:
    networks:
      - frontend
```

## Debugging Guide

### Network Debugging

**Issue**: Service cannot connect to another service

**Investigation**:
1. Check service is running: `docker-compose ps`
2. Check network: `docker network inspect university-erp_default`
3. Check DNS: `docker-compose exec core-api nslookup postgres`
4. Check connectivity: `docker-compose exec core-api ping postgres`
5. Check port: `docker-compose exec core-api nc -zv postgres 5432`

**Tools**:
- Docker network inspect
- Docker exec for commands
- nslookup for DNS
- ping for connectivity
- nc for port checking

## Future Enhancements

### Network Segmentation

**Status**: Not implemented

**Proposal**: Implement network segmentation:
- Separate networks for different tiers
- Frontend network for web services
- Backend network for data services
- Nginx connects both networks
- Better security

### Service Mesh

**Status**: Not implemented

**Proposal**: Implement service mesh:
- Istio or Linkerd
- Service-to-service encryption
- Traffic management
- Observability
- Better security

## Production Considerations

### Production Networking

**Production Deployment**:
- Use private networks for internal communication
- Use load balancer for external access
- Enable TLS for all external communication
- Configure firewall rules
- Monitor network traffic
- Implement network segmentation

### Network Monitoring

**Monitoring Metrics**:
- Network latency
- Network throughput
- Connection counts
- Error rates
- DNS resolution time

## Example Requests

### Check Network

**Request**:
```bash
docker network inspect university-erp_default
```

**Response**:
```json
{
  "Name": "university-erp_default",
  "Driver": "bridge",
  "Containers": {
    "university-erp-postgres": {
      "Name": "university-erp-postgres",
      "IPv4Address": "172.18.0.2/16"
    },
    "university-erp-redis": {
      "Name": "university-erp-redis",
      "IPv4Address": "172.18.0.3/16"
    }
  }
}
```

### Test Connectivity

**Request**:
```bash
docker-compose exec core-api ping postgres
```

**Response**:
```
PING postgres (172.18.0.2) 56(84) bytes of data.
64 bytes from postgres (172.18.0.2): icmp_seq=1 ttl=64 time=0.123 ms
```

## Example Responses

### DNS Resolution

**Request**:
```bash
docker-compose exec core-api nslookup postgres
```

**Response**:
```
Server:         127.0.0.11
Address:        127.0.0.11:53

Name:   postgres
Address: 172.18.0.2
```

## Sequence Diagrams

### Service Communication Flow

```
Core API → DNS Resolution → PostgreSQL IP
              ↓
         TCP Connection
              ↓
         Database Query
              ↓
         Response
```

## Architecture Diagrams

### Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Host Machine                             │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Port 3000    │  │  Port 5432    │  │  Port 6379     │
│  (Exposed)    │  │  (Exposed)    │  │  (Exposed)     │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                  Docker Network                            │
│                  university-erp_default                    │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  PostgreSQL    │  │  Redis         │
│  172.18.0.4   │  │  172.18.0.2   │  │  172.18.0.3    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How do Docker services communicate?

**Answer**: Docker services communicate via:
- Docker network (default bridge network)
- Service discovery via container names
- DNS resolution provided by Docker
- Services can resolve container names to IP addresses
- Communication happens within Docker network

### Q2: What is the difference between bridge and host network?

**Answer**: 
- **Bridge Network**: Services have their own network stack, isolated from host, can communicate with each other by container name
- **Host Network**: Services use host network stack, no isolation, better performance, port conflicts possible

### Q3: How do you secure Docker networking?

**Answer**: Security via:
- Expose only necessary ports
- Use network segmentation (separate networks)
- Enable TLS for external communication
- Configure firewall rules
- Use private networks for internal communication

## Exercises

### Exercise 1: Inspect Network

**Task**: Inspect Docker network.

**Steps**:
1. List networks: `docker network ls`
2. Inspect network: `docker network inspect university-erp_default`
3. Check containers in network
4. Check IP addresses
5. Test connectivity

**Verification**:
- Network inspected
- Containers listed
- IP addresses known
- Connectivity tested

### Exercise 2: Test Service Discovery

**Task**: Test service discovery.

**Steps**:
1. From Core API container, ping PostgreSQL
2. From Core API container, ping Redis
3. From Core API container, nslookup services
4. Test port connectivity
5. Verify DNS resolution

**Verification**:
- Service discovery works
- DNS resolution works
- Connectivity works

## Real Production Scenarios

### Scenario 1: Service Cannot Connect to Database

**Situation**: Core API cannot connect to PostgreSQL

**Response**:
1. Check PostgreSQL is running
2. Check network configuration
3. Check DNS resolution
4. Check port connectivity
5. Check firewall rules
6. Verify connection string

### Scenario 2: Port Conflict

**Situation**: Port already in use

**Response**:
1. Find process using port: `lsof -i :5432`
2. Kill process or change port
3. Update docker-compose.yml
4. Restart services
5. Verify no conflicts

## Navigation

**Next Section**: [03-Storage](./03-Storage.md)

**Previous Section**: [01-Docker-Services](./01-Docker-Services.md)

**Related Documentation**:
- [01-Docker-Services](./01-Docker-Services.md) - Docker services
- [15-Deployment](../15-Deployment/README.md) - Deployment details
- [17-Production](../17-Production/README.md) - Production guide
