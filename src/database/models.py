from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from src.database.db import engine

# Create parent base
Base = declarative_base()


# Create base class
class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String(length=25), index=True)
    phone = Column(String(length=13), index=True)
    birth_date = Column(DateTime, index=True)
