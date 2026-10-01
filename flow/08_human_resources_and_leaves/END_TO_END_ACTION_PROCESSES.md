# Module 08: Human Resources & Leaves — End-to-End Action Processes

> **Scope**: Request and response protocols, DTO structures, controllers, and Prisma mutations for staff profiles, leave applications, multi-tier approvals, balance deductions, and institutional holiday calendars.

---

## Action 1: Submit Leave Application (`POST /api/hr/leaves`)

- **HTTP Method & URL**: `POST /api/hr/leaves`
- **Guards**: `JwtAuthGuard`
- **Request Body (DTO: `CreateLeaveDto`)**:
  ```json
  {
    "leaveTypeId": "lt_casual_01",
    "startDate": "2026-09-18",
    "endDate": "2026-09-20",
    "reason": "Attending IEEE Research Conference",
    "substituteStaffId": "stf_4412",
    "attachmentDocumentId": "doc_conf_invite_09"
  }
  ```
- **Backend Flow**:
  1. Computes total chargeable working days (queries `HolidayCalendar` to exclude gazetted holidays).
  2. Queries `LeaveBalance` for caller and `leaveTypeId`.
  3. Verifies `availableBalance >= requestedDays`.
  4. Creates `LeaveApplication` record with status `PENDING_HOD_APPROVAL`.
  5. Pushes email notification to substitute faculty and department HOD.
- **Prisma Mutation**:
  ```prisma
  const application = await prisma.leaveApplication.create({
    data: {
      staffId: req.user.staffId,
      leaveTypeId: dto.leaveTypeId,
      startDate: new Date(dto.startDate),
      endDate: new Date(dto.endDate),
      totalDays: 3,
      reason: dto.reason,
      substituteStaffId: dto.substituteStaffId,
      attachmentDocId: dto.attachmentDocumentId,
      status: "PENDING_HOD_APPROVAL"
    }
  });
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": "leave_app_9912",
    "status": "PENDING_HOD_APPROVAL",
    "totalDays": 3,
    "appliedAt": "2026-09-11T12:00:00.000Z"
  }
  ```

---

## Action 2: HOD Sanction & Leave Balance Deduction (`PATCH /api/hr/leaves/:id/approve`)

- **HTTP Method & URL**: `PATCH /api/hr/leaves/:id/approve`
- **Guards**: `JwtAuthGuard`, `RolesGuard('HOD', 'InstAdmin', 'SuperAdmin')`
- **Request Body**:
  ```json
  {
    "remarks": "Approved. Duty leave sanctioned with conference duty certificate requirement."
  }
  ```
- **Prisma Database Mutation**:
  ```prisma
  await prisma.$transaction(async (tx) => {
    const leave = await tx.leaveApplication.findUnique({
      where: { id },
      include: { staff: true }
    });

    await tx.leaveApplication.update({
      where: { id },
      data: {
        status: "APPROVED",
        reviewedBy: req.user.id,
        reviewRemarks: dto.remarks,
        reviewedAt: new Date()
      }
    });

    // Deduct from LeaveBalance
    await tx.leaveBalance.update({
      where: {
        staffId_leaveTypeId_year: {
          staffId: leave.staffId,
          leaveTypeId: leave.leaveTypeId,
          year: new Date().getFullYear()
        }
      },
      data: {
        consumedDays: { increment: leave.totalDays },
        remainingDays: { decrement: leave.totalDays }
      }
    });
  });
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "status": "APPROVED",
    "deductedDays": 3
  }
  ```
