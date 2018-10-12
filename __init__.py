import os

from flask import Flask, redirect, url_for
from database import db_session, init_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    init_db()
    # a simple page that says hello
    @app.route('/')
    def start():
        return redirect(url_for('auth.login'))

    import auth
    app.register_blueprint(auth.bp)
    import admin
    app.register_blueprint(admin.bp)
    import manager
    app.register_blueprint(manager.bp)
    import canvasser
    app.register_blueprint(canvasser.bp)
    
    return app
    

if __name__ == "__main__":
    app = create_app()
    app.run()
