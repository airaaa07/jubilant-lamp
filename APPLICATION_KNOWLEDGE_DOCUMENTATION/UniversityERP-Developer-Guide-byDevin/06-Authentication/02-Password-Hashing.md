# Password Hashing

## Purpose

This document explains password hashing used in the University ERP authentication system. It details how passwords are hashed, verified, and stored securely.

## Why This Document Exists

**Confirmed by Code**: The University ERP uses bcrypt for password hashing. Understanding password hashing is critical for:
- Storing passwords securely
- Preventing password theft
- Implementing secure authentication
- Debugging password issues
- Meeting security requirements

Without understanding password hashing, developers may store passwords insecurely or may introduce security vulnerabilities.

## Where This Is Used

- **Onboarding**: New developers learn password hashing
- **Feature Development**: Implementing password hashing
- **Code Reviews**: Reviewing password hashing code
- **Security**: Implementing security measures
- **Compliance**: Meeting security standards

## Dependencies

### Password Hashing Dependencies

**Confirmed by Code**: Password hashing depends on:

- **bcrypt**: Password hashing library
- **Prisma**: User data storage
- **TypeScript**: Type-safe password handling

## Internal Architecture

### Password Hashing Architecture

**Confirmed by Code**: Password hashing follows secure practices.

```
┌─────────────────────────────────────────────────────────┐
│              Password Hashing Flow                        │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Plain Text   │  │  Hashing       │  │  Stored Hash   │
│  Password    │  │  (bcrypt)       │  │  (Database)     │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Password Hashing

**Confirmed by Code**: Passwords hashed with bcrypt.

**Hash Password**:
```typescript
import * as bcrypt from 'bcrypt';

async hashPassword(password: string): Promise<string> {
  const saltRounds = 10;
  const hashedPassword = await bcrypt.hash(password, saltRounds);
  return hashedPassword;
}
```

**What This Does**:
- **bcrypt.hash()**: Hashes password with bcrypt
- **saltRounds**: Number of salt rounds (10)
- **Async**: Async operation
- **Returns**: Hashed password string

**Usage**:
```typescript
const hashedPassword = await bcrypt.hash('password', 10);
// Output: $2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
```

### Password Verification

**Confirmed by Code**: Passwords verified with bcrypt.

**Verify Password**:
```typescript
async verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
  const isMatch = await bcrypt.compare(password, hashedPassword);
  return isMatch;
}
```

**What This Does**:
- **bcrypt.compare()**: Compares password with hash
- **Async**: Async operation
- **Returns**: Boolean indicating match

**Usage**:
```typescript
const isMatch = await bcrypt.compare('password', hashedPassword);
// Output: true or false
```

### Password Strength

**Confirmed by Code**: Password strength validated.

**Password Validation**:
```typescript
import { z } from 'zod';

const PasswordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character');
```

**What This Does**:
- **min(8)**: Minimum 8 characters
- **regex(/[A-Z]/)**: At least one uppercase
- **regex(/[a-z]/)**: At least one lowercase
- **regex(/[0-9]/)**: At least one number
- **regex(/[^A-Za-z0-9]/)**: At least one special character

## Database Interactions

### Password-Database Flow

**Confirmed by Code**: Hashed passwords stored in database.

**Flow**:
```
Plain Password → Hash with bcrypt → Store Hash in Database
```

## Redis Interactions

### Password-Redis Flow

**Confirmed by Code**: Passwords don't interact with Redis.

**Flow**:
```
Password → No Redis interaction
```

## Queue Interactions

### Password-Queue Flow

**Confirmed by Code**: Passwords don't interact with queues.

**Flow**:
```
Password → No queue interaction
```

## Worker Interactions

### Password-Worker Flow

**Confirmed by Code**: Workers don't handle passwords.

**Flow**:
```
Worker → No password interaction
```

## Business Rules

### Password Hashing Rules

**Confirmed by Code**: Password hashing follows these rules:

1. **Hashing**: Always hash passwords before storage
2. **bcrypt**: Use bcrypt for hashing
3. **Salt Rounds**: Use 10 salt rounds
4. **Verification**: Verify passwords with bcrypt.compare()
5. **Strength**: Validate password strength

### Password Strength Rules

**Confirmed by Code**: Password strength rules:

1. **Minimum Length**: At least 8 characters
2. **Uppercase**: At least one uppercase letter
3. **Lowercase**: At least one lowercase letter
4. **Number**: At least one number
5. **Special Character**: At least one special character

## Security

### Password Security

**Confirmed by Code**: Security considerations for passwords:

1. **Hashing**: Always hash passwords
2. **bcrypt**: Use bcrypt (not md5, sha1)
3. **Salt Rounds**: Use adequate salt rounds
4. **Never Store Plain Text**: Never store plain text passwords
5. **Never Log Passwords**: Never log passwords

## Performance Considerations

### Password Hashing Performance

**Confirmed by Code**: Performance considerations:

1. **Salt Rounds**: Balance security and performance (10 rounds)
2. **Async Operations**: Use async for hashing
3. **Caching**: Don't cache hashed passwords
4. **Validation**: Validate password strength before hashing
5. **Rate Limiting**: Rate limit password attempts

## Common Mistakes

### Mistake 1: Storing Plain Text Passwords

**Symptom**: Security vulnerability

**Cause**: Not hashing passwords

**Fix**:
```typescript
// Hash password before storage
const hashedPassword = await bcrypt.hash(password, 10);
```

### Mistake 2: Using Weak Hashing

**Symptom**: Passwords easily cracked

**Cause**: Using weak hashing (md5, sha1)

**Fix**:
```typescript
// Use bcrypt
const hashedPassword = await bcrypt.hash(password, 10);
```

### Mistake 3: Not Validating Password Strength

**Symptom**: Weak passwords allowed

**Cause**: Not validating password strength

**Fix**:
```typescript
// Add password validation
const PasswordSchema = z.string().min(8).regex(/[A-Z]/);
```

## Debugging Guide

### Password Debugging

**Issue**: Password verification failing

**Investigation**:
1. Check password hashing
2. Check password comparison
3. Check stored hash
4. Check password input
5. Test with known password

**Tools**:
- bcrypt.compare()
- Hash inspector
- Database logs
- Console logs

## Future Enhancements

### Password Policies

**Status**: Not implemented

**Proposal**: Implement password policies:
- Password expiry
- Password history
- Password complexity requirements
- Account lockout after failed attempts
- Password reset flow

### Multi-Factor Authentication

**Status**: Not implemented

**Proposal**: Implement MFA:
- TOTP-based MFA
- SMS-based MFA
- Email-based MFA
- Better security
- Required for sensitive operations

## Production Considerations

### Production Passwords

**Production Deployment**:
- Use adequate salt rounds
- Validate password strength
- Implement rate limiting
- Monitor failed login attempts
- Implement account lockout

### Password Monitoring

**Monitoring Metrics**:
- Failed login attempts
- Password reset requests
- Account lockouts
- Password strength distribution
- Password change frequency

## Example Requests

### Password Hashing Example

**Request**: Hash password

```typescript
const hashedPassword = await bcrypt.hash('password', 10);
```

## Example Responses

### Password Hashing Response

**Response**: Hashed password

```
$2b$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
```

## Sequence Diagrams

### Password Hashing Flow

```
User Password → Hash with bcrypt → Store Hash in Database
```

### Password Verification Flow

```
User Password → Compare with Hash → Match? → Access Granted/Denied
```

## Architecture Diagrams

### Password Hashing Architecture

```
┌─────────────────────────────────────────────────────────┐
│              User Input                                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Password Validation                          │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              bcrypt Hashing                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Database                                     │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: Why use bcrypt instead of md5 or sha1?

**Answer**: bcrypt vs md5/sha1:
- bcrypt: Designed for passwords, slow, salted
- md5/sha1: Fast, not designed for passwords, vulnerable to rainbow tables
- bcrypt: Adaptive cost factor
- md5/sha1: Fixed cost
- bcrypt: Built-in salt

### Q2: How does bcrypt work?

**Answer**: bcrypt works via:
- Blowfish encryption algorithm
- Salt added to each password
- Multiple rounds (cost factor)
- Slow hashing (prevents brute force)
- Output: Hashed password string

### Q3: How do you verify passwords?

**Answer**: Password verification via:
- Hash input password with bcrypt
- Compare with stored hash
- bcrypt.compare() handles this
- Returns boolean
- Secure comparison

## Exercises

### Exercise 1: Hash a Password

**Task**: Hash a password with bcrypt.

**Steps**:
1. Import bcrypt
2. Hash password with 10 salt rounds
3. Store hash
4. Test hash
5. Verify hash

**Verification**:
- Password hashed
- Hash stored
- Hash verified
- Tests pass

### Exercise 2: Verify a Password

**Task**: Verify a password against hash.

**Steps**:
1. Get stored hash
2. Get input password
3. Compare with bcrypt.compare()
4. Return result
5. Test verification

**Verification**:
- Password compared
- Result correct
- Tests pass

## Real Production Scenarios

### Scenario 1: Password Hash Breach

**Situation**: Password hashes leaked

**Response**:
1. Force password reset for all users
2. Increase salt rounds
3. Implement MFA
4. Monitor for suspicious activity
5. Notify users

### Scenario 2: Password Reset

**Situation**: User forgot password

**Response**:
1. Generate reset token
2. Send reset email
3. Verify reset token
4. Allow password reset
5. Hash new password

## Navigation

**Next Section**: [03-Session-Management](./03-Session-Management.md)

**Previous Section**: [01-JWT-Tokens](./01-JWT-Tokens.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [19-Security](../19-Security/README.md) - Security details
