from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, User, Admin

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/admPage', methods=('GET', 'POST'))
def admPage():
    return render_template('admin_html/admin.html')
