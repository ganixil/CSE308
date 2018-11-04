from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Campaign, Role,CampaignLocation,CampaignCanvasser, CampaignManager, Questionnaire
from gmap import key
import googlemaps



class DateObject():
	def __init__(self, date, canEmail, dateId):
		self.date = date
		self.canEmail = canEmail
		self.dateId = dateId

class assignmentMapping():
	def __init__(self, date, canEmail, dateId, assignment):
		self.date = date
		self.canEmail = canEmail
		self.dateId = dateId
		self.assignment = assignment

#link google map
gmaps = googlemaps.Client(key = key)
#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/create_campaign', methods=['GET','POST'])
def createCampaign():
	managerObject = db_session.query(Role).filter(Role.role =='manager')

	manager_email =[]
	for m in managerObject:
		manager_email.append(m.email)

	manager_name = []
	for e in manager_email:
		manager_name.append(db_session.query(User).filter(User.email==e).first().name)


	canvasObject  = db_session.query(Role).filter(Role.role == 'canvasser')

	canvasser_email=[]
	for c in canvasObject:
		canvasser_email.append(c.email)

	canvasser_name = []
	for e in canvasser_email:
		canvasser_name.append(db_session.query(User).filter(User.email==e).first().name)

	campaignObject = db_session.query(Campaign)
	if request.method == 'POST':
		


		################################################Create a campaign 
		campaignName = request.form['campaign_name']
		startdate = request.form['start_date']
		enddate = request.form['end_date']
		talking = request.form['talking']
		duration = request.form['duration']

		campObj = Campaign(campaignName, startdate, enddate, talking,int(duration))
		db_session.add(campObj)

		####################################################ADD Manager to database
		managers = request.form.getlist('flaskManager')
		
		for m in managers:
			nameObj = db_session.query(User).filter(User.name == m).first()
			role = db_session.query(Role).filter(Role.role == 'manager',  Role.email == nameObj.email).first()
			mObject = CampaignManager()
			role.roles_relation.append(mObject)
			campObj.campaigns_relation.append(mObject)
		####################################################ADD Canvasser to database
		canvassers = request.form.getlist('flaskCanvasser')

		for c in canvassers:
			nameObj = db_session.query(User).filter(User.name == c).first()
			role = db_session.query(Role).filter(Role.role == 'canvasser',  Role.email == nameObj.email).first()
			cObject = CampaignCanvasser()
			role.roles_relation_1.append(cObject)
			campObj.campaigns_relation_1.append(cObject)
		####################################################ADD Location to database
		locations = request.form.getlist('flaskLocation')
		for l  in locations:
			lat = gmaps.geocode(l)[0]['geometry']['location']['lat']
			lng = gmaps.geocode(l)[0]['geometry']['location']['lng']
			loc = CampaignLocation(l,lat,lng,None)
			campObj.campaigns_relation_2.append(loc)
			db_session.commit()

		####################################################ADD question to database
		questions = request.form.getlist('flaskQuestion')
		for q in questions:
			ques = Questionnaire(q)
			campObj.campaigns_relation_3.append(ques)
			db_session.commit()


		db_session.commit()
	else:
		return render_template('manager_html/create_campaign.html', managers=manager_name, canvasser=canvasser_name)

	return render_template('manager_html/view_campaign.html', camp=campaignObject)



