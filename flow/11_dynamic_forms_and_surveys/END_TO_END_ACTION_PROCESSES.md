# Module 11: Dynamic Forms & Surveys — End-to-End Action Processes

> **Scope**: Dynamic schema persistence, JSON schema validation, submission payload parsing, draft saving, workflow triggers, and submission review endpoints.

---

## Action 1: Create Form Template (`POST /api/forms`)

- **HTTP Method & URL**: `POST /api/forms`
- **Guards**: `JwtAuthGuard`, `RolesGuard('SuperAdmin', 'UnivAdmin', 'InstAdmin')`
- **Request Body (DTO: `CreateFormTemplateDto`)**:
  ```json
  {
    "title": "Hostel Late Pass Request Form",
    "description": "Required for entry past 09:00 PM",
    "category": "FACILITIES",
    "workflowDefinitionId": "wf_def_late_pass_01",
    "schema": {
      "version": "1.0",
      "fields": [
        {
          "id": "fld_date_01",
          "type": "DATE",
          "label": "Late Return Date",
          "required": true
        },
        {
          "id": "fld_reason_02",
          "type": "TEXTAREA",
          "label": "Reason for Late Entry",
          "required": true,
          "minLength": 20
        }
      ]
    }
  }
  ```
- **Prisma Mutation**:
  ```prisma
  const template = await prisma.formTemplate.create({
    data: {
      title: dto.title,
      description: dto.description,
      category: dto.category,
      schema: dto.schema,
      workflowDefinitionId: dto.workflowDefinitionId,
      universityId: req.user.universityId,
      isActive: true
    }
  });
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "form_tmpl_9912",
    "title": "Hostel Late Pass Request Form",
    "isActive": true,
    "createdAt": "2026-09-11T12:00:00.000Z"
  }
  ```

---

## Action 2: Submit Form & Trigger Workflow (`POST /api/forms/:id/submit`)

- **HTTP Method & URL**: `POST /api/forms/:id/submit`
- **Request Body**:
  ```json
  {
    "responses": {
      "fld_date_01": "2026-09-15",
      "fld_reason_02": "Attending inter-college hackathon event till 10 PM."
    }
  }
  ```
- **Backend Flow**:
  1. Validates `responses` object against `FormTemplate.schema` rules.
  2. Creates `FormSubmission` row with status `SUBMITTED`.
  3. If form is linked to a `WorkflowDefinition`, instantiates a new `WorkflowInstance` and routes task to first stage approver (Hostel Warden).
- **Response (201 Created)**:
  ```json
  {
    "submissionId": "fsub_00412",
    "workflowInstanceId": "wf_inst_8819",
    "status": "SUBMITTED"
  }
  ```
