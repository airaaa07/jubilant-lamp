# Module 06: Fees, Finance & Payments — End-to-End Action Processes

> **Enterprise Technical Specification**: Financial accounting lifecycle, automated fee demand generation, double-entry student ledgers, Razorpay payment gateway order initialization and cryptographic webhook reconciliation, offline cash/draft collection, fee waiver workflows, deposit refund processing, and university payment window configurations (commit `6f060a59`).

---

## Complete Action & Endpoint Catalog

| Action # | Endpoint | HTTP Method | Primary Actor | Description & Security Scope |
|:---:|:---|:---:|:---|:---|
| **01** | `/api/settings/payment-windows` | `PUT` | UnivAdmin | Configures application and admission fee payment window expiry hours (commit `6f060a59`). |
| **02** | `/api/fee/heads` | `POST` / `GET` | UnivAdmin | Defines catalog fee heads (Tuition, Development, Lab, Caution Deposit, Library, Hostel). |
| **03** | `/api/fee/structures` | `POST` / `GET` | UnivAdmin / InstAdmin | Creates academic term fee structures per Programme and Batch cohort. |
| **04** | `/api/fee/batch-charge` | `POST` | Finance Officer | Bulk generates semester fee demands for all active enrolled students in a batch. |
| **05** | `/api/fee/demands` | `POST` | Finance Officer | Creates ad-hoc individual fee demands (Breakage fine, Condonation fee, Re-evaluation). |
| **06** | `/api/fee/demands/summary` | `GET` | Finance Officer | High-level financial reporting: Total Billed, Total Collected, Total Outstanding, Concessions. |
| **07** | `/api/fee/demands/ledger/:userId` | `GET` | Student / Finance | Retrieves complete chronologically sorted double-entry debit/credit ledger statement. |
| **08** | `/api/fee/razorpay/demand-order` | `POST` | Student | Initializes Razorpay payment order for outstanding fee demand. |
| **09** | `/api/fee/razorpay/verify-demand-payment` | `POST` | Student / Gateway | Cryptographically verifies HMAC-SHA256 signature and records credit transaction. |
| **10** | `/api/fee/payments` (Offline) | `POST` | Cashier | Records manual offline collection (Cash, Cheque, Demand Draft, NEFT/RTGS with UTR). |
| **11** | `/api/fee/waivers` | `POST` | Student / Staff | Applies for merit, sports, or hardship fee waiver; attaches supporting proofs. |
| **12** | `/api/fee/waivers/:id/approve` | `PATCH` | Finance Committee | Sanctions fee waiver; automatically credits student ledger and reduces demand balance. |
| **13** | `/api/fee/deposit-refund` | `POST` | Alumnus / Leaver | Requests refund of refundable caution deposits upon graduation or approved cancellation. |
| **14** | `/api/fee/reports/defaulters` | `GET` | Finance Officer | Queries students with overdue balances exceeding grace periods for hall ticket blocking. |

---

## Action 1: Bulk Fee Demand Generation (`POST /api/fee/batch-charge`)

```mermaid
sequenceDiagram
    autonumber
    actor Finance as Finance Officer
    participant Ctrl as FeeController
    participant Service as FeeService
    participant DB as PostgreSQL (Prisma)
    participant Queue as BullMQ (Notifications)

    Finance->>Ctrl: POST /api/fee/batch-charge { batchTermId, dueDate, feeStructureId }
    Ctrl->>Service: chargeBatch(dto, user)
    Service->>DB: Query all enrolled students in batchTermId
    DB-->>Service: 120 Student records

    loop For each student
        Service->>DB: Calculate concessions / scholarships active on student profile
        Service->>DB: $transaction [
            1. feeDemand.create({ studentId, totalAmount: 45000, balanceAmount: 40000 })
            2. feeLedger.create({ entryType: 'DEBIT', category: 'TERM_TUITION', amount: 45000 })
            3. If scholarship active: feeLedger.create({ entryType: 'CREDIT', amount: 5000 })
        ]
        Service->>Queue: emit("FEE_DEMAND_RAISED", { studentId, amount: 40000, dueDate })
    end

    Service-->>Ctrl: { success: true, demandsGenerated: 120, totalBilled: 4800000 }
    Ctrl-->>Finance: 201 Created
```

### Protocol Specifications
- **HTTP Method & URL**: `POST /api/fee/batch-charge`
- **Guards**: `JwtAuthGuard`, `RolesGuard('UnivAdmin', 'InstAdmin', 'FinanceOfficer')`
- **Request Body (DTO: `BatchChargeDto`)**:
  ```json
  {
    "batchTermId": "bterm_2026_cse_t3",
    "feeStructureId": "feestr_btech_2026_t3",
    "dueDate": "2026-10-15",
    "allowInstallments": true
  }
  ```
