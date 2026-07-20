# University ERP - API Reference

## Overview

The API is a **REST API** built with NestJS, following standard REST conventions. All endpoints are prefixed with `/api` and require JWT authentication unless marked as public.

## Base URL

```
Development: http://localhost:3000/api
Production: https://[domain]/api
```

## Authentication

### JWT Authentication

Most endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Public Endpoints

The following endpoints are public (no authentication required):

- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `GET /api/auth/captcha`
- `POST /api/auth/register`
- `POST /api/auth/register/send-otp`
- `POST /api/auth/register/verify-otp`
- `POST /api/auth/register/send-email-otp`
- `POST /api/auth/register/verify-email-otp`
- `GET /api/auth/public/registration-config`
- `POST /api/auth/forgot-password-sms`
- `POST /api/auth/reset-password-sms`

## Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```

### Error Response

```json
{
  "success": false,
  "message": "Error message",
  "statusCode": 400,
  "error": "Bad Request"
}
```

## Rate Limiting

- **Default**: 300 requests per minute per IP
- **Login**: 5 requests per minute
- **OTP Send**: 3 requests per minute
- **OTP Verify**: 10 requests per minute

## API Endpoints

### Authentication Module (`/api/auth`)

#### POST `/api/auth/login`
- **Description**: User login
- **Body**: `{ email, password }`
- **Response**: `{ accessToken, refreshToken, user }`
- **Rate Limit**: 5/min

#### POST `/api/auth/refresh`
- **Description**: Refresh access token
- **Body**: `{ refreshToken }`
- **Response**: `{ accessToken }`

#### POST `/api/auth/logout`
- **Auth**: Required
- **Description**: User logout
- **Response**: `{ success: true }`

#### GET `/api/auth/me`
- **Auth**: Required
- **Description**: Get current user profile
- **Response**: `{ user }`

#### PATCH `/api/auth/me`
- **Auth**: Required
- **Description**: Update current user profile
- **Body**: `{ salutation?, firstName?, lastName?, ... }`
- **Response**: `{ user }`

#### GET `/api/auth/captcha`
- **Description**: Generate CAPTCHA
- **Response**: `{ svg, token }`

#### POST `/api/auth/register`
- **Description**: User registration
- **Body**: Registration DTO
- **Response**: `{ success: true }`

#### GET `/api/auth/public/registration-config`
- **Description**: Get registration configuration
- **Response**: `{ emailRequired, smsRequired }`

#### POST `/api/auth/register/send-otp`
- **Description**: Send mobile OTP for registration
- **Body**: `{ phone }`
- **Rate Limit**: 3/min

#### POST `/api/auth/register/verify-otp`
- **Description**: Verify mobile OTP
- **Body**: `{ phone, code }`
- **Rate Limit**: 10/min

#### POST `/api/auth/register/send-email-otp`
- **Description**: Send email OTP for registration
- **Body**: `{ email }`
- **Rate Limit**: 3/min

#### POST `/api/auth/register/verify-email-otp`
- **Description**: Verify email OTP
- **Body**: `{ email, code }`
- **Rate Limit**: 10/min

### Master Data Module (`/api/master-data`)

#### Universities (`/api/master-data/universities`)

##### GET `/api/master-data/universities`
- **Auth**: Required, Scope: university
- **Query**: `page, limit, search`
- **Response**: `{ data: University[], meta }`

##### GET `/api/master-data/universities/:id`
- **Auth**: Required, Scope: university
- **Response**: `{ data: University }`

##### POST `/api/master-data/universities`
- **Auth**: Required, Scope: university
- **Body**: CreateUniversityDto
- **Response**: `{ data: University }`

##### PATCH `/api/master-data/universities/:id`
- **Auth**: Required, Scope: university
- **Body**: UpdateUniversityDto
- **Response**: `{ data: University }`

##### DELETE `/api/master-data/universities/:id`
- **Auth**: Required, Scope: university
- **Response**: `{ data: University }`

#### Institutes (`/api/master-data/institutes`)

