# UI Design Specs: Infrastructure & Facilities Screens

## Pages Covered
- `HostelPage.tsx`
- `TransportPage.tsx`
- `LibraryPage.tsx`
- Resource Reservation & Optimisation (embedded in Settings/Workflows)

---

## 1. Hostel Allocation & Management Page (`HostelPage.tsx`)

### Screen Purpose
Comprehensive hostel management (67KB) covering hostel blocks, floor plans, room allocations, bed capacity, mess fee components, room rates, warden settings, student requests (with waitlist), refunds, occupancy reports, and bulk fee operations.

### Layout & Component Specs
- **Hostel Block Grid**: Card view of hostel blocks showing occupancy percentage, gender type, warden details.
- **Visual Room Matrix**: Grid of room cards color-coded by occupancy state:
  - Green: Full Occupancy
  - Yellow: Partial Bed Available
  - Slate: Empty Room
- **Student Request Panel** (`HostelRequestSection.tsx`): Student-facing hostel application form, request tracking, waitlist position.
- **Allocation Management**: Room/bed assignment, confirmation, release with fee adjustment.
- **Fee Components**: Hostel-specific fee heads (Room, Mess, Maintenance) with rate tables per room type.
- **Reports Dashboard**: Summary, occupancy, and vacancy reports.

### Hostel API Endpoints
| Category | Method | Endpoint | Purpose |
|:---|:---|:---|:---|
| **Requests** | POST | `/api/hostel/requests` | Student submits hostel request |
| | GET | `/api/hostel/requests` | List all requests |
| | GET | `/api/hostel/requests/mine` | My requests (student) |
| | GET | `/api/hostel/requests/waitlist` | Waitlist queue |
| | PATCH | `/api/hostel/requests/:id` | Update request status |
| | DELETE | `/api/hostel/requests/:id` | Cancel request |
| **Hostels** | POST | `/api/hostel/hostels` | Create hostel block |
| | GET | `/api/hostel/hostels` | List hostels |
| | PATCH | `/api/hostel/hostels/:id` | Update hostel |
| | DELETE | `/api/hostel/hostels/:id` | Delete hostel |
| | GET | `/api/hostel/hostels/export` | Export fee data |
| | POST | `/api/hostel/hostels/bulk` | Bulk fee operations |
| **Rooms** | POST | `/api/hostel/rooms` | Create room |
| | GET | `/api/hostel/rooms` | List rooms with filters |
| | PATCH | `/api/hostel/rooms/:id` | Update room |
| | DELETE | `/api/hostel/rooms/:id` | Delete room |
| | GET | `/api/hostel/rooms/:id/occupants` | Room occupant list |
| **Fee Config** | GET | `/api/hostel/hostels/:id/components` | Fee components |
| | GET | `/api/hostel/hostels/:id/room-rates` | Room rate table |
| | PUT | `/api/hostel/hostels/:id/room-rates` | Save rates |
| | PUT | `/api/hostel/hostels/:id/settings` | Save hostel settings |
| | POST | `/api/hostel/components` | Create fee component |
| | PATCH | `/api/hostel/components/:id` | Update component |
| | DELETE | `/api/hostel/components/:id` | Delete component |
| **Allocations** | POST | `/api/hostel/allocations` | Block room for student |
| | GET | `/api/hostel/allocations` | List allocations |
| | GET | `/api/hostel/allocations/student/:id` | Student allocation |
| | PATCH | `/api/hostel/allocations/:id/confirm` | Confirm allocation |
| | PATCH | `/api/hostel/allocations/:id/release` | Release room |
| **Config** | GET | `/api/hostel/config` | Get hostel module config |
| | PATCH | `/api/hostel/config` | Update config |
| **Reports** | GET | `/api/hostel/reports/summary` | Summary dashboard |
| | GET | `/api/hostel/reports/occupancy` | Occupancy report |
| | GET | `/api/hostel/reports/vacant` | Vacant rooms report |

### Backend Services
- **`hostel.service.ts`**: Core hostel CRUD, room management, allocation logic, fee component management.
- **`hostel-request.service.ts`**: Student request lifecycle, waitlist management, auto-allocation.
- **`hostel-refund.service.ts`**: Refund processing on room release, prorated calculation.

---

## 2. Transport Management Page (`TransportPage.tsx`)

### Screen Purpose
Manages bus routes, pickup stops, vehicle fleet tracking, driver assignments, bus pass generation, and student enrollment in transport.

### Layout & Component Specs
- **Route Cards**: Timeline cards displaying Route Name, Bus Number, Driver Contact, Stop Sequence, enrolled student count.
- **Bus Pass Generator**: Student bus pass card with QR code verification.
- **Student Enrollment**: Route assignment, pass generation, and fee linkage.

### Transport API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| POST | `/api/transport/routes` | Create route |
| GET | `/api/transport/routes` | List routes |
| PATCH | `/api/transport/routes/:id` | Update route |
| DELETE | `/api/transport/routes/:id` | Delete route |
| POST | `/api/transport/stops` | Create stop |
| POST | `/api/transport/vehicles` | Create vehicle |
| POST | `/api/transport/enrollments` | Enroll student |
| GET | `/api/transport/enrollments` | List enrollments |

---

## 3. Library Circulation Console (`LibraryPage.tsx`)

### Screen Purpose
Manages book catalog search, ISBN circulation (issue/return), digital reservations, library fine tracking, and overdue notifications.

### Layout & Component Specs
- **Book Search Catalog**: Grid layout of book covers with real-time stock count.
- **Circulation Issue Form**: Modal for scanning student barcode and book ISBN.
- **Fine Tracking**: Automatic overdue fine calculation.

### Library API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/library/books` | Search book catalog |
| POST | `/api/library/loans/issue` | Issue book loan |
| POST | `/api/library/loans/return` | Return book |
| GET | `/api/library/loans` | List active loans |
| GET | `/api/library/fines` | List fines |

### Backend Services
- **`library.service.ts`**: Core library operations.
- **`library-scheduler.service.ts`**: Scheduled overdue checks and notification dispatch.

---

## 4. Resource Reservation Module (`resource-reservation.controller.ts`)

### Screen Purpose
Manages booking of campus resources (classrooms, labs, auditoriums) for events, exams, and special sessions.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/resource-reservation` | List reservations |
| POST | `/api/resource-reservation` | Create reservation |
| PATCH | `/api/resource-reservation/:id` | Update reservation |
| DELETE | `/api/resource-reservation/:id` | Cancel reservation |

### Backend Services
- **`resource-reservation.service.ts`**: Reservation CRUD, conflict detection.
- **`scheduler.service.ts`**: Automated hold expiration and cleanup.

---

## 5. Resource Optimisation Module (`resource-optimisation.controller.ts`)

### Screen Purpose
Analytics and optimization recommendations for campus resource utilization — identifies underused rooms, suggests timetable improvements, and tracks space efficiency metrics.

### API Endpoints
| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | `/api/resource-optimisation` | Get optimization analysis |
| GET | `/api/resource-optimisation/utilization` | Utilization metrics |
