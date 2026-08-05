# UI Design Specs: Fee & Financial Management Screens

## Pages Covered
- `FeesPage.tsx`
- `ProgramFeeManager.tsx`
- `ResourceFeeManager.tsx`
- Razorpay Payment Gateway Modal UI

---

## 1. Fee Management & Ledger Console (`FeesPage.tsx`)

### Screen Purpose
Central financial management screen for defining fee structures, generating head-wise fee demands, reviewing student payment ledgers, processing deposit refunds, and integrating Razorpay payment processing.

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Fee Management & Financial Ledger                           │
│  [ Fee Demands ] [ Fee Structures ] [ Payment Ledger ]       │
├──────────────────────────────────────────────────────────────┤
│  Summary Widgets                                             │
│  ┌────────────────────┐ ┌────────────────────┐ ┌───────────┐ │
│  │ Total Billing      │ │ Collected Fees     │ │ Overdue   │ │
│  │ $12,450,000        │ │ $10,800,000 (86%)  │ │ $1,650,000│ │
│  └────────────────────┘ └────────────────────┘ └───────────┘ │
│                                                              │
│  Fee Demands Table                             [ + Demand ]  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Demand ID │ Student Name │ Term   │ Amount  │ Status   │  │
│  ├───────────┼──────────────┼────────┼─────────┼──────────┤  │
│  │ DEM-10492 │ Alex Kim     │ Term 3 │ $2,500  │ PAID     │  │
│  │ DEM-10493 │ Sarah Chen   │ Term 3 │ $2,500  │ PENDING  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Summary Metrics Cards**: Glassmorphism stat widgets displaying Total Billed Amount, Total Collected Amount with progress bar, and Overdue Balance.
- **Demands Data Table**: Filterable table showing Demand ID, Student Roll Number, Fee Head Breakdown (Tuition, Library, Hostel), Due Date, Amount, and Status Pill (`PAID` green, `PARTIALLY_PAID` yellow, `PENDING` slate, `OVERDUE` red).
- **Razorpay Online Payment Modal**: Modal overlay displaying demand summary, Razorpay checkout button, instant payment receipt preview, and PDF download action.
