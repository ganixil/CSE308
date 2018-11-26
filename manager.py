from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Campaign, Role,CampaignLocation,CampaignCanvasser, CampaignManager, Questionnaire, Assignment, GlobalVariables, CanAva
from sqlalchemy.sql.expression import func
from gmap import key
import googlemaps
from assignmentCreator import makeAssign
import datetime
from datetime import date
import math


#link google map
gmaps = googlemaps.Client(key = key)

#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

''' Store All Campaigns Info : Key = campaign Name ; Value = Detail Info the specified Campaign'''
camp = {}

''' Create Assignment for one Campaing'''
def createAssignment(newCamp):
	'''
	newCamp---> campaign Object
	'''
	# flag for marking the assignment the campaign as possible
	assignmentPossible = False

	# get headquarters for starting location for routing algorithm
	globalVars = db_session.query(GlobalVariables).first()
	hq = (globalVars.hqX, globalVars.hqY)
	# get campaign location data
	locations = []
	# add the headquarters to the location set
	locations.append(hq)
	# add all campaign locations to the locations set
	locations_relation = newCamp.campaigns_relation_2
	for ele in locations_relation:
		locations.append((ele.lat, ele.lng))

	# get the start and end dates of the campaign
	startDate = newCamp.startDate
	endDate = newCamp.endDate

	# make assignments with the routing alorithm
	assignments = makeAssign(locations, newCamp.duration)

	dates = [] ###### Store the Valid CanAva Objects

	''' Get all Campaign Canvassers'''
	camp_canvassers = newCamp.campaigns_relation_1
	for ele in camp_canvassers:
		''' Get all this Campaign Canvasser's all avaliable dates'''
		canDates = db_session.query(CanAva).filter(CanAva.role_id == ele.role_id).all()
		for ele_ava in canDates:
			if ele_ava.theDate >= startDate and ele_ava.theDate <= endDate:
				dates.append(ele_ava)

	'''sort dates by earliest available CanAva objects'''
	dates.sort(key= lambda d: d.theDate)

	# assign assignments to dates
	mappedAssignments = {}  ### Key = Canvasser'role_id Value = CanAva and assignment
	while(len(dates) > 0 and len(assignments) > 0):
		dTemp = dates.pop(0)  #### CanAva
		aTemp = assignments.pop(0)  #####  Location's lat and lng
		if(dTemp.role_id in mappedAssignments):
			mappedAssignments[dTemp.role_id].append((dTemp,aTemp))
		else:
			mappedAssignments[dTemp.role_id] = [(dTemp, aTemp)]

	
	#if no more assingments then this mapping is possible
	if(len(assignments) == 0):
		assignmentPossible = True

	## add assignments to database
	for ele in mappedAssignments:  ## Key---> Role Id ; Value= the serveral list of [CanAva, assingment]
		# ele is the key---> role_id
		campCanvasser= db_session.query(CampaignCanvasser).filter(CampaignCanvasser.campaign_name == newCamp.name, CampaignCanvasser.role_id == ele).first()
		for order in range(len(mappedAssignments[ele])):
			######### Order ---> serveral list of [CanAva, assignment]
			####### mappedAssignments[ele][order][0]---> get CanAva
			ass_obj = Assignment(mappedAssignments[ele][order][0].theDate, order)
			''' Add Assignment Object to CampaignCanvasser Obejct'''
			campCanvasser.canvasser_relation.append(ass_obj)

			####### mappedAssignments[ele][order][1][0]---> get assignment(lat, lng)
			lat =mappedAssignments[ele][order][1][0][0]  ####### Lat
			lng = mappedAssignments[ele][order][1][0][1]  ########## lng
			''' Add Assignment Object to CampaigbLocation Obejct'''
			allCampLocation =db_session.query(CampaignLocation).filter(CampaignLocation.campaign_name == newCamp.name).all()
			campLocation = [loc for loc in allCampLocation if (math.isclose(loc.lat, lat) and math.isclose(loc.lng, lng))]
			campLocation[0].location_relation.append(ass_obj)

			db_session.commit()

			# remove taken dates out of available in the database
			# Delet(CanAva)
			db_session.delete(mappedAssignments[ele][order][0])
			db_session.commit()


	return assignmentPossible




#function to render the manager page and set the manager page url
@bp.route('/manpage', methods=('GET', 'POST'))
def manPage():
	########### View Campaign Is the First Page #########################
	return redirect(url_for('manager.viewCampaign'))
	

