# Glossary

## Overview

This document provides comprehensive definitions of terms, acronyms, and concepts used throughout the University ERP system and documentation.

## A

### API (Application Programming Interface)
A set of rules and protocols that allows different software applications to communicate with each other. In the University ERP, RESTful APIs are used for communication between the frontend and backend.

### Authentication
The process of verifying the identity of a user or system. The University ERP uses JWT (JSON Web Tokens) for authentication.

### Authorization
The process of determining what permissions an authenticated user has. The University ERP uses role-based access control (RBAC) for authorization.

### Academic Year
The period during which a university conducts its academic activities. In the University ERP, academic years are configured in the system and used for tracking student progress.

### Attendance
The record of a student's presence or absence in classes. The University ERP tracks attendance for students and faculty.

## B

### Backend
The server-side of the application that handles business logic, database operations, and API endpoints. The University ERP backend is built with NestJS.

### BTECH (Bachelor of Technology)
An undergraduate engineering degree program. The University ERP manages BTECH programs and related student data.

### Batch
A group of students admitted to a program in a particular academic year. The University ERP organizes students into batches for management purposes.

### Bull
A Redis-based queue for Node.js. The University ERP uses Bull for background job processing.

## C

### CBE (Curriculum Based Education)
An educational system where students follow a predefined curriculum. The University ERP has a CBE Engine for managing curriculum-based calculations.

### CORS (Cross-Origin Resource Sharing)
A security feature that allows or restricts cross-origin HTTP requests. The University ERP configures CORS for API access.

### Controller
In NestJS, a controller is responsible for handling incoming requests and returning responses to the client. Controllers define routes and handle HTTP methods.

### Course
A specific subject or module within a program. The University ERP manages courses, their schedules, and student enrollments.

### Cache
A hardware or software component that stores data so that future requests for that data can be served faster. The University ERP uses Redis for caching.

## D

### Database
An organized collection of structured information or data. The University ERP uses PostgreSQL as its primary database.

### DTO (Data Transfer Object)
An object that carries data between processes. In NestJS, DTOs are used to validate and transform data between the client and server.

### Department
An academic division within a university. The University ERP manages departments and their associated courses and staff.

### Docker
A platform for developing, shipping, and running applications in containers. The University ERP uses Docker for containerization.

### Docker Compose
A tool for defining and running multi-container Docker applications. The University ERP uses Docker Compose for local development.

## E

### Entity
In Prisma, an entity represents a database table. The University ERP defines entities for all database models.

### Environment Variable
A dynamic-named value that can affect the way running processes behave on a computer. The University ERP uses environment variables for configuration.

### E2E (End-to-End) Testing
Testing the complete flow of an application from start to finish. The University ERP uses Playwright for E2E testing.

### Exam
A formal test of a student's knowledge or proficiency. The University ERP manages exams, schedules, and results.

### Exam Paper
A structured document containing questions for an exam. The University ERP manages exam papers and their questions.

## F

### Frontend
The client-side of the application that users interact with. The University ERP frontend is built with React.

### Fee
A monetary charge for services provided by the university. The University ERP manages fee structures, payments, and student payables.

### Faculty
The teaching staff of a university. The University ERP manages faculty data, assignments, and schedules.

### Flow
In the workflow engine, a flow represents a business process with states and transitions. The University ERP uses flows for various business processes.

## G

### Guard
In NestJS, a guard is a class annotated with the @Injectable() decorator that implements the CanActivate interface. Guards determine whether a given request will be handled by the route handler or not.

### Guard Clause
A programming pattern that checks a condition and returns early if the condition is met. Used throughout the University ERP codebase for early returns.

### Git
A distributed version control system. The University ERP uses Git for version control.

### GraphQL
A query language for APIs. The University ERP currently uses REST but may consider GraphQL in the future.

## H

### Hostel
University accommodation for students. The University ERP manages hostel rooms, allocations, and related data.

### Hook
In React, a hook is a special function that lets you hook into React state and lifecycle features from function components. The University ERP uses custom hooks for reusable logic.

### HTTP (Hypertext Transfer Protocol)
The foundation of data communication for the World Wide Web. The University ERP uses HTTP for API communication.

### HTTPS (HTTP Secure)
An extension of HTTP that uses encryption for secure communication. The University ERP uses HTTPS in production.

## I

### Interceptor
In NestJS, an interceptor is a class annotated with the @Injectable() decorator that implements the NestInterceptor interface. Interceptors can bind extra logic before/after method execution.

### Instance
In Kubernetes, a pod is a group of one or more containers. The University ERP uses Kubernetes for container orchestration.

### Index
In databases, an index is a data structure that improves the speed of data retrieval operations. The University ERP uses database indexes for performance optimization.

### Issue
In the library module, an issue refers to lending a book to a user. The University ERP tracks book issues and returns.

## J

### JWT (JSON Web Token)
A compact URL-safe means of representing claims to be transferred between two parties. The University ERP uses JWT for authentication.