@bp.route('/show_campaign',methods=('POST','GET'))
def showCampaign():
	if request.method == "POST":

		try:
			if request.form['submit_btn'] == 'submit_form':
				print("POST_SUBMIT_-------------------0")
				#Update old Campaign name
				oldCamp = db_session.query(Campaign).filter(Campaign.campaign_name ==  request.form['scampaign_name']).first()
				oldCamp.campaign_name = request.form['new_campaign_name']
				db_session.commit()
				print("POST_SUBMIT_-------------------1")
				#Remove all manager asociated with Old Campaign
				db_session.query(CampaignManager).filter(CampaignManager.campaign_id == oldCamp.id).delete()
				db_session.commit()
				print("POST_SUBMIT_-------------------2")
				#Add new managers to Old campaign
				newManagers = request.form.getlist('flaskManager')
				for m in newManagers:
					nameObj = db_session.query(User).filter(User.name == m).first();
					role = db_session.query(Role).filter(Role.role == 'manager',  Role.email== nameObj.email).first()
					mObject = CampaignManager()
					role.roles_relation.append(mObject)
					oldCamp.campaigns_relation.append(mObject)
					db_session.commit()
				print("POST_SUBMIT_-------------------2")
				#Remove all canvasser asociated with Old Campaign
				db_session.query(CampaignCanvasser).filter(CampaignCanvasser.campaign_id == oldCamp.id).delete()
				db_session.commit()

				#Add new canvasser to Old campaign
				newCanvassers = request.form.getlist('flaskCanvasser')
				for c in newCanvassers:
					nameObj = db_session.query(User).filter(User.name == c).first()
					role = db_session.query(Role).filter(Role.role=='canvasser', Role.email == nameObj.email).first()
					cObject = CampaignCanvasser()
					role.roles_relation_1.append(cObject)
					oldCamp.campaigns_relation_1.append(cObject)
					db_session.commit()


				#Update new start and enddate, talking, duration
				startdate = request.form['start_date']
				enddate = request.form['end_date']
				talking = request.form['talking']
				duration = request.form['duration']

				oldCamp.startDate = startdate
				oldCamp.endDate = enddate
				oldCamp.talking = talking
				oldCamp.duration = duration


				#Remove all location associated with campaign
				db_session.query(CampaignLocation).filter(CampaignLocation.campaign_id == oldCamp.id).delete()
				db_session.commit()

				#Add new locations to old oldCampaign
				locations = request.form.getlist('flaskLocation')

				for l in locations:
					loc = CampaignLocation(l,None,None,None)
					oldCamp.campaigns_relation_2.append(loc)
					db_session.commit()
				
				#Remove all questions
				db_session.query(Questionnaire).filter(Questionnaire.campaign_id == oldCamp.id).delete()
				db_session.commit()

				#Add new questions
				questions = request.form.getlist('flaskQuestion')
				for q in questions:
					ques = Questionnaire(q)
					oldCamp.campaigns_relation_3.append(ques)
					db_session.commit()


				db_session.commit()

				campaignObject = db_session.query(Campaign)
				return render_template('manager_html/view_campaign.html', camp=campaignObject)
				
		except:
			#Display all information after creating a campaign in EDIT CAMPAIGN
			managerObject = db_session.query(Role).filter(Role.role =='manager')
			canvasObject  = db_session.query(Role).filter(Role.role == 'canvasser')
			

			campaignName = request.form['new_campaign_name']
			campaignObject = db_session.query(Campaign)

			campId = None
			start=None
			end=None
			
			for camp in campaignObject:
				if camp.campaign_name == campaignName:
					campId = camp.id
					start = camp.startDate
					end= camp.endDate
					break
			
			roleList = db_session.query(Role)
			
			#############################################   Display All Current Manager in table
			currentManagers = db_session.query(CampaignManager)
			managerId = []
			for man in currentManagers:
				if man.campaign_id == campId:
					managerId.append(man.user_id)
			
			displayManagers=[]
			for r in roleList:
				if r.id in managerId:
					nameObj = db_session.query(User).filter(User.email== r.email).first();
					displayManagers.append(nameObj.name)

			############################################	 Display All Current Canvasser in table 
			currentCanvassers = db_session.query(CampaignCanvasser)
			canvasId = []
			for can in currentCanvassers:
				if can.campaign_id == campId:
					canvasId.append(can.user_id)
			

			displayCanvas=[]
			for r in roleList:
				if r.id in canvasId:
					nameObj = db_session.query(User).filter(User.email== r.email).first();
					displayCanvas.append(nameObj.name)
			
			############################################	 Display All Manager in selector
			allMan = []
			roleList = db_session.query(Role).filter(Role.role =='manager')

			for r in roleList:
				userObj = db_session.query(User).filter(User.email == r.email).first()
				allMan.append(userObj.name)

			############################################	 Display All Canvasser in selector		
			allCan = []
			roleList = db_session.query(Role).filter(Role.role == 'canvasser')

			for r in roleList:
				userObj = db_session.query(User).filter(User.email == r.email).first()
				allCan.append(userObj.name)

			############################################	 Display All Question in table

			currentQuestions = db_session.query(Questionnaire)
			displayQuestion = []
			for q in currentQuestions:
				if q.campaign_id == campId:
					displayQuestion.append(q.question)

			############################################	 Display current Location in table
			currentLocations = db_session.query(CampaignLocation)
			displayLocation = []
			for l in currentLocations:
				if l.campaign_id == campId:
					displayLocation.append(l.location)
			print("Locations for this campaign is : ",displayLocation)


			############################################	 Display current talking point in table
			talkObj = db_session.query(Campaign).filter(Campaign.id == campId).first().talking
			print("Taking----------> ", talkObj)

			durationObj = db_session.query(Campaign).filter(Campaign.id == campId).first().duration
			print("Duration is" , durationObj)
																	       # campaign questions
			return render_template('manager_html/edit_campaign.html', duration= durationObj, talk=talkObj,locations=displayLocation,questions=displayQuestion, camp=campaignObject, show=campaignName, managers=allMan, canvasser=allCan, currentManagers=displayManagers, currentCanvassers=displayCanvas,start=start, end=end)


