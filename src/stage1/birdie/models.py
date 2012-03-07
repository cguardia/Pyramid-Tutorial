from sqlalchemy import Column
from sqlalchemy import TIMESTAMP
from sqlalchemy import Unicode
from sqlalchemy import Integer

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Chirp(Base):
    __tablename__ = 'chirps'
    id = Column(Integer, primary_key=True)
    chirp = Column(Unicode(255))
    author = Column(Unicode(20))
    timestamp = Column(TIMESTAMP())

    def __init__(self, chirp, author, timestamp):
        self.chirp = chirp
        self.author = author
        self.timestamp = timestamp

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
