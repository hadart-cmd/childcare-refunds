# Childcare Refund Manager

A practical app concept for managing therapy treatment refunds across multiple children and therapists.

## Why this is a great fit

Your problem has clear, structured data and a repeatable workflow:

1. A treatment happens.
2. You get a receipt (sometimes covering multiple treatments).
3. You submit to insurance/funder.
4. You track refund progress.

That makes this ideal for an application with reporting, reminders, and OCR-assisted data entry.

## Core entities

- **Children**: each child profile.
- **Therapists**: providers linked to one or more children.
- **Receipts**: uploaded file (PDF/image) that can contain multiple treatment lines.
- **Treatments**: date, amount, child, therapist, and receipt linkage.
- **Refund claims**: grouped submissions and status tracking.

## Suggested refund status model

Use a strict enum to prevent confusion:

- `NOT_ISSUED` (prepared but not submitted)
- `ISSUED` (submitted to insurer/funder)
- `REFUND_RECEIVED` (money received)

For the MVP schema, each treatment has one refund-claim record so status progression remains simple and auditable.

Optional additions:

- `PARTIALLY_REFUNDED`
- `REJECTED`

## MVP feature set

### 1) Data management

- Create/edit children and therapists.
- Record treatments manually.
- Attach each treatment to a receipt.
- Group multiple treatments from one receipt.

### 2) Receipt upload + extraction

- Upload PDF/JPG/PNG receipts.
- Parse both printed and handwritten receipt text (where legible).
- OCR/HTR extracts:
  - therapist name
  - date(s)
  - line-item amount(s)
  - total amount
- User reviews and confirms extracted data before saving.

### 3) Refund tracking

- Mark status (`NOT_ISSUED` → `ISSUED` → `REFUND_RECEIVED`).
- Keep a single claim timeline per treatment to avoid duplicate status records.
- Store:
  - claim submission date
  - expected amount
  - received amount/date
  - notes/reference number

### 4) Dashboard & reporting

- Outstanding claims by child/therapist.
- Total paid vs refunded per month.
- Filters by date range and status.

## Recommended architecture

- **Frontend**: React + TypeScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **File storage**: S3-compatible bucket or local object storage
- **OCR**:
  - baseline: Tesseract + invoice parsing rules (printed text)
  - handwritten-capable: cloud OCR/HTR (Google Vision, AWS Textract AnalyzeExpense, or Azure Document Intelligence)

## OCR strategy (important)

Receipt formats vary a lot. A robust approach is:

1. OCR text extraction.
2. Rule-based parser (dates, currencies, provider name candidates).
3. Confidence scoring for each extracted field, including handwriting confidence.
4. If handwriting confidence is low, route to a manual review queue.
5. Human confirmation UI before final save.

This keeps automation high while avoiding silent mistakes.

## Suggested roadmap

### Phase 1 (1-2 weeks)

- CRUD for children, therapists, receipts, treatments.
- Refund status tracking.
- Basic dashboard and filters.

### Phase 2 (1-2 weeks)

- OCR upload pipeline + manual confirmation screen.
- Duplicate detection (same date/amount/provider).

### Phase 3

- CSV export for accountant/insurance.
- Email reminders for pending claims.
- Mobile-friendly capture flow (photo to receipt).

## Security and privacy checklist

Because this includes children and health-adjacent data:

- Role-based authentication.
- Encrypt files at rest.
- Audit log for edits/status changes.
- Backup and restore plan.
- Keep only required personal data.

## Practical recommendation

Yes — this is an excellent app idea and very feasible.

The biggest win will come from **OCR/HTR + confirmation workflow** plus **clean status tracking** across children and therapists. Handwritten fields can be parsed as well, but should always use confidence scoring and review fallback. If you want, the next step is to scaffold the backend + database schema and deliver a clickable MVP quickly.
