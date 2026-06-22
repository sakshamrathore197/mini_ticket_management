# Mini Support Ticket Management System

## 1. Project Name

Mini Support Ticket Management System

---

## 2. Short Project Description

The Mini Support Ticket Management System is a web-based application developed using FastAPI, SQLAlchemy, SQLite, HTML, CSS, and Jinja2 Templates. The system helps organizations manage client support requests efficiently by creating, assigning, tracking, updating, resolving, and closing support tickets.

The application provides ticket lifecycle management, employee assignment, status tracking, remark history, dashboard analytics, and login functionality for administrators and employees.

---

## 3. Features Implemented

### Dashboard

* Total Tickets Count
* Open Tickets Count
* In Progress Tickets Count
* Resolved Tickets Count
* Closed Tickets Count
* Critical Tickets Count
* Today's Tickets Count
* Latest Tickets Display

### Ticket Management

* Create New Ticket
* Auto Ticket Number Generation
* Ticket List View
* Ticket Detail View
* Ticket Assignment to Employee
* Ticket Status Update
* Ticket Resolution Workflow
* Ticket Closing Workflow

### Remarks & History

* Add Ticket Remarks
* View Remark History
* Track Status History
* Store Complete Ticket Activity

### Search & Filter

* Search by Ticket Number
* Search by Client Name
* Search by Mobile Number
* Search by Company Name
* Search by Issue Title
* Filter by Ticket Status

### Employee Management

* Add Employee
* Delete Employee
* Assign Tickets to Employees

### Authentication

* Admin Login
* Session-Based Authentication
* Logout Functionality

### Validations

* Required Field Validation
* Duplicate Active Ticket Check
* Closed Ticket Update Restriction
* Ticket Close Validation

---

## 4. Setup Instructions

### Step 1: Clone the Project

```bash
git clone <repository-url>
```

### Step 2: Navigate to Project Folder

```bash
cd support_ticket_system
```

### Step 3: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart itsdangerous
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

---

## 5. Run Instructions

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Open the application in browser:

```text
http://127.0.0.1:8000
```

---

## 6. Test Login Details

### Admin Login

Email:

```text
admin@gmail.com
```

Password:

```text
admin123
```

### Employee Login

Create employees through the Employee Management page and use the created credentials to log in.

---

## 7. Important Notes

* SQLite is used as the database.
* Ticket numbers are generated automatically in the format:

```text
QW-TKT-0001
QW-TKT-0002
QW-TKT-0003
```

* A ticket can only be closed after it has been resolved.
* Closing remarks are mandatory when closing a ticket.
* Duplicate active tickets are prevented using mobile number and issue title validation.
* Every ticket status change is stored in the Ticket History table.
* Every ticket remark is stored in the Ticket Remark History table.
* Employee assignment is handled during ticket creation.
* Session middleware is used for login management.
* If database structure changes, delete the existing SQLite database and restart the application to recreate tables.

---

## Technology Stack

* FastAPI
* SQLAlchemy
* SQLite
* HTML
* CSS
* Jinja2 Templates
* Uvicorn
* Starlette Session Middleware

---

## Developed Features Summary

✅ Dashboard Analytics

✅ Ticket Creation

✅ Ticket Assignment

✅ Ticket Tracking

✅ Ticket Status Updates

✅ Ticket Remarks

✅ Ticket History

✅ Ticket Closing Workflow

✅ Search & Filter

✅ Employee Management

✅ Login & Logout

✅ Session Management

✅ Responsive Navigation
