from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Campaign, Role,CampaignLocation,CampaignCanvasser, CampaignManager, Questionnaire




#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/create_campaign', methods=['GET','POST'])
def createCampaign():
	managerObject = db_session.query(Role).filter(Role.role =='manager')

	manager_email =[]
	for m in managerObject:
		manager_email.append(m.email)

	manager_name = []
	for e in manager_email:
		manager_name.append(db_session.query(User).filter(User.email==e).first().name)


	canvasObject  = db_session.query(Role).filter(Role.role == 'canvasser')

	canvasser_email=[]
	for c in canvasObject:
		canvasser_email.append(c.email)

	canvasser_name = []
	for e in canvasser_email:
		canvasser_name.append(db_session.query(User).filter(User.email==e).first().name)


	campaignObject = db_session.query(Campaign)
	if request.method == 'POST':
		
		campaignName = request.form['campaign_name']
		startdate = request.form['start_date']
		enddate = request.form['end_date']
		talking = request.form['talking']
		duration = request.form['duration']
		managers = request.form.getlist('flaskManager')
		canvassers = request.form.getlist('flaskCanvasser')
		locations = request.form.getlist('flaskLocation')
		questions = request.form.getlist('flaskQuestion')

		
		campObj = Campaign(campaignName, startdate, enddate, talking,duration)
		db_session.add(campObj)

		##
		for m in managers:
			nameObj = db_session.query(User).filter(User.name == m).first()
			role = db_session.query(Role).filter(Role.role == 'manager',  Role.email == nameObj.email).first()
			mObject = CampaignManager()
			role.roles_relation.append(mObject)
			campObj.campaigns_relation.append(mObject)

		for c in canvassers:
			nameObj = db_session.query(User).filter(User.name == c).first()
			role = db_session.query(Role).filter(Role.role == 'canvasser',  Role.email == nameObj.email).first()
			cObject = CampaignCanvasser()
			role.roles_relation_1.append(cObject)
			campObj.campaigns_relation_1.append(cObject)

		for l  in locations:
			loc = CampaignLocation(l)
			campObj.campaigns_relation_2.append(loc)

		for q in questions:
			ques = Questionnaire(q)
			campObj.campaigns_relation_3.append(ques)
		
		db_session.commit()
		
	else:
		return render_template('manager_html/create_campaign.html', managers=manager_name, canvasser=canvasser_name)

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
	result = 1
	return render_template('manager_html/view_campaign_result.html')


@bp.route('/edit_campaign')
def editCampaign():
	campaignObject = db_session.query(Campaign)

	return render_template('manager_html/edit_campaign.html', camp=campaignObject)

@bp.route('/show_campaign',methods=('POST','GET'))
def showCampaign():
	if request.method == "POST":

		try:
			if request.form['submit_btn'] == 'submit_form':
				
				#Update old Campaign name
				oldCamp = db_session.query(Campaign).filter(Campaign.campaign_name ==  request.form['scampaign_name']).first()
				oldCamp.campaign_name = request.form['new_campaign_name']
				db_session.commit()

				#Remove all manager asociated with Old Campaign
				db_session.query(CampaignManager).filter(CampaignManager.campaign_id == oldCamp.id).delete()
				db_session.commit()
				
				#Add new managers to Old campaign
				newManagers = request.form.getlist('flaskManager')
				for m in newManagers:
					nameObj = db_session.query(User).filter(User.name == m).first();
					role = db_session.query(Role).filter(Role.role == 'manager',  Role.email== nameObj.email).first()
					mObject = CampaignManager()
					role.roles_relation.append(mObject)
					oldCamp.campaigns_relation.append(mObject)
					db_session.commit()
				
				#Remove all canvasser asociated with Old Campaign
				db_session.query(CampaignCanvasser).filter(CampaignCanvasser.campaign_id == oldCamp.id).delete()
				db_session.commit()

				#Add new canvasser to Old campaign
				newCanvassers = request.form.getlist('flaskCanvasser')
				for c in newCanvassers:
					nameObj = db_session.query(User).filter(User.name == c).first()
					role = db_session.query(Role).filter(Role.role=='canvasser', Role.email == nameObj.email).first()
					cObject = CampaignCanvasser()
					role.roles_relation_1.append(cObject)
					oldCamp.campaigns_relation_1.append(cObject)
					db_session.commit()


				db_session.commit()




				campaignObject = db_session.query(Campaign)
				return render_template('manager_html/view_campaign.html', camp=campaignObject)
				
		except:
			managerObject = db_session.query(Role).filter(Role.role =='manager')
			canvasObject  = db_session.query(Role).filter(Role.role == 'canvasser')
			campaignName = request.form['new_campaign_name']
			campaignObject = db_session.query(Campaign)

			currentManagers = db_session.query(CampaignManager)
			currentCanvassers = db_session.query(CampaignCanvasser)
			roleList = db_session.query(Role)
			campId = None
			start=None
			end=None
			
			for camp in campaignObject:
				if camp.campaign_name == campaignName:
					campId = camp.id
					start = camp.startDate
					end= camp.endDate
					break
			#############################################
			managerId = []
			for man in currentManagers:
				if man.campaign_id == campId:
					managerId.append(man.user_id)
			
			displayManagers=[]
			for r in roleList:
				if r.id in managerId:
					nameObj = db_session.query(User).filter(User.email== r.email).first();
					displayManagers.append(nameObj.name)

			############################################
			canvasId = []
			for can in currentCanvassers:
				if can.campaign_id == campId:
					canvasId.append(can.user_id)
			

			displayCanvas=[]
			for r in roleList:
				if r.id in canvasId:
					nameObj = db_session.query(User).filter(User.email== r.email).first();
					displayCanvas.append(nameObj.name)
				

			

			return render_template('manager_html/edit_campaign.html', camp=campaignObject, show = campaignName, managers=displayManagers, canvasser=displayCanvas, currentManagers=displayManagers, currentCanvassers=displayCanvas,start=start, end=end)



####################################################################################### CONOR's CODE#######################################################


@bp.route('/create_canvas_assignment')
def createCanvasAssignment():
	result = 1;
	return render_template('manager_html/create_canvas_assignment.html');






@bp.route('/view_canvas_assignment')
def viewCanvasAssignment():
	result = 1;
	return render_template('manager_html/view_canvas_assignment.html');



'''
cam =db_session.query(Campaign).filter(Campiang.campaign_name == "camp1")
for ele in cam.campaigns_relation:
	if (ele.campaign_id ==user1){
	campaigns_relation.remove(ele)
	}
'''
