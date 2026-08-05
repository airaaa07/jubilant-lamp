# UI Design Specs: Workflow & Automation Screens

## Pages Covered
- `WorkflowDesignerPage.tsx`
- `WorkflowMonitorPage.tsx`
- `MyTasksPage.tsx`

---

## 1. Visual Workflow Designer Screen (`WorkflowDesignerPage.tsx`)

### Screen Purpose
Interactive drag-and-drop canvas for building multi-step approval workflows, configuring dynamic approver roles, Razorpay payment gates, and resource reservation hold timeouts.

### Visual Mockup Render
![Visual Workflow Designer UI Mockup](/home/admin/.gemini/antigravity-ide/brain/61696b17-1fe4-429b-b9b6-60a5b523471f/workflow_designer_ui_1785931519025.png)

### Layout & Component Specs
- **Left Palette (Workflow Blocks)**: Sidebar panel with draggable node blocks:
  - `Approval Node` (User/Role decision)
  - `Payment Gate Node` (Razorpay integration)
  - `Condition Node` (Branching logic)
  - `Resource Hold Node` (Saga reservation)
- **Center Canvas**: Interactive grid canvas with SVG connection arrows between step nodes (`Start` -> `HOD Approval` -> `Payment Gate` -> `Dean Approval` -> `End`).
- **Right Inspector Panel**: Configurator panel for setting approver role rules, status transition rules, and hold expiration timers.

---

## 2. My Approval Tasks Page (`MyTasksPage.tsx`)

### Screen Purpose
Personalized inbox for staff members and administrators to view, review, approve, or reject pending workflow tasks assigned to their role.

### Layout & Component Specs
- **Task List Table**: Table displaying Task ID, Workflow Name, Initiator User, Received Date, Status Badge (`PENDING`), and Action Buttons (`View Details`, `Approve`, `Reject`, `Delegate`).
- **Approval Comment Modal**: Popup dialog allowing approvers to enter mandatory review comments before submitting approval.
