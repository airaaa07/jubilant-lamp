# Remaining Modules Overview

## Purpose

This document provides an overview of the remaining modules in the University ERP system. For detailed documentation of each module, refer to the individual module documentation files.

## Module List

### 5. Attendance Module
**Purpose**: Manages student and faculty attendance tracking.

**Key Features**:
- Student attendance recording
- Faculty attendance recording
- Attendance reports
- Attendance configuration
- Attendance alerts

**Dependencies**: PrismaModule, AuthModule, AcademicModule, NotificationsModule

**Key Tables**: StudentAttendance, FacultyAttendance, AttendanceConfig

**Business Rules**:
- Attendance must be recorded daily
- Attendance percentage calculated
- Minimum attendance requirement enforced
- Attendance alerts sent to parents

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 6. Examination Module
**Purpose**: Manages examinations, questions, papers, and results.

**Key Features**:
- Exam scheduling
- Question bank management
- Exam paper generation
- Online examinations
- Result processing
- Re-assessment requests

**Dependencies**: PrismaModule, AuthModule, AcademicModule, WorkflowModule, NotificationsModule

**Key Tables**: ExamPaper, ExamPaperQuestion, ExamAttempt, ExamResponse, StudentMarks, StudentTermResult

**Business Rules**:
- Exams scheduled per timetable
- Questions selected from question bank
- Results calculated based on grading policy
- Re-assessment requests processed
- Results published after approval

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 7. Fee Module
**Purpose**: Manages fee structures, payments, scholarships, and financial records.

**Key Features**:
- Fee structure management
- Fee demand generation
- Payment processing
- Scholarship management
- Fee waivers
- Government reimbursements
- Financial reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule, WorkflowModule, NotificationsModule

**Key Tables**: FeeStructure, FeeLedger, Payment, Scholarship, FeeWaiver, GovtReimbursement, StudentPayable

**Business Rules**:
- Fee structure defined per program
- Fee demands generated per term
- Payments recorded against demands
- Scholarships applied based on criteria
- Fee waivers approved by workflow

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 8. Timetable Module
**Purpose**: Manages class schedules, time slots, and timetable generation.

**Key Features**:
- Time slot management
- Timetable generation
- Room allocation
- Staff assignment
- Timetable conflicts detection
- Timetable publishing

**Dependencies**: PrismaModule, AuthModule, AcademicModule, MasterDataModule

**Key Tables**: TimeSlot, TimetableEntry, Room, RoomBooking

**Business Rules**:
- Time slots defined per institute
- Timetable generated per term
- Conflicts detected and resolved
- Room allocation optimized
- Staff workload balanced

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 9. Library Module
**Purpose**: Manages library books, issues, reservations, and library operations.

**Key Features**:
- Book catalog management
- Book copy management
- Book issue/return
- Book reservation
- Library configuration
- Library reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule, NotificationsModule

**Key Tables**: Book, BookCopy, BookIssue, BookReservation, LibraryConfig

**Business Rules**:
- Books cataloged with metadata
- Copies tracked individually
- Issue duration limited
- Reservations prioritized
- Overdue fines calculated

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 10. Hostel Module
**Purpose**: Manages hostel rooms, allocations, and hostel operations.

**Key Features**:
- Hostel management
- Room management
- Room allocation
- Hostel configuration
- Hostel reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule, AcademicModule

**Key Tables**: Hostel, HostelRoom, HostelAllocation, HostelConfig

**Business Rules**:
- Hostels have capacity limits
- Rooms have capacity limits
- Allocations based on priority
- Hostel fees charged
- Room changes tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 11. Transport Module
**Purpose**: Manages transport routes, vehicles, and transport passes.

**Key Features**:
- Route management
- Vehicle management
- Transport pass management
- Transport configuration
- Transport reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule, AcademicModule

**Key Tables**: TransportRoute, TransportVehicle, TransportPass, TransportConfig

**Business Rules**:
- Routes defined with stops
- Vehicles assigned to routes
- Passes issued to students
- Transport fees charged
- Route changes tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 12. HR Module
**Purpose**: Manages staff, payroll, leaves, and HR operations.

**Key Features**:
- Staff management
- Staff subject assignment
- Leave management
- Staff documents
- Payroll processing
- HR reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule, AcademicModule, WorkflowModule

