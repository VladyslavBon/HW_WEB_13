from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.sсhemas import ContactCreate


async def get_contacts(user: User, db: Session):
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    contacts = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    return contacts


async def get_contact_by_email(email: str, user: User, db: Session):
    contacts = (
        db.query(Contact)
        .filter(and_(Contact.email == email, Contact.user_id == user.id))
        .first()
    )
    return contacts


async def search_contact(query: str, user: User, db: Session):
    contact = (
        db.query(Contact)
        .filter(and_(Contact.firstname.ilike(f"%{query}%"), Contact.user_id == user.id))
        .all()
    )
    if contact:
        return contact
    contact = (
        db.query(Contact)
        .filter(and_(Contact.lastname.ilike(f"%{query}%"), Contact.user_id == user.id))
        .all()
    )
    if contact:
        return contact
    contact = (
        db.query(Contact)
        .filter(and_(Contact.email.ilike(f"%{query}%"), Contact.user_id == user.id))
        .all()
    )
    if contact:
        return contact


async def create_contact(body: ContactCreate, user: User, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactCreate, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete_contact(contact_id: int, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_birthday_per_week(user: User, db: Session):
    contacts = []
    all_contacts = await get_contacts(user, db)
    for contact in all_contacts:
        if (
            timedelta(0)
            <= (
                datetime.now().date()
                - (contact.birthday.replace(year=int((datetime.now()).year)))
            )
            <= timedelta(7)
        ):
            contacts.append(contact)
    return contacts
