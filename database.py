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

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key = True)
    campaign_name = Column(String(80), nullable = False)  #One company with unique name
    talking = Column(String(80), default="None", nullable= False) # defautl = None 
    questionairs = Column(String(80), nullable= True)  # question1;question2;....
    durations = Column(Integer, default = 0, nullable=False) # default = 0
    campaigns_relation= relationship("CampaignUser", backref = "campaigns")
    campaigns_relation_1= relationship("CampaignLocation", backref = "campaigns")

    def __init__(self, campaign_name, talking, questionairs, durations):
        self.campaign_name = campaign_name
        self.talking = talking
        self.questionairs = questionairs
        self.durations = durations

class Role(Base):  # One user can have many role : one to many
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    email=Column(String(80), ForeignKey('users.email', onupdate="CASCADE", ondelete="CASCADE"), nullable=False) #User's email
    name = Column(String(80), nullable = False)
    role= Column(String(20), nullable=False)
    #One roles can be work on multiple campaign
    roles_relation = relationship("CampaignUser", backref= "roles")
    UniqueConstraint(email, role)
    # A collection of roles on User
    def __init__(self, name, role):
        self.role = role
        self.name = name
    
    def __repr__(self):
        return "<Role(email='%s',role='%s')>" % (self.email,self.role)

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key= True)
    number = Column(Integer, nullable = True) # street number
    street = Column(String(60), nullable= False) 
    unit = Column(String(60), nullable = True) # Apartment16B
    city = Column(String(60), nullable= False)
    state = Column(String(60), nullable = False)
    zipCode = Column(String(10), nullable = False)
    # One locations can be owner by multiple campaigns
    locations_relation = relationship('CampaignLocation', backref = "locations") 

    def __init__(self, number, street, unit, city, state, zipCode):
        self.number = number
        self.street = street
        self.unit = unit
        self.city = city
        self.state = state
        self.zipCode = zipCode

class CampaignUser(Base):   #Association Table (Campaign + Users)
    __tablename__ = 'campaign_users'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    role_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_id, role_id) # one person + one campaign 


class CampaignLocation(Base):   #Association Table (Campaign + Locations)
    __tablename__ = 'campaign_locations'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    location_id = Column(Integer, ForeignKey('locations.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_id, location_id) # one person + one campaign 

class GlobalVariables(Base):
    __tablename__ = 'globals'
    id = Column(Integer, primary_key=True)
    workDayLength = Column(Integer, default = 1, nullable =False)
    averageSpeed = Column(Float, default = 0.5, nullable = False)

    def __init__(self, workDayLength, averageSpeed):
        self.workDayLength = workDayLength
        self.averageSpeed = averageSpeed

class CanAva(Base):
    __tablename__='canvas_availability'   
    id = Column(Integer,primary_key = True)
    title = Column(String(80),nullable = False)
    start = Column(String(80),nullable = False)
    end = Column(String(80),nullable = False)
    allDay = Column(String(80),nullable = False)
    email=Column(String(80), nullable=False) #User's email

    def __init__(self,title,start,end,allDay,email):
        self.title = title
        self.start = start
        self.end = end
        self.allDay = allDay
        self.email = email
    


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
    role = Role('User1','admin')
    role1= Role('User2','manager')
    role2= Role('User1','manager')
    
    user1.users_relation=[role, role2]
    user2.users_relation.append(role1)
    db_session.commit()
    campaign1 = Campaign("sell compaing", "for test", "question1; qeustion2", 1)
    campaign2 = Campaign("election compaing", "for test", "question1; qeustion2", 2)

    location1 = Location(1, "street", "unit", "city", "state", "1111")
    location2 = Location(2, "street2", "unit2", "city2", "state2", "1211")

    test= CampaignUser()  #user1 + campaign1
    test2= CampaignUser() # user1 + campaign2
    test3 = CampaignUser() # user2+ campaign1

    testL1= CampaignLocation() # location1 + campaign1
    testL2 = CampaignLocation() # location2 + campaign1
    testL3 = CampaignLocation() # location2 + campaign2

    role2.roles_relation = [test,  test2]
    role1.roles_relation.append(test3)

    location2.locations_relation =[testL3, testL2]
    location1.locations_relation.append(testL1)

    campaign1.campaigns_relation = [test, test3]
    campaign2.campaigns_relation.append(test2)

    campaign1.campaigns_relation_1 = [testL1, testL2]
    campaign2.campaigns_relation_1.append(testL3)


    db_session.commit()
    glo = GlobalVariables(1, 1)
    db_session.add(glo)
    db_session.commit()

