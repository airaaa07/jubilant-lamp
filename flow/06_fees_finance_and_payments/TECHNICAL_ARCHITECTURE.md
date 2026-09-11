# Module 06: Fees, Finance & Payments — Technical Architecture

> **Scope**: Double-entry student ledger architecture, payment gateway idempotency and reconciliation models, fee demand generation scheduling, and payment window expiry logic.

---

## 1. Double-Entry Student Fee Ledger Architecture

Every financial debit (fee demand raised) and credit (payment received, scholarship applied, waiver granted) is recorded as an immutable ledger transaction in `FeeLedger`.

```mermaid
erDiagram
    Student ||--o{ FeeDemand : "owes"
    Student ||--o{ FeeLedger : "maintains financial ledger"
    FeeDemand ||--o{ Payment : "settled by"
    FeeStructure ||--o{ FeeHead : "composed of"
    Student ||--o{ FeeWaiver : "granted"
    Student ||--o{ Scholarship : "awarded"

    FeeDemand {
        string id PK
        string studentId FK
        string feeStructureId FK
        decimal totalAmount
        decimal paidAmount
        decimal balanceAmount
        datetime dueDate
        string status
    }

    Payment {
        string id PK
        string feeDemandId FK
        decimal amount
        string paymentMode
        string gatewayOrderId
        string gatewayPaymentId
        string status
        datetime paidAt
    }

    FeeLedger {
        string id PK
        string studentId FK
        string entryType
        string category
        decimal amount
        decimal runningBalance
        string referenceId
        datetime createdAt
    }
```

### Running Balance Formula
$$\text{Current Balance} = \sum (\text{DEBIT Amounts}) - \sum (\text{CREDIT Amounts})$$

---

## 2. Payment Expiry & Resource Hold Expiration Engine

When an applicant is offered a seat (or an approved hostel room/bus pass), a background job enforces the configured payment window (e.g. 48 hours per commit `6f060a59`).

```mermaid
stateDiagram-v2
    [*] --> OFFER_ISSUED: Merit Offer Released
    OFFER_ISSUED --> PENDING_PAYMENT: Admission Demand Raised
    
    state PENDING_PAYMENT {
        [*] --> TimerRunning
        TimerRunning --> CountdownActive: Live Clock on Portal
    }

    PENDING_PAYMENT --> ADMITTED: Payment Received Before Deadline
    PENDING_PAYMENT --> OFFER_EXPIRED: Hours Elapsed Without Payment

    OFFER_EXPIRED --> SEAT_RELEASED: Background Worker cancels offer
    SEAT_RELEASED --> NEXT_IN_MERIT: Seat offered to next ranked candidate
```
