from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, CanAva
import json

#create canvasser blueprint
bp = Blueprint('canvasser', __name__, url_prefix='/canvasser')
user=""
#canvasser page url and render method
@bp.route('/update_ava')
def update_ava():
	title = request.args.get('title')
	start = request.args.get('start')
	end = request.args.get('end')
	allDay = request.args.get('allDay')
	ava = CanAva(title,start,end,allDay,user)
	db_session.add(ava)
	db_session.commit()

	return "set availability ok"

@bp.route('/canPage/<u_email>', methods=('GET', 'POST'))
def canPage(u_email):
	global user
	user = u_email
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
	return render_template('canvasser_html/canvas.html',avails=canvasEvents)