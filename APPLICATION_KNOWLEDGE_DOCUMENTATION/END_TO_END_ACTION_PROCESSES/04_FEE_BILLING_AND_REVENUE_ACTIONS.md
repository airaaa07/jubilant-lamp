# Action Lifecycle Manual: Fee Billing & Revenue Settlement

## Action 4.1: Daily 2:00 AM Automated Recurring Billing Cron Execution

### 1. Trigger & System Execution
- **Initiator**: NestJS Cron Scheduler (`@Cron('0 2 * * *')`)
- **Service**: `RecurringBillingService.processDailyBilling`
- **Execution Time**: 2:00 AM Daily

### 2. Backend Logic & Rule Evaluation
- Queries all active student profiles (`users.role == 'Student'` AND `users.isActive == true`).
- Matches student `batch_id` and current active `term_id` against `fee_structures`.
- Checks if a `FeeDemand` already exists for the student for the target term.
- If demand is missing: calculates head-wise breakdown (Tuition Fee + Development Fee + Lab Fee).

### 3. Database Transactions & Persistence
- `INSERT INTO fee_demands (id, user_id, term_id, amount = 2500, due_date = NOW() + 30 Days, status = 'PENDING')`
- `INSERT INTO fee_demand_items (demand_id, fee_head_id, amount)`
- `INSERT INTO fee_ledger (user_id, demand_id, transaction_type = 'DEBIT', amount = 2500, balance_after = 2500)`

### 4. Side Effects & Outcome
- Dispatches batch notification email (`"Term 3 Fee Invoice Issued - Due in 30 Days"`) to student and parent email addresses.
- Outstanding balance pill updated on student dashboard.

---

## Action 4.2: Student Razorpay Payment Checkout & Webhook Settlement

### 1. User Action & Frontend Trigger
- **User Role**: Student (`role: Student`) / Parent
- **Screen**: `FeesPage.tsx`
- **User Input**: Selects pending demand `DEM-10492` ($2,500), clicks **Pay Online via Razorpay**.

### 2. Order Creation Phase
- `POST /api/v1/fee/demands/DEM-10492/create-order`
- `FeeService` calls Razorpay API `orders.create({ amount: 250000, currency: "INR", receipt: "DEM-10492" })`.
- Returns `razorpayOrderId` (`order_Nf89a7sD0a8s`).

### 3. Payment Execution & Webhook Verification
- Student completes credit card / UPI payment inside Razorpay modal overlay.
- Razorpay sends HTTP POST webhook to `/api/v1/fee/webhooks/razorpay`:
  - Payload contains `razorpay_payment_id`, `razorpay_order_id`, `razorpay_signature`.
- `FeeService.verifySignature` verifies HMAC-SHA256 signature against `RAZORPAY_KEY_SECRET`.

### 4. Database Mutations (Atomic Transaction)
- `UPDATE fee_demands SET status = 'PAID', paid_at = NOW() WHERE id = 'DEM-10492'`
- `INSERT INTO payments (id, demand_id, razorpay_payment_id, amount = 2500, status = 'SUCCESS')`
- `INSERT INTO fee_ledger (user_id, payment_id, transaction_type = 'CREDIT', amount = 2500, balance_after = 0)`

### 5. Document & Final Outcome
- `DocumentsService.renderReceiptPDF` generates official fee receipt PDF -> Uploads to MinIO `generated-docs/receipts/REC-10492.pdf`.
- Fee demand status updated to `PAID` in green; receipt download button available on screen.
