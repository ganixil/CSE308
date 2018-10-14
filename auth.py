import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from database import db_session, User, init_db, Role

#create blueprint for auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

#login method url path
@bp.route('/login',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('choice')  # Use this method for getting options
        error = None
        print("choice = %s" % role)
        if role is not None:
            user = User.query.filter(User.email == email).first()

            if(user is None):  # Without this user.
                error = "This user does not exit!!!!"
            elif(not check_password_hash(user.password, password)):
                error ="Incorrect pasword"

            if error is None: 
                session.clear()
                session['user'] = user.email
                if(role == 'admin'):
                    return redirect(url_for('admin.adminPage',u_name=user.name)) #passing u_name into the html file
        
                elif(role == 'manager'):
                    managerUser = Role.query.filter(Role.email == user.email, Role.role == role).first()
                    session.clear()
                    session['managerUserId'] = managerUser.id
                    return redirect(url_for('manager.manPage',u_name=user.name))
             #redirects to canvasser page
                elif(role == 'canvasser'):
                    session.clear()
                    canvasserUser = Role.query.filter(Role.id == user.email, Role.role == role).first()
                    session['canvasserUserId'] = canvasserUser.id
                    return redirect(url_for('canvasser.canPage',u_name=user.name))
    
    return render_template('index.html')

@bp.route("/logout")
def logout():
    if 'user' in session:
        session.clear()
    return render_template('index.html')
