from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.db import get_session, init_db
from app.models import Child, Receipt, RefundClaim, RefundStatus, Therapist, Treatment


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Childcare Refund Manager", lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def dashboard(request: Request, session: Session = Depends(get_session)):
    claims = session.exec(select(RefundClaim).order_by(RefundClaim.created_at.desc())).all()
    treatments = session.exec(select(Treatment)).all()

    outstanding = len([c for c in claims if c.status != RefundStatus.REFUND_RECEIVED])
    total_paid = sum(t.amount for t in treatments)
    total_refunded = sum((c.received_amount or 0) for c in claims)

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "outstanding": outstanding,
            "total_paid": total_paid,
            "total_refunded": total_refunded,
            "claims": claims,
        },
    )


@app.get("/children")
def list_children(request: Request, session: Session = Depends(get_session)):
    children = session.exec(select(Child).order_by(Child.full_name)).all()
    return templates.TemplateResponse(request, "children.html", {"children": children})


@app.post("/children")
def create_child(
    full_name: str = Form(...),
    date_of_birth: Optional[date] = Form(None),
    session: Session = Depends(get_session),
):
    child = Child(full_name=full_name, date_of_birth=date_of_birth)
    session.add(child)
    session.commit()
    return RedirectResponse(url="/children", status_code=303)


@app.get("/therapists")
def list_therapists(request: Request, session: Session = Depends(get_session)):
    therapists = session.exec(select(Therapist).order_by(Therapist.full_name)).all()
    return templates.TemplateResponse(request, "therapists.html", {"therapists": therapists})


@app.post("/therapists")
def create_therapist(
    full_name: str = Form(...),
    specialty: Optional[str] = Form(None),
    provider_number: Optional[str] = Form(None),
    session: Session = Depends(get_session),
):
    therapist = Therapist(full_name=full_name, specialty=specialty, provider_number=provider_number)
    session.add(therapist)
    session.commit()
    return RedirectResponse(url="/therapists", status_code=303)


@app.get("/treatments")
def list_treatments(request: Request, session: Session = Depends(get_session)):
    treatments = session.exec(select(Treatment).order_by(Treatment.treatment_date.desc())).all()
    children = session.exec(select(Child).order_by(Child.full_name)).all()
    therapists = session.exec(select(Therapist).order_by(Therapist.full_name)).all()
    receipts = session.exec(select(Receipt).order_by(Receipt.created_at.desc())).all()

    child_map = {str(c.id): c.full_name for c in children}
    therapist_map = {str(t.id): t.full_name for t in therapists}

    return templates.TemplateResponse(
        request,
        "treatments.html",
        {
            "treatments": treatments,
            "children": children,
            "therapists": therapists,
            "receipts": receipts,
            "child_map": child_map,
            "therapist_map": therapist_map,
        },
    )


@app.post("/treatments")
def create_treatment(
    child_id: UUID = Form(...),
    therapist_id: UUID = Form(...),
    treatment_date: date = Form(...),
    amount: float = Form(...),
    notes: Optional[str] = Form(None),
    receipt_id: Optional[UUID] = Form(None),
    session: Session = Depends(get_session),
):
    treatment = Treatment(
        child_id=child_id,
        therapist_id=therapist_id,
        treatment_date=treatment_date,
        amount=amount,
        notes=notes,
        receipt_id=receipt_id,
    )
    session.add(treatment)
    session.commit()
    session.refresh(treatment)

    claim = RefundClaim(treatment_id=treatment.id, expected_refund_amount=amount)
    session.add(claim)
    session.commit()

    return RedirectResponse(url="/treatments", status_code=303)


@app.get("/receipts")
def list_receipts(request: Request, session: Session = Depends(get_session)):
    receipts = session.exec(select(Receipt).order_by(Receipt.created_at.desc())).all()
    return templates.TemplateResponse(request, "receipts.html", {"receipts": receipts})


@app.post("/receipts")
def create_receipt(
    file_name: str = Form(...),
    mime_type: Optional[str] = Form(None),
    issued_on: Optional[date] = Form(None),
    total_amount: Optional[float] = Form(None),
    session: Session = Depends(get_session),
):
    receipt = Receipt(file_name=file_name, mime_type=mime_type, issued_on=issued_on, total_amount=total_amount)
    session.add(receipt)
    session.commit()
    return RedirectResponse(url="/receipts", status_code=303)


@app.get("/claims")
def list_claims(request: Request, session: Session = Depends(get_session)):
    claims = session.exec(select(RefundClaim).order_by(RefundClaim.created_at.desc())).all()
    treatments = session.exec(select(Treatment)).all()
    treatment_map = {str(t.id): t for t in treatments}
    return templates.TemplateResponse(
        request,
        "claims.html",
        {"claims": claims, "statuses": list(RefundStatus), "treatment_map": treatment_map},
    )


@app.post("/claims/{claim_id}")
def update_claim(
    claim_id: UUID,
    status: RefundStatus = Form(...),
    submitted_on: Optional[date] = Form(None),
    received_amount: Optional[float] = Form(None),
    received_on: Optional[date] = Form(None),
    reference_number: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    session: Session = Depends(get_session),
):
    claim = session.get(RefundClaim, claim_id)
    if claim:
        claim.status = status
        claim.submitted_on = submitted_on
        claim.received_amount = received_amount
        claim.received_on = received_on
        claim.reference_number = reference_number
        claim.notes = notes
        session.add(claim)
        session.commit()
    return RedirectResponse(url="/claims", status_code=303)
