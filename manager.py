from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from database import db_session, Manager, User

bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/manpage', methods=('GET', 'POST'))
def manPage():
    return render_template('manager_html/create_canvas_assignment.html')
