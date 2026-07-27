# Environment Configuration & Local ngrok Setup Guide

## E-commerce Ordering & Payment System

**Backend Engineer Technical Assessment**

---

# Repository

GitHub Repository

https://github.com/jim8489/ecommerce_backend

---

# 1. Overview

This guide explains how to configure and run the E-commerce Ordering & Payment System in a local development environment using Docker or a standard Python virtual environment.

The backend is developed with Django REST Framework and PostgreSQL. The system supports authentication, product management, order processing, and payment integrations with Stripe and bKash.

---

# 2. System Requirements

Before running the project, ensure the following software is installed.

## Required Software

* Git
* Python 3.11 or later
* PostgreSQL 16
* Docker Desktop
* Docker Compose
* Node.js 20+
* npm
* Visual Studio Code (recommended)

---

# 3. Clone the Repository

Clone the repository from GitHub.

```bash
git clone https://github.com/jim8489/ecommerce_backend.git
```

Move into the project directory.

```bash
cd ecomerce_backend
```

---

# 4. Backend Setup (Without Docker)

## Create Virtual Environment

macOS/Linux:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 5. Environment Variables

Create a file named:

```
.env
```

in the project root.

Example configuration:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DATABASE_NAME=ecommerce_backend
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432


# Stripe

STRIPE_SECRET_KEY=your_stripe_secret_key

STRIPE_PUBLISHABLE_KEY=your_publishable_key

STRIPE_WEBHOOK_SECRET=your_webhook_secret


# bKash Sandbox

BKASH_BASE_URL=https://tokenized.sandbox.bka.sh/v1.2.0-beta

BKASH_USERNAME=your_username

BKASH_PASSWORD=your_password

BKASH_APP_KEY=your_app_key

BKASH_APP_SECRET=your_app_secret

BKASH_CALLBACK_URL=your_callback_url
```

Sensitive credentials should never be committed to GitHub.

---

# 6. Database Migration

Generate migrations if required:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

---

# 7. Create Superuser

Create an administrator account:

```bash
python manage.py createsuperuser
```

Provide:

* Email
* Password

---

# 8. Load Sample Data

If seed scripts are available:

```bash
python manage.py seed_products
```

Alternatively, create sample products through Django Admin.

---

# 9. Run Development Server

Start Django:

```bash
python manage.py runserver
```

Backend:

```
http://127.0.0.1:8000/
```

---

# 10. Frontend Setup

Navigate to frontend directory:

```bash
cd ecommerce_frontend
```

Install dependencies:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

# 11. Docker Setup

Docker provides a consistent environment for PostgreSQL and Django services.

Build containers:

```bash
docker compose build
```

Start containers:

```bash
docker compose up
```

Rebuild after changes:

```bash
docker compose up --build
```

Stop containers:

```bash
docker compose down
```

---

# 12. Verify Docker

After successful startup:

Backend:

```
http://localhost:8000
```

Admin:

```
http://localhost:8000/admin/
```

Swagger:

```
http://localhost:8000/api/schema/swagger-ui/
```

---

# 13. Running Tests

Run all tests:

```bash
python manage.py test
```

Run specific application tests:

```bash
python manage.py test apps.payments.tests
```

Example:

```
Found tests
System check identified no issues

OK
```

---

# 14. API Documentation

The project uses **drf-spectacular** for OpenAPI documentation.

Swagger UI:

```
/api/schema/swagger-ui/
```

OpenAPI Schema:

```
/api/schema/
```

---

# 15. Project Structure

```text
Ecomerce_backend/

│
├── apps/
│   ├── accounts/
│   ├── products/
│   ├── orders/
│   ├── payments/
│   └── recommendations/
│
├── config/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── README.md
└── docs/
    └── SETUP_GUIDE.md
```

---

# 16. Local ngrok Setup (Stripe Webhook Testing)

## Overview

ngrok is used to expose the local Django server to the internet.

Stripe requires a public HTTPS endpoint to send webhook events. During local development, ngrok creates a secure tunnel between Stripe and the local Django application.

The request flow:

```
Stripe
   |
   |
Stripe CLI
   |
   |
ngrok Tunnel
   |
   |
Django Webhook Endpoint
```

---

# Install ngrok

Download ngrok:

```
https://ngrok.com/download
```

Verify installation:

```bash
ngrok version
```

---

# Authenticate ngrok

After creating an ngrok account, add your authentication token:

```bash
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
```

---

# Start Django Server

Run:

```bash
python manage.py runserver
```

Django will run:

```
http://127.0.0.1:8000
```

---

# Start ngrok Tunnel

Open another terminal:

```bash
ngrok http 8000
```

Example:

```
Forwarding

https://abcd-1234.ngrok-free.app
        |
        |
localhost:8000
```

The HTTPS URL can now receive external requests.

---

# Stripe CLI Setup

Install Stripe CLI:

```
https://stripe.com/docs/stripe-cli
```

Login:

```bash
stripe login
```

Start webhook forwarding:

```bash
stripe listen \
--forward-to localhost:8000/api/payments/stripe/webhook/
```

Example output:

```
Ready!

Your webhook signing secret is:

whsec_xxxxxxxxxxxxx
```

Add the secret to `.env`:

```env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

Restart Django after changing environment variables.

---

# Test Stripe Webhooks

Trigger a test payment event:

```bash
stripe trigger payment_intent.succeeded
```

Expected output:

```
payment_intent.succeeded

POST /api/payments/stripe/webhook/

200 OK
```

---

# 17. Troubleshooting

## Database Connection Error

Check:

* PostgreSQL is running
* Database name
* Username
* Password
* Port configuration

For Docker:

```bash
docker ps
```

Verify database container is running.

---

## Migration Errors

Run:

```bash
python manage.py migrate
```

If migrations are missing:

```bash
python manage.py makemigrations
```

---

## Stripe Webhook Errors

Verify:

* Stripe CLI is running
* Webhook URL is correct

```
localhost:8000/api/payments/stripe/webhook/
```

Check:

```
STRIPE_WEBHOOK_SECRET
```

inside `.env`.

---

## bKash Authentication Issues

Verify:

* Sandbox credentials
* API base URL
* Application key
* Application secret

Authentication failures usually indicate incorrect sandbox credentials or unavailable sandbox access.

---

# 18. Security Notes

* Never commit `.env` files.
* Never expose payment secrets publicly.
* Use separate credentials for development and production.
* Keep Stripe webhook secrets private.
* Keep ngrok authentication tokens private.

---

# 19. Conclusion

Following this guide will configure a complete local development environment for the E-commerce Ordering & Payment System.

The project supports:

* Local Python development
* Docker-based deployment
* PostgreSQL database setup
* Stripe webhook testing through ngrok
* Payment gateway configuration
* Automated API testing

This setup provides a consistent environment for development, testing, and demonstration.