from sqlalchemy.orm import Session
from model.models import Contact
from model.schemas import contactCreate, contactUpdate
from datetime import datetime

# Create a contact
def create_contact(db: Session, contact: contactCreate):
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        phone_numbers=",".join(contact.phone_numbers),
        emails=",".join(contact.emails) if contact.emails else None,
        address=contact.address,
        birthday=contact.birthday,
        notes=contact.notes,
        favorite=contact.favorite,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Getting a single contact by ID
def get_single_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

# Get all contacts
def get_all_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()


# Update a contact
def update_contact(db: Session, contact_id: int, updates: contactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None

    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key in ["phone_numbers", "emails"] and value is not None:
            value = ",".join(value)
        setattr(db_contact, key, value)

    db_contact.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Delete a contact
def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact