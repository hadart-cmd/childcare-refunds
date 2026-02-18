from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RefundStatus(str, Enum):
    NOT_ISSUED = "NOT_ISSUED"
    ISSUED = "ISSUED"
    REFUND_RECEIVED = "REFUND_RECEIVED"


class Child(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: str
    date_of_birth: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Therapist(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    full_name: str
    specialty: Optional[str] = None
    provider_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Receipt(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    file_name: str
    mime_type: Optional[str] = None
    issued_on: Optional[date] = None
    total_amount: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Treatment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    child_id: UUID = Field(foreign_key="child.id")
    therapist_id: UUID = Field(foreign_key="therapist.id")
    receipt_id: Optional[UUID] = Field(default=None, foreign_key="receipt.id")
    treatment_date: date
    amount: float
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class RefundClaim(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    treatment_id: UUID = Field(foreign_key="treatment.id", unique=True)
    status: RefundStatus = Field(default=RefundStatus.NOT_ISSUED)
    submitted_on: Optional[date] = None
    expected_refund_amount: Optional[float] = None
    received_amount: Optional[float] = None
    received_on: Optional[date] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
