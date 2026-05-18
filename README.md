# classnest

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0%2B-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-316192?style=for-the-badge&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-orange?style=for-the-badge&logo=sqlalchemy)
![Docker](https://img.shields.io/badge/Docker-20.10%2B-2496ED?style=for-the-badge&logo=docker)

## Overview

`classnest` is a robust backend API built with FastAPI, designed to power an educational platform. It provides comprehensive functionalities for managing classes, courses, tutors, schools, user authentication, scheduling, and more. The project leverages modern asynchronous Python capabilities with SQLAlchemy 2.0 for database interactions, ensuring high performance and scalability.

This repository contains the core API logic, database models, and business services necessary for a dynamic learning environment.

## Features

*   **User Authentication & Authorization**: Secure user management with JWT, password hashing (bcrypt), and OTP verification.
*   **Class & Course Management**: APIs for creating, retrieving, updating, and deleting classes and courses.
*   **Tutor & School Profiles**: Dedicated endpoints for managing tutor and school information.
*   **Scheduling & Calendar**: Functionality for managing schedules, bookings, and calendar events.
*   **Shopping Cart**: API for handling user's cart items, likely for course enrollment.
*   **Favorites**: Users can mark favorite tutors or classes.
*   **Database ORM**: Asynchronous database operations using SQLAlchemy 2.0 with `asyncpg`.
*   **Data Validation**: Robust data validation and serialization with Pydantic 2.0.
*   **Email Services**: Integration with SendGrid for sending transactional emails (e.g., OTPs).
*   **Configuration Management**: Environment-specific settings handled via `python-dotenv` and Pydantic Settings.
*   **Health Monitoring**: Dedicated health check endpoint.

## Tech Stack

*   **Language**: Python 3.9+
*   **Web Framework**: FastAPI
*   **ASGI Server**: Uvicorn
*   **Database**: PostgreSQL (via `asyncpg` and `psycopg2`)
*   **ORM**: SQLAlchemy 2.0
*   **Migrations**: Alembic
*   **Data Validation**: Pydantic 2.0
*   **Authentication**: PyJWT, Passlib (bcrypt), python-jose
*   **Email**: SendGrid, `email-validator`
*   **HTTP Client**: httpx, requests
*   **Logging**: structlog
*   **Testing**: pytest, pytest-asyncio
*   **Containerization**: Docker, Docker Compose
*   **Cloud Integration**: boto3 (for AWS services, e.g., S3 for uploads)
*   **Data Processing**: pandas, numpy, scipy (potential for analytics or data manipulation)

## Installation

To get `classnest` up and running locally, follow these steps:

### Prerequisites

*   Python 3.9+
*   Poetry (recommended for dependency management) or pip
*   Docker & Docker Compose (for database setup)

### 1. Clone the repository

```bash
git clone https://github.com/shripalm/classnest.git
cd classnest
```

### 2. Set up Environment Variables

Create a `.env` file in the project root based on `.env.example` and fill in the required values.

```bash
cp .env.example .env
# Open .env and configure your settings
```

### 3. Database Setup (with Docker Compose)

Start the PostgreSQL database using Docker Compose:

```bash
docker-compose up -d db
```

### 4. Install Dependencies

Using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

Once the database is running, apply migrations using Alembic:

```bash
alembic upgrade head
```

### 6. Start the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be accessible at `http://localhost:8000`. The interactive API documentation (Swagger UI) will be available at `http://localhost:8000/docs`.

## Environment Variables

The application relies on several environment variables for configuration. A `.env.example` file is provided for reference.

| Variable                      | Description                                                               |
| :---------------------------- | :------------------------------------------------------------------------ |
| `PROJECT_NAME`                | Name of the project.                                                      |
| `APP_ENV`                     | Application environment (e.g., `development`, `production`).              |
| `APP_HOST`                    | Host for the application.                                                 |
| `APP_PORT`                    | Port for the application.                                                 |
| `STAGE_PATH`                  | Base path for API staging (if applicable).                                |
| `DB_URL`                      | PostgreSQL database connection URL (e.g., `postgresql+asyncpg://user:pass@host:port/db`). |
| `DB_POOL_SIZE`                | SQLAlchemy connection pool size.                                          |
| `DB_MAX_OVERFLOW`             | SQLAlchemy max overflow connections.                                      |
| `DB_POOL_TIMEOUT`             | SQLAlchemy pool timeout.                                                  |
| `DB_POOL_RECYCLE`             | SQLAlchemy pool recycle time.                                             |
| `SECRET_KEY`                  | Secret key for JWT token signing. **CRITICAL for security.**              |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiration time for access tokens in minutes.                             |
| `LOG_LVL`                     | Logging level (e.g., `INFO`, `DEBUG`).                                    |
| `SMTP_HOST`                   | SMTP server host for email.                                               |
| `SMTP_PORT`                   | SMTP server port.                                                         |
| `SMTP_USER`                   | SMTP username.                                                            |
| `SMTP_PASSWORD`               | SMTP password.                                                            |
| `SMTP_FROM_EMAIL`             | Email address for sending emails.                                         |
| `SMTP_FROM_NAME`              | Name associated with the sender email.                                    |
| `SENDGRID_API_KEY`            | SendGrid API key for transactional emails.                                |
| `SENDGRID_FROM_EMAIL`         | SendGrid sender email address.                                            |
| `SENDGRID_FROM_NAME`          | SendGrid sender name.                                                     |
| `OTP_EXPIRE_MINUTES`          | Expiration time for One-Time Passwords in minutes.                        |
| `OTP_LENGTH`                  | Length of generated One-Time Passwords.                                   |

## API Endpoints

The API exposes a set of endpoints under the `/api/v1` prefix. Detailed documentation can be found at `/docs` or `/redoc` when the application is running.

```
/api/v1/auth
/api/v1/calendar
/api/v1/cart
/api/v1/dev_settings
/api/v1/routers/auth
/api/v1/routers/calendar
/api/v1/routers/cart
/api/v1/routers/classes
/api/v1/routers/courses
/api/v1/routers/dev_settings
/api/v1/routers/favorites
/api/v1/routers/health
/api/v1/routers/schedule
/api/v1/routers/schools
/api/v1/routers/subjects
/api/v1/routers/tutors
/api/v1/schedule
```

## Folder Structure

The project follows a modular structure to ensure maintainability and scalability:

```
.
├── .env.example             # Example environment variables
├── Dockerfile               # Docker build instructions
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
└── app/
    ├── __init__.py
    ├── main.py              # FastAPI application entry point
    ├── api/                 # API versioning
    │   └── v1/
    │       └── routers/     # API endpoint definitions
    │           ├── auth.py
    │           ├── calendar.py
    │           ├── cart.py
    │           ├── classes.py
    │           ├── courses.py
    │           ├── dev_settings.py
    │           ├── favorites.py
    │           ├── health.py
    │           ├── schedule.py
    │           ├── schools.py
    │           ├── subjects.py
    │           └── tutors.py
    ├── core/                # Core application configurations and utilities
    │   ├── config.py        # Pydantic settings management
    │   ├── logging_config.py
    │   └── security.py      # JWT, password hashing utilities
    ├── db/                  # Database related files
    │   ├── session.py       # Database session management
    │   ├── base_class.py    # Base class for SQLAlchemy models
    │   └── listeners.py
    ├── enums/               # Enumerations
    │   └── user_enum.py
    ├── middleware/          # FastAPI middleware
    │   ├── client_middleware.py
    │   └── logging_middleware.py
    ├── models/              # SQLAlchemy ORM models
    │   ├── user.py
    │   ├── tutor.py
    │   ├── school.py
    │   ├── course_model.py
    │   ├── classes.py
    │   ├── schedule.py
    │   ├── calendar.py
    │   ├── cart.py
    │   ├── otp.py
    │   ├── child.py
    │   ├── favorite_tutor.py
    │   └── subject_model.py
    ├── repositories/        # Database interaction logic (CRUD operations)
    │   ├── user_repository.py
    │   ├── tutor_repository.py
    │   ├── school_repository.py
    │   ├── course_repository.py
    │   ├── class_repository.py
    │   ├── schedule_repository.py
    │   ├── calendar_repository.py
    │   ├── cart_repository.py
    │   ├── otp_repository.py
    │   ├── child_repository.py
    │   ├── favorite_tutor_repository.py
    │   └── subject_repository.py
    ├── schemas/             # Pydantic models for request/response validation
    │   ├── auth_schema.py
    │   ├── user_schema.py
    │   ├── tutor_schema.py
    │   ├── school_schema.py
    │   ├── course_schema.py
    │   ├── class_schema.py
    │   ├── schedule_schema.py
    │   ├── calendar_schema.py
    │   ├── cart_schema.py
    │   ├── favorite_tutor_schema.py
    │   ├── subject_schema.py
    │   └── response.py      # Generic response schemas
    ├── services/            # Business logic and service layer
    │   ├── auth_service.py
    │   └── upload.py        # File upload service (e.g., to S3)
    └── utils/               # Utility functions
        ├── exception_handlers.py
        ├── logging.py
        ├── pagination.py
        └── response.py
```

## Scripts

Currently, there are no custom shell scripts defined in the metadata. Standard Python commands for running the application, managing dependencies, and performing database migrations are used.

*   **Run application**: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
*   **Run migrations**: `alembic upgrade head`
*   **Generate new migration**: `alembic revision --autogenerate -m "Description of migration"`
*   **Run tests**: `pytest`

## Deployment

The project includes a `Dockerfile` for containerizing the application and a `docker-compose.yml` for orchestrating the application with its database.

To build and run the application using Docker Compose:

```bash
docker-compose up --build
```

This will build the `classnest` service image, start the PostgreSQL database, and run the FastAPI application.

## Future Improvements

*   **Real-time Features**: Integrate WebSockets for real-time notifications (e.g., new messages, schedule updates).
*   **Advanced Search & Filtering**: Implement more sophisticated search capabilities for classes, courses, and tutors.
*   **Payment Gateway Integration**: Add support for payment processing for course enrollments.
*   **Admin Panel**: Develop an administrative interface for managing platform content and users.
*   **Caching**: Implement caching strategies (e.g., Redis) to improve API response times for frequently accessed data.
*   **CI/CD Pipeline**: Set up continuous integration and deployment for automated testing and deployment.
*   **Observability**: Enhance monitoring, logging, and tracing for production environments.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (if available).