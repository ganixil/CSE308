from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Campaign

#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/create_campaign', methods=('GET', 'POST'))
def createCampaign():
	if request.method == 'POST':
		campaignName = request.form['campaign_name']
		managers = request.form.getlist('flaskManager')
		print(campaignName)

		for manager in managers:
			print(manager)
	return render_template('manager_html/create_campaign.html')

#function to render the manager page and set the manager page url
@bp.route('/manpage', methods=('GET', 'POST'))
def manPage():
    return render_template('manager_html/create_canvas_assignment.html')


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