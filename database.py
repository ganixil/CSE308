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
    name = Column(String(80), nullable=False)
    email=Column(String(80), ForeignKey('users.email', onupdate="CASCADE", ondelete="CASCADE"), nullable=False) #User's email
    role= Column(String(20), nullable=False)
    UniqueConstraint(email, role)

    def __init__(self, role, user, name):
        self.role = role
        self.owner = user
        self.name = name    
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
    id = Column(Integer, primary_key=True) #id = campaign name
    campaign = Column(String(40), nullable=False)
    personName = Column(String(20), nullable=False)
    role = Column(String(20), nullable=False)
    date = Column(String(20), nullable=False)
    location = Column(String(20), nullable=False)        


    def __init__(self, campaign, personName, role, date, time, location):
        self.campaign = campaign
        self.personName = personName
        self.role = role
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
    user1 =User('user1@c.com', p1, 'Kevin')
    user2 = User('user2@c.com', p1, 'Conor')
    user3 =User('user3@c.com', p1, 'XiangY')
    user4 = User('user4@c.com', p1, 'Xiang')
    db_session.add(user1)
    db_session.add(user2)
    db_session.add(user3)
    db_session.add(user4)
    db_session.commit()

    role = Role('admin', user1, user1.name)
    role1= Role('manager', user1, user1.name)
    role2= Role('admin', user2, user2.name)
    role3= Role('manager', user3, user3.name)
    role4= Role('manager', user4, user4.name)
    campaign1 = Campaign("Miss Camp", "Kevin", "manager", "10/19", "12:00pm", "12 street")
    db_session.add(role)
    db_session.add(role1)
    db_session.add(role2)
    db_session.add(role3)
    db_session.add(role4)
    db_session.add(campaign1)
    glo = GlobalVariables(1, 1)
    db_session.add(glo)
    db_session.commit()

