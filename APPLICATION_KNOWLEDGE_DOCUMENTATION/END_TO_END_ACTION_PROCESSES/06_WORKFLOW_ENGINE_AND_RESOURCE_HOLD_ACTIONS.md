# Action Lifecycle Manual: Visual Workflow Engine & Saga Holds

## Action 6.1: Multi-Actor Workflow Inbox Approval Action

### 1. User Action & Frontend Trigger
- **User Role**: Department HOD (`role: HOD`)
- **Screen**: `MyTasksPage.tsx`
- **User Input**: Selects pending approval item `TASK-8802` (Student Course Exemption Request), enters review comment (`"Prerequisites met in previous semester, approved."`).
- **Trigger**: Click **Approve & Advance Step** button.

### 2. Frontend Payload
- `POST /api/v1/workflow/instances/inst-8802/action`
- Payload:
  ```json
  {
    "stepInstanceId": "step-8802-1",
    "action": "APPROVE",
    "comments": "Prerequisites met in previous semester, approved."
  }
  ```

### 3. Backend Workflow Engine Logic (`WorkflowEngineService.processAction`)
- Verifies `req.user` matches assigned actor role (`HOD`) for step.
- Updates current step instance status to `APPROVED`.
- Evaluates transition rules in `WorkflowDefinition` graph:
  - Next state: `DEAN_APPROVAL_REQUIRED`.
  - Resolves next actor role (`Dean`).

### 4. Database Mutations (Atomic Transaction)
- `UPDATE workflow_step_instances SET status = 'APPROVED', comments = :comments, completed_at = NOW() WHERE id = 'step-8802-1'`
- `INSERT INTO workflow_step_instances (instance_id, state_id, assigned_role = 'Dean', status = 'PENDING')`
- `UPDATE workflow_instances SET current_state = 'AWAITING_DEAN_APPROVAL'`

### 5. Side Effects & Outcome
- Removes task from HOD's `MyTasksPage.tsx` inbox.
- Inserts new pending task into Dean's `MyTasksPage.tsx` inbox.
- Dispatches notification email to Dean.

---

## Action 6.2: Midnight Saga Hold Expiration Cron Execution

### 1. Trigger & Execution
- **Initiator**: NestJS Cron Scheduler (`@Cron('0 0 * * *')`)
- **Service**: `WorkflowSchedulerService.expirePaymentDemands`
- **Execution Time**: Daily Midnight (00:00)

### 2. Backend Logic
- Scans `workflow_holds` for active resource reservations (`status == 'ACTIVE'`) where `expires_at < NOW()`.
- Executes Saga compensating actions:
  - Releases soft reservation hold on facility/room (`ResourceReservationService.releaseHold`).
  - Cancels associated fee demand (`FeeService.cancelDemand`).
  - Marks workflow instance `EXPIRED`.

### 3. Database Mutations
- `UPDATE workflow_holds SET status = 'EXPIRED' WHERE expires_at < NOW() AND status = 'ACTIVE'`
- `UPDATE workflow_instances SET status = 'EXPIRED' WHERE id IN (...)`
- `UPDATE fee_demands SET status = 'CANCELLED' WHERE id IN (...)`
