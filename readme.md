# IRCTC Mini Backend System (Django + DRF + MongoDB)

## Overview

This project is a simplified backend system inspired by IRCTC.
It supports user authentication, train search, ticket booking, and analytics on most searched routes.

The system demonstrates transactional consistency, concurrency control, and analytics logging using two different databases.

---

## Tech Stack

* Backend: Django + Django REST Framework
* Authentication: JWT (SimpleJWT)
* Relational Database: SQLite/MySQL (Transactional data)
* NoSQL Database: MongoDB (Search logs & analytics)

---

## Architecture

The system uses a dual-database architecture:

**Relational DB (Django ORM)**

* Users
* Trains
* Bookings

**MongoDB**

* Search logs
* Route analytics

Reason:
Transactional data requires ACID guarantees, while logging data requires high write throughput and aggregation queries.

---

## Features

### Authentication

* Register user
* Login user
* JWT based authentication
* Role based permissions (Admin/User)

### Train System

* Admin can create trains
* Users can search trains
* Every search logged in MongoDB

### Booking System

* Atomic seat booking
* Prevents race condition using row-level locking
* Users can view their bookings

### Analytics

* Top 5 most searched routes
* Implemented using MongoDB aggregation pipeline

---

## Concurrency Handling

Seat booking uses:
`select_for_update()` inside `transaction.atomic()`

This locks the train row during booking and prevents overbooking when multiple users attempt booking simultaneously.

---

## Setup Instructions

### 1. Clone repository

```
git clone <repo_url>
cd irctc_backend
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment

Create `.env` file from template:

```
cp .env.example .env
```

### 5. Run migrations

```
python manage.py migrate
```

### 6. Create admin

```
python manage.py createsuperuser
```

### 7. Run server

```
python manage.py runserver
```

---

## API Endpoints

### Authentication

* `POST /api/auth/register/`
* `POST /api/auth/login/`

### Trains

* `POST /api/trains/` (Admin)
* `GET /api/trains/search/?source=&destination=`

### Bookings

* `POST /api/bookings/`
* `GET /api/bookings/my/`

### Analytics

* `GET /api/analytics/top-routes/` (Admin)

---

## Key Concepts Demonstrated

* JWT Authentication
* Role based authorization
* Transaction management
* Row-level database locking
* Race condition prevention
* NoSQL analytics logging
* Aggregation queries