**Key Tables**: Staff, StaffSubject, LeaveType, LeaveApplication, LeaveBalance, StaffDocument

**Business Rules**:
- Staff assigned to departments
- Staff assigned to subjects
- Leave balance calculated
- Leave applications approved by workflow
- Payroll processed monthly

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 13. Documents Module
**Purpose**: Manages document generation, templates, and document issuance.

**Key Features**:
- Document template management
- Document generation
- Document issuance
- Document tracking
- Document reports

**Dependencies**: PrismaModule, AuthModule, MinioModule, WorkflowModule

**Key Tables**: DocumentTemplate, IssuedDocument

**Business Rules**:
- Document templates defined
- Documents generated from templates
- Documents issued to students
- Document issuance tracked
- Documents stored in MinIO

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 14. Workflow Module
**Purpose**: Provides workflow engine for approval processes.

**Key Features**:
- Workflow definition
- Workflow state management
- Workflow transitions
- Workflow instances
- Workflow tasks
- Workflow reservations

**Dependencies**: PrismaModule, AuthModule, BullModule

**Key Tables**: WorkflowDefinition, WorkflowState, WorkflowTransition, WorkflowInstance, WorkflowTask, WorkflowReservation

**Business Rules**:
- Workflows defined with states and transitions
- Instances track process progress
- Tasks assigned to users
- Reservations for resources
- Workflow history tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 15. Notifications Module
**Purpose**: Manages email and SMS notifications.

**Key Features**:
- Email notifications
- SMS notifications
- Notification templates
- Notification queue
- Notification tracking

**Dependencies**: PrismaModule, BullModule, RedisModule

**Key Tables**: Notification

**Business Rules**:
- Notifications queued for async processing
- Email sent via email service
- SMS sent via SMS service
- Notification status tracked
- Failed notifications retried

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 16. Notice Board Module
**Purpose**: Manages notices and announcements.

**Key Features**:
- Notice creation
- Notice publishing
- Notice tags
- Notice targeting
- Notice expiration

**Dependencies**: PrismaModule, AuthModule, MasterDataModule

**Key Tables**: Notice, NoticeTag

**Business Rules**:
- Notices have expiration dates
- Notices can be tagged
- Notices can target specific audiences
- Expired notices archived
- Notice views tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 17. Banners Module
**Purpose**: Manages system-wide banners and announcements.

**Key Features**:
- Banner creation
- Banner publishing
- Banner targeting
- Banner expiration
- Banner tracking

**Dependencies**: PrismaModule, AuthModule

**Key Tables**: Banner, BannerReceipt

**Business Rules**:
- Banners have expiration dates
- Banners can target specific users
- Banner dismissals tracked
- Expired banners archived
- Banner views tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 18. Users Module
**Purpose**: Manages user accounts and user data.

**Key Features**:
- User management
- User profile management
- User role assignment
- User activation/deactivation
- User reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule

**Key Tables**: User, UserProfile, UserRoleAssignment

**Business Rules**:
- Users have unique emails
- Users assigned roles
- Users assigned to universities/institutes
- User profiles contain personal data
- User status tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 19. Settings Module
**Purpose**: Manages system settings and configurations.

**Key Features**:
- System settings
- Institute settings
- Department settings
- Configuration management
- Settings validation

**Dependencies**: PrismaModule, AuthModule, MasterDataModule

**Key Tables**: Settings (inferred)

**Business Rules**:
- Settings have default values
- Settings can be overridden at different levels
- Settings validated
- Settings changes logged
- Settings cached

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 20. Forms Module
**Purpose**: Manages dynamic form builder and form submissions.

**Key Features**:
- Form template creation
- Form field management
- Form submission
- Form validation
- Form reports

**Dependencies**: PrismaModule, AuthModule, WorkflowModule

**Key Tables**: FormTemplate, FormSubmission, ModuleAccess

**Business Rules**:
- Form templates define structure
- Form submissions validated
- Form submissions can trigger workflows
- Form data stored as JSON
- Form access controlled

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 21. Analytics Module
**Purpose**: Provides reports and analytics for the system.

**Key Features**:
- Report generation
- Data analytics
- Dashboard metrics
- Export functionality
- Scheduled reports

