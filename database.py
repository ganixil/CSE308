from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Float
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from datetime import date
import pymysql

#database connection string example
#'mysql+pymysql://username:password@address:port/databaseName'
#connect to the database with the database connection string
engine = create_engine('mysql+pymysql://xiangyiliu:111308288@mysql3.cs.stonybrook.edu:3306/xiangyiliu', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))

#make the sqlalchemy object relation mapper base class
Base = declarative_base()
Base.query = db_session.query_property()

#function to initalize the database
def init_db():
    Base.metadata.create_all(bind=engine)

#database table models/object relational classes
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(80))
    accType = Column(String(9))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        #'polymorphic_on':accType
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

class GlobalVariables(Base):
    __tablename__ = 'globalVariables'
    id = Column(Integer, primary_key=True)
    workDayLength = Column(Float)
    averageSpeed = Column(Float)
    def __init__(self, id, workDayLength, averageSpeed):
        self.id = id
        self.workDayLength = workDayLength
        self.averageSpeed = averageSpeed

class Campaign(Base):

    __tablename__ = 'campaign'
    id = Column(String(100), primary_key=True)
    manager = Column(String(20), nullable=False)
    canvasser = Column(String(20), nullable=False)
    date = Column(String(20))
    location = Column(String(20))        

    
    #id = campaign name

    def __init__(self, id, manager, canvasser, date, time, location):
        self.id = id
        self.manager = manager
        self.canvasser = canvasser
        self.date = date
        self.time = time
        self.location = location



#to be implemented
#class Availability(Base):
    #__tablename__ = 'availabilities'
    #id = Column(Integer, primary_key=True)
    #date = Column(Date)
    #canvasserId = Column(Integer, ForeignKey('canvassers.id'))
    #def __init__(self, id, date, canvasserId):
        #self.id
        #self.date = date
        #self.canvasserId = canvasserId


#for populating the database for testing purposes
if __name__ == "__main__":
    init_db()
    p1 = generate_password_hash('password')
    can = Canvasser(1, 'user1@c.com', p1, 'Mark', 'canvasser')
    ad = Admin(2, 'user2@c.com', p1, 'John', 'admin')
    campaign1 = Campaign("werh", "Kevin", "xin", "date", "time", "12 street")
    man = Manager(3, 'user3@c.com', p1, 'Phil', 'manager')
    glo = GlobalVariables(1, 1, 2)
    
    db_session.add(glo)
    db_session.add(can)
    db_session.add(ad)
    db_session.add(man)
    db_session.add(campaign1)
    db_session.commit()

