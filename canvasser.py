from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort
from database import db_session, User, CanAva, Role, CampaignCanvasser, Assignment, CampaignLocation, Campaign
import json
import logging
import datetime
import time
import re

# Create canvasser blueprint
bp = Blueprint('canvasser', __name__, url_prefix='/canvasser')

#### Keep the canvasser's email to be avaliable for getting User, Role Object
user_email=""
''' 
	'asignments'  --- dict : ###### Key = Assignment, Value = (location,lat, lng)
	Although the order for assignments in DB is base on the value of date
	However, if the canvasser change the next location to visite. it will change the order.
	Therefore, i will load the assignments based on the value of assignment.order
'''
assignments={}
past_assignments={}  ## store past assignments which date value less than today
upcoming_assignments={} ## store past assignments which date value not less than today
detail={}

today = datetime.date.today()

''' 
	update_ava() --- update the avaliability dates for the canvasser
	remove_ava() --- remove the availability dates for the canvasser
'''
@bp.route('/update_ava')
def update_ava():
	# Fetching info from the calendar implemented in canvasser
	title = request.args.get('title')
	start = request.args.get('start')
	############ Change Date string to Date object (yyyy-mm-dd)
	dateStrings = start.split()
	dateString = dateStrings[3] + " " + dateStrings[1] + " " + dateStrings[2]
	struc = time.strptime(dateString, '%Y %b %d')
	startDate = datetime.date(struc.tm_year, struc.tm_mon, struc.tm_mday)

	''' Create CanAva object,and add it to DB'''
	ava_obj = CanAva(startDate)
	''' Query Role Id firstly, the get the CanAva obj'''
	role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role == 'canvasser').first()
	role_obj.roles_relation_2.append(ava_obj)
	db_session.commit()

	logging.info("updating availability for email "+user_email+" with "+" the date on "+start)
	return 'update'

@bp.route('/remove_ava')
def remove_ava():
	# Fetching info from the calendar implemented in canvasser
	title = request.args.get('title')
	start = request.args.get('start')
	############ Change Date string to Date object (yyyy-mm-dd)
	dateStrings = start.split()
	dateString = dateStrings[3] + " " + dateStrings[1] + " " + dateStrings[2]
	struc = time.strptime(dateString, '%Y %b %d')
	startDate = datetime.date(struc.tm_year, struc.tm_mon, struc.tm_mday)

	''' Query Role Id firstly, the query CanAva obj'''
	role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role == 'canvasser').first()
	ava_obj = db_session.query(CanAva).filter(CanAva.role_id == role_obj.id, CanAva.theDate == startDate).first()
	db_session.delete(ava_obj)
	db_session.commit()

	logging.info("delete available date for email "+user_email+" with "+" the date on "+start)
	return 'remove'


# Method for rendering the canvasser's homepage
@bp.route('/canPage/<u_name>', methods=('GET', 'POST'))
def canPage(u_name):
	global user_email
	global assignments
	''' The first time to load assignments for the canvasser'''
	assignments={}

	user_email = session['info']['email']
 
	#### Query Role from DB  #########
	role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role =='canvasser').first()

	#### Load available dates of the canvasser to the calendar
	events = db_session.query(CanAva).filter(CanAva.role_id == role_obj.id).all()
	avails =[]
	if len(events)>0:
		for instance in events:
			avails.append({
				'title':"Avaliable",
				'constraint': 'Ava',
				'start':str(instance.theDate),
				'textColor':'black !important',
				'backgroundColor': "#FF3B30!important"
				})

	camp_canvassers = db_session.query(CampaignCanvasser).filter(CampaignCanvasser.role_id == role_obj.id).all()
	######### Load all assigmenets the canvasser to the calendar
	for ele in camp_canvassers:
		## Get assignments of this canvasser for one specified Campign
		ass_obj = db_session.query(Assignment).filter(Assignment.canvasser_id == ele.id).all()
		for ass in ass_obj:
			###  Retrieve location values for getting the marker later in html page
			location = db_session.query(CampaignLocation).filter(CampaignLocation.id == ass.location_id).first()
			assignments[ass] =(location.location,location.lat,location.lng)
			avails.append({
				'title':"Have Assignment",
				'constraint': 'Ass',
				'start':str(ass.theDate),
				'textColor':'black !important',
				'backgroundColor': "#7FFFD4 !important"
				})
	######### Sort assignments based on the value of the assignments' order
	if assignments !={}:
		######## Get all itmes(key, value) of the dict: assignments
		items = assignments.items()
		items = sorted(items, key=lambda x: (x[0]).order)
		###### resign assignments with the new order
		assignments={}
		for ele in items:
			assignments[ele[0]] = ele[1]

		print("canPage: the order of assignments: %s" %assignments.keys())

	if(len(avails) != 0):
		canvasEvents = json.dumps(avails)
		logging.debug("fetching info availability  and assignemnt from database for "+ user_email)
		logging.info("Load all information for the homepage of the canvasser with email: "+user_email)
		return render_template('canvasser_html/canvas.html',avails=canvasEvents, u_name=u_name)
	##### len(avails) = 0
	return render_template('canvasser_html/canvas.html',avails=None, u_name=u_name)