##### GET `/api/master-data/institutes`
- **Auth**: Required
- **Query**: `page, limit, search`
- **Response**: `{ data: Institute[], meta }`

##### GET `/api/master-data/institutes/:id`
- **Auth**: Required
- **Response**: `{ data: Institute }`

##### POST `/api/master-data/institutes`
- **Auth**: Required
- **Body**: CreateInstituteDto
- **Response**: `{ data: Institute }`

##### PATCH `/api/master-data/institutes/:id`
- **Auth**: Required
- **Body**: UpdateInstituteDto
- **Response**: `{ data: Institute }`

##### DELETE `/api/master-data/institutes/:id`
- **Auth**: Required
- **Response**: `{ data: Institute }`

#### Departments (`/api/master-data/departments`)

##### GET `/api/master-data/departments`
- **Auth**: Required
- **Query**: `page, limit, instituteId`
- **Response**: `{ data: Department[], meta }`

##### GET `/api/master-data/departments/:id`
- **Auth**: Required
- **Response**: `{ data: Department }`

##### POST `/api/master-data/departments`
- **Auth**: Required
- **Body**: CreateDepartmentDto
- **Response**: `{ data: Department }`

##### PATCH `/api/master-data/departments/:id`
- **Auth**: Required
- **Body**: UpdateDepartmentDto
- **Response**: `{ data: Department }`

##### DELETE `/api/master-data/departments/:id`
- **Auth**: Required
- **Response**: `{ data: Department }`

### Admissions Module (`/api/admissions`)

#### GET `/api/admissions/start-requests`
- **Auth**: Required
- **Description**: List start-admissions requests
- **Response**: `{ data: StartRequest[] }`

#### POST `/api/admissions/start-requests`
- **Auth**: Required
- **Description**: Raise start-admissions request
- **Body**: `{ batchId, requestedSeats, note? }`
- **Response**: `{ data: StartRequest }`

#### PATCH `/api/admissions/start-requests/:id/review`
- **Auth**: Required
- **Description**: Review start-admissions request
- **Body**: `{ decision, approvedSeats?, reviewNote? }`
- **Response**: `{ data: StartRequest }`

#### GET `/api/admissions/applications`
- **Auth**: Required
- **Description**: List admission applications
- **Query**: `status, page, limit`
- **Response**: `{ data, meta }`

#### GET `/api/admissions/merit-list/:batchId`
- **Auth**: Required
- **Description**: Get merit list for batch
- **Response**: `{ data: MeritList[] }`

#### POST `/api/admissions/merit-list/:batchId/offer`
- **Auth**: Required
- **Description**: Bulk offer seats
- **Body**: `{ instanceIds[] }`
- **Response**: `{ data }`

#### POST `/api/admissions/merit-list/:batchId/reject`
- **Auth**: Required
- **Description**: Bulk reject applications
- **Body**: `{ instanceIds?, reason? }`
- **Response**: `{ data }`

### Attendance Module (`/api/attendance`)

#### GET `/api/attendance/students`
- **Auth**: Required
- **Description**: Get student attendance
- **Query**: `studentId, courseId, date, session`
- **Response**: `{ data: StudentAttendance[] }`

#### POST `/api/attendance/students`
- **Auth**: Required
- **Description**: Mark student attendance
- **Body**: AttendanceDto[]
- **Response**: `{ success: true }`

#### GET `/api/attendance/faculty`
- **Auth**: Required
- **Description**: Get faculty attendance
- **Query**: `staffId, date, session`
- **Response**: `{ data: FacultyAttendance[] }`

#### POST `/api/attendance/faculty`
- **Auth**: Required
- **Description**: Mark faculty attendance
- **Body**: FacultyAttendanceDto[]
- **Response**: `{ success: true }`

#### GET `/api/attendance/config`
- **Auth**: Required
- **Description**: Get attendance configuration
- **Response**: `{ data: AttendanceConfig }`

