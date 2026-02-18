# User Guide

## What this app tracks

The system manages five core records:

1. **Children** – profiles of children receiving therapy.
2. **Therapists** – providers and identifying details.
3. **Receipts** – uploaded/recorded payment documents.
4. **Treatments** – dated services linked to child + therapist (+ optional receipt).
5. **Refund claims** – one claim per treatment that moves through status stages.

## Refund lifecycle

Each treatment has one claim with a strict status lifecycle:

- `NOT_ISSUED` – prepared but not submitted.
- `ISSUED` – submitted to insurer/funder.
- `REFUND_RECEIVED` – payout has been received.

## Daily workflow

1. Add all children from **Children**.
2. Add therapists from **Therapists**.
3. Record receipts in **Receipts**.
4. Record treatments in **Treatments**.
   - When saved, the app auto-creates a claim with `NOT_ISSUED`.
5. Open **Claims** and update claim fields:
   - status
   - submission date
   - received amount/date
   - reference number and notes
6. Review **Dashboard** totals and outstanding claim count.

## Data entry tips

- Use consistent therapist names to avoid duplicates.
- Enter receipt total amounts even when receipts include multiple lines.
- Capture claim reference numbers as soon as submissions are made.
- Update `received_amount` and `received_on` immediately when money lands.

## Troubleshooting

- If a page is empty, verify prerequisite data exists (e.g., treatments need children + therapists).
- If app fails to start, verify dependencies are installed and `DATABASE_URL` is valid.
- Use `/healthz` to quickly confirm app service availability.
