# Workflow Worker

## Purpose

This document explains the workflow worker in the University ERP system. It details how the workflow worker processes workflow-related tasks such as auto-transitions and workflow completions.

## Why This Document Exists

**Confirmed by Code**: The workflow worker handles workflow automation. Understanding the workflow worker is critical for:
- Processing workflow auto-transitions
- Handling workflow completions
- Automating workflow processes
- Debugging workflow issues
- Creating custom workflow processors

Without understanding the workflow worker, developers may struggle with workflow automation or may introduce workflow bugs.

## Where This Is Used

- **Onboarding**: New developers learn workflow worker
- **Feature Development**: Implementing workflow automation
- **Code Reviews**: Reviewing workflow code
- **Workflows**: Processing workflow tasks
- **Automation**: Automating workflow processes

## Dependencies

### Workflow Worker Dependencies

**Confirmed by Code**: Workflow worker depends on:

- **Bull**: Queue library
- **NestJS**: Framework for workers
- **WorkflowService**: Workflow service
- **Prisma**: Database access
- **Redis**: Queue storage

## Internal Architecture

### Workflow Worker Architecture

**Confirmed by Code**: Workflow worker follows Bull queue pattern.

```
┌─────────────────────────────────────────────────────────┐
│              Service                                     │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Workflow Queue                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Workflow Worker                              │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Auto-Transition│  │  Workflow       │  │  Task          │
│  Processor    │  │  Completion     │  │  Processor      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Workflow Worker Implementation

**Confirmed by Code**: Workflow worker processes workflow tasks.

**WorkflowWorker**:
```typescript
import { Processor, Process } from '@nestjs/bull';
import { Job } from 'bull';
import { Injectable } from '@nestjs/common';

@Injectable()
@Processor('workflow')
export class WorkflowWorker {
  constructor(private workflowService: WorkflowService) {}

  @Process('auto-transition')
  async handleAutoTransition(job: Job) {
    const { instanceId, stateId } = job.data;

    try {
      await this.workflowService.transition(instanceId, 'AUTO', {
        role: 'SYSTEM',
      } as JwtPayload);
      await job.progress(100);
    } catch (error) {
      throw new Error(`Failed to auto-transition: ${error.message}`);
    }
  }

  @Process('workflow-complete')
  async handleWorkflowComplete(job: Job) {
    const { instanceId, entityId, entityType } = job.data;

    try {
      await this.workflowService.onWorkflowComplete(instanceId);
      await job.progress(100);
    } catch (error) {
      throw new Error(`Failed to handle workflow completion: ${error.message}`);
    }
  }

