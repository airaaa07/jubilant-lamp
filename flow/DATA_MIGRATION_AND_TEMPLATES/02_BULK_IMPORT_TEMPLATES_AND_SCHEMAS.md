# Enterprise Bulk Import Templates & Schema Specifications
## Standardized CSV, Excel & JSON Ingestion Templates with Data Validation Rules

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-MIG-TEMPLATES-V4.2
CLASSIFICATION: TECHNICAL SPECIFICATION & OPERATIONAL ARTIFACT
TARGET AUDIENCE: DATA MIGRATION TEAMS, SYSTEM ADMINISTRATORS, REGISTRARS, ACADEMIC CLERKS
========================================================================================================================
```

---

## Executive Overview & Template Architecture

To facilitate zero-loss data transition from legacy systems, **UniversityERP** provides standardized, round-trip validated ingestion schemas. Each schema is available as:
1. **Flat CSV / Excel Workbook format** (for end-user administrative upload via UI modals).
2. **Hierarchical JSON payload** (for automated REST API ingestion via `POST /master-data/bulk-import/*` and `POST /onboarding/students/*`).

Every field in these schemas includes strict validation rules:
- **Mandatory (M) vs Optional (O)**.
- **Regex format constraints** (e.g. ISO-8601 dates, E.164 phone numbers).
- **Accepted Enum sets**.
- **Cross-entity relational lookups** (referential integrity checks).

---

## Template Catalog Index

1. [Template 01: University Catalog Hierarchy](#template-01-university-catalog-hierarchy)
2. [Template 02: Institute Academic Structure](#template-02-institute-academic-structure)
3. [Template 03: Staff & Faculty Directory](#template-03-staff--faculty-directory)
4. [Template 04: Student Primary Matriculation & Demographic Profile](#template-04-student-primary-matriculation--demographic-profile)
5. [Template 05: Historical Academic Performance & Attendance](#template-05-historical-academic-performance--attendance)
6. [Template 06: Fee Heads & Master Fee Structures](#template-06-fee-heads--master-fee-structures)
7. [Template 07: Fee Demands & Historical Payments](#template-07-fee-demands--historical-payments)
8. [Template 08: Campus Hostel & Room Allotments](#template-08-campus-hostel--room-allotments)
9. [Template 09: Transport Routes, Vehicles & Student Passes](#template-09-transport-routes-vehicles--student-passes)
10. [Template 10: Central Library Catalog & Book Copies](#template-10-central-library-catalog--book-copies)

---

### Template 01: University Catalog Hierarchy
*Endpoint: `POST /master-data/bulk-import/catalog` and `POST /master-data/bulk-import/subjects`*

#### CSV 1A: University Departments (`university_departments.csv`)
```csv
code,name,shortName,description,isAcademic
ENG,Faculty of Engineering,FOE,Engineering and Applied Sciences,true
MGT,School of Management,SOM,Business Administration and Finance,true
SCI,School of Basic Sciences,SBS,Pure and Natural Sciences,true
```

#### CSV 1B: University Courses / Degrees (`university_courses.csv`)
```csv
departmentCode,code,name,shortName,description
ENG,BTECH,Bachelor of Technology,B.Tech,Four-year undergraduate engineering degree
ENG,MTECH,Master of Technology,M.Tech,Two-year postgraduate engineering degree
MGT,MBA,Master of Business Administration,MBA,Two-year graduate management degree
```

#### CSV 1C: University Streams / Programs (`university_streams.csv`)
```csv
departmentCode,courseCode,code,name,shortName,year,version,level,streamType,regulatedBy,totalCredits,unitName,unitCount,minAggregate,minGradePoint,minAttendance
ENG,BTECH,CSE,Computer Science and Engineering,CS,2024,v01,UG,Regular,AICTE,160,Semester,8,50.0,5.0,75
ENG,BTECH,ECE,Electronics and Communication Engineering,EC,2024,v01,UG,Regular,AICTE,160,Semester,8,50.0,5.0,75
MGT,MBA,FIN,Finance and Banking,FIN,2024,v01,PG,Regular,UGC,100,Semester,4,55.0,6.0,75
```

#### CSV 1D: University Subjects (`university_subjects.csv`)
```csv
programCode,code,name,shortName,part,isElective,syllabus
CSE,CS101,Programming in C and Data Structures,C-DS,1,false,Pointers Arrays Trees Graphs Recursion
CSE,CS102,Discrete Mathematics,DM,1,false,Set Theory Graph Theory Logic Boolean Algebra
CSE,CS201,Object Oriented Programming with Java,OOP-Java,2,false,JVM Classes Inheritance Polymorphism Multithreading
CSE,CS305,Artificial Intelligence & Machine Learning,AI-ML,3,true,Supervised Learning Neural Networks Deep Learning
```

---

### Template 02: Institute Academic Structure
*Endpoint: `POST /master-data/bulk-import/institutes`*

#### CSV 2A: Campuses & Institutes (`institutes.csv`)
```csv
name,shortName,schemaName,address,about
Main Campus College of Technology,MCET,inst_mcet,100 University Boulevard Metro City,Premier constituent engineering institution
City Business School,CBS,inst_cbs,45 Commercial Road City Center,Flagship graduate business school
```

#### CSV 2B: Institute Academic Departments (`institute_departments.csv`)
```csv
instituteSchemaName,code,name,universityDeptCode
inst_mcet,DEPT_CSE,Department of Computer Science,ENG
inst_mcet,DEPT_ECE,Department of Electronics,ENG
inst_cbs,DEPT_MBA,Department of Management Studies,MGT
```

#### CSV 2C: Institute Programmes (`institute_programmes.csv`)
*(Note: Display 'Course' = DB Model `Programme`)*
```csv
instituteSchemaName,departmentCode,code,name,calendarType,durationYears,totalCredits,universityCourseCode
inst_mcet,DEPT_CSE,BTECH_CS,B.Tech Computer Science,semester,4,160,BTECH
inst_mcet,DEPT_ECE,BTECH_EC,B.Tech Electronics,semester,4,160,BTECH
inst_cbs,DEPT_MBA,MBA_GEN,Master of Business Administration,semester,2,100,MBA
```

#### CSV 2D: Institute Courses / Specializations (`institute_courses.csv`)
*(Note: Display 'Program' = DB Model `Course`)*
```csv
instituteSchemaName,departmentCode,courseCode,code,name,medium,applicationFee,tuitionFee,admissionFee,labFee,miscFee,universityStreamCode
inst_mcet,DEPT_CSE,BTECH_CS,CSE_CORE,B.Tech CSE Core,English,1500,65000,10000,8000,5000,CSE
inst_mcet,DEPT_ECE,BTECH_EC,ECE_CORE,B.Tech ECE Core,English,1500,60000,10000,8000,5000,ECE
inst_cbs,DEPT_MBA,MBA_GEN,MBA_FIN,MBA Financial Management,English,2000,85000,15000,0,5000,FIN
```

#### CSV 2E: Batches & Sections (`batches_and_sections.csv`)
```csv
instituteSchemaName,departmentCode,courseCode,programCode,batchName,academicYear,semester,yearNumber,batchSize,sectionName,sectionSize
inst_mcet,DEPT_CSE,BTECH_CS,CSE_CORE,B.Tech CSE 2024-2028,2024,Semester I,1,120,A,60
inst_mcet,DEPT_CSE,BTECH_CS,CSE_CORE,B.Tech CSE 2024-2028,2024,Semester I,1,120,B,60
inst_mcet,DEPT_ECE,BTECH_EC,ECE_CORE,B.Tech ECE 2024-2028,2024,Semester I,1,60,A,60
```

---

### Template 03: Staff & Faculty Directory
*Endpoint: `POST /staff/bulk-import`*

#### CSV 3: Staff Master (`staff_directory.csv`)
```csv
employeeId,firstName,lastName,email,phone,gender,staffType,designation,departmentCode,joiningDate,experienceYears,qualification,address
EMP1001,Rajesh,Sharma,rajesh.sharma@university.edu,+919810011221,M,teaching,Professor & HOD,DEPT_CSE,2015-07-01,15.5,Ph.D. Computer Science,Plot 42 Sector 15 Metro City
EMP1002,Sunita,Menon,sunita.menon@university.edu,+919810011222,F,teaching,Associate Professor,DEPT_CSE,2018-08-15,8.0,M.Tech Software Engineering,Flat 301 Royal Palms Metro City
EMP2001,Vikram,Singh,vikram.singh@university.edu,+919810011223,M,non_teaching,Lab Technician,DEPT_CSE,2020-01-10,4.2,BCA,Quarter 12 Staff Colony
EMP3001,Anil,Kumar,anil.kumar@university.edu,+919810011224,M,administrative,Assistant Registrar,DEPT_MBA,2012-03-01,18.0,M.Com MBA,House 58 Green Park
```

---

### Template 04: Student Primary Matriculation & Demographic Profile
*Endpoint: `POST /onboarding/students/validate` and `POST /onboarding/students/commit`*

#### CSV 4: Student Base & Demographics (`students_onboarding.csv`)
```csv
enrollmentNo,rollNo,email,firstName,middleName,lastName,dateOfBirth,gender,category,phone,guardianName,guardianRelation,guardianMobile,guardianEmail,batchName,sectionName,admissionDate,permanentAddress,abcId
2024CSE001,R-001,rohit.sharma@student.edu,Rohit,Kumar,Sharma,2005-04-12,M,GEN,+919876543210,Manoj Sharma,Father,+919876543211,manoj.sharma@gmail.com,B.Tech CSE 2024-2028,A,2024-07-20,"124 Model Town, Metro City",123456789012
2024CSE002,R-002,priya.patel@student.edu,Priya,,Patel,2005-09-24,F,OBC,+919876543212,Suresh Patel,Father,+919876543213,suresh.patel@gmail.com,B.Tech CSE 2024-2028,A,2024-07-21,"88 Gandhi Nagar, Metro City",123456789013
2024CSE003,R-003,amit.verma@student.edu,Amit,,Verma,2004-11-05,M,SC,+919876543214,Ramesh Verma,Father,+919876543215,ramesh.verma@gmail.com,B.Tech CSE 2024-2028,B,2024-07-21,"52 Railway Colony, Metro City",123456789014
```

---

### Template 05: Historical Academic Performance & Attendance
*Endpoint: `POST /onboarding/students/commit` (via `history` array)*

#### CSV 5: Academic History & Marks (`student_academic_history.csv`)
```csv
enrollmentNo,termNumber,subjectLabel,componentType,marksObtained,maxMarks,attendedSessions,totalSessions
2024CSE001,1,Subject_CS101_v01,internal_test_1,18.5,20,28,30
2024CSE001,1,Subject_CS101_v01,internal_test_2,17.0,20,28,30
2024CSE001,1,Subject_CS101_v01,external,54.0,60,28,30
2024CSE001,1,Subject_CS102_v01,internal_test_1,16.0,20,25,30
2024CSE001,1,Subject_CS102_v01,external,48.0,60,25,30
2024CSE002,1,Subject_CS101_v01,internal_test_1,19.0,20,30,30
2024CSE002,1,Subject_CS101_v01,external,58.0,60,30,30
```

---

### Template 06: Fee Heads & Master Fee Structures
*Endpoint: `POST /fee/heads` and `POST /fee/structures`*

#### CSV 6A: Fee Heads (`fee_heads.csv`)
```csv
code,name,description,category,isRefundable,isRecurring
TUITION,Tuition Fee,Instructional and faculty delivery charges,ACADEMIC,false,true
LAB,Laboratory & Computing Fee,Lab consumable and software licensing,ACADEMIC,false,true
DEV,University Development Fund,Campus infrastructure expansion,INSTITUTIONAL,false,true
CAUTION,Institute Caution Deposit,Refundable security deposit against damages,DEPOSIT,true,false
EXAM,Semester Examination Fee,Conduct and evaluation of term assessments,EXAM,false,true
HOSTEL_RENT,Hostel Room Rent,Residential accommodation license fee,HOSTEL,false,true
HOSTEL_MESS,Hostel Mess Advance,Monthly dining facility charges,HOSTEL,false,true
```

#### CSV 6B: Fee Structure Configuration (`fee_structures.csv`)
```csv
programmeCode,academicYear,termNumber,feeHeadCode,amount,dueDate,lateFineDaily,graceDays
BTECH_CS,2024,1,TUITION,65000,2024-08-10,100,7
BTECH_CS,2024,1,LAB,8000,2024-08-10,50,7
BTECH_CS,2024,1,DEV,5000,2024-08-10,0,7
BTECH_CS,2024,1,CAUTION,10000,2024-08-10,0,0
BTECH_CS,2024,1,EXAM,2500,2024-10-15,100,5
```

---

### Template 07: Fee Demands & Historical Payments
*Endpoint: `POST /fee/demands/bulk` and `POST /fee/payments`*

#### CSV 7: Fee Demands and Payments (`fee_demands_and_payments.csv`)
```csv
demandNo,enrollmentNo,academicYear,termNumber,feeHeadCode,amountDue,dueDate,amountPaid,paymentDate,paymentMode,transactionRef,receiptNo,status
DEM20240001,2024CSE001,2024,1,TUITION,65000,2024-08-10,65000,2024-08-05,ONLINE,pay_Nq28sA102x,REC2024001,paid
DEM20240002,2024CSE001,2024,1,LAB,8000,2024-08-10,8000,2024-08-05,ONLINE,pay_Nq28sA102x,REC2024001,paid
DEM20240003,2024CSE001,2024,1,CAUTION,10000,2024-08-10,10000,2024-08-05,ONLINE,pay_Nq28sA102x,REC2024001,paid
DEM20240004,2024CSE002,2024,1,TUITION,65000,2024-08-10,35000,2024-08-08,CHALLAN,CHL892011,REC2024045,partially_paid
DEM20240005,2024CSE003,2024,1,TUITION,65000,2024-08-10,0,,,unpaid
```

---

### Template 08: Campus Hostel & Room Allotments
*Endpoint: `POST /hostel/rooms/bulk` and `POST /hostel/allocations/bulk`*

#### CSV 8A: Hostel Rooms (`hostel_rooms.csv`)
```csv
hostelCode,blockName,floorNumber,roomNumber,roomType,capacity,monthlyRent,hasAirConditioner
H1_BOYS,Block A,1,101,DOUBLE,2,6000,false
H1_BOYS,Block A,1,102,DOUBLE,2,6000,false
H1_BOYS,Block B,2,201,SINGLE_AC,1,12000,true
H2_GIRLS,Block C,1,101,DOUBLE,2,6000,false
```

#### CSV 8B: Student Room Allocations (`hostel_allocations.csv`)
```csv
hostelCode,roomNumber,enrollmentNo,academicYear,checkInDate,allocatedByStaffId
H1_BOYS,101,2024CSE001,2024,2024-07-28,EMP3001
H2_GIRLS,101,2024CSE002,2024,2024-07-29,EMP3001
```

---

### Template 09: Transport Routes, Vehicles & Student Passes
*Endpoint: `POST /transport/routes/bulk` and `POST /transport/passes/bulk`*

#### CSV 9: Transport Fleet & Passes (`transport_routes_and_passes.csv`)
```csv
routeNumber,routeName,vehicleRegistrationNo,driverName,driverPhone,stopName,stopTime,enrollmentNo,passNumber,feeAmount,validTill
RT-04,North Suburb Express,DL-01-AB-1234,Gurpreet Singh,+919811223344,Model Town Crossing,07:45 AM,2024CSE001,PASS2024001,18000,2025-06-30
RT-04,North Suburb Express,DL-01-AB-1234,Gurpreet Singh,+919811223344,Civil Lines Metro,08:00 AM,2024CSE003,PASS2024002,18000,2025-06-30
```

---

### Template 10: Central Library Catalog & Book Copies
*Endpoint: `POST /library/books/bulk`*

#### CSV 10: Library Books & Inventory (`library_catalog.csv`)
```csv
isbn,title,authors,publisher,edition,year,callNumber,category,barcode,copyNumber,shelfLocation
978-0131103627,The C Programming Language,Brian W. Kernighan & Dennis M. Ritchie,Prentice Hall,2nd,1988,005.133 KER,Computer Science,BK-000101,1,Stack A-04
978-0131103627,The C Programming Language,Brian W. Kernighan & Dennis M. Ritchie,Prentice Hall,2nd,1988,005.133 KER,Computer Science,BK-000102,2,Stack A-04
978-0262033848,Introduction to Algorithms,Thomas H. Cormen et al.,MIT Press,3rd,2009,005.1 COR,Computer Science,BK-000201,1,Stack A-08
```

---

## Technical Ingestion Validation Engine

When executing bulk import via API or UI, the system runs through a multi-stage validation pipeline:

```
+----------------------------------------------------------------------------------------------------+
|                                    INSPECTION & INGESTION PIPELINE                                 |
+----------------------------------------------------------------------------------------------------+
  [Step 1: Syntax & Envelope Validation]
      * Checks MIME type (CSV / XLSX / JSON)
      * Validates required column headers match the dictionary exactly
      * Enforces UTF-8 character encoding (rejects non-standard encodings)

  [Step 2: Schema & Type Coercion (Zod Engine)]
      * Dates: converts YYYY-MM-DD or DD/MM/YYYY into native JavaScript Date objects
      * Numbers: converts string decimals to floats / integers
      * Enums: maps localized casing (e.g. "female" -> 'F', "Semester" -> 'semester')

  [Step 3: Relational Reference Resolution]
      * Resolves natural human codes into database UUIDs (e.g. 'CSE' -> 'stream_id_uuid')
      * Verifies all referenced parents exist in the database
      * Detects foreign key violations in dry-run mode (`validate: true`)

  [Step 4: Atomic Batch Transaction]
      * Chunks datasets into 500-record transactions
      * Uses `prisma.$transaction` to guarantee all-or-nothing atomicity
      * Emits granular success and failure error logs (stating exact row number & offending value)
+----------------------------------------------------------------------------------------------------+
```

---
```
========================================================================================================================
END OF SPECIFICATION: BULK IMPORT TEMPLATES & SCHEMAS (UERP-MIG-TEMPLATES-V4.2)
========================================================================================================================
```
