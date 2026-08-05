# User Journeys - Complete Role-Based Experiences

## Table of Contents
1. [SuperAdmin Journey](#superadmin-journey)
2. [University Admin Journey](#university-admin-journey)
3. [Institute Admin Journey](#institute-admin-journey)
4. [Student Journey](#student-journey)
5. [Teaching Faculty Journey](#teaching-faculty-journey)
6. [HOD Journey](#hod-journey)
7. [Librarian Journey](#librarian-journey)
8. [Accountant Journey](#accountant-journey)
9. [Warden Journey](#warden-journey)
10. [Applicant Journey](#applicant-journey)
11. [Parent Journey](#parent-journey)
12. [Counsellor Journey](#counsellor-journey)

---

## SuperAdmin Journey

### Who is SuperAdmin?
The SuperAdmin is the highest-level system administrator with complete access to all modules and university-level configuration. They are responsible for system setup, user management, and overall configuration.

### Typical Day in the Life

#### Morning: System Health and Configuration
**Login**: SuperAdmin logs in via LoginPage
- Enters email: erpsupport@slashcurate.com
- Enters password
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views system health indicators
- Checks recent user registrations
- Reviews pending approval tasks
- Monitors system metrics

**System Configuration**: SettingsPage.tsx
- Navigates to Settings
- Reviews university-level configurations
- Checks integration status (email, SMS, payment gateway)
- Verifies module access settings
- Reviews backup schedules

#### Mid-Day: User and Access Management
**User Management**: UserManagementPage.tsx
- Reviews new user registrations
- Approves/rejects registration requests
- Assigns roles to new users
- Reviews staff account creation requests
- Manages SuperAdmin accounts (create other super admins)

**Role Management**: SettingsPage.tsx (Roles tab)
- Reviews role definitions
- Creates new roles if needed
- Configures role permissions
- Manages role assignments

**Module Access**: SettingsPage.tsx (Module Access)
- Configures which roles can access which modules
- Enables/disables modules per institute
- Sets up navigation menu customization

#### Afternoon: Master Data and Setup
**University Management**: MasterDataPage.tsx
- Reviews university configuration
- Manages institute creation/editing
- Configures university departments
- Sets up university-wide academic catalog

**ID Format Configuration**: IdFormatsPage.tsx
- Configures enrollment number patterns
- Sets up receipt number formats
- Configures exam roll number patterns
- Tests format generation

**Backup Management**: SettingsPage.tsx (Backup)
- Reviews backup schedules
- Checks backup verification status
- Manually triggers backup if needed
- Reviews backup logs

#### Evening: Monitoring and Reports
**Audit Log Review**: AuditLogPage.tsx
- Reviews recent system activities
- Checks for suspicious activities
- Monitors user access patterns
- Reviews configuration changes

**Analytics Review**: AnalyticsPage.tsx
- Views system-wide analytics
- Reviews user adoption metrics
- Checks module usage statistics
- Reviews performance indicators

### Key Responsibilities

1. **System Setup**
   - Initial university configuration
   - Institute creation and setup
   - Role and permission configuration
   - Integration setup (email, SMS, payment)

2. **User Management**
   - SuperAdmin account management
   - University admin assignment
   - Role and permission management
   - User account issues resolution

3. **Configuration Management**
   - University-level settings
   - Module access control
   - Navigation customization
   - Branding configuration

4. **System Health**
   - Backup monitoring
   - Integration health checks
   - Performance monitoring
   - Security audits

### Screens Frequently Used
- DashboardPage.tsx
- SettingsPage.tsx
- UserManagementPage.tsx
- MasterDataPage.tsx
- AuditLogPage.tsx
- AnalyticsPage.tsx
- IdFormatsPage.tsx

### Decisions Made
- University-level policy configuration
- Role and permission assignments
- Module availability decisions
- Integration enablement decisions
- Backup strategy decisions

### Interactions with Other Users
- **University Admins**: Delegates day-to-day administration
- **Institute Admins**: Provides access and support
- **Technical Team**: Coordinates system changes
- **Users**: Resolves access issues

### Pain Points
- System-wide configuration changes require careful testing
- User access issues can be urgent
- Integration failures need immediate attention
- Backup failures require quick resolution

### Success Metrics
- System uptime and availability
- User satisfaction with access
- Integration reliability
- Backup success rate
- Configuration accuracy

---

## University Admin Journey

### Who is University Admin?
University Admin manages university-level operations including academic programs, university departments, and cross-institute coordination. They report to SuperAdmin and oversee Institute Admins.

### Typical Day in the Life

#### Morning: Academic Planning
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views university-wide metrics
- Checks pending approvals
- Reviews institute activities
- Monitors enrollment trends

**University Catalog Management**: MasterDataPage.tsx
- Manages university-level programs (Programme)
- Configures university streams
- Sets up university subjects
- Manages university departments

**Stream Label Configuration**: MasterDataPage.tsx
- Creates new stream labels
- Configures academic rules (grading, attendance)
- Sets fee schedules for streams
- Version control for rule changes

#### Mid-Day: Institute Coordination
**Institute Management**: MasterDataPage.tsx
- Reviews institute performance
- Manages institute creation/editing
- Configures institute-specific settings
- Coordinates cross-institute activities

**Department Management**: MasterDataPage.tsx
- Manages university departments
- Assigns HODs to departments
- Configures departmental permissions
- Reviews departmental performance

**Admission Oversight**: AdmissionsPage.tsx
- Reviews university-wide admission statistics
- Monitors seat allocation across institutes
- Reviews merit list generation
- Coordinates admission policies

#### Afternoon: Examination and Results
**Exam Configuration**: ExaminationsPage.tsx
- Sets university-wide exam policies
- Configures exam schedules
- Reviews question bank standards
- Monitors exam results

**Result Publishing**: ExaminationsPage.tsx
- Reviews term results before publication
- Approves university-wide result publication
- Monitors revaluation requests
- Reviews academic performance

**Fee Structure Oversight**: FeesPage.tsx
- Reviews fee structures across institutes
- Approves major fee changes
- Monitors fee collection trends
- Reviews scholarship programs

#### Evening: Reporting and Planning
**Analytics Review**: AnalyticsPage.tsx
- Views university-wide analytics
- Reviews enrollment trends
- Monitors academic performance
- Reviews financial metrics

**Workflow Monitoring**: WorkflowMonitorPage.tsx
- Reviews university-wide workflow instances
- Monitors approval bottlenecks
- Reviews process completion rates
- Identifies process improvements

### Key Responsibilities

1. **Academic Governance**
   - University program catalog
   - Stream and subject definitions
   - Academic rule configuration
   - Grading and attendance policies

2. **Institute Coordination**
   - Institute performance monitoring
   - Cross-institute resource allocation
   - Standardization across institutes
   - Institute admin support

3. **Admission Management**
   - University-wide admission policies
   - Seat allocation coordination
   - Merit list oversight
   - Counseling program management

4. **Examination Oversight**
   - University exam policies
   - Result publication approval
   - Revaluation process oversight
   - Academic performance monitoring

### Screens Frequently Used
- DashboardPage.tsx
- MasterDataPage.tsx
- AdmissionsPage.tsx
- ExaminationsPage.tsx
- FeesPage.tsx
- AnalyticsPage.tsx
- WorkflowMonitorPage.tsx

### Decisions Made
- Academic program creation/modification
- Stream rule configuration
- Institute-level policy decisions
- Admission policy decisions
- Examination policy decisions

### Interactions with Other Users
- **SuperAdmin**: Receives delegated authority
- **Institute Admins**: Provides guidance and oversight
- **HODs**: Coordinates academic activities
- **Exam Controllers**: Manages examination processes

### Pain Points
- Coordinating across multiple institutes
- Standardizing policies while allowing flexibility
- Managing cross-institute resource conflicts
- Ensuring data consistency across institutes

### Success Metrics
- Enrollment targets achievement
- Academic performance standards
- Institute satisfaction levels
- Process efficiency
- Policy compliance

---

## Institute Admin Journey

### Who is Institute Admin?
Institute Admin manages day-to-day operations of a specific institute/college. They handle local master data, staff management, student services, and institute-level configuration.

### Typical Day in the Life

#### Morning: Daily Operations
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views institute-specific metrics
- Checks pending tasks and approvals
- Reviews today's schedule
- Monitors staff and student activity

**Notice Board Management**: NoticeBoardPage.tsx
- Posts institute announcements
- Reviews notice expiry
- Manages notice categories
- Pins important notices

**Staff Attendance Review**: AttendancePage.tsx
- Reviews staff attendance for today
- Identifies absent staff
- Approves leave requests
- Addresses attendance issues

#### Mid-Day: Academic Management
**Course and Batch Management**: MasterDataPage.tsx
- Manages institute-specific courses
- Creates and configures batches
- Manages sections within batches
- Configures batch-term structure

**Subject Management**: MasterDataPage.tsx
- Configures subjects for courses
- Sets up subject pools for electives
- Manages subject labels
- Configures prerequisite rules

**Staff-Subject Assignment**: MasterDataPage.tsx
- Assigns subjects to faculty
- Manages teaching loads
- Reviews subject allocation
- Adjusts assignments as needed

**Timetable Management**: TimetablePage.tsx
- Reviews current timetable
- Handles timetable adjustments
- Schedules special lectures
- Manages resource bookings

#### Afternoon: Student Services
**Student Onboarding**: OnboardStudentsPage.tsx
- Reviews new student registrations
- Manages student profile creation
- Assigns students to batches/sections
- Coordinates enrollment process

**Fee Management**: FeesPage.tsx
- Reviews fee collection status
- Approves fee concessions
- Manages refund requests
- Addresses fee payment issues

**Hostel Management**: HostelPage.tsx
- Reviews hostel occupancy
- Manages room allocations
- Addresses hostel complaints
- Manages hostel fee billing

**Transport Management**: TransportPage.tsx
- Reviews transport utilization
- Manages route assignments
- Issues transport passes
- Addresses transport issues

#### Evening: Approvals and Monitoring
**My Tasks**: MyTasksPage.tsx
- Reviews pending approval tasks
- Approves/rejects requests
- Delegates tasks if needed
- Follows up on overdue tasks

**Workflow Monitoring**: WorkflowMonitorPage.tsx
- Reviews institute workflow instances
- Identifies bottlenecks
- Monitors process completion
- Generates workflow reports

**User Management**: UserManagementPage.tsx
- Reviews new staff account requests
- Manages role assignments
- Addresses user access issues
- Manages staff profile updates

### Key Responsibilities

1. **Institute Operations**
   - Daily operational oversight
   - Staff management and coordination
   - Student services delivery
   - Infrastructure management

2. **Academic Administration**
   - Course and batch management
   - Subject and faculty assignment
   - Timetable management
   - Academic scheduling

3. **Student Services**
   - Student onboarding
   - Fee management
   - Hostel and transport services
   - Document issuance

4. **Approvals and Workflows**
   - Request approvals
   - Workflow monitoring
   - Process optimization
   - Staff support

### Screens Frequently Used
- DashboardPage.tsx
- MasterDataPage.tsx
- TimetablePage.tsx
- FeesPage.tsx
- HostelPage.tsx
- TransportPage.tsx
- MyTasksPage.tsx
- UserManagementPage.tsx
- NoticeBoardPage.tsx

### Decisions Made
- Course and batch creation
- Staff-subject assignments
- Timetable adjustments
- Fee concession approvals
- Hostel allocation decisions
- Resource booking approvals

### Interactions with Other Users
- **University Admin**: Receives guidance and reports
- **HODs**: Coordinates academic activities
- **Staff**: Provides support and oversight
- **Students**: Addresses issues and requests

### Pain Points
- Managing daily operational issues
- Coordinating with multiple departments
- Handling urgent student requests
- Balancing administrative and academic priorities

### Success Metrics
- Operational efficiency
- Staff and student satisfaction
- Process completion rates
- Issue resolution time
- Service delivery quality

---

## Student Journey

### Who is Student?
Student is the primary user of the system for academic activities, from enrollment to graduation. They access the system for academics, fees, examinations, and various services.

### Typical Day in the Life

#### Morning: Academic Dashboard
**Login**: LoginPage.tsx
- Enters student email and password
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views today's class schedule
- Checks upcoming deadlines
- Views attendance summary
- Reviews pending fee payments
- Checks notice board updates

**Timetable View**: TimetablePage.tsx
- Reviews today's classes
- Checks room locations
- Views faculty assignments
- Notes any schedule changes

#### Mid-Day: Academic Activities
**Attendance Check**: AttendancePage.tsx
- Views attendance record
- Checks attendance percentage
- Identifies any deficit areas
- Views attendance defaulter warnings

**Subject Enrollment**: ElectivesPage.tsx (if applicable)
- Views available elective subjects
- Selects preferred electives
- Submits election form
- Views enrollment status

**Library Access**: LibraryPage.tsx
- Searches for books
- Views borrowed books
- Checks due dates
- Reserves unavailable books
- Pays library fines if any

#### Afternoon: Services and Requests
**Fee Payment**: FeesPage.tsx
- Views pending fee demands
- Reviews fee breakdown
- Pays fees via Razorpay
- Downloads payment receipts
- Views payment history

**Document Requests**: FormsPage.tsx
- Requests documents (bonafide, ID card)
- Fills document request form
- Pays document fee if applicable
- Tracks request status
- Downloads issued documents

**Leave Application**: LeaveRequestsPage.tsx (if applicable - for research scholars/assignments)
- Applies for leave
- Views leave balance
- Tracks application status
- Views leave history

**Hostel Services**: HostelPage.tsx (if residing)
- Views hostel allocation details
- Pays hostel fees
- Submits complaints/requests
- Requests hostel services

#### Evening: Examinations and Results
**Exam Preparation**: ExaminationsPage.tsx
- Views exam schedule
- Downloads hall tickets
- Accesses previous year papers
- Takes practice tests if available

**Online Exam**: ExamTakePage.tsx (for CBE)
- Enters exam interface
- Takes proctored exam
- Submits answers
- Views submission confirmation

**Results View**: StudentProfilePage.tsx
- Views term results
- Checks SGPA/CGPA
- Downloads mark sheets
- Applies for revaluation if needed

**Profile Management**: StudentProfilePage.tsx
- Updates personal information
- Changes password
- Manages profile photo
- Updates contact details

### Key Responsibilities

1. **Academic Engagement**
   - Attend classes regularly
   - Maintain attendance requirements
   - Complete subject enrollment
   - Participate in examinations

2. **Financial Compliance**
   - Pay fees on time
   - Manage fee payments
   - Apply for concessions if eligible
   - Handle refund requests

3. **Service Utilization**
   - Use library services
   - Request documents
   - Access hostel/transport services
   - Utilize counselling services

4. **Profile Management**
   - Keep profile updated
   - Manage account security
   - Access academic records
   - Communicate with administration

### Screens Frequently Used
- DashboardPage.tsx
- TimetablePage.tsx
- AttendancePage.tsx
- FeesPage.tsx
- ExaminationsPage.tsx
- StudentProfilePage.tsx
- LibraryPage.tsx
- FormsPage.tsx
- ElectivesPage.tsx

### Decisions Made
- Subject/election selections
- Document requests
- Fee payment timing
- Leave applications
- Revaluation requests
- Service utilization choices

### Interactions with Other Users
- **Faculty**: Attend classes, seek guidance
- **HOD**: Academic issues, approvals
- **Admin**: Services, fees, documents
- **Librarian**: Library services
- **Counsellor**: Academic guidance

### Pain Points
- Fee payment deadlines
- Attendance requirements
- Document request delays
- Exam stress and technical issues
- Service request processing time

### Success Metrics
- Academic performance (SGPA/CGPA)
- Attendance compliance
- Fee payment timeliness
- Service satisfaction
- Profile completeness

---

## Teaching Faculty Journey

### Who is Teaching Faculty?
Teaching Faculty are academic staff responsible for teaching, assessment, and student guidance. They use the system for class management, attendance, examinations, and academic coordination.

### Typical Day in the Life

#### Morning: Class Preparation
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views today's class schedule
- Checks pending tasks
- Reviews student requests
- Views department notices

**Timetable Review**: TimetablePage.tsx
- Confirms today's class schedule
- Checks room assignments
- Views class timings
- Notes any special lectures

#### Mid-Day: Teaching Activities
**Attendance Marking**: AttendancePage.tsx
- Selects class for attendance
- Marks student attendance
- Adds attendance notes
- Submits attendance record
- Views attendance summary

**Class Management**: During class (physical)
- Uses system for class resources
- Accesses digital materials
- Records class notes if needed

**Student Interaction**: During/after class
- Addresses student queries
- Provides academic guidance
- Notes student issues
- Recommends counselling if needed

#### Afternoon: Assessment and Evaluation
**Exam Paper Creation**: ExaminationsPage.tsx
- Accesses question bank
- Creates exam papers
- Selects questions
- Sets marking scheme
- Reviews paper configuration

**Student Evaluation**: ExaminationsPage.tsx
- Grades student papers
- Enters marks
- Provides feedback
- Submits grades
- Reviews grade statistics

**Question Bank Contribution**: ExaminationsPage.tsx
- Adds new questions to bank
- Categorizes by difficulty
- Provides answer keys
- Reviews existing questions

#### Evening: Academic Coordination
**Subject Management**: MasterDataPage.tsx
- Reviews subject syllabus
- Updates subject materials
- Manages subject resources
- Coordinates with HOD

**Leave Application**: LeaveRequestsPage.tsx
- Applies for leave
- Views leave balance
- Checks class impact
- Submits leave request

**Invigilation Duty**: MyInvigilationPage.tsx
- Views assigned invigilation duties
- Checks exam schedules
- Reviews invigilation guidelines
- Reports invigilation issues

**My Tasks**: MyTasksPage.tsx
- Reviews pending approvals
- Approves student requests
- Provides recommendations
- Completes assigned tasks

### Key Responsibilities

1. **Teaching and Learning**
   - Conduct classes as per timetable
   - Mark student attendance
   - Provide academic guidance
   - Maintain teaching quality

2. **Assessment and Evaluation**
   - Create exam papers
   - Evaluate student performance
   - Provide timely feedback
   - Contribute to question bank

3. **Academic Coordination**
   - Coordinate with HOD
   - Participate in department activities
   - Contribute to curriculum development
   - Mentor students

4. **Professional Development**
   - Manage leave and duties
   - Participate in training
   - Contribute to research
   - Engage in academic activities

### Screens Frequently Used
- DashboardPage.tsx
- TimetablePage.tsx
- AttendancePage.tsx
- ExaminationsPage.tsx
- LeaveRequestsPage.tsx
- MyTasksPage.tsx
- MyInvigilationPage.tsx
- MasterDataPage.tsx

### Decisions Made
- Attendance marking
- Exam paper creation
- Student grading
- Leave applications
- Student recommendations
- Academic guidance

### Interactions with Other Users
- **Students**: Teaching, guidance, evaluation
- **HOD**: Academic coordination, reporting
- **Peers**: Subject coordination, sharing
- **Admin**: Services, requests
- **Exam Cell**: Exam coordination

### Pain Points
- Time management for multiple classes
- Balancing teaching and evaluation
- Managing student expectations
- Coordinating exam duties
- Keeping up with administrative tasks

### Success Metrics
- Student performance
- Attendance compliance
- Exam paper quality
- Student feedback
- Professional development

---

## HOD Journey

### Who is HOD?
Head of Department manages departmental academic operations, faculty coordination, and curriculum implementation. They bridge between institute administration and teaching faculty.

### Typical Day in the Life

#### Morning: Department Overview
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views departmental metrics
- Checks faculty attendance
- Reviews pending approvals
- Monitors departmental notices

**Faculty Coordination**: HRPage.tsx
- Reviews faculty attendance
- Addresses faculty issues
- Approves leave requests
- Manages faculty workload

#### Mid-Day: Academic Management
**Subject and Curriculum**: MasterDataPage.tsx
- Reviews subject offerings
- Coordinates curriculum implementation
- Manages subject allocations
- Reviews syllabus coverage

**Faculty-Subject Assignment**: MasterDataPage.tsx
- Assigns subjects to faculty
- Balances teaching loads
- Addresses allocation conflicts
- Reviews faculty expertise

**Attendance Monitoring**: AttendancePage.tsx
- Reviews departmental attendance
- Identifies defaulters
- Addresses attendance issues
- Monitors faculty compliance

**Timetable Coordination**: TimetablePage.tsx
- Reviews department timetable
- Addresses scheduling conflicts
- Approves special lectures
- Coordinates resource allocation

#### Afternoon: Student and Examination Management
**Student Academic Performance**: AnalyticsPage.tsx
- Reviews student performance
- Identifies at-risk students
- Coordinates remedial actions
- Monitors result trends

**Examination Coordination**: ExaminationsPage.tsx
- Reviews exam schedules
- Coordinates paper setting
- Monitors exam conduct
- Reviews result processing

**Elective Management**: ElectivesPage.tsx
- Approves elective offerings
- Reviews student elections
- Addresses capacity issues
- Finalizes elective allocations

#### Evening: Approvals and Reporting
**My Tasks**: MyTasksPage.tsx
- Reviews departmental approvals
- Approves student requests
- Addresses faculty requests
- Completes administrative tasks

**Workflow Monitoring**: WorkflowMonitorPage.tsx
- Reviews departmental workflows
- Monitors approval timelines
- Identifies bottlenecks
- Optimizes processes

**Department Reporting**: AnalyticsPage.tsx
- Generates departmental reports
- Reviews performance metrics
- Identifies improvement areas
- Plans academic initiatives

### Key Responsibilities

1. **Department Leadership**
   - Faculty management and coordination
   - Academic planning and implementation
   - Departmental administration
   - Resource allocation

2. **Academic Quality**
   - Curriculum implementation
   - Teaching quality monitoring
   - Student performance oversight
   - Academic standards maintenance

3. **Faculty Development**
   - Workload management
   - Professional development support
   - Performance evaluation
   - Mentoring and guidance

4. **Student Success**
   - Academic performance monitoring
   - Student support coordination
   - Remedial action planning
   - Career guidance facilitation

### Screens Frequently Used
- DashboardPage.tsx
- MasterDataPage.tsx
- TimetablePage.tsx
- AttendancePage.tsx
- ExaminationsPage.tsx
- HRPage.tsx
- AnalyticsPage.tsx
- MyTasksPage.tsx
- ElectivesPage.tsx

### Decisions Made
- Faculty-subject assignments
- Leave approvals
- Academic policy implementation
- Student academic interventions
- Resource allocation
- Curriculum adjustments

### Interactions with Other Users
- **Institute Admin**: Reporting and coordination
- **Faculty**: Management and support
- **Students**: Academic guidance
- **Other HODs**: Coordination and collaboration
- **University Admin**: Policy implementation

### Pain Points
- Balancing administrative and academic roles
- Managing faculty conflicts
- Addressing student performance issues
- Coordinating with multiple stakeholders
- Resource constraints

### Success Metrics
- Departmental academic performance
- Faculty satisfaction
- Student success rates
- Process efficiency
- Administrative compliance

---

## Librarian Journey

### Who is Librarian?
Librarian manages library operations including book circulation, catalog management, and reader services. They ensure smooth library operations and support academic needs.

### Typical Day in the Life

#### Morning: Library Operations
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views library statistics
- Checks today's due items
- Reviews pending reservations
- Monitors library notices

**Library Configuration**: LibraryPage.tsx (Settings)
- Reviews library policies
- Configures loan periods
- Sets fine rates
- Updates library rules

#### Mid-Day: Circulation Services
**Book Issue**: LibraryPage.tsx (Circulation)
- Processes book issue requests
- Validates student eligibility
- Updates book status
- Sets due dates
- Issues receipts

**Book Return**: LibraryPage.tsx (Circulation)
- Processes book returns
- Calculates overdue fines
- Updates book availability
- Creates fine demands
- Notifies reserved students

**Reservation Management**: LibraryPage.tsx
- Processes book reservations
- Manages reservation queue
- Notifies available books
- Expires old reservations

**Catalog Management**: LibraryPage.tsx (Catalog)
- Adds new books to catalog
- Updates book information
- Manages book copies
- Assigns categories and locations

#### Afternoon: Library Services
**Fine Management**: FeesPage.tsx
- Reviews library fine payments
- Processes fine waivers if applicable
- Addresses fine disputes
- Updates fine records

**Library Analytics**: AnalyticsPage.tsx
- Reviews circulation statistics
- Identifies popular books
- Monitors collection utilization
- Generates library reports

**User Support**: During operations
- Assists students with book search
- Resolves circulation issues
- Provides library orientation
- Addresses user complaints

#### Evening: Closing Tasks
**Daily Reconciliation**: LibraryPage.tsx
- Reconciles daily circulation
- Identifies discrepancies
- Updates library statistics
- Prepares daily reports

**Inventory Management**: LibraryPage.tsx
- Reviews book availability
- Identifies missing/damaged books
- Plans acquisition requests
- Updates inventory records

**Notice Board**: NoticeBoardPage.tsx
- Posts library announcements
- Updates library hours
- Notifies new arrivals
- Manages library notices

### Key Responsibilities

1. **Library Operations**
   - Book circulation management
   - Catalog maintenance
   - User service delivery
   - Library policy enforcement

2. **Collection Management**
   - Book acquisition and processing
   - Inventory management
   - Collection development
   - Preservation and maintenance

3. **User Services**
   - Circulation services
   - Reference assistance
   - Library orientation
   - User support

4. **Library Administration**
   - Policy implementation
   - Statistics and reporting
   - Budget management
   - Staff coordination

### Screens Frequently Used
- DashboardPage.tsx
- LibraryPage.tsx
- FeesPage.tsx
- NoticeBoardPage.tsx
- AnalyticsPage.tsx
- UserManagementPage.tsx

### Decisions Made
- Book acquisition decisions
- Fine waiver decisions
- Library policy adjustments
- Reservation prioritization
- Service hours decisions

### Interactions with Other Users
- **Students**: Circulation services, assistance
- **Faculty**: Collection development support
- **Admin**: Library administration
- **Vendors**: Book acquisition

### Pain Points
- Managing high circulation volume
- Handling overdue items
- Reserving popular books
- Maintaining inventory accuracy
- Balancing budget and needs

### Success Metrics
- Circulation statistics
- User satisfaction
- Collection utilization
- Fine collection rate
- Inventory accuracy

---

## Accountant Journey

### Who is Accountant?
Accountant manages financial operations including fee collection, payment processing, and financial reporting. They ensure timely fee collection and accurate financial records.

### Typical Day in the Life

#### Morning: Financial Overview
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views today's payment targets
- Checks pending fee demands
- Reviews collection statistics
- Monitors refund requests

**Fee Collection**: FeesPage.tsx
- Processes fee payments
- Records manual payments
- Generates receipts
- Updates payment records
- Handles payment queries

#### Mid-Day: Fee Management
**Fee Structure Review**: ProgramFeeManager.tsx
- Reviews fee structures
- Updates fee components if needed
- Configures payment schedules
- Manages fee heads

**Concession Management**: FeesPage.tsx
- Reviews concession applications
- Verifies eligibility
- Approves/rejects concessions
- Updates fee records

**Scholarship Processing**: FeesPage.tsx
- Processes scholarship applications
- Verifies eligibility criteria
- Calculates scholarship amounts
- Updates student fee records

#### Afternoon: Refunds and Reimbursements
**Refund Processing**: FeesPage.tsx
- Reviews refund requests
- Verifies refund eligibility
- Processes refund transactions
- Updates financial records
- Generates refund receipts

**Government Reimbursements**: FeesPage.tsx
- Processes government scholarship claims
- Verifies student eligibility
- Submits reimbursement claims
- Tracks claim status
- Records reimbursement receipts

**Financial Reporting**: AnalyticsPage.tsx
- Generates daily collection reports
- Reviews fee collection trends
- Identifies defaulters
- Prepares financial summaries

#### Evening: Reconciliation and Follow-up
**Payment Reconciliation**: FeesPage.tsx
- Reconciles daily payments
- Identifies discrepancies
- Updates financial records
- Prepares bank deposits

**Defaulter Management**: FeesPage.tsx
- Identifies fee defaulters
- Generates defaulter lists
- Sends payment reminders
- Initiates recovery actions

**My Tasks**: MyTasksPage.tsx
- Reviews financial approval tasks
- Approves financial requests
- Processes payment-related workflows
- Completes assigned tasks

### Key Responsibilities

1. **Fee Collection**
   - Process fee payments
   - Generate receipts
   - Manage payment records
   - Handle payment queries

2. **Financial Management**
   - Manage fee structures
   - Process concessions
   - Handle scholarships
   - Manage reimbursements

3. **Refund Processing**
   - Process refund requests
   - Verify eligibility
   - Execute refund transactions
   - Maintain refund records

4. **Financial Reporting**
   - Generate financial reports
   - Monitor collection trends
   - Identify defaulters
   - Prepare financial summaries

### Screens Frequently Used
- DashboardPage.tsx
- FeesPage.tsx
- ProgramFeeManager.tsx
- AnalyticsPage.tsx
- MyTasksPage.tsx
- UserManagementPage.tsx

### Decisions Made
- Concession approvals
- Refund processing
- Payment dispute resolution
- Defaulter classification
- Financial reporting decisions

### Interactions with Other Users
- **Students**: Fee collection, queries
- **Admin**: Financial reporting
- **Finance Head**: Policy guidance
- **Banks**: Payment processing

### Pain Points
- High payment volume management
- Handling payment disputes
- Processing refund requests
- Managing defaulters
- Maintaining accurate records

### Success Metrics
- Fee collection rate
- Payment processing accuracy
- Refund processing time
- Defaulter recovery rate
- Financial reporting accuracy

---

## Warden Journey

### Who is Warden?
Warden manages hostel operations including room allocation, student welfare, and hostel facility management. They ensure safe and comfortable hostel living for students.

### Typical Day in the Life

#### Morning: Hostel Operations
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views hostel occupancy
- Checks pending requests
- Reviews hostel notices
- Monitors hostel activities

**Room Allocation**: HostelPage.tsx
- Reviews allocation requests
- Allocates rooms to students
- Updates room occupancy
- Manages room changes
- Handles vacating requests

#### Mid-Day: Student Welfare
**Student Issues**: HostelPage.tsx
- Addresses student complaints
- Handles maintenance requests
- Resolves student conflicts
- Provides student support

**Hostel Facilities**: HostelPage.tsx
- Monitors facility conditions
- Coordinates maintenance
- Manages common areas
- Ensures safety standards

**Attendance and Discipline**: HostelPage.tsx
- Monitors student attendance
- Enforces hostel rules
- Addresses disciplinary issues
- Maintains discipline records

#### Afternoon: Fee and Administration
**Hostel Fee Management**: FeesPage.tsx
- Reviews hostel fee payments
- Processes fee concessions
- Manages mess fee billing
- Handles fee queries

**Refund Processing**: HostelPage.tsx
- Reviews security deposit refund requests
- Verifies room condition
- Processes refund approvals
- Updates refund records

**Hostel Configuration**: HostelPage.tsx
- Reviews hostel policies
- Configures fee components
- Manages hostel rules
- Updates hostel information

#### Evening: Safety and Reporting
**Safety Checks**: Physical rounds
- Conducts safety rounds
- Checks facility security
- Monitors student activities
- Addresses safety concerns

**Daily Reporting**: HostelPage.tsx
- Generates daily reports
- Documents incidents
- Updates hostel records
- Reports to administration

**Notice Board**: NoticeBoardPage.tsx
- Posts hostel notices
- Updates hostel rules
- Communicates with students
- Manages hostel announcements

### Key Responsibilities

1. **Hostel Management**
   - Room allocation and management
   - Student welfare and support
   - Facility maintenance
   - Safety and security

2. **Student Discipline**
   - Rule enforcement
   - Attendance monitoring
   - Disciplinary action
   - Conflict resolution

3. **Financial Management**
   - Hostel fee collection
   - Refund processing
   - Mess fee management
   - Financial record keeping

4. **Administration**
   - Policy implementation
   - Report generation
   - Staff coordination
   - Parent communication

### Screens Frequently Used
- DashboardPage.tsx
- HostelPage.tsx
- FeesPage.tsx
- NoticeBoardPage.tsx
- MyTasksPage.tsx
- UserManagementPage.tsx

### Decisions Made
- Room allocation decisions
- Disciplinary actions
- Refund approvals
- Maintenance prioritization
- Policy enforcement decisions

### Interactions with Other Users
- **Students**: Daily interaction and support
- **Admin**: Reporting and coordination
- **Maintenance staff**: Facility management
- **Parents**: Communication and updates

### Pain Points
- Managing student behavior
- Handling maintenance issues
- Balancing enforcement and welfare
- Processing refund requests
- Ensuring safety standards

### Success Metrics
- Student satisfaction
- Facility maintenance quality
- Fee collection rate
- Disciplinary incident rate
- Safety compliance

---

## Applicant Journey

### Who is Applicant?
Applicant is a prospective student who is applying for admission to the university. They interact with the system for registration, application submission, fee payment, and admission tracking.

### Application Journey

#### Step 1: Discovery and Information
**Access**: Public website or landing page
- Learns about programs offered
- Reviews admission requirements
- Understands application process
- Prepares necessary documents

#### Step 2: Registration
**Registration Page**: RegisterPage.tsx
- Enters personal information
- Provides contact details
- Selects applicant role
- Creates password
- Submits registration

**OTP Verification**: RegisterPage.tsx
- Receives OTP via email/SMS
- Enters OTP for verification
- Account activated on success

#### Step 3: Application Form
**Application Form**: StudentApplicationsPage.tsx or public form
- Fills personal details
- Provides academic history
- Uploads documents (marksheets, ID proofs)
- Selects program preferences
- Uploads photograph
- Saves draft as needed

#### Step 4: Application Fee Payment
**Payment Gateway**: Razorpay integration
- Views application fee amount
- Proceeds to payment
- Completes payment via Razorpay
- Receives payment confirmation

#### Step 5: Application Tracking
**Application Status**: StudentApplicationsPage.tsx
- Tracks application status
- Views coordinator review status
- Monitors approver decision
- Receives status notifications

#### Step 6: Counselling (Optional)
**Counselling Desk**: CounsellingDeskPage.tsx
- Requests counselling guidance
- Interacts with counsellor
- Receives program recommendations
- Gets application assistance

#### Step 7: Admission and Seat Allocation
**Admission Status**: StudentApplicationsPage.tsx
- Receives admission offer
- Views seat allocation details
- Accepts admission offer
- Proceeds to fee payment

#### Step 8: Admission Fee Payment
**Fee Payment**: FeesPage.tsx
- Views admission fee breakdown
- Pays admission fee via Razorpay
- Receives payment confirmation
- Downloads fee receipt

#### Step 9: Onboarding
**Onboarding**: OnboardStudentsPage.tsx (admin side)
- Completes profile setup
- Provides additional information
- Gets student ID assigned
- Receives login credentials

#### Step 10: Enrollment
**Student Portal**: Student journey begins
- Logs in as student
- Accesses academic services
- Begins academic journey

### Key Interactions

1. **Registration Process**
   - Create account
   - Verify identity
   - Complete profile

2. **Application Submission**
   - Fill application form
   - Upload documents
   - Pay application fee

3. **Application Tracking**
   - Monitor status
   - Respond to queries
   - Provide additional information

4. **Admission Process**
   - Receive offer
   - Accept admission
   - Pay admission fee

5. **Onboarding**
   - Complete enrollment
   - Get student ID
   - Access student services

### Screens Used
- RegisterPage.tsx
- StudentApplicationsPage.tsx
- CounsellingDeskPage.tsx
- FeesPage.tsx
- LoginPage.tsx (after enrollment)

### Decisions Made
- Program selection
- Document preparation
- Payment timing
- Admission acceptance
- Counselling utilization

### Interactions with Other Users
- **Admission Coordinators**: Application review
- **Approvers**: Admission decision
- **Counsellors**: Guidance and support
- **Finance Officers**: Fee processing

### Pain Points
- Document preparation and upload
- Application fee payment
- Waiting for admission decision
- Understanding process requirements
- Onboarding complexity

### Success Metrics
- Application completion rate
- Document accuracy
- Fee payment timeliness
- Admission conversion rate
- Onboarding success

---

## Parent Journey

### Who is Parent?
Parent is a guardian who wants to monitor their child's academic progress, fee payments, and overall performance. They access the system through the parent portal or linked accounts.

### Typical Monitoring Journey

#### Step 1: Account Setup
**Parent Linking**: StudentProfilePage.tsx (student initiates)
- Student links parent account
- Parent receives invitation
- Creates parent account
- Verifies relationship

#### Step 2: Dashboard Access
**Parent Dashboard**: Parent portal (accessed via login)
- Views child's academic summary
- Checks attendance status
- Reviews fee payment status
- Monitors overall performance

#### Step 3: Academic Monitoring
**Academic Performance**: StudentProfilePage.tsx (parent view)
- Views term results
- Checks SGPA/CGPA
- Reviews subject-wise performance
- Downloads mark sheets

**Attendance Monitoring**: AttendancePage.tsx (parent view)
- Views attendance record
- Checks attendance percentage
- Identifies attendance issues
- Reviews attendance trends

#### Step 4: Fee Management
**Fee Status**: FeesPage.tsx (parent view)
- Views pending fee demands
- Reviews payment history
- Checks fee payment status
- Pays fees on behalf of child

#### Step 5: Communication
**Notice Board**: NoticeBoardPage.tsx
- Views institute notices
- Checks examination schedules
- Reviews holiday announcements
- Monitors event notifications

**Direct Communication**: Through system
- Communicates with teachers
- Contacts administration
- Receives important alerts
- Responds to queries

#### Step 6: Reports and Analytics
**Performance Reports**: AnalyticsPage.tsx (parent view)
- Views academic performance trends
- Reviews attendance patterns
- Monitors fee payment history
- Generates progress reports

### Key Monitoring Activities

1. **Academic Performance**
   - Track grades and results
   - Monitor subject performance
   - Identify areas of concern
   - Review teacher feedback

2. **Attendance Monitoring**
   - Check daily attendance
   - Monitor attendance trends
   - Address attendance issues
   - Ensure compliance

3. **Fee Management**
   - View fee obligations
   - Make timely payments
   - Track payment history
   - Manage concessions

4. **Communication**
   - Receive school communications
   - Contact teachers/administration
   - Respond to queries
   - Provide feedback

### Screens Used
- Parent Dashboard (if separate portal)
- StudentProfilePage.tsx (parent view)
- AttendancePage.tsx (parent view)
- FeesPage.tsx (parent view)
- NoticeBoardPage.tsx

### Decisions Made
- Fee payment timing
- Communication preferences
- Academic support decisions
- Extra-curricular participation

### Interactions with Other Users
- **Child**: Monitor and support
- **Teachers**: Academic communication
- **Administration**: Fee and general queries
- **Other Parents**: Community interaction

### Pain Points
- Understanding academic performance
- Managing fee payments
- Interpreting attendance data
- Communication gaps
- Technical access issues

### Success Metrics
- Child's academic performance
- Fee payment compliance
- Attendance compliance
- Communication effectiveness
- Parent satisfaction

---

## Counsellor Journey

### Who is Counsellor?
Counsellor provides guidance to applicants for program selection, career advice, and admission support. They are empanelled by the university and compensated based on enrollment attribution.

### Typical Day in the Life

#### Morning: Request Review
**Login**: LoginPage.tsx
- Enters credentials
- Navigates to Dashboard

**Dashboard Review**: DashboardPage.tsx
- Views pending counselling requests
- Checks assigned requests
- Reviews response targets
- Monitors enrollment credits

#### Mid-Day: Counselling Sessions
**Counselling Desk**: CounsellingDeskPage.tsx
- Reviews assigned requests
- Studies applicant profiles
- Prepares guidance materials
- Initiates counselling conversation

**Guidance Delivery**: CounsellingDeskPage.tsx
- Provides program information
- Discusss career options
- Recommends suitable programs
- Answers applicant questions
- Guides application process

**Follow-up Communication**: CounsellingDeskPage.tsx
- Responds to applicant queries
- Provides additional information
- Shares program details
- Assists with application

#### Afternoon: Application Support
**Application Assistance**: CounsellingDeskPage.tsx
- Helps applicants with forms
- Reviews application details
- Provides document guidance
- Assists with fee payment process

**Application Tracking**: CounsellingDeskPage.tsx
- Monitors submitted applications
- Tracks admission status
- Provides status updates
- Assists with next steps

#### Evening: Reporting and Compensation
**Performance Review**: CounsellingAdminPage.tsx
- Reviews counselling statistics
- Monitors response time
- Tracks enrollment attribution
- Views compensation details

**Documentation**: CounsellingDeskPage.tsx
- Documents counselling sessions
- Records recommendations made
- Updates applicant profiles
- Maintains interaction history

**Feedback Collection**: CounsellingDeskPage.tsx
- Requests applicant feedback
- Reviews ratings received
- Identifies improvement areas
- Updates counselling approach

### Key Responsibilities

1. **Applicant Guidance**
   - Provide program information
   - Offer career advice
   - Assist with application process
   - Support decision making

2. **Communication**
   - Respond to applicant queries
   - Provide timely information
   - Maintain professional communication
   - Build rapport with applicants

3. **Application Support**
   - Assist with form filling
   - Guide document preparation
   - Support fee payment process
   - Track application status

4. **Performance Management**
   - Meet response time targets
   - Achieve enrollment attribution
   - Maintain quality ratings
   - Improve counselling effectiveness

### Screens Frequently Used
- DashboardPage.tsx
- CounsellingDeskPage.tsx
- CounsellingAdminPage.tsx
- AnalyticsPage.tsx

### Decisions Made
- Program recommendations
- Application guidance
- Communication priorities
- Follow-up strategies
- Improvement initiatives

### Interactions with Other Users
- **Applicants**: Primary interaction
- **University Admin**: Contract and compensation
- **Admission Team**: Application coordination
- **Other Counsellors**: Best practice sharing

### Pain Points
- Managing high request volume
- Providing timely responses
- Achieving enrollment targets
- Maintaining quality ratings
- Handling difficult cases

### Success Metrics
- Response time
- Enrollment attribution
- Applicant satisfaction ratings
- Application completion rate
- Compensation earned

---

## Summary

This UniversityERP system serves diverse user types with distinct journeys:

**Administrative Users:**
- SuperAdmin: System-wide configuration and oversight
- University Admin: Academic governance and coordination
- Institute Admin: Day-to-day operations and management

**Academic Users:**
- Student: Learning, assessment, and services
- Teaching Faculty: Teaching, evaluation, and guidance
- HOD: Department leadership and coordination

**Support Staff:**
- Librarian: Library services and management
- Accountant: Financial operations and reporting
- Warden: Hostel management and student welfare

**External Users:**
- Applicant: Admission process and onboarding
- Parent: Student monitoring and support
- Counsellor: Guidance and enrollment support

Each user journey is designed to:
- Support the user's primary responsibilities
- Provide relevant information and tools
- Enable efficient task completion
- Facilitate communication with stakeholders
- Support decision-making processes

The system's role-based access control ensures users see only relevant features and data, while workflow automation streamlines approval processes and notifications keep all stakeholders informed.

---

**Document Version**: 1.0  
**Last Updated**: 2025-08-05
