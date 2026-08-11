# University ERP — Application Operations & Troubleshooting Guide

This README contains commonly used commands for running, monitoring, troubleshooting, building, and maintaining the **University ERP** application.

---

## 1. Project Location

Main project directory:

```bash
/home/admin/UniversityERP
```

Core API:

```bash
/home/admin/UniversityERP/apps/core-api
```

Admin Portal:

```bash
/home/admin/UniversityERP/web/admin-portal
```

---

# 2. Prisma Studio — Database Management

Prisma Studio can be used to visually inspect and manage the PostgreSQL database.

Run:

```bash
npx prisma studio \
  --schema=/home/admin/UniversityERP/apps/core-api/prisma/schema.prisma
```

Then open:

```text
http://localhost:5555
```

> If Prisma Studio is running on a remote server and you want to access it from your local machine, use SSH port forwarding.

---

# 3. PM2 — Application Management

The application processes are managed using PM2.

## Check PM2 Processes

```bash
pm2 list
```

or:

```bash
pm2 status
```

---

## View Logs for All Applications

```bash
pm2 logs
```

---

## View Admin Portal Logs

```bash
pm2 logs admin-portal
```

---

## View Core API Logs

```bash
pm2 logs core-api
```

---

# 4. Application Log Files

Application logs are stored under:

```text
/var/log/university-erp/
```

## Core API

### Output Logs

```bash
tail -f /var/log/university-erp/core-api-out.log
```

### Error Logs

```bash
tail -f /var/log/university-erp/core-api-error.log
```

---

## Admin Portal

### Output Logs

```bash
tail -f /var/log/university-erp/portal-out.log
```

### Error Logs

```bash
tail -f /var/log/university-erp/admin-portal-error.log
```

---

# 5. Worker Logs

The following background workers run inside Docker containers.

## CBE Engine

```bash
docker logs -f erp-cbe-engine
```

## Notification Worker

```bash
docker logs -f erp-notification-worker
```

## Certificate Generator

```bash
docker logs -f erp-cert-generator
```

---

# 6. Restart Applications

## Restart Admin Portal

```bash
pm2 restart admin-portal --update-env
```

## Restart Core API

```bash
pm2 restart core-api --update-env
```

## Restart All PM2 Applications

```bash
pm2 restart all --update-env
```

The `--update-env` option ensures that updated environment variables are passed to the restarted process.

---

# 7. Running the Admin Portal Manually

Go to:

```bash
cd /home/admin/UniversityERP/web/admin-portal
```

Run the development server:

```bash
npm run dev -- --host 0.0.0.0 --port 5173
```

The portal will listen on:

```text
Port: 5173
```

---

# 8. Building the Core API

Go to the Core API directory:

```bash
cd /home/admin/UniversityERP/apps/core-api
```

Build the backend:

```bash
npm run build
```

After building, restart the Core API:

```bash
pm2 restart core-api
```

---

# 9. Docker Compose

To recreate and start all Docker Compose services:

```bash
docker compose up -d --force-recreate
```

Check running containers:

```bash
docker ps
```

---

# 10. PostgreSQL Container

To open a shell inside the PostgreSQL container:

```bash
docker exec -it erp-postgres sh
```

---

# 11. Updating Environment Variables

When `.env` values are changed, restart PM2 applications with:

```bash
pm2 restart all --update-env
```

---

## Check Whether PM2 Received the Updated Environment

First check the PM2 process ID:

```bash
pm2 list
```

Then:

```bash
pm2 env <id> | grep DATABASE_URL
```

For example:

```bash
pm2 env 0 | grep DATABASE_URL
```

---

## If the Environment Variable Is Not Updated

From the project root:

```bash
cd /home/admin/UniversityERP
```

Load the `.env` variables:

```bash
set -a
source .env
set +a
```

Then restart the application:

```bash
pm2 restart core-api --update-env
```

Verify again:

```bash
pm2 env <id> | grep DATABASE_URL
```

---

# 12. Loading DATABASE_URL from `.env`

From a directory where the relative path is correct:

```bash
export $(grep DATABASE_URL ../../.env | xargs)
```

Check the value:

```bash
echo $DATABASE_URL
```

> Be careful when printing `DATABASE_URL`, because it may contain database credentials.

---

# 13. Prisma Migration Status

From the project root, load the `.env` file and check Prisma migration status:

```bash
export $(grep -v '^#' .env | xargs)
```

Then:

```bash
echo $DATABASE_URL
```

Check migration status:

```bash
npx dotenv -e .env -- \
  npx prisma migrate status \
  --schema apps/core-api/prisma/schema.prisma
```

---

# 14. Search for Prisma Error Handling

To search the source and compiled files for a specific Prisma error message:

```bash
grep -R "Unmapped Prisma error" src dist
```

Run this from:

```bash
/home/admin/UniversityERP/apps/core-api
```

---

# 15. PostgreSQL — Direct Database Connection

Connect directly to PostgreSQL:

```bash
psql -h localhost -p 5432 -U erp_user -d <dbName>
```

Replace:

```text
<dbName>
```

with the actual database name.

---

# 16. PostgreSQL Database Comparison

