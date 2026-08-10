# Database Schema Sync — `.21` → `.17`

## Purpose

This guide explains how to synchronize the PostgreSQL **database schema** on server `.17` with the working/current database on server `.21`.

The goal is:

```text
Working server
192.168.1.21
      │
      │  schema comparison
      ▼
Server being fixed
192.168.1.17
      │
      ▼
Make tables / columns / indexes / foreign keys match .21
```

The existing `.17` database can be changed as required to match `.21`.

> **Important:** `.21` is treated as the source of truth.

---

# 1. Understand the problem

The application on `.17` was returning:

```text
GET /api/auth/public/course-types
400 Bad Request
```

The backend logs also showed:

```text
WARN [ExceptionFilter] Unmapped Prisma error P2022
```

and:

```text
The table `public.hostel_requests` does not exist in the current database.
```

However:

```bash
npx prisma migrate status
```

reported:

```text
Database schema is up to date!
```

This means migration history alone was not enough to prove that `.17` and `.21` had identical actual PostgreSQL schemas.

---

# 2. Confirm the application directory

On `.17`:

```bash
cd /home/admin/UniversityERP/apps/core-api
```

Confirm:

```bash
pwd
```

Expected:

```text
/home/admin/UniversityERP/apps/core-api
```

The directory should contain:

```text
prisma/
package.json
src/
dist/
```

---

# 3. Verify PostgreSQL is running on `.17`

Run:

```bash
ss -lntp | grep 5432
```

Expected result is something similar to:

```text
LISTEN 0 4096 0.0.0.0:5432 0.0.0.0:*
LISTEN 0 4096 [::]:5432 [::]:*
```

This confirms PostgreSQL is listening on port `5432`.

---

# 4. Connect to the `.17` database

The `.17` application uses a database similar to:

```text
postgresql://erp_user:PASSWORD@localhost:5432/university_erp
```

Connect:

```bash
psql -h localhost -p 5432 -U erp_user -d university_erp
```

Enter the database password.

Expected:

```text
psql (16.x)
Type "help" for help.

university_erp=#
```

---

# 5. Verify the `.17` database

For example:

```sql
\d public.fee_heads
```

Also check:

```sql
\d public.stream_labels
```

and:

```sql
\d public.hostel_requests
```

Initially, `.17` did not have:

```text
public.hostel_requests
```

which matched the backend error.

Exit PostgreSQL:

```sql
\q
```

---

# 6. Check Prisma migration status on `.17`

From:

```text
/home/admin/UniversityERP/apps/core-api
```

run:

```bash
npx prisma migrate status
```

The result was:

```text
11 migrations found in prisma/migrations

Database schema is up to date!
```

This is useful, but it does **not** guarantee that `.17` and `.21` have identical actual database structures.

---

# 7. Verify that `.21` is reachable

From `.17`, connect directly to the PostgreSQL server on `.21`:

```bash
psql -h 192.168.1.21 -p 5432 -U erp_user -d university_erp \
  -c "SELECT current_database(), current_user, version();"
```

Expected result:

```text
current_database | current_user | version
-----------------+--------------+----------------
university_erp   | erp_user     | PostgreSQL 16.x ...
```

This confirms that `.17` can access the `.21` database.

---

# 8. Compare `.17` and `.21`

The important operation is:

```text
FROM = .17 database
TO   = .21 database
```

This asks Prisma:

> What SQL changes are required to make `.17` structurally match `.21`?

Do **not** reverse these URLs.

The command used was:

```bash
npx prisma migrate diff \
  --from-url "postgresql://erp_user:YOUR_PASSWORD@localhost:5432/university_erp" \
  --to-url "postgresql://erp_user:YOUR_PASSWORD@192.168.1.21:5432/university_erp" \
  --script \
  -o /tmp/schema-sync.sql
```

Replace:

```text
YOUR_PASSWORD
```

with the actual database password when running the command.

Do not expose the real password in documentation, Git, screenshots, or chat.

---

# 9. Inspect the generated schema difference

The comparison creates:

```text
/tmp/schema-sync.sql
```

Inspect it:

```bash
cat /tmp/schema-sync.sql
```

or:

```bash
less /tmp/schema-sync.sql
```

The generated SQL showed differences such as:

### Missing columns

```sql
ALTER TABLE "batch_term_subjects"
ADD COLUMN "sort_order" INTEGER NOT NULL DEFAULT 0;
```

```sql
ALTER TABLE "fee_heads"
ADD COLUMN "year_overrides" JSONB;
```

### Missing tables

For example:

```sql
CREATE TABLE "hostel_requests" (...)
```

and:

```sql
CREATE TABLE "hostel_fee_components" (...)
```

```sql
CREATE TABLE "hostel_refund_requests" (...)
```