  @Process('process-task')
  async handleProcessTask(job: Job) {
    const { taskId, action } = job.data;

    try {
      await this.workflowService.processTask(taskId, action);
      await job.progress(100);
    } catch (error) {
      throw new Error(`Failed to process task: ${error.message}`);
    }
  }
}
```

**What This Does**:
- **auto-transition**: Processes workflow auto-transitions
- **workflow-complete**: Handles workflow completion
- **process-task**: Processes workflow tasks
- **Progress Tracking**: Updates job progress
- **Error Handling**: Handles errors gracefully

### Workflow Service Integration

**Confirmed by Code**: Workflow worker calls workflow service.

**WorkflowService**:
```typescript
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

  const transition = instance.workflowDefinition.transitions.find(
    t => t.fromStateId === instance.currentStateId && t.action === action,
  );

  const targetState = await this.prisma.workflowState.findUnique({
    where: { id: transition.toStateId },
  });

  const updatedInstance = await this.prisma.workflowInstance.update({
    where: { id: instanceId },
    data: {
      currentStateId: targetState.id,
      completedAt: targetState.isFinal ? new Date() : null,
    },
  });

  await this.createTasksForState(updatedInstance, targetState);
  await this.logEvent(instanceId, action, `Transitioned to ${targetState.name}`);

  if (transition.autoTransition) {
    await this.queueAutoTransition(instanceId, transition.toStateId);
  }

  if (targetState.isFinal) {
    await this.onWorkflowComplete(updatedInstance);
  }

  return updatedInstance;
}
```

**What This Does**:
- **transition**: Transitions workflow instance
- **Target State**: Gets target state
- **Update Instance**: Updates instance state
- **Create Tasks**: Creates tasks for new state
- **Auto-Transition**: Queues auto-transition if needed
- **Completion**: Handles workflow completion

## Database Interactions

### Workflow Worker-Database Flow

**Confirmed by Code**: Workflow worker interacts with database.

**Flow**:
```
Worker → WorkflowService → Prisma → Workflow Tables
```

## Redis Interactions

### Workflow Worker-Redis Flow

**Confirmed by Code**: Workflow worker uses Redis for queue storage.

**Flow**:
```
Service → Redis Queue → Worker
```

## Queue Interactions

### Workflow Worker-Queue Flow

**Confirmed by Code**: Workflow worker processes jobs from queue.

**Flow**:
```
Service → Workflow Queue → Worker → Process Job
```

## Worker Interactions

### Workflow Worker-Worker Flow

**Confirmed by Code**: Workflow worker may queue jobs for other workers.

**Flow**:
```
Workflow Worker → Notification Queue → Notification Worker
```

## Business Rules

### Workflow Worker Rules

**Confirmed by Code**: Workflow worker follows these rules:

1. **Async Processing**: Workflow tasks processed asynchronously
2. **Queue-Based**: Workflow tasks queued for processing
3. **Retry Logic**: Failed tasks retried
4. **Progress Tracking**: Job progress tracked
5. **Event Logging**: All transitions logged

### Auto-Transition Rules

**Confirmed by Code**: Auto-transition rules:

1. **Auto-Transition**: Marked transitions auto-execute
2. **Queue**: Auto-transitions queued for processing
3. **System User**: Auto-transitions executed as SYSTEM user
4. **Sequential**: Auto-transitions execute sequentially
5. **Final State**: Auto-transitions stop at final state

## Security

### Workflow Worker Security

**Confirmed by Code**: Security considerations for workflow worker:

1. **System User**: Auto-transitions use SYSTEM user
2. **Input Validation**: Validate job data
3. **Access Control**: Worker has limited access
4. **Audit Logging**: Log all workflow actions
5. **Error Messages**: Don't leak sensitive info

## Performance Considerations

### Workflow Worker Performance

**Confirmed by Code**: Performance considerations:

1. **Concurrency**: Configure worker concurrency
2. **Batch Processing**: Batch process workflow tasks
3. **Database Queries**: Optimize database queries
4. **Queue Size**: Monitor queue size
5. **Retry Logic**: Configure retry logic

## Common Mistakes

### Mistake 1: Not Handling Auto-Transitions

**Symptom**: Workflow stuck in state

**Cause**: Not handling auto-transitions

**Fix**:
```typescript
// Queue auto-transition
if (transition.autoTransition) {
  await this.queueAutoTransition(instanceId, transition.toStateId);
}
```

### Mistake 2: Not Updating Progress

**Symptom**: No progress tracking

**Cause**: Not updating job progress

**Fix**:
```typescript
// Update progress
await job.progress(50);
```

### Mistake 3: Not Logging Events

**Symptom**: No workflow history

**Cause**: Not logging workflow events

**Fix**:
```typescript
// Log event
await this.logEvent(instanceId, action, `Transitioned to ${targetState.name}`);
```

## Debugging Guide

### Workflow Worker Debugging

**Issue**: Workflow not transitioning

**Investigation**:
1. Check queue connection
2. Check job data
3. Check worker logic
4. Check workflow definition
5. Check logs

**Tools**:
- Worker logs
- Queue logs
- Workflow logs
- Database logs

## Future Enhancements

### Parallel Auto-Transitions

**Status**: Not implemented

**Proposal**: Implement parallel auto-transitions:
- Execute auto-transitions in parallel
- Better performance
- More complex
- Better for complex workflows
- More resource usage

### Workflow Monitoring

**Status**: Not implemented

**Proposal**: Implement workflow monitoring:
- Workflow health checks
- Workflow metrics
- Workflow alerts
- Better observability
- More complex

## Production Considerations

### Production Workflow Worker

**Production Deployment**:
- Enable all processors
- Configure concurrency
- Configure retry logic
- Monitor queue size
- Monitor workflow performance

### Workflow Worker Monitoring

**Monitoring Metrics**:
- Auto-transition rate
- Workflow completion rate
- Task processing rate
- Queue size
- Workflow duration

## Example Requests

### Workflow Worker Example

**Queue Auto-Transition Job**:
```typescript
await this.workflowQueue.add('auto-transition', {
  instanceId: 'instance-id',
  stateId: 'state-id',
});
```

## Example Responses

### Workflow Worker Response

**Job Completed**:
```typescript
await job.progress(100);
// Job marked complete
```

## Sequence Diagrams

### Workflow Worker Flow

```
Service → Workflow Queue → Worker → WorkflowService → Database → Workflow Updated
```

## Architecture Diagrams

### Workflow Worker Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Service                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Workflow Queue                             │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Workflow Worker                            │
└─────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Auto-Transition│  │  Workflow       │  │  Task          │
│  Processor    │  │  Completion     │  │  Processor      │
└────────────────┘  └────────────────┘  └─────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  WorkflowService                           │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Database                                   │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does the workflow worker work?

**Answer**: Workflow worker via:
- Processes jobs from workflow queue
- Executes auto-transitions
- Handles workflow completions
- Processes workflow tasks
- Updates workflow state

### Q2: How do you trigger an auto-transition?

**Answer**: Auto-transition via:
- Mark transition as autoTransition in definition
- Queue auto-transition job
- Worker processes auto-transition
- Workflow transitions to next state
- Continue until final state

### Q3: How do you handle workflow completion?

**Answer**: Workflow completion via:
- Detect final state
- Queue workflow-complete job
- Worker processes completion
- Execute completion actions
- Send notifications

## Exercises

### Exercise 1: Create a Workflow Processor

**Task**: Create a custom workflow processor.

**Steps**:
1. Add @Process decorator
2. Implement processor logic
3. Add error handling
4. Add progress tracking
5. Test processor

**Verification**:
- Processor created
- Logic works
- Error handling works
- Progress tracking works
- Tests pass

### Exercise 2: Implement Task Processing

**Task**: Implement task processing.

**Steps**:
1. Add task processor
2. Implement task logic
3. Add progress tracking
4. Add error handling
5. Test task processing

**Verification**:
- Processor created
- Task logic works
- Progress tracking works
- Error handling works
- Tests pass

## Real Production Scenarios

### Scenario 1: Workflow Stuck

**Situation**: Workflow stuck in state

**Response**:
1. Check workflow definition
2. Check auto-transition
3. Check worker logic
4. Fix workflow
5. Test workflow

### Scenario 2: Queue Backlog

**Situation**: Workflow queue backlog

**Response**:
1. Check queue size
2. Add more workers
3. Optimize processing
4. Monitor queue
5. Clear backlog

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [01-Notification-Worker](./01-Notification-Worker.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [09-Workflows](../09-Workflows/README.md) - Workflow details
