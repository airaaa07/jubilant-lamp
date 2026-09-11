# Module 07: Campus Facilities & Logistics — Technical Architecture

> **Scope**: Resource reservation conflict engine, hostel occupancy state machines, transport fleet route capacity algorithms, and library circulation models.

---

## 1. Campus Facilities Entity Relationships

```mermaid
erDiagram
    Hostel ||--o{ HostelRoom : "contains"
    HostelRoom ||--o{ HostelAllocation : "allocates"
    Student ||--o{ HostelAllocation : "resides in"
    Student ||--o{ HostelRequest : "applies for"
    
    TransportRoute ||--o{ TransportVehicle : "serviced by"
    TransportRoute ||--o{ TransportPass : "issues passes for"
    Student ||--o{ TransportPass : "holds"

    Book ||--o{ BookCopy : "stocks physical"
    BookCopy ||--o{ BookIssue : "circulates via"
    Student ||--o{ BookIssue : "borrows"

    Room ||--o{ RoomBooking : "booked via"
    Equipment ||--o{ ResourceReservation : "reserved via"
```

---

## 2. Resource Reservation Conflict Engine

When an auditorium, seminar hall, laboratory, or bus is reserved, the reservation engine checks against both scheduled class timetables and ad-hoc event bookings.

```mermaid
flowchart TD
    Req["Reservation Request<br/>{ resourceId, startTime, endTime, purpose }"] --> CheckTimetable{"Does Resource clash with Academic TimetableEntry?"}
    CheckTimetable -->|Yes| ConflictA["Reject: Class in session during requested time"]
    CheckTimetable -->|No| CheckExistingBooking{"Does Resource clash with existing approved RoomBooking?"}
    CheckExistingBooking -->|Yes| ConflictB["Reject: Already booked by another department"]
    CheckExistingBooking -->|No| CheckMaintenance{"Is Resource flagged under maintenance?"}
    CheckMaintenance -->|Yes| ConflictC["Reject: Resource undergoing maintenance"]
    CheckMaintenance -->|No| CommitBooking["Commit Reservation: Status PENDING_HOD_APPROVAL"]
```