#### PATCH `/api/attendance/config`
- **Auth**: Required
- **Description**: Update attendance configuration
- **Body**: UpdateAttendanceConfigDto
- **Response**: `{ data: AttendanceConfig }`

### Fee Module (`/api/fees`)

#### Fee Heads (`/api/fees/fee-heads`)

##### GET `/api/fees/fee-heads`
- **Auth**: Required
- **Query**: `page, limit, category`
- **Response**: `{ data: FeeHead[], meta }`

##### POST `/api/fees/fee-heads`
- **Auth**: Required
- **Body**: CreateFeeHeadDto
- **Response**: `{ data: FeeHead }`

##### PATCH `/api/fees/fee-heads/:id`
- **Auth**: Required
- **Body**: UpdateFeeHeadDto
- **Response**: `{ data: FeeHead }`

#### Fee Structures (`/api/fees/fee-structures`)

##### GET `/api/fees/fee-structures`
- **Auth**: Required
- **Query**: `programmeId, academicYear, semester`
- **Response**: `{ data: FeeStructure[] }`

##### POST `/api/fees/fee-structures`
- **Auth**: Required
- **Body**: CreateFeeStructureDto
- **Response**: `{ data: FeeStructure }`

##### PATCH `/api/fees/fee-structures/:id`
- **Auth**: Required
- **Body**: UpdateFeeStructureDto
- **Response**: `{ data: FeeStructure }`

#### Fee Ledger (`/api/fees/ledger`)

##### GET `/api/fees/ledger/:studentId`
- **Auth**: Required
- **Description**: Get student fee ledger
- **Response**: `{ data: FeeLedger[] }`

##### POST `/api/fees/ledger/:studentId/pay`
- **Auth**: Required
- **Description**: Record payment
- **Body**: PaymentDto
- **Response**: `{ data: Payment }`

#### Scholarships (`/api/fees/scholarships`)

##### GET `/api/fees/scholarships`
- **Auth**: Required
- **Response**: `{ data: Scholarship[] }`

##### POST `/api/fees/scholarships`
- **Auth**: Required
- **Body**: CreateScholarshipDto
- **Response**: `{ data: Scholarship }`

### Examination Module (`/api/examinations`)

#### Exam Papers (`/api/examinations/papers`)

##### GET `/api/examinations/papers`
- **Auth**: Required
- **Query**: `batchId, status`
- **Response**: `{ data: ExamPaper[], meta }`

##### GET `/api/examinations/papers/:id`
- **Auth**: Required
- **Response**: `{ data: ExamPaper }`

##### POST `/api/examinations/papers`
- **Auth**: Required
- **Body**: CreateExamPaperDto
- **Response**: `{ data: ExamPaper }`

##### PATCH `/api/examinations/papers/:id`
- **Auth**: Required
- **Body**: UpdateExamPaperDto
- **Response**: `{ data: ExamPaper }`

##### POST `/api/examinations/papers/:id/publish`
- **Auth**: Required
- **Description**: Publish exam paper
- **Response**: `{ success: true }`

#### Exam Attempts (`/api/examinations/attempts`)

##### GET `/api/examinations/attempts/:id`
- **Auth**: Required
- **Description**: Get exam attempt
- **Response**: `{ data: ExamAttempt }`

##### POST `/api/examinations/attempts/:id/submit`
- **Auth**: Required
- **Description**: Submit exam
- **Body**: SubmitExamDto
- **Response**: `{ data: ExamAttempt }`

##### POST `/api/examinations/attempts/:id/auto-submit`
- **Auth**: Required
- **Description**: Auto-submit exam (time up)
- **Response**: `{ data: ExamAttempt }`

#### Question Bank (`/api/examinations/questions`)

##### GET `/api/examinations/questions`
- **Auth**: Required
- **Query**: `universitySubjectId, topic, difficulty, status`
- **Response**: `{ data: Question[], meta }`

##### POST `/api/examinations/questions`
- **Auth**: Required
- **Body**: CreateQuestionDto
- **Response**: `{ data: Question }`

