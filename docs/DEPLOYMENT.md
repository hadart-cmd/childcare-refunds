# Deployment Guide

This guide describes how to deploy Childcare Refund Manager in development and production-style environments.

## 1) Configuration

The app reads `DATABASE_URL` from the environment.

- Local default (if unset): `sqlite:///./refunds.db`
- PostgreSQL examples:
  - `postgresql://user:password@host:5432/refunds`
  - `postgres://user:password@host:5432/refunds`

Both PostgreSQL URL styles are accepted and normalized by the app at runtime.

## 2) Local deployment (virtualenv)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/healthz
```

## 3) Docker deployment

Build:

```bash
docker build -t childcare-refund-manager .
```

Run with SQLite volume:

```bash
docker run --rm -p 8000:8000 -v $(pwd)/data:/app/data \
  -e DATABASE_URL=sqlite:////app/data/refunds.db \
  childcare-refund-manager
```

Run with PostgreSQL:

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL=postgresql://refunds:secret@postgres:5432/refunds \
  childcare-refund-manager
```

## 4) Reverse proxy notes (Nginx/Caddy)

- Forward traffic to `127.0.0.1:8000`.
- Preserve `Host`, `X-Forwarded-Proto`, and `X-Forwarded-For` headers.
- Enable HTTPS with automatic certificate renewal.

## 5) Backup strategy

- SQLite: snapshot the DB file daily.
- PostgreSQL: use daily logical dumps (`pg_dump`) and point-in-time recovery if available.
- Keep encrypted backups in a separate account/location.

## 6) Production hardening checklist

- Add authentication and role-based access.
- Run with PostgreSQL instead of SQLite.
- Use object storage for receipts (S3-compatible).
- Add audit logs for entity and claim status changes.
- Add structured app logging and uptime monitoring.
