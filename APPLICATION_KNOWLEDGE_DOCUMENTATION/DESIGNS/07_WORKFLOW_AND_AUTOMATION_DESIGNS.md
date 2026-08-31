# UI Design Specs: Workflow & Automation Screens

## Pages Covered
- `WorkflowDesignerPage.tsx`
- `WorkflowMonitorPage.tsx`
- `MyTasksPage.tsx`
- `WorkflowProgress.tsx` (component)
- `InstanceDrawer.tsx` (component)

---

## 1. Visual Workflow Designer Screen (`WorkflowDesignerPage.tsx`)

### Screen Purpose
Interactive drag-and-drop canvas (37KB) for building multi-step approval workflows, configuring dynamic approver roles, Razorpay payment gates, and resource reservation hold timeouts. Includes a workflow catalog and definition management.

### Layout & Component Specs
- **Left Palette (Workflow Blocks)**: Sidebar panel with draggable node blocks:
  - `Approval Node` (User/Role decision)
  - `Payment Gate Node` (Razorpay integration)
  - `Condition Node` (Branching logic)
  - `Resource Hold Node` (Saga reservation with timeout)
- **Center Canvas**: Interactive grid canvas with SVG connection arrows between step nodes (`Start` → `HOD Approval` → `Payment Gate` → `Dean Approval` → `End`).
- **Right Inspector Panel**: Configurator panel for setting approver role rules, status transition rules, hold expiration timers.
- **Definition Management**: Create, update, publish lifecycle for workflow definitions.

### Workflow API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/workflow/catalog` | Available workflow types catalog |
| GET | `/api/workflow/definitions` | List workflow definitions |
| POST | `/api/workflow/definitions` | Create workflow definition |
| GET | `/api/workflow/definitions/:id` | Get definition detail |
| PATCH | `/api/workflow/definitions/:id` | Update definition metadata |
| DELETE | `/api/workflow/definitions/:id` | Delete draft definition |
| PUT | `/api/workflow/definitions/:id/graph` | Save visual graph/node layout |
| POST | `/api/workflow/definitions/:id/publish` | Publish definition (makes it active) |

---

## 2. My Approval Tasks Page (`MyTasksPage.tsx`)

### Screen Purpose
Personalized inbox (60KB) for staff members and administrators to view, review, approve, reject, or delegate pending workflow tasks assigned to their role. Includes payment gate integration.

### Layout & Component Specs
- **Task List Table**: Table displaying Task ID, Workflow Name, Initiator User, Received Date, Status Badge (`PENDING`), and Action Buttons.
- **Approval Actions**:
  - `Approve & Advance Step` → `POST /api/workflow/tasks/:id/act { action: 'APPROVE', comments }`
  - `Reject` → `POST /api/workflow/tasks/:id/act { action: 'REJECT', comments }`
  - `Delegate` → `POST /api/workflow/tasks/:id/act { action: 'DELEGATE', targetUserId }`
- **Payment Gate Tasks**: When a workflow step requires payment:
  - Create Razorpay order: `POST /api/workflow/tasks/:id/payment/order`
  - Verify payment: `POST /api/workflow/tasks/:id/payment/verify`
- **Approval Comment Modal**: Popup dialog for mandatory review comments before submitting.

### Task API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/workflow/inbox` | Get current user's pending tasks |
| POST | `/api/workflow/tasks/:id/act` | Execute task action (approve/reject/delegate) |
| POST | `/api/workflow/tasks/:id/payment/order` | Create payment order for payment gate |
| POST | `/api/workflow/tasks/:id/payment/verify` | Verify Razorpay payment |

---

## 3. Workflow Monitor Page (`WorkflowMonitorPage.tsx`)

### Screen Purpose
Administrative dashboard for monitoring all active workflow instances across the system, tracking aging, bottlenecks, and expired holds.

### Layout & Component Specs
- **Instance Table**: Filterable list of all workflow instances with status, current step, initiator, created date, aging metrics.
- **Instance Drawer** (`InstanceDrawer.tsx`): Slide-out detail panel showing full workflow execution history, step-by-step timeline.
- **Workflow Progress Component** (`WorkflowProgress.tsx`): Visual progress indicator showing completed/current/pending steps.
- **Aging Analytics**: Instance aging breakdown by status (active, waiting, expired).

### Monitor API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/workflow/instances` | List all instances with filters |
| GET | `/api/workflow/instances-aging` | Instance aging analytics |
| GET | `/api/workflow/instances/:id` | Get instance detail |
| POST | `/api/workflow/admin/run-expiry` | Manually trigger hold expiration |

---

## 4. Backend Services

### `workflow-definition.service.ts`
Workflow definition CRUD, graph serialization/deserialization, publish lifecycle.

### `workflow-engine.service.ts`
Core workflow execution engine — state machine processing, actor resolution, step transition, notification dispatch.

### `workflow-payment.service.ts`
Razorpay integration for payment gate nodes — order creation, signature verification, payment-to-step linkage.

### `reservation.service.ts`
Resource hold management for saga-pattern workflows — soft reservation with TTL, compensating actions on expiry.

### `workflow-scheduler.service.ts`
NestJS `@Cron` scheduled job — expires overdue payment demands, releases stale resource holds, cancels timed-out workflow instances.
