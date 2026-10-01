# Enterprise Dynamic Tokens & Variable Interpolation Catalog
## Comprehensive Reference for Canvas Document Designer, ID Formats & Notification Engines

```
========================================================================================================================
UNIVERSITY ENTERPRISE RESOURCE PLANNING (UniversityERP)
DOCUMENT ID: UERP-DOC-TOKENS-V4.2
CLASSIFICATION: TECHNICAL REFERENCE & SPECIFICATION
TARGET AUDIENCE: DOCUMENT DESIGNERS, REGISTRAR EXCELLENCE CELLS, SOFTWARE ENGINEERS, TEMPLATE AUTHORS
========================================================================================================================
```

---

## Executive Overview & Interpolation Architecture

**UniversityERP** features a universal, context-aware template engine capable of dynamically binding runtime student, staff, examination, and financial records into:
1. **Canvas Document Designer**: Degree certificates, provisional certificates, grade cards, bonafide letters, and smart ID cards.
2. **Deterministic ID Formats**: Algorithmic generation of Enrollment Numbers, Employee IDs, and Receipt Numbers.
3. **Telephony & Notification Engine**: TRAI DLT-approved transactional SMS, automated emails, and push notifications.

Dynamic tokens use standard double curly bracket notation: `{{path.to.variable}}`.
The resolution engine supports nested property traversal, custom extended schema attributes (`ext.<key>`), formatters, and QR/Barcode scannable payload generators.

---

## 1. Student Master & Identity Tokens

Available in templates with `subjectType = 'student'`.

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{student.enrollmentNo}}` | Enrollment No | **YES** | `2024CS001` | Primary university matriculation number |
| `{{student.firstName}}` | First Name | NO | `Rohit` | Legal first name |
| `{{student.middleName}}` | Middle Name | NO | `Kumar` | Middle name (if present) |
| `{{student.lastName}}` | Last Name | NO | `Sharma` | Family surname |
| `{{student.fullName}}` | Full Name | NO | `Rohit Kumar Sharma` | Formatted: First + Middle + Last |
| `{{student.dateOfBirth}}` | Date of Birth | NO | `15/08/2004` | Standard localized date format (`DD/MM/YYYY`) |
| `{{student.gender}}` | Gender | NO | `Male` | Expanded gender label |
| `{{student.category}}` | Social Category | NO | `General` | Reservation category |
| `{{student.status}}` | Student Status | NO | `Active` | Active, Cancelled, Suspended, Graduated |
| `{{student.guardianName}}` | Guardian Name | NO | `Manoj Sharma` | Father / Mother / Legal Guardian name |
| `{{student.guardianMobile}}`| Guardian Mobile| NO | `+91 98765 43210` | Guardian emergency telephone |
| `{{student.guardianEmail}}` | Guardian Email | NO | `manoj@gmail.com` | Guardian primary email |
| `{{student.address}}` | Permanent Address| NO | `Flat 402, Green Valley, Metro City` | Full physical domicile address |
| `{{student.photoUrl}}` | Student Photo | NO | `<img>` (Data URI / CDN) | Dynamic base64 or secure S3/GCS photo asset |
| `{{student.ext.<key>}}` | Custom Extended Attr| **YES** | *(Dynamic)* | Custom fields defined in Profile Governance |

---

## 2. Academic Program, Cohort & Hierarchy Tokens

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{academic.section}}` | Section | NO | `Section A` | Assigned classroom division |
| `{{academic.batchName}}` | Batch Cohort | NO | `B.Tech CSE 2024-2028` | Full cohort label |
| `{{academic.academicYear}}` | Academic Year | NO | `2024` | Matriculation calendar year |
| `{{academic.academicSession}}`| Academic Session | NO | `2024-2025` | Operational fiscal / academic year |
| `{{academic.semester}}` | Current Semester | NO | `Semester III` | Roman / Arabic term designation |
| `{{academic.termName}}` | Term Label | NO | `Semester III` | Latest published term name |
| `{{academic.termNumber}}` | Term Number | NO | `3` | Integer index of current term |
| `{{academic.medium}}` | Medium | NO | `English` | Medium of curriculum instruction |
| `{{academic.course}}` | Specialization | NO | `Computer Science & Engineering` | Degree specialization |
| `{{academic.courseCode}}` | Specialization Code| NO | `CSE_CORE` | Short internal program code |
| `{{academic.programme}}` | Degree Programme | NO | `Bachelor of Technology` | Formal statutory degree title |
| `{{academic.programmeCode}}`| Programme Code | NO | `BTECH` | Degree level code |
| `{{academic.department}}` | Department | NO | `Department of Computer Science` | Teaching department name |
| `{{academic.departmentCode}}`| Dept Code | NO | `DEPT_CSE` | Department code |
| `{{academic.institute}}` | Institute / Campus | NO | `Main Campus College of Technology`| Constituent campus name |
| `{{academic.instituteShortName}}`| Inst Short Name | NO | `MCET` | Campus acronym |
| `{{academic.university}}` | University Name | NO | `State Technological University` | Full statutory university title |
| `{{academic.universityShortName}}`| Univ Acronym | NO | `STU` | University short title |

