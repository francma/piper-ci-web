#!/usr/bin/env python3
from functools import wraps
from typing import Dict, Any, Union

from flask import Flask, render_template, session, redirect, url_for, request, flash
import json

from piper_web.src.identity import *
from piper_web.src.exceptions import *
from piper_web.src.dummy import DummyFacade
from piper_web.src.facade import Facade


class Container:

    def __init__(self, config: Dict[Any, Any]) -> None:
        self.config: Dict[Any, Any] = config
        self.app: Flask = None
        self.facade: Union[DummyFacade, Facade] = None

    def create_facade(self) -> Union[Facade, DummyFacade]:
        if self.config['app']['dummy']:
            return DummyFacade(self.config['core']['base_url'])
        else:
            return Facade(self.config['core']['base_url'])

    def get_app(self) -> Flask:
        if self.app is None:
            self.app = self.create_app(self.create_facade())

        return self.app

    def create_app(self, facade: Union[Facade, DummyFacade]) -> Flask:
        app = Flask(__name__)
        app.secret_key = self.config['app']['secret']

        def authorize(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'token' not in session:
                    identity = None
                else:
                    identity = Identity(session['token'], session['email'])

                return f(identity, *args, **kwargs)
            return decorated_function

        @app.template_filter('pretty_json')
        def pretty_json_filter(s):
            return json.dumps(s, indent=4)

        @app.errorhandler(PiperPermissionError)
        def handle_invalid_usage(error):
            flash('You need to be logged in', 'error')
            return redirect('/login')

        @app.route('/')
        @app.route('/projects')
        @authorize
        def home_view(identity):
            projects = facade.list_projects(identity)
            return render_template('home.html', identity=identity, projects=projects)

        @app.route('/projects/<int:project_id>/builds')
        @authorize
        def project_view(identity, project_id):
            project = facade.get_project(identity, project_id)
            builds = facade.list_builds(identity, project['id'])
            return render_template('project.html', identity=identity, builds=builds, project=project)

        @app.route('/projects/<int:project_id>/builds/<int:build_id>')
        @authorize
        def detail_view(identity, project_id, build_id):
            stages = facade.list_stages(identity, build_id)
            jobs = dict()
            build = facade.get_build(identity, build_id)
            project = facade.get_project(identity, project_id)
            for stage in stages:
                jobs[stage['id']] = facade.list_jobs(identity, stage['id'])

            return render_template('detail.html', identity=identity, project=project, build=build, stages=stages,
                                   jobs=jobs)

        @app.route('/projects/<int:project_id>/builds/<int:build_id>/jobs/<int:job_id>')
        @authorize
        def job_view(identity, project_id, build_id, job_id):
            job = facade.get_job(identity, job_id)
            build = facade.get_build(identity, build_id)
            project = facade.get_project(identity, project_id)

            return render_template('job.html', identity=identity, project=project, build=build, job=job)

        @app.route('/logs/<int:job_id>')
        @authorize
        def log_view(identity, job_id):
            offset = int(request.args.get('offset', 0))

            return facade.get_log(identity, job_id, offset)

        @app.route('/login', methods=['POST', 'GET'])
        def login_view():
            if request.method == 'POST':
                token = request.form['token']
                identity = facade.get_identity(token)
                if identity is None:
                    flash('Invalid token', 'error')
                    redirect(url_for('login'))
                session['token'] = identity.token
                session['email'] = identity.email
                return redirect('/')
            return render_template('login.html')

        @app.route('/logout')
        def logout_view():
            session.pop('token', None)
            session.pop('email', None)
            flash('Logged out')
            return redirect('/')

        return app
