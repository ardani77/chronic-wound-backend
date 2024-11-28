import os
# from flask import(Blueprint, Response, redirect, request)
from flask import Flask, jsonify, render_template
from wound.model.db_setting import *
from wound.keperawatan_luka import controller as keperawatan_luka
from wound.user import controller as user
from wound.auth import controller as auth
from wound.clinic import controller as clinic
from wound.controllers.treatment_group import (
    treatment, wound_history, wound_image, medical_checkup, wound_inspection
)

def create_app(test_config = None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    x = app.config.from_pyfile("../instance/setting.cfg", silent=True)
    global_url_prefix = "/v1"
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(keperawatan_luka.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(treatment.bp, url_prefix=global_url_prefix)
    app.register_blueprint(wound_history.bp, url_prefix=global_url_prefix)
    app.register_blueprint(wound_inspection.bp, url_prefix=global_url_prefix)
    app.register_blueprint(wound_image.bp, url_prefix=global_url_prefix)
    app.register_blueprint(medical_checkup.bp, url_prefix=global_url_prefix)
    app.register_blueprint(clinic.bp)
    
    init_app(app)
    
    #app.register_blueprint(submission.bp)

    ####routing

    """@app.before_request
    def before_request():
        if request.is_secure:
            url = request.url.replace('https://', 'http://', 1)
            code = 301
            return redirect(url, code=code)"""

    @app.route('/index')
    @app.route('/')
    def index():
        your_list= [1,2,3,4]
        return render_template('Login.html', navigation=your_list)

    #@app.route('/test', methods = ["POST"])
    #def post_user():
    #    return "testing"

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    return app 