##### PATCH `/api/examinations/questions/:id`
- **Auth**: Required
- **Body**: UpdateQuestionDto
- **Response**: `{ data: Question }`

#### Exam Config (`/api/examinations/config`)

##### GET `/api/examinations/config`
- **Auth**: Required
- **Response**: `{ data: ExamConfig }`

##### PATCH `/api/examinations/config`
- **Auth**: Required
- **Body**: UpdateExamConfigDto
- **Response**: `{ data: ExamConfig }`

### Timetable Module (`/api/timetable`)

#### Time Slots (`/api/timetable/time-slots`)

##### GET `/api/timetable/time-slots`
- **Auth**: Required
- **Query**: `instituteId, dayOfWeek`
- **Response**: `{ data: TimeSlot[] }`

##### POST `/api/timetable/time-slots`
- **Auth**: Required
- **Body**: CreateTimeSlotDto
- **Response**: `{ data: TimeSlot }`

##### PATCH `/api/timetable/time-slots/:id`
- **Auth**: Required
- **Body**: UpdateTimeSlotDto
- **Response**: `{ data: TimeSlot }`

#### Timetable Entries (`/api/timetable/entries`)

##### GET `/api/timetable/entries`
- **Auth**: Required
- **Query**: `sectionId, courseId, staffId, date`
- **Response**: `{ data: TimetableEntry[] }`

##### POST `/api/timetable/entries`
- **Auth**: Required
- **Body**: CreateTimetableEntryDto
- **Response**: `{ data: TimetableEntry }`

##### PATCH `/api/timetable/entries/:id`
- **Auth**: Required
- **Body**: UpdateTimetableEntryDto
- **Response**: `{ data: TimetableEntry }`

##### DELETE `/api/timetable/entries/:id`
- **Auth**: Required
- **Response**: `{ success: true }`

### Library Module (`/api/library`)

#### Books (`/api/library/books`)

##### GET `/api/library/books`
- **Auth**: Required
- **Query**: `page, limit, search, category`
- **Response**: `{ data: Book[], meta }`

##### POST `/api/library/books`
- **Auth**: Required
- **Body**: CreateBookDto
- **Response**: `{ data: Book }`

##### PATCH `/api/library/books/:id`
- **Auth**: Required
- **Body**: UpdateBookDto
- **Response**: `{ data: Book }`

#### Book Issues (`/api/library/issues`)

##### GET `/api/library/issues`
- **Auth**: Required
- **Query**: `borrowerId, status`
- **Response**: `{ data: BookIssue[] }`

##### POST `/api/library/issues`
- **Auth**: Required
- **Body**: IssueBookDto
- **Response**: `{ data: BookIssue }`

##### POST `/api/library/issues/:id/return`
- **Auth**: Required
- **Description**: Return book
- **Body**: ReturnBookDto
- **Response**: `{ data: BookIssue }`

#### Book Reservations (`/api/library/reservations`)

##### GET `/api/library/reservations`
- **Auth**: Required
- **Query**: `borrowerId, status`
- **Response**: `{ data: BookReservation[] }`

##### POST `/api/library/reservations`
- **Auth**: Required
- **Body**: ReserveBookDto
- **Response**: `{ data: BookReservation }`

##### DELETE `/api/library/reservations/:id`
- **Auth**: Required
- **Description**: Cancel reservation
- **Response**: `{ success: true }`

### Hostel Module (`/api/hostel`)

#### Hostels (`/api/hostel/hostels`)

##### GET `/api/hostel/hostels`
- **Auth**: Required
- **Query**: `instituteId`
- **Response**: `{ data: Hostel[] }`

##### POST `/api/hostel/hostels`
- **Auth**: Required
- **Body**: CreateHostelDto
- **Response**: `{ data: Hostel }`

##### PATCH `/api/hostel/hostels/:id`
- **Auth**: Required
- **Body**: UpdateHostelDto
- **Response**: `{ data: Hostel }`

#### Hostel Rooms (`/api/hostel/rooms`)