### Jest
A JavaScript testing framework. The University ERP uses Jest for unit and integration testing.

### Job
In Bull queue, a job represents a task to be processed. The University ERP uses jobs for background processing.

## K

### Kubernetes
An open-source container orchestration platform. The University ERP uses Kubernetes for production deployment.

### Key
In Redis, a key is used to store and retrieve values. The University ERP uses Redis keys for caching.

### K8s
Abbreviation for Kubernetes.

## L

### Library
A collection of books and other materials. The University ERP manages library books, issues, and returns.

### Log
A record of events that occur in a system. The University ERP uses Winston for structured logging.

### Load Balancer
A device that acts as a reverse proxy and distributes network or application traffic across multiple servers. The University ERP uses load balancers for scaling.

### LTS (Long Term Support)
A version of software that is supported for a longer period. The University ERP uses Node.js LTS versions.

## M

### Middleware
In NestJS, middleware is a function that is called before the route handler. Middleware functions can perform actions on the request and response objects.

### Migration
In Prisma, a migration is a set of SQL commands that modify the database schema. The University ERP uses migrations for database schema changes.

### MinIO
An object storage server compatible with Amazon S3. The University ERP uses MinIO for file storage.

### Module
In NestJS, a module is a class annotated with the @Module() decorator that organizes application code into cohesive blocks. The University ERP is organized into modules.

### Monorepo
A repository that contains multiple projects. The University ERP uses a monorepo structure with Turborepo.

## N

### NestJS
A progressive Node.js framework for building efficient, scalable Node.js server-side applications. The University ERP backend is built with NestJS.

### Node.js
A JavaScript runtime built on Chrome's V8 JavaScript engine. The University ERP uses Node.js for the backend.

### npm (Node Package Manager)
The default package manager for Node.js. The University ERP uses npm for dependency management.

### NPM
Abbreviation for Node Package Manager.

### N+1 Query Problem
A common performance issue where N additional queries are executed for each result from an initial query. The University ERP avoids this using Prisma's include/select.

## O

### ORM (Object-Relational Mapping)
A technique that lets you query and manipulate data from a database using an object-oriented paradigm. The University ERP uses Prisma as its ORM.

### OTP (One-Time Password)
A password that is valid for only one login session or transaction. The University ERP uses OTP for email and mobile verification.

### Optimistic Locking
A concurrency control method that assumes conflicts between multiple transactions are rare. The University ERP uses optimistic locking for data consistency.

## P

### PostgreSQL
An open-source relational database management system. The University ERP uses PostgreSQL as its primary database.

### Prisma
A next-generation ORM for Node.js and TypeScript. The University ERP uses Prisma for database access.

### Pipe
In NestJS, a pipe is a class annotated with the @Injectable() decorator that implements the PipeTransform interface. Pipes transform input data to the desired form.

### Portal
A web application that provides a single point of access to information and services. The University ERP has admin and student portals.

### Production
The live environment where the application is deployed for end-users. The University ERP has production deployment procedures.

## Q

### Queue
A data structure that follows First-In-First-Out (FIFO) principle. The University ERP uses Redis-based queues for background job processing.

### Query
A request for data or information from a database. The University ERP uses Prisma queries for database operations.

## R

### React
A JavaScript library for building user interfaces. The University ERP frontend is built with React.

### Redis
An open-source, in-memory data structure store used as a database, cache, and message broker. The University ERP uses Redis for caching and queuing.

### Role
A set of permissions assigned to a user. The University ERP uses roles for authorization.

### RBAC (Role-Based Access Control)
An approach to restricting system access to authorized users. The University ERP uses RBAC for authorization.

### REST (Representational State Transfer)
An architectural style for designing networked applications. The University API follows REST principles.

### Router
In React, a router manages navigation between different components. The University ERP uses React Router for navigation.

## S

### Schema
In databases, a schema is the structure of a database. In Prisma, the schema.prisma file defines the database schema.

### Section
A subdivision of a batch. The University ERP organizes students into sections for better management.

### Service
In NestJS, a service is a class annotated with the @Injectable() decorator that contains business logic. Services are used by controllers.

### Stream
A particular specialization or focus within a course. The University ERP manages streams for different course specializations.

### Subject
A specific topic within a course. The University ERP manages subjects and their associated teachers and schedules.

### Student
A person enrolled in a course of study at a university. The University ERP manages all student-related data.

### Staff
Employees of the university who are not faculty. The University ERP manages staff data and roles.

### SSL (Secure Sockets Layer)
A standard technology for keeping an internet connection secure. The University ERP uses SSL/TLS for secure communication.

## T

### TypeScript
A strongly typed programming language that builds on JavaScript. The University ERP uses TypeScript for both backend and frontend.

### Token
In authentication, a token is a piece of data that proves a user's identity. The University ERP uses JWT tokens.

### Transport
The system for moving people from one place to another. The University ERP manages university transport services.

### Transaction
A sequence of operations performed as a single logical unit of work. The University ERP uses database transactions for data consistency.

