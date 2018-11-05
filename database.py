from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Boolean, Float, String, Date, Text, ForeignKey, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from datetime import date
import pymysql

# Database connection string example
# 'mysql+pymysql://username:password@address:port/databaseName'
# Connect to the database with the database connection string
engine = create_engine('mysql+pymysql://xiangyiliu:111308288@mysql3.cs.stonybrook.edu:3306/xiangyiliu', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
# Make the sqlalchemy object relation mapper base class
Base = declarative_base()
Base.query = db_session.query_property()


# Function to initalize the database
def init_db():
    Base.metadata.create_all(bind=engine)


# Database table models/object relational classes
class User(Base):
    __tablename__ = 'users'

    email = Column(String(80), primary_key=True)
    password = Column(String(255), nullable=False)
    name = Column(String(80), nullable=False)
    avatar = Column(String(80), nullable=True)
    users_relation = relationship('Role', backref='users')

    def __init__(self,email, password, name,avatar):
        self.email = email
        self.password = password
        self.name = name
        self.avatar = avatar

    def __repr__(self):
        return "<User(email='%s', password='%s')>" % (self.email, self.password)


class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key = True)
    campaign_name = Column(String(80), nullable = False)  # One company with a unique name
    startDate = Column(String(30), nullable=False)
    endDate = Column(String(30), nullable=False)
    talking = Column(String(80), default="None", nullable= True) # defautl = None 
    duration = Column(Integer, default = 0, nullable=True) # default = 0
    campaigns_relation= relationship("CampaignManager", backref = "campaigns",cascade="all,save-update,delete-orphan")
    campaigns_relation_1= relationship("CampaignCanvasser", backref = "campaigns",cascade="all,save-update,delete-orphan")
    campaigns_relation_2= relationship("CampaignLocation", backref = "campaigns",cascade="all,save-update,delete-orphan")
    campaigns_relation_3=relationship("Questionnaire",backref="campaigns",cascade="all,save-update,delete-orphan")

    def __init__(self, campaign_name, startDate, endDate,talking,duration):
        self.campaign_name = campaign_name
        self.startDate = startDate
        self.endDate = endDate
        self.talking = talking
        self.duration = duration

class Questionnaire(Base):
    __tablename__ = 'questionnaire'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE"))
    question = Column(String(80),nullable = False)

    def __init__(self, question):
       self.question = question

class Role(Base):  # One user can have many role : one to many
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    email=Column(String(80), ForeignKey('users.email', onupdate="CASCADE", ondelete="CASCADE")) #User's email
    role= Column(String(20), nullable=False)
    # One role can work on multiple campaigns
    roles_relation = relationship("CampaignManager", backref= "roles",cascade="all,save-update,delete-orphan")
    roles_relation_1 = relationship("CampaignCanvasser", backref= "roles",cascade="all,save-update,delete-orphan")
    UniqueConstraint(email, role)

    # A collection of roles on User
    def __init__(self, role):
        self.role = role
    
    def __repr__(self):
        return "<Role(email='%s',role='%s')>" % (self.email,self.role)

        
class CampaignLocation(Base):   # Association Table (Campaign + Locations)
    __tablename__ = 'campaign_locations'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    location = Column(String(80),nullable=False)
    x = Column(Float,nullable = True)
    y = Column(Float,nullable = True)
    canvasser_email = Column(String(80),nullable = True)
    UniqueConstraint(campaign_id, location)

    def __init__(self,  location, x, y, canvasser_email):
        self.location = location
        self.x = x
        self.y = y
        self.canvasser_email = canvasser_email

class CampaignManager(Base):   # Association Table (Campaign + Manager)
    __tablename__ = 'campaign_Manager'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    user_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_id, user_id) # one manager + one campaign 


class CampaignCanvasser(Base):   # Association Table (Campaign + User)
    __tablename__ = 'campaign_Canvasser'
    id = Column(Integer, primary_key = True)
    campaign_id = Column(Integer,ForeignKey('campaigns.id', onupdate="CASCADE", ondelete="CASCADE") )
    user_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_id, user_id) # one canvasser + one campaign 





class GlobalVariables(Base):
    __tablename__ = 'globals'
    id = Column(Integer, primary_key=True)
    workDayLength = Column(Integer, default = 1, nullable =False)
    averageSpeed = Column(Float, default = 1, nullable = False)
    hqX = Column(Float)
    hqY = Column(Float)

    def __init__(self, workDayLength, averageSpeed, hqX, hqY):
        self.workDayLength = workDayLength
        self.averageSpeed = averageSpeed
        self.hqX = hqX
        self.hqY = hqY

