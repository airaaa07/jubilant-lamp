# Module 13: System Governance & Administration — End-to-End Action Processes

> **Scope**: Backend API endpoints, DTO validation schemas, and database operations for security policy enforcement, SMS DLT registrations (commit `b2c9fe5f`), navigation menu layouts, database backup/restore orchestration, and immutable audit trails.

---

## Action 1: Save SMS Template with DLT Template Name (`PUT /api/settings/message-templates/:key`)

Per commit `b2c9fe5f`, the service records `dltTemplateName` alongside `dltTemplateId` in the template configuration without altering sending payloads.

- **HTTP Method & URL**: `PUT /api/settings/message-templates/:key`
- **Guards**: `JwtAuthGuard`, `RolesGuard('SuperAdmin', 'UnivAdmin')`
- **Request Body (DTO: `SaveMessageTemplateDto`)**:
  ```json
  {
    "channel": "SMS",
    "dltTemplateName": "UNIV_DOC_VERIFY_SUBMIT",
    "dltTemplateId": "140716892301928",
    "category": "SERVICE_IMPLICIT",
    "approvalDate": "2026-08-15",
    "body": "Dear {#var#}, your document verification request for {#var#} has been received by {#var#}. Ref: {#var#}."
  }
  ```
- **Backend Flow (Commit `b2c9fe5f`)**:
  1. Validates DLT numeric ID format.
  2. Ensures variable slots in body match approved DLT patterns (`{#var#}` or `{#var1#}`).
  3. Saves `dltTemplateName` as an inert metadata attribute stored alongside the override JSON.
- **Prisma Database Mutation**:
  ```prisma
  const template = await prisma.messageTemplate.upsert({
    where: {
      key_universityId: {
        key: params.key,
        universityId: req.user.universityId
      }
    },
    create: {
      key: params.key,
      channel: dto.channel,
      body: dto.body,
      metadata: {
        dltTemplateName: dto.dltTemplateName,
        dltTemplateId: dto.dltTemplateId,
        category: dto.category,
        approvalDate: dto.approvalDate
      },
      universityId: req.user.universityId
    },
    update: {
      body: dto.body,
      metadata: {
        dltTemplateName: dto.dltTemplateName,
        dltTemplateId: dto.dltTemplateId,
        category: dto.category,
        approvalDate: dto.approvalDate
      }
    }
  });
  ```
- **Response (200 OK)**:
  ```json
  {
    "key": "doc_verification_submitted",
    "channel": "SMS",
    "dltTemplateName": "UNIV_DOC_VERIFY_SUBMIT",
    "dltTemplateId": "140716892301928",
    "updatedAt": "2026-09-11T12:00:00.000Z"
  }
  ```

---

## Action 2: Save Navigation Layout (`PUT /api/settings/nav-layout`)

Per `navLayout.ts` and commit `71e2fdf3`:

- **HTTP Method & URL**: `PUT /api/settings/nav-layout`
- **Request Body (DTO: `NavLayoutDto`)**:
  ```json
  {
    "entries": [
      { "type": "item", "to": "/dashboard" },
      { "type": "item", "to": "/notice-board" },
      {
        "type": "folder",
        "id": "f_academic_01",
        "label": "Academic Management",
        "collapsed": true,
        "items": ["/attendance", "/timetable", "/exams", "/admissions"]
      }
    ]
  }
  ```
- **Backend Flow**:
  1. Runs `normalizeLayout(dto, ALL_NAV_TOS)` to prune dead routes and deduplicate items.
  2. Saves normalized layout to `University.config.navLayout`.
- **Response (200 OK)**: `{ "success": true, "layout": { "entries": [...] } }`

---

## Action 3: Trigger Database Restore & Maintenance Mode (`POST /api/backup/snapshots/:id/restore`)

- **HTTP Method & URL**: `POST /api/backup/snapshots/:id/restore`
- **Guards**: `JwtAuthGuard`, `RolesGuard('SuperAdmin')`
- **Backend Flow**:
  1. Sets Redis maintenance key: `SET university:maintenance:enabled true EX 3600`.
  2. Sets maintenance reason: `"Database restore from snapshot 2026-09-10.dump"`.
  3. Spawns shell worker to run `pg_restore` into PostgreSQL database.
  4. Once complete, restarts Nginx keepalive pools per commit `af4aa1d7`.
  5. Clears Redis maintenance key.
- **Response (202 Accepted)**:
  ```json
  {
    "status": "MAINTENANCE_STARTED",
    "snapshotId": "snap_20260910_0200",
    "estimatedDurationSeconds": 45
  }
  ```