####################################################################################### CONOR's CODE#######################################################


@bp.route('/create_canvas_assignment', methods=('GET', 'POST'))
def createCanvasAssignment():
	if request.method == 'POST':
		# flag for marking the assignment the campaign as possible
		assignmentPossible = False
		# get headquarters for starting location for routing algorithm
		globalVars = db_session.query(GlobalVariables).first()
		hq = (globalVars.hqX, globalVars.hqY)
		campName = request.form['name'] #for getting the campaign name
		# get campaign data
		campObj = db_session.query(Campaign).filter(Campaign.campaign_name == campName)
		# get campaign location data
		dbLocations = db_session.query(CampaignLocation).filter(CampaignLocation.campaign_id == campObj.id)
		locations = []
		# add the headquarters to the location set
		locations.append(hq)
		# add all campaign locations to the locations set
		for i in range(len(dbLocations)):
			locations.append((dbLocations[i].x, dbLocations[i].y))
		# make assignments with the routing alorithm
		assignments = makeAssign(locations)
		# get the campaign's canvassers
		canvassers = campObj.campaigns_relation_1
		ids = []
		dates = []
		# get the start and end dates of the campaign
		startDate = campObj.startDate
		endDate = campObj.endDate
		# collect the available dates of each canvasser in the campaign
		for i in range(len(canvassers)):
			cEmail = canvassers[i].user_email # need to modify DB
			canDates = db_session.query(CanAva).filter(CanAva.email == cEmail).all()
			for j in range(len(canDates)):
				# filter out dates not in the campaign range
				if(canDates.theDate > startDate and canDates.theDate < endDate):
					dates.append(DateObject(canDates.theDate, canDates.email, canDates.id))
					#ids.append(canvassers.user_id)
		# sort dates by earliest available using bubble sort
		sortComplete = 0
		while(sortComplete == 0):
			sortComplete = 1
			for i in range(len(dates)):
				if(i != (len(dates)-1)):

					if(dates[i].date > dates[i+1].date):

						temp = dates[i+1]
						dates[i+1] = dates[i]
						dates[i] = temp
						sortComplete = 0

		# assign assignments to dates
		mappedAssignments = []
		while(len(dates) > 0 and len(assignments > 0)):
			dTemp = dates.pop(0)
			aTemp = assignments.pop(0)
			mappedAssignments.append(assignmentMapping(dTemp.date, dTemp.canEmail, dTemp.dateId, aTemp))
		# if no more assingments then this mapping is possible
		if(len(assignments) == 0):
			assignmentPossible = True

		if(assignmentPossible == False):
			return 'not possible'
			# if not enough dates/canvassers display warning

		for i in range(len(mappedAssignments)):

			for j in range:
				pass
				
	return render_template('manager_html/create_canvas_assignment.html')


@bp.route('/view_canvas_assignment')
def viewCanvasAssignment():
	result = 1;
	return render_template('manager_html/view_canvas_assignment.html');

#function to render the manager page and set the manager page url
@bp.route('/manpage', methods=('GET', 'POST'))
def manPage():
	campaignObject = db_session.query(Campaign)
	return render_template('manager_html/view_campaign.html', camp=campaignObject)
	
@bp.route('/view_campaign')
def viewCampaign():
	campaignObject = db_session.query(Campaign)
	return render_template('manager_html/view_campaign.html', camp=campaignObject)

#UPDATE THIS ROUTE STATEMENT
@bp.route('/view_campaign_result')
def viewCampaignResult():
	result = 1
	return render_template('manager_html/view_campaign_result.html')


@bp.route('/edit_campaign')
def editCampaign():
	campaignObject = db_session.query(Campaign)

	return render_template('manager_html/edit_campaign.html', camp=campaignObject)
