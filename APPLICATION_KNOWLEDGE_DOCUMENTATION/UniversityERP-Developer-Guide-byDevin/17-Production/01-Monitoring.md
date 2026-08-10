# Monitoring

## Purpose

This document explains monitoring in the University ERP system. It details how monitoring is implemented, monitoring tools, metrics, and alerting.

## Why This Document Exists

**Confirmed by Code**: The University ERP requires effective monitoring. Understanding monitoring is critical for:
- Monitoring system health
- Detecting issues early
- Performance optimization
- Capacity planning
- Troubleshooting issues

Without understanding monitoring, developers may struggle with production issues or may not detect issues early.

## Where This Is Used

- **Onboarding**: New developers learn monitoring
- **Feature Development**: Adding monitoring to features
- **Code Reviews**: Reviewing monitoring approaches
- **Production**: Monitoring production systems
- **Troubleshooting**: Troubleshooting issues

## Dependencies

### Monitoring Dependencies

**Confirmed by Code**: Monitoring depends on:

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Alertmanager**: Alerting
- **Health Checks**: Health check endpoints
- **Metrics**: Application metrics

## Internal Architecture

### Monitoring Architecture

**Confirmed by Code**: Monitoring follows metrics-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Metrics Exporter                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Prometheus                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Grafana                                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Alerts                                        │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Prometheus Metrics

**Confirmed by Code**: Prometheus metrics for monitoring.

**Metrics Service**:
```typescript
import { Injectable } from '@nestjs/common';
import { Counter, Histogram, Registry } from 'prom-client';

@Injectable()
export class MetricsService {
  private registry: Registry;
  private httpRequestsTotal: Counter;
  private httpRequestDuration: Histogram;

  constructor() {
    this.registry = new Registry();
    
    this.httpRequestsTotal = new Counter({
      name: 'http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status_code'],
      registers: [this.registry],
    });

    this.httpRequestDuration = new Histogram({
      name: 'http_request_duration_seconds',
      help: 'HTTP request duration in seconds',
      labelNames: ['method', 'route'],
      buckets: [0.1, 0.5, 1, 2, 5],
      registers: [this.registry],
    });
  }

  incrementHttpRequests(method: string, route: string, statusCode: number) {
    this.httpRequestsTotal.inc({ method, route, status_code: statusCode });
  }

  observeHttpRequestDuration(method: string, route: string, duration: number) {
    this.httpRequestDuration.observe({ method, route }, duration / 1000);
  }

  getMetrics() {
    return this.registry.metrics();
  }
}
```

**What This Does**:
- **Counter**: Count HTTP requests
- **Histogram**: Measure request duration
- **incrementHttpRequests**: Increment request counter
- **observeHttpRequestDuration**: Observe request duration
- **getMetrics**: Get metrics for Prometheus

### Metrics Middleware

**Confirmed by Code**: Middleware for collecting metrics.

**MetricsMiddleware**:
```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { MetricsService } from '../metrics.service';

@Injectable()
export class MetricsMiddleware implements NestMiddleware {
  constructor(private metricsService: MetricsService) {}

  use(req: Request, res: Response, next: NextFunction) {
    const start = Date.now();

    res.on('finish', () => {
      const duration = Date.now() - start;
      this.metricsService.incrementHttpRequests(req.method, req.route?.path || req.path, res.statusCode);
      this.metricsService.observeHttpRequestDuration(req.method, req.route?.path || req.path, duration);
    });

    next();
  }
}
```

**What This Does**:
- **MetricsMiddleware**: Middleware for metrics
- **start**: Record start time
- **finish**: Record metrics on response finish
- **incrementHttpRequests**: Increment request counter
- **observeHttpRequestDuration**: Observe request duration

### Prometheus Endpoint

**Confirmed by Code**: Prometheus endpoint for scraping.

**Metrics Controller**:
```typescript
@Controller('metrics')
export class MetricsController {
  constructor(private metricsService: MetricsService) {}

  @Get()
  getMetrics() {
    return this.metricsService.getMetrics();
  }
}
```

**What This Does**:
- **getMetrics**: Return metrics for Prometheus scraping

## Database Interactions

### Monitoring-Database Flow

**Confirmed by Code**: Database metrics collected.

**Flow**:
```
Monitoring → Database Metrics → Prometheus → Grafana
```

## Redis Interactions

### Monitoring-Redis Flow

**Confirmed by Code**: Redis metrics collected.

**Flow**:
```
Monitoring → Redis Metrics → Prometheus → Grafana
```

## Queue Interactions

### Monitoring-Queue Flow

**Confirmed by Code**: Queue metrics collected.

**Flow**:
```
Monitoring → Queue Metrics → Prometheus → Grafana
```

## Worker Interactions

### Monitoring-Worker Flow

**Confirmed by Code**: Worker metrics collected.

**Flow**:
```
Monitoring → Worker Metrics → Prometheus → Grafana
```

## Business Rules

### Monitoring Rules

**Confirmed by Code**: Monitoring follows these rules:

1. **Metrics**: Collect relevant metrics
2. **Labels**: Use meaningful labels
3. **Buckets**: Use appropriate histogram buckets
4. **Scraping**: Configure Prometheus scraping
5. **Alerting**: Configure alerting rules

### Alerting Rules

**Confirmed by Code**: Alerting rules:

