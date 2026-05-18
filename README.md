# ClassNest Backend

A modern, scalable FastAPI-based backend for ClassNest, an online tutoring and course management platform. This API handles user authentication, tutoring services, course management, scheduling, and more.

## 🎯 Features

- **User Authentication & Authorization**: Secure JWT-based authentication with OTP verification
- **Tutor Management**: Profile management, availability scheduling, and course offerings
- **Course & Class Management**: Create, manage, and organize courses and classes
- **Student & Parent Accounts**: Support for multiple user roles with hierarchical relationships
- **Favorites System**: Students can save and manage favorite tutors
- **Cart & Booking Management**: Shopping cart and class booking functionality
- **Calendar & Scheduling**: Advanced scheduling with calendar integration
- **School Management**: Multi-school support with organizational structure
- **Email Notifications**: SendGrid integration for email communications
- **AWS S3 Integration**: Support for file uploads and storage
- **Comprehensive Logging**: Structured logging with context tracking
- **Async Processing**: Fast, non-blocking operations with asyncio
- **Database Migrations**: Alembic-based schema versioning

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **Database**: PostgreSQL with async support via `asyncpg`
- **ORM**: SQLAlchemy 2.0+ (async)
- **Migrations**: Alembic
- **Authentication**: JWT + Python-Jose
- **Email**: SendGrid
- **Cloud Storage**: AWS S3
- **Testing**: pytest with pytest-asyncio
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Docker & Docker Compose (optional, for containerized deployment)
- AWS credentials (for S3 integration)
- SendGrid API key (for email functionality)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/shripalm/ClassNest.git
cd backend-classnest
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/classnest

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
SENDGRID_API_KEY=your-sendgrid-api-key

# AWS Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=your-aws-region
AWS_S3_BUCKET_NAME=your-bucket-name

# Application Settings
PROJECT_NAME=ClassNest
STAGE=development
DEBUG=True
```

### 5. Database Setup

Initialize the database and run migrations:

```bash
# Check migration status
alembic current

# Run all pending migrations
alembic upgrade head

# Create a new migration (after modifying models)
alembic revision --autogenerate -m "description of changes"
```

### 6. Run the Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the app directly
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

**Interactive API Documentation**: `http://localhost:8000/docs` (Swagger UI)

## 🐳 Docker Setup

### Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app
```

The application will be accessible at `http://localhost:8000`

## 📁 Project Structure

```
backend-classnest/
├── alembic/                    # Database migrations
│   ├── versions/               # Migration scripts
│   ├── env.py                  # Migration environment config
│   └── script.py.mako          # Migration template
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routers/        # API endpoint routers
│   ├── core/
│   │   ├── config.py           # Application configuration
│   │   ├── security.py         # JWT & authentication logic
│   │   └── logging_config.py   # Logging setup
│   ├── db/
│   │   ├── session.py          # Database session management
│   │   ├── base_class.py       # Base model class
│   │   └── listeners.py        # SQLAlchemy event listeners
│   ├── models/                 # SQLAlchemy ORM models
│   ├── schemas/                # Pydantic request/response schemas
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic layer
│   ├── middleware/             # FastAPI middleware
│   ├── enums/                  # Enum definitions
│   ├── utils/                  # Utility functions
│   ├── static/                 # Static files
│   └── main.py                 # Application entry point
├── tests/                      # Test suite
│   ├── conftest.py             # pytest fixtures and configuration
│   └── test_*.py               # Test modules
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image configuration
├── alembic.ini                 # Alembic configuration
├── pytest.ini                  # pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/verify-otp` - Verify OTP
- `POST /api/v1/auth/request-otp` - Request OTP

### Tutors
- `GET /api/v1/tutors` - List all tutors
- `GET /api/v1/tutors/{tutor_id}` - Get tutor details
- `POST /api/v1/tutors` - Create new tutor profile
- `PUT /api/v1/tutors/{tutor_id}` - Update tutor profile

### Courses
- `GET /api/v1/courses` - List all courses
- `POST /api/v1/courses` - Create new course
- `GET /api/v1/courses/{course_id}` - Get course details

### Classes
- `GET /api/v1/classes` - List all classes
- `POST /api/v1/classes` - Create new class
- `GET /api/v1/classes/{class_id}` - Get class details

### Favorites
- `GET /api/v1/favorites` - Get user's favorite tutors
- `POST /api/v1/favorites` - Add tutor to favorites
- `DELETE /api/v1/favorites/{tutor_id}` - Remove from favorites

### Scheduling
- `GET /api/v1/schedule` - Get schedule
- `POST /api/v1/schedule` - Create schedule entry
- `GET /api/v1/calendar` - Get calendar events

### Cart
- `GET /api/v1/cart` - Get user's cart
- `POST /api/v1/cart` - Add item to cart
- `DELETE /api/v1/cart/{item_id}` - Remove from cart

### Health Check
- `GET /api/v1/health` - Application health status

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/

# Run with markers
pytest -m auth
```

### Test Configuration

Tests are configured in `pytest.ini`. See `tests/conftest.py` for fixtures and test setup.

## 📊 Database Migrations

### Create a Migration

After modifying models, create a new migration:

```bash
alembic revision --autogenerate -m "Add new_field to users table"
```

### View Migration Status

```bash
alembic current
alembic history --indicate-current
```

### Rollback Migrations

```bash
# Rollback one revision
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Rollback to beginning
alembic downgrade base
```

## 🔐 Environment Variables

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `SENDGRID_API_KEY` | SendGrid API key | Optional |
| `AWS_ACCESS_KEY_ID` | AWS access key | Optional |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Optional |
| `DEBUG` | Debug mode | False |

## 🔧 Development

### Code Style

The project follows PEP 8 guidelines. Format code with:

```bash
# Install formatting tools
pip install black flake8 isort

# Format code
black app/
isort app/

# Check style
flake8 app/
```

### Logging

The application uses structured logging with `structlog`. Check logs in the application output or configured log files.

## 🚢 Deployment

### Docker Deployment

```bash
# Build image
docker build -t classnest-backend:latest .

# Run container
docker run -p 8000:80 \
  -e DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/classnest \
  -e SECRET_KEY=your-secret-key \
  classnest-backend:latest
```

### Production Considerations

- Set `DEBUG=False` in production
- Use a strong `SECRET_KEY`
- Enable HTTPS/TLS
- Use environment-specific configuration
- Set up proper database backups
- Configure monitoring and alerts
- Use a production-grade ASGI server (e.g., Gunicorn with Uvicorn workers)

## 📝 API Documentation

Once the server is running, view:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open a Pull Request

Please ensure:
- All tests pass
- Code follows PEP 8 style guide
- New features include tests
- Documentation is updated

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
# Verify DATABASE_URL format: postgresql+asyncpg://user:password@host:port/database

# Check migrations are up to date
alembic current
alembic upgrade head
```

### Port Already in Use

```bash
# Change port
uvicorn app.main:app --port 8001
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: shripal.nextstep@gmail.com

---

**Made with ❤️ by the Shripal Mehta**
