from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort
from database import db_session, User, CanAva, Role
import json
import logging
import datetime
import time

# Create canvasser blueprint
bp = Blueprint('canvasser', __name__, url_prefix='/canvasser')
user_email=""


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
	print(ava_obj)
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
	# if len(events)>0:
	# 	for instance in events:
	# 		avails.append({
	# 			'title':"Free",
	# 			'start':str(instance.theDate),
	# 			'end':str(instance.theDate),
	# 			'allDay':True
	# 			})

	# 	canvasEvents = json.dumps(avails)
	# 	logging.debug("fetching info availability from database for "+user_email)
	# 	return render_template('canvasser_html/canvas.html',avails=canvasEvents)
	return render_template('canvasser_html/canvas.html',avails=None)
