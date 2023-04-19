import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact(contact_id, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


def nearest_bdays(contacts):
    near_contacts = []
    for contact in contacts:
        next_bday = datetime.date(datetime.date.today().year, contact.birth_date.month, contact.birth_date.day)
        if next_bday > datetime.date.today():
            if next_bday - datetime.date.today() < datetime.timedelta(7):
                near_contacts.append(contact)
    return near_contacts


async def get_nearest_bdays(db: Session):
    contacts = nearest_bdays(db.query(Contact).all())
    return contacts


async def get_contact_by_field(field_name, field_value: str, db: Session):
    if not hasattr(Contact, field_name):
        raise HTTPException(status_code=404, detail="Invalid field name")
    contacts = db.query(Contact).filter(getattr(Contact, field_name) == field_value).all()
    return contacts


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    if contact:
        db.add(contact)
        db.commit()
        db.refresh(contact)
        db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birth_date = body.birth_date
        db.commit()
        db.refresh(contact)
    return contact


async def remove(contact_id, db: Session):
    contact = await get_contact(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