##### GET `/api/hostel/rooms`
- **Auth**: Required
- **Query**: `hostelId`
- **Response**: `{ data: HostelRoom[] }`

##### POST `/api/hostel/rooms`
- **Auth**: Required
- **Body**: CreateHostelRoomDto
- **Response**: `{ data: HostelRoom }`

##### PATCH `/api/hostel/rooms/:id`
- **Auth**: Required
- **Body**: UpdateHostelRoomDto
- **Response**: `{ data: HostelRoom }`

#### Hostel Allocations (`/api/hostel/allocations`)

##### GET `/api/hostel/allocations`
- **Auth**: Required
- **Query**: `studentId, roomId, status`
- **Response**: `{ data: HostelAllocation[] }`

##### POST `/api/hostel/allocations`
- **Auth**: Required
- **Body**: CreateHostelAllocationDto
- **Response**: `{ data: HostelAllocation }`

##### PATCH `/api/hostel/allocations/:id/vacate`
- **Auth**: Required
- **Description**: Vacate room
- **Body**: `{ vacateReason }`
- **Response**: `{ data: HostelAllocation }`

### Transport Module (`/api/transport`)

#### Transport Routes (`/api/transport/routes`)

##### GET `/api/transport/routes`
- **Auth**: Required
- **Query**: `instituteId`
- **Response**: `{ data: TransportRoute[] }`

##### POST `/api/transport/routes`
- **Auth**: Required
- **Body**: CreateTransportRouteDto
- **Response**: `{ data: TransportRoute }`

##### PATCH `/api/transport/routes/:id`
- **Auth**: Required
- **Body**: UpdateTransportRouteDto
- **Response**: `{ data: TransportRoute }`

#### Transport Passes (`/api/transport/passes`)

##### GET `/api/transport/passes`
- **Auth**: Required
- **Query**: `studentId, routeId, status`
- **Response**: `{ data: TransportPass[] }`

##### POST `/api/transport/passes`
- **Auth**: Required
- **Body**: CreateTransportPassDto
- **Response**: `{ data: TransportPass }`

##### PATCH `/api/transport/passes/:id/cancel`
- **Auth**: Required
- **Description**: Cancel pass
- **Body**: `{ cancelReason }`
- **Response**: `{ data: TransportPass }`

### HR Module (`/api/hr`)

#### Staff (`/api/hr/staff`)

##### GET `/api/hr/staff`
- **Auth**: Required
- **Query**: `page, limit, departmentId, staffType`
- **Response**: `{ data: Staff[], meta }`

##### GET `/api/hr/staff/:id`
- **Auth**: Required
- **Response**: `{ data: Staff }`

##### POST `/api/hr/staff`
- **Auth**: Required
- **Body**: CreateStaffDto
- **Response**: `{ data: Staff }`

##### PATCH `/api/hr/staff/:id`
- **Auth**: Required
- **Body**: UpdateStaffDto
- **Response**: `{ data: Staff }`

#### Leave Applications (`/api/hr/leave-applications`)

##### GET `/api/hr/leave-applications`
- **Auth**: Required
- **Query**: `staffId, status`
- **Response**: `{ data: LeaveApplication[] }`

##### POST `/api/hr/leave-applications`
- **Auth**: Required
- **Body**: CreateLeaveApplicationDto
- **Response**: `{ data: LeaveApplication }`

##### PATCH `/api/hr/leave-applications/:id/review`
- **Auth**: Required
- **Body**: `{ decision, reviewNote }`
- **Response**: `{ data: LeaveApplication }`

#### Leave Balances (`/api/hr/leave-balances`)

##### GET `/api/hr/leave-balances/:staffId`
- **Auth**: Required
- **Response**: `{ data: LeaveBalance[] }`

### Documents Module (`/api/documents`)

#### Document Templates (`/api/documents/templates`)

##### GET `/api/documents/templates`
- **Auth**: Required
- **Query**: `universityId`
- **Response**: `{ data: DocumentTemplate[] }`

