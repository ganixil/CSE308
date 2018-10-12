from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Admin

#create the admin blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')


#function to render the admin page and set the admin page url
@bp.route('/admPage', methods=('GET', 'POST'))
def admPage():
<<<<<<< HEAD
	return render_template('admin_html/admin.html',session=db_session.query(User).order_by(User.id))
=======
	return render_template('admin_html/admin.html',session=db_session,User=User)



	#HEELO
>>>>>>> 4d58368dc95898e477595f9a67d6cdf8face6e81
