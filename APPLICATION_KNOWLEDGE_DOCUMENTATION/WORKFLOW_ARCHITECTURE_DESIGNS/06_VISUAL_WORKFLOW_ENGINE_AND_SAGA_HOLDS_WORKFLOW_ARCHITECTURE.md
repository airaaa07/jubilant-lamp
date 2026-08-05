# Technical Workflow Architecture: Visual Workflow Engine & Saga Holds

## Overview
This document details the end-to-end technical workflow architecture, graph execution engine, dynamic actor resolution, payment gate holds, and Saga pattern resource reservations.

---

## 🔄 End-to-End Sequence Diagram: Visual Workflow & Saga Hold Engine

```mermaid
sequenceDiagram
    autonumber
    actor Initiator as Initiator (User / Student)
    participant WfC as WorkflowController
    participant WfEngine as WorkflowEngineService
    participant WfActor as WorkflowActorResolver
    participant ResS as ReservationService (Saga Hold)
    participant Cron as WorkflowSchedulerCron (Midnight)
    participant DB as PostgreSQL Database

    Initiator->>WfC: POST /api/v1/workflow/instances (Start Instance for Entity)
    WfC->>WfEngine: startInstance(definitionId, entityType, entityId)
    WfEngine->>DB: Fetch WorkflowDefinition Graph (States & Transitions)
    WfEngine->>DB: INSERT into workflow_instances (status: "IN_PROGRESS")
    WfEngine->>DB: INSERT into workflow_step_instances (current_state: "SUBMITTED")

    note over WfEngine,WfActor: Step 1: Resolve Dynamic Approver Actor
    WfEngine->>WfActor: resolveActor(role: "HOD", departmentId)
    WfActor->>DB: Query User with role HOD in user's department
    WfActor-->>WfEngine: Return HOD userId

    actor Approver as HOD Approver
    Approver->>WfC: POST /api/v1/workflow/instances/:id/action (Approve)
    WfEngine->>DB: UPDATE workflow_step_instances status = "APPROVED"

    note over WfEngine,ResS: Step 2: Resource Reservation (Saga Pattern Hold)
    WfEngine->>ResS: createResourceHold(resourceId, duration: 24 Hours)
    ResS->>DB: INSERT into workflow_holds (hold_token, status: "ACTIVE", expires_at)
    WfEngine->>DB: UPDATE workflow_instances status = "AWAITING_PAYMENT"

    note over Cron,WfEngine: Case A: Payment Timeout Elapsed (Midnight Cron)
    Cron->>WfEngine: expirePaymentDemands()
    WfEngine->>DB: Query workflow_holds WHERE expires_at < NOW() AND status = 'ACTIVE'
    WfEngine->>ResS: releaseResourceHold(hold_token)
    ResS->>DB: UPDATE workflow_holds status = "EXPIRED"
    WfEngine->>DB: UPDATE workflow_instances status = "EXPIRED"

    note over WfEngine,ResS: Case B: Successful Payment Settlement
    WfEngine->>ResS: confirmResourceReservation(hold_token)
    ResS->>DB: UPDATE workflow_holds status = "CONFIRMED"
    WfEngine->>DB: UPDATE workflow_instances status = "APPROVED"
```

---

## 🔀 Workflow Instance State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Graph Created
    DRAFT --> ACTIVE: Published by Admin
    ACTIVE --> IN_PROGRESS: Triggered by Entity Action
    IN_PROGRESS --> AWAITING_APPROVAL: Step Transition to Approval Node
    AWAITING_APPROVAL --> AWAITING_PAYMENT: Approved -> Payment Node Required
    AWAITING_PAYMENT --> APPROVED: Payment Received -> Final State Reached
    AWAITING_APPROVAL --> REJECTED: Rejected by Approver Node
    AWAITING_PAYMENT --> EXPIRED: Payment Timeout (Midnight Cron)
    IN_PROGRESS --> CANCELLED: Aborted by Initiator
    APPROVED --> [*]
    REJECTED --> [*]
    EXPIRED --> [*]
    CANCELLED --> [*]
```

---

## ⚙️ Saga Pattern Resource Reservation Model

When a multi-step workflow requires reserving physical facilities (auditoriums, labs, hostels) or holding fees:

1. **Soft Hold Phase**: `ReservationService` creates a `WorkflowHold` record with a 24-hour expiration window. The resource is marked `HELD` to prevent double-booking.
2. **Commit Phase**: Upon successful payment confirmation via Razorpay, the hold is converted to `CONFIRMED`.
3. **Rollback (Compensating Action) Phase**: If payment is not completed within 24 hours, the `WorkflowSchedulerService` cron executes a compensating action: releases the soft hold, returns resource status to `AVAILABLE`, and cancels the workflow instance.
