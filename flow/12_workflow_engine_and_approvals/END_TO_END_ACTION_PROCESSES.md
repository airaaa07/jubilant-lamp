# Module 12: Visual Workflow Engine & Approvals — End-to-End Action Processes

> **Scope**: Backend state execution pipelines, task resolution, transition rule checks, saga reservation holds, aging timeouts, and notification dispatches.

---

## Action 1: Execute Workflow Task Action (`POST /api/workflow/tasks/:id/act`)

- **HTTP Method & URL**: `POST /api/workflow/tasks/:id/act`
- **Guards**: `JwtAuthGuard`
- **Request Body (DTO: `ActOnTaskDto`)**:
  ```json
  {
    "action": "APPROVE",
    "remarks": "Verified against physical grade ledger.",
    "reassignToUserId": null
  }
  ```
- **Backend Flow**:
  1. Validates caller holds role assigned to task's current state, or is explicitly named `assigneeId`.
  2. Evaluates outgoing `WorkflowTransition` for target state where `transition.action == dto.action`.
  3. Executes atomic Prisma transaction:
     - Updates current `WorkflowTask.status = 'COMPLETED'`.
     - Advances `WorkflowInstance.currentStateId = transition.toStateId`.
     - Records `WorkflowInstanceEvent` (Audit trail with user ID, timestamps, remarks).
     - If `toState` requires next approval: creates new `WorkflowTask` for next actor role.
     - If `toState` is terminal (`isTerminal: true`): marks instance `COMPLETED` and commits saga holds.
- **Prisma Database Mutation**:
  ```prisma
  await prisma.$transaction(async (tx) => {
    const task = await tx.workflowTask.findUnique({
      where: { id },
      include: { workflowInstance: { include: { workflowDefinition: true } } }
    });

    const transition = await tx.workflowTransition.findFirst({
      where: {
        fromStateId: task.workflowInstance.currentStateId,
        action: dto.action
      },
      include: { toState: true }
    });

    await tx.workflowTask.update({
      where: { id },
      data: {
        status: "COMPLETED",
        completedAt: new Date(),
        completedById: req.user.id,
        remarks: dto.remarks
      }
    });

    await tx.workflowInstance.update({
      where: { id: task.workflowInstanceId },
      data: {
        currentStateId: transition.toStateId,
        status: transition.toState.isTerminal ? "COMPLETED" : "IN_PROGRESS"
      }
    });

    await tx.workflowInstanceEvent.create({
      data: {
        workflowInstanceId: task.workflowInstanceId,
        actorId: req.user.id,
        fromStateId: transition.fromStateId,
        toStateId: transition.toStateId,
        action: dto.action,
        remarks: dto.remarks
      }
    });
  });
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "nextState": "TRANSCRIPT_FEE_PAYMENT",
    "instanceStatus": "IN_PROGRESS"
  }
  ```

---

## Action 2: Automatic SLA Expiration Cron (`POST /api/workflow/admin/run-expiry`)

- **Backend Flow**:
  1. Queries all `WorkflowTask` rows where `status == 'PENDING'` and `slaExpiresAt < now()`.
  2. For each task, checks state's timeout configuration (`timeoutAction: 'ESCALATE'` or `'AUTO_REJECT'`).
  3. If Escalate: reassigns task to department `HOD` or `SuperAdmin`.
  4. Dispatches SLA breach email alerts to supervising administrators.
- **Response (200 OK)**: `{ "processedCount": 4, "escalatedCount": 4 }`
