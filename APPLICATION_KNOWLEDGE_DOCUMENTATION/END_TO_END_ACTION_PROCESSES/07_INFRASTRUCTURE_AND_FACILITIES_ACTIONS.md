# Action Lifecycle Manual: Infrastructure & Facilities

## Action 7.1: Hostel Bed Allocation Execution

### 1. User Action & Frontend Trigger
- **User Role**: Hostel Warden (`role: InstAdmin` / Warden)
- **Screen**: `HostelPage.tsx`
- **User Input**: Selects Student (Alex Kim), Hostel Block A, Room 302, Bed 2, Start Date (Fall 2024).
- **Trigger**: Click **Confirm Room & Bed Allocation**.

### 2. API & Backend Logic (`HostelService.allocateBed`)
- `POST /api/v1/hostel/allocations`
- Checks `hostel_rooms.capacity` vs current `occupied_beds`.
- Creates `HostelAllocation` record.
- Triggers Hostel Mess Fee demand creation via `FeeService`.

### 3. Database Mutations
- `INSERT INTO hostel_allocations (id, student_id, room_id, bed_number, start_date, status = 'ALLOCATED')`
- `UPDATE hostel_rooms SET occupied_beds = occupied_beds + 1 WHERE id = :roomId`
- `INSERT INTO fee_demands (user_id, amount = 800, fee_head_id = 'HEAD_HOSTEL')`

### 4. Outcome
- Bed 2 marked occupied in green on Room Matrix view. Student receives hostel room allocation pass.

---

## Action 7.2: Library Book Circulation Issue & Return

### 1. User Action & Frontend Trigger
- **User Role**: Librarian (`role: InstAdmin` / Librarian)
- **Screen**: `LibraryPage.tsx`
- **User Input**: Scans Student ID barcode (`STU-2024-042`) and Book Copy ISBN (`978-0131103627`).
- **Trigger**: Click **Issue Book Loan**.

### 2. Backend Execution (`LibraryService.issueBook`)
- `POST /api/v1/library/loans/issue`
- Checks student max loan limit (e.g. Max 3 active loans).
- Calculates due date (+14 Days).

### 3. Database Mutations
- `INSERT INTO book_loans (student_id, book_copy_id, issue_date = NOW(), due_date = NOW() + 14 Days, status = 'ISSUED')`
- `UPDATE book_copies SET status = 'CHECKED_OUT' WHERE id = :copyId`

### 4. Book Return & Fine Action
- Upon return, if `NOW() > due_date`:
  - `UPDATE book_loans SET return_date = NOW(), status = 'RETURNED'`
  - `INSERT INTO library_fines (student_id, loan_id, amount = overdueDays * $1/day, status = 'UNPAID')`
  - `UPDATE book_copies SET status = 'AVAILABLE'`
