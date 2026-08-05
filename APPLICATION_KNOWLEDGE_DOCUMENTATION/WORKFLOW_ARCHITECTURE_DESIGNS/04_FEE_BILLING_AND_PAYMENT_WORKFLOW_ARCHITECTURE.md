# Technical Workflow Architecture: Fee Billing, Ledger & Razorpay Integration

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, daily 2 AM recurring billing cron, double-entry financial ledger mutations, and Razorpay payment processing integrations.

---

## 🔄 End-to-End Sequence Diagram: Fee Demand & Payment Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student / Parent
    participant Cron as NestJS Cron Scheduler (02:00 AM)
    participant RecBill as RecurringBillingService
    participant FeeS as FeeService
    participant PayG as Razorpay Payment Gateway
    participant DB as PostgreSQL Database
    participant PdfS as DocumentsService

    note over Cron,RecBill: Daily 2:00 AM Recurring Billing Execution
    Cron->>RecBill: processDailyBilling()
    RecBill->>DB: Query Active Enrolled Students & Applicable Fee Structures
    RecBill->>DB: INSERT into fee_demands (status: "PENDING", dueDate)
    RecBill->>DB: INSERT into fee_demand_items (Head breakdown: Tuition, Library, Lab)

    Student->>FeeS: GET /api/v1/fee/demands/my-demands
    FeeS-->>Student: Return Outstanding Fee Demands

    Student->>FeeS: POST /api/v1/fee/demands/:id/pay (Initiate Payment)
    FeeS->>PayG: Create Razorpay Order (amount, currency)
    PayG-->>FeeS: Return razorpayOrderId
    FeeS-->>Student: Return Order Details & Razorpay Checkout Key

    Student->>PayG: Complete Payment via Razorpay Modal
    PayG-->>FeeS: Webhook / Verification Callback (signature, paymentId)
    FeeS->>FeeS: Verify Razorpay HMAC Signature
    
    FeeS->>DB: UPDATE fee_demands SET status = "PAID"
    FeeS->>DB: INSERT into payments (razorpay_payment_id, status: "SUCCESS")
    FeeS->>DB: INSERT into fee_ledger (type: "CREDIT", amount, balance)
    
    FeeS->>PdfS: generateReceiptPDF(paymentId)
    PdfS->>DB: INSERT into generated_documents & Upload MinIO PDF
    FeeS-->>Student: Payment Confirmed & Fee Receipt Issued
```

---

## 🔀 Fee Demand State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> PENDING: Created via Billing Cron / Manual Demand
    PENDING --> PARTIALLY_PAID: Partial Amount Paid
    PARTIALLY_PAID --> PAID: Remaining Balance Settled
    PENDING --> PAID: Full Payment Confirmed (Razorpay)
    PENDING --> OVERDUE: Due Date Exceeded (Cron Update)
    OVERDUE --> PAID: Late Fee + Demand Settled
    PENDING --> CANCELLED: Waived / Scholarship Applied
    PARTIALLY_PAID --> CANCELLED: Refunded / Adjusted
    PAID --> [*]
    CANCELLED --> [*]
```

---

## 📊 Double-Entry Financial Ledger Mutations

All financial transactions mutate the immutable `fee_ledger` table:

1. **Fee Demand Creation**:
   - `INSERT INTO fee_ledger (user_id, demand_id, transaction_type = 'DEBIT', amount = 2500, balance_after = 2500)`
2. **Razorpay Payment Settled**:
   - `INSERT INTO fee_ledger (user_id, payment_id, transaction_type = 'CREDIT', amount = 2500, balance_after = 0)`
3. **Scholarship Waiver Applied**:
   - `INSERT INTO fee_ledger (user_id, scholarship_id, transaction_type = 'CREDIT', amount = 500, balance_after = 0)`
