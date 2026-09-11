# Enterprise Field Mapping Matrix & Core Data Dictionary
## 4-Way Technical Cross-Reference: Legacy CSV $\longleftrightarrow$ UI Input $\longleftrightarrow$ DTO Property $\longleftrightarrow$ Prisma DB Column

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-MIG-DICT-V4.2
CLASSIFICATION: DATA ARCHITECTURE & RELATIONAL MAPPING SPECIFICATION
TARGET AUDIENCE: ETL DEVELOPERS, FULL-STACK ENGINEERS, DATABASE ADMINISTRATORS, SYSTEM AUDITORS
========================================================================================================================
```

---

## Executive Overview & Dictionary Architecture

A common point of failure during campus ERP implementations is misalignment between:
1. **The Legacy CSV / Excel header** provided by institutional clerks.
2. **The React UI Input Element** exposed in the administrative front-end.
3. **The NestJS DTO property** received by the backend API controller.
4. **The Prisma ORM Schema column** persisted into PostgreSQL.

This document establishes the authoritative, unbroken 4-way cross-reference across all core entities in **UniversityERP**.

---

## 1. University Master Catalog & Organization

| Legacy CSV Column | UI Input Element / Label | API DTO Property (`bulk-import.dto.ts`) | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `code` | Input: "Department Code" | `departments[].code` | `UniversityDepartment.code` | `VARCHAR(50) NOT NULL` | Unique within University; Uppercase alphanumeric |
| `name` | Input: "Department Name" | `departments[].name` | `UniversityDepartment.name` | `VARCHAR(255) NOT NULL` | Full legal faculty name |
| `isAcademic` | Checkbox: "Academic Dept" | `departments[].isAcademic` | `UniversityDepartment.isAcademic` | `BOOLEAN DEFAULT true` | Distinguishes teaching vs administrative units |
| `departmentCode` | Select: "Faculty / Dept" | `courses[].departmentCode` | `UniversityDepartment.code` (FK lookup) | `UUID NOT NULL` | Resolved to `UniversityDepartment.id` |
| `courseCode` | Input: "Degree Code" | `courses[].code` | `UniversityCourse.code` | `VARCHAR(50) NOT NULL` | e.g. `BTECH`, `MBA`, `BCA` |
| `programCode` | Input: "Program / Stream Code"| `programs[].code` | `UniversityStream.code` | `VARCHAR(50) NOT NULL` | e.g. `CSE`, `ECE`, `MECH` |
| `totalCredits` | Number: "Graduation Credits"| `programs[].totalCredits` | `StreamLabel.totalCredits` | `INTEGER NOT NULL DEFAULT 160`| NEP 2020 minimum degree credits |
| `unitCount` | Number: "Terms / Semesters" | `programs[].unitCount` | `StreamLabel.unitCount` | `INTEGER NOT NULL DEFAULT 8` | Standard duration in academic terms |
| `minAttendance`| Number: "Min Attendance %" | `programs[].minAttendance` | `StreamLabel.minAttendance` | `INTEGER NOT NULL DEFAULT 75` | Statutory mandatory attendance bar |
| `subjectCode` | Input: "Subject Code" | `subjects[].code` | `UniversitySubject.code` | `VARCHAR(50) NOT NULL` | e.g. `CS101`, `MATH201` |
| `part` | Select: "Course Year / Part"| `subjects[].part` | `UniversitySubject.part` | `INTEGER NOT NULL DEFAULT 1` | 1 = 1st Year, 2 = 2nd Year, etc. |
| `isElective` | Toggle: "Elective Subject" | `subjects[].isElective` | `UniversitySubject.isElective` | `BOOLEAN DEFAULT false` | CBCS classification |

---

## 2. Institute Master & Academic Operational Hierarchy

| Legacy CSV Column | UI Input Element / Label | API DTO Property | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `schemaName` | Input: "Database Schema Key" | `institutes[].schemaName` | `Institute.schemaName` | `VARCHAR(63) UNIQUE NOT NULL`| Isolated tenant prefix, e.g. `inst_mcet` |
| `shortName` | Input: "Campus Acronym" | `institutes[].shortName` | `Institute.shortName` | `VARCHAR(20) NOT NULL` | Used on reports and ID cards |
| `deptCode` | Input: "Inst Dept Code" | `departments[].code` | `Department.code` | `VARCHAR(50) NOT NULL` | Inst-scoped department code |
| `programmeCode`| Input: "Programme Code" | `courses[].code` | `Programme.code` | `VARCHAR(50) NOT NULL` | Note: UI 'Course' maps to DB `Programme` |
| `durationYears`| Number: "Duration (Years)" | `courses[].durationYears` | `Programme.durationYears` | `INTEGER NOT NULL DEFAULT 4` | Program length in years |
| `instCourseCode`| Input: "Specialization Code" | `programs[].code` | `Course.code` | `VARCHAR(50) NOT NULL` | Note: UI 'Program' maps to DB `Course` |
| `applicationFee`| Number: "Application Fee" | `programs[].applicationFee` | `Course.applicationFee` | `DECIMAL(10,2) DEFAULT 0.00` | Invoiced during Stage 1 Admissions |
| `tuitionFee` | Number: "Annual Tuition" | `programs[].tuitionFee` | `Course.tuitionFee` | `DECIMAL(10,2) DEFAULT 0.00` | Base tuition demand |
| `batchName` | Input: "Batch Cohort Name" | `batches[].batchName` | `Batch.batchName` | `VARCHAR(100) NOT NULL` | e.g. `B.Tech CSE 2024-2028` |
| `academicYear` | Number: "Joining Year" | `batches[].academicYear` | `Batch.academicYear` | `INTEGER NOT NULL` | Admission calendar year |
| `batchSize` | Number: "Approved Intake" | `batches[].batchSize` | `Batch.batchSize` | `INTEGER NOT NULL` | Statutory intake seat ceiling |
| `sectionName` | Input: "Section Identifier" | `sections[].name` | `Section.name` | `VARCHAR(20) NOT NULL` | Class cohort: `A`, `B`, `C` |

---

## 3. Staff & Faculty Directory

| Legacy CSV Column | UI Input Element / Label | API DTO Property | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `employeeId` | Input: "Staff Employee ID" | `employeeId` | `Staff.employeeId` | `VARCHAR(50) UNIQUE NOT NULL`| Physical payroll identity |
| `firstName` | Input: "First Name" | `firstName` | `User.firstName`, `Staff.firstName` | `VARCHAR(100) NOT NULL` | Synchronized across User & Staff |
| `lastName` | Input: "Last Name" | `lastName` | `User.lastName`, `Staff.lastName` | `VARCHAR(100) NOT NULL` | Synchronized across User & Staff |
| `email` | Input: "Official Email" | `email` | `User.email`, `Staff.email` | `VARCHAR(255) UNIQUE NOT NULL`| SSO login username |
| `phone` | Input: "Mobile Number" | `phone` | `User.phone`, `Staff.phone` | `VARCHAR(20) UNIQUE NOT NULL`| E.164 standard format |
| `staffType` | Select: "Employment Type" | `staffType` | `Staff.staffType` | `ENUM('teaching','non_teaching')`| Governs academic permission sets |
| `designation` | Input: "Job Designation" | `designation` | `Staff.designation` | `VARCHAR(100) NOT NULL` | e.g. `Assistant Professor` |
| `experienceYears`| Number: "Experience" | `experienceYears` | `Staff.experienceYears` | `DECIMAL(4,1) DEFAULT 0.0` | NIRF / NAAC faculty reporting |

---

## 4. Student Identity, Demographics & Profiles

| Legacy CSV Column | UI Input Element / Label | API DTO Property (`onboarding.dto.ts`) | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `enrollmentNo` | Input: "Enrollment Number" | `students[].enrollmentNo` | `Student.enrollmentNo` | `VARCHAR(50) UNIQUE NOT NULL`| Permanent university registration ID |
| `rollNo` | Input: "Class Roll No" | `students[].rollNo` | `Student.rollNo` | `VARCHAR(50)` | Section-specific roll call ID |
| `dateOfBirth` | Date: "Date of Birth" | `students[].dateOfBirth` | `StudentProfile.dateOfBirth` | `DATE NOT NULL` | Age verification & verification gate |
| `gender` | Radio: "Gender" | `students[].gender` | `StudentProfile.gender` | `VARCHAR(10) NOT NULL` | `'M' | 'F' | 'O'` |
| `category` | Select: "Social Category" | `students[].category` | `StudentProfile.category` | `VARCHAR(20) NOT NULL` | `'GEN' | 'OBC' | 'SC' | 'ST' | 'EWS'` |
| `guardianName` | Input: "Father/Guardian" | `students[].guardianName` | `StudentProfile.guardianName` | `VARCHAR(255) NOT NULL` | Emergency contact & identity record |
| `guardianMobile`| Input: "Guardian Mobile"| `students[].guardianMobile`| `StudentProfile.guardianMobile` | `VARCHAR(20) NOT NULL` | Target for fee alerts & attendance SMS |
| `guardianEmail`| Input: "Guardian Email" | `students[].guardianEmail` | `StudentProfile.guardianEmail` | `VARCHAR(255)` | Target for semester report cards |
| `permanentAddress`| Textarea: "Home Address"| `students[].permanentAddress`| `StudentProfile.permanentAddress`| `TEXT` | Domicile verification |
| `abcId` | Input: "APAAR / ABC ID" | `students[].abcId` | `StudentProfile.ext -> 'abcId'` | `VARCHAR(12)` | 12-digit Academic Bank of Credits ID |

---

## 5. Academic Performance, Marks & Attendance

| Legacy CSV Column | UI Input Element / Label | API DTO Property | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `termNumber` | Number: "Semester Number" | `history[].termNumber` | `BatchTerm.termNumber` | `INTEGER NOT NULL` | Term index (1 through 8) |
| `subjectLabel` | Select: "Course / Subject" | `subjects[].subjectLabel` | `BatchTermSubject.subjectLabel` | `VARCHAR(100) NOT NULL` | Foreign key reference to subject version |
| `componentType`| Select: "Exam Component" | `marks[].componentType` | `StudentMarks.componentType` | `ENUM('internal_1','external')`| CIA or End-Semester examination |
| `marksObtained`| Number: "Score Secured" | `marks[].marksObtained` | `StudentMarks.marksObtained` | `DECIMAL(5,2) NOT NULL` | Numerical grade points earned |
| `maxMarks` | Number: "Maximum Score" | `marks[].maxMarks` | `StudentMarks.maxMarks` | `DECIMAL(5,2) NOT NULL` | Component ceiling |
| `attendedSessions`| Number: "Classes Attended"| `attendance[].attended` | `StudentSubjectAttendance.attended` | `INTEGER NOT NULL DEFAULT 0` | Physical / Biometric class presence |
| `totalSessions`| Number: "Classes Delivered"| `attendance[].totalSessions`| `StudentSubjectAttendance.totalSessions`| `INTEGER NOT NULL DEFAULT 0` | Classroom delivery denominator |

---

## 6. Financial Architecture, Demands & Ledgers

| Legacy CSV Column | UI Input Element / Label | API DTO Property | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `demandNo` | Display: "Invoice / Demand #"| `demandNo` | `FeeDemand.demandNo` | `VARCHAR(50) UNIQUE NOT NULL`| Invoiced bill number |
| `feeHeadCode` | Select: "Fee Category" | `fees[].feeHead` | `FeeHead.code` | `VARCHAR(50) NOT NULL` | Linked to Tuition, Lab, Hostel, etc. |
| `amountDue` | Currency: "Billable Amount"| `fees[].amountDue` | `FeeDemand.amountDue` | `DECIMAL(10,2) NOT NULL` | Invoiced obligation |
| `amountPaid` | Currency: "Collected Amount"| `fees[].amountPaid` | `FeeDemand.amountPaid` | `DECIMAL(10,2) DEFAULT 0.00` | Running settled balance |
| `dueDate` | Date: "Payment Deadline" | `fees[].dueDate` | `FeeDemand.dueDate` | `DATE NOT NULL` | Expiry threshold before late fines |
| `status` | Badge: "Payment Status" | `fees[].status` | `FeeDemand.status` | `ENUM('unpaid','paid','waived')`| Lifecycle status flag |
| `receiptNo` | Display: "Receipt Number" | `receiptNo` | `Payment.receiptNo` | `VARCHAR(50) UNIQUE` | Formal financial audit receipt ID |
| `transactionRef`| Input: "Gateway / Bank Ref"| `transactionRef` | `Payment.transactionRef` | `VARCHAR(100)` | Razorpay `pay_id` or Bank UTR number |

---

## 7. Campus Logistics & Ancillary Facilities

| Legacy CSV Column | UI Input Element / Label | API DTO Property | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `hostelCode` | Select: "Hostel Building" | `hostelCode` | `Hostel.code` | `VARCHAR(50) NOT NULL` | Residential facility code |
| `roomNumber` | Input: "Room Identifier" | `roomNumber` | `HostelRoom.roomNumber` | `VARCHAR(20) NOT NULL` | Physical room door number |
| `roomType` | Select: "Room Category" | `roomType` | `HostelRoom.roomType` | `ENUM('SINGLE','DOUBLE','TRIPLE')`| Governs occupancy and pricing |
| `checkInDate` | Date: "Possession Date" | `checkInDate` | `HostelAllocation.checkInDate` | `DATE NOT NULL` | Move-in timestamp |
| `routeNumber` | Select: "Transit Route" | `routeNumber` | `TransportRoute.routeNumber` | `VARCHAR(50) NOT NULL` | Campus bus route code |
| `passNumber` | Display: "Bus Pass ID" | `passNumber` | `TransportPass.passNumber` | `VARCHAR(50) UNIQUE NOT NULL`| Scannable transit identity |
| `isbn` | Input: "Book ISBN" | `isbn` | `Book.isbn` | `VARCHAR(20) NOT NULL` | Standard bibliographic index |
| `barcode` | Barcode Scanner: "Copy ID" | `barcode` | `BookCopy.barcode` | `VARCHAR(50) UNIQUE NOT NULL`| Physical RFID / Barcode sticker |

---

## 8. Documents, Certificates & Security Stock

| Legacy CSV Column | UI Input Element / Label | API DTO Property | Prisma DB Model & Column | PostgreSQL Type & Constraints | Notes / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `templateName` | Select: "Document Template"| `templateName` | `DocumentTemplate.name` | `VARCHAR(100) NOT NULL` | Canvas layout definition |
| `serialNo` | Display: "Security Serial #"| `serialNo` | `IssuedDocument.serialNo` | `VARCHAR(50) UNIQUE NOT NULL`| Security watermark paper serial |
| `verifyUrl` | QR Code Payload | `verifyUrl` | `IssuedDocument.verifyUrl` | `VARCHAR(500) NOT NULL` | Public digital validation URL |
| `comment` | Input: "Audit Tracking Note"| `comment` | `CertificateStock.comment` | `TEXT` | Stores `issued: <enr>/<email>` or damaged reason |

---
```
========================================================================================================================
END OF SPECIFICATION: FIELD MAPPING MATRIX & DATA DICTIONARY (UERP-MIG-DICT-V4.2)
========================================================================================================================
```