class CanAva(Base):
    __tablename__='canvas_availability'   
    id = Column(Integer,primary_key = True)
    #title = Column(String(80),nullable = False)
    #start = Column(String(80),nullable = False)
    #end = Column(String(80),nullable = False)
    #allDay = Column(String(80),nullable = False)
    theDate = Column(Date)

    email=Column(String(80), nullable=False) # User's email

    def __init__(self,title, theDate,email):
        self.title = title
        self.theDate = theDate  
        self.email = email

class Assignment(Base):
    __tablename__='assignment'
    id = Column(Integer, primary_key = True)
    theDate = Column(Date)
    x = Column(Float)
    y = Column(Float)
    email = Column(String(80))
    order = Column(Integer)
    def __init__(self, theDate, x, y, email, order):
        self.theDate = theDate
        self.x = x
        self.y = y
        self.email = email
        self.order = order


# For populating the database for testing purposes.
if __name__ == "__main__":
    init_db()
    p1 = generate_password_hash('password')
    user1 =User('user1@c.com', p1, 'User1', 'user1.jpg')
    user2 = User('user2@c.com', p1, 'User2','user2.png')
    user3 = User('user3@c.com', p1, 'User3','')
    user4 = User('user4@c.com', p1, 'User4','')
    db_session.add(user1)
    db_session.add(user2)
    db_session.add(user3)
    db_session.add(user4)

    role = Role('admin')
    role1= Role('manager')
    role2 = Role('canvasser')
    role3= Role('manager')
    role4= Role('canvasser')
    role5 = Role('manager')
    role6 = Role('admin')
    role7 = Role('canvasser')
    role8 = Role('manager')

    user1.users_relation=[role, role1] # user1 = admin + manager
    user2.users_relation=[role2, role3] # user2 = manager + canvasser
    user3.users_relation= [role4, role5]  # user3 = canvasser+ manager
    user4.users_relation=[role6, role7, role8] # user4 = admin +  canvasser + manager


    campaign1 = Campaign("sell compaing1", "1/1" , "2/2","talk something","5")
    campaign2 = Campaign("election compaing2", "1/1", "2/2","say something","5")
    db_session.add(campaign1)
    db_session.add(campaign2)


    campM1= CampaignManager() # (role1 + campaign1  
    campM2= CampaignManager() # (role8 + campaign1
    campM3= CampaignManager() # (role3 + campaign2    
    campM4= CampaignManager() # (role5 + campaign2   

    role1.roles_relation.append(campM1) 
    role8.roles_relation.append(campM1) 
    role3.roles_relation.append(campM2) 
    role5.roles_relation.append(campM2) 

    campaign1.campaigns_relation.append(campM1) 
    campaign1.campaigns_relation.append(campM2)
    campaign2.campaigns_relation.append(campM2)
    campaign2.campaigns_relation.append(campM2)


    campCan1= CampaignCanvasser()  # (role2 + campaign1)  --->user2
    campCan2= CampaignCanvasser() # (role4 + campaign2)  ---> user3 
    campCan3= CampaignCanvasser()  # (role2  + campaign2)  --->user1
    campCan4= CampaignCanvasser() #  (role7 + campaign2)  ---> user4

    role2.roles_relation_1.append(campCan1)
    role4.roles_relation_1.append(campCan2)  
    role2.roles_relation_1.append(campCan3) 
    role7.roles_relation_1.append(campCan4) 

    campaign1.campaigns_relation_1.append(campCan1) 
    campaign2.campaigns_relation_1.append(campCan2) 
    campaign2.campaigns_relation_1.append(campCan3)
    campaign2.campaigns_relation_1.append(campCan4)


    testL1= CampaignLocation("street1",None,None,None) # location1 + campaign1
    testL2 = CampaignLocation("street2",None,None,None) # location2 + campaign1
    testL3 = CampaignLocation("street3",None,None,None) # location2 + campaign2

    campaign1.campaigns_relation_2 = [testL1, testL2]
    campaign2.campaigns_relation_2.append(testL3)

    glo = GlobalVariables(1, 1,1,1)
    db_session.add(glo)
    
    db_session.commit()




