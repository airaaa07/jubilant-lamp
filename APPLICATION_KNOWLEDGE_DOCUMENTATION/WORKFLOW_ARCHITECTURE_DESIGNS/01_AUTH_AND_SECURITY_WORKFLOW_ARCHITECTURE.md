# Technical Workflow Architecture: Authentication, Guards & Security

## Overview
This document details the end-to-end technical architecture, request guard pipeline, token lifecycle, password history validation, OTP generation, and database state mutations for system authentication and security.

---

## 🔄 End-to-End Sequence Diagram: Authentication & Guard Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client App
    participant TG as ThrottlerGuard (Rate Limiter)
    participant AG as GlobalJwtAuthGuard
    participant MG as MaintenanceGuard
    participant AuthC as AuthController
    participant AuthS as AuthService
    participant DB as PostgreSQL Database
    participant Redis as Redis Cache

    User->>TG: POST /api/v1/auth/login { email, password }
    Note over TG: Rate Limit Check (5 req/min on login)
    TG->>AG: Request Allowed
    Note over AG: Public Route Check (@Public() decorator)
    AG->>AuthC: Forward Unauthenticated Request
    AuthC->>AuthS: login(dto)
    AuthS->>DB: Query User by email
    DB-->>AuthS: Return User Record & Password Hash
    
    alt Account Locked / Inactive
        AuthS-->>User: Throw 401 Unauthorized ("Account locked")
    else Invalid Password
        AuthS->>DB: Increment failedLoginAttempts
        AuthS-->>User: Throw 401 Unauthorized ("Invalid credentials")
    else Password Match Verified (Bcrypt)
        AuthS->>DB: Reset failedLoginAttempts = 0, update lastLoginAt
        AuthS->>AuthS: Generate Access Token (JWT) & Refresh Token
        AuthS->>Redis: Store Refresh Token Hash (TTL: 7 Days)
        AuthS-->>User: Return { accessToken, refreshToken, userProfile }
    end
```

---

## ⚙️ Request Processing Pipeline Architecture

```mermaid
flowchart TD
    Req["Incoming HTTP Request"] --> RateLimit["1. ThrottlerGuard Check<br/>(300 req/min default, 5/min sensitive)"]
    RateLimit -- "Exceeded" --> ERR429["HTTP 429 Too Many Requests"]
    RateLimit -- "Pass" --> AuthCheck["2. GlobalJwtAuthGuard Check"]
    
    AuthCheck -- "Has @Public() Header" --> MaintCheck["3. MaintenanceGuard Check"]
    AuthCheck -- "Protected Route" --> VerifyJWT["Verify Bearer Token Signature & Expiry"]
    
    VerifyJWT -- "Invalid / Expired" --> ERR401["HTTP 401 Unauthorized"]
    VerifyJWT -- "Valid JWT" --> PopulateReq["Populate req.user Context"]
    PopulateReq --> MaintCheck
    
    MaintCheck -- "MAINTENANCE_MODE = true & Non-SuperAdmin" --> ERR503["HTTP 503 Service Unavailable"]
    MaintCheck -- "Pass" --> ScopeCheck["4. Role & Tenant Scope Guard"]
    
    ScopeCheck -- "Scope Mismatch" --> ERR403["HTTP 403 Forbidden"]
    ScopeCheck -- "Authorized" --> Controller["Execute Controller Action"]
```

---

## 📊 Database Mutations & State Changes

### 1. User Table (`users`)
- `failed_login_attempts`: Incremented on invalid password; reset to `0` on successful authentication.
- `locked_until`: Populated with timestamp if `failed_login_attempts >= MAX_ATTEMPTS`.
- `last_login_at`: Updated to `now()` upon successful token issuance.

### 2. Password History Table (`password_history`)
- When password is changed/reset (`setupAccount` / `resetPassword`):
  - `INSERT INTO password_history (user_id, password_hash, created_at)`
  - Query checks: `SELECT * FROM password_history WHERE user_id = :id ORDER BY created_at DESC LIMIT N`. Throws error if new password matches any historical hash.
