# Module System

## Purpose

This document explains the module system used in the University ERP backend. It details the module structure, module organization, and module dependencies.

## Why This Document Exists

**Confirmed by Code**: The University ERP backend has 36 modules organized by domain. Understanding the module system is critical for:
- Navigating the codebase
- Understanding module dependencies
- Creating new modules
- Refactoring existing modules
- Understanding code organization

Without understanding the module system, developers may struggle to find code or understand the architecture.

## Where This Is Used

- **Onboarding**: New developers learn module structure
- **Feature Development**: Creating new features in modules
- **Code Reviews**: Understanding module dependencies
- **Refactoring**: Refactoring module structure
- **Architecture Reviews**: Evaluating module architecture

## Dependencies

### Module Dependencies

**Confirmed by Code**: Modules depend on:

- **NestJS Module System**: Module organization
- **Shared Modules**: Infrastructure modules
- **Domain Modules**: Business logic modules
- **PrismaModule**: Database access
- **RedisModule**: Caching
- **MinioModule**: Object storage

## Internal Architecture

### Module Hierarchy

**Confirmed by Code**: Modules are organized in a hierarchy.

```
┌─────────────────────────────────────────────────────────┐
│                  AppModule                                │
│                  (Root Module)                            │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Infrastructure│  │  Domain         │  │  Feature        │
│  Modules      │  │  Modules        │  │  Modules        │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Module Categories

**Confirmed by Code**: Modules are categorized by type.

**Infrastructure Modules**:
- **ConfigModule**: Configuration management
- **PrismaModule**: Database access
- **RedisModule**: Caching
- **MinioModule**: Object storage
- **BullModule**: Queue management

**Domain Modules**:
- **AuthModule**: Authentication
- **MasterDataModule**: Master data management
- **AdmissionsModule**: Admissions management
- **AcademicModule**: Academic management
- **AttendanceModule**: Attendance tracking
- **ExaminationModule**: Examination system
- **FeeModule**: Fee management
- **TimetableModule**: Timetable management
- **LibraryModule**: Library management
- **HostelModule**: Hostel management
- **TransportModule**: Transport management
- **HrModule**: Human resources
- **DocumentsModule**: Document management
- **WorkflowModule**: Workflow engine
- **NotificationsModule**: Notifications
- **NoticeBoardModule**: Notice board
- **BannersModule**: Banner management
- **UsersModule**: User management
- **SettingsModule**: Settings management
- **FormsModule**: Dynamic forms
- **AnalyticsModule**: Analytics
- **AuditModule**: Audit logging
- **CounsellingModule**: Counselling
- **SocialMonitoringModule**: Social media monitoring
- **ResourceReservationModule**: Resource reservation

## Code Walkthrough

### Module Definition

**Confirmed by Code**: Modules follow NestJS module pattern.

**Example Module**:
```typescript
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    RedisModule,
  ],
  controllers: [MyController],
  providers: [MyService],
  exports: [MyService],
})
export class MyModule {}
```

**What This Does**:
- **imports**: Imports required modules
- **controllers**: Registers controllers
- **providers**: Registers providers
- **exports**: Exports providers for other modules

### Module Structure

**Confirmed by Code**: Each module has a standard structure.

```
my-module/
├── my-module.controller.ts
├── my-module.service.ts
├── my-module.module.ts
├── dto/
│   ├── create-my-module.dto.ts
│   ├── update-my-module.dto.ts
│   └── query-my-module.dto.ts
├── entities/
│   └── my-module.entity.ts
└── tests/
    ├── my-module.controller.spec.ts
    └── my-module.service.spec.ts
```

**What This Does**:
- Organizes module files
- Separates concerns
- Enables testing
- Maintains consistency

### Module Registration

**Confirmed by Code**: Modules registered in AppModule.

**AppModule**:
```typescript
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    RedisModule,
    MinioModule,
    BullModule.forRoot({
      redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT),
      },
    }),
    AuthModule,
    MasterDataModule,
    AdmissionsModule,
    AcademicModule,
    AttendanceModule,
    ExaminationModule,
    FeeModule,
    TimetableModule,
    LibraryModule,
    HostelModule,
    TransportModule,
    HrModule,
    DocumentsModule,
    WorkflowModule,
    NotificationsModule,
    NoticeBoardModule,
    BannersModule,
    UsersModule,
    SettingsModule,
    FormsModule,
    AnalyticsModule,
    AuditModule,
    CounsellingModule,
    SocialMonitoringModule,
    ResourceReservationModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

**What This Does**:
- Registers all modules
- Configures global modules
- Sets up infrastructure
- Enables module communication