The following commands can be used to compare two PostgreSQL databases using Prisma.

Example scenario:

```text
Server .17 → Server .21
```

The Prisma migration diff shows what changes are required to make one database structure match the other.

---

## Compare Local Database Against Server .21

Go to:

```bash
cd /home/admin/UniversityERP/apps/core-api
```

Set the local `DATABASE_URL`:

```bash
export $(grep DATABASE_URL ../../.env | xargs)
```

Run:

```bash
npx prisma migrate diff \
  --from-url "$DATABASE_URL" \
  --to-url "postgresql://erp_user:PASSWORD@192.168.1.21:5432/<dbName>" \
  --script
```

This generates SQL showing the schema differences.

---

# 17. Generate Schema Sync SQL

To compare the database on the current server against the database on `192.168.1.21`:

```bash
npx prisma migrate diff \
  --from-url "postgresql://erp_user:<dbPassword>@localhost:5432/<dbName>" \
  --to-url "postgresql://erp_user:<dbPassword>@192.168.1.21:5432/<dbName>" \
  --script \
  -o /tmp/schema-sync.sql
```

The generated SQL will be saved to:

```text
/tmp/schema-sync.sql
```

---

# 18. Review the Generated SQL

Before applying any database changes, **always review the generated SQL**.

Run:

```bash
cat /tmp/schema-sync.sql
```

Check carefully for:

* `DROP TABLE`
* `DROP COLUMN`
* `ALTER TABLE`
* `CREATE TABLE`
* `CREATE INDEX`
* Foreign-key changes
* Data-destructive operations

Do not blindly execute generated SQL against a production database.

---

# 19. Apply Generated Schema Sync

If the generated SQL has been reviewed and is confirmed to be safe:

```bash
psql -h localhost -p 5432 -U erp_user \
  -d <dbName> \
  -v ON_ERROR_STOP=1 \
  -1 \
  -f /tmp/schema-sync.sql
```

### Options Used

| Option               | Purpose                                    |
| -------------------- | ------------------------------------------ |
| `-h localhost`       | PostgreSQL host                            |
| `-p 5432`            | PostgreSQL port                            |
| `-U erp_user`        | PostgreSQL user                            |
| `-d <dbName>`        | Target database                            |
| `-v ON_ERROR_STOP=1` | Stop immediately if an SQL error occurs    |
| `-1`                 | Run the script inside a single transaction |
| `-f`                 | Execute SQL from the specified file        |

The `-1` option is particularly useful for schema synchronization because the changes are executed as one transaction, allowing PostgreSQL to roll back the transaction if an error occurs.

---

# 20. Git History

## View Complete Commit History in Chronological Order

```bash
git log --reverse --oneline
```

This displays the oldest commit first and the newest commit last.

---

# 21. Compare Current Branch Against `main`

To check how many commits the `dev` branch is behind `main`:

```bash
git rev-list --count dev..main
```

### Important

This command answers:

> How many commits exist in `main` that are not present in `dev`?

For example:

```text
5
```

means `main` has 5 commits that `dev` does not have.

To see the actual commits:

```bash
git log --oneline dev..main
```

---

# 22. PM2 Process IDs

PM2 automatically assigns process IDs.

The IDs cannot be manually assigned.

For example:

```text
id   name
0    core-api
1    admin-portal
```

The IDs may increase if processes are repeatedly deleted and recreated.

---

## Reset PM2 IDs

If you want to reset the PM2 process numbering:

### Step 1 — Delete Existing Processes

```bash
pm2 delete all
```

Check:

```bash
pm2 status
```

There should be no PM2 processes.

---

## Step 2 — Start Core API First

From the project root:

```bash
cd /home/admin/UniversityERP
```

Start:

```bash
pm2 start ecosystem.native.config.js
```

The Core API should receive:

```text
id 0
```

---

## Step 3 — Start Admin Portal Second

```bash
cd /home/admin/UniversityERP/web/admin-portal
```

Run:

```bash
pm2 start npm \
  --name admin-portal \
  --cwd /home/admin/UniversityERP/web/admin-portal \
  -- run dev -- --host 0.0.0.0 --port 5173
```

The Admin Portal should receive:

```text
id 1
```

---

## Step 4 — Save PM2 Configuration

```bash
pm2 save
```

### Important

Do not depend on PM2 IDs for normal operations.

Prefer:

```bash
pm2 restart core-api
pm2 restart admin-portal
```

instead of:

```bash
pm2 restart 0
pm2 restart 1
```

The application names are more reliable than the automatically assigned PM2 IDs.

---

# 23. PM2 `start.sh` Configuration

For the Admin Portal, use the following PM2 configuration:

```bash
pm2 start npm \
  --name admin-portal \
  --cwd $PORTAL_DIR \
  -- run dev -- --host 0.0.0.0 --port 5173 \
  --error $LOG_DIR/portal-error.log \
  --output $LOG_DIR/portal-out.log
```

### Avoid

```bash
pm2 start --name admin-portal \
  --cwd $PORTAL_DIR \
  "npm run dev -- --host 0.0.0.0" \
  --error $LOG_DIR/portal-error.log \
  --output $LOG_DIR/portal-out.log
```

