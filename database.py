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

''' Database table models/object relational classes'''

class User(Base):
    __tablename__ = 'users'

    email = Column(String(80), primary_key=True)
    password = Column(String(255), nullable=False)
    name = Column(String(80), nullable=False)
    avatar = Column(String(80), nullable=True, default ="None")
    ##########  One User Can Have Multiple Roles(Canvasser, Admin, Managers)
    users_relation = relationship('Role', backref='users', cascade="all,save-update,delete-orphan", lazy = True)

    def __init__(self,email, password, name,avatar):
        self.email = email
        self.password = password
        self.name = name
        self.avatar = avatar

    def __repr__(self):
        return "<User(email='%s', password='%s', avatar='%s')>" % (self.email, self.password, self.avatar)


class Role(Base): 
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    email=Column(String(80), ForeignKey('users.email', onupdate="CASCADE", ondelete="CASCADE")) #User's email
    role= Column(String(20), nullable=False)  ####### (canvasser, manager, admin)

    ################## Only manager role has this relationship, it refers to one or multiple campaings##############
    roles_relation = relationship("CampaignManager", backref= "roles",cascade="all,save-update, delete-orphan")
    ################## Only canvasser role has this relationship, it refers to one or multiple campaings##############
    roles_relation_1 = relationship("CampaignCanvasser", backref= "roles",cascade="all,save-update,delete-orphan")
    ################## Only canvasser role has this relationship, it refers to one or one on its available dates ##############
    roles_relation_2 = relationship("CanAva", backref= "roles",cascade="all,save-update,delete-orphan")

    UniqueConstraint(email, role)  

    # A collection of roles on User
    def __init__(self, role):
        self.role = role
    
    def __repr__(self):
        return "<Role(email='%s',role='%s')>" % (self.email,self.role)


class Campaign(Base):
    __tablename__ = 'campaigns'

    name = Column(String(80),  primary_key = True) 
    startDate = Column(Date, nullable=False)  ##  Formart = 2018-11-11
    endDate = Column(Date, nullable=False)
    talking = Column(Text, default="None", nullable= True) 
    duration = Column(Integer, default = 0, nullable=True)

    ########## One Campaign has multiple Managers##############
    campaigns_relation= relationship("CampaignManager", backref = "campaigns",cascade="all,save-update,delete-orphan")
    ######### One Campaign has multiple Canvassers################
    campaigns_relation_1= relationship("CampaignCanvasser", backref = "campaigns",cascade="all,save-update,delete-orphan")
    ########## One campaign has multiple Locations###################
    campaigns_relation_2= relationship("CampaignLocation", backref = "campaigns",cascade="all,save-update,delete-orphan")
    ######### One campaign has multiple questions############
    campaigns_relation_3=relationship("Questionnaire",backref="campaigns",cascade="all,save-update,delete-orphan")

    def __init__(self, name, startDate, endDate,talking,duration):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.talking = talking
        self.duration = duration

    def __repr__(self):
        return "<Campaign(name='%s', startDate='%s', endDate='%s')>" % (self.name, self.startDate, self.endDate)


class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    id = Column(Integer, primary_key = True)
    campaign_name = Column(String(80),ForeignKey('campaigns.name', onupdate="CASCADE", ondelete="CASCADE"))
    question = Column(String(100),nullable = False)

    def __init__(self, question):
       self.question = question

    def __repr__(self):
        return "<Questionnaire(Campaign name='%s', question='%s', endDate='%s')>" % (self.campaign_name, self.question)

    
class CampaignLocation(Base):   # Association Table (Campaign + Locations)
    __tablename__ = 'campaign_locations'

    id = Column(Integer, primary_key = True)
    campaign_name = Column(String(80),ForeignKey('campaigns.name', onupdate="CASCADE", ondelete="CASCADE") )
    location = Column(String(80),nullable=False)
    lat = Column(Float,nullable = False)
    lng = Column(Float,nullable = False)

    location_relation=relationship("Assignment", backref="campaign_locations",cascade="all,save-update,delete-orphan")

    UniqueConstraint(campaign_name, location)

    def __init__(self,  location, lat, lng):
        self.location = location
        self.lat= lat
        self.lng = lng

    def __repr__(self):
        return "<Locations(Campaign name='%s', location='%s' lat ='%s')>" % (self.campaign_name, self.location, self.lat)



class CampaignManager(Base):   # Association Table (Campaign + ManagerRole)
    __tablename__ = 'campaign_managers'

    id = Column(Integer, primary_key = True)
    campaign_name = Column(String(80),ForeignKey('campaigns.name', onupdate="CASCADE", ondelete="CASCADE") )
    role_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    UniqueConstraint(campaign_name, role_id) 

    def __repr__(self):
        return "<Managers(Campaign name='%s', role_id='%s')>" % (self.campaign_name, self.role_id)


