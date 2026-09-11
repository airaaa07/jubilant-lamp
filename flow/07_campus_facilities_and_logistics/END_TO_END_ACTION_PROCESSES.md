# Module 07: Campus Facilities & Logistics — End-to-End Action Processes

> **Scope**: Backend request pipelines, DTO schemas, and database mutations for hostel room allocations, vacating requests, transport fleet/pass operations, library barcode circulation, and resource bookings.

---

## Action 1: Allocate Hostel Bed (`POST /api/hostel/allocations`)

- **HTTP Method & URL**: `POST /api/hostel/allocations`
- **Guards**: `JwtAuthGuard`, `RolesGuard('HostelWarden', 'InstAdmin', 'SuperAdmin')`
- **Request Body (DTO: `AllocateHostelBedDto`)**:
  ```json
  {
    "requestId": "hreq_8812",
    "roomId": "hroom_102",
    "bedNumber": "A",
    "commenceDate": "2026-09-15"
  }
  ```
- **Backend Flow**:
  1. Validates `roomId` has available capacity and `bedNumber` is not currently occupied.
  2. Queries `HostelConfig` for term fee amounts and caution deposit amounts.
  3. Executes atomic Prisma transaction:
     - Creates `HostelAllocation` row (`status: ACTIVE`).
     - Updates `HostelRoom.occupiedBeds = occupiedBeds + 1`.
     - Updates `HostelRequest.status = 'ALLOCATED'`.
     - Inserts `FeeDemand` for hostel rent and caution deposit.
- **Prisma Mutation**:
  ```prisma
  await prisma.$transaction(async (tx) => {
    const allocation = await tx.hostelAllocation.create({
      data: {
        studentId: req.studentId,
        hostelRoomId: dto.roomId,
        bedNumber: dto.bedNumber,
        startDate: new Date(dto.commenceDate),
        status: "ACTIVE"
      }
    });

    await tx.hostelRoom.update({
      where: { id: dto.roomId },
      data: { occupiedBeds: { increment: 1 } }
    });

    await tx.hostelRequest.update({
      where: { id: dto.requestId },
      data: { status: "ALLOCATED" }
    });

    // Generate fee demand for hostel
    await tx.feeDemand.create({
      data: {
        studentId: req.studentId,
        totalAmount: 35000,
        balanceAmount: 35000,
        paidAmount: 0,
        dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        status: "PENDING"
      }
    });

    return allocation;
  });
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "hall_9921",
    "bed": "102-A",
    "status": "ACTIVE",
    "commenceDate": "2026-09-15T00:00:00.000Z"
  }
  ```

---

## Action 2: Library Book Issue (`POST /api/library/issue`)

- **HTTP Method & URL**: `POST /api/library/issue`
- **Request Body**:
  ```json
  {
    "studentBarcode": "STD-2026-081",
    "bookCopyBarcode": "BK-99124-02"
  }
  ```
- **Backend Flow**:
  1. Verifies student loan limit (`maxLoans = 4`, current active loans < 4).
  2. Verifies student has no outstanding unpaid overdue fines $> ₹100$.
  3. Updates `BookCopy.status = 'ISSUED'`.
  4. Creates `BookIssue` record with `dueDate = now() + 14 days`.
- **Response (201 Created)**:
  ```json
  {
    "issueId": "bissue_0041",
    "bookTitle": "Clean Code",
    "dueDate": "2026-09-25T18:00:00.000Z",
    "activeLoanCount": 3
  }
  ```
