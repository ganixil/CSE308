from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, init_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/admpage', methods=('GET', 'POST'))
def admpage():
    return render_template('admin_html/admin.html')