# Enter viewing upcomming assignment html page
@bp.route('/view_all_assignment/<u_email>')
def view_assignment(u_email):
	global assignments
	global today
	global past_assignments
	global upcoming_assignments
	print("Enter View Assignment")

	if assignments=={}:
		'''Without any assignments'''
		flash("You do not have any assignments")
		return redirect(url_for('canvasser.canPage', u_name = session['info']['name']))
	'''if there're some assignments'''
	past_assignments={}
	upcoming_assignments={}
	for ele in assignments:
		if ele.theDate < today:
			past_assignments[ele] = assignments[ele]
		else:
			upcoming_assignments[ele] = assignments[ele]

	return render_template('canvasser_html/view_assignment.html',upcoming_assignments= upcoming_assignments, past_assignments= past_assignments, detail=None)


'''Work For viewingn assignment detail'''
@bp.route('/view_assignment_detail/<ass_id>')
def view_assignment_detail(ass_id):
	global assignments
	global user_email
	global detail
	print("enter view_assigment detail")

	detail={}
	''' Retrieve Canvasser Name'''
	canvasser = db_session.query(User).filter(User.email == user_email).first()
	detail['canvasser_name'] = canvasser.name
	''' Retrieve Assignment Object'''
	assignment = db_session.query(Assignment).filter(Assignment.id == ass_id).first()
	''' I need info: Canvasser Name; Campaign Name, Date, Location Latitude, Longtitude,
		Talking Point, Questionnair;
	'''
	detail['assignment'] = assignment #### For getting date and order values

	campaign_loc = db_session.query(CampaignLocation).filter(CampaignLocation.id == assignment.location_id).first()
	detail['campaign_name'] = campaign_loc.campaign_name

	###### loc=(location, lat,lng)
	loc=(campaign_loc.location, campaign_loc.lat, campaign_loc.lng)
	detail['location'] = loc ######## detail[2] = (location, lat, lng)

	'''Get Specified Campaign Object'''
	camp = db_session.query(Campaign).filter(Campaign.name == campaign_loc.campaign_name).first()
	'''Get Questionaire'''
	detail['questions'] = camp.campaigns_relation_3
	'''Get Tlking Point'''
	detail['talking'] = camp.talking

	return render_template('canvasser_html/view_assignment.html',upcoming_assignments= upcoming_assignments, past_assignments= past_assignments, detail=detail)

@bp.route('/view_result/<ass_id>')
def view_result(ass_id):
	print("enter view result : canvasser")
	global upcoming_assignments
	global past_assignments
	global detail
	return render_template('canvasser_html/view_assignment.html',upcoming_assignments= upcoming_assignments, past_assignments= past_assignments, detail=detail)