@bp.route('/view_campaign')
def viewCampaign():
	if len(camp) !=0:   ############### Reload Campaings Info from  datebase
		camp.clear()
	############# Get All Campaigns Obejct from DB
	campaigns= db_session.query(Campaign).all()
	###### Loop for retrieving each campaign info
	for  obj in campaigns:
		camp_ele =[]
		camp_ele.append(obj) # camp_ele[0] = campaign 

		managers= [] #### Store all manager user objects for each campaign
		for ele in obj.campaigns_relation:
			manager_role = db_session.query(Role).filter(Role.id == ele.role_id).first()
			manager_user = db_session.query(User).filter(User.email == manager_role.email).first()
			managers.append(manager_user)
		camp_ele.append(managers)  # camp_ele[1] = manager

		canvassers = []  #### Store all canvasser user objects for each campaign
		for ele in obj.campaigns_relation_1:
			canvasser_role = db_session.query(Role).filter(Role.id == ele.role_id).first()
			canvasser_user = db_session.query(User).filter(User.email == canvasser_role.email).first()
			canvassers.append(canvasser_user)
		camp_ele.append(canvassers) # camp_ele[2] = canvasser

		locations = [] #### Store all location objects for each campaign
		for ele in obj.campaigns_relation_2:
			locations.append(ele)
		camp_ele.append(locations) # camp_ele[3] = locations

		questions= [] #### Store all question objects for each campaign
		for ele in obj.campaigns_relation_3:
			questions.append(ele)
		camp_ele.append(questions) # camp_ele[4] = questions

		camp[obj.name] = camp_ele
	return render_template('manager_html/view_campaign.html', camp=camp, name = None, camp_list = [], index =0 )

''' Selecct One Campaign, And View its Details'''
@bp.route('/view_campaign_detail/', methods=('POST','GET'))
def viewCampaignDetail():
	print("Enter View Campaign Detail\n")
	campaign_name = request.form['campaign-name']
	name = request.form['action']  # Managers/Canvassers/Locations/Questions
	if(name == "Managers"):
		return render_template('manager_html/view_campaign.html', camp=camp, name = campaign_name,camp_list = camp[campaign_name][1], index =1)
	elif (name == "Canvassers"):
		return render_template('manager_html/view_campaign.html', camp=camp, name = campaign_name,camp_list = camp[campaign_name][2], index =2)
	elif (name == "Locations"):
		return render_template('manager_html/view_campaign.html', camp=camp, name = campaign_name, camp_list = camp[campaign_name][3], index =3)
	elif (name == "Questions"):
		return render_template('manager_html/view_campaign.html', camp=camp, name = campaign_name, camp_list = camp[campaign_name][4], index =4)
	else:
		return render_template('manager_html/view_campaign.html', camp=camp, name = None, camp_list =[], index = 0)


