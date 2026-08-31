# Action Lifecycle Manual: Infrastructure, Hostel, Transport & Library

## Action 7.1: Hostel Allocation, Room Rates & Waitlist Lifecycle

### 1. Student Application & Waitlisting
- **Screen**: `HostelPage.tsx` (Student View).
- Student selects hostel block, room type preference (Single/Double/Triple), and mess package.
- `POST /api/hostel/requests` -> creates hostel request record.
- If rooms are full, request is placed in `GET /api/hostel/requests/waitlist` with queue number.

### 2. Warden Allocation & Confirmation
- Warden views `HostelPage.tsx` room matrix.
- Selects vacant bed in room `A-204` -> `POST /api/hostel/allocations` (room status becomes `BLOCKED`).
- Student reviews allocation, clicks **Confirm** -> `PATCH /api/hostel/allocations/:id/confirm`.
- System triggers hostel fee demand creation via `FeeService`.

### 3. Room Release & Prorated Refund
- Student vacates room -> Warden clicks **Release Room** -> `PATCH /api/hostel/allocations/:id/release`.
- `HostelRefundService` calculates unused days and generates prorated refund entry.

---

## Action 7.2: Transport Route Management & Bus Pass Issuance

### 1. Route & Stop Setup
- **Screen**: `TransportPage.tsx`.
- Admin defines route (`Route 12 - North Campus`), stops with pickup times, and assigns bus vehicle (`POST /api/transport/routes`, `POST /api/transport/stops`).

### 2. Student Bus Pass
- Student enrolls in route via `POST /api/transport/enrollments`.
- Transport fee demand generated.
- After payment, system generates digital bus pass with QR code, visible on `StudentProfilePage.tsx` (Transport tab).

---

## Action 7.3: Library Book Circulation, Fines & Reservation

### 1. Issue & Return
- **Screen**: `LibraryPage.tsx`.
- Librarian scans student barcode and book ISBN -> `POST /api/library/loans/issue`.
- Upon return, librarian clicks **Return** -> `POST /api/library/loans/return`.

### 2. Overdue Fine Scheduler
- `LibrarySchedulerService` runs daily cron:
  - Scans overdue loans (`dueDate < now()`).
  - Calculates fine per day (e.g. ₹5/day).
  - Posts fine charge to student ledger.
