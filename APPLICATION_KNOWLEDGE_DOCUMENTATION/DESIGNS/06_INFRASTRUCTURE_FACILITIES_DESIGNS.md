# UI Design Specs: Infrastructure & Facilities Screens

## Pages Covered
- `HostelPage.tsx`
- `TransportPage.tsx`
- `LibraryPage.tsx`

---

## 1. Hostel Allocation & Mess Management Page (`HostelPage.tsx`)

### Screen Purpose
Manages hostel blocks, floor plans, room allocations, bed capacity, mess fee demands, and warden gate pass approval workflows.

### Layout & Component Specs
- **Hostel Block Grid**: Card view of hostel blocks (e.g. Block A - Boys, Block B - Girls) showing occupancy percentage (e.g. `180 / 200 Beds Occupied (90%)`).
- **Visual Room Matrix**: Grid of room cards color-coded by occupancy state:
  - Green (`Full Occupancy`)
  - Yellow (`Partial Bed Available`)
  - Slate (`Empty Room`)
- **Gate Pass Approval Panel**: Data list of pending gate pass requests with warden approval/rejection toggle buttons.

---

## 2. Transport Management Page (`TransportPage.tsx`)

### Screen Purpose
Manages bus routes, pickup stops, vehicle fleet tracking, driver assignments, and bus pass generation.

### Layout & Component Specs
- **Route Cards**: Route timeline cards displaying Route Name, Bus Number, Driver Contact, Stop Sequence (e.g. Stop 1: Campus -> Stop 2: Main Sq -> Stop 3: North Station), and enrolled student counts.
- **Bus Pass Generator Widget**: Card view displaying student bus pass with QR code verification stamp.

---

## 3. Library Circulation Console Page (`LibraryPage.tsx`)

### Screen Purpose
Manages book catalog search, ISBN circulation (issue/return), digital book reservations, and library fine tracking.

### Layout & Component Specs
- **Book Search Catalog**: Grid layout of book covers with real-time stock count (`Available: 3 Copies / Total: 10`).
- **Circulation Issue Form**: Modal for scanning student barcode and book ISBN to execute instant loan checkout.
