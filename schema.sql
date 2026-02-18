-- PostgreSQL schema for Childcare Refund Manager MVP

CREATE TYPE refund_status AS ENUM ('NOT_ISSUED', 'ISSUED', 'REFUND_RECEIVED');

CREATE TABLE children (
  id UUID PRIMARY KEY,
  full_name TEXT NOT NULL,
  date_of_birth DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE therapists (
  id UUID PRIMARY KEY,
  full_name TEXT NOT NULL,
  specialty TEXT,
  provider_number TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE child_therapists (
  child_id UUID NOT NULL REFERENCES children(id) ON DELETE CASCADE,
  therapist_id UUID NOT NULL REFERENCES therapists(id) ON DELETE CASCADE,
  PRIMARY KEY (child_id, therapist_id)
);

CREATE TABLE receipts (
  id UUID PRIMARY KEY,
  file_name TEXT NOT NULL,
  mime_type TEXT,
  storage_key TEXT NOT NULL,
  source_text TEXT,
  handwriting_detected BOOLEAN NOT NULL DEFAULT FALSE,
  extraction_engine TEXT,
  ocr_confidence NUMERIC(5,2),
  handwriting_confidence NUMERIC(5,2),
  issued_on DATE,
  total_amount NUMERIC(12,2),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE treatments (
  id UUID PRIMARY KEY,
  child_id UUID NOT NULL REFERENCES children(id),
  therapist_id UUID NOT NULL REFERENCES therapists(id),
  receipt_id UUID REFERENCES receipts(id) ON DELETE SET NULL,
  treatment_date DATE NOT NULL,
  amount NUMERIC(12,2) NOT NULL CHECK (amount >= 0),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE refund_claims (
  id UUID PRIMARY KEY,
  treatment_id UUID NOT NULL UNIQUE REFERENCES treatments(id) ON DELETE CASCADE,
  status refund_status NOT NULL DEFAULT 'NOT_ISSUED',
  submitted_on DATE,
  expected_refund_amount NUMERIC(12,2),
  received_amount NUMERIC(12,2),
  received_on DATE,
  reference_number TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_treatments_child_date ON treatments(child_id, treatment_date);
CREATE INDEX idx_treatments_therapist_date ON treatments(therapist_id, treatment_date);
CREATE INDEX idx_claims_status ON refund_claims(status);
