from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Campaign, Role,CampaignLocation,CampaignCanvasser, CampaignManager, Questionnaire
import logging


#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

''' Store All Campaigns Info : Key = campaign Name ; Value = Detail Info the specified Campaign'''
camp = {}

#function to render the manager page and set the manager page url
@bp.route('/manpage', methods=('GET', 'POST'))
def manPage():
	########### View Campaign Is the First Page #########################
	return redirect(url_for('manager.viewCampaign'))
	
@bp.route('/view_campaign')
def viewCampaign():
	logging.info("Enter View Campaigns of the system")

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
		for ele in  camp[campaign_name][3]:
			print("%s\n" %ele)
		return render_template('manager_html/view_campaign.html', camp=camp, name = campaign_name, camp_list = camp[campaign_name][3], index =3)
	elif (name == "Questions"):
		return render_template('manager_html/view_campaign.html', camp=camp, name = campaign_name, camp_list = camp[campaign_name][4], index =4)
	else:
		return render_template('manager_html/view_campaign.html', camp=camp, name = None, camp_list =[], index = 0)


@bp.route('/create_campaign', methods=['GET','POST'])
def createCampaign():
	print("Enter Edit Campaign \n")
	return render_template('manager_html/edit_campaign.html', camp=camp, name = None, camp_list = [], index = 0)

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