**Dependencies**: PrismaModule, AuthModule, RedisModule

**Key Tables**: Analytics data derived from other tables

**Business Rules**:
- Reports generated on demand
- Reports can be scheduled
- Reports cached for performance
- Reports scoped by user role
- Export formats supported

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 22. Audit Module
**Purpose**: Manages audit logging for system events.

**Key Features**:
- Audit log recording
- Audit log querying
- Audit log retention
- Audit log reports
- Audit log export

**Dependencies**: PrismaModule, AuthModule

**Key Tables**: AuditLog

**Business Rules**:
- All write operations logged
- Audit log includes user, action, entity
- Audit log retained for specified period
- Audit log queryable
- Audit log exportable

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 23. Counselling Module
**Purpose**: Manages student counselling services.

**Key Features**:
- Counsellor management
- Counsellor contracts
- Counselling requests
- Counselling comments
- Counsellor enrollment credits

**Dependencies**: PrismaModule, AuthModule, AcademicModule

**Key Tables**: Counsellor, CounsellorContract, CounsellingRequest, CounsellingComment, CounsellorEnrollmentCredit

**Business Rules**:
- Counsellors assigned to institutes
- Counselling requests tracked
- Counselling sessions documented
- Enrollment credits tracked
- Counsellor performance measured

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 24. Social Monitoring Module
**Purpose**: Manages social media monitoring for institutions.

**Key Features**:
- Social handle management
- Social post tracking
- Sentiment analysis
- Alert generation
- Social reports

**Dependencies**: PrismaModule, AuthModule, External APIs

**Key Tables**: SocialHandle, SocialPost

**Business Rules**:
- Social handles monitored
- Posts tracked and analyzed
- Sentiment calculated
- Alerts generated for negative sentiment
- Social reports generated

**Security**: Scope-based access, data scoping by tenant hierarchy

---

### 25. Resource Reservation Module
**Purpose**: Manages room and equipment booking.

**Key Features**:
- Room booking
- Equipment booking
- Reservation management
- Conflict detection
- Reservation reports

**Dependencies**: PrismaModule, AuthModule, MasterDataModule, WorkflowModule

**Key Tables**: Room, RoomBooking, Equipment, ResourceReservation, BatchTermSubjectResource

**Business Rules**:
- Resources have capacity limits
- Reservations time-bounded
- Conflicts detected
- Reservations approved by workflow
- Reservation history tracked

**Security**: Scope-based access, data scoping by tenant hierarchy

---

## Common Patterns Across Modules

### Controller Pattern
All modules follow the same controller pattern:
- Use guards for authentication and authorization
- Use @Scope decorator for module-level access
- Standard CRUD operations (GET, POST, PATCH, DELETE)
- Query parameters for filtering
- DTOs for validation

### Service Pattern
All modules follow the same service pattern:
- Business logic in service
- Database operations via Prisma
- Data scoping based on user role
- Error handling
- Transaction support

### Security Pattern
All modules follow the same security pattern:
- GlobalJwtAuthGuard for authentication
- ScopeGuard for module-level access
- Data scoping by tenant hierarchy
- Input validation via DTOs
- Audit logging for changes

### Performance Pattern
All modules follow the same performance pattern:
- Redis caching for frequently accessed data
- Database indexing for foreign keys
- Query optimization
- Pagination for large datasets
- Lazy loading for related data

## Module Interactions

### Common Interactions
- **Auth Module**: Used by all modules for authentication
- **Master Data Module**: Used by most modules for organizational data
- **Workflow Module**: Used by modules requiring approval processes
- **Notifications Module**: Used by modules requiring notifications
- **PrismaModule**: Used by all modules for database access

### Data Flow
```
Frontend → Controller → Service → Prisma → Database
              ↓
         Guards (Auth/Scope)
              ↓
         DTOs (Validation)
```

## Future Enhancements

### Module Federation
Implement module federation for independent deployment and better scalability.

### Event-Driven Architecture
Implement event-driven architecture for better decoupling and async communication.

### Microservices
Consider splitting modules into microservices for better scalability and isolation.

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [04-Academic-Module](./04-Academic-Module.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [09-Workflows](../09-Workflows/README.md) - Workflow details
