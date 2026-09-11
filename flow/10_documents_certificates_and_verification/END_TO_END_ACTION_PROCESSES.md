# Module 10: Documents, Certificates & Verification — End-to-End Action Processes

> **Scope**: Backend API lifecycles, canvas serialization to PDF, ID format serial generation (`document_type` token per commit `7e4a63a3`), certificate stock audit comment tracking per commit `f23b646e`, and public verification email triggers via Communication Message Templates per commit `ff8a09d1`.

---

## Action 1: Issue Document & ID Format Serial Generation (`POST /api/documents/issue`)

Per commits `218bf299`, `7e4a63a3`, `f23b646e`, and `cd7838fa`:

```mermaid
sequenceDiagram
    autonumber
    Client->>DocumentsController: POST /api/documents/issue { templateId, studentId, hardcopy, prePrintedSerial }
    DocumentsController->>DocumentsService: issueDocument(dto, user)
    DocumentsService->>IdFormatService: generateSerial("DOCUMENT_NUMBER", { document_type: template.type, year: 2026 })
    IdFormatService->>Prisma: idSequenceCounter.update({ increment: 1 })
    IdFormatService-->>DocumentsService: Serial "DOC-2026-DEG-00412"
    
    alt Hardcopy with pre-printed stock
        DocumentsService->>Prisma: certificateStock.findUnique({ where: { serialNumber: dto.prePrintedSerial } })
        DocumentsService->>Prisma: certificateStock.update({
            status: "ISSUED",
            comment: "issued: " + student.enrollmentNo + "/" + user.email
        })
    end

    DocumentsService->>Prisma: issuedDocument.create({
        serialNumber: "DOC-2026-DEG-00412",
        prePrintedSerial: dto.prePrintedSerial,
        studentId, templateId, issuedBy: user.id
    })
    DocumentsService->>CertWorker: Render HTML/PDF with QR Code
    DocumentsService-->>DocumentsController: Success object with signed PDF URL
    DocumentsController-->>Client: 201 Created
```

### Protocol Specifications
- **HTTP Method & URL**: `POST /api/documents/issue`
- **Guards**: `JwtAuthGuard`, `RolesGuard('UnivAdmin', 'InstAdmin', 'ExaminationController')`
- **Request Body (DTO: `IssueDocumentDto`)**:
  ```json
  {
    "templateId": "tmpl_degree_cert_01",
    "studentId": "std_2026_cse_042",
    "batchTermId": "bterm_08",
    "deliveryMode": "HARDCOPY",
    "prePrintedSerial": "STK-2026-99120"
  }
  ```
- **Prisma Database Mutation**:
  ```prisma
  await prisma.$transaction(async (tx) => {
    // 1. Generate document number from ID Format engine
    const serialNo = await idFormatService.generateNumber(tx, "Document Number", {
      document_type: template.type,
      institute_code: student.institute.code,
      year: new Date().getFullYear().toString()
    });

    // 2. If hardcopy, allocate and comment on stock
    if (dto.deliveryMode === "HARDCOPY" && dto.prePrintedSerial) {
      await tx.certificateStock.update({
        where: { serialNumber: dto.prePrintedSerial },
        data: {
          status: "ISSUED",
          comment: `issued: ${student.enrollmentNo}/${req.user.email}`,
          issuedAt: new Date(),
          issuedToStudentId: student.id
        }
      });
    }

    // 3. Create IssuedDocument
    const issued = await tx.issuedDocument.create({
      data: {
        serialNumber: serialNo,
        prePrintedSerial: dto.prePrintedSerial ?? null,
        documentTemplateId: dto.templateId,
        studentId: dto.studentId,
        issuedById: req.user.id,
        status: "ISSUED",
        metadata: {
          termName: term.name,
          cgpa: studentResult.cgpa
        }
      }
    });

    return issued;
  });
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "doc_iss_8819",
    "serialNumber": "DOC-2026-DEG-00412",
    "prePrintedSerial": "STK-2026-99120",
    "verificationUrl": "https://erp.university.edu/verify?serial=DOC-2026-DEG-00412",
    "issuedAt": "2026-09-11T12:00:00.000Z"
  }
  ```

---

## Action 2: Public Verification Decision & Email Dispatch (`PATCH /api/documents/verification-requests/:id/decide`)

Per commit `ff8a09d1`, requester emails are dispatched via the central Communication Message Templates:
- `doc_verification_submitted`: Notifies third-party requester (e.g. background check agency) that request was received.
- `doc_verification_decided`: Dispatches official decision letter (VERIFIED or REJECTED) with cryptographic authenticity token.

- **HTTP Method & URL**: `PATCH /api/documents/verification-requests/:id/decide`
- **Request Body**:
  ```json
  {
    "decision": "VERIFIED",
    "remarks": "Document genuine and records match university archives."
  }
  ```
- **Backend Flow**:
  1. Updates `DocumentVerificationRequest` status to `VERIFIED`.
  2. Resolves template `doc_verification_decided` from `MessageTemplate` registry.
  3. Replaces tokens (`{{requesterName}}`, `{{documentSerial}}`, `{{decision}}`, `{{remarks}}`).
  4. Queues email job via `NotificationWorker`.
- **Response (200 OK)**: `{ "success": true, "status": "VERIFIED" }`