##### POST `/api/documents/templates`
- **Auth**: Required
- **Body**: CreateDocumentTemplateDto
- **Response**: `{ data: DocumentTemplate }`

##### PATCH `/api/documents/templates/:id`
- **Auth**: Required
- **Body**: UpdateDocumentTemplateDto
- **Response**: `{ data: DocumentTemplate }`

#### Issued Documents (`/api/documents/issued`)

##### GET `/api/documents/issued`
- **Auth**: Required
- **Query**: `subjectId, subjectType, status`
- **Response**: `{ data: IssuedDocument[] }`

##### POST `/api/documents/issued`
- **Auth**: Required
- **Body**: IssueDocumentDto
- **Response**: `{ data: IssuedDocument }`

##### POST `/api/documents/issued/:id/revoke`
- **Auth**: Required
- **Body**: `{ revokeReason }`
- **Response**: `{ data: IssuedDocument }`

### Workflow Module (`/api/workflow`)

#### Workflow Definitions (`/api/workflow/definitions`)

##### GET `/api/workflow/definitions`
- **Auth**: Required
- **Query**: `entityType, status`
- **Response**: `{ data: WorkflowDefinition[] }`

##### POST `/api/workflow/definitions`
- **Auth**: Required
- **Body**: CreateWorkflowDefinitionDto
- **Response**: `{ data: WorkflowDefinition }`

##### PATCH `/api/workflow/definitions/:id`
- **Auth**: Required
- **Body**: UpdateWorkflowDefinitionDto
- **Response**: `{ data: WorkflowDefinition }`

##### POST `/api/workflow/definitions/:id/activate`
- **Auth**: Required
- **Description**: Activate workflow definition
- **Response**: `{ data: WorkflowDefinition }`

#### Workflow Instances (`/api/workflow/instances`)

##### GET `/api/workflow/instances`
- **Auth**: Required
- **Query**: `definitionId, status, entityType, entityId`
- **Response**: `{ data: WorkflowInstance[], meta }`

##### GET `/api/workflow/instances/:id`
- **Auth**: Required
- **Response**: `{ data: WorkflowInstance }`

##### POST `/api/workflow/instances`
- **Auth**: Required
- **Body**: StartWorkflowDto
- **Response**: `{ data: WorkflowInstance }`

#### Workflow Tasks (`/api/workflow/tasks`)

##### GET `/api/workflow/tasks`
- **Auth**: Required
- **Query**: `assignedUserId, status, actorRole`
- **Response**: `{ data: WorkflowTask[] }`

##### PATCH `/api/workflow/tasks/:id/act`
- **Auth**: Required
- **Body**: `{ decision, comment, collectedData }`
- **Response**: `{ data: WorkflowTask }`

### Users Module (`/api/users`)

#### Users (`/api/users`)

##### GET `/api/users`
- **Auth**: Required
- **Query**: `page, limit, role, instituteId`
- **Response**: `{ data: User[], meta }`

##### GET `/api/users/:id`
- **Auth**: Required
- **Response**: `{ data: User }`

##### PATCH `/api/users/:id`
- **Auth**: Required
- **Body**: UpdateUserDto
- **Response**: `{ data: User }`

##### DELETE `/api/users/:id`
- **Auth**: Required
- **Response**: `{ success: true }`

#### Roles (`/api/users/roles`)

##### GET `/api/users/roles`
- **Auth**: Required
- **Query**: `universityId`
- **Response**: `{ data: Role[] }`

##### POST `/api/users/roles`
- **Auth**: Required
- **Body**: CreateRoleDto
- **Response**: `{ data: Role }`

##### PATCH `/api/users/roles/:id`
- **Auth**: Required
- **Body**: UpdateRoleDto
- **Response**: `{ data: Role }`

### Notifications Module (`/api/notifications`)

#### Notifications (`/api/notifications`)

##### GET `/api/notifications`
- **Auth**: Required
- **Query**: `userId, isRead`
- **Response**: `{ data: Notification[] }`

