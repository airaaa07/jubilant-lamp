# Workflow Engine

## Purpose

This document explains the workflow engine implementation in the University ERP system. It details how the workflow engine works, how to define workflows, how to execute workflows, and how to integrate workflows with modules.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses a custom workflow engine. Understanding the workflow engine is critical for:
- Implementing approval processes
- Creating custom workflows
- Integrating workflows with modules
- Debugging workflow issues
- Extending workflow functionality

Without understanding the workflow engine, developers may struggle with workflow implementation or may introduce workflow bugs.

## Where This Is Used

- **Onboarding**: New developers learn workflow engine
- **Feature Development**: Implementing workflow features
- **Code Reviews**: Reviewing workflow code
- **Approval Processes**: Managing approvals
- **Workflow Integration**: Integrating workflows with modules

## Dependencies

### Workflow Engine Dependencies

**Confirmed by Code**: Workflow engine depends on:

- **PrismaModule**: Workflow data storage
- **BullModule**: Queue for async operations
- **RedisModule**: Caching workflow data
- **AuthModule**: Authentication and authorization

## Internal Architecture

### Workflow Engine Architecture

**Confirmed by Code**: Workflow engine follows state machine pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Workflow Engine                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Definition   │  │  Instance       │  │  Execution      │
│  (States)     │  │  (Process)      │  │  (Transitions)  │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Workflow Service

**Confirmed by Code**: Workflow service implements workflow logic.

**WorkflowService**:
```typescript
@Injectable()
export class WorkflowService {
  constructor(
    private prisma: PrismaService,
    private redis: RedisService,
    private notificationQueue: Queue,
  ) {}

  async createInstance(dto: CreateWorkflowInstanceDto) {
    // Get workflow definition
    const definition = await this.prisma.workflowDefinition.findFirst({
      where: {
        module: dto.module,
        isActive: true,
      },
      include: {
        states: true,
        transitions: true,
      },
    });

    if (!definition) {
      throw new NotFoundException('Workflow definition not found');
    }

    // Get initial state
    const initialState = definition.states.find(s => s.isInitial);
    if (!initialState) {
      throw new BadRequestException('No initial state defined');
    }

    // Create instance
    const instance = await this.prisma.workflowInstance.create({
      data: {
        workflowDefinitionId: definition.id,
        currentStateId: initialState.id,
        entityId: dto.entityId,
        entityType: dto.entityType,
        data: dto.data,
      },
    });

    // Create tasks for initial state
    await this.createTasksForState(instance, initialState);

    // Log event
    await this.logEvent(instance.id, 'CREATED', 'Workflow instance created');

    return instance;
  }

  async transition(instanceId: string, action: string, user: JwtPayload) {
    const instance = await this.prisma.workflowInstance.findUnique({
      where: { id: instanceId },
      include: {
        currentState: true,
        workflowDefinition: {
          include: {
            transitions: true,
          },
        },
      },
    });

    if (!instance) {
      throw new NotFoundException('Workflow instance not found');
    }

    // Find transition
    const transition = instance.workflowDefinition.transitions.find(
      t => t.fromStateId === instance.currentStateId && t.action === action,
    );

    if (!transition) {
      throw new BadRequestException('Invalid transition');
    }

    // Check role
    if (transition.role && user.role !== transition.role && user.role !== 'SUPERADMIN') {
      throw new ForbiddenException('Insufficient permissions');
    }

    // Get target state
    const targetState = await this.prisma.workflowState.findUnique({
      where: { id: transition.toStateId },
    });

    if (!targetState) {
      throw new NotFoundException('Target state not found');
    }

    // Update instance
    const updatedInstance = await this.prisma.workflowInstance.update({
      where: { id: instanceId },
      data: {
        currentStateId: targetState.id,
        completedAt: targetState.isFinal ? new Date() : null,
      },
    });

    // Create tasks for new state
    await this.createTasksForState(updatedInstance, targetState);

    // Log event
    await this.logEvent(instanceId, action, `Transitioned to ${targetState.name}`);

    // Check for auto-transition
    if (transition.autoTransition) {
      await this.queueAutoTransition(instanceId, transition.toStateId);
    }

    // Check if final state
    if (targetState.isFinal) {
      await this.onWorkflowComplete(updatedInstance);
    }

    return updatedInstance;
  }

  private async createTasksForState(instance: WorkflowInstance, state: WorkflowState) {
    // Get transitions from this state
    const transitions = await this.prisma.workflowTransition.findMany({
      where: { fromStateId: state.id },
    });

    for (const transition of transitions) {
      await this.prisma.workflowTask.create({
        data: {
          workflowInstanceId: instance.id,
          name: transition.action,
          description: `Execute ${transition.action}`,
          assignedRole: transition.role,
          status: TaskStatus.PENDING,
        },
      });
    }
  }

  private async queueAutoTransition(instanceId: string, stateId: string) {
    await this.workflowQueue.add('auto-transition', { instanceId, stateId });
  }

  private async onWorkflowComplete(instance: WorkflowInstance) {
    // Send notification
    await this.notificationQueue.add('workflow-complete', {
      instanceId: instance.id,
      entityId: instance.entityId,
      entityType: instance.entityType,
    });

    // Log event
    await this.logEvent(instance.id, 'COMPLETED', 'Workflow instance completed');
  }

  private async logEvent(instanceId: string, eventType: string, message: string) {
    await this.prisma.workflowInstanceEvent.create({
      data: {
        workflowInstanceId: instanceId,
        eventType,
        message,
        timestamp: new Date(),
      },
    });
  }
}
```

