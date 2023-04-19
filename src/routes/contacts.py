from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repos_contacts

router = APIRouter(prefix='', tags=['contacts'])


@router.get('/all', response_model=List[ContactResponse])
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repos_contacts.get_contacts(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts


@router.get('/bday', response_model=List[ContactResponse])
async def get_nearest_bdays(db: Session = Depends(get_db)):
    contacts = await repos_contacts.get_nearest_bdays(db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repos_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@router.get('/{field_name}/{field_value}', response_model=List[ContactResponse])
async def get_contacts_by_field(field_name: str, field_value: str, db: Session = Depends(get_db)):
    contacts = await repos_contacts.get_contact_by_field(field_name, field_value, db)

    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repos_contacts.create(body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong Data')
    return contact


@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(body: ContactModel,
                         contact_id: int = Path(ge=1),
                         db: Session = Depends(get_db)):
    contact = await repos_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove(contact_id, db: Session = Depends(get_db)):
    contact = await repos_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact

