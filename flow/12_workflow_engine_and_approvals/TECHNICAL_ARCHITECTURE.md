# Module 12: Visual Workflow Engine & Approvals — Technical Architecture

> **Scope**: Directed graph execution engine, Saga pattern reservation holds, SLA aging algorithms, and workflow data models.

---

## 1. Directed Graph State Machine Execution Model

Workflow definitions represent deterministic finite state automata (DFA). Transitions are evaluated using incoming user actions and conditional predicates.

```mermaid
graph LR
    SUBMITTED(("SUBMITTED<br/>(Start)")) -->|Action: Forward| DEPT_REVIEW["DEPT_REVIEW<br/>(Actor: HOD)"]
    DEPT_REVIEW -->|Action: Approve| FEE_PAYMENT["FEE_PAYMENT<br/>(Actor: Student)"]
    DEPT_REVIEW -->|Action: Reject| REJECTED((("REJECTED<br/>(Terminal)")))
    
    FEE_PAYMENT -->|Event: Paid| ISSUANCE["ISSUANCE<br/>(Actor: Registrar)"]
    FEE_PAYMENT -->|Timeout: 48h| EXPIRED((("EXPIRED<br/>(Terminal)")))
    
    ISSUANCE -->|Action: Complete| COMPLETED((("COMPLETED<br/>(Terminal)")))
```

---

## 2. Saga Pattern Resource Reservation Holds

When a workflow requires scarce resources (hostel room bed, admission seat, bus pass quota), the engine places a temporary **Saga Hold** (`WorkflowReservation`).

```mermaid
sequenceDiagram
    autonumber
    participant Engine as Workflow Engine
    participant DB as Prisma DB
    participant Resource as Hostel / Seat Master

    Engine->>Resource: Place temporary reservation hold (Hold TTL: 48 Hours)
    Resource->>DB: Increment reservedSeats, decrement availableCapacity
    
    alt Workflow Approved & Paid within TTL
        Engine->>Resource: Commit Reservation
        Resource->>DB: Convert reservedSeats -> filledSeats (Permanent)
    else Workflow Rejected or TTL Expired
        Engine->>Resource: Compensating Transaction (Rollback Hold)
        Resource->>DB: Decrement reservedSeats, restore availableCapacity
    end
```

---

## 3. Workflow Entity Relationships

```mermaid
erDiagram
    WorkflowDefinition ||--o{ WorkflowState : "defines states"
    WorkflowDefinition ||--o{ WorkflowTransition : "defines edges"
    WorkflowDefinition ||--o{ WorkflowInstance : "instantiates"
    
    WorkflowInstance ||--o{ WorkflowTask : "assigns pending"
    WorkflowInstance ||--o{ WorkflowInstanceEvent : "records history"
    WorkflowInstance ||--o{ WorkflowReservation : "holds saga resources"
    
    WorkflowState ||--o{ WorkflowTransition : "from state"
    WorkflowState ||--o{ WorkflowTransition : "to state"

    WorkflowInstance {
        string id PK
        string workflowDefinitionId FK
        string currentStateId FK
        string status
        string initiatedById FK
        datetime createdAt
    }

    WorkflowTask {
        string id PK
        string workflowInstanceId FK
        string assignedRole
        string assignedUserId FK
        datetime slaExpiresAt
        string status
        string remarks
    }
```
