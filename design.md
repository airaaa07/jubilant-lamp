```text
                    University ERP

               ┌──────────────────────┐
               │  React Admin Portal  │
               │  React + Vite + TS   │
               └──────────┬───────────┘
                          │
                       REST API
                          │
                          ▼
                ┌─────────────────────┐
                │      Core API       │
                │       NestJS        │
                └───────┬─────────────┘
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
 ┌────────────┐    ┌──────────┐    ┌─────────────┐
 │ PostgreSQL │    │  Redis   │    │    MinIO    │
 │ Prisma ORM │    │ Cache &  │    │Object Storage│
 └────────────┘    │  Queues  │    └─────────────┘
                   └────┬─────┘
                        │
                   Bull Queues
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
   Notification Worker   Certificate Generator
                        │
                        ▼
                 ┌──────────────┐
                 │  CBE Engine  │
                 │WebSocket Exams│
                 └──────────────┘

Optional Integrations
────────────────────────────────
• Elasticsearch
• Vault
• Azure Blob Storage
• SMTP
• SMS Gateway
```
