import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, relationship

from . import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmake(bind=engine)
session = Session()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    company = Column(String(100))
    location = Column(String(100))
    industry = Column(String(100))
    link_to_website = Column(String(250))
    positions = relationship('Position', backref='company')

class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    position_name = Column(String(100))
    date_added = Column(DateTime, default=datetime.datetime.now)
    date_due = Column(DateTime, default=datetime.datetime.now)
    link_to_website = Column(String(250))
    company_id = Column(Integer, foreign_key='companies.id')
    application = relationship('Application', backref='position')

class Application(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    cv = Column(Boolean)
    cover_letter = Column(Boolean)
    application_questions = Column(Boolean)
    recruitment_process = Column(Text)
    contact_info = Column(Text)
    application_status = Column(Boolean)
    position_id = Column(Integer, foreign_key='positions.id')

Base.metadata.create_all(engine)