1. **Thresholds**: Set appropriate thresholds
2. **Severity**: Use appropriate severity levels
3. **Notifications**: Configure notifications
4. **Escalation**: Configure escalation
5. **Silence**: Configure silence periods

## Security

### Monitoring Security

**Confirmed by Code**: Security considerations for monitoring:

1. **Access Control**: Restrict monitoring access
2. **Authentication**: Authenticate monitoring access
3. **Encryption**: Encrypt monitoring data
4. **Network**: Use private networks
5. **Audit**: Log monitoring access

## Performance Considerations

### Monitoring Performance

**Confirmed by Code**: Performance considerations:

1. **Metrics Overhead**: Minimize metrics overhead
2. **Scraping Interval**: Configure appropriate scraping interval
3. **Cardinality**: Control metric cardinality
4. **Retention**: Configure appropriate retention
5. **Optimization**: Optimize metrics collection

## Common Mistakes

### Mistake 1: High Cardinality

**Symptom**: High memory usage

**Cause**: High metric cardinality

**Fix**:
```typescript
// Use fewer labels
this.httpRequestsTotal.inc({ method, route, status_code }); // OK
this.httpRequestsTotal.inc({ method, route, status_code, userId }); // NOT OK
```

### Mistake 2: Not Setting Buckets

**Symptom**: Inaccurate histograms

**Cause**: Not setting appropriate buckets

**Fix**:
```typescript
// Set appropriate buckets
buckets: [0.1, 0.5, 1, 2, 5], // OK
buckets: [0.001, 0.002, 0.003], // NOT OK
```

### Mistake 3: Not Configuring Alerts

**Symptom**: Issues not detected

**Cause**: Not configuring alerts

**Fix**:
```yaml
# Configure alerts
groups:
- name: alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.05
    annotations:
      summary: High error rate
```

## Debugging Guide

### Monitoring Debugging

**Issue**: Metrics not showing

**Investigation**:
1. Check Prometheus configuration
2. Check metrics endpoint
3. Check scraping configuration
4. Check labels
5. Check Grafana configuration

**Tools**:
- Prometheus UI
- Grafana UI
- Metrics endpoint
- Logs

## Future Enhancements

### Distributed Tracing

**Status**: Not implemented

**Proposal**: Implement distributed tracing:
- OpenTelemetry integration
- Trace requests across services
- Better debugging
- More complex
- Better for production

### Synthetic Monitoring

**Status**: Not implemented

**Proposal**: Implement synthetic monitoring:
- Simulate user actions
- Monitor from multiple locations
- Better visibility
- More complex
- Better for production

## Production Considerations

### Production Monitoring

**Production Deployment**:
- Enable metrics collection
- Configure Prometheus
- Configure Grafana
- Configure alerting
- Monitor monitoring system

### Monitoring Monitoring

**Monitoring Metrics**:
- Metric collection rate
- Scraping success rate
- Alert firing rate
- Dashboard load time
- Query performance

## Example Requests

### Monitoring Example

**Get Metrics**:
```bash
curl http://localhost:3000/metrics
```

**Prometheus Query**:
```bash
curl http://prometheus:9090/api/v1/query?query=rate(http_requests_total[5m])
```

## Example Responses

### Monitoring Response

**Response**: Metrics output

```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",route="/users",status_code="200"} 1234
```

## Sequence Diagrams

### Monitoring Flow

```
Application → Metrics → Prometheus → Grafana → Alerts
```

## Architecture Diagrams

### Monitoring Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Application                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Metrics Exporter                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Prometheus                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Grafana                                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Alerts                                        │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How is monitoring implemented?

**Answer**: Monitoring via:
- Prometheus for metrics collection
- Grafana for visualization
- Metrics middleware for collection
- Health checks for availability
- Alerting for notifications

### Q2: What metrics do you collect?

**Answer**: Metrics collected via:
- HTTP request count
- HTTP request duration
- Error rate
- Database query duration
- Redis operation duration

### Q3: How do you configure alerts?

**Answer**: Alert configuration via:
- Prometheus alerting rules
- Threshold-based alerts
- Severity levels
- Notification channels
- Escalation policies

## Exercises

### Exercise 1: Add Metrics

**Task**: Add metrics to an endpoint.

**Steps**:
1. Create metric
2. Add to metrics service
3. Increment metric
4. Test metrics
5. Verify in Prometheus

**Verification**:
- Metric created
- Metric incremented
- Metrics visible
- Prometheus scraping works
- Tests pass

### Exercise 2: Create Grafana Dashboard

**Task**: Create a Grafana dashboard.

**Steps**:
1. Create dashboard
2. Add panels
3. Configure queries
4. Set up alerts
5. Test dashboard

**Verification**:
- Dashboard created
- Panels added
- Queries configured
- Alerts configured
- Dashboard works

## Real Production Scenarios

### Scenario 1: High Error Rate

**Situation**: High error rate alert

**Response**:
1. Check alerts
2. Check logs
3. Check metrics
4. Identify root cause
5. Fix issue

### Scenario 2: Slow Response Time

**Situation**: Slow response time alert

**Response**:
1. Check metrics
2. Check database queries
3. Check Redis
4. Optimize queries
5. Monitor improvement

## Navigation

**Next Section**: [02-Logging](./02-Logging.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [02-Infrastructure](../02-Infrastructure/README.md) - Infrastructure details
- [15-Deployment](../15-Deployment/README.md) - Deployment details
