# Module 10: Documents, Certificates & Verification — Technical Architecture

> **Scope**: Canvas document serialization to HTML/PDF, ID format pattern tokenizer with `document_type` custom token, certificate physical inventory lifecycle, and QR verification cryptographic validation.

---

## 1. Document Canvas Rendering & Serialization Pipeline

Templates authored in `CanvasDocumentDesigner.tsx` serialize to a JSON model containing coordinates, styling, tables, pair layouts, and dynamic token placeholders.

```mermaid
flowchart TD
    CanvasEditor["CanvasDocumentDesigner.tsx (UI)"] --> CanvasJSON["Canvas Model JSON<br/>{ elements: [Text, Image, Table, StudentDetails], width: 794, height: 1123 }"]
    CanvasJSON --> Storage["Prisma: DocumentTemplate.canvasModel"]
    
    Storage --> RenderEngine["render.ts / canvas-serialize.ts (Core API)"]
    RenderEngine --> TokenResolver["student-data.fn.ts & field-catalog.ts"]
    TokenResolver -->|Inject Values| ResolvedHTML["Self-Contained HTML Sheet with Base64 Assets & QR Code"]
    
    ResolvedHTML --> InAppModal["DocumentPreviewModal.tsx (Scaled CSS A4 Sheet, Commit 367b73a9)"]
    ResolvedHTML --> PuppeteerPDF["Certificate Generator Worker (High-Resolution Print PDF)"]
```

---

## 2. Certificate Stock Inventory State Machine

Per commits `f23b646e`, `ca129574`, and `8a62655c`, physical stationary security sheets (watermarked paper with holographic serials) follow an audited custody lifecycle.

```mermaid
stateDiagram-v2
    [*] --> STOCK_BATCH_CREATED: Admin logs Batch of 500 Blank Certificates
    STOCK_BATCH_CREATED --> UNUSED: Stock Serials Generated (STK-001 to STK-500)
    
    state UNUSED {
        [*] --> InVault
        InVault --> VaultAudited: Page Size 5/10/20 Paging (Commit acd19130)
    }

    UNUSED --> ISSUED: Hardcopy Issue Flow (Commit cd7838fa)
    note right of ISSUED: Comment recorded: 'issued: <enrollmentNo>/<user email>' (Commit f23b646e)
    
    UNUSED --> DAMAGED: Physical Defect / Printer Jam
    note right of DAMAGED: Comment recorded: 'damaged: <reason>/<user email>' (Commit f23b646e)

    ISSUED --> REVOKED: Degree Withdrawn / Legal Invalidation
    DAMAGED --> [*]
    REVOKED --> [*]
```

---

## 3. QR Verification Cryptographic Validation Pipeline

Every certificate carries a 2D QR code embedding a signed verification URL:
`https://erp.university.edu/verify?serial=DOC-2026-DEG-00412`

```mermaid
flowchart LR
    Scanner["Employer / Verifier Scans QR"] --> PublicVerifyPage["/verify Route (PublicVerifyPage.tsx)"]
    PublicVerifyPage --> PublicConfig["GET /api/documents/config"]
    PublicConfig --> LogoFallback["Logo Fallback Check (Commit 8440e7c8):<br/>Doc Logo -> University.logoPath"]
    LogoFallback --> VerifyCall["GET /api/documents/verify/:serial"]
    VerifyCall --> DBCheck[("Prisma: IssuedDocument.findUnique()")]
    DBCheck --> HashCheck{"SHA-256 Digest matches Document Record?"}
    HashCheck -->|Valid & Active| Authentic["Render Authentic Badge & Recipient Details"]
    HashCheck -->|Revoked| Revoked["Render Red Revocation Notice & Reason"]
    HashCheck -->|Not Found| Fraud["Render Invalid / Counterfeit Warning"]
```
