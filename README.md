# README.md

# E-commerce Ordering & Payment System

A scalable **E-commerce Ordering & Payment System** developed with **Django REST Framework** and **React**, supporting secure authentication, product management, order processing, and multiple payment providers through the **Strategy Design Pattern**.

This project was developed as part of a **Backend Engineer Technical Assessment**, focusing on clean software architecture, extensibility, RESTful API design, deterministic business logic, and production-ready development practices.

---

# Repository

**GitHub Repository**

https://github.com/jim8489/ecommerce_backend

---

# Project Overview

The application allows customers to browse products, place orders, and complete payments using different payment providers while administrators manage products, categories, inventory, and customer orders.

The backend has been designed following Object-Oriented Programming principles and utilises the Strategy Design Pattern, allowing new payment gateways to be integrated without modifying existing business logic.

---

# Features

## Authentication

* User Registration
* JWT Login Authentication
* Refresh Tokens
* Protected APIs
* Custom User Model
* Email-based Authentication

---

## Product Management

* Product CRUD
* Category CRUD
* SKU Validation
* Product Search
* Product Filtering
* Product Ordering
* Pagination
* Product Status (Active / Inactive)

---

## Category Management

* Hierarchical Categories
* Parent–Child Relationships
* DFS Category Traversal
* Cached Category Tree

---

## Shopping

* Shopping Cart
* Order Creation
* Multiple Order Items
* Automatic Total Calculation

---

## Payment System

### Stripe

* Payment Intent Creation
* Payment Confirmation
* Stripe Webhooks
* Secure Secret Key Storage

### bKash

* Tokenized Checkout integration architecture
* Payment initiation flow
* Payment verification flow
* Callback handling structure
* Strategy-based payment provider implementation

---

## Recommendation System

Implemented using:

* Depth First Search (DFS)
* Cached Category Tree
* Hierarchical Category Traversal

---

## Security

* JWT Authentication
* Role-based Authorization
* Environment Variables
* Payment Verification
* Validation
* Secure API Design

---

# Technology Stack

## Backend

* Python 3.11
* Django
* Django REST Framework
* PostgreSQL
* SimpleJWT
* drf-spectacular (Swagger)
* Stripe SDK
* Requests

---

## Frontend

* React
* Vite
* Axios
* React Router

---

## Database

* PostgreSQL

---

## Deployment

* Docker
* Docker Compose
* ngrok
* Vercel

---

# System Architecture

```text
React Frontend
        │
        ▼
JWT Authentication
        │
        ▼
Django REST API
        │
        ▼
Business Services
        │
 ┌──────────────┐
 │PaymentFactory│
 └──────────────┘
      │      │
      ▼      ▼
 Stripe   bKash
      │      │
      └──┬───┘
         ▼
 PostgreSQL
```

---

# Database Design

The system consists of the following relational entities.

* Users
* Categories
* Products
* Orders
* Order Items
* Payments

Each table contains indexed fields for efficient querying and follows proper foreign key relationships.

---

# Design Patterns

## Strategy Pattern

The payment module follows the Strategy Pattern.

```
PaymentStrategy

        ▲

 ┌──────────────┐
 │              │
StripeStrategy  BkashStrategy
        ▲
        │
PaymentFactory
        ▲
        │
PaymentService
```

Advantages

* Open/Closed Principle
* Easily add PayPal
* Easily add SSLCommerz
* No modification of Order Logic

---

# Algorithms

## Order Management

Deterministic algorithms are used for:

* Subtotal Calculation
* Order Total Calculation
* Inventory Reduction

---

## Product Recommendation

Depth First Search (DFS)

The recommendation engine traverses the category hierarchy using DFS and caches the category tree to minimise database access.

---

# Caching

Current implementation uses

```
LocMemCache
```

The architecture can be upgraded to

* Redis
* Memcached

without changing the recommendation logic.

---

# REST APIs

## Authentication

```
POST /api/auth/register/

POST /api/auth/login/

POST /api/auth/token/refresh/
```

---

## Products

```
GET /api/products/

GET /api/products/{id}/

POST /api/products/

PUT /api/products/{id}/

DELETE /api/products/{id}/
```

---

## Categories

```
GET /api/categories/

POST /api/categories/
```

---

## Orders

```
GET /api/orders/

POST /api/orders/

GET /api/orders/{id}/
```

---

## Payments

```
POST /api/payments/initiate/

POST /api/payments/confirm/

POST /api/payments/stripe/webhook/

GET /api/payments/
```

---

## Recommendations

```
GET /api/recommendations/{category_id}/
```

---

# Payment Flow

## Stripe

```
Frontend

↓

Backend

↓

Create Payment Intent

↓

Stripe Checkout

↓

Webhook

↓

Payment Verification

↓

Order Paid

↓

Reduce Stock
```

---

## bKash

```
Frontend

↓

Backend

↓

Token

↓

Checkout

↓

Execute

↓

Query

↓

Callback

↓

Order Paid

↓

Reduce Stock
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

Stop

```bash
docker compose down
```

---

# Running Locally

## Backend

```bash
git clone https://github.com/jim8489/ecommerce_backend.git

cd ecommerce_backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Example

```env
SECRET_KEY=

DEBUG=True

DATABASE_URL=

STRIPE_SECRET_KEY=

STRIPE_PUBLISHABLE_KEY=

STRIPE_WEBHOOK_SECRET=

BKASH_BASE_URL=

BKASH_USERNAME=

BKASH_PASSWORD=

BKASH_APP_KEY=

BKASH_APP_SECRET=
```

---

# Swagger API Documentation

Generate interactive documentation

```
/api/schema/swagger-ui/
```

OpenAPI Schema

```
/api/schema/
```

---

# Testing

Run all tests

```bash
python manage.py test
```

Run a specific app

```bash
python manage.py test apps.payments.tests
```

---

# Logging

Application logging is configured using Django's logging framework.

Logs include

* Payment initiation
* Payment confirmation
* Inventory updates
* Webhook processing
* Validation failures

---

# Project Structure

```
backend/

apps/

accounts/

products/

orders/

payments/

recommendations/

config/

frontend/

src/

README.md

Dockerfile

docker-compose.yml
```

---

# Future Improvements

* Redis Cache
* Celery Background Tasks
* Email Notifications
* Product Reviews
* Wishlist
* Coupons
* Inventory Alerts
* Multi-language Support
* PayPal Integration
* SSLCommerz Integration

---

# Assessment Requirements Covered

| Requirement              | Status                         |
| ------------------------ | ------------------------------ |
| User Management          | ✅                              |
| Product Management       | ✅                              |
| Order Management         | ✅                              |
| Stripe Integration       | ✅                              |
| bKash Integration        | ✅ (Integration layer implemented)|
| Strategy Pattern         | ✅                              |
| OOP Design               | ✅                              |
| DFS Algorithm            | ✅                              |
| Category Caching         | ✅                              |
| Docker                   | ✅                              |
| Swagger                  | ✅                              |
| Unit Testing             | ✅                              |
| API Testing              | ✅                              |
| Logging & Error Handling | ✅                              |
| PostgreSQL               | ✅                              |

---

# Author

Developed by **Muntasir Maruf Bosunia**

Backend Engineer Technical Assessment

2026
