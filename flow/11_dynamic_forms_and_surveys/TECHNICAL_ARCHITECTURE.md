# Module 11: Dynamic Forms & Surveys — Technical Architecture

> **Scope**: Dynamic schema architecture, field dependency evaluation engine, workflow trigger integration, and submission lifecycle models.

---

## 1. Dynamic Form Schema Architecture

Form schemas are defined in JSON Schema standard format, rendering through a dynamic React field component engine.

```mermaid
flowchart TD
    SchemaJSON["FormTemplate.schema (JSON)"] --> Parser["Dynamic Form Engine (FormsPage.tsx)"]
    
    Parser --> DependencyGraph["Field Dependency & Condition Evaluator"]
    DependencyGraph -->|Conditions Met| ActiveFields["Active Rendered Inputs"]
    DependencyGraph -->|Conditions Not Met| HiddenFields["Unmounted / Cleared Inputs"]
    
    ActiveFields --> Validator["Zod / React Hook Form Client Validator"]
    Validator -->|Valid| SubmitPayload["POST /api/forms/:id/submit"]
    SubmitPayload --> ServerValidator["Core API JSON Schema Validator (AJV / Class-Validator)"]
    ServerValidator --> Storage[("Prisma: FormSubmission (responses JSONB)")]
```

---

## 2. Form Submission Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Student initiates form
    DRAFT --> DRAFT: POST /api/forms/:id/save-draft (Progress autosaved)
    DRAFT --> SUBMITTED: POST /api/forms/:id/submit (All required fields verified)
    
    state SUBMITTED {
        [*] --> UnderReview
        UnderReview --> Stage1Approved: First-Level Reviewer Approves
        Stage1Approved --> Stage2Approved: Second-Level Reviewer Approves
        UnderReview --> ReturnedForRevision: Reviewer asks for additional documents
    }

    ReturnedForRevision --> SUBMITTED: Student updates and resubmits
    Stage2Approved --> APPROVED: Final Sanction (Action executed)
    UnderReview --> REJECTED: Request Declined
    
    APPROVED --> [*]
    REJECTED --> [*]
```
