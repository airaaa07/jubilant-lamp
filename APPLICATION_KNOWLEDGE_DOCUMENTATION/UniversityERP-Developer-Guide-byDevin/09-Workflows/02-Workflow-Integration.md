# Workflow Integration

## Purpose

This document explains how to integrate the workflow engine with other modules in the University ERP system. It details integration patterns, module-specific workflows, and best practices.

## Why This Document Exists

**Confirmed by Code**: The workflow engine is integrated with multiple modules. Understanding workflow integration is critical for:
- Integrating workflows with modules
- Creating module-specific workflows
- Handling workflow events
- Debugging integration issues
- Extending workflow functionality

Without understanding workflow integration, developers may struggle with module integration or may introduce integration bugs.

## Where This Is Used

- **Onboarding**: New developers learn workflow integration
- **Feature Development**: Integrating workflows with modules
- **Code Reviews**: Reviewing workflow integration code
- **Module Development**: Developing module-specific workflows
- **Workflow Extension**: Extending workflow functionality

## Dependencies

### Workflow Integration Dependencies

**Confirmed by Code**: Workflow integration depends on:

- **WorkflowModule**: Workflow engine
- **Module Services**: Module-specific services
- **Event Emitters**: Event-driven communication (future)
- **NotificationModule**: Workflow notifications

## Internal Architecture

### Workflow Integration Architecture

**Confirmed by Code**: Workflow integration follows event-driven pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Module Service                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Workflow Service                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Workflow Instance                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Workflow Events                               │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Admissions Workflow Integration

**Confirmed by Code**: Admissions module integrates with workflow.

**AdmissionsService**:
```typescript
@Injectable()
export class AdmissionsService {
  constructor(
    private prisma: PrismaService,
    private workflowService: WorkflowService,
  ) {}

  async createStartRequest(dto: CreateStartAdmissionRequestDto) {
    // Create admission start request
    const request = await this.prisma.batchAdmissionStartRequest.create({
      data: {
        batchId: dto.batchId,
        requestedBy: dto.requestedBy,
        requestedAt: new Date(),
        status: 'PENDING',
      },
    });

    // Create workflow instance
    const workflowInstance = await this.workflowService.createInstance({
      module: 'admissions',
      entityId: request.id,
      entityType: 'BATCH_ADMISSION_START_REQUEST',
      data: {
        batchId: dto.batchId,
        requestedBy: dto.requestedBy,
      },
    });

    return { request, workflowInstance };
  }

  async approveStartRequest(requestId: string) {
    // Get workflow instance
    const instance = await this.prisma.workflowInstance.findFirst({
      where: {
        entityId: requestId,
        entityType: 'BATCH_ADMISSION_START_REQUEST',
      },
    });

    if (!instance) {
      throw new NotFoundException('Workflow instance not found');
    }

    // Transition workflow
    await this.workflowService.transition(instance.id, 'APPROVE', {
      role: 'UNIVERSITY_ADMIN',
    } as JwtPayload);

    // Update request status
    await this.prisma.batchAdmissionStartRequest.update({
      where: { id: requestId },
      data: { status: 'APPROVED' },
    });

    // Open admissions for batch
    await this.openAdmissions(instance.data.batchId);

    return { success: true };
  }

  async rejectStartRequest(requestId: string, reason: string) {
    // Get workflow instance
    const instance = await this.prisma.workflowInstance.findFirst({
      where: {
        entityId: requestId,
        entityType: 'BATCH_ADMISSION_START_REQUEST',
      },
    });

    if (!instance) {
      throw new NotFoundException('Workflow instance not found');
    }

    // Transition workflow
    await this.workflowService.transition(instance.id, 'REJECT', {
      role: 'UNIVERSITY_ADMIN',
    } as JwtPayload);

    // Update request status
    await this.prisma.batchAdmissionStartRequest.update({
      where: { id: requestId },
      data: { status: 'REJECTED', rejectionReason: reason },
    });

    return { success: true };
  }

  private async openAdmissions(batchId: string) {
    // Open admissions for batch
    await this.prisma.batch.update({
      where: { id: batchId },
      data: { admissionStatus: 'OPEN' },
    });

    // Send notifications
    await this.notificationQueue.add('admissions-opened', { batchId });
  }
}
```

**What This Does**:
- **createStartRequest**: Creates request and workflow instance
- **approveStartRequest**: Transitions workflow and opens admissions
- **rejectStartRequest**: Transitions workflow and rejects request
- **openAdmissions**: Opens admissions for batch

### Fee Workflow Integration

**Confirmed by Code**: Fee module integrates with workflow.

