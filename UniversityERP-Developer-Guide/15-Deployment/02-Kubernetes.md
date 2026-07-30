# Kubernetes

## Purpose

This document explains Kubernetes in the University ERP system. It details how Kubernetes is used for orchestration, deployment configurations, and production management.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses Kubernetes for production orchestration. Understanding Kubernetes is critical for:
- Deploying to production
- Managing containers
- Scaling applications
- Debugging Kubernetes issues
- Optimizing Kubernetes resources

Without understanding Kubernetes, developers may struggle with production deployment or may introduce Kubernetes-related bugs.

## Where This Is Used

- **Onboarding**: New developers learn Kubernetes
- **Feature Development**: Preparing for deployment
- **Code Reviews**: Reviewing Kubernetes configurations
- **Production**: Deploying to production
- **Scaling**: Scaling applications

## Dependencies

### Kubernetes Dependencies

**Confirmed by Code**: Kubernetes depends on:

- **Kubernetes Cluster**: Kubernetes runtime
- **Docker**: Container runtime
- **kubectl**: Kubernetes CLI
- **Helm**: Package manager (optional)

## Internal Architecture

### Kubernetes Architecture

**Confirmed by Code**: Kubernetes follows cluster-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                           │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  Admin Portal  │  │  PostgreSQL     │
│  Deployment   │  │  Deployment     │  │  Deployment     │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Services                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Ingress                                       │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Kubernetes Deployment (Core API)

**Confirmed by Code**: Kubernetes deployment for backend API.

**core-api-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: core-api
  labels:
    app: core-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: core-api
  template:
    metadata:
      labels:
        app: core-api
    spec:
      containers:
      - name: core-api
        image: university-erp/core-api:latest
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: core-api-secrets
              key: database-url
        - name: REDIS_HOST
          value: "redis"
        - name: REDIS_PORT
          value: "6379"
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: core-api-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

**What This Does**:
- **replicas**: 3 replicas for high availability
- **image**: Docker image
- **env**: Environment variables from secrets
- **resources**: Resource limits and requests
- **livenessProbe**: Health check
- **readinessProbe**: Readiness check

### Kubernetes Service (Core API)

**Confirmed by Code**: Kubernetes service for backend API.

**core-api-service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: core-api
spec:
  selector:
    app: core-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: ClusterIP
```

**What This Does**:
- **selector**: Selects pods with label
- **ports**: Port configuration
- **type**: ClusterIP for internal access

### Kubernetes Deployment (Admin Portal)

**Confirmed by Code**: Kubernetes deployment for frontend.

**admin-portal-deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: admin-portal
  labels:
    app: admin-portal
spec:
  replicas: 2
  selector:
    matchLabels:
      app: admin-portal
  template:
    metadata:
      labels:
        app: admin-portal
    spec:
      containers:
      - name: admin-portal
        image: university-erp/admin-portal:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
```

**What This Does**:
- **replicas**: 2 replicas for frontend
- **image**: Docker image
- **resources**: Resource limits and requests
- **livenessProbe**: Health check

### Kubernetes Ingress

**Confirmed by Code**: Kubernetes ingress for routing.

**ingress.yaml**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: university-erp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.universityerp.com
    - admin.universityerp.com
    secretName: university-erp-tls
  rules:
  - host: api.universityerp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: core-api
            port:
              number: 80
  - host: admin.universityerp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: admin-portal
            port:
              number: 80
```

**What This Does**:
- **tls**: TLS configuration
- **rules**: Routing rules
- **annotations**: Ingress annotations
- **cert-manager**: Automatic TLS

## Database Interactions

### Kubernetes-Database Flow

**Confirmed by Code**: Database deployed as Kubernetes deployment or external service.

**Flow**:
```
Kubernetes → PostgreSQL Deployment → Database
```

## Redis Interactions

### Kubernetes-Redis Flow

**Confirmed by Code**: Redis deployed as Kubernetes deployment or external service.

**Flow**:
```
Kubernetes → Redis Deployment → Cache
```

## Queue Interactions

### Kubernetes-Queue Flow

**Confirmed by Code**: Queue runs in same pod as API.

**Flow**:
```
Kubernetes → Core API Pod → Bull Queue
```

## Worker Interactions

### Kubernetes-Worker Flow

**Confirmed by Code**: Workers run in same pod as API.

**Flow**:
```
Kubernetes → Core API Pod → Workers
```

## Business Rules

### Kubernetes Rules

**Confirmed by Code**: Kubernetes follows these rules:

1. **Replicas**: Multiple replicas for high availability
2. **Resource Limits**: Set resource limits and requests
3. **Health Checks**: Implement liveness and readiness probes
4. **Secrets**: Use Kubernetes secrets for sensitive data
5. **Services**: Use services for internal communication

### Deployment Rules

**Confirmed by Code**: Deployment rules:

1. **Rolling Updates**: Use rolling updates for zero downtime
2. **Rollback**: Ability to rollback deployments
3. **Strategy**: Configure deployment strategy
4. **Labels**: Use labels for pod selection
5. **Selectors**: Use selectors for service routing

## Security

### Kubernetes Security

**Confirmed by Code**: Security considerations for Kubernetes:

1. **Secrets**: Use Kubernetes secrets
2. **RBAC**: Configure RBAC for access control
3. **Network Policies**: Use network policies
4. **Pod Security**: Use pod security policies
5. **Image Security**: Use trusted images

## Performance Considerations

### Kubernetes Performance

**Confirmed by Code**: Performance considerations:

1. **Resource Limits**: Set appropriate resource limits
2. **Horizontal Pod Autoscaler**: Use HPA for scaling
3. **Node Affinity**: Use node affinity for performance
4. **Pod Anti-Affinity**: Use pod anti-affinity for HA
5. **Resource Requests**: Set appropriate resource requests

## Common Mistakes

### Mistake 1: Not Setting Resource Limits

**Symptom**: Resource exhaustion

**Cause**: Not setting resource limits

**Fix**:
```yaml
# Set resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Mistake 2: Not Using Secrets

