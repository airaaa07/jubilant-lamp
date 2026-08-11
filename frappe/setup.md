# Frappe Framework – Setup and Application Creation

## Documentation

For official Frappe Framework documentation and Demo Apps, refer to:

[Frappe Framework Documentation](https://docs.frappe.io/framework/)
[Frappe Framework Demo Apps](https://buildwithhussain.com/)

---

## 1. Navigate to the Frappe Bench

Open your terminal and navigate to the `frappe-bench` directory:

```bash
cd frappe-bench
```

---

## 2. Start the Frappe Development Server

Run the following command:

```bash
bench start
```

This starts the Frappe development server.

---

## 3. Open Frappe in Your Browser

Once the server is running, open the following URL in your browser:

```text
http://<ServerIP>:8001
```

Replace `<ServerIP>` with the IP address of your server.

**Example:**

```text
http://192.168.1.100:8001
```

---

## 4. Log In

Use the following credentials to log in:

| Field        | Value           |
| ------------ | --------------- |
| **Username** | `Administrator` |
| **Password** | `root`          |

> **Note:** If this is a development environment, the default password may be `root`. For production environments, use a strong password and do not document or share credentials publicly.

---

## 5. Create a New Frappe App

To create a new application, run the following command from inside the `frappe-bench` directory:

```bash
bench new-app library_management
```

This command creates a new Frappe application named **Library Management**.

---

## Quick Reference

```bash
# Navigate to the Frappe Bench
cd frappe-bench

# Start the development server
bench start

# Create a new Frappe application
bench new-app library_management
```

### Access

```text
URL: http://<ServerIP>:8001
Username: Administrator
Password: root
```