## Database Interactions

### PrismaModule

**Confirmed by Code**: PrismaModule provides database access.

**PrismaModule Definition**:
```typescript
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

**PrismaService**:
```typescript
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

**Usage in Modules**:
```typescript
@Module({
  imports: [PrismaModule],
  providers: [MyService],
})
export class MyModule {
  constructor(private prisma: PrismaService) {}
}
```

## Redis Interactions

### RedisModule

**Confirmed by Code**: RedisModule provides caching.

**RedisModule Definition**:
```typescript
@Module({
  providers: [RedisService],
  exports: [RedisService],
})
export class RedisModule {}
```

**RedisService**:
```typescript
@Injectable()
export class RedisService extends Redis implements OnModuleDestroy {
  constructor(configService: ConfigService) {
    super({
      host: configService.get<string>('REDIS_HOST', 'localhost'),
      port: configService.get<number>('REDIS_PORT', 6379),
    });
  }

  async onModuleDestroy() {
    await this.quit();
  }
}
```

**Usage in Modules**:
```typescript
@Module({
  imports: [RedisModule],
  providers: [MyService],
})
export class MyModule {
  constructor(private redis: RedisService) {}
}
```

## Queue Interactions

### BullModule

**Confirmed by Code**: BullModule provides queue management.

**BullModule Definition**:
```typescript
@Module({
  imports: [
    BullModule.forRoot({
      redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT),
      },
    }),
    BullModule.registerQueue({
      name: 'notifications',
    }),
  ],
  controllers: [NotificationController],
  providers: [NotificationService],
})
export class NotificationModule {}
```

**Usage in Modules**:
```typescript
@Injectable()
export class NotificationService {
  constructor(
    @InjectQueue('notifications') private notificationsQueue: Queue,
  ) {}

  async sendEmail(data: EmailDto) {
    await this.notificationsQueue.add('email', data);
  }
}
```

## Worker Interactions

### Worker Modules

**Confirmed by Code**: Workers are separate modules in worker services.

**Notification Worker Module**:
```typescript
@Module({
  imports: [
    BullModule.forRoot({
      redis: {
        host: process.env.REDIS_HOST,
        port: parseInt(process.env.REDIS_PORT),
      },
    }),
    BullModule.registerQueue({
      name: 'notifications',
    }),
  ],
  processors: [NotificationProcessor],
})
export class NotificationWorkerModule {}
```

## Business Rules

### Module Rules

**Confirmed by Code**: Modules follow these rules:

1. **Single Responsibility**: Each module handles one domain
2. **Encapsulation**: Modules encapsulate their providers
3. **Reusability**: Modules can be imported by other modules
4. **Export Services**: Services exported for use in other modules
5. **Shared Infrastructure**: Infrastructure modules shared by all modules

### Module Dependency Rules

**Confirmed by Code**: Module dependencies follow these rules:

1. **No Circular Dependencies**: Avoid circular dependencies
2. **Infrastructure First**: Infrastructure modules imported first
3. **Domain Modules**: Domain modules can import infrastructure modules
4. **Feature Modules**: Feature modules can import domain modules
5. **Lazy Loading**: Large modules can be lazy loaded

## Security

### Module Security

**Confirmed by Code**: Security considerations for modules:

1. **Module Isolation**: Modules isolated from each other
2. **Guard Application**: Guards applied at module level
3. **Service Access**: Services access controlled by guards
4. **Data Scoping**: Data scoped by tenant
5. **Audit Logging**: All writes audited

## Performance Considerations

### Module Performance

**Confirmed by Code**: Performance considerations for modules:

1. **Lazy Loading**: Large modules can be lazy loaded
2. **Shared Services**: Services shared across modules
3. **Connection Pooling**: Database connections pooled
4. **Caching**: Frequently accessed data cached
5. **Module Size**: Keep modules focused and small

## Common Mistakes

### Mistake 1: Circular Dependencies

**Symptom**: Application fails to start

**Cause**: Circular dependency between modules

**Fix**:
```typescript
// Wrong
@Module({
  imports: [ModuleB],
})
export class ModuleA {}

@Module({
  imports: [ModuleA],
})
export class ModuleB {}

// Correct - Extract shared code to separate module
@Module({
  imports: [SharedModule],
})
export class ModuleA {}

@Module({
  imports: [SharedModule],
})
export class ModuleB {}
```

### Mistake 2: Not Exporting Services

**Symptom**: Service not available in other modules

**Cause**: Not exporting service from module

