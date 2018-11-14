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
from assignmentModeling import DateObject, assignmentMapping


#link google map
gmaps = googlemaps.Client(key = key)

#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

''' Store All Campaigns Info : Key = campaign Name ; Value = Detail Info the specified Campaign'''
camp = {}

''' Create Assignment for one Campaing'''
def createAssignment(newCamp,canvassers,locations):
	# flag for marking the assignment the campaign as possible
	assignmentPossible = False
	# get headquarters for starting location for routing algorithm
	globalVars = db_session.query(GlobalVariables).first()
	hq = (globalVars.hqX, globalVars.hqY)
	# get campaign location data
	all_locations = []
	# add the headquarters to the location set
	all_locations.append(hq)
	# add all campaign locations to the locations set
	for ele in locations:
		ele_arr = ele.split('|')
		all_locations.append((float(ele_arr[1]), float(ele_arr[2])))
	# make assignments with the routing alorithm
	startDate = newCamp.startDate
	endDate = newCamp.endDate
	print(type(startDate))
	print(all_locations)
	assignments = makeAssign(all_locations, int(newCamp.duration))

	dates = []
	# get the start and end dates of the campaign
	startDate = newCamp.startDate
	endDate = newCamp.endDate
	print(type(startDate))
	# startdatetime.strptime(date_string, '%Y-%m-%d').date()
	# startDate = datetime.date(int(startDate[0:4]), int(startDate[5:7]), int(startDate[8:]))
	# endDate = datetime.date(int(endDate[0:4]), int(endDate[5:7]), int(endDate[8:]))
	# 	emails = []
	# 	for i in range(len(canvassers)):
	# 		roleObj = db_session.query(Role).filter(Role.id == canvassers[i].user_id).first()
	# 		emails.append(roleObj.email)
	# 	# collect the available dates of each canvasser in the campaign
	# 	for i in range(len(emails)):
	# 		cEmail = emails[i]
	# 		canDates = db_session.query(CanAva).filter(CanAva.email == cEmail).all()
	# 		for j in range(len(canDates)):
	# 			# filter out dates not in the campaign range
	# 			if(canDates[j].theDate >= startDate and canDates[j].theDate <= endDate):
	# 				dates.append(DateObject(canDates[j].theDate, canDates[j].email, canDates[j].id))
	# 	# sort dates by earliest available using bubble sort
	# 	sortComplete = 0
	# 	while(sortComplete == 0):
	# 		sortComplete = 1
	# 		for i in range(len(dates)):
	# 			if(i != (len(dates)-1)):
	# 				if(dates[i].date > dates[i+1].date):
	# 					temp = dates[i+1]
	# 					dates[i+1] = dates[i]
	# 					dates[i] = temp
	# 					sortComplete = 0
	# 	# assign assignments to dates
	# 	mappedAssignments = []
	# 	while(len(dates) > 0 and len(assignments) > 0):
	# 		dTemp = dates.pop(0)
	# 		aTemp = assignments.pop(0)
	# 		mappedAssignments.append(assignmentMapping(dTemp.date, dTemp.canEmail, dTemp.dateId, aTemp))
	# 	# if no more assingments then this mapping is possible
	# 	if(len(assignments) == 0):
	# 		assignmentPossible = True

	# 	# add assignments to database
	# 	for i in range(len(mappedAssignments)):
	# 		for j in range(len(mappedAssignments[i].assignment)):
	# 			assignObj = Assignment(mappedAssignments[i].date, mappedAssignments[i].assignment[j][0], mappedAssignments[i].assignment[j][1], mappedAssignments[i].canEmail, j, campObj.id)
	# 			db_session.add(assignObj)
	# 			db_session.commit()

	# 	# remove taken dates out of available in the database
	# 	for i in range(len(mappedAssignments)):
	# 		dateDelete = db_session.query(CanAva).filter(CanAva.id == mappedAssignments[i].dateId).first()
	# 		db_session.delete(dateDelete)
	# 		db_session.commit()
	# 	# if not enough dates/canvassers display warning
	# 	if(assignmentPossible == False):
	# 		return 'not possible'

	# campObj= db_session.query(Campaign)
	return True




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
	print("Create Campaign here \n")
	''' Key is 'email', Value is 'name'''
	all_managers={}
	all_canvassers={}

	'''Get all managers '''
	manager_roles = db_session.query(Role).filter(Role.role == 'manager', Role.email != u_email).all()
	for ele in manager_roles:
		ele_user = db_session.query(User).filter(User.email == ele.email).first()
		all_managers[ele.email] = ele_user.name
	'''Get all cavasser'''
	canvasser_roles = db_session.query(Role).filter(Role.role == 'canvasser').all()
	for ele in canvasser_roles:
		ele_user = db_session.query(User).filter(User.email == ele.email).first()
		all_canvassers[ele.email] = ele_user.name
	if request.method == 'POST':
		campaign_name = request.form['name']
		startDate = request.form['start_date']
		endDate = request.form['end_date']
		talking = request.form['talking']
		duration = request.form.get('duration')  # default = ''
		managers = request.form.getlist('managers')  ## format = [email|name]
		canvassers = request.form.getlist('canvassers') ## format = [mail|name]
		questions = request.form.getlist('question_list')
		locations = request.form.getlist('location_list')  ## format = address|lat|lng
		''' Create New Campaign Object'''
		newCamp = Campaign(campaign_name,startDate,endDate,talking,duration)
		db_session.add(newCamp)
		''' Add all managers to the newCamp relationship,'''
		for ele in managers:
			ele_arr = ele.split('|')
			ele_obj = CampaignManager()
			role_obj = db_session.query(Role).filter(Role.email == ele_arr[0], Role.role == 'manager').first()
			role_obj.roles_relation.append(ele_obj)
			newCamp.campaigns_relation.append(ele_obj)
		''' Add all canvassers to the newCamp relationship-1, androle relationship-1'''
		for ele in canvassers:
			ele_arr = ele.split('|')
			ele_obj = CampaignCanvasser()
			role_obj = db_session.query(Role).filter(Role.email == ele_arr[0], Role.role == 'canvasser').first()
			role_obj.roles_relation_1.append(ele_obj)
			newCamp.campaigns_relation_1.append(ele_obj)

		''' Add all questions to the newCamp relationship-3'''
		for ele in questions:
			ele_obj = Questionnaire(ele)
			newCamp.campaigns_relation_3.append(ele_obj)
		''' Add all locationto the newCamp relationship-2'''
		for ele in locations:
			ele_arr = ele.split('|')
			ele_obj =  CampaignLocation(ele_arr[0], ele_arr[1], ele_arr[2])
			newCamp.campaigns_relation_2.append(ele_obj)

		db_session.commit()
		createAssignment(newCamp,canvassers,locations)

	return render_template('manager_html/create_campaign.html', managers = all_managers, canvassers = all_canvassers, index = 5)


@bp.route('/edit_campaign', methods=['GET','POST'])
def editCampaign():
	print("Enter Edit Campaign \n")
	return render_template('manager_html/edit_campaign.html', camp=camp, name = None, camp_list = [], index = 0)

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
