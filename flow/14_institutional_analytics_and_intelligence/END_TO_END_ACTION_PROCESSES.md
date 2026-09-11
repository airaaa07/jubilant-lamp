# Institutional Analytics & Intelligence — End-to-End Action Processes

```
========================================================================================================================
MODULE 14: INSTITUTIONAL ANALYTICS & EXECUTIVE INTELLIGENCE
DOCUMENT: END_TO_END_ACTION_PROCESSES.md
TARGET PERSONAS: CHIEF DATA OFFICERS, BACKEND ENGINEERS, INSTITUTIONAL RESEARCH ANALYSTS
PRIMARY CONTROLLER: apps/core-api/src/modules/analytics/analytics.controller.ts
========================================================================================================================
```

---

## Action 14.1: Fetch Executive Cockpit Macro Telemetry

### 1. HTTP Request Lifecycle
- **Method**: `GET`
- **Path**: `/api/v1/analytics/exec`
- **Headers**:
  ```http
  Authorization: Bearer <JWT_TOKEN>
  X-University-Id: <UUID>
  ```
- **Guards**: `JwtAuthGuard`, `RolesGuard`
- **Authorized Roles**: `SuperAdmin`, `UnivAdmin`, `InstAdmin`, `Chairperson`, `President`, `Registrar`, `Finance Head`, `Controller of Examinations` (`EXEC_ROLES`).

### 2. Processing Pipeline (`AnalyticsService.getExecDashboard`)
1. Controller validates caller holds one of the statutory `EXEC_ROLES`.
2. Service establishes transaction-level read locks on analytical views or executes parallel aggregation queries:
   ```typescript
   const [enrollment, finance, academic, logistics] = await Promise.all([
     this.getEnrollmentKpi(universityId, caller.scope),
     this.getFinanceKpi(universityId, caller.scope),
     this.getAcademicHealthKpi(universityId, caller.scope),
     this.getLogisticsKpi(universityId, caller.scope)
   ]);
   ```
3. Queries compute:
   - Total active students (`Student.status = 'active'`).
   - Sum of settled fee collections vs open demands in `FeeDemand`.
   - Aggregate pass rate across all published `StudentTermResult` records.
   - Aggregate campus room occupancy in `HostelAllocation`.

### 3. Response Payload (`HTTP 200 OK`)
```json
{
  "success": true,
  "data": {
    "kpis": {
      "totalStudents": 12450,
      "growthPercentageYoY": 8.4,
      "totalRevenueCollected": 482000000.00,
      "budgetReceivables": 520000000.00,
      "collectionRate": 92.69,
      "overallPassRate": 88.42,
      "facultyStudentRatio": "1:15.2"
    },
    "charts": {
      "enrollmentFunnel": [
        { "stage": "Leads", "count": 28400 },
        { "stage": "Applications", "count": 18200 },
        { "stage": "Scrutinized", "count": 16400 },
        { "stage": "Offered", "count": 13500 },
        { "stage": "Enrolled", "count": 12450 }
      ],
      "attendanceRiskCohorts": [
        { "department": "Computer Science", "shortageCount": 14 },
        { "department": "Mechanical Engineering", "shortageCount": 28 }
      ]
    }
  }
}
```

---

## Action 14.2: Drill-Down Metric Aggregation (`/analytics/exec/detail`)

### 1. HTTP Request Lifecycle
- **Method**: `GET`
- **Path**: `/api/v1/analytics/exec/detail?metric=fees&group=department`
- **Guards**: `JwtAuthGuard`, `RolesGuard` (`Roles(...EXEC_ROLES)`)
- **Query Parameters**:
  - `metric`: `'admissions' | 'attendance' | 'fees' | 'examination' | 'library'`.
  - `group`: `'campus' | 'department' | 'batch'`.

### 2. Processing Pipeline
- Evaluates group-by expressions in SQL/Prisma:
  ```sql
  SELECT d.name AS department_name, 
         SUM(fd.amount_due) AS total_due, 
         SUM(fd.amount_paid) AS total_paid
  FROM fee_demands fd
  JOIN students s ON fd.student_id = s.id
  JOIN batches b ON s.batch_id = b.id
  JOIN courses c ON b.course_id = c.id
  JOIN departments d ON c.department_id = d.id
  WHERE d.university_id = $1
  GROUP BY d.name;
  ```
- Emits structured breakdown for interactive charting.

---
```
========================================================================================================================
END OF DOCUMENT: MODULE 14 END_TO_END_ACTION_PROCESSES.md
========================================================================================================================
```
