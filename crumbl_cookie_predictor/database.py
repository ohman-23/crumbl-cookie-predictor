from requests import session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pandas as pd
import json
from enum import Enum

Base = declarative_base()

class CookieEntries(Base):
    __tablename__ = "cookie_entries"
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    image = Column("image", String, nullable=True)
    description = Column("description", Text(100), nullable=True)
    temperature = Column("temperature", String, nullable=True)
    recorded_at = Column("recorded_at", DateTime, default=datetime.utcnow())

    def __init__(self, name, image=None, description=None, temperature=None, recorded_at=None):
        self.name = name
        self.image = image
        self.description = description
        self.temperature = temperature
        if (recorded_at is not None) and (type(recorded_at) is datetime):
            self.recorded_at = recorded_at

    def __repr__(self):
        return f"{self.name} | {self.recorded_at}"

class DatabaseNames(Enum):
    DESCRIPTIVE = "sqlite:///crumbl_cookies_descriptive.db"
    BASIC = "sqlite:///crumbl_cookies_basic.db"

class Database:
    def __init__(self, db=DatabaseNames.BASIC):
        db_name = db
        if db is not None:
            db_name = db
        engine = create_engine(db_name.value, echo=False)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)

        self.db_name = db_name.value
        self.session = Session()
    
    def close(self):
        self.session.close()

    def save_to_json(self):
        print("Not Implemented Yet")
        pass

    def save_to_csv(self):
        print("Not Implemented Yet")
        pass
