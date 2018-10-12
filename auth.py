import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from database import db_session, User, init_db, Admin, Manager, Canvasser

#create blueprint for auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

#login method url path
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        u = User.query.filter(User.email == email).first()
        #if no user with that name stay on login page
        if(u == None):
            return render_template('index.html')
        #check password
        if(not check_password_hash(u.password, password)):
           #incorrect password stay on login page
            return render_template('index.html')
        #redirects to admin page
        if(u.accType == 'admin'):
            adminUser = Admin.query.filter(Admin.id == u.id).first()
            session.clear()
            session['adminUserId'] = adminUser.id
            return redirect(url_for('admin.admPage'))
        #redirects to manager page
        elif(u.accType == 'manager'):
            managerUser = Manager.query.filter(Manager.id == u.id).first()
            session.clear()
            session['managerUserId'] = managerUser.id
            return redirect(url_for('manager.manPage'))
        #redirects to canvasser page
        else:
            session.clear()
            canvasserUser = Canvasser.query.filter(Canvasser.id == u.id).first()
            session['canvasserUserId'] = canvasserUser.id
            return redirect(url_for('canvasser.canPage'))
        
    return render_template('index.html')
