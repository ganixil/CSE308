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
    campaign_name = Column(String(80), nullable = False)  # One company with a unique name
    startDate = Column(String(30), nullable=False)
    endDate = Column(String(30), nullable=False)
    
    # talking = Column(Text, default="None", nullable= False) # defautl = None 
    # questionairs = Column(Text, nullable= True)  # question1;question2;....
    # durations = Column(Integer, default = 0, nullable=False) # default = 0
    campaigns_relation= relationship("CampaignManager", backref = "campaigns")
    campaigns_relation_1= relationship("CampaignCanvasser", backref = "campaigns")
    campaigns_relation_2= relationship("CampaignLocation", backref = "campaigns")
    #campaigns_relation_date = relationship("CampaignDate", backref= "campaigns")

    def __init__(self, campaign_name, startDate, endDate):
        self.campaign_name = campaign_name
        self.startDate = startDate
        self.endDate = endDate


class CampaignDate(Base):
    __tablename__ = 'date'
    id = Column(Integer, primary_key =True)
    startDate = Column(String(30), nullable=False)
    endDate = Column(String(30), nullable=False)

    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endaDate


class Role(Base):  # One user can have many role : one to many
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    email=Column(String(80), ForeignKey('users.email', onupdate="CASCADE", ondelete="CASCADE")) #User's email
    name = Column(String(80), nullable = False)
    role= Column(String(20), nullable=False)
    # One role can work on multiple campaigns
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
    # unit = Column(String(60), nullable = True) # Apartment16B
    # city = Column(String(60), nullable= False)
    # state = Column(String(60), nullable = False)
    # zipCode = Column(String(10), nullable = False)
    
    # One locations can be owner by multiple campaigns
    locations_relation = relationship('CampaignLocation', backref = "locations") 

    def __init__(self,  street):
        self.street = street
        

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


class CampaignLocation(Base):   # Association Table (Campaign + Locations)
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


class CanAva(Base):
    __tablename__='canvas_availability'   
    id = Column(Integer,primary_key = True)
    title = Column(String(80),nullable = False)
    start = Column(String(80),nullable = False)
    end = Column(String(80),nullable = False)
    allDay = Column(String(80),nullable = False)
    email=Column(String(80), nullable=False) # User's email

    def __init__(self,title,start,end,allDay,email):
        self.title = title
        self.start = start
        self.end = end
        self.allDay = allDay
        self.email = email   


# For populating the database for testing purposes.
if __name__ == "__main__":
    # init_db()
    # p1 = generate_password_hash('password')
    # user1 =User('user1@c.com', p1, 'User1')
    # user2 = User('user2@c.com', p1, 'User2')
    # user3 = User('user3@c.com', p1, 'User3')
    # user4 = User('user4@c.com', p1, 'User4')
    # db_session.add(user1)
    # db_session.add(user2)
    # db_session.add(user3)
    # db_session.add(user4)

    # campaign1 = Campaign("sell compaing1", "1/1" , "2/2")
    # campaign2 = Campaign("election compaing2", "1/1", "2/2")
    # db_session.add(campaign1)
    # db_session.add(campaign2)

    # location1 = Location( "street")
    # location2 = Location( "street2")
    # location3 = Location( "street3")
    # db_session.add(location1)
    # db_session.add(location2)
    # db_session.add(location3)

    # db_session.commit()

    # role = Role('User1','admin')
    # role1= Role('User1','manager')
    # role2 = Role('User2', 'canvasser')
    # role3= Role('User2','manager')
    # role4= Role('User3', 'canvasser')
    # role5 = Role('User3', 'manager')
    # role6 = Role('User4', 'admin')
    # role7 = Role('User4', 'canvasser')
    # role8 = Role('User4', 'manager')
    
    # user1.users_relation=[role, role1] # user1 = admin + manager
    # user2.users_relation=[role2, role3] # user2 = manager + canvasser
    # user3.users_relation= [role4, role5]  # user3 = canvasser+ manager
    # user4.users_relation=[role6, role7, role8] # user4 = admin +  canvasser + manager



    # campM1= CampaignManager() # (role1 + campaign1  
    # campM2= CampaignManager() # (role8 + campaign1
    # campM3= CampaignManager() # (role3 + campaign2    
    # campM4= CampaignManager() # (role5 + campaign2   

    # role1.roles_relation.append(campM1) 
    # role8.roles_relation.append(campM1) 
    # role3.roles_relation.append(campM2) 
    # role5.roles_relation.append(campM2) 

    # campaign1.campaigns_relation.append(campM1) 
    # campaign1.campaigns_relation.append(campM2)
    # campaign2.campaigns_relation.append(campM2)
    # campaign2.campaigns_relation.append(campM2)




    # campCan1= CampaignCanvasser()  # (role2 + campaign1)  --->user2
    # campCan2= CampaignCanvasser() # (role4 + campaign2)  ---> user3 
    # campCan3= CampaignCanvasser()  # (role2  + campaign2)  --->user1
    # campCan4= CampaignCanvasser() #  (role7 + campaign2)  ---> user4

    # role2.roles_relation_1.append(campCan1)
    # role4.roles_relation_1.append(campCan2)  
    # role2.roles_relation_1.append(campCan3) 
    # role7.roles_relation_1.append(campCan4) 

    # campaign1.campaigns_relation_1.append(campCan1) 
    # campaign2.campaigns_relation_1.append(campCan2) 
    # campaign2.campaigns_relation_1.append(campCan3)
    # campaign2.campaigns_relation_1.append(campCan4)


    # testL1= CampaignLocation() # location1 + campaign1
    # testL2 = CampaignLocation() # location2 + campaign1
    # testL3 = CampaignLocation() # location2 + campaign2


    # location2.locations_relation =[testL3, testL2]  # 
    # location1.locations_relation.append(testL1)

    # campaign1.campaigns_relation_2 = [testL1, testL2]
    # campaign2.campaigns_relation_2.append(testL3)
    # glo = GlobalVariables(1, 1)
    # db_session.add(glo)

    # db_session.commit()
    p1 = generate_password_hash('password')
        
    user1 = User('user1@c.com', p1, 'User1')
    db_session.add(user1)
    role1 = Role('User1', 'canvasser')
    user1.users_relation=[role1]

    user2 = User('user2@c.com', p1, 'User2')
    db_session.add(user2)
    role2 = Role('User2', 'canvasser')
    user2.users_relation=[role2]

    user3 = User('user3@c.com', p1, 'User3')
    db_session.add(user3)
    role3 = Role('User3', 'canvasser')
    user3.users_relation=[role3]
    db_session.commit()




