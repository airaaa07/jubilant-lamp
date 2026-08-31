# Action Lifecycle Manual: Workflow Engine & Saga Resource Holds

## Action 6.1: Visual Workflow Definition & Publication

### 1. Visual Graph Composition
- **Role**: SuperAdmin / Process Architect
- **Screen**: `WorkflowDesignerPage.tsx`
- Adds approval nodes (HOD, Dean, Finance), payment gates, condition branches, and resource reservation holds.
- Connects nodes with transitions.
- Clicks **Save Graph** -> `PUT /api/workflow/definitions/:id/graph`.
- Clicks **Publish** -> `POST /api/workflow/definitions/:id/publish` (activates definition).

---

## Action 6.2: Workflow Instance Execution & Actor Inbox Routing

### 1. Instance Triggering
- User action (e.g. Leave Application, Hostel Application, Enrollment Cancellation) triggers workflow.
- `WorkflowEngineService.startWorkflow(definitionKey, contextData)` initializes instance in `workflow_instances`.
- State machine evaluates first step.
- Resolves actor role using department/institute scope (e.g. "HOD of applicant's department").
- Creates task in `workflow_tasks` with status `PENDING`.

### 2. Task Execution (Inbox Action)
- Approver logs in, opens `MyTasksPage.tsx`.
- Reviews request context and attached documents.
- Action:
  - **Approve**: `POST /api/workflow/tasks/:id/act { action: 'APPROVE', comments: 'Approved' }` -> advances state machine.
  - **Reject**: `POST /api/workflow/tasks/:id/act { action: 'REJECT', comments: 'Reason' }` -> terminates instance with status `REJECTED`.
  - **Delegate**: `POST /api/workflow/tasks/:id/act { action: 'DELEGATE', targetUserId }` -> reassigns task.

---

## Action 6.3: Saga Resource Hold & Timeout Expiration

### 1. Temporary Resource Hold
- Workflow steps requiring limited resources (e.g. hostel room, event auditorium) acquire a soft reservation hold via `ReservationService.acquireHold(resourceId, ttlMinutes: 30)`.
- Prevents double-booking while user completes prerequisite steps (such as payment gate).

### 2. Payment Gate Completion
- User receives payment task -> initiates Razorpay checkout via `POST /api/workflow/tasks/:id/payment/order`.
- Payment verified -> `POST /api/workflow/tasks/:id/payment/verify` -> hold converted to permanent allocation.

### 3. Automated Expiry & Compensating Action
- If user fails to pay within TTL:
  - Background scheduler (`WorkflowSchedulerService`) detects expired hold.
  - Releases soft reservation (`ReservationService.releaseHold`).
  - Cancels workflow instance with status `EXPIRED`.
  - Admin can manually trigger expiry check via `POST /api/workflow/admin/run-expiry`.