### Turborepo
A build system for JavaScript/TypeScript monorepos. The University ERP uses Turborepo for build orchestration.

## U

### University
An institution of higher education. The University ERP is designed for university management.

### User
A person who uses the University ERP system. Users can be students, staff, faculty, or administrators.

### Unit Test
A test that verifies the functionality of a specific section of code. The University ERP uses Jest for unit testing.

## V

### Validation
The process of checking data for correctness and completeness. The University ERP uses class-validator for DTO validation.

### Vite
A build tool that aims to provide a faster and leaner development experience for modern web projects. The University ERP uses Vite for the frontend build.

### Version Control
The management of changes to documents, computer programs, large websites, and other collections of information. The University ERP uses Git for version control.

## W

### Workflow
A sequence of processes that accomplish a specific task. The University ERP has a workflow engine for managing business processes.

### Worker
A process that performs background tasks. The University ERP uses workers for background job processing.

### Winston
A logging library for Node.js. The University ERP uses Winston for structured logging.

### WebSocket
A communication protocol that provides full-duplex communication channels over a single TCP connection. The University ERP uses WebSockets for real-time features.

## X

### XSS (Cross-Site Scripting)
A security vulnerability that allows attackers to inject malicious scripts into web pages. The University ERP implements measures to prevent XSS attacks.

## Y

### YAML (YAML Ain't Markup Language)
A human-readable data serialization language. The University ERP uses YAML for Docker Compose configuration.

## Z

### Zone
In NestJS, a zone is a context that persists across async operations. The University ERP uses zones for request-scoped data.

## Acronyms Summary

| Acronym | Full Form |
|---------|-----------|
| API | Application Programming Interface |
| BTECH | Bachelor of Technology |
| CBE | Curriculum Based Education |
| CORS | Cross-Origin Resource Sharing |
| DTO | Data Transfer Object |
| E2E | End-to-End |
| HPA | Health Pod Autoscaler |
| HTTP | Hypertext Transfer Protocol |
| HTTPS | HTTP Secure |
| JWT | JSON Web Token |
| K8s | Kubernetes |
| LTS | Long Term Support |
| N+1 | N plus one query problem |
| npm | Node Package Manager |
| ORM | Object-Relational Mapping |
| OTP | One-Time Password |
| RBAC | Role-Based Access Control |
| REST | Representational State Transfer |
| SSL | Secure Sockets Layer |
| XSS | Cross-Site Scripting |

## Technology Stack Terms

### Backend Technologies

- **NestJS**: Progressive Node.js framework
- **TypeScript**: Typed JavaScript superset
- **Prisma**: Next-generation ORM
- **PostgreSQL**: Relational database
- **Redis**: In-memory data store
- **Bull**: Queue system
- **MinIO**: Object storage
- **Winston**: Logging library
- **Passport**: Authentication middleware
- **JWT**: JSON Web Tokens

### Frontend Technologies

- **React**: UI library
- **TypeScript**: Typed JavaScript superset
- **Vite**: Build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching library
- **React Router**: Routing library
- **Axios**: HTTP client
- **Zod**: Schema validation

### DevOps Technologies

- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Kubernetes**: Container orchestration
- **GitHub Actions**: CI/CD
- **Prometheus**: Monitoring
- **Grafana**: Visualization
- **Nginx**: Web server and reverse proxy

## University-Specific Terms

### Academic Terms

- **Academic Year**: Period of academic activity
- **Semester**: Half of an academic year
- **Term**: A subdivision of an academic year
- **Batch**: Group of students admitted in a year
- **Section**: Subdivision of a batch
- **Course**: A subject or module
- **Stream**: Specialization within a course
- **Subject**: Specific topic within a course
- **Credits**: Weight assigned to a course
- **CGPA**: Cumulative Grade Point Average

### Administrative Terms

- **Department**: Academic division
- **Program**: Course of study
- **Degree**: Academic qualification
- **Diploma**: Certificate of completion
- **Certificate**: Document of achievement
- **Transcript**: Academic record
- **Marksheet**: Examination results document
- **Attendance Record**: Record of presence/absence
- **Fee Structure**: Fee schedule
- **Scholarship**: Financial aid

### Examination Terms

- **Exam**: Formal test
- **Exam Paper**: Document with questions
- **Question**: Individual test item
- **Mark**: Score for a question
- **Grade**: Letter grade
- **Result**: Overall exam outcome
- **Reassessment**: Re-evaluation of marks
- **Supplementary Exam**: Additional exam for failed subjects
- **Passing Marks**: Minimum marks to pass
- **Total Marks**: Maximum possible marks

## Additional Resources

- [NestJS Glossary](https://docs.nestjs.com/)
- [React Glossary](https://react.dev/)
- [Prisma Glossary](https://www.prisma.io/docs/)
- [Docker Glossary](https://docs.docker.com/)
- [Kubernetes Glossary](https://kubernetes.io/docs/)
