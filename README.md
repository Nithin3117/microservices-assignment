# Microservices Assignment

A microservices-based backend application developed using **Python, FastAPI, Docker, Docker Compose, JWT Authentication, SQLAlchemy, SQLite, and NATS**.

The system contains two backend services and an API Gateway. The User Service communicates asynchronously with the Notification Service using NATS.

---

## 1. Project Overview

This project demonstrates a simple microservices architecture with:

- **API Gateway**
- **User Service**
- **Notification Service**
- **NATS message broker**
- **JWT-based authentication**
- **Docker and Docker Compose**
- **SQLite databases**
- **REST APIs**
- **Asynchronous event-driven communication**

### Main Workflow

When a new user registers:

```text
Client
   |
   v
API Gateway
   |
   v
User Service
   |
   | user.created event
   v
NATS
   |
   v
Notification Service
   |
   v
Welcome Notification
```

The User Service and Notification Service communicate through **NATS**, rather than directly communicating through REST APIs.

---

# 2. System Architecture

The system contains the following components:

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                                  │ HTTP
                                  ▼
                         ┌──────────────────┐
                         │   API Gateway    │
                         │    Port 8000      │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    │ HTTP                      │ HTTP
                    ▼                           ▼
          ┌──────────────────┐       ┌──────────────────────┐
          │   User Service   │       │ Notification Service │
          │    Port 8001     │       │      Port 8002       │
          └────────┬─────────┘       └──────────▲───────────┘
                   │                            │
                   │ user.created               │
                   ▼                            │
             ┌───────────┐                      │
             │   NATS    │──────────────────────┘
             │  Port4222 │
             └───────────┘
```

``
# 3. Services

## API Gateway

**Port:** `8000`

The API Gateway acts as the single entry point for clients.

Responsibilities:

- Receives client requests
- Routes requests to backend services
- Forwards request headers and query parameters
- Handles downstream service errors
- Provides a central API entry point

---

## User Service

**Port:** `8001`

Responsibilities:

- User registration
- User login
- JWT authentication
- Protected user profile endpoint
- User database management
- Publishing `user.created` events through NATS

Main endpoints:

```text
POST /users/register
POST /users/login
GET  /users/me
```

---

## Notification Service

**Port:** `8002`

Responsibilities:

- Subscribe to `user.created` events
- Create welcome notifications
- Store notifications
- Return notification records through the API

Main endpoint:

```text
GET /notifications
```

---

## NATS

**Port:** `4222`

NATS is used as the asynchronous message broker.

The main event is:

```text
user.created
```

The User Service publishes this event after successful user registration.

The Notification Service subscribes to this event and creates a welcome notification.

---

# 4. Event-Driven Communication

The User Service and Notification Service communicate asynchronously through NATS.

### Event Flow

```text
1. User registers
        |
        v
2. User Service creates user
        |
        v
3. User Service publishes "user.created"
        |
        v
4. NATS receives event
        |
        v
5. Notification Service receives event
        |
        v
6. Welcome notification is created
```

Example event:

```json
{
  "event": "user.created",
  "user_id": 3,
  "name": "Final Test",
  "email": "finaltest2026@test.com"
}
```

Example notification:

```text
Welcome Final Test! Your account has been created.
```

---

# 5. Authentication

The User Service uses **JWT authentication**.

### Login

The user sends valid credentials to:

```text
POST /api/users/login
```

The service returns an access token.

The token is then sent using:

```text
Authorization: Bearer <JWT_TOKEN>
```

### Protected Endpoint

```text
GET /api/users/me
```

Without a valid token:

```text
401 Unauthorized
```

With a valid token:

```json
{
  "id": 3,
  "name": "Final Test",
  "email": "finaltest2026@test.com"
}
```

---

# 6. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Programming language |
| FastAPI | Backend REST APIs |
| SQLAlchemy | Database ORM |
| SQLite | Local database |
| NATS | Asynchronous messaging |
| nats-py | Python NATS client |
| JWT | Authentication |
| Docker | Containerization |
| Docker Compose | Multi-service orchestration |
| Git | Version control |
| GitHub | Source code hosting |

---

# 7. Project Structure

```text
microservices-assignment/
│
├── api-gateway/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── notification-service/
│   ├── database.py
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   ├── nats_client.py
│   ├── requirements.txt
│   └── schemas.py
│
├── user-service/
│   ├── auth.py
│   ├── database.py
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   ├── nats_client.py
│   ├── requirements.txt
│   └── schemas.py
│
├── architecture.png
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# 8. API Documentation

The project uses FastAPI's automatically generated API documentation.

After starting the project, open:

```text
http://localhost:8000/docs
```

This provides an interactive Swagger UI for testing the APIs.

---

## API Gateway Health Check

### GET `/`

Returns the API Gateway status.

Example response:

```json
{
  "service": "API Gateway",
  "status": "running"
}
```

---

# 9. User APIs

All User Service requests are accessed through the API Gateway.

## Register User

### POST

```text
/api/users/register
```

Example request:

```json
{
  "name": "Nithin Test",
  "email": "nithin2026@test.com",
  "password": "Test@12345"
}
```

Example response:

```json
{
  "id": 3,
  "name": "Nithin Test",
  "email": "nithin2026@test.com"
}
```

---

## Login

### POST

```text
/api/users/login
```

The login endpoint authenticates the user and returns a JWT access token.

Example:

```json
{
  "email": "nithin2026@test.com",
  "password": "Test@12345"
}
```

