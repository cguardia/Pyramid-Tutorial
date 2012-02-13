from sqlalchemy import Column
from sqlalchemy import TIMESTAMP
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import Authenticated
from pyramid.security import Allow

from cryptacular.bcrypt import BCRYPTPasswordManager

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
crypt = BCRYPTPasswordManager()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    userid = Column(Unicode(20))
    password = Column(Unicode(20))
    fullname = Column(Unicode(40))
    about = Column(Unicode(255))

    def __init__(self, userid, password, fullname, about):
        self.userid = userid
        self.password = crypt.encode(password)
        self.fullname = fullname
        self.about = about

class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    follower = Column(Integer, ForeignKey('users.id'))
    follows = Column(Integer, ForeignKey('users.id'))

    def __init__(self, follower, follows):
        self.follower = follower
        self.follows = follows

class Chirp(Base):
    __tablename__ = 'chirps'
    id = Column(Integer, primary_key=True)
    chirp = Column(Unicode(255))
    timestamp = Column(TIMESTAMP())
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship(User, cascade='delete', backref='chirps')

    def __init__(self, chirp, author, timestamp):
        self.chirp = chirp
        self.author = author
        self.timestamp = timestamp

class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, 'view')
    ]
    def __init__(self, request):
        pass

def check_login(login, password):
    session = DBSession()
    user = session.query(User).filter_by(userid=login).first()
    if user is not None:
        hashed_password = user.password
        if crypt.check(hashed_password, password):
            return True
    return False

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