---

## 3. Results, CGPA & Marksheet Tokens

Used on semester grade cards, consolidated transcripts, and final degree certificates.

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{results.cgpa}}` | CGPA | **YES** | `8.75` | 10-point scale cumulative GPA |
| `{{results.cgpaPercentage}}`| Equivalent % | NO | `83.12%` | Calculated based on university conversion formula |
| `{{results.degreeClass}}` | Classification | NO | `First Class with Distinction` | Statutory honors / division award |
| `{{results.degreeAwarded}}` | Award Status | NO | `Conferred` | Conferred or Pending Senate sign-off |
| `{{results.latestSgpa}}` | Latest SGPA | NO | `8.90` | Performance in most recent term |
| `{{results.totalCreditsEarned}}`| Credits Earned | NO | `162` | NEP 2020 accumulated credits |
| `{{results.totalCreditsAttempted}}`| Credits Attempted | NO | `162` | Total credits registered |
| `{{results.totalBacklogs}}` | Active Backlogs | NO | `0` | Uncleared failed courses |
| `{{termName}}` | Term Heading | NO | `Semester IV` | Used in per-term marksheets |
| `{{examHeldDate}}` | Examination Date | NO | `May - June 2026` | Date of assessment delivery |
| `{{resultDeclaredOn}}` | Declaration Date | NO | `15/07/2026` | Official result gazette date |
| `{{sgpa}}` | Term SGPA | NO | `8.45` | Grade point average for specific term |
| `{{subjectsTable}}` | Subjects Mark Grid | NO | `<table>` HTML Grid | Renders tabular marks, credits, and letter grades |

---

## 4. Financial Status & Fee Ledgers Tokens

Used on fee receipts, dues clearance certificates, and admission offer invoices.

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{fees.totalDue}}` | Total Invoiced | NO | `₹ 1,45,000.00` | Cumulative historical demands |
| `{{fees.totalPaid}}` | Total Collected | NO | `₹ 1,45,000.00` | Total confirmed receipts |
| `{{fees.lateFees}}` | Penalty Balance | NO | `₹ 0.00` | Accrued late fee interest |
| `{{fees.outstanding}}` | Balance Outstanding| **YES** | `₹ 0.00` | Pending institutional dues |
| `{{fees.status}}` | Fee Status | NO | `CLEARED` | `CLEARED` or `DEFAULT` |

---

## 5. Attendance & Biometric Tokens

Used on exam admit cards (hall tickets) and eligibility notices.

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{attendance.percent}}` | Attendance % | **YES** | `88.5%` | Aggregated term attendance percentage |
| `{{attendance.present}}` | Present Sessions | NO | `142` | Actual classes attended |
| `{{attendance.total}}` | Delivered Sessions | NO | `160` | Total classroom sessions held |

---

## 6. Document Metadata & Anti-Counterfeit Security Tokens

Automatically injected by the Document Service during document rendering.

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{serialNo}}` | Document Serial | **YES** | `DEG-2026-004128` | Security stock serial or UUID serial |
| `{{documentType}}` | Document Classification | NO | `DEGREE_CERTIFICATE` | Canonical document category |
| `{{documentCode}}` | Document Code | NO | `CERT_BTECH_2024` | System template identifier |
| `{{issuedAt}}` | Date of Issuance | NO | `24/09/2026` | Timestamp of digital rendering |
| `{{issuedBy}}` | Issuing Authority | NO | `Controller of Examinations` | Authority signature label |
| `{{verifyUrl}}` | Verification Link | **YES** | `https://verify.univ.edu/doc/X7k9P` | Public digital validation URL for QR |