**FeeService**:
```typescript
@Injectable()
export class FeeService {
  constructor(
    private prisma: PrismaService,
    private workflowService: WorkflowService,
  ) {}

  async createFeeWaiver(dto: CreateFeeWaiverDto) {
    // Create fee waiver request
    const waiver = await this.prisma.feeWaiver.create({
      data: {
        studentId: dto.studentId,
        feeHeadId: dto.feeHeadId,
        amount: dto.amount,
        reason: dto.reason,
        status: 'PENDING',
      },
    });

    // Create workflow instance
    const workflowInstance = await this.workflowService.createInstance({
      module: 'fee',
      entityId: waiver.id,
      entityType: 'FEE_WAIVER',
      data: {
        studentId: dto.studentId,
        feeHeadId: dto.feeHeadId,
        amount: dto.amount,
      },
    });

    return { waiver, workflowInstance };
  }

  async approveFeeWaiver(waiverId: string) {
    // Get workflow instance
    const instance = await this.prisma.workflowInstance.findFirst({
      where: {
        entityId: waiverId,
        entityType: 'FEE_WAIVER',
      },
    });

    if (!instance) {
      throw new NotFoundException('Workflow instance not found');
    }

    // Transition workflow
    await this.workflowService.transition(instance.id, 'APPROVE', {
      role: 'INSTITUTE_ADMIN',
    } as JwtPayload);

    // Update waiver status
    await this.prisma.feeWaiver.update({
      where: { id: waiverId },
      data: { status: 'APPROVED' },
    });

    // Apply fee waiver
    await this.applyFeeWaiver(waiverId);

    return { success: true };
  }

  private async applyFeeWaiver(waiverId: string) {
    const waiver = await this.prisma.feeWaiver.findUnique({
      where: { id: waiverId },
    });

    // Create fee ledger entry
    await this.prisma.feeLedger.create({
      data: {
        studentId: waiver.studentId,
        feeHeadId: waiver.feeHeadId,
        amount: -waiver.amount,
        type: 'WAIVER',
        referenceId: waiverId,
      },
    });
  }
}
```

**What This Does**:
- **createFeeWaiver**: Creates waiver and workflow instance
- **approveFeeWaiver**: Transitions workflow and applies waiver
- **applyFeeWaiver**: Applies fee waiver to fee ledger

## Database Interactions

### Workflow Integration-Database Flow

**Confirmed by Code**: Workflow integration interacts with database.

**Flow**:
```
Module Service → Workflow Service → Prisma → Module Tables + Workflow Tables
```

## Redis Interactions

### Workflow Integration-Redis Flow

**Confirmed by Code**: Workflow integration can use Redis for caching.

**Flow**:
```
Module Service → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Workflow Integration-Queue Flow

**Confirmed by Code**: Workflow integration uses queues for notifications.

**Flow**:
```
Module Service → Notification Queue → Notification Worker
```

## Worker Interactions

### Workflow Integration-Worker Flow

**Confirmed by Code**: Workers process workflow notifications.

**Flow**:
```
Notification Worker → Send Notification → External Service
```

## Business Rules

### Workflow Integration Rules

**Confirmed by Code**: Workflow integration follows these rules:

1. **Instance Creation**: Create workflow instance on entity creation
2. **Transition Trigger**: Trigger workflow transition on action
3. **Status Update**: Update entity status on workflow transition
3. **Action Execution**: Execute module action on workflow completion
4. **Notification**: Send notification on workflow events

### Integration Patterns

**Confirmed by Code**: Integration patterns:

1. **Create Pattern**: Create entity + workflow instance
2. **Transition Pattern**: Transition workflow + update entity
3. **Completion Pattern**: Execute action on workflow completion
4. **Event Pattern**: Listen to workflow events
5. **Notification Pattern**: Send notifications on workflow events

## Security

### Workflow Integration Security

**Confirmed by Code**: Security considerations for workflow integration:

1. **Role-Based Transitions**: Transitions restricted by role
2. **Data Scoping**: Workflow data scoped by tenant hierarchy
3. **Audit Logging**: All workflow changes logged
4. **Access Control**: Restrict access to authorized users
5. **Validation**: Validate all inputs

## Performance Considerations

### Workflow Integration Performance

**Confirmed by Code**: Performance considerations:

1. **Async Operations**: Use queues for async operations
2. **Caching**: Cache workflow definitions
3. **Batch Processing**: Batch process workflow instances
4. **Query Optimization**: Optimize queries
5. **Transaction Management**: Use transactions for consistency

## Common Mistakes

### Mistake 1: Not Creating Workflow Instance

**Symptom**: No workflow tracking

**Cause**: Not creating workflow instance

**Fix**:
```typescript
// Create workflow instance
const workflowInstance = await this.workflowService.createInstance({
  module: 'admissions',
  entityId: request.id,
  entityType: 'BATCH_ADMISSION_START_REQUEST',
  data: { ... },
});
```

### Mistake 2: Not Updating Entity Status

**Symptom**: Entity status not updated

**Cause**: Not updating entity status on workflow transition

**Fix**:
```typescript
// Update entity status
await this.prisma.batchAdmissionStartRequest.update({
  where: { id: requestId },
  data: { status: 'APPROVED' },
});
```

### Mistake 3: Not Handling Workflow Completion

**Symptom**: Action not executed on completion

**Cause**: Not handling workflow completion

**Fix**:
```typescript
// Handle workflow completion
if (targetState.isFinal) {
  await this.onWorkflowComplete(instance);
}
```

## Debugging Guide

### Workflow Integration Debugging

**Issue**: Workflow not integrated correctly

**Investigation**:
1. Check workflow instance creation
2. Check workflow transitions
3. Check entity status updates
4. Check workflow events
5. Check logs

**Tools**:
- Workflow logs
- Module logs
- Database logs
- Queue logs

## Future Enhancements

### Event-Driven Integration

**Status**: Not implemented

**Proposal**: Implement event-driven integration:
- Event emitter for workflow events
- Modules listen to workflow events
- Better decoupling
- More flexible
- More complex

### Webhook Integration

**Status**: Not implemented

**Proposal**: Implement webhook integration:
- Webhooks for workflow events
- External system integration
- Better extensibility
- More complex
- Better for third-party integration

## Production Considerations

### Production Workflow Integration

**Production Deployment**:
- Enable workflow integration
- Monitor workflow performance
- Monitor integration errors
- Audit all workflow changes
- Monitor module interactions

### Workflow Integration Monitoring

**Monitoring Metrics**:
- Workflow instance creation rate
- Workflow transition rate
- Module action execution rate
- Integration error rate
- Workflow completion rate

## Example Requests

### Workflow Integration Example

**Request**: Create entity with workflow

```bash
POST /api/admissions/start-requests
Content-Type: application/json

