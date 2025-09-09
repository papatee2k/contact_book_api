from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud, model.models, model.schemas
from db import SessionLocal

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)


# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a contact
@router.post("/", response_model=model.schemas.contactOut)
def create_contact(contact: model.schemas.contactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)


# Get all contacts
@router.get("/", response_model=List[model.schemas.contactOut])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_contacts(db, skip=skip, limit=limit)


# Get a single contact
@router.get("/{contact_id}", response_model=model.schemas.contactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_single_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# Update a contact
@router.put("/{contact_id}", response_model=model.schemas.contactOut)
def update_contact(contact_id: int, updates: model.schemas.contactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, updates=updates)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# Delete a contact
@router.delete("/{contact_id}", response_model=model.schemas.contactOut)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
