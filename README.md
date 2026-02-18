# Childcare Refund Manager

Childcare Refund Manager is a FastAPI web application for organizing therapy payments and reimbursement progress across children, therapists, receipts, and claims.

It is designed for a practical workflow:
1. A treatment occurs.
2. A receipt is collected.
3. A claim is submitted.
4. Refund progress is tracked until payment arrives.

---

## Application overview

### Core modules

- **Web app (`app/main.py`)**
  - HTML pages for dashboard, children, therapists, receipts, treatments, and claims.
  - Form-based creation and updates.
  - Auto-creation of one refund claim per treatment.

- **Data model (`app/models.py`)**
  - `Child`, `Therapist`, `Receipt`, `Treatment`, `RefundClaim`.
  - `RefundStatus` enum: `NOT_ISSUED`, `ISSUED`, `REFUND_RECEIVED`.

- **Database wiring (`app/db.py`)**
  - Uses `DATABASE_URL` env var.
  - Defaults to SQLite for local development.
  - Accepts PostgreSQL URLs for deployment.

- **Frontend templates (`app/templates/*`) + styles (`app/static/styles.css`)**
  - Simple, readable operational UI.

---

## Feature walkthrough

### 1) Dashboard

Shows quick metrics:
- Outstanding claim count
- Total paid (from treatments)
- Total refunded (from claims)
- Recent claims table

### 2) Children

Create and list child profiles with optional date of birth.

### 3) Therapists

Create and list provider records, including specialty and provider number.

### 4) Receipts

Record receipt metadata (file name, type, issue date, total amount).

### 5) Treatments

Add treatments linked to a child and therapist, with optional receipt linkage.
Each new treatment automatically creates a related refund claim.

### 6) Claims

Update reimbursement progress for each treatment claim:
- Status
- Submission date
- Received amount/date
- Reference number and notes

---

## Installation and local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

Open: <http://localhost:8000>

Health endpoint:

```bash
curl http://localhost:8000/healthz
```

---

## Testing

```bash
pytest
```

If dependencies are unavailable in your environment, you can still run a syntax check:

```bash
python -m compileall app tests
```

---

## Deployment

You can deploy locally, with Docker, or behind a reverse proxy.

- Full deployment guide: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
- Dockerfile included at repo root.

---

## User guide

For a full task-by-task operating guide (daily workflow, tips, troubleshooting):

- [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)

---

## Database notes

- Local development uses SQLite by default.
- A PostgreSQL-oriented MVP schema draft is also provided in [`schema.sql`](schema.sql).
- For production, prefer PostgreSQL, authentication, audit logs, encrypted backups, and secure object storage for receipt files.
