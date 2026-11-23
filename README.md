# API Sentinel

API Sentinel is a learning and portfolio project: an API testing and reliability platform with project/collection organization, saved HTTP requests, request execution, authentication, and an AI-assisted test-case generation interface.

> Status: active development. The AI endpoint currently uses a deterministic example-rules provider, not a connected LLM. Request execution is intentionally restricted to public HTTP(S) destinations and should be further hardened before public deployment.

## Features

- FastAPI REST API with interactive Swagger documentation.
- PostgreSQL persistence through SQLAlchemy 2.
- Alembic schema migrations.
- User registration, Argon2 password hashing, JWT bearer authentication.
- User-owned projects with CRUD operations.
- Collections and saved API request definitions.
- HTTP request execution with timeout and response-size limits.
- Provider abstraction for AI test generation; deterministic local provider included.
- Pytest coverage and GitHub Actions CI.

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment:
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Create your local environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
   Change `JWT_SECRET_KEY` to a long random value. Do not commit `.env`.
4. Start PostgreSQL:
   ```powershell
   docker compose up -d
   ```
5. Create and apply the initial migration:
   ```powershell
   alembic revision --autogenerate -m "initial schema"
   alembic upgrade head
   ```
   Review generated migration files before applying them. If you are continuing from an older database with an existing migration history, do not overwrite or stamp blindly; reconcile the migration chain first.
6. Start the API:
   ```powershell
   uvicorn app.main:app --reload
   ```
7. Open http://127.0.0.1:8000/docs.

## Main API workflow

1. `POST /api/v1/users/register` with email and password (minimum 12 characters).
2. `POST /api/v1/auth/login` using form fields `username` (email) and `password`.
3. Click **Authorize** in Swagger and paste the returned access token.
4. Create a project using `POST /api/v1/projects`.
5. Create a collection using `POST /api/v1/projects/{project_id}/collections`.
6. Save a request using `POST /api/v1/collections/{collection_id}/requests`.
7. Execute it using `POST /api/v1/requests/{request_id}/run`.
8. Generate sample test ideas using `POST /api/v1/ai/generate-tests`.

## Tests and quality

```powershell
pytest -q
ruff check app tests
```

CI runs both commands on pushes and pull requests to `main`.

## Security notes

- Passwords are hashed with Argon2; plaintext passwords are never stored.
- JWT secret must be unique and private in any non-local environment.
- Project, collection, and request routes require authentication and enforce project ownership.
- Request execution blocks localhost/private/reserved IP addresses, disables redirects and proxy environment inheritance, uses a timeout, and truncates response bodies. This is a baseline SSRF defense, not a complete production-grade network sandbox. DNS rebinding and infrastructure-specific egress risks require network-level controls.
- Do not store production credentials in request headers without adding encryption-at-rest and secret redaction.
- Add rate limiting, audit logging, token revocation/refresh, stronger URL validation, deployment secrets, and security review before production use.

## Architecture

`API routes -> services -> repositories -> SQLAlchemy models -> PostgreSQL`

The AI layer uses a provider protocol so a real LLM implementation can be added without coupling routes to a vendor.

## Roadmap

- [x] FastAPI foundation and health endpoints
- [x] PostgreSQL and SQLAlchemy persistence
- [x] Alembic migrations
- [x] User registration and JWT authentication
- [x] User-owned project CRUD
- [x] Collections and saved requests
- [x] HTTPX request execution
- [x] AI provider interface and local example generator
- [x] Pytest suite and GitHub Actions CI configuration
- [x] Documentation and setup guide
- [ ] Real LLM provider integration, background jobs, reporting, deployment, and production security hardening

## Portfolio honesty

This repository is a functional starter implementation. The AI generation currently returns rule-based examples; describe it that way unless/until a real model provider is integrated and tested.
