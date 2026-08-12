# Microservices Assignment

## Overview
A small microservices-based system built with Python and FastAPI. It contains two backend services and one API Gateway.

### Components
1. User Service
2. Notification Service
3. API Gateway

## Architecture
- Client communicates with the API Gateway.
- The API Gateway routes user and notification requests to the appropriate backend service.
- User Service publishes a `user.created` event through NATS after successful registration.
- Notification Service subscribes to `user.created` and creates a welcome notification asynchronously.
- JWT authentication protects the user profile endpoint.

## Technologies
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- NATS / nats-py
- JWT authentication
- Docker
- Docker Compose

## Services and Ports
| Service | Port |
|---|---:|
| API Gateway | 8000 |
| User Service | 8001 |
| Notification Service | 8002 |
| NATS | 4222 |
| NATS Monitoring | 8222 |

## Run Locally

### Prerequisites
- Docker Desktop
- Docker Compose

### Start
```bash
docker compose up --build
```

Or run in detached mode:
```bash
docker compose up --build -d
```

### Check services
```bash
docker compose ps
```

### API Gateway
Open:
`http://localhost:8000`

Swagger documentation:
`http://localhost:8000/docs`

## Main API Endpoints

### User Service through API Gateway
- `POST /api/users/register`
- `POST /api/users/login`
- `GET /api/users/me` (Bearer JWT required)

### Notification Service through API Gateway
- `GET /api/notifications`

## Event Flow
1. Client sends registration request to API Gateway.
2. API Gateway forwards it to User Service.
3. User Service creates the user and publishes `user.created` through NATS.
4. Notification Service receives the event.
5. Notification Service stores a welcome notification.
6. The notification can be retrieved through `GET /api/notifications`.

## Configuration
Service-to-service NATS and URL configuration is supplied through Docker Compose environment variables. Use `.env.example` as a reference for environment configuration.

## Security
- Passwords are handled by the User Service authentication layer.
- JWT access tokens are used for authenticated requests.
- Sensitive configuration is kept outside source code through environment variables.

## Project Structure
```text
microservices-assignment/
├── api-gateway/
├── notification-service/
├── user-service/
├── docker-compose.yml
├── architecture.png
├── README.md
├── .env.example
└── .gitignore
```

## Submission
Source code:
https://github.com/Nithin3117/microservices-assignment