# Enter canvas_start html
@bp.route('/set_start_canvasser')
def set_canvasser():
	global assignments
	global user_email
	global today

	'''
		use ass_info to organize assignments : current day's assignment, 
		next location assignment, most recently visted assignmnet
	'''
	ass_info={} 

	current_ass=None  ## Keep current day's assignment
	next_ass=None   ## Keep the next location need to be visted in default
	'''Retrieve the today's assignment from global variable 'assignments'''
	for ele in assignments:
		if ele.theDate == today:
			current_ass = ele
		elif ele.theDate > today:
			next_ass = ele
			break

	visited_ass =None     # Record the most recently visited location
	next_locations=[]  ###### Record all next locations need to be visited
	for ele in assignments:  ######### the order based on the Assignment's order
		if ele.done:
			''' Find the most recently visited location '''
			visited_ass = ele
		if ele.theDate > today:
			next_locations.append(ele)

	''' if there's one assignment on today, it means we need to find the detailed travel directions from this location to next location
		    if there's without any assignment on today, it means we need to find the detailed travel direction from the most
		    	visited location to next location
		    if no visited assignments, and no current day's assigments, then we do not need to get any travel direction
	'''
	if visited_ass == None:
		if current_ass:
			visited_ass = current_ass

	visited_ass = current_ass
	ass_info['current_ass'] = current_ass
	ass_info['next_ass'] = next_ass
	ass_info['visited_ass'] = visited_ass
	ass_info['next_locations'] = next_locations

	print("assignemnt Info for canvass")
	for ele in ass_info:
		print("%s---> %s" %(ele,ass_info[ele]))
	''' Get Current assignment's Campaign Name'''
	current_camp_name =""
	if current_ass :
		current_camp_name = db_session.query(CampaignLocation).filter(CampaignLocation.id == current_ass.location_id).first()
	ass_info['campaign_name'] = current_camp_name.campaign_name

	return render_template('canvasser_html/canvas_start.html', assignments= assignments, ass_info = ass_info)


# Enter canvas_start html
@bp.route('/change_next_location', methods=['GET','POST'])
def change_next_location():
	if request.method == 'POST':
		global assignments
		print("Change Next Location")

		next_ass_str = request.form['next_loc']
		next_ass_arr = re.split(r'[()]', next_ass_str) ##[address_value, id, space]
		next_ass_id = int(next_ass_arr[1])
		'''Retrieve orgin next assignment object from next_ass_id'''
		next_ass_obj = db_session.query(Assignment).filter(Assignment.id == next_ass_id).first()

		ass_id = request.form.get('end')
		''' Retrieve assignment object from ass_id'''
		ass_obj = db_session.query(Assignment).filter(Assignment.id == int(ass_id)).first()
		if ass_obj == None:
			flash("This assignment does not exist")
			return redirect(url_for("canvasser.set_canvasser"))

		old_order = int(next_ass_obj.order)### to mark the original next location
		new_order=int(ass_obj.order)  ### to mark which location we selected


		''' Use to store the assignments which their order not less than the original next assignment's order'''
		if(old_order != new_order):
			''' Just think about the situation which we change the next location to anther one'''
			other_ass =[] 
			for ele in assignments:
				if ele.order >= old_order:
					other_ass.append(ele)

			for ele in other_ass:
				if ele.order < new_order:
					ele_obj = db_session.query(Assignment).filter(Assignment.id == ele.id).first()
					ele_obj.order += 1

			## The selected next location should be the first of the upcoming assignments
			ass_obj.order = int(old_order)
			db_session.commit()
			# ''' Reload assignments: same to the canPage'''
			assignments={}
			role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role =='canvasser').first()
			camp_canvassers = db_session.query(CampaignCanvasser).filter(CampaignCanvasser.role_id == role_obj.id).all()
			for ele in camp_canvassers:
				ass_obj = db_session.query(Assignment).filter(Assignment.canvasser_id == ele.id).all()
				for ass in ass_obj:
					location = db_session.query(CampaignLocation).filter(CampaignLocation.id == ass.location_id).first()
					assignments[ass] =(location.location,location.lat,location.lng)
			# assignments.keys() = sorted(assignments.keys(), key=lambda x: x.order)
			flash("Change Next Location Successfully!!")

	return redirect(url_for("canvasser.set_canvasser"))


# Enter done_canvas html
@bp.route('/done_canvas/<ass_id>')
def done_canvasser(ass_id):
	return render_template('canvasser_html/done_canvas.html')