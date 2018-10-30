from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Campaign, Role, Location,CampaignLocation,CampaignCanvasser, CampaignManager




#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/create_campaign', methods=['GET','POST'])
def createCampaign():
	managerObject = db_session.query(Role).filter(Role.role =='manager')
	canvasObject  = db_session.query(Role).filter(Role.role == 'canvasser')
	campaignObject = db_session.query(Campaign)
	if request.method == 'POST':
		
		campaignName = request.form['campaign_name']
		address = request.form['address'];
		startdate = request.form['start_date']
		enddate = request.form['end_date']
		managers = request.form.getlist('flaskManager')
		canvassers = request.form.getlist('flaskCanvasser')
		
		
		campObj = Campaign(campaignName, startdate, enddate)
		locationObj = Location(address)
		db_session.add(locationObj)
		db_session.add(campObj)

		##
		testL = CampaignLocation()
		locationObj.locations_relation.append(testL)
		campObj.campaigns_relation_2.append(testL)
		##
		for m in managers:
			role = db_session.query(Role).filter(Role.role == 'manager',  Role.name == m).first()
			print(role)
			mObject = CampaignManager()
			role.roles_relation.append(mObject)
			campObj.campaigns_relation.append(mObject)


		for c in canvassers:
			role = db_session.query(Role).filter(Role.role == 'canvasser',  Role.name == c).first()
			print(role)
			cObject = CampaignCanvasser()
			role.roles_relation_1.append(cObject)
			campObj.campaigns_relation_1.append(cObject)

		
		db_session.commit()
		
	else:
		return render_template('manager_html/create_campaign.html', managers=managerObject, canvasser=canvasObject)

	return render_template('manager_html/view_campaign.html', camp=campaignObject)

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
	result = 1;
	return render_template('manager_html/view_campaign_result.html')


@bp.route('/edit_campaign')
def editCampaign():
	result = 1;
	return render_template('manager_html/edit_campaign.html')

@bp.route('/create_canvas_assignment')
def createCanvasAssignment():
	result = 1;
	return render_template('manager_html/create_canvas_assignment.html');

@bp.route('/view_canvas_assignment')
def viewCanvasAssignment():
	result = 1;
	return render_template('manager_html/view_canvas_assignment.html');