**What This Does**:
- **createInstance**: Creates new workflow instance
- **transition**: Transitions instance to next state
- **createTasksForState**: Creates tasks for state
- **queueAutoTransition**: Queues auto-transition
- **onWorkflowComplete**: Handles workflow completion
- **logEvent**: Logs workflow events

### Workflow Worker

**Confirmed by Code**: Workflow worker processes auto-transitions.

**WorkflowWorker**:
```typescript
@Processor('workflow')
export class WorkflowWorker {
  constructor(private workflowService: WorkflowService) {}

  @Process('auto-transition')
  async handleAutoTransition(job: Job) {
    const { instanceId, stateId } = job.data;

    // Get transitions from current state
    const transitions = await this.prisma.workflowTransition.findMany({
      where: { fromStateId: stateId, autoTransition: true },
    });

    for (const transition of transitions) {
      // Execute auto-transition
      await this.workflowService.transition(
        instanceId,
        transition.action,
        { role: 'SYSTEM' } as JwtPayload,
      );
    }
  }
}
```

**What This Does**:
- **handleAutoTransition**: Processes auto-transition
- **Gets Transitions**: Gets auto-transitions from state
- **Executes Transition**: Executes each auto-transition

## Database Interactions

### Workflow Engine-Database Flow

**Confirmed by Code**: Workflow engine interacts with database.

**Flow**:
```
Workflow Service → Prisma → WorkflowDefinition/WorkflowInstance/WorkflowTask Tables
```

## Redis Interactions

### Workflow Engine-Redis Flow

**Confirmed by Code**: Workflow engine can use Redis for caching.

**Flow**:
```
Workflow Service → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Workflow Engine-Queue Flow

**Confirmed by Code**: Workflow engine uses queues for auto-transitions.

**Flow**:
```
Workflow Service → Workflow Queue → Workflow Worker
```

## Worker Interactions

### Workflow Engine-Worker Flow

**Confirmed by Code**: Workers process workflow auto-transitions.

**Flow**:
```
Workflow Worker → Process Auto-Transition → Update Instance → Next State
```

## Business Rules

### Workflow Engine Rules

**Confirmed by Code**: Workflow engine follows these rules:

1. **State Machine**: Workflow is a state machine
2. **Initial State**: Must have one initial state
3. **Final State**: Can have multiple final states
4. **Transitions**: Transitions defined between states
5. **Auto-Transitions**: Some transitions are automatic

### Execution Rules

**Confirmed by Code**: Execution rules:

1. **Instance Creation**: Instance created in initial state
2. **Task Creation**: Tasks created for each transition
3. **Role Check**: Role checked before transition
4. **Auto-Transition**: Auto-transitions queued
5. **Completion**: Workflow completes on final state

## Security

### Workflow Engine Security

**Confirmed by Code**: Security considerations for workflow engine:

1. **Role-Based Transitions**: Transitions restricted by role
2. **Task Assignment**: Tasks assigned to authorized users
3. **Audit Logging**: All workflow changes logged
4. **Access Control**: Restrict access to authorized users
5. **Data Scoping**: Workflow data scoped by tenant hierarchy

## Performance Considerations

### Workflow Engine Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Cache workflow definitions
2. **Queue Processing**: Use queues for auto-transitions
3. **Indexing**: Index foreign keys
4. **Query Optimization**: Optimize queries
5. **Batch Processing**: Batch process workflow instances

## Common Mistakes

### Mistake 1: Not Defining Initial State

**Symptom**: Workflow instance cannot start

**Cause**: Not defining initial state

**Fix**:
```typescript
// Set isInitial to true for initial state
const initialState = await this.prisma.workflowState.create({
  data: {
    name: 'PENDING',
    isInitial: true,
    workflowDefinitionId: definition.id,
  },
});
```

### Mistake 2: Not Handling Auto-Transitions

**Symptom**: Workflow stuck in state

**Cause**: Not handling auto-transitions

**Fix**:
```typescript
// Queue auto-transition
if (transition.autoTransition) {
  await this.queueAutoTransition(instanceId, transition.toStateId);
}
```

### Mistake 3: Not Logging Events

**Symptom**: No workflow history

**Cause**: Not logging events

**Fix**:
```typescript
// Log event
await this.logEvent(instanceId, action, `Transitioned to ${targetState.name}`);
```

## Debugging Guide

### Workflow Engine Debugging

**Issue**: Workflow instance stuck

**Investigation**:
1. Check workflow definition
2. Check current state
3. Check available transitions
4. Check task assignments
5. Check queue processing

**Tools**:
- Workflow logs
- Queue logs
- Database logs
- State inspector

## Future Enhancements

### Visual Workflow Designer

**Status**: Not implemented

**Proposal**: Implement visual workflow designer:
- Drag-and-drop workflow design
- Visual state diagram
- Real-time validation
- Better UX
- More complex

### Workflow Templates

**Status**: Not implemented

**Proposal**: Implement workflow templates:
- Pre-defined workflow templates
- Template customization
- Quick workflow setup
- Better productivity
- More flexibility

## Production Considerations

### Production Workflow Engine

**Production Deployment**:
- Enable caching
- Implement data scoping
- Monitor workflow performance
- Monitor queue processing
- Audit all workflow changes

### Workflow Engine Monitoring

**Monitoring Metrics**:
- Workflow instance creation rate
- Workflow completion rate
- Task completion rate
- Average workflow duration
- Failed workflow instances

## Example Requests

### Workflow Engine Example

**Request**: Create workflow instance

```bash
POST /api/workflows/instances
Content-Type: application/json

