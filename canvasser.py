from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, CanAva
import json

#create canvasser blueprint
bp = Blueprint('canvasser', __name__, url_prefix='/canvasser')
user_email=""
#canvasser page url and render method

@bp.route('/update_ava')
def update_ava():
	#fetching info from the calendar implemented in canvasser
	#heavily rely on the javascript->html->jinja2->python interactions
	title = request.args.get('title')
	start = request.args.get('start')
	end = request.args.get('end')
	allDay = request.args.get('allDay')
	ava = CanAva(title,start,end,allDay,user_email)
	db_session.add(ava)
	logging.info("updating availability for email "+user_email+" with "+tile+""+start+""+end)
	db_session.commit()

	return "set availability ok"

@bp.route('/canPage/<u_email>', methods=('GET', 'POST'))
def canPage(u_email):
	global user_email
	user_email = u_email

	#fetching data from db and format it into json
	#this part is intend for fetching stored availabilities in db
	events = db_session.query(CanAva).filter(CanAva.email == u_email)
	avails =[]
	for instance in events:
		avails.append({
			'title':instance.title,
			'start':instance.start,
			'end':instance.end,
			'allDay':instance.allDay
			})
	canvasEvents = json.dumps(avails)
	logging.debg("fetching info availability from database for "+u_email)
	return render_template('canvasser_html/canvas.html',avails=canvasEvents)