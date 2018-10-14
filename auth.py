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
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('choice')  # Use this method for getting options
        print("choice = %s" % role)
        if role is not None:
            user = User.query.filter(User.email == email).first()
            userRole = Role.query.filter(Role.email == email, Role.role == role).first()

            if((user is None) or (userRole is None)):  # Without this user.
                error = "This user does not exit. Please check it again !"
            elif(not check_password_hash(user.password, password)):
                error ="Incorrect password. Please Enter it again !"
            else:
                session.clear()
                session['user'] = email  # Add this user and track it
                if(role == 'admin'):
                    return redirect(url_for('admin.adminPage',u_name=user.name)) #passing u_name into the html file
                elif(role == 'manager'):
                    return redirect(url_for('manager.manPage',u_name=user.name))
                elif(role == 'canvasser'):
                    return redirect(url_for('canvasser.canPage',u_name=user.name))
      
    return render_template('index.html', error= error)


@bp.route("/logout")
def logout():
    if 'user' in session:
        session.clear()
    error = None
    return render_template('index.html', error = error)
