# Module 03: Academics, Curriculum & Timetable — Technical Architecture

> **Scope**: Timetable scheduling algorithms, slot conflict resolution logic, subject pool elective distribution engine, attendance computation formulas, and term completion state machines.

---

## 1. Timetable Scheduling & Collision Detection Engine

The timetable system prevents three types of resource conflicts across physical and academic entities:
1. **Teacher Conflict**: A faculty member cannot be scheduled in two distinct rooms or sections during the same `TimeSlot`.
2. **Room Conflict**: A physical classroom or laboratory cannot host multiple sections concurrently (unless explicitly configured as a shared lecture hall).
3. **Section Conflict**: A student section cannot have overlapping lecture slots.

```mermaid
flowchart TD
    SlotRequest["Create/Update TimetableEntry<br/>{ timeSlotId, staffSubjectId, roomId, sectionId }"] --> QueryActive["Query Existing Overlapping Entries for timeSlotId"]
    
    QueryActive --> CheckTeacher{"Staff busy in timeSlot?"}
    CheckTeacher -->|Yes| ConflictTeacher["Throw ConflictException: Teacher already booked"]
    CheckTeacher -->|No| CheckRoom{"Room occupied in timeSlot?"}
    
    CheckRoom -->|Yes| ConflictRoom["Throw ConflictException: Room already booked"]
    CheckRoom -->|No| CheckSection{"Section busy in timeSlot?"}
    
    CheckSection -->|Yes| ConflictSection["Throw ConflictException: Section already has lecture"]
    CheckSection -->|No| CommitEntry["Prisma: timetableEntry.create() -> 201 Created"]
```

---

## 2. Elective Subject Pool Architecture

```mermaid
erDiagram
    BatchTerm ||--o{ SubjectPool : "defines elective groups in"
    SubjectPool ||--o{ SubjectPoolMember : "contains candidate"
    SubjectPoolMember ||--|| BatchTermSubject : "references course subject"
    Student ||--o{ StudentTermElection : "locks choices in"
    StudentTermElection ||--o{ StudentSubjectEnrollment : "generates enrollments"

    SubjectPool {
        string id PK
        string batchTermId FK
        string name
        int minCreditsRequired
        int maxCreditsAllowed
        datetime electionStartDate
        datetime electionEndDate
        boolean isLocked
    }

    SubjectPoolMember {
        string id PK
        string subjectPoolId FK
        string batchTermSubjectId FK
        int seatCapacity
        int currentElectedCount
    }
```

---

## 3. Attendance Calculation & Eligibility Rule Model

Attendance is computed dynamically and aggregated in `SubjectAttendanceSummary`.

$$\text{Attendance Percentage} = \left(\frac{\text{Lectures Attended} + \text{Approved Medical Leaves}}{\text{Total Conducted Lectures}}\right) \times 100$$

```mermaid
stateDiagram-v2
    [*] --> AttendingLectures
    AttendingLectures --> Eligible: Overall Attendance >= 75%
    AttendingLectures --> CondonationRequired: Attendance between 65% and 74.9%
    AttendingLectures --> Ineligible: Attendance < 65%

    CondonationRequired --> FeePaid: Student applies & pays Condonation Fee
    FeePaid --> Eligible: HOD approves medical/extenuating waiver
    CondonationRequired --> Ineligible: Window lapses without waiver

    Eligible --> AdmitCardIssued: Exam Hall Ticket Released
    Ineligible --> ExamAdmitCardIneligibility: Blocked from Exam Hall Ticket
```