@bp.route('/create_campaign/<u_email>', methods=['GET','POST'])
def createCampaign(u_email):
	''' Key is 'email', Value is 'name'''
	all_managers={}
	all_canvassers={}

	'''Get all managers from db '''
	manager_roles = db_session.query(Role).filter(Role.role == 'manager', Role.email != u_email).all()
	for ele in manager_roles:
		ele_user = db_session.query(User).filter(User.email == ele.email).first()
		all_managers[ele.email] = ele_user.name

	'''Get all cavasser from db'''
	canvasser_roles = db_session.query(Role).filter(Role.role == 'canvasser').all()
	for ele in canvasser_roles:
		ele_user = db_session.query(User).filter(User.email == ele.email).first()
		all_canvassers[ele.email] = ele_user.name

	''' For submit button'''
	if request.method == 'POST':
		campaign_name = request.form['name'] # string
		startDate = request.form['start_date'] #string 2018-11-26
		endDate = request.form['end_date'] 
		talking = request.form['talking'] #string 
		duration = request.form['duration']  # string : default = 1
		managers = request.form.getlist('managers')  ## list of emails
		canvassers = request.form.getlist('canvassers') ## list of emails
		questions_text = request.form['questions_text']  #string (multi-lines)
		locations = request.form['locations_text'] #string (multi-lines)s
		#print("%s %s %s %s %s %s %s %s %s" %(campaign_name, startDate, endDate, talking, duration, managers, canvassers, questions, locations))
		
		valid_locations =[]  #### Store valiad locations(address, lat, lng)

		if not (campaign_name and startDate and endDate and duration and locations):
			flash("Failed to create campaign, there're empty values!!")
			return render_template('manager_html/create_campaign.html', managers = all_managers, canvassers = all_canvassers, index = 5)
		## No empty
		questions=[] ### split quqestion with new line into one list 
		if questions_text != None and questions_text.trim() !="":
			questions = questions_text.split("\n")

		valid_locations =[]  #### Store valiad locations(address, lat, lng)

		''' Check if locations are valid or not'''
		if locations != "" :
			 locations_arr = locations.split('\n')
			 for ele in locations_arr:
			 	if(gmaps.geocode(ele) == []):
			 		flash("Failed to create campaign, the address("+ele+") is not valid!!")
			 		return render_template('manager_html/create_campaign.html', managers = all_managers, canvassers = all_canvassers, index = 5)
			 	lat = gmaps.geocode(ele)[0]['geometry']['location']['lat']
			 	lng = gmaps.geocode(ele)[0]['geometry']['location']['lng']
			 	address=gmaps.geocode(ele)[0]['formatted_address']
			 	test = (address,lat, lng)
			 	'''Check if there're some repeated locations'''
			 	if test in valid_locations:
			 		flash("Failed to create campaign, the address: ("+address+") is repeated!!!")
			 		return render_template('manager_html/create_campaign.html', managers = all_managers, canvassers = all_canvassers, index = 5)
			 	else:
			 		valid_locations.append((address,lat, lng))

		# print("valid location list---> %s" %valid_locations)

		''' Create New Campaign Object'''
		check_camp = db_session.query(Campaign).filter(Campaign.name == campaign_name).first()
		if(check_camp):
			flash("This Campaign Name already exists, please enter the unique campaign name!")
			return render_template('manager_html/create_campaign.html', managers = all_managers, canvassers = all_canvassers, index = 5)
		''' New Campaign Object'''
		newCamp = Campaign(campaign_name,startDate,endDate,talking,int(duration))
		db_session.add(newCamp)

		''' Add all managers to the newCamp relationship,'''
		for ele in managers:
			ele_obj = CampaignManager()
			role_obj = db_session.query(Role).filter(Role.email == ele, Role.role == 'manager').first()
			role_obj.roles_relation.append(ele_obj)
			newCamp.campaigns_relation.append(ele_obj)

		''' Add all canvassers to the newCamp relationship-1, androle relationship-1'''
		for ele in canvassers:
			ele_obj = CampaignCanvasser()
			role_obj = db_session.query(Role).filter(Role.email == ele, Role.role == 'canvasser').first()
			role_obj.roles_relation_1.append(ele_obj)
			newCamp.campaigns_relation_1.append(ele_obj)

		''' Add all questions to the newCamp relationship-3'''
		for ele in questions:
			if ele.trim() !="":
				ele_obj = Questionnaire(ele)
				newCamp.campaigns_relation_3.append(ele_obj)

		''' Add all locationto the newCamp relationship-2'''
		for ele in valid_locations:
			ele_obj =  CampaignLocation(ele[0], float(ele[1]), float(ele[2]))
			newCamp.campaigns_relation_2.append(ele_obj)

		db_session.commit()
		#if not enough dates/canvassers display warning
		if(not createAssignment(newCamp)):
			flash("Create Campagin successfully, but did not make compeletely assingments !")
		else:
			flash("Create Compaingn and make compeletely assignments successfully !")
		return redirect(url_for('manager.manPage'))

	return render_template('manager_html/create_campaign.html', managers = all_managers, canvassers = all_canvassers, index = 5)