```sql
CREATE TABLE "notification_logs" (...)
```

```sql
CREATE TABLE "student_concessions" (...)
```

```sql
CREATE TABLE "student_term_elections" (...)
```

```sql
CREATE TABLE "program_seat_approvals" (...)
```

```sql
CREATE TABLE "batch_setup_drafts" (...)
```

### Missing indexes

For example:

```sql
CREATE INDEX "hostel_requests_institute_id_status_idx"
ON "hostel_requests"("institute_id", "status");
```

### Missing foreign keys

For example:

```sql
ALTER TABLE "student_term_elections"
ADD CONSTRAINT ...
```

### Obsolete structures

The diff also contained changes such as:

```sql
DROP TABLE "batch_admission_start_requests";
```

```sql
DROP TABLE "clone_test_check";
```

and:

```sql
ALTER TABLE "programmes"
DROP COLUMN "intake_capacity";
```

These occur because `.21` is being treated as the current/source-of-truth schema.

---

# 10. Do NOT blindly use `migrate reset`

Do not use:

```bash
npx prisma migrate reset
```

Do not use:

```bash
npx prisma db push --force-reset
```

Do not restore the complete `.21` database over `.17`.

Those operations can destroy or replace existing data.

The purpose here is to synchronize the actual schema using the generated diff.

---

# 11. Apply the schema synchronization

Once the generated `/tmp/schema-sync.sql` has been reviewed, apply it to `.17`.

Run:

```bash
psql -h localhost -p 5432 -U erp_user \
  -d university_erp \
  -v ON_ERROR_STOP=1 \
  -1 \
  -f /tmp/schema-sync.sql
```

### Important options

```text
-v ON_ERROR_STOP=1
```

means:

> Stop immediately if any SQL statement fails.

And:

```text
-1
```

means:

> Execute the entire SQL file inside one transaction.

Therefore:

```text
All changes succeed
       ↓
COMMIT
```

or:

```text
Any error
       ↓
ROLLBACK
```

This prevents the database from being left halfway through the schema update.

---

# 12. Verify the newly created tables

After the SQL completes successfully:

```bash
psql -h localhost -p 5432 -U erp_user \
  -d university_erp \
  -c '\d public.hostel_requests'
```

Also check:

```bash
psql -h localhost -p 5432 -U erp_user \
  -d university_erp \
  -c '\d public.fee_heads'
```

And optionally:

```bash
psql -h localhost -p 5432 -U erp_user \
  -d university_erp \
  -c '\dt public.*'
```

The previously missing:

```text
hostel_requests
```

should now exist.

---

# 13. Regenerate Prisma Client

After the database schema has been synchronized:

```bash
npx prisma generate
```

This ensures the Prisma Client used by the API is generated from the current Prisma schema.

---

# 14. Restart the backend

Restart the PM2 application:

```bash
pm2 restart core-api
```

Check:

```bash
pm2 status
```

Then:

```bash
pm2 logs core-api --lines 100
```

Look for new Prisma errors.

In particular, the previous error:

```text
P2022
```

should no longer occur for schema-related missing columns.

The previous scheduler error:

```text
The table `public.hostel_requests` does not exist
```

should also disappear.

---

# 15. Test the API

Test the endpoint directly through the HTTPS frontend/proxy:

```bash
curl -k -i \
  https://192.168.1.17:5173/api/auth/public/course-types
```

Or test the backend directly:

```bash
curl -i \
  http://localhost:3000/api/auth/public/course-types
```

The endpoint should no longer return the previous:

```json
{
  "success": false,
  "statusCode": 400,
  "message": "Invalid request"
}
```

Instead, it should return the actual course-type response.

---

# 16. Verify the schema is now equal to `.21`

After synchronization, generate the comparison again:

```bash
npx prisma migrate diff \
  --from-url "postgresql://erp_user:YOUR_PASSWORD@localhost:5432/university_erp" \
  --to-url "postgresql://erp_user:YOUR_PASSWORD@192.168.1.21:5432/university_erp" \
  --script \
  -o /tmp/schema-check.sql
```

Then:

```bash
cat /tmp/schema-check.sql
```

Ideally:

```text
/tmp/schema-check.sql
```

should be empty or contain no meaningful schema changes.

That indicates:

```text
.17 PostgreSQL schema
        =
.21 PostgreSQL schema
```

---

# 17. Final architecture

After the synchronization, the intended state is:

```text
                    ┌─────────────────────┐
                    │   Working Server     │
                    │       .21            │
                    │                     │
                    │ PostgreSQL           │
                    │ university_erp       │
                    └──────────┬──────────┘
                               │
                               │
                         source of truth
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Server .17        │
                    │                     │
                    │ Core API            │
                    │ PostgreSQL          │
                    │ university_erp      │
                    │                     │
                    │ schema synchronized │
                    └─────────────────────┘
```

