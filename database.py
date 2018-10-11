from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
import pymysql

#'mysql+pymysql://username:password@address:port/databaseName'
engine = create_engine('mysql+pymysql://xiangyiliu:111308288@mysql3.cs.stonybrook.edu:3306/xiangyiliu', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    name = Column(String(80))
    accType = Column(String(9))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':accType
    }

    def __init__(self, id, email, password, name, accType):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.accType = accType

    def __repr__(self):
        return "<User(email='%s', password='%s', accType='%s')>" % (self.email, self.password, self.accType)

class Canvasser(User):
    __tablename__ = 'canvassers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    #availability = relationship('Availability')
    __mapper_args__ = {
        'polymorphic_identity':'canvasser',
    }

    
    def __init__(self, id, email, password, name, accType):
        User.__init__(self, id, email, password, name, accType)

class Admin(User):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'admin',
    }

    def __init__(self, id, email, password, name, accType):
        User.__init__(self, id, email, password, name, accType)

class Manager(User):
    __tablename__ = 'managers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'manager',
    }

    def __init__(self, id, email, password, name, accType):
        User.__init__(self, id, email, password, name, accType)

#class Availability(Base):
    #__tablename__ = 'availabilities'
    #id = Column(Integer, primary_key=True)
    #date = Column(Date)
    #canvasserId = Column(Integer, ForeignKey('canvassers.id'))
    #def __init__(self, id, date, canvasserId):
        #self.id
        #self.date = date
        #self.canvasserId = canvasserId

#class Admin(Base):
#    __tablename__ = 'admins'
  #  id = Column

if __name__ == "__main__":
    init_db()
    can = Canvasser(1, 'user1@c.com', 'password', 'Mark', 'canvasser')
    ad = Admin(2, 'user2@c.com', 'password', 'John', 'admin')
    man = Manager(3, 'user3@c.com', 'password', 'Phil', 'manager')
    db_session.add(can)
    db_session.add(ad)
    db_session.add(man)
    db_session.commit()