class CampaignCanvasser(Base):   # Association Table (Campaign + CanvasserRole)
    __tablename__ = 'campaign_canvassers'

    id = Column(Integer, primary_key = True)
    campaign_name = Column(String(80),ForeignKey('campaigns.name', onupdate="CASCADE", ondelete="CASCADE") )
    role_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))

    canvasser_relation=relationship("Assignment", backref="campaign_canvassers",cascade="all,save-update,delete-orphan")

    UniqueConstraint(campaign_name, role_id) # one canvasser + one campaign 

    def __repr__(self):
        return "<Canvassers(Campaign name='%s', role_id='%s')>" % (self.campaign_name, self.role_id)


class GlobalVariables(Base):
    __tablename__ = 'globals'

    id = Column(Integer, primary_key=True)
    workDayLength = Column(Integer, default = 1, nullable =False)
    averageSpeed = Column(Float, default = 1, nullable = False)
    hqX = Column(Float, nullable=False)
    hqY = Column(Float, nullable =False)

    def __init__(self, workDayLength, averageSpeed, hqX, hqY):
        self.workDayLength = workDayLength
        self.averageSpeed = averageSpeed
        self.hqX = hqX
        self.hqY = hqY

    def __repr__(self):
        return "<GlobalVariables(workDayLength='%d', averageSpeed='%f')>" % (self.workDayLength, self.averageSpeed)


class CanAva(Base):
    __tablename__='can_avas'  

    id = Column(Integer,primary_key = True)
    role_id = Column(Integer, ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"))
    theDate = Column(Date, nullable= False)
    UniqueConstraint(role_id, theDate)

    def __init__(self,theDate):
        self.theDate = theDate  

    def __repr__(self):
        return "<CanAva(role_id='%d', theDate='%s')>" % (self.role_id, self.theDate)


class Assignment(Base):
    __tablename__='assignments'

    id = Column(Integer, primary_key = True)
    canvasser_id = Column(Integer, ForeignKey('campaign_canvassers.id', onupdate="CASCADE", ondelete="CASCADE"))
    location_id = Column(Integer, ForeignKey('campaign_locations.id', onupdate="CASCADE", ondelete="CASCADE"))
    theDate = Column(Date, nullable= False)
    order = Column(Integer, nullable = False)

    def __init__(self, theDate,order):
        self.theDate = theDate
        self.order = order

    def __repr__(self):
        return "<Assignment(location_id='%d', canvasser_id='%s', theDate='%s', order='%d')>" % (self.location_id, self.canvasser_id, self.theDate, self.order)


# For populating the database for testing purposes.
if __name__ == "__main__":
    init_db()
    p1 = generate_password_hash('password')
    user1 =User('user1@c.com', p1, 'User1', 'user1.jpg')
    user2 = User('user2@c.com', p1, 'User2','user2.png')
    user3 = User('user3@c.com', p1, 'User3', None)
    user4 = User('user4@c.com', p1, 'User4', None)
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

    canAva_1 = CanAva('2018-11-15')
    canAva_2 = CanAva('2018-11-16')
    canAva_3 = CanAva('2018-11-16')
    canAva_4 = CanAva('2018-11-17')

    role4.roles_relation_2.append(canAva_1)
    role4.roles_relation_2.append(canAva_2)

    role7.roles_relation_2.append(canAva_3)
    role7.roles_relation_2.append(canAva_4)


    campaign1 = Campaign("sell compaing1", "2018-11-1" , "2018-11-20","talk something",5)
    campaign2 = Campaign("election compaing2", "2018-11-5", "2018-11-25","say something",5)
    db_session.add(campaign1)
    db_session.add(campaign2)


    campM1= CampaignManager() # (role1 + campaign1 ) ---user1
    campM2= CampaignManager() # (role8 + campaign1) ---- user4
    campM3= CampaignManager() # (role3 + campaign2)  ---- user2
    campM4= CampaignManager() # (role5 + campaign2)  ---- user3

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


    location1= CampaignLocation("Stony Brook University, Nicolls Road, Stony Brook, NY, USA",40.915089,-73.115936) # location1 + campaign1
    location2 = CampaignLocation("39 FAWN LN N SOUTH SETAUKET NY 11720", 40.900930,-73.072380) # location2 + campaign1
    location3 = CampaignLocation("160 Mark Tree Road, Centereach, NY",40.867069,-73.085403) # location2 + campaign1
    campaign1.campaigns_relation_2.append(location1)
    campaign1.campaigns_relation_2.append(location2)
    campaign1.campaigns_relation_2.append(location3)

    location4= CampaignLocation("Stony Brook University, Nicolls Road, Stony Brook, NY, USA",40.915089,-73.115936) # location1 + campaign2
    location5 = CampaignLocation("39 FAWN LN N SOUTH SETAUKET NY 11720", 40.900930,-73.072380) # location2 + campaign2
    location6 = CampaignLocation("160 Mark Tree Road, Centereach, NY",40.867069,-73.085403) # location2 + campaign2
    campaign2.campaigns_relation_2.append(location4)
    campaign2.campaigns_relation_2.append(location5)
    campaign2.campaigns_relation_2.append(location6)


    glo = GlobalVariables(1,1,1,1)
    db_session.add(glo)
    
    db_session.commit()