**Symptom**: Secrets exposed in config

**Cause**: Not using Kubernetes secrets

**Fix**:
```yaml
# Use secrets
env:
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: core-api-secrets
      key: jwt-secret
```

### Mistake 3: Not Implementing Health Checks

**Symptom**: Unhealthy pods not restarted

**Cause**: Not implementing health checks

**Fix**:
```yaml
# Add health checks
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
```

## Debugging Guide

### Kubernetes Debugging

**Issue**: Pod not starting

**Investigation**:
1. Check pod logs
2. Check pod events
3. Check resource limits
4. Check configuration
5. Check networking

**Tools**:
- kubectl logs
- kubectl describe
- kubectl get events
- kubectl exec

## Future Enhancements

### Helm Charts

**Status**: Not implemented

**Proposal**: Implement Helm charts:
- Easier deployment
- Version management
- Better configuration management
- More complex
- Better for production

### Horizontal Pod Autoscaler

**Status**: Not implemented

**Proposal**: Implement HPA:
- Automatic scaling
- Better resource utilization
- Cost optimization
- More complex
- Better for production

## Production Considerations

### Production Kubernetes

**Production Deployment**:
- Use multiple replicas
- Set resource limits
- Use secrets
- Implement health checks
- Enable monitoring

### Kubernetes Monitoring

**Monitoring Metrics**:
- Pod resource usage
- Pod uptime
- Deployment status
- Service availability
- Ingress metrics

## Example Requests

### Kubernetes Example

**Deploy to Kubernetes**:
```bash
kubectl apply -f k8s/
```

**Check pod status**:
```bash
kubectl get pods
```

## Example Responses

### Kubernetes Response

**Response**: Deployment successful

```bash
deployment.apps/core-api created
service/core-api created
```

## Sequence Diagrams

### Kubernetes Flow

```
kubectl apply → Deployment → Pods → Services → Ingress → External Access
```

## Architecture Diagrams

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Kubernetes Cluster                           │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Core API     │  │  Admin Portal  │  │  PostgreSQL     │
│  Deployment   │  │  Deployment     │  │  Deployment     │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Services                                      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Ingress                                       │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is Kubernetes used in the system?

**Answer**: Kubernetes via:
- Container orchestration
- Deployment management
- Service discovery
- Load balancing
- Auto-scaling

### Q2: How do you configure resource limits?

**Answer**: Resource limits via:
- Set requests for minimum resources
- Set limits for maximum resources
- Configure in deployment spec
- Monitor resource usage
- Adjust based on needs

### Q3: How do you handle secrets in Kubernetes?

**Answer**: Secrets handling via:
- Kubernetes secrets
- Environment variables from secrets
- RBAC for access control
- Secret encryption
- Secret rotation

## Exercises

### Exercise 1: Create Kubernetes Deployment

**Task**: Create a Kubernetes deployment.

**Steps**:
1. Create deployment YAML
2. Configure replicas
3. Set resource limits
4. Add health checks
5. Test deployment

**Verification**:
- Deployment created
- Replicas configured
- Resource limits set
- Health checks added
- Tests pass

### Exercise 2: Create Kubernetes Service

**Task**: Create a Kubernetes service.

**Steps**:
1. Create service YAML
2. Configure selector
3. Configure ports
4. Choose service type
5. Test service

**Verification**:
- Service created
- Selector configured
- Ports configured
- Service accessible
- Tests pass

## Real Production Scenarios

### Scenario 1: Pod Not Starting

**Situation**: Pod not starting

**Response**:
1. Check pod logs
2. Check pod events
3. Check resource limits
4. Fix issue
5. Restart pod

### Scenario 2: High Resource Usage

**Situation**: High resource usage

**Response**:
1. Check resource limits
2. Check resource requests
3. Optimize application
4. Scale horizontally
5. Monitor resources

## Navigation

**Next Section**: [03-CI-CD](./03-CI-CD.md)

**Previous Section**: [01-Docker](./01-Docker.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [17-Production](../17-Production/README.md) - Production details