- **Prisma Database Mutation**:
  ```prisma
  await prisma.$transaction(async (tx) => {
    const students = await tx.student.findMany({
      where: { batchId: batchTerm.batchId, status: "ENROLLED" },
      include: { studentConcessions: { where: { isActive: true } } }
    });

    for (const std of students) {
      const concessionTotal = std.studentConcessions.reduce((acc, c) => acc + Number(c.amount), 0);
      const netAmount = Math.max(0, structure.totalAmount - concessionTotal);

      const demand = await tx.feeDemand.create({
        data: {
          studentId: std.id,
          feeStructureId: dto.feeStructureId,
          totalAmount: structure.totalAmount,
          concessionAmount: concessionTotal,
          paidAmount: 0,
          balanceAmount: netAmount,
          dueDate: new Date(dto.dueDate),
          status: "PENDING"
        }
      });

      // Debit ledger entry
      await tx.feeLedger.create({
        data: {
          studentId: std.id,
          entryType: "DEBIT",
          category: "SEMESTER_FEE",
          amount: structure.totalAmount,
          referenceId: demand.id,
          remarks: `Semester fee demand for Term ${batchTerm.termNumber}`
        }
      });

      // If concession exists, record offsetting credit
      if (concessionTotal > 0) {
        await tx.feeLedger.create({
          data: {
            studentId: std.id,
            entryType: "CREDIT",
            category: "SCHOLARSHIP_CONCESSION",
            amount: concessionTotal,
            referenceId: demand.id,
            remarks: `Institutional scholarship concession applied`
          }
        });
      }
    }
  });
  ```
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "demandsGenerated": 120,
    "totalBilledAmount": 4800000,
    "dueDate": "2026-10-15T00:00:00.000Z"
  }
  ```

---

## Action 2: Online Razorpay Payment Checkout & Ledger Reconciliation (`POST /api/fee/razorpay/verify-demand-payment`)

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant Portal as FeesPage.tsx
    participant Ctrl as FeeController
    participant Service as FeeService
    participant Gateway as Razorpay Servers
    participant DB as PostgreSQL (Prisma)

    Student->>Portal: Clicks "Pay Now" on Demand #DEM-8821 (₹40,000)
    Portal->>Ctrl: POST /api/fee/razorpay/demand-order { demandId: "dem_8821" }
    Ctrl->>Gateway: Create Order { amount: 4000000, currency: "INR", receipt: "dem_8821" }
    Gateway-->>Ctrl: { orderId: "order_Kz89102" }
    Ctrl-->>Portal: Returns orderId
    
    Portal->>Gateway: Mounts Checkout SDK -> Student completes UPI payment
    Gateway-->>Portal: Returns { razorpay_payment_id, razorpay_order_id, razorpay_signature }
    
    Portal->>Ctrl: POST /api/fee/razorpay/verify-demand-payment
    Ctrl->>Service: verifyPayment(payload)
    Service->>Service: Verify HMAC-SHA256(order_id + "|" + payment_id, SECRET) == signature
    
    Service->>DB: $transaction [
        1. payment.create({ gatewayPaymentId, amount: 40000, status: 'SUCCESS' })
        2. feeDemand.update({ paidAmount: 40000, balanceAmount: 0, status: 'PAID' })
        3. feeLedger.create({ entryType: 'CREDIT', amount: 40000, category: 'ONLINE_PAYMENT' })
    ]
    DB-->>Service: Committed
    Service-->>Ctrl: { success: true, receiptNo: "REC-2026-0941" }
    Ctrl-->>Portal: 200 OK -> Displays success modal & receipt download
```

### Protocol Specifications
- **HTTP Method & URL**: `POST /api/fee/razorpay/verify-demand-payment`
- **Request Body (DTO: `VerifyPaymentDto`)**:
  ```json
  {
    "demandId": "dem_8821",
    "razorpayOrderId": "order_Kz89102",
    "razorpayPaymentId": "pay_Kz899120",
    "razorpaySignature": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "receiptNumber": "REC-2026-0941",
    "amountPaid": 40000,
    "remainingBalance": 0,
    "paymentTimestamp": "2026-09-11T12:00:00.000Z"
  }
  ```

---

## Action 3: Offline Fee Cash/Cheque Counter Collection (`POST /api/fee/payments`)

- **HTTP Method & URL**: `POST /api/fee/payments`
- **Guards**: `JwtAuthGuard`, `RolesGuard('Cashier', 'FinanceOfficer', 'InstAdmin')`
- **Request Body (DTO: `CollectOfflinePaymentDto`)**:
  ```json
  {
    "studentId": "std_2026_cse_042",
    "demandId": "dem_8821",
    "amount": 40000,
    "paymentMode": "DEMAND_DRAFT",
    "instrumentNumber": "DD-992019",
    "bankName": "Punjab National Bank",
    "branchName": "Connaught Place, New Delhi",
    "instrumentDate": "2026-09-08"
  }
  ```
- **Backend Flow**:
  1. Validates cashier session is open and active.
  2. Updates `FeeDemand` balance.
  3. Creates `Payment` record with physical instrument metadata.
  4. Creates `FeeLedger` credit entry.
  5. Generates official printable PDF Cashier Receipt with institutional seal.
- **Response (201 Created)**:
  ```json
  {
    "paymentId": "pay_off_99120",
    "receiptNumber": "OFF-REC-2026-4819",
    "amountCollected": 40000,
    "cashierName": "Robert Chen (Cashier Counter 2)"
  }
  ```
