from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Boolean, Float, String, Date, Text, ForeignKey, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from datetime import date
import pymysql

#database connection string example
#'mysql+pymysql://username:password@address:port/databaseName'
#connect to the database with the database connection string
engine = create_engine('mysql+pymysql://root:1969@localhost:3306/cse308', convert_unicode=True)
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
    users_relation = relationship('Role', backref='users')

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
    talking = Column(Text, default="None", nullable= False) # defautl = None 
    questionairs = Column(Text, nullable= True)  # question1;question2;....
    durations = Column(Integer, default = 0, nullable=False) # default = 0
    campaigns_relation= relationship("CampaignManager", backref = "campaigns")
    campaigns_relation_2= relationship("CampaignLocation", backref = "campaigns")
    campaigns_relation_1= relationship("CampaignCanvasser", backref = "campaigns")

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
    roles_relation = relationship("CampaignManager", backref= "roles")
    roles_relation_1 = relationship("CampaignCanvasser", backref= "roles")
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

class CampaignManager(Base):   #Association Table (Campaign + Manager)
    __tablename__ = 'campaign_Manager'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    role_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_id, role_id) # one manager + one campaign 


class CampaignCanvasser(Base):   #Association Table (Campaign + User)
    __tablename__ = 'campaign_Canvasser'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    role_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_id, role_id) # one canvasser + one campaign 



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
    averageSpeed = Column(Integer, default = 1, nullable = False)

    def __init__(self, workDayLength, averageSpeed):
        self.workDayLength = workDayLength
        self.averageSpeed = averageSpeed
    

#for populating the database for testing purposes
if __name__ == "__main__":
    init_db()
    p1 = generate_password_hash('password')
    user1 =User('user1@c.com', p1, 'User1')
    user2 = User('user2@c.com', p1, 'User2')
    user3 = User('user3@c.com', p1, 'User3')
    db_session.add(user1)
    db_session.add(user2)
    db_session.add(user3)
    db_session.commit()
    role = Role('User1','admin')
    role1= Role('User2','manager')
    role5 = Role('User2', 'canvasser')
    role2= Role('User1','manager')
    role3= Role('User3', 'canvasser')
    role4 = Role('User3', 'manager')
    
    user1.users_relation=[role, role2] # user1 = admin + manager
    user2.users_relation=[role1, role5] # user2 = manager + canvasser
    user3.users_relation= [role3, role4]  # user3 = canvasser+ manager
    db_session.commit()

    campaign1 = Campaign("sell compaing", "for test", "question1; qeustion2", 1)
    campaign2 = Campaign("election compaing", "for test", "question1; qeustion2", 2)
    db_session.add(campaign1)
    db_session.add(campaign2)
    db_session.commit()

    location1 = Location(1, "street", "unit", "city", "state", "1111")
    location2 = Location(2, "street2", "unit2", "city2", "state2", "1211")
    db_session.add(location1)
    db_session.add(location2)
    db_session.commit()

    test= CampaignManager()  #user3 + campaign1 + manager -->  role4
    test2= CampaignManager() # user2 + campaign2 +manager  --> role1

    role1.roles_relation.append(test2) # manager + role1
    role4.roles_relation.append(test) # manager + role4

    campaign1.campaigns_relation.append(test) # manager + campaign1
    campaign2.campaigns_relation.append(test2) # manager + campaign2

    testC= CampaignCanvasser()  #user3 + campaign1 + canvasser ---> role3
    testC2= CampaignCanvasser() # user1 + campaign2 + canvasser ---> role2

    role3.roles_relation_1.append(testC) # canvasser + role3
    role2.roles_relation_1.append(testC2) # canvasser+ role2

    campaign1.campaigns_relation.append(testC) # canvasser + campaign1
    campaign2.campaigns_relation.append(testC2) # canvasser + campaing2

    testL1= CampaignLocation() # location1 + campaign1
    testL2 = CampaignLocation() # location2 + campaign1
    testL3 = CampaignLocation() # location2 + campaign2

    location2.locations_relation =[testL3, testL2]
    location1.locations_relation.append(testL1)

    campaign1.campaigns_relation_2 = [testL1, testL2]
    campaign2.campaigns_relation_2.append(testL3)


    db_session.commit()
    glo = GlobalVariables(1, 1)
    db_session.add(glo)
    db_session.commit()


