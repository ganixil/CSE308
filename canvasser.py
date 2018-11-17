from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort
from database import db_session, User, CanAva, Role, CampaignCanvasser, Assignment, CampaignLocation, Camapaign
import json
import logging
import datetime
import time

# Create canvasser blueprint
bp = Blueprint('canvasser', __name__, url_prefix='/canvasser')
user_email=""
assignments={}  ####### Key = Assignment, Value = (location,lat, lng)


# Canvasser page url and render method, this method is for updating availability
@bp.route('/update_ava')
def update_ava():
	# Fetching info from the calendar implemented in canvasser
	# Using the javascript->html->jinja2->python interactions
	title = request.args.get('title')
	# format the date string so it can be used to make a Python date object
	start = request.args.get('start')

	dateStrings = start.split()
	dateString = dateStrings[3] + " " + dateStrings[1] + " " + dateStrings[2]
	struc = time.strptime(dateString, '%Y %b %d')
	''' yyyy-mm-dd'''
	startDate = datetime.date(struc.tm_year, struc.tm_mon, struc.tm_mday)

	''' Create CanAva object,and add it to DB'''
	ava_obj = CanAva(startDate)
	role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role == 'canvasser').first()
	role_obj.roles_relation_2.append(ava_obj)
	db_session.commit()
	logging.info("updating availability for email "+user_email+" with "+" the date on "+start)

	return 'update'


# Canvasser page url and render method, this method is for delete the avaliable date
@bp.route('/remove_ava')
def remove_ava():
	# Fetching info from the calendar implemented in canvasser
	# Using the javascript->html->jinja2->python interactions
	title = request.args.get('title')
	# format the date string so it can be used to make a Python date object
	start = request.args.get('start')

	dateStrings = start.split()
	dateString = dateStrings[3] + " " + dateStrings[1] + " " + dateStrings[2]
	struc = time.strptime(dateString, '%Y %b %d')
	''' yyyy-mm-dd'''
	startDate = datetime.date(struc.tm_year, struc.tm_mon, struc.tm_mday)

	''' Query Role Id firstly, the query CanAva obj'''
	role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role == 'canvasser').first()
	''' Create CanAva object,and removev from DB'''
	ava_obj = db_session.query(CanAva).filter(CanAva.role_id == role_obj.id, CanAva.theDate == startDate).first()

	db_session.delete(ava_obj)
	db_session.commit()

	logging.info("delete available date for email "+user_email+" with "+" the date on "+start)
	return 'remove'


# Method for rendering the canvasser's homepage
@bp.route('/canPage/<u_name>', methods=('GET', 'POST'))
def canPage(u_name):
	global user_email
	user_email = session['info']['email']
 
	#### Query Role from DB  #########
	role_obj = db_session.query(Role).filter(Role.email == user_email, Role.role =='canvasser').first()

	'''
	Fetch CanAva Objects to get Event date
	'''
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
	for ele in camp_canvassers:
		## Get one Campaign Canvasser Object
		ass_obj = db_session.query(Assignment).filter(Assignment.canvasser_id == ele.id).all()
		for ele_ass in ass_obj:
			avails.append({
				'title':"Have Assignment",
				'constraint': 'Ass',
				'start':str(ele_ass.theDate),
				'textColor':'black !important',
				'backgroundColor': "#7FFFD4 !important"
				})

	if(len(avails) != 0):
		canvasEvents = json.dumps(avails)
		logging.debug("fetching info availability  and assignemnt from database for "+ user_email)
		return render_template('canvasser_html/canvas.html',avails=canvasEvents, u_name=u_name)
	return render_template('canvasser_html/canvas.html',avails=None, u_name=u_name)

# Enter viewing upcomming assignment html page
@bp.route('/view_all_assignment')
def view_assignment():
	global assignements
	print("Enter View Assignment")
	''' Retrieve Role Object'''
	can_role = db_session.query(Role).filter(Role.email == user_email, Role.role == 'canvasser').first()
	''' Retrieve Camapaign Canvasser  Object List'''
	can_camps = db_session.query(CampaignCanvasser).filter(CampaignCanvasser.role_id == can_role.id).all()
	''' Store all asssigements of this Canvasser'''
	for ele in can_camps:
		''' Retrieve assignement object from DB'''
		all_assignments=db_session.query(Assignment).filter(Assignment.canvasser_id == ele.id).all()
		for ass in all_assignments:
			location = db_session.query(CampaignLocation).filter(CampaignLocation.id == ass.location_id).first()
			assignments[ass] =(location.location,location.lat,location.lng)

	if assignments=={}:
		'''Without any assignments'''
		flash("You do not have any assignments")
		return redirect(url_for('canvassser.canPage', u_name = session['info']['name']))
	'''if there're some assignments'''
	return render_template('canvasser_html/view_assignment.html',assignments = assignments, detail=None)

'''Work For viewingn assignment detail'''
@bp.route('/view_assigment_detail/<ass_id>')
def view_assigment_detail(ass_id):
	print("enter view_assigment")
	detail={}
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
	return render_template('canvasser_html/view_assignment.html',assignements=assignements,detail=detail)



# Enter canvas_start html
@bp.route('/set_start_canvasser')
def set_canvasser():
	return render_template('canvasser_html/canvas_start.html')

# Enter done_canvas html
@bp.route('/done_canvas')
def done_canvasser():
	return render_template('canvasser_html/done_canvas.html')