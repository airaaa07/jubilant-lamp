# UI Design Specs: Fee & Financial Management Screens

## Pages Covered
- `FeesPage.tsx`
- `ProgramFeeManager.tsx`
- `ResourceFeeManager.tsx`
- `ChargeFeeModal.tsx`
- Razorpay Payment Gateway Modal UI

---

## 1. Fee Management & Ledger Console (`FeesPage.tsx`)

### Screen Purpose
Central financial management screen (150KB) for defining fee structures, generating head-wise fee demands, reviewing student payment ledgers, managing scholarships/waivers/reimbursements, processing deposit refunds, recurring billing, and Razorpay payment integration.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Fee Management & Financial Ledger                           │
│  [Demands] [Structures] [Ledger] [Heads] [Scholarships]     │
│  [Waivers] [Reimbursements] [Reports] [Deposit Refunds]     │
├──────────────────────────────────────────────────────────────┤
│  Summary Widgets                                             │
│  ┌────────────────────┐ ┌────────────────────┐ ┌───────────┐│
│  │ Total Billing      │ │ Collected Fees     │ │ Overdue   ││
│  │ ₹12,450,000       │ │ ₹10,800,000 (86%) │ │ ₹1,650,000││
│  └────────────────────┘ └────────────────────┘ └───────────┘│
│                                                              │
│  Fee Demands Table                             [ + Demand ]  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Demand ID │ Student Name │ Term   │ Amount  │ Status   │  │
│  ├───────────┼──────────────┼────────┼─────────┼──────────┤  │
│  │ DEM-10492 │ Alex Kim     │ Term 3 │ ₹2,500  │ PAID     │  │
│  │ DEM-10493 │ Sarah Chen   │ Term 3 │ ₹2,500  │ PENDING  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Summary Metrics Cards**: Glassmorphism stat widgets — Total Billed, Collected (with progress bar), Overdue Balance.
- **Demands Data Table**: Filterable table with Demand ID, Student Roll, Fee Head Breakdown, Due Date, Amount, Status Pill (`PAID` green, `PARTIALLY_PAID` yellow, `PENDING` slate, `OVERDUE` red).
- **Charge Fee Modal** (`ChargeFeeModal.tsx`): Quick-charge modal for manual fee demand creation.
- **Razorpay Payment Modal**: Checkout overlay → receipt preview → PDF download.

### Fee Structures Sub-Module
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/structures` | Create fee structure |
| GET | `/api/fee/structures` | List fee structures |
| GET | `/api/fee/structures/:id` | Get structure detail |
| PATCH | `/api/fee/structures/:id` | Update structure |
| DELETE | `/api/fee/structures/:id` | Deactivate structure |

### Fee Heads Sub-Module
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/heads` | Create fee head |
| GET | `/api/fee/heads` | List fee heads |
| PATCH | `/api/fee/heads/:id` | Update fee head |

### Ledger & Payments
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/ledger/generate` | Generate ledger entries |
| GET | `/api/fee/ledger/student/:studentId` | Student ledger view |
| PATCH | `/api/fee/ledger/:id/late-fee` | Apply late fee |
| POST | `/api/fee/payments` | Record payment |
| GET | `/api/fee/payments/receipt/:receiptNo` | Get receipt data |
| GET | `/api/fee/payments/student/:studentId` | Student payment history |

### Scholarships
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/scholarships` | Create scholarship |
| GET | `/api/fee/scholarships` | List scholarships |
| PATCH | `/api/fee/scholarships/:id` | Update scholarship |

### Fee Waivers
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/waivers` | Request waiver |
| PATCH | `/api/fee/waivers/:id/approve` | Approve waiver |
| PATCH | `/api/fee/waivers/:id/reject` | Reject waiver |
| GET | `/api/fee/waivers` | List waivers |

### Reimbursements
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/reimbursements` | Create reimbursement |
| PATCH | `/api/fee/reimbursements/:id/receive` | Mark received |
| GET | `/api/fee/reimbursements` | List reimbursements |

### Reports
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/fee/reports/collection` | Collection summary report |
| GET | `/api/fee/reports/defaulters` | Defaulters list report |

### Deposit Refunds
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/fee/deposit-refund/eligibility` | Check refund eligibility |
| GET | `/api/fee/deposit-refund/mine` | My refund applications |
| POST | `/api/fee/deposit-refund` | Initiate refund request (with bank details) |

### Recurring Billing
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/fee/recurring/run` | Trigger recurring billing cycle |

---

## 2. Program Fee Manager (`ProgramFeeManager.tsx`)

### Screen Purpose
49KB dedicated manager for configuring programme-level fee structures — mapping fee heads to specific programmes, batches, and terms with amount schedules.

### Layout & Component Specs
- **Programme-Fee Matrix**: Grid showing programmes vs fee heads with amount cells
- **Batch Term Scoping**: Filter by batch and term to set term-specific amounts
- **Bulk Edit Mode**: Multi-cell selection for batch amount updates

---

## 3. Resource Fee Manager (`ResourceFeeManager.tsx`)

### Screen Purpose
Manager for facility-based fee configuration (Hostel, Transport, Library) — resource-specific fee heads with capacity-aware pricing.

---

## 4. Backend Services

### `fee.service.ts`
Core fee processing — demand generation, payment recording, Razorpay order creation & webhook verification, receipt PDF generation, ledger entry creation.

### `program-deposit-refund.service.ts`
Handles deposit refund eligibility checking, refund application processing, bank detail validation, refund approval workflows.

### `recurring-billing.service.ts`
NestJS `@Cron('0 2 * * *')` daily billing — scans active students, matches batch/term against fee structures, generates missing demands with head-wise breakdown, dispatches notification emails.
