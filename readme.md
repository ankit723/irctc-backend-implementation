# IRCTC Mini Backend System (Django + DRF + MongoDB)

## Overview

This project is a simplified railway booking backend inspired by IRCTC.
It demonstrates authentication, train search, ticket booking, concurrency-safe seat reservation, and analytics using a dual database architecture.

The backend exposes REST APIs secured using JWT authentication and role-based permissions.

---

## Tech Stack

* Backend: Django + Django REST Framework
* Authentication: JWT (SimpleJWT)
* Relational Database: SQLite/MySQL (transactional data)
* NoSQL Database: MongoDB (search logs & analytics)

---

## System Architecture

### Relational Database (Django ORM)

Used for transactional data:

* Users
* Trains
* Bookings (tickets)

### MongoDB

Used for non-transactional high-volume data:

* Train search logs
* Route popularity analytics

Reason:
Transactional operations require ACID guarantees, while logging requires high write throughput and aggregation queries.

---

## Features

### Authentication

* User registration
* User login
* JWT token generation
* Role based access control (Admin/User)

### Train Management

* Admin users can create and update trains via API
* Users can search trains
* Every search request is logged in MongoDB

### Booking System

* Atomic seat reservation
* Prevents overbooking using database row-level locking
* Users can view their booking history

### Analytics

* Top 5 most searched routes
* Implemented using MongoDB aggregation pipeline

---

## ⚠️ Important: Admin Account Required

Train creation and analytics endpoints are **admin-protected APIs**.

Before testing the project, the reviewer must create a super admin account from the terminal.

The admin account is required to:

* Create trains
* Update trains
* Access analytics endpoints

Regular users created via `/api/auth/register/` **cannot** perform these actions.

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repo_url>
cd irctc_backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

Then open `.env` and ensure:

```
SECRET_KEY=django-insecure-irctc-project-secret
DEBUG=True
MONGO_URI=mongodb://localhost:27017/
```

### 5. Run Migrations

```bash
python manage.py migrate
```

---

## 6. Create Super Admin (MANDATORY STEP)

This step is required to access train creation APIs.

```bash
python manage.py createsuperuser
```

You will be prompted:

```
Email:
Name:
Password:
```

After this, the admin user can:

* Login via API
* Obtain JWT token
* Create trains

---

## 7. Run Server

```bash
python manage.py runserver
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## How to Obtain Admin Token

Login using the admin credentials created above:

**Endpoint**

```
POST /api/auth/login/
```

**Body**

```json
{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

The response will contain:

```
access token
refresh token
```

Use the `access` token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## API Endpoints

### Authentication

* `POST /api/auth/register/`
* `POST /api/auth/login/`

### Train APIs

* `POST /api/trains/` (Admin only)
* `GET /api/trains/search/?source=&destination=`

### Booking APIs

* `POST /api/bookings/`
* `GET /api/bookings/my/`

### Analytics APIs

* `GET /api/analytics/top-routes/` (Admin only)

---

## Concurrency Handling

Seat booking is protected using:

`transaction.atomic()` + `select_for_update()`

This locks the train record during booking so only one request can modify seat availability at a time, preventing overbooking when multiple users book simultaneously.

---

## Key Backend Concepts Demonstrated

* JWT authentication
* Role based authorization (RBAC)
* Transaction management
* Row-level locking
* Race condition prevention
* Dual database architecture
* MongoDB aggregation analytics
