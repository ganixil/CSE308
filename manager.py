from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, Manager, User, Campaign

#create the manager blueprint
bp = Blueprint('manager', __name__, url_prefix='/manager')

#function to render the manager page and set the manager page url
@bp.route('/manpage', methods=('GET', 'POST'))
def manPage():
    return render_template('manager_html/create_canvas_assignment.html')


@bp.route('/view_campaign', methods=('GET', 'POST'))
def viewCampaign():
	campaignObject = db_session.query(Campaign)
	return render_template('manager_html/view_campaign.html', camp=campaignObject)