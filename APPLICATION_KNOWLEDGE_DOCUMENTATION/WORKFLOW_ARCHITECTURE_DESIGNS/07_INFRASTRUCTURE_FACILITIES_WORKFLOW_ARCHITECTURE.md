# Technical Workflow Architecture: Infrastructure & Facilities

## Overview
This document details the end-to-end technical workflow architecture, sequence diagrams, state machines, and background cleanup jobs for Hostel room allocation, Warden gate passes, Transport route passes, and Library circulation.

---

## 🔄 End-to-End Sequence Diagram: Library Circulation & Reservation

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student
    actor Librarian as Librarian
    participant LibC as LibraryController
    participant LibS as LibraryService
    participant Cron as LibraryCron (Midnight)
    participant DB as PostgreSQL Database

    Student->>LibC: POST /api/v1/library/reservations (Hold Book)
    LibS->>DB: Check Book Availability & Active Reservations
    LibS->>DB: INSERT into book_reservations (status: "ACTIVE", expires_at: 2 Days)
    LibS-->>Student: Reservation Confirmed (Pick up within 48h)

    note over Cron,LibS: Midnight Cleanup Execution (Case A: Uncollected Book)
    Cron->>LibS: cleanupExpiredReservations()
    LibS->>DB: Query book_reservations WHERE expires_at < NOW() AND status = 'ACTIVE'
    LibS->>DB: UPDATE book_reservations status = "EXPIRED"
    LibS->>DB: UPDATE book_copies status = "AVAILABLE"

    note over Librarian,LibS: Case B: Student Picks Up Book at Library Desk
    Librarian->>LibC: POST /api/v1/library/loans/issue (Scan Student Card & Book Barcode)
    LibS->>DB: UPDATE book_reservations status = "FULFILLED"
    LibS->>DB: INSERT into book_loans (due_date: +14 Days, status: "ISSUED")
    LibS->>DB: UPDATE book_copies status = "CHECKED_OUT"

    note over Student,LibS: Book Return & Fine Calculation
    Librarian->>LibC: POST /api/v1/library/loans/return (Scan Book)
    LibS->>LibS: Calculate Overdue Days & Fine Amount
    opt Overdue Days > 0
        LibS->>DB: INSERT into library_fines (amount, status: "UNPAID")
        LibS->>DB: Create Fee Demand for Fine
    end
    LibS->>DB: UPDATE book_loans status = "RETURNED", return_date = NOW()
    LibS->>DB: UPDATE book_copies status = "AVAILABLE"
```

---

## 🔀 Warden Hostel Gate Pass State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> SUBMITTED: Student Requests Gate Pass
    SUBMITTED --> WARDEN_APPROVED: Warden Grants Outing Request
    SUBMITTED --> REJECTED: Warden Denies Request
    WARDEN_APPROVED --> CHECKED_OUT: Security Guard Scans QR at Gate
    CHECKED_OUT --> CHECKED_IN: Security Guard Scans QR upon Return
    CHECKED_OUT --> OVERDUE_RETURN: Return Time Exceeded
    OVERDUE_RETURN --> CHECKED_IN: Late Return Recorded & Warden Notified
    CHECKED_IN --> [*]
    REJECTED --> [*]
```

---

## 📊 Database Mutations across Infrastructure Entities

1. **Hostel Allocation (`hostel_allocations`)**:
   - `INSERT INTO hostel_allocations (student_id, room_id, bed_number, start_date, status = 'ALLOCATED')`
   - Updates `hostel_rooms.occupied_beds += 1`.
2. **Transport Pass (`transport_passes`)**:
   - Linked to `route_id`, `stop_id`, and `fee_demand_id`. Validated upon scanning bus pass.
