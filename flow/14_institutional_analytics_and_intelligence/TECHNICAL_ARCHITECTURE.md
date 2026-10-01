# Institutional Analytics & Intelligence — Technical Architecture

```
========================================================================================================================
MODULE 14: INSTITUTIONAL ANALYTICS & EXECUTIVE INTELLIGENCE
DOCUMENT: TECHNICAL_ARCHITECTURE.md
ARCHITECTURE: HIGH-THROUGHPUT READ-OPTIMIZED AGGREGATION ENGINE
PERSISTENCE: POSTGRESQL MATERIALIZED VIEWS & REDIS CACHING TIER
========================================================================================================================
```

---

## 1. High-Performance Analytical Engine Topology

Executive analytics queries over millions of historical attendance, marks, and ledger records must not degrade the performance of live transactional operations (such as student fee checkouts or biometric attendance punches):

```mermaid
graph TD
    subgraph Transactional OLTP Core
        PG_PRIMARY[("PostgreSQL 16 Primary DB<br/>(Write-Master: 138 Prisma Models)")]
        WAL[Continuous WAL Stream]
    end

    subgraph Analytical Read Replica & Caching Tier
        WAL --> PG_REPLICA[("PostgreSQL Read-Only Replica<br/>(Aggregations & Group-By Queries)")]
        REDIS[("Redis Cluster<br/>(Cached KPI Payloads, TTL: 5 Mins)")]
    end

    subgraph Analytics Service
        ANALYTICS[AnalyticsService<br/>(analytics.service.ts)]
    end

    subgraph Consuming Clients
        EXEC_PORTAL[Executive Cockpit<br/>(/analytics/exec)]
        FAC_PORTAL[Faculty Workload Dashboard<br/>(/analytics/me)]
        NAAC_EXPORT[NAAC / NIRF Exporter]
    end

    ANALYTICS -->|Check Cache Hit| REDIS
    REDIS -.->|Cache Miss| ANALYTICS
    ANALYTICS -->|Execute Aggregations| PG_REPLICA
    ANALYTICS -->|Populate Cache| REDIS

    EXEC_PORTAL --> ANALYTICS
    FAC_PORTAL --> ANALYTICS
    NAAC_EXPORT --> ANALYTICS
```

---

## 2. Analytical Caching & Invalidation Policy

1. **Macro KPI Cache Key**: `analytics:exec:kpis:<universityId>:<academicYear>` (TTL: 300 seconds / 5 minutes).
2. **Cache Invalidation Triggers**:
   - Automated cache bust on **End-Semester Result Publishing** (`results.service.ts`).
   - Automated cache bust on **Bulk Recurring Billing Run** (`fee.service.ts`).
   - Manual on-demand cache refresh button available to SuperAdmin / UnivAdmin on the dashboard.

---
```
========================================================================================================================
END OF DOCUMENT: MODULE 14 TECHNICAL_ARCHITECTURE.md
========================================================================================================================
```
