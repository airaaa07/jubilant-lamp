# Action Lifecycle Manual: Fee Billing, Revenue & Payments

## Action 4.1: Fee Structure Setup & Demand Generation

### 1. Fee Structure Definition
- **Role**: Finance Officer / Admin
- **Screen**: `FeesPage.tsx` / `ProgramFeeManager.tsx`
- **Input**: Programme, Batch, Term, Fee Heads breakdown (Tuition: ₹50,000, Lab: ₹5,000, Examination: ₹3,000, Library: ₹2,000, Due Date: `2026-10-15`).
- **Endpoint**: `POST /api/fee/structures` -> saved in `fee_structures` & `fee_structure_items`.

### 2. Bulk Demand Generation
- Finance clicks **Generate Demands** on `FeesPage.tsx`.
- Calls `POST /api/fee/ledger/generate` with `{ batchTermId }`.
- System creates `fee_demands` for all enrolled active students with status `PENDING`.
- Alternatively, automated nightly cron `@Cron('0 2 * * *')` executes `RecurringBillingService.processDailyBilling` to scan and generate missing term demands.

---

## Action 4.2: Online Payment via Razorpay Gateway & Webhook Reconciliation

### 1. User Action
- **Screen**: `FeesPage.tsx` (Student View).
- Student clicks **Pay Online** next to pending demand `DEM-2026-4891`.

### 2. Order Creation
- Frontend invokes `POST /api/fee/demands/:id/create-order`.
- Backend interacts with Razorpay API, creates order with receipt string, returns `{ orderId, amount, currency: 'INR', keyId }`.

### 3. Razorpay Checkout & Webhook
- Razorpay modal opens on client; student completes payment via UPI / Card / NetBanking.
- Razorpay sends server-to-server webhook `POST /api/fee/webhooks/razorpay` containing `razorpay_order_id`, `razorpay_payment_id`, and `razorpay_signature`.
- Backend verifies cryptographic HMAC SHA256 signature using `RAZORPAY_WEBHOOK_SECRET`.

### 4. Database Mutations & Receipt Generation
- `prisma.feeDemand.update(...)` setting status = `PAID`, `paidAt = now()`.
- `prisma.feePayment.create(...)` creating receipt record with auto-incremented receipt number `REC-2026-00981`.
- `prisma.studentLedger.create(...)` recording credit transaction.
- Generates official PDF receipt for instant download via `GET /api/fee/payments/receipt/:receiptNo`.

---

## Action 4.3: Scholarships, Waivers & Deposit Refunds

### 1. Scholarships & Waivers
- Student submits fee waiver request via `POST /api/fee/waivers`.
- Admin reviews request on `FeesPage.tsx` (Waivers tab).
- Admin clicks **Approve** -> `PATCH /api/fee/waivers/:id/approve` -> recalculates remaining fee demand amount.

### 2. Deposit Refund Flow
- Student checks refund eligibility via `GET /api/fee/deposit-refund/eligibility`.
- Student inputs bank details (Account No, IFSC, Account Holder) -> `POST /api/fee/deposit-refund`.
- Finance approves refund -> system generates payout transaction and updates deposit ledger.
