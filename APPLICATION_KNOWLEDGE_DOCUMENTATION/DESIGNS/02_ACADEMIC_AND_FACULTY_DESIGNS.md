# UI Design Specs: Academic & Faculty Management Screens

## Pages Covered
- `MasterDataPage.tsx`
- `ElectivesPage.tsx`
- `TimetablePage.tsx`
- `AttendancePage.tsx`
- `DirectoryPage.tsx`

---

## 1. Master Data Management Page (`MasterDataPage.tsx`)

### Screen Purpose
Central administrative console for building and maintaining the multi-tenant university structure, institute entities, departments, programs, batches, terms, and versioned rules (`StreamLabel` & `SubjectLabel`).

### Visual Wireframe & Layout Structure
```
┌──────────────────────────────────────────────────────────────┐
│  Academic Structure & Master Data                            │
│  [ Universities ] [ Institutes ] [ Programs ] [ Version Rules]│
├──────────────────────────────────────────────────────────────┤
│  Institute List                               [ + Add New ]  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Code  │ Institute Name        │ Depts │ Head │ Status  │  │
│  ├───────┼───────────────────────┼───────┼──────┼─────────┤  │
│  │ ENG01 │ School of Engineering │   6   │ Dr.A │ ACTIVE  │  │
│  │ MED02 │ School of Medicine    │   4   │ Dr.B │ ACTIVE  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Component Breakdown & Specs
- **Top Tab Bar**: Horizontal tab strip with pills (`Universities`, `Institutes`, `Departments`, `Programs`, `Stream Labels`, `Subject Catalog`).
- **Entity Data Table**: High-density table with sorting, search filtering, inline action buttons (`Edit`, `Manage Rules`, `Deactivate`).
- **Stream Label Rules Modal**: Slide-over panel for configuring immutable batch graduation rules (e.g. Total Credits required: 160, Core Subject Credits: 120, Elective Credits: 40).

---

## 2. Interactive Timetable Scheduler Page (`TimetablePage.tsx`)

### Screen Purpose
Grid view displaying class schedules per section, room allocation, and faculty availability. Supports auto-scheduler solver execution and manual drag-and-drop slot adjustments.

### Layout & Component Specs
- **Weekly Schedule Matrix**: 7-column grid (Monday to Sunday) across period time slots (8:00 AM to 5:00 PM).
- **Class Slot Cards**: Rounded grid cards color-coded by subject type:
  - Lecture: Blue gradient container (`bg-blue-950/40 border-blue-800`)
  - Lab Session: Emerald gradient container (`bg-emerald-950/40 border-emerald-800`)
  - Tutorial: Purple gradient container (`bg-purple-950/40 border-purple-800`)
- **Conflict Highlight Overlay**: Red pulse outline (`ring-2 ring-rose-500 animate-pulse`) displayed over slots with faculty or classroom double-booking conflicts.

---

## 3. Attendance Recording Page (`AttendancePage.tsx`)

### Screen Purpose
Allows teaching faculty to mark daily class attendance, review attendance percentages, and generate low-attendance alert notices.

### Layout & Component Specs
- **Attendance Toggle Grid**: Student list with quick toggle buttons for each student (`PRESENT` green pill / `ABSENT` red pill / `EXCUSED` yellow pill).
- **Summary Header Widget**: Donut chart showing overall session attendance percentage (e.g. `88% Present - 44 / 50 Students`).