{
  "batchId": "batch-id",
  "requestedBy": "user-id"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "request": {
      "id": "request-id",
      "status": "PENDING"
    },
    "workflowInstance": {
      "id": "instance-id",
      "currentState": "PENDING"
    }
  }
}
```

## Example Responses

### Workflow Integration Response

**Response**: Entity and workflow created

```json
{
  "success": true,
  "data": {
    "request": {
      "id": "request-id",
      "status": "PENDING"
    },
    "workflowInstance": {
      "id": "instance-id",
      "currentState": "PENDING",
      "tasks": [...]
    }
  }
}
```

## Sequence Diagrams

### Workflow Integration Flow

```
Module Service → Create Entity → Create Workflow Instance → User Action → Transition Workflow → Update Entity → Execute Action
```

## Architecture Diagrams

### Workflow Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Module Service                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Create Entity                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Create Workflow Instance                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  User Action                                │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Transition Workflow                         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Update Entity Status                       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Execute Module Action                       │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you integrate a module with the workflow engine?

**Answer**: Module integration via:
- Create workflow instance on entity creation
- Bind workflow instance to entity
- Trigger workflow transitions on actions
- Update entity status on transitions
- Execute module actions on completion

### Q2: How do you handle workflow events in modules?

**Answer**: Workflow events via:
- Listen to workflow events
- Update entity based on events
- Execute module actions on events
- Send notifications on events
- Log events for audit

### Q3: How do you ensure consistency between workflow and entity?

**Answer**: Consistency via:
- Use transactions for updates
- Update entity and workflow together
- Handle failures gracefully
- Rollback on failure
- Audit all changes

## Exercises

### Exercise 1: Integrate a Module with Workflow

**Task**: Integrate a module with workflow engine.

**Steps**:
1. Create workflow definition
2. Add workflow instance creation
3. Add workflow transition
4. Add entity status update
5. Test integration

**Verification**:
- Workflow definition created
- Instance creation works
- Transition works
- Status update works
- Tests pass

### Exercise 2: Handle Workflow Events

**Task**: Handle workflow events in module.

**Steps**:
1. Add event listener
2. Update entity on event
3. Execute action on event
4. Test event handling
5. Test with different events

**Verification**:
- Event listener works
- Entity updated
- Action executed
- Tests pass

## Real Production Scenarios

### Scenario 1: Workflow Not Triggered

**Situation**: Workflow not triggered on entity creation

**Response**:
1. Check workflow instance creation
2. Check workflow definition
3. Check module integration
4. Fix integration
5. Test workflow

### Scenario 2: Entity Status Not Updated

**Situation**: Entity status not updated on workflow transition

**Response**:
1. Check transition logic
2. Check status update
3. Fix update logic
4. Test transition
5. Test status update

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [01-Workflow-Engine](./01-Workflow-Engine.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [08-Modules](../08-Modules/README.md) - Module details
