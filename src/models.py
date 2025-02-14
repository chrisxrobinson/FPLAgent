from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    team = Column(String)
    position = Column(String)
    points = Column(Integer)
    form = Column(Float)

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    points = Column(Integer)
    form = Column(Float)

class Fixture(Base):
    __tablename__ = "fixtures"
    
    id = Column(Integer, primary_key=True)
    home_team = Column(String)
    away_team = Column(String)
    date = Column(DateTime)
    result = Column(String)

def init_db():
    engine = create_engine('sqlite:///data/fplagent.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