@bp.route('/edit_campaign/<u_email>', methods=['GET','POST'])
def editCampaign(u_email):
	all_campaigns = db_session.query(Campaign).all()

	''' Key is 'email', Value is 'name'''
	all_managers={}
	all_canvassers={}


	'''Get all managers '''
	manager_roles = db_session.query(Role).filter(Role.role == 'manager').all()
	for ele in manager_roles:
		ele_user = db_session.query(User).filter(User.email == ele.email).first()
		all_managers[ele.email] = ele_user.name
	'''Get all cavasser'''
	canvasser_roles = db_session.query(Role).filter(Role.role == 'canvasser').all()
	for ele in canvasser_roles:
		ele_user = db_session.query(User).filter(User.email == ele.email).first()
		all_canvassers[ele.email] = ele_user.name


	if request.method == 'POST':
		if request.form['submit'] == 'select_campaign':
			campaign_name = request.form['campaign_list']

			campaign = db_session.query(Campaign).filter(Campaign.name == campaign_name).first()
			campaign_manager = campaign.campaigns_relation
			campaign_canvasser = campaign.campaigns_relation_1
			campaign_location = campaign.campaigns_relation_2
			campaign_question = campaign.campaigns_relation_3

			###here is all the manager assign to the campaign
			managers={}
			for cm in campaign_manager:
				cm_email = db_session.query(Role).filter(Role.id == cm.role_id).first().email
				cm_user = db_session.query(User).filter(User.email == cm_email).first()
				managers[cm_email] = cm_user.name

			###here is all the canvasser assign to the campaign
			canvassers={}
			for cc in campaign_canvasser:
				cc_email = db_session.query(Role).filter(Role.id == cc.role_id).first().email
				cc_user = db_session.query(User).filter(User.email == cc_email).first()
				canvassers[cc_email] = cc_user.name

			###
			#comparing two dictionary 
			###
			unselected_managers=all_managers
			all(map(unselected_managers.pop, managers))

			unselected_canvassers=all_canvassers
			all(map(unselected_canvassers.pop, canvassers))

			return render_template('manager_html/edit_campaign.html', campaign_name = campaign_name, all_campaigns = all_campaigns,unselected_managers = unselected_managers, unselected_canvassers = unselected_canvassers, managers = managers, canvassers=canvassers, start_date = campaign.startDate, end_date = campaign.endDate, talking=campaign.talking, question=campaign_question, location=campaign_location, duration=campaign.duration,index = 6)

		elif request.form['submit'] == 'submit_change':

			old_campaign_name = request.form['campaign_list']
			new_campaign_name = request.form['campaign_name']
			startDate = request.form['start_date']
			endDate = request.form['end_date']
			talking = request.form['talking']
			duration = request.form.get('duration')  # default = ''
			managers = request.form.getlist('managers')  ## format = email
			canvassers = request.form.getlist('canvassers') ## format = email
			questions = request.form.getlist('question_list')
			locations = request.form.getlist('location_list')  ## format = address|lat|lng

			current_campaign = db_session.query(Campaign).filter(Campaign.name == old_campaign_name).first()

			if new_campaign_name is '':
				current_campaign.name = old_campaign_name
			else:
				current_campaign.name = new_campaign_name


			current_campaign.startDate = startDate
			current_campaign.endDate = endDate
			current_campaign.talking = talking
			current_campaign.duration = duration

			current_campaign.campaigns_relation = []
			current_campaign.campaigns_relation_1 = []
			current_campaign.campaigns_relation_2 = []
			current_campaign.campaigns_relation_3 = []

			db_session.commit()

			for ele in managers:
				ele_obj = CampaignManager()
				role_obj = db_session.query(Role).filter(Role.email == ele, Role.role == 'manager').first()
				role_obj.roles_relation.append(ele_obj)
				current_campaign.campaigns_relation.append(ele_obj)

			''' Add all canvassers to the newCamp relationship-1, androle relationship-1'''
			for ele in canvassers:
				ele_obj = CampaignCanvasser()
				role_obj = db_session.query(Role).filter(Role.email == ele, Role.role == 'canvasser').first()
				role_obj.roles_relation_1.append(ele_obj)
				current_campaign.campaigns_relation_1.append(ele_obj)

			''' Add all questions to the newCamp relationship-3'''
			for ele in questions:
				ele_obj = Questionnaire(ele)
				current_campaign.campaigns_relation_3.append(ele_obj)

			''' Add all locationto the newCamp relationship-2'''
			for ele in locations:
				ele_arr = ele.split('|')
				ele_obj =  CampaignLocation(ele_arr[0],float(ele_arr[1]), float(ele_arr[2]))
				current_campaign.campaigns_relation_2.append(ele_obj)

			db_session.commit()

			return redirect(url_for('manager.manPage'))
	else:
		return render_template('manager_html/edit_campaign.html', all_campaigns = all_campaigns,index = 6)



''' Method for deleting Campaing'''
@bp.route('/delete_campaign/<campName>/', methods=('GET', 'POST'))
def delete(campName):
    if request.method == 'POST':
    	deletedCamp = db_session.query(Campaign).filter(Campaign.name == campName).first()
    	if deletedCamp is not None:
    		''' Find the deletedCamp, and delete'''
    		db_session.delete(deletedCamp)
    		db_session.commit()
    		flash("Delete the Campaign Successfully","info")
    return redirect(url_for('manager.viewCampaign'))


@bp.route('/view_assignment', methods=['GET','POST'])
def viewAssignment():
	print("Enter View Assignment \n")
	return render_template('manager_html/edit_campaign.html', camp=camp, name = None, camp_list = [], index = 0)

@bp.route('/edit_assignment', methods=['GET','POST'])
def editAssignment():
	print("Enter Edit Assignment \n")
	return render_template('manager_html/edit_assignment.html', camp=camp, name = None, camp_list = [], index = 0)

@bp.route('/view_result', methods=['GET','POST'])
def viewResult():
	print("Enter Edit Assignment \n")
	return render_template('manager_html/edit_assignment.html', camp=camp, name = None, camp_list = [], index = 0)
