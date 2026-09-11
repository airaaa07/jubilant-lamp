# Module 06: Fees, Finance & Payments — End-to-End Action Processes

> **Scope**: Payment order initialization, cryptographic webhook signature verification, double-entry student fee ledger updates, demand generation, fee waiver workflows, and payment window configuration.

---

## Action 1: Save Payment Windows Configuration (`PUT /api/settings/payment-windows`)

Per commit `6f060a59`, Payment Windows configuration is a university-level setting exposed via the Fee Management gear modal.

- **HTTP Method & URL**: `PUT /api/settings/payment-windows`
- **Guards**: `JwtAuthGuard`, `RolesGuard('SuperAdmin', 'UnivAdmin')`
- **Request Body (DTO: `PaymentWindowsDto`)**:
  ```json
  {
    "applicationFeeHours": 48,
    "admissionFeeHours": 72
  }
  ```
- **Validation Pipeline**: `@IsInt()`, `@Min(1)`, `@Max(720)`.
- **Prisma Mutation**:
  ```prisma
  const university = await prisma.university.findUnique({
    where: { id: req.user.universityId }
  });

  const existingConfig = (university.config as any) || {};
  const updatedConfig = {
    ...existingConfig,
    paymentWindows: {
      applicationFeeHours: dto.applicationFeeHours,
      admissionFeeHours: dto.admissionFeeHours
    }
  };

  await prisma.university.update({
    where: { id: req.user.universityId },
    data: { config: updatedConfig }
  });
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "paymentWindows": {
      "applicationFeeHours": 48,
      "admissionFeeHours": 72
    }
  }
  ```

---

## Action 2: Online Payment Verification & Ledger Commit (`POST /api/fee/verify`)

```mermaid
sequenceDiagram
    autonumber
    Client->>FeeController: POST /api/fee/verify { orderId, paymentId, signature }
    FeeController->>FeeService: verifyAndCommitPayment(dto, user)
    FeeService->>Crypto: Verify HMAC-SHA256(orderId + "|" + paymentId, SECRET) == signature
    alt Signature invalid
        FeeService-->>FeeController: Throw UnauthorizedException("Tampered payment signature")
    else Signature authentic
        FeeService->>Prisma: $transaction [
            1. Query Payment record by gatewayOrderId
            2. Update Payment status to 'SUCCESS', record gatewayPaymentId
            3. Update FeeDemand status to 'PAID', balanceAmount to 0
            4. Insert FeeLedger record (Credit transaction)
            5. If application fee: advance RegistrationRequest status
            6. If admission fee: advance RegistrationRequest to 'ADMITTED'
        ]
        Prisma-->>FeeService: Committed
        FeeService->>NotificationWorker: emit("PAYMENT_RECEIPT_EMAIL", { paymentId })
        FeeService-->>FeeController: Success payload with receipt URL
        FeeController-->>Client: 200 OK
    end
```

### Protocol Specifications
- **HTTP Method & URL**: `POST /api/fee/verify`
- **Request Body**:
  ```json
  {
    "gatewayOrderId": "order_OqZ18x89k",
    "gatewayPaymentId": "pay_OqZ29y01k",
    "gatewaySignature": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  }
  ```
- **Prisma Database Mutation**:
  ```prisma
  await prisma.$transaction(async (tx) => {
    const payment = await tx.payment.findUnique({
      where: { gatewayOrderId: dto.gatewayOrderId }
    });

    await tx.payment.update({
      where: { id: payment.id },
      data: {
        status: "SUCCESS",
        gatewayPaymentId: dto.gatewayPaymentId,
        paidAt: new Date()
      }
    });

    await tx.feeDemand.update({
      where: { id: payment.feeDemandId },
      data: {
        status: "PAID",
        paidAmount: { increment: payment.amount },
        balanceAmount: 0
      }
    });

    await tx.feeLedger.create({
      data: {
        studentId: payment.studentId,
        entryType: "CREDIT",
        category: "PAYMENT_ONLINE",
        amount: payment.amount,
        referenceId: payment.id,
        remarks: `Online Payment via Razorpay (${dto.gatewayPaymentId})`
      }
    });
  });
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "receiptNumber": "REC-2026-00491",
    "amount": 45000,
    "currency": "INR"
  }
  ```