---

## 7. Staff & Faculty Tokens

Available in templates with `subjectType = 'staff'` (e.g. Appointment Orders, Experience Certificates, Faculty ID Cards).

| Token Name | Human Label | Scannable (QR/Barcode) | Sample Output | Description / Source Field |
| :--- | :--- | :---: | :--- | :--- |
| `{{staff.employeeId}}` | Employee ID | **YES** | `EMP1024` | Official payroll employee code |
| `{{staff.firstName}}` | First Name | NO | `Jane` | Staff given name |
| `{{staff.lastName}}` | Last Name | NO | `Doe` | Staff surname |
| `{{staff.fullName}}` | Full Name | NO | `Dr. Jane Doe` | Formatted title + full name |
| `{{staff.designation}}` | Designation | NO | `Professor & HOD` | Employment job title |
| `{{staff.staffType}}` | Category | NO | `teaching` | `teaching` or `non_teaching` |
| `{{staff.dateOfJoining}}` | Joining Date | NO | `01/07/2018` | Institutional joining date |
| `{{staff.experienceYears}}`| Experience | NO | `7.5 Years` | Accumulated institutional service |
| `{{staff.email}}` | Official Email | NO | `jane.doe@university.edu` | Corporate email address |
| `{{staff.phone}}` | Mobile Phone | NO | `+91 98123 45678` | Contact telephone |
| `{{org.department}}` | Department | NO | `Department of Physics` | Assigned school / department |
| `{{org.institute}}` | Institute Campus | NO | `School of Basic Sciences` | Campus / constituent college |

---

## 8. Dynamic ID Format & Sequence Generator Tokens

Configured in `/id-format` for automated sequential identifier generation:

| Token Key | Output Format | Example Value | Description |
| :--- | :--- | :--- | :--- |
| `{{YEAR}}` | 4-digit Calendar Year | `2026` | Current year or admission cohort year |
| `{{YEAR_2DIGIT}}` | 2-digit Year | `26` | Abbreviated year prefix |
| `{{MONTH}}` | 2-digit Month | `09` | Current month index (`01`–`12`) |
| `{{INST_CODE}}` | Institute Acronym | `MCET` | Up to 6-char campus short code |
| `{{DEPT_CODE}}` | Dept Acronym | `CSE` | 3-char department identifier |
| `{{PROG_CODE}}` | Degree Level | `UG` | `UG`, `PG`, or `PHD` |
| `{{SEQ:n}}` | Zero-padded Sequence | `0042` (for `{{SEQ:4}}`) | Atomic auto-increment counter per pattern |

*Example Format Pattern*: `{{YEAR}}{{DEPT_CODE}}{{SEQ:4}}` $\longrightarrow$ `2026CSE0042`

---

## 9. Notification & SMS Interpolation Tokens (TRAI DLT Compatible)

Transactional messaging templates strictly map variables to DLT placeholders `{#var#}`:

| Message Event | Template Text with Tokens | DLT Reg. ID | Target Audience |
| :--- | :--- | :--- | :--- |
| **Admission Offer** | `Dear {{studentName}}, congratulations! You have been offered provisional admission to {{programme}}. Pay fee before {{dueDate}}: {{link}} - STU ERP` | `110716892001` | Candidate |
| **Fee Demand Due** | `Notice: Fee demand of Rs. {{amount}} for {{termName}} is due on {{dueDate}} for Student {{enrollmentNo}}. Please clear to avoid late fine: {{link}} - STU ERP` | `110716892002` | Guardian & Student |
| **Attendance Shortage** | `Alert: Attendance of {{studentName}} in {{subject}} has fallen to {{attendancePercent}}% (minimum 75% required). Contact HOD immediately. - STU ERP` | `110716892003` | Guardian |
| **Exam Admit Card** | `Admit Card for {{examName}} is released for {{enrollmentNo}}. Download hall ticket from portal: {{link}} - STU ERP` | `110716892004` | Student |
| **Cancellation Exit** | `Enrollment {{enrollmentNo}} for {{studentName}} has been cancelled. Institutional clearance certificate issued: {{link}} - STU ERP` | `110716892005` | Student |

---
```
========================================================================================================================
END OF SPECIFICATION: DYNAMIC TOKENS CATALOG (UERP-DOC-TOKENS-V4.2)
========================================================================================================================
```
