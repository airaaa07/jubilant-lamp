```mermaid
flowchart LR

    INQUIRY[Website / Walk-in / Campaign / Phone]
    LEAD[Create Lead]
    DEDUPE[Check Existing Person]
    ASSIGN[Assign Counselor]
    CONTACT[First Contact]
    QUALIFY[Qualify Lead]

    APPSTART[Application Started]
    APPSUBMIT[Application Submitted]
    DOCS[Document Verification]
    TEST[Entrance Test]
    INTERVIEW[Interview]
    OFFER[Offer]
    PAYMENT[Fee Payment]
    ENROLLED[Enrolled]

    INQUIRY --> LEAD
    LEAD --> DEDUPE
    DEDUPE --> ASSIGN
    ASSIGN --> CONTACT
    CONTACT --> QUALIFY

    QUALIFY --> APPSTART
    APPSTART --> APPSUBMIT
    APPSUBMIT --> DOCS
    DOCS --> TEST
    TEST --> INTERVIEW
    INTERVIEW --> OFFER
    OFFER --> PAYMENT
    PAYMENT --> ENROLLED

    PAYMENT <--> ERP[ERP]

    QUALIFY -.-> LOST[Lost]
    ```
    DOCS -.-> REJECTED[Rejected]
    OFFER -.-> DECLINED[Declined]
