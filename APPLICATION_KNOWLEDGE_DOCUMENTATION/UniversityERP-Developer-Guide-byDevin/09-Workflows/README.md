# 09-Workflows

## Purpose

This folder provides comprehensive documentation about the workflow engine of the University ERP system. It details how workflows are defined, executed, managed, and integrated with other modules.

## Why This Folder Exists

**Confirmed by Code**: The University ERP uses a workflow engine for approval processes. Understanding the workflow engine is critical for:
- Implementing approval workflows
- Managing workflow states
- Integrating workflows with modules
- Debugging workflow issues
- Creating custom workflows

Without understanding the workflow engine, developers may struggle with approval processes or may introduce workflow bugs.

## Where This Is Used

- **Onboarding**: New developers learn workflow engine
- **Feature Development**: Implementing workflow features
- **Code Reviews**: Reviewing workflow code
- **Approval Processes**: Managing approvals
- **Workflow Integration**: Integrating workflows with modules

## Dependencies

### Workflow Dependencies

**Confirmed by Code**: Workflow engine depends on:

- **PrismaModule**: Workflow data storage
- **BullModule**: Queue for async operations
- **AuthModule**: Authentication and authorization
- **RedisModule**: Caching workflow data

## Internal Architecture

### Workflow Architecture

**Confirmed by Code**: Workflow engine follows state machine pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Workflow Engine                               │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Definition   │  │  Instance       │  │  Transition     │
│  (States)     │  │  (Process)      │  │  (Flow)         │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Task         │  │  Reservation    │  │  Event         │
│  (Actions)    │  │  (Resources)    │  │  (History)      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Workflow Definition

**Confirmed by Code**: Workflow definitions stored in database.

**WorkflowDefinition Model**:
```prisma
model WorkflowDefinition {
  id          String                @id @default(cuid())
  name        String
  description String?
  module      String
  version     Int
  isActive    Boolean               @default(true)
  states      WorkflowState[]
  transitions WorkflowTransition[]
  instances   WorkflowInstance[]
  createdAt   DateTime              @default(now())
  updatedAt   DateTime              @updatedAt

  @@unique([module, version])
  @@index([module])
  @@index([isActive])
}
```

**What This Does**:
- **name**: Workflow name
- **module**: Module this workflow belongs to
- **version**: Workflow version
- **isActive**: Whether workflow is active
- **states**: Workflow states
- **transitions**: State transitions

### Workflow State

**Confirmed by Code**: Workflow states defined per workflow.

**WorkflowState Model**:
```prisma
model WorkflowState {
  id                   String                @id @default(cuid())
  workflowDefinitionId String
  name                 String
  description          String?
  isInitial            Boolean               @default(false)
  isFinal              Boolean               @default(false)
  transitionsFrom      WorkflowTransition[]  @relation("FromState")
  transitionsTo        WorkflowTransition[]  @relation("ToState")
  workflowDefinition   WorkflowDefinition    @relation(fields: [workflowDefinitionId], references: [id])

  @@unique([workflowDefinitionId, name])
  @@index([workflowDefinitionId])
}
```

**What This Does**:
- **name**: State name
- **isInitial**: Whether this is initial state
- **isFinal**: Whether this is final state
- **transitionsFrom**: Transitions from this state
- **transitionsTo**: Transitions to this state

### Workflow Transition

**Confirmed by Code**: Workflow transitions defined between states.

**WorkflowTransition Model**:
```prisma
model WorkflowTransition {
  id                   String             @id @default(cuid())
  workflowDefinitionId String
  fromStateId          String
  toStateId            String
  action               String
  role                 UserRole?
  autoTransition       Boolean            @default(false)
  workflowDefinition   WorkflowDefinition @relation(fields: [workflowDefinitionId], references: [id])
  fromState            WorkflowState      @relation("FromState", fields: [fromStateId], references: [id])
  toState              WorkflowState      @relation("ToState", fields: [toStateId], references: [id])

  @@unique([workflowDefinitionId, fromStateId, toStateId])
  @@index([workflowDefinitionId])
  @@index([fromStateId])
  @@index([toStateId])
}
```

**What This Does**:
- **fromStateId**: Source state
- **toStateId**: Target state
- **action**: Action name for transition
- **role**: Role required for transition
- **autoTransition**: Whether transition is automatic

### Workflow Instance

**Confirmed by Code**: Workflow instances track process execution.

**WorkflowInstance Model**:
```prisma
model WorkflowInstance {
  id                   String                @id @default(cuid())
  workflowDefinitionId String
  currentStateId       String
  entityId             String
  entityType           String
  data                 Json?
  startedAt            DateTime              @default(now())
  completedAt          DateTime?
  tasks                WorkflowTask[]
  events               WorkflowInstanceEvent[]
  reservations         WorkflowReservation[]
  currentState         WorkflowState         @relation(fields: [currentStateId], references: [id])
  workflowDefinition   WorkflowDefinition    @relation(fields: [workflowDefinitionId], references: [id])

  @@index([workflowDefinitionId])
  @@index([currentStateId])
  @@index([entityId, entityType])
}
```

**What This Does**:
- **entityId**: ID of entity being processed
- **entityType**: Type of entity being processed
- **currentStateId**: Current state of instance
- **data**: Additional data for instance
- **startedAt**: When instance started
- **completedAt**: When instance completed

### Workflow Task

**Confirmed by Code**: Workflow tasks represent actions to be performed.

