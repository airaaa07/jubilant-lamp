# Module 13: System Governance & Administration — Technical Architecture

> **Scope**: Immutable audit log stream, telecom SMS DLT regulatory pipeline, disaster recovery maintenance polling architecture, and dynamic navigation layout normalization.

---

## 1. Disaster Recovery & Global Maintenance Polling Architecture

During disruptive maintenance operations (such as a database snapshot restore), a global banner prevents user operations that could corrupt in-flight transactions.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as SuperAdmin
    participant Settings as SettingsPage.tsx
    participant CoreAPI as Core API (/api/backup)
    participant Redis as Redis Cache
    participant AllUsers as User Browsers (AdminLayout.tsx)

    Admin->>Settings: Clicks "Restore Snapshot" -> Confirms
    Settings->>CoreAPI: POST /api/backup/snapshots/:id/restore
    CoreAPI->>Redis: SET erp:maintenance { enabled: true, reason: "Database restore running" }
    
    par Background pg_restore
        CoreAPI->>CoreAPI: Executes pg_restore on PostgreSQL
    and Active Polling Loop
        AllUsers->>CoreAPI: GET /api/backup/maintenance (every 15s)
        CoreAPI->>Redis: GET erp:maintenance
        Redis-->>CoreAPI: { enabled: true, reason: "Database restore running" }
        CoreAPI-->>AllUsers: 200 OK { enabled: true, reason: "..." }
        AllUsers->>AllUsers: MaintenanceBanner mounts at top of screen (Yellow warning bar)
    end

    CoreAPI->>Redis: DEL erp:maintenance
    AllUsers->>CoreAPI: GET /api/backup/maintenance (next tick)
    CoreAPI-->>AllUsers: { enabled: false }
    AllUsers->>AllUsers: MaintenanceBanner dismounts automatically
```

---

## 2. Telecom SMS DLT Pipeline Architecture

Per regulatory mandates (TRAI / DLT), SMS payloads must strictly adhere to pre-approved header/body formats. Commit `b2c9fe5f` incorporates the operator template name alongside the numeric ID without modifying byte serialization.

```mermaid
flowchart TD
    Trigger["System Event (e.g. OTP / Fee Paid / Doc Verified)"] --> Resolver["Message Template Service"]
    Resolver --> FetchTemplate["Fetch MessageTemplate Record"]
    FetchTemplate --> DLTCheck["Verify DLT Metadata (Name, Numeric ID, Category)"]
    
    DLTCheck --> TokenSubstitution["Substitute Variables: {#var#} -> Actual Value"]
    TokenSubstitution --> LengthCheck["GSM 7-Bit Character & Multipart Segment Counter"]
    
    LengthCheck --> Dispatch["Dispatch to Telecom SMS Gateway via HTTP/SMPP"]
    Dispatch --> DeliveryLog["Prisma: NotificationLog.create({ status: 'SENT', dltId })"]
```

---

## 3. Navigation Layout Normalization Model

Per `navLayout.ts`, layouts stored in `University.config.navLayout` are normalized upon load and save to ensure consistency against `ALL_NAV_TOS`.

$$\text{Normalized Layout} = (\text{Stored Layout} \cap \text{Known Targets}) \cup (\text{Known Targets} \setminus \text{Stored Targets})$$

This mathematical property guarantees:
1. Dead or deleted routes are automatically pruned from stored folders.
2. Newly developed modules (appended to `NAV_ITEMS`) automatically appear at the end of the top level without requiring manual configuration.
3. No duplicate routes can exist across folders and top-level entries.