---

# 18. What caused the original problem?

The important discovery was that the two databases had different actual schemas.

`.17` was missing structures that existed on `.21`.

For example:

```text
.21
 ├── hostel_requests
 ├── hostel_fee_components
 ├── hostel_refund_requests
 ├── notification_logs
 ├── student_concessions
 ├── student_term_elections
 ├── program_seat_approvals
 └── batch_setup_drafts

.17
 └── several of these were missing
```

The API code expected the newer schema.

For example:

```ts
await this.prisma.hostelRequest.findMany(...)
```

but PostgreSQL on `.17` reported:

```text
The table `public.hostel_requests` does not exist
```

That produced Prisma errors such as:

```text
P2022
```

The frontend/proxy was therefore not the root problem.

---

# 19. Important distinction: proxy vs database

The frontend request was:

```text
https://192.168.1.17:5173/api/auth/public/course-types
```

Vite was configured with:

```ts
proxy: {
  '/api': {
    target: 'http://localhost:3000',
    changeOrigin: true,
  }
}
```

Therefore:

```text
Browser
   │
   │ HTTPS :5173
   ▼
Vite
   │
   │ /api → http://localhost:3000
   ▼
NestJS Core API
   │
   ▼
PostgreSQL
```

The fact that:

```bash
curl http://localhost:3000/api/auth/public/course-types
```

also returned:

```text
400 Bad Request
```

proved that the issue was already inside the backend/database path and was not merely the Vite proxy.

---

# 20. About the React DevTools error

The browser error:

```text
Uncaught Error:
Attempting to use a disconnected port object
```

with:

```text
react_devtools_backend_compact.js
backendManager.js
postMessage
```

is generally associated with the React Developer Tools browser extension losing its communication port.

It is separate from the PostgreSQL schema problem.

The important backend errors were:

```text
P2022
```

and:

```text
The table `public.hostel_requests` does not exist
```

---

# 21. Recommended future practice

The root issue happened because `.17` and `.21` had diverged database schemas.

To prevent this in the future:

```text
Code change
    ↓
Prisma schema change
    ↓
Create migration
    ↓
Commit migration to Git
    ↓
Deploy code + migration
    ↓
Run migration on target DB
```

Use:

```bash
npx prisma migrate dev
```

for development migration creation, and:

```bash
npx prisma migrate deploy
```

for deployment environments.

Avoid making production schema changes manually unless there is a deliberate recovery/migration procedure.

The database schema should be version-controlled through:

```text
prisma/schema.prisma
prisma/migrations/
```

so that `.17`, `.21`, staging, and future servers do not silently diverge.

---

# Quick Command Summary

## On `.17`

```bash
cd /home/admin/UniversityERP/apps/core-api
```

Check PostgreSQL:

```bash
ss -lntp | grep 5432
```

Check local DB:

```bash
psql -h localhost -p 5432 -U erp_user -d university_erp
```

Check migrations:

```bash
npx prisma migrate status
```

---

## Verify `.21`

```bash
psql -h 192.168.1.21 -p 5432 -U erp_user -d university_erp \
  -c "SELECT current_database(), current_user, version();"
```

---

## Generate `.17 → .21` schema diff

```bash
npx prisma migrate diff \
  --from-url "postgresql://erp_user:YOUR_PASSWORD@localhost:5432/university_erp" \
  --to-url "postgresql://erp_user:YOUR_PASSWORD@192.168.1.21:5432/university_erp" \
  --script \
  -o /tmp/schema-sync.sql
```

Inspect:

```bash
cat /tmp/schema-sync.sql
```

---

## Apply

```bash
psql -h localhost -p 5432 -U erp_user \
  -d university_erp \
  -v ON_ERROR_STOP=1 \
  -1 \
  -f /tmp/schema-sync.sql
```

---

## Regenerate Prisma

```bash
npx prisma generate
```

---

## Restart API

```bash
pm2 restart core-api
```

Check:

```bash
pm2 logs core-api --lines 100
```

---

## Test

```bash
curl -k -i \
  https://192.168.1.17:5173/api/auth/public/course-types
```

---

## Verify `.17 → .21` is now empty

```bash
npx prisma migrate diff \
  --from-url "postgresql://erp_user:YOUR_PASSWORD@localhost:5432/university_erp" \
  --to-url "postgresql://erp_user:YOUR_PASSWORD@192.168.1.21:5432/university_erp" \
  --script \
  -o /tmp/schema-check.sql
```

```bash
cat /tmp/schema-check.sql
```

Expected:

```text
No schema differences
```

or an empty SQL file.
