from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, Float, String, Date, Table, ForeignKey, UniqueConstraint
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
    email = Column(String(80), primary_key=True)
    password = Column(String(255), nullable=False)
    name = Column(String(80), nullable=False)
    rols = relationship('Role', backref='owner')

    def __init__(self,email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return "<User(email='%s', password='%s')>" % (self.email, self.password)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    email=Column(String(80), ForeignKey('users.email', onupdate="CASCADE", ondelete="CASCADE"), nullable=False) #User's email
    role= Column(String(20), nullable=False)
    UniqueConstraint(email, role)

    def __init__(self, role, user):
        self.role = role
        self.owner = user
    
    def __repr__(self):
        return "<Role(email='%s',role='%s')>" % (self.email,self.role)

class GlobalVariables(Base):
    __tablename__ = 'globals'
    id = Column(Integer, primary_key=True)
    workDayLength = Column(Integer, default = 1, nullable =False)
    averageSpeed = Column(Float, default = 0.5, nullable = False)

    def __init__(self, workDayLength, averageSpeed):
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
    user1 =User('user1@c.com', p1, 'User1')
    user2 = User('user2@c.com', p1, 'User2')
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    role = Role('admin', user1)
    role1= Role('manager', user1)
    role2= Role('admin', user2)
    campaign1 = Campaign("werh", "Kevin", "xin", "date", "time", "12 street")
    db_session.add(role)
    db_session.add(role1)
    db_session.add(role2)
    db_session.add(campaign1)
    glo = GlobalVariables(1, 1)
    db_session.add(glo)
    db_session.commit()

