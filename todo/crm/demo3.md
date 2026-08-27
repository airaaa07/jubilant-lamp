flowchart TB

    %% ==============================
    %% PEOPLE
    %% ==============================

    USERS[University Users]

    PROSPECT[Prospects]
    APPLICANTS[Applicants]
    STUDENTS[Students]
    PARENTS[Parents]
    ALUMNI[Alumni]

    %% ==============================
    %% CHANNELS
    %% ==============================

    subgraph CHANNELS["Engagement Channels"]

        WEBSITE[Website]
        PORTAL[Portal]
        WHATSAPP[WhatsApp]
        SMS[SMS]
        EMAIL[Email]
        PHONE[Telephony]
        CHAT[Live Chat]

    end

    %% ==============================
    %% CRM
    %% ==============================

    subgraph CRM["University CRM / Engagement Platform"]

        AUTH[Authentication]
        RBAC[Roles & Permissions]

        PEOPLE[Person 360]
        RELATIONSHIP[Relationship Engine]

        LEAD[Lead Engine]
        ADMISSION[Admission Engine]

        ACTIVITY[Activity Engine]
        TASK[Task Engine]

        COMM[Communication Engine]
        CONVERSATION[Conversation Engine]

        CASE[Case Engine]
        SLA[SLA Engine]

        CAMPAIGN[Campaign Engine]
        SEGMENT[Segmentation Engine]

        WORKFLOW[Workflow Engine]
        JOURNEY[Journey Engine]

        NOTIFICATION[Notification Engine]

        KNOWLEDGE[Knowledge Base]

        AI[AI Engine]

        REPORTING[Reporting Engine]
        SEARCH[Search Engine]

        DOCUMENT[Document Engine]

        AUDIT[Audit Engine]

        INTEGRATION[ERP Integration Engine]

    end

    %% ==============================
    %% ERP
    %% ==============================

    subgraph ERP["Existing University ERP"]

        STUDENT_MASTER[Student Master]
        APPLICATIONS[Applications]
        FEES[Fees]
        ACADEMIC[Academic]
        ATTENDANCE[Attendance]
        EXAMS[Exams]
        HOSTEL[Hostel]
        LIBRARY[Library]
        HR[HR]

    end

    %% ==============================
    %% INFRA
    %% ==============================

    subgraph INFRA["Infrastructure"]

        DATABASE[(Database)]
        CACHE[(Cache)]
        QUEUE[(Job Queue)]
        STORAGE[(File Storage)]
        OBSERVABILITY[Logs / Monitoring]

    end

    %% ==============================
    %% USER ACCESS
    %% ==============================

    USERS --> AUTH
    AUTH --> RBAC

    PROSPECT --> WEBSITE
    PROSPECT --> WHATSAPP
    PROSPECT --> PHONE

    APPLICANTS --> PORTAL
    STUDENTS --> PORTAL
    PARENTS --> WHATSAPP
    ALUMNI --> EMAIL

    %% ==============================
    %% CHANNELS
    %% ==============================

    WEBSITE --> LEAD
    PORTAL --> PEOPLE
    WHATSAPP --> COMM
    SMS --> COMM
    EMAIL --> COMM
    PHONE --> COMM
    CHAT --> COMM

    %% ==============================
    %% CRM CORE
    %% ==============================

    PEOPLE --> RELATIONSHIP

    LEAD --> PEOPLE
    LEAD --> ADMISSION

    ADMISSION --> PEOPLE

    PEOPLE --> ACTIVITY
    PEOPLE --> TASK
    PEOPLE --> CASE

    COMM --> CONVERSATION
    CONVERSATION --> ACTIVITY

    CASE --> SLA

    CAMPAIGN --> SEGMENT
    CAMPAIGN --> COMM

    WORKFLOW --> LEAD
    WORKFLOW --> TASK
    WORKFLOW --> COMM
    WORKFLOW --> CASE
    WORKFLOW --> NOTIFICATION
    WORKFLOW --> INTEGRATION

    JOURNEY --> WORKFLOW

    AI --> PEOPLE
    AI --> CASE
    AI --> COMM
    AI --> KNOWLEDGE
    AI --> SEARCH

    REPORTING --> PEOPLE
    REPORTING --> LEAD
    REPORTING --> CASE
    REPORTING --> CAMPAIGN
    REPORTING --> ACTIVITY

    SEARCH --> PEOPLE
    SEARCH --> LEAD
    SEARCH --> CASE

    %% ==============================
    %% ERP INTEGRATION
    %% ==============================

    INTEGRATION <--> STUDENT_MASTER
    INTEGRATION <--> APPLICATIONS
    INTEGRATION <--> FEES
    INTEGRATION <--> ACADEMIC
    INTEGRATION <--> ATTENDANCE
    INTEGRATION <--> EXAMS
    INTEGRATION <--> HOSTEL
    INTEGRATION <--> LIBRARY
    INTEGRATION <--> HR

    %% ==============================
    %% INFRASTRUCTURE
    %% ==============================

    PEOPLE --> DATABASE
    LEAD --> DATABASE
    ADMISSION --> DATABASE
    ACTIVITY --> DATABASE
    TASK --> DATABASE
    CASE --> DATABASE
    CAMPAIGN --> DATABASE
    WORKFLOW --> DATABASE
    JOURNEY --> DATABASE

    COMM --> QUEUE
    WORKFLOW --> QUEUE
    INTEGRATION --> QUEUE
    AI --> QUEUE

    DOCUMENT --> STORAGE

    COMM --> OBSERVABILITY
    WORKFLOW --> OBSERVABILITY
    INTEGRATION --> OBSERVABILITY
    AI --> OBSERVABILITY

    %% ==============================
    %% AUTOMATED STUDENT LIFECYCLE
    %% ==============================

    STUDENT_MASTER -->|Events| WORKFLOW
    FEES -->|Fee Events| WORKFLOW
    ATTENDANCE -->|Engagement Events| WORKFLOW
    APPLICATIONS -->|Application Events| WORKFLOW

    WORKFLOW -->|Actions| COMM
    WORKFLOW -->|Actions| TASK
    WORKFLOW -->|Actions| CASE
    WORKFLOW -->|Actions| NOTIFICATION