##### PATCH `/api/notifications/:id/read`
- **Auth**: Required
- **Description**: Mark notification as read
- **Response**: `{ data: Notification }`

##### PATCH `/api/notifications/mark-all-read`
- **Auth**: Required
- **Description**: Mark all notifications as read
- **Response**: `{ success: true }`

### Notice Board Module (`/api/notice-board`)

#### Notices (`/api/notice-board/notices`)

##### GET `/api/notice-board/notices`
- **Auth**: Required
- **Query**: `tab, instituteId, tagId`
- **Response**: `{ data: Notice[] }`

##### POST `/api/notice-board/notices`
- **Auth**: Required
- **Body**: CreateNoticeDto
- **Response**: `{ data: Notice }`

##### PATCH `/api/notice-board/notices/:id`
- **Auth**: Required
- **Body**: UpdateNoticeDto
- **Response**: `{ data: Notice }`

##### DELETE `/api/notice-board/notices/:id`
- **Auth**: Required
- **Response**: `{ success: true }`

#### Notice Tags (`/api/notice-board/tags`)

##### GET `/api/notice-board/tags`
- **Auth**: Required
- **Query**: `instituteId`
- **Response**: `{ data: NoticeTag[] }`

##### POST `/api/notice-board/tags`
- **Auth**: Required
- **Body**: CreateNoticeTagDto
- **Response**: `{ data: NoticeTag }`

### Banners Module (`/api/banners`)

#### Banners (`/api/banners`)

##### GET `/api/banners`
- **Auth**: Required
- **Query**: `universityId, instituteId`
- **Response**: `{ data: Banner[] }`

##### POST `/api/banners`
- **Auth**: Required
- **Body**: CreateBannerDto
- **Response**: `{ data: Banner }`

##### PATCH `/api/banners/:id`
- **Auth**: Required
- **Body**: UpdateBannerDto
- **Response**: `{ data: Banner }`

##### DELETE `/api/banners/:id`
- **Auth**: Required
- **Response**: `{ success: true }`

### Settings Module (`/api/settings`)

#### Settings (`/api/settings`)

##### GET `/api/settings`
- **Auth**: Required
- **Response**: `{ data: Settings }`

##### PATCH `/api/settings`
- **Auth**: Required
- **Body**: UpdateSettingsDto
- **Response**: `{ data: Settings }`

### Forms Module (`/api/forms`)

#### Form Templates (`/api/forms/templates`)

##### GET `/api/forms/templates`
- **Auth**: Required
- **Query**: `category, instituteId, isActive`
- **Response**: `{ data: FormTemplate[] }`

##### POST `/api/forms/templates`
- **Auth**: Required
- **Body**: CreateFormTemplateDto
- **Response**: `{ data: FormTemplate }`

##### PATCH `/api/forms/templates/:id`
- **Auth**: Required
- **Body**: UpdateFormTemplateDto
- **Response**: `{ data: FormTemplate }`

#### Form Submissions (`/api/forms/submissions`)

##### GET `/api/forms/submissions`
- **Auth**: Required
- **Query**: `formTemplateId, studentId, status`
- **Response**: `{ data: FormSubmission[] }`

##### POST `/api/forms/submissions`
- **Auth**: Required
- **Body**: SubmitFormDto
- **Response**: `{ data: FormSubmission }`

##### PATCH `/api/forms/submissions/:id/review`
- **Auth**: Required
- **Body**: `{ status, rejectionNote }`
- **Response**: `{ data: FormSubmission }`

### Analytics Module (`/api/analytics`)

#### Analytics (`/api/analytics`)

##### GET `/api/analytics/dashboard`
- **Auth**: Required
- **Response**: `{ data: DashboardStats }`

##### GET `/api/analytics/attendance`
- **Auth**: Required
- **Query**: `batchId, termId`
- **Response**: `{ data: AttendanceStats }`

##### GET `/api/analytics/fees`
- **Auth**: Required
- **Query**: `batchId, termId`
- **Response**: `{ data: FeeStats }`