Example response:

```json
{
  "access_token": "<JWT_TOKEN>"
}
```

---

## Get Current User

### GET

```text
/api/users/me
```

Required header:

```text
Authorization: Bearer <JWT_TOKEN>
```

Example response:

```json
{
  "id": 3,
  "name": "Nithin Test",
  "email": "nithin2026@test.com"
}
```

---

# 10. Notification API

## Get Notifications

### GET

```text
/api/notifications
```

Example response:

```json
[
  {
    "id": 1,
    "user_id": 3,
    "message": "Welcome Nithin Test! Your account has been created.",
    "type": "WELCOME",
    "status": "SENT"
  }
]
```

---

# 11. API Status Codes

The application uses standard HTTP status codes.

| Status Code | Meaning |
|---|---|
| `200` | Successful request |
| `401` | Authentication required / invalid token |
| `405` | HTTP method not allowed |
| `409` | User already exists |
| `422` | Validation error |
| `503` | Downstream service unavailable |

---

# 12. Running the Project Locally

## Prerequisites

Install:

- Docker Desktop
- Git

Make sure Docker Desktop is running before starting the services.

---

## Clone the Repository

```bash
git clone https://github.com/Nithin3117/microservices-assignment.git
```

Enter the project directory:

```bash
cd microservices-assignment
```

---

## Start the Services

Run:

```bash
docker compose up --build
```

Or run in detached mode:

```bash
docker compose up --build -d
```

---

## Check Running Containers

```bash
docker compose ps
```

The following services should be running:

```text
api-gateway
user-service
notification-service
nats
```

---

# 13. Access the Services

### API Gateway

```text
http://localhost:8000
```

### Swagger Documentation

```text
http://localhost:8000/docs
```

### User Service

```text
http://localhost:8001
```

### Notification Service

```text
http://localhost:8002
```

### NATS

```text
nats://localhost:4222
```

---

# 14. Testing the Application

## Test Gateway

```powershell
Invoke-RestMethod -Uri "http://localhost:8000"
```

Expected:

```text
service : API Gateway
status  : running
```

---

## Test User Registration

```powershell
$body = @{
    name = "Final Test"
    email = "finaltest2026@test.com"
    password = "Test@12345"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:8000/api/users/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

---

## Test Notifications

```powershell
Invoke-RestMethod `
    -Uri "http://localhost:8000/api/notifications" `
    -Method Get
```

After successful registration, the Notification Service should create a welcome notification through the NATS event.

---

## Test Authentication

Login and save the returned access token.

Then request:

```text
GET /api/users/me
```

using:

```text
Authorization: Bearer <JWT_TOKEN>
```

A valid token returns the authenticated user.

A request without the token returns:

```text
401 Unauthorized
```

---

# 15. Useful Docker Commands

### View all services

```bash
docker compose ps
```

### View User Service logs

```bash
docker compose logs user-service --tail=50
```

### View Notification Service logs

```bash
docker compose logs notification-service --tail=50
```

### View API Gateway logs

```bash
docker compose logs api-gateway --tail=50
```

### Stop services

```bash
docker compose down
```

---

# 16. Environment Configuration

The project uses environment variables for service configuration.

Example configuration is provided in:

```text
.env.example
```

Docker Compose provides the required service URLs and NATS connection information.

Example:

```text
NATS_URL=nats://nats:4222
USER_SERVICE_URL=http://user-service:8001
NOTIFICATION_SERVICE_URL=http://notification-service:8002
```

---

# 17. Error Handling

The API Gateway handles downstream service connection errors and returns:

```json
{
  "detail": "Service temporarily unavailable"
}
```

with HTTP status:

```text
503 Service Unavailable
```

FastAPI/Pydantic validation handles invalid request data.

Authentication errors return appropriate `401 Unauthorized` responses.

---

# 18. Verification Completed

The following functionality was tested successfully:

- [x] Docker containers start successfully
- [x] API Gateway is running
- [x] User Service is running
- [x] Notification Service is running
- [x] NATS is running
- [x] User registration works
- [x] User login works
- [x] JWT token authentication works
- [x] Protected `/users/me` endpoint works
- [x] Unauthorized access is rejected
- [x] User Service publishes `user.created`
- [x] Notification Service receives `user.created`
- [x] Welcome notification is created
- [x] Notifications can be retrieved through the Gateway
- [x] Docker Compose deployment works

---

# 19. Submission Materials

This GitHub repository contains the complete submission materials in one place.

### Source Code

The complete source code is available in:

```text
api-gateway/
user-service/
notification-service/
```

### Project Documentation

This `README.md` contains:

- Project overview
- Architecture
- Technologies
- Service descriptions
- Event-driven communication
- Authentication
- API documentation
- Setup instructions
- Testing instructions
- Docker commands
- Verification details

### Architecture Diagram

```text
architecture.png
```

### API Documentation

The API documentation is also available through FastAPI Swagger:

```text
http://localhost:8000/docs
```

### Local Run Instructions

The complete local setup instructions are provided in this README.

### Submission Notes

The project is submitted through the following GitHub repository:

**GitHub Repository:**

https://github.com/Nithin3117/microservices-assignment

---

# 20. Submission

**GitHub Repository:**

https://github.com/Nithin3117/microservices-assignment

The repository contains the complete source code, README documentation, architecture diagram, Docker configuration, API documentation, and setup instructions.

---

## Author

**Nithin Bollineni**

B.Tech Student
