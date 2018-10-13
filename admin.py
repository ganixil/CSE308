from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from database import db_session, User, Admin, GlobalVariables

#create the admin blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')


#function to render the admin page and set the admin page url
@bp.route('/adminPage/<u_name>', methods=('GET', 'POST'))
def adminPage(u_name):
	usr_session = db_session.query(User).order_by(User.id)
	gblvar_session = db_session.query(GlobalVariables).first()
	return render_template('admin_html/admin.html',usr_session=usr_session, gblvar_session = gblvar_session,u_name=u_name)