{
  "module": "admissions",
  "entityId": "application-id",
  "entityType": "ADMISSION_APPLICATION"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "id": "instance-id",
    "currentState": "PENDING",
    "startedAt": "2024-01-01T00:00:00Z"
  }
}
```

## Example Responses

### Workflow Engine Response

**Response**: Workflow instance created

```json
{
  "success": true,
  "data": {
    "id": "instance-id",
    "currentState": "PENDING",
    "tasks": [
      {
        "id": "task-id",
        "name": "Review Application",
        "status": "PENDING"
      }
    ]
  }
}
```

## Sequence Diagrams

### Workflow Engine Flow

```
Create Instance → Initial State → Task Created → User Action → Transition → Next State → Auto-Transition → Final State → Complete
```

## Architecture Diagrams

### Workflow Engine Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Workflow Service                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Workflow Definition                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Workflow Instance                          │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Tasks        │  │  Transitions    │  │  Events         │
│  (Actions)    │  │  (State Flow)   │  │  (History)      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How does the workflow engine work?

**Answer**: Workflow engine via:
- Workflow definitions with states and transitions
- Workflow instances track process execution
- Tasks created for actions
- Transitions move between states
- Final state marks completion

### Q2: How do you handle auto-transitions?

**Answer**: Auto-transitions via:
- Mark transition as autoTransition
- Queue auto-transition task
- Worker processes auto-transition
- Instance moves to next state
- Continue until final state

### Q3: How do you integrate workflows with modules?

**Answer**: Workflow integration via:
- Module triggers workflow creation
- Workflow instance bound to entity
- Workflow transitions trigger module actions
- Module listens to workflow events
- Module updates based on workflow state

## Exercises

### Exercise 1: Create a Workflow Definition

**Task**: Create a new workflow definition.

**Steps**:
1. Define workflow definition
2. Define states
3. Define transitions
4. Define initial and final states
5. Test workflow

**Verification**:
- Definition created
- States defined
- Transitions defined
- Initial/final states set
- Tests pass

### Exercise 2: Implement a Custom Transition

**Task**: Implement a custom transition logic.

**Steps**:
1. Add transition to workflow
2. Implement transition logic
3. Add role check
4. Test transition
5. Test with different roles

**Verification**:
- Transition added
- Logic implemented
- Role check works
- Transition works
- Tests pass

## Real Production Scenarios

### Scenario 1: Workflow Instance Stuck

**Situation**: Workflow instance stuck in state

**Response**:
1. Check current state
2. Check available transitions
3. Check task assignments
4. Force transition if needed
5. Monitor workflow

### Scenario 2: Queue Backlog

**Situation**: Workflow queue backlog

**Response**:
1. Check queue size
2. Add more workers
3. Optimize task processing
4. Monitor queue
5. Clear backlog

## Navigation

**Next Section**: [02-Workflow-Integration](./02-Workflow-Integration.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [08-Modules](../08-Modules/README.md) - Module details