**Fix**:
```typescript
// Wrong
@Module({
  providers: [MyService],
})
export class MyModule {}

// Correct
@Module({
  providers: [MyService],
  exports: [MyService],
})
export class MyModule {}
```

### Mistake 3: Large Modules

**Symptom**: Module hard to maintain

**Cause**: Module too large with too much code

**Fix**:
```typescript
// Split large module into smaller modules
// Extract shared code to separate module
// Keep modules focused on single responsibility
```

## Debugging Guide

### Module Debugging

**Issue**: Module not working

**Investigation**:
1. Check module is registered in AppModule
2. Check module imports
3. Check module exports
4. Check provider registration
5. Check module logs

**Tools**:
- NestJS CLI
- Application logs
- Module inspector
- Dependency injection debugger

## Future Enhancements

### Dynamic Module Loading

**Status**: Not implemented

**Proposal**: Implement dynamic module loading:
- Load modules on demand
- Reduce initial load time
- Better performance
- Dynamic feature flags

### Module Federation

**Status**: Not implemented

**Proposal**: Implement module federation:
- Share modules across applications
- Independent deployment
- Better scalability
- Micro-frontend architecture

## Production Considerations

### Production Modules

**Production Deployment**:
- Lazy load non-critical modules
- Optimize module loading
- Monitor module performance
- Monitor module dependencies
- Optimize module size

### Module Monitoring

**Monitoring Metrics**:
- Module load time
- Module memory usage
- Module dependencies
- Module performance
- Module errors

## Example Requests

### Create New Module

**Request**: Create a new module

**Implementation**:
```bash
# Using NestJS CLI
nest g module my-module
nest g controller my-module
nest g service my-module
```

## Example Responses

### Module Structure

**Response**: Module structure

```
my-module/
├── my-module.controller.ts
├── my-module.service.ts
├── my-module.module.ts
└── dto/
    ├── create-my-module.dto.ts
    └── update-my-module.dto.ts
```

## Sequence Diagrams

### Module Loading

```
Application Start
        ↓
    Load AppModule
        ↓
    Load Infrastructure Modules
        ↓
    Load Domain Modules
        ↓
    Register Controllers
        ↓
    Register Providers
        ↓
    Application Ready
```

## Architecture Diagrams

### Module Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  AppModule                                │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Infrastructure│  │  Auth Module   │  │  Academic      │
│  Modules      │  │                │  │  Module        │
└────────────────┘  └────────────────┘  └─────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Shared Services                           │
│  PrismaService, RedisService, MinioService              │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How does the NestJS module system work?

**Answer**: NestJS module system:
- Modules encapsulate related functionality
- Modules can import other modules
- Modules can export providers
- Modules define controllers and providers
- Modules enable code organization and reusability

### Q2: How do you avoid circular dependencies in modules?

**Answer**: Avoid circular dependencies via:
- Extract shared code to separate module
- Use dependency injection carefully
- Use forwardRef if necessary
- Refactor module structure
- Keep modules focused

### Q3: How do you optimize module performance?

**Answer**: Optimize module performance via:
- Lazy load non-critical modules
- Keep modules focused and small
- Share services across modules
- Optimize module dependencies
- Monitor module performance

## Exercises

### Exercise 1: Create a New Module

**Task**: Create a new NestJS module.

**Steps**:
1. Use NestJS CLI to generate module
2. Generate controller
3. Generate service
4. Generate DTOs
5. Register module in AppModule
6. Test module

**Verification**:
- Module created
- Controller works
- Service works
- Module registered

### Exercise 2: Refactor Module

**Task**: Refactor a large module.

**Steps**:
1. Identify large module
2. Split into smaller modules
3. Extract shared code
4. Update imports
5. Test refactored code

**Verification**:
- Modules split
- Shared code extracted
- Imports updated
- Tests pass

## Real Production Scenarios

### Scenario 1: Module Load Time Slow

**Situation**: Application slow to start

**Response**:
1. Identify slow modules
2. Implement lazy loading
3. Optimize module dependencies
4. Test performance
5. Monitor load time

### Scenario 2: Module Dependency Issue

**Situation**: Module dependency causing issues

**Response**:
1. Identify dependency issue
2. Refactor to remove circular dependency
3. Extract shared code
4. Update imports
5. Test refactored code

## Navigation

**Next Section**: [03-Controllers](./03-Controllers.md)

**Previous Section**: [01-NestJS-Framework](./01-NestJS-Framework.md)

**Related Documentation**:
- [01-NestJS-Framework](./01-NestJS-Framework.md) - NestJS framework
- [04-Services](./04-Services.md) - Services
- [08-Modules](../08-Modules/README.md) - All modules