Using `pm2 start npm` explicitly tells PM2 that `npm` is the executable and that `run dev` should be passed as its arguments.

---

# 24. PM2 Monitoring

For an interactive PM2 monitoring view:

```bash
pm2 monitor
```

PM2 monitoring dashboard:

[PM2 Monitoring Dashboard](https://app.pm2.io/?utm_source=chatgpt.com#/bucket/6a72e4f762b9aee536853f9f)

### PM2 Account

Username:

```text
kirankumar.boinapally@slashcurate.com
```

> **Do not store the PM2 password in this README.** Keep it in a password manager or another secure credential store.

---

# 25. Quick Command Reference

## PM2

```bash
pm2 list
pm2 status
pm2 logs
pm2 logs core-api
pm2 logs admin-portal
pm2 restart core-api --update-env
pm2 restart admin-portal --update-env
pm2 restart all --update-env
pm2 monitor
pm2 save
```

---

## Application Logs

### Core API

```bash
tail -f /var/log/university-erp/core-api-out.log
tail -f /var/log/university-erp/core-api-error.log
```

### Admin Portal

```bash
tail -f /var/log/university-erp/portal-out.log
tail -f /var/log/university-erp/admin-portal-error.log
```

---

## Worker Logs

```bash
docker logs -f erp-cbe-engine
docker logs -f erp-notification-worker
docker logs -f erp-cert-generator
```

---

## Docker

```bash
docker ps
docker compose up -d --force-recreate
docker exec -it erp-postgres sh
```

---

## Prisma

```bash
npx prisma studio \
  --schema=/home/admin/UniversityERP/apps/core-api/prisma/schema.prisma
```

```bash
npx dotenv -e .env -- \
  npx prisma migrate status \
  --schema apps/core-api/prisma/schema.prisma
```

---

## Build

```bash
cd /home/admin/UniversityERP/apps/core-api
npm run build
pm2 restart core-api
```

---

## Git

```bash
git log --reverse --oneline
git rev-list --count dev..main
git log --oneline dev..main
```

---

# 26. Recommended Troubleshooting Flow

When the application is not working, check in this order:

### 1. Check PM2

```bash
pm2 status
```

Confirm:

```text
core-api       online
admin-portal   online
```

### 2. Check Core API Logs

```bash
pm2 logs core-api
```

or:

```bash
tail -f /var/log/university-erp/core-api-error.log
```

### 3. Check Admin Portal Logs

```bash
pm2 logs admin-portal
```

or:

```bash
tail -f /var/log/university-erp/admin-portal-error.log
```

### 4. Check Docker Containers

```bash
docker ps
```

### 5. Check Worker Logs

```bash
docker logs -f erp-cbe-engine
docker logs -f erp-notification-worker
docker logs -f erp-cert-generator
```

### 6. Check Database Connection

```bash
echo $DATABASE_URL
```

Then:

```bash
psql -h localhost -p 5432 -U erp_user -d <dbName>
```

### 7. Check Prisma Migration Status

```bash
npx dotenv -e .env -- \
  npx prisma migrate status \
  --schema apps/core-api/prisma/schema.prisma
```

### 8. Rebuild Core API if Code Was Changed

```bash
cd /home/admin/UniversityERP/apps/core-api
npm run build
pm2 restart core-api --update-env
```

### 9. If Environment Variables Were Changed

```bash
pm2 restart all --update-env
```

Then verify:

```bash
pm2 env <id> | grep DATABASE_URL
```

---

# 27. Important Database Safety Notes

Before running any command that changes a database:

1. Confirm the **source database**.
2. Confirm the **target database**.
3. Review `/tmp/schema-sync.sql`.
4. Check for destructive operations such as:

   * `DROP TABLE`
   * `DROP COLUMN`
   * `TRUNCATE`
   * destructive `ALTER TABLE`
5. Take a database backup when appropriate.
6. Use `ON_ERROR_STOP=1`.
7. Prefer running schema changes inside a transaction where possible.

Never assume that `prisma migrate diff --script` is safe to execute without reviewing the generated SQL.

---

# 28. Important Paths

| Component        | Path                                                           |
| ---------------- | -------------------------------------------------------------- |
| Project Root     | `/home/admin/UniversityERP`                                    |
| Core API         | `/home/admin/UniversityERP/apps/core-api`                      |
| Prisma Schema    | `/home/admin/UniversityERP/apps/core-api/prisma/schema.prisma` |
| Admin Portal     | `/home/admin/UniversityERP/web/admin-portal`                   |
| Application Logs | `/var/log/university-erp/`                                     |
| Schema Sync SQL  | `/tmp/schema-sync.sql`                                         |

---

# 29. Main Services

| Service               | Management          |
| --------------------- | ------------------- |
| Core API              | PM2                 |
| Admin Portal          | PM2                 |
| PostgreSQL            | Docker              |
| Redis                 | Docker              |
| Elasticsearch         | Docker              |
| CBE Engine            | Docker              |
| Notification Worker   | Docker              |
| Certificate Generator | Docker              |
| Prisma Studio         | `npx prisma studio` |

---