##### GET `/api/analytics/examinations`
- **Auth**: Required
- **Query**: `batchId, termId`
- **Response**: `{ data: ExamStats }`

### Audit Module (`/api/audit`)

#### Audit Logs (`/api/audit/logs`)

##### GET `/api/audit/logs`
- **Auth**: Required
- **Query**: `actorId, module, entityType, entityId, fromDate, toDate`
- **Response**: `{ data: AuditLog[], meta }`

### Counselling Module (`/api/counselling`)

#### Counsellors (`/api/counselling/counsellors`)

##### GET `/api/counselling/counsellors`
- **Auth**: Required
- **Response**: `{ data: Counsellor[] }`

##### POST `/api/counselling/counsellors`
- **Auth**: Required
- **Body**: CreateCounsellorDto
- **Response**: `{ data: Counsellor }`

##### PATCH `/api/counselling/counsellors/:id/revoke`
- **Auth**: Required
- **Description**: Revoke counsellor
- **Response**: `{ data: Counsellor }`

#### Counselling Requests (`/api/counselling/requests`)

##### GET `/api/counselling/requests`
- **Auth**: Required
- **Query**: `status, counsellorId`
- **Response**: `{ data: CounsellingRequest[] }`

##### POST `/api/counselling/requests`
- **Auth**: Required
- **Body**: CreateCounsellingRequestDto
- **Response**: `{ data: CounsellingRequest }`

##### PATCH `/api/counselling/requests/:id/allocate`
- **Auth**: Required
- **Body**: `{ counsellorId }`
- **Response**: `{ data: CounsellingRequest }`

##### PATCH `/api/counselling/requests/:id/advise`
- **Auth**: Required
- **Body**: `{ recommendationNote, recommendedProgrammeId, recommendedCourseId }`
- **Response**: `{ data: CounsellingRequest }`

### Health Check

#### GET `/health`
- **Auth**: Not required
- **Description**: Health check endpoint
- **Response**: `{ status: 'ok', checks: { database, redis, minio } }`

## Error Codes

### HTTP Status Codes

- **200 OK**: Successful request
- **201 Created**: Resource created
- **204 No Content**: Successful request with no response body
- **400 Bad Request**: Invalid request
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authorization failed
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., duplicate)
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### Prisma Error Codes

- **P2002**: Unique constraint violation
- **P2003**: Foreign key constraint violation
- **P2025**: Record not found
- **P2000**: Value too long
- **P2011**: Null constraint violation

## Pagination

### Query Parameters

- **page**: Page number (default: 1)
- **limit**: Items per page (default: 10, max: 100)

### Response Meta

```json
{
  "success": true,
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```

## Filtering

### Common Query Parameters

- **search**: Text search
- **status**: Filter by status
- **instituteId**: Filter by institute
- **departmentId**: Filter by department
- **fromDate**: Date range start
- **toDate**: Date range end

## Sorting

### Query Parameter

- **sortBy**: Field to sort by
- **sortOrder**: asc or desc (default: asc)

## Swagger Documentation

### Development Only

Swagger UI is available in non-production environments:

```
http://localhost:3000/api/docs
```

### Authentication in Swagger

1. Click "Authorize" button
2. Enter JWT token (without "Bearer " prefix)
3. Click "Authorize"

## API Versioning

Currently, the API does not use versioning. All endpoints are at `/api`.

Future versions may introduce versioning like `/api/v1/`, `/api/v2/`.

## WebSocket Endpoints

### CBE Engine

The CBE engine uses WebSocket connections for real-time exam delivery:

```
ws://localhost:3001
```

### Events

- **exam:join**: Join exam session
- **exam:submit**: Submit exam
- **exam:heartbeat**: Heartbeat for liveness
- **exam:directive**: Receive invigilator directive
- **exam:proctor**: Proctoring events

## Known Limitations

1. **No GraphQL**: REST API only
2. **No gRPC**: REST API only
3. **No API Versioning**: Single version
4. **No Batch Operations**: Limited batch endpoints
5. **No Webhooks**: No webhook support