**WorkflowTask Model**:
```prisma
model WorkflowTask {
  id                   String             @id @default(cuid())
  workflowInstanceId   String
  name                 String
  description          String?
  assignedTo           String?
  assignedRole         UserRole?
  status               TaskStatus         @default(PENDING)
  completedAt          DateTime?
  data                 Json?
  workflowInstance     WorkflowInstance @relation(fields: [workflowInstanceId], references: [id])

  @@index([workflowInstanceId])
  @@index([assignedTo])
  @@index([status])
}

enum TaskStatus {
  PENDING
  IN_PROGRESS
  COMPLETED
  FAILED
}
```

**What This Does**:
- **name**: Task name
- **assignedTo**: User assigned to task
- **assignedRole**: Role assigned to task
- **status**: Task status
- **data**: Task data

## Database Interactions

### Workflow-Database Flow

**Confirmed by Code**: Workflow engine interacts with database.

**Flow**:
```
Workflow Service → Prisma → WorkflowDefinition/WorkflowInstance/WorkflowTask Tables
```

## Redis Interactions

### Workflow-Redis Flow

**Confirmed by Code**: Workflow engine can use Redis for caching.

**Flow**:
```
Workflow Service → Redis Cache → Database (if cache miss)
```

## Queue Interactions

### Workflow-Queue Flow

**Confirmed by Code**: Workflow engine uses queues for async operations.

**Flow**:
```
Workflow Service → Workflow Queue → Workflow Worker
```

## Worker Interactions

### Workflow-Worker Flow

**Confirmed by Code**: Workers process workflow tasks.

**Flow**:
```
Workflow Worker → Process Task → Update Instance → Notifications
```

## Business Rules

### Workflow Rules

**Confirmed by Code**: Workflow follows these rules:

1. **State Machine**: Workflow is a state machine
2. **Transitions**: Transitions defined between states
3. **Role-Based**: Transitions can be role-based
4. **Auto-Transitions**: Some transitions are automatic
5. **Task Assignment**: Tasks assigned to users or roles

### Instance Rules

**Confirmed by Code**: Instance rules:

1. **Entity Binding**: Instance bound to entity
2. **State Tracking**: Current state tracked
3. **Task Creation**: Tasks created for actions
4. **Event Logging**: All transitions logged
5. **Completion**: Instance marked complete when final state reached

## Security

### Workflow Security

**Confirmed by Code**: Security considerations for workflow:

1. **Role-Based Transitions**: Transitions restricted by role
2. **Task Assignment**: Tasks assigned to authorized users
3. **Audit Logging**: All workflow changes logged
4. **Access Control**: Restrict access to authorized users
5. **Data Scoping**: Workflow data scoped by tenant hierarchy

## Performance Considerations

### Workflow Performance

**Confirmed by Code**: Performance considerations:

1. **Caching**: Cache workflow definitions
2. **Queue Processing**: Use queues for async operations
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

### Mistake 2: Not Defining Transitions

**Symptom**: Workflow instance stuck in state

**Cause**: Not defining transitions

**Fix**:
```typescript
// Define transitions between states
await this.prisma.workflowTransition.create({
  data: {
    fromStateId: fromState.id,
    toStateId: toState.id,
    action: 'APPROVE',
    role: 'UNIVERSITY_ADMIN',
    workflowDefinitionId: definition.id,
  },
});
```

### Mistake 3: Not Using Queues for Auto-Transitions

**Symptom**: Auto-transitions blocking

**Cause**: Not using queues for auto-transitions

**Fix**:
```typescript
// Use queue for auto-transitions
if (transition.autoTransition) {
  await this.workflowQueue.add('auto-transition', { instanceId, transitionId });
}
```

## Debugging Guide

### Workflow Debugging

**Issue**: Workflow instance stuck

**Investigation**:
1. Check workflow definition
2. Check current state
3. Check available transitions
4. Check task assignments
5. Check logs

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

### Production Workflows

**Production Deployment**:
- Enable caching
- Implement data scoping
- Monitor workflow performance
- Monitor queue processing
- Audit all workflow changes

### Workflow Monitoring

**Monitoring Metrics**:
- Workflow instance creation rate
- Workflow completion rate
- Task completion rate
- Average workflow duration
- Failed workflow instances

## Example Requests

### Workflow Example

**Request**: Create workflow instance

```bash
POST /api/workflows/instances
Content-Type: application/json

{
  "workflowDefinitionId": "workflow-id",
  "entityId": "entity-id",
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

### Workflow Response

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

### Workflow Flow

```
Create Instance → Initial State → Task Created → User Action → Transition → Next State → Final State → Complete
```

## Architecture Diagrams

### Workflow Architecture

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

### Q2: How do you define a workflow?

**Answer**: Workflow definition via:
- Define workflow definition
- Define states (initial, intermediate, final)
- Define transitions between states
- Define actions for transitions
- Define role requirements

### Q3: How do you handle auto-transitions?

**Answer**: Auto-transitions via:
- Mark transition as autoTransition
- Queue auto-transition task
- Worker processes auto-transition
- Instance moves to next state
- Continue until final state

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

### Exercise 2: Process a Workflow Instance

**Task**: Process a workflow instance through states.

**Steps**:
1. Create workflow instance
2. Process initial state
3. Execute transitions
4. Complete tasks
5. Reach final state

**Verification**:
- Instance created
- States processed
- Transitions executed
- Tasks completed
- Final state reached

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

**Next Section**: [01-Workflow-Engine](./01-Workflow-Engine.md)

**Previous Section**: [08-Modules](../08-Modules/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [08-Modules](../08-Modules/README.md) - Module details
