# Data Flow

## Overview

This document provides comprehensive information about data flow in the University ERP system. It details how data moves through the system, from user input to storage and back, including all transformations and processing steps.

## Data Flow Principles

**Confirmed by Code**: The system follows clear data flow principles.

**Principles:**
1. **Unidirectional Data Flow**: Data flows in one direction
2. **Immutable Data**: Data is not mutated directly
3. **Single Source of Truth**: Database is the source of truth
4. **Caching Layer**: Redis provides caching for performance
5. **Validation at Boundaries**: Data is validated at entry points

## Request-Response Data Flow

### User Registration Flow

**Confirmed by Code**: User registration follows a specific data flow.

**Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Client Request                                          │
├─────────────────────────────────────────────────────────────────┤
│ Client → POST /api/auth/register                               │
│ {                                                               │
│   "email": "user@example.com",                                  │
│   "password": "password123",                                    │
│   "name": "John Doe",                                          │
│   "role": "STUDENT"                                            │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: API Gateway                                             │
├─────────────────────────────────────────────────────────────────┤
│ - Route request to auth module                                  │
│ - Log request                                                   │
│ - Check rate limiting                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Validation Pipe                                         │
├─────────────────────────────────────────────────────────────────┤
│ - Validate email format                                         │
│ - Validate password strength                                    │
│ - Validate required fields                                      │
│ - Transform DTO                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Auth Controller                                          │
├─────────────────────────────────────────────────────────────────┤
│ @Post('register')                                               │
│ async register(@Body() dto: RegisterDto) {                     │
│   return this.authService.register(dto);                        │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Auth Service                                            │
├─────────────────────────────────────────────────────────────────┤
│ async register(dto: RegisterDto) {                              │
│   // Check if user exists                                       │
│   const existingUser = await this.userRepo.findByEmail(        │
│     dto.email                                                   │
│   );                                                            │
│   if (existingUser) {                                          │
│     throw new ConflictException('Email already exists');       │
│   }                                                             │
│                                                                 │
│   // Hash password                                              │
│   const hashedPassword = await bcrypt.hash(dto.password, 10);   │
│                                                                 │
│   // Create user                                                │
│   const user = await this.userRepo.create({                     │
│     email: dto.email,                                           │
│     passwordHash: hashedPassword,                               │
│     name: dto.name,                                             │
│     role: dto.role,                                             │
│   });                                                           │
│                                                                 │
│   // Cache user                                                 │
│   await this.cacheService.set(`user:${user.id}`, user, 3600);   │
│                                                                 │
│   // Queue welcome email                                        │
│   await this.queueService.add('email', {                        │
│     to: user.email,                                             │
│     subject: 'Welcome to University ERP',                       │
│     body: 'Welcome email content',                              │
│   });                                                           │
│                                                                 │
│   // Generate tokens                                            │
│   const tokens = await this.generateTokens(user);                │
│                                                                 │
│   return { user, ...tokens };                                  │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: User Repository                                         │
├─────────────────────────────────────────────────────────────────┤
│ async findByEmail(email: string) {                              │
│   // Check cache first                                          │
│   const cached = await this.cacheService.get(`user:email:${email}`);│
│   if (cached) return cached;                                    │
│                                                                 │
│   // Query database                                             │
│   const user = await this.prisma.user.findUnique({               │
│     where: { email },                                           │
│   });                                                           │
│                                                                 │
│   // Cache result                                               │
│   if (user) {                                                   │
│     await this.cacheService.set(                                │
│       `user:email:${email}`,                                    │
│       user,                                                     │
│       3600                                                      │
│     );                                                          │
│   }                                                             │
│                                                                 │
│   return user;                                                  │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Cache Service                                           │
├─────────────────────────────────────────────────────────────────┤
│ async get<T>(key: string): Promise<T | null> {                  │
│   const cached = await this.redis.get(key);                     │
│   if (!cached) return null;                                     │
│   return JSON.parse(cached) as T;                               │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 8: Redis                                                   │
├─────────────────────────────────────────────────────────────────┤
│ GET user:email:user@example.com                                 │
│ Response: null (cache miss)                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 9: Prisma ORM                                              │
├─────────────────────────────────────────────────────────────────┤
│ SELECT * FROM users WHERE email = 'user@example.com'            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 10: PostgreSQL                                             │
├─────────────────────────────────────────────────────────────────┤
│ Execute query                                                   │
│ Return: null (user not found)                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 11: User Repository (Create)                               │
├─────────────────────────────────────────────────────────────────┤
│ async create(data: CreateUserDto) {                            │
│   const user = await this.prisma.user.create({                   │
│     data,                                                        │
│   });                                                           │
│   return user;                                                  │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 12: Prisma ORM                                              │
├─────────────────────────────────────────────────────────────────┤
│ INSERT INTO users (email, password_hash, name, role)           │
│ VALUES ('user@example.com', 'hashed_password', 'John Doe', 'STUDENT')│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 13: PostgreSQL                                             │
├─────────────────────────────────────────────────────────────────┤
│ Execute INSERT                                                  │
│ Return: created user data                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 14: Cache User                                             │
├─────────────────────────────────────────────────────────────────┤
│ await this.cacheService.set(`user:${user.id}`, user, 3600);     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 15: Redis                                                   │
├─────────────────────────────────────────────────────────────────┤
│ SET user:user-id {user_data} EX 3600                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 16: Queue Email                                             │
├─────────────────────────────────────────────────────────────────┤
│ await this.queueService.add('email', { ... });                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 17: Bull Queue                                             │
├─────────────────────────────────────────────────────────────────┤
│ Add job to email queue                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 18: Redis                                                   │
├─────────────────────────────────────────────────────────────────┤
│ Store job in Redis                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 19: Generate Tokens                                         │
├─────────────────────────────────────────────────────────────────┤
│ async generateTokens(user: User) {                              │
│   const payload = { sub: user.id, email: user.email, role: user.role };│
│   const accessToken = this.jwtService.sign(payload, {            │
│     expiresIn: '1h',                                              │
│   });                                                           │
│   const refreshToken = this.jwtService.sign(payload, {          │
│     expiresIn: '7d',                                              │
│   });                                                           │
│   return { accessToken, refreshToken };                         │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 20: Auth Service Response                                   │
├─────────────────────────────────────────────────────────────────┤
│ return {                                                         │
│   user: {                                                       │
│     id: user.id,                                                 │
│     email: user.email,                                           │
│     name: user.name,                                             │
│     role: user.role,                                             │
│   },                                                            │
│   accessToken,                                                  │
│   refreshToken,                                                 │
│ };                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 21: Auth Controller Response                                │
├─────────────────────────────────────────────────────────────────┤
│ return {                                                         │
│   success: true,                                                │
│   data: { user, accessToken, refreshToken },                     │
│ };                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 22: HTTP Response                                           │
├─────────────────────────────────────────────────────────────────┤
│ Status: 201 Created                                             │
│ Body: {                                                         │
│   success: true,                                                │
│   data: { user, accessToken, refreshToken },                     │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 23: Client Response                                         │
├─────────────────────────────────────────────────────────────────┤
│ Store tokens in localStorage                                     │
│ Redirect to dashboard                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Attendance Marking Flow

**Confirmed by Code**: Attendance marking follows a specific data flow.

**Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Staff Marks Attendance                                   │
├─────────────────────────────────────────────────────────────────┤
│ Client → POST /api/attendance/mark                               │
│ {                                                               │
│   "studentId": "student-1",                                      │
│   "subjectId": "subject-1",                                      │
│   "date": "2024-01-01",                                         │
│   "status": "PRESENT"                                           │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Auth Guard                                              │
├─────────────────────────────────────────────────────────────────┤
│ - Validate JWT token                                            │
│ - Check user role (must be STAFF or ADMIN)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Attendance Controller                                   │
├─────────────────────────────────────────────────────────────────┤
│ @Post('mark')                                                    │
│ @UseGuards(JwtAuthGuard, RolesGuard)                            │
│ @Roles('STAFF', 'ADMIN')                                        │
│ async mark(@Body() dto: MarkAttendanceDto) {                     │
│   return this.attendanceService.mark(dto);                       │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Attendance Service                                      │
├─────────────────────────────────────────────────────────────────┤
│ async mark(dto: MarkAttendanceDto) {                            │
│   // Check if attendance already marked                         │
│   const existing = await this.attendanceRepo.findExisting(      │
│     dto.studentId,                                              │
│     dto.subjectId,                                              │
│     dto.date                                                    │
│   );                                                            │
│   if (existing) {                                               │
│     throw new ConflictException('Attendance already marked');   │
│   }                                                             │
│                                                                 │
│   // Create attendance record                                   │
│   const attendance = await this.attendanceRepo.create({         │
│     studentId: dto.studentId,                                    │
│     subjectId: dto.subjectId,                                    │
│     date: dto.date,                                             │
│     status: dto.status,                                         │
│     markedBy: this.currentUser.id,                               │
│   });                                                           │
│                                                                 │
│   // Invalidate cache                                            │
│   await this.cacheService.delete(`attendance:${dto.studentId}`);│
│                                                                 │
│   // Emit attendance marked event                                │
│   this.eventService.emit('attendance.marked', {                  │
│     studentId: dto.studentId,                                    │
│     subjectId: dto.subjectId,                                    │
│     status: dto.status,                                         │
│   });                                                           │
│                                                                 │
│   return attendance;                                            │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Attendance Repository                                   │
├─────────────────────────────────────────────────────────────────┤
│ async findExisting(studentId, subjectId, date) {                │
│   return this.prisma.attendance.findUnique({                     │
│     where: {                                                    │
│       studentId_subjectId_date: {                                 │
│         studentId,                                               │
│         subjectId,                                               │
│         date: new Date(date),                                    │
│       },                                                        │
│     },                                                          │
│   });                                                           │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Prisma ORM                                              │
├─────────────────────────────────────────────────────────────────┤
│ SELECT * FROM attendance                                        │
│ WHERE student_id = 'student-1'                                  │
│   AND subject_id = 'subject-1'                                  │
│   AND date = '2024-01-01'                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: PostgreSQL                                             │
├─────────────────────────────────────────────────────────────────┤
│ Execute query                                                   │
│ Return: null (no existing record)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 8: Attendance Repository (Create)                          │
├─────────────────────────────────────────────────────────────────┤
│ async create(data: CreateAttendanceDto) {                       │
│   return this.prisma.attendance.create({                         │
│     data,                                                        │
│     include: {                                                  │
│       student: true,                                             │
│       subject: true,                                             │
│     },                                                          │
│   });                                                           │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 9: Prisma ORM                                              │
├─────────────────────────────────────────────────────────────────┤
│ INSERT INTO attendance (student_id, subject_id, date, status, marked_by)│
│ VALUES ('student-1', 'subject-1', '2024-01-01', 'PRESENT', 'staff-1')│
│ RETURNING *                                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 10: PostgreSQL                                            │
├─────────────────────────────────────────────────────────────────┤
│ Execute INSERT                                                  │
│ Return: created attendance with relations                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 11: Invalidate Cache                                       │
├─────────────────────────────────────────────────────────────────┤
│ await this.cacheService.delete(`attendance:${dto.studentId}`);   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 12: Redis                                                  │
├─────────────────────────────────────────────────────────────────┤
│ DEL attendance:student-1                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 13: Emit Event                                             │
├─────────────────────────────────────────────────────────────────┤
│ this.eventService.emit('attendance.marked', { ... });          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 14: Event Service                                          │
├─────────────────────────────────────────────────────────────────┤
│ - Publish event to subscribers                                  │
│ - WebSocket gateway receives event                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 15: WebSocket Gateway                                      │
├─────────────────────────────────────────────────────────────────┤
│ - Send notification to student's WebSocket connection            │
│ - Update real-time attendance status                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 16: Client (Student Portal)                                │
├─────────────────────────────────────────────────────────────────┤
│ - Receive WebSocket notification                                 │
│ - Update UI with new attendance status                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 17: HTTP Response                                          │
├─────────────────────────────────────────────────────────────────┤
│ Status: 201 Created                                             │
│ Body: {                                                         │
│   success: true,                                                │
│   data: attendance,                                             │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Background Job Data Flow

### Email Sending Flow

**Confirmed by Code**: Email sending uses queue-based processing.

**Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Job Added to Queue                                       │
├─────────────────────────────────────────────────────────────────┤
│ Service → queueService.add('email', {                            │
│   to: 'user@example.com',                                       │
│   subject: 'Welcome',                                          │
│   body: 'Welcome email',                                        │
│ })                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Bull Queue                                              │
├─────────────────────────────────────────────────────────────────┤
│ - Create job object                                              │
│ - Add job to Redis list                                         │
│ - Set job status to 'waiting'                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Redis                                                    │
├─────────────────────────────────────────────────────────────────┤
│ LPUSH bull:email:waiting {job_data}                             │
│ HSET bull:email:job-id {job_metadata}                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Worker Polls Queue                                      │
├─────────────────────────────────────────────────────────────────┤
│ Worker → getNextJob('email')                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Bull Queue                                              │
├─────────────────────────────────────────────────────────────────┤
│ - Move job from waiting to active                                │
│ - Update job status to 'active'                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Redis                                                    │
├─────────────────────────────────────────────────────────────────┤
│ LREM bull:email:waiting {job_data}                              │
│ LPUSH bull:email:active {job_data}                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 7: Worker Processes Job                                     │
├─────────────────────────────────────────────────────────────────┤
│ Processor → process(job)                                       │
│ {                                                               │
│   const { to, subject, body } = job.data;                       │
│   await this.emailService.send(to, subject, body);               │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 8: Email Service                                           │
├─────────────────────────────────────────────────────────────────┤
│ async send(to, subject, body) {                                 │
│   await this.transporter.sendMail({                             │
│     from: 'noreply@university.edu',                             │
│     to,                                                          │
│     subject,                                                     │
│     html: body,                                                 │
│   });                                                           │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 9: SMTP Server                                              │
├─────────────────────────────────────────────────────────────────┤
│ - Receive email request                                         │
│ - Process email                                                 │
│ - Deliver to recipient                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 10: Worker Completes Job                                    │
├─────────────────────────────────────────────────────────────────┤
│ Processor → job.progress(100)                                   │
│ Processor → job.done({ success: true })                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 11: Bull Queue                                              │
├─────────────────────────────────────────────────────────────────┤
│ - Move job from active to completed                              │
│ - Update job status to 'completed'                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 12: Redis                                                    │
├─────────────────────────────────────────────────────────────────┤
│ LREM bull:email:active {job_data}                               │
│ LPUSH bull:email:completed {job_data}                            │
└─────────────────────────────────────────────────────────────────┘
```

## WebSocket Data Flow

### Real-time Notification Flow

**Confirmed by Code**: WebSocket enables real-time notifications.

**Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Client Connects to WebSocket                             │
├─────────────────────────────────────────────────────────────────┤
│ Client → ws://localhost:3000?token=<jwt_token>                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: WebSocket Gateway                                        │
├─────────────────────────────────────────────────────────────────┤
│ @WebSocketGateway()                                              │
│ handleConnection(client: Socket) {                              │
│   // Validate token                                              │
│   const token = client.handshake.auth.token;                     │
│   const user = await this.authService.validateToken(token);      │
│                                                                 │
│   // Join user room                                             │
│   client.join(`user:${user.id}`);                                │
│                                                                 │
│   // Store client connection                                    │
│   this.connections.set(user.id, client);                         │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Server Emits Event                                      │
├─────────────────────────────────────────────────────────────────┤
│ Service → eventService.emit('notification', {                    │
│   userId: 'user-1',                                             │
│   title: 'Attendance Marked',                                   │
│   message: 'Your attendance has been marked',                    │
│ })                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Event Service                                            │
├─────────────────────────────────────────────────────────────────┤
│ - Publish event to subscribers                                  │
│ - WebSocket gateway receives event                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: WebSocket Gateway                                        │
├─────────────────────────────────────────────────────────────────┤
│ async handleNotification(data) {                                │
│   const client = this.connections.get(data.userId);             │
│   if (client) {                                                 │
│     client.emit('notification', data);                           │
│   }                                                             │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Client Receives Event                                   │
├─────────────────────────────────────────────────────────────────┤
│ Client → socket.on('notification', (data) => {                   │
│   console.log('Received notification:', data);                   │
│   // Update UI                                                  │
│   showNotification(data);                                        │
│ });                                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Transformation

### DTO to Entity Transformation

**Confirmed by Code**: Data transforms between layers.

**Transformation Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Client Request (DTO)                                   │
├─────────────────────────────────────────────────────────────────┤
│ {                                                               │
│   "email": "user@example.com",                                  │
│   "password": "password123",                                    │
│   "name": "John Doe"                                            │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Validation Pipe                                         │
├─────────────────────────────────────────────────────────────────┤
│ - Validate email format                                         │
│ - Validate password strength                                    │
│ - Transform to internal DTO                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Service Layer                                          │
├─────────────────────────────────────────────────────────────────┤
│ - Hash password                                                 │
│ - Add default values                                            │
│ - Transform to entity                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: Repository Layer                                       │
├─────────────────────────────────────────────────────────────────┤
│ - Map to Prisma model                                           │
│ - Prepare for database                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 5: Database (Entity)                                      │
├─────────────────────────────────────────────────────────────────┤
│ {                                                               │
│   "id": "user-id",                                              │
│   "email": "user@example.com",                                  │
│   "password_hash": "hashed_password",                           │
│   "name": "John Doe",                                           │
│   "role": "STUDENT",                                            │
│   "is_active": true,                                            │
│   "email_verified": false,                                      │
│   "created_at": "2024-01-01T10:00:00.000Z",                     │
│   "updated_at": "2024-01-01T10:00:00.000Z"                      │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

### Entity to Response Transformation

**Confirmed by Code**: Response data transforms for client.

**Transformation Flow:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Database (Entity)                                      │
├─────────────────────────────────────────────────────────────────┤
│ {                                                               │
│   "id": "user-id",                                              │
│   "email": "user@example.com",                                  │
│   "password_hash": "hashed_password",                           │
│   "name": "John Doe",                                           │
│   "role": "STUDENT",                                            │
│   "is_active": true,                                            │
│   "email_verified": false,                                      │
│   "created_at": "2024-01-01T10:00:00.000Z",                     │
│   "updated_at": "2024-01-01T10:00:00.000Z"                      │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Repository Layer                                       │
├─────────────────────────────────────────────────────────────────┤
│ - Remove sensitive fields (password_hash)                        │
│ - Transform to internal model                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Service Layer                                          │
├─────────────────────────────────────────────────────────────────┤
│ - Add computed fields                                           │
│ - Format dates                                                  │
│ - Transform to response DTO                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: Controller Layer                                       │
├─────────────────────────────────────────────────────────────────┤
│ - Wrap in standard response format                              │
│ - Add metadata                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 5: Client Response (DTO)                                  │
├─────────────────────────────────────────────────────────────────┤
│ {                                                               │
│   "success": true,                                              │
│   "data": {                                                     │
│     "id": "user-id",                                            │
│     "email": "user@example.com",                                │
│     "name": "John Doe",                                         │
│     "role": "STUDENT",                                          │
│     "isActive": true,                                           │
│     "emailVerified": false,                                     │
│     "createdAt": "2024-01-01T10:00:00.000Z",                    │
│     "updatedAt": "2024-01-01T10:00:00.000Z"                     │
│   }                                                             │
│ }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Data Consistency

**Confirmed by Code**: The system ensures data consistency.

### Transaction Flow

**Confirmed by Code**: Transactions ensure data consistency.

**Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Begin Transaction                                      │
├─────────────────────────────────────────────────────────────────┤
│ await this.prisma.$transaction(async (tx) => {                  │
│   // All operations in this transaction                         │
│ });                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Operation 1                                             │
├─────────────────────────────────────────────────────────────────┤
│ const user = await tx.user.create({                             │
│   data: { email, passwordHash, name, role },                    │
│ });                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Operation 2                                             │
├─────────────────────────────────────────────────────────────────┤
│ const student = await tx.student.create({                       │
│   data: { userId: user.id, rollNumber, batch, course },         │
│ });                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Operation 3                                             │
├─────────────────────────────────────────────────────────────────┤
│ await tx.enrollment.createMany({                                │
│   data: subjects.map(subject => ({                              │
│     studentId: student.id,                                      │
│     subjectId: subject.id,                                      │
│     semester: 1,                                                │
│   })),                                                          │
│ });                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Commit Transaction                                     │
├─────────────────────────────────────────────────────────────────┤
│ // If all operations succeed, commit                           │
│ // If any operation fails, rollback                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Step 6: Invalidate Cache                                       │
├─────────────────────────────────────────────────────────────────┤
│ await this.cacheService.invalidate('user:*');                   │
│ await this.cacheService.invalidate('student:*');                │
└─────────────────────────────────────────────────────────────────┘
```

## Data Security

**Confirmed by Code**: Data security is enforced at multiple layers.

### Security Flow

**Flow Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Input Validation                                      │
├─────────────────────────────────────────────────────────────────┤
│ - Validate data types                                           │
│ - Validate data format                                          │
│ - Sanitize input                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Authentication                                         │
├─────────────────────────────────────────────────────────────────┤
│ - Validate JWT token                                            │
│ - Check token expiration                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Authorization                                          │
├─────────────────────────────────────────────────────────────────┤
│ - Check user role                                               │
│ - Check permissions                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: Data Encryption                                        │
├─────────────────────────────────────────────────────────────────┤
│ - Encrypt sensitive data at rest                                │
│ - Encrypt data in transit (TLS)                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 5: Output Filtering                                       │
├─────────────────────────────────────────────────────────────────┤
│ - Remove sensitive fields from response                         │
│ - Mask sensitive data                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Next Steps

After understanding data flow:

1. **Read Component Diagrams**: Understand component interactions
2. **Read API Documentation**: Understand API endpoints
3. **Read Database Guide**: Understand data model
4. **Read Caching Guide**: Understand caching strategies

## Additional Resources

- [Data Flow Diagrams](https://www.uml-diagrams.org/data-flow-diagrams.html)
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
