# Institutional Analytics & Intelligence — UI Click Flows & Interaction Walkthroughs

```
========================================================================================================================
MODULE 14: INSTITUTIONAL ANALYTICS & EXECUTIVE INTELLIGENCE
DOCUMENT: UI_CLICK_FLOWS.md
TARGET PERSONAS: CHANCELLORS, PRESIDENTS, REGISTRARS, FINANCE CONTROLLERS, DEANS, ACCREDITATION DIRECTORS
UI ROUTES: /analytics, /dashboard, /analytics/exec
========================================================================================================================
```

---

## Screen 01: Executive Cockpit (`/analytics/exec`)

### 1.1 Header & Scope Filtering Controls
- **User Role**: `SuperAdmin`, `UnivAdmin`, `President`, `Chairperson`, `Registrar`, `Finance Head`, `Controller of Examinations` (`EXEC_ROLES`).
- **Campus Selector**: Dropdown listing all constituent campuses (`All Campuses`, `Main College of Tech`, `City Business School`).
- **Academic Year Selector**: `2026-2027 (Active)`, `2025-2026`, `2024-2025`.
- **Top 4 Macro Metric KPI Cards**:
  1. **Total Student Enrollment**: Displayed with year-over-year growth badge (e.g. `12,450 (+8.4% YoY)`).
  2. **Total Revenue Collected vs Budget**: Displayed as currency and progress percentage (e.g. `₹48.2 Cr / ₹52.0 Cr (92.7%)`).
  3. **Institutional Pass Percentage**: High-contrast grade health indicator (e.g. `88.4%`).
  4. **Average Faculty-Student Ratio (FSR)**: Metric badge compliant with AICTE/UGC standards (e.g. `1:15.2`).

### 1.2 The 4 Executive Intelligence Tabs

#### Tab A: Institutional Overview (`#overview`)
- **Enrollment Funnel Chart**: Sankey diagram tracking Lead Acquisition $\to$ Applications Received $\to$ Scrutiny Cleared $\to$ Offers Released $\to$ Matriculated Enrolled.
- **Campus Demographic Diversity Matrix**: Geographical student distribution map, category representation (General, OBC, SC, ST, EWS), and gender balance ratio (e.g. 52% Male, 48% Female).

#### Tab B: Academic Health & Pedagogy (`#academic`)
- **Attendance Risk Radar**: Identifies student cohorts with attendance shortages below the 75% examination threshold.
- **Grade Distribution Heatmap**: Relative letter grade spread (`O`, `A+`, `A`, `B+`, `B`, `C`, `F`) broken down by department.
- **CBE Exam Completion Velocity**: Average duration taken to complete computer-based tests vs allotted time.

#### Tab C: Fiscal Collection & Receivables (`#finance`)
- **Real-Time Cashiering Stream**: Hourly and daily fee collection velocity across online Razorpay transactions and offline cashier desks.
- **Defaulter Aging Histogram**: Receivables categorized into aging buckets (`0–30 Days`, `31–60 Days`, `61–90 Days`, `90+ Days`).
- **Caution Deposit Liability Ledger**: Total security deposit reserve held vs pending refund claims for departing students.

#### Tab D: Infrastructure & Campus Logistics (`#logistics`)
- **Hostel Bed Occupancy**: Visual gauges across all residential blocks (Capacity vs Occupied vs Under Maintenance).
- **Transport Fleet Utilization**: Passenger count per route vs bus seating limits.
- **Library Circulation Index**: Top 10 most borrowed textbooks and average loan turnover rates.

---

## Screen 02: Personal Performance & Workload Analytics (`/analytics/me`)

- **User Role**: `TeachingFaculty`, `Professor`, `Lecturer`
- **Widgets**:
  - **Weekly Teaching Workload**: Actual classroom contact hours delivered vs AICTE statutory minimum (e.g. 16 hours/week for Assistant Professors).
  - **Syllabus Coverage Tracker**: Progress percentage across curriculum units per subject.
  - **Class Attendance Health**: Real-time average attendance across assigned sections.
  - **Evaluation Completion Rate**: Count of CIA test scripts graded vs pending.

---
```
========================================================================================================================
END OF DOCUMENT: MODULE 14 UI_CLICK_FLOWS.md
========================================================================================================================
```
