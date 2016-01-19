from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    TIMESTAMP,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Chirp(Base):
    __tablename__ = 'chirps'
    id = Column(Integer, primary_key=True)
    chirp = Column(Unicode(255))
    author = Column(Unicode(20))
    timestamp = Column(TIMESTAMP())

