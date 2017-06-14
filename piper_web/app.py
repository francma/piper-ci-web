#!/usr/bin/env python3
from functools import wraps

from flask import Flask, render_template, session, redirect, url_for, request, flash
import json

from piper_web.identity import Identity
from piper_web.model import *

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def identity(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' not in session:
            ident = None
        else:
            ident = Identity(session['token'], session['email'])

        return f(ident, *args, **kwargs)
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
@identity
def projects(ident):
    return render_template('projects.html', identity=ident, projects=list_projects(ident))


@app.route('/projects/<int:project_id>/builds')
@identity
def builds(ident, project_id):
    return render_template('builds.html', identity=ident, builds=list_builds(ident, project_id), project_id=project_id)


@app.route('/projects/<int:project_id>/builds/<int:build_id>')
@identity
def detail(ident, project_id, build_id):
    stages = list_stages(ident, build_id)
    jobs = dict()
    for stage in stages:
        jobs[stage['id']] = list_jobs(ident, stage['id'])

    return render_template('build.html', identity=ident, project_id=project_id, build_id=build_id, stages=stages, jobs=jobs)


@app.route('/projects/<int:project_id>/builds/<int:build_id>/jobs/<int:job_id>')
@identity
def job_view(ident, project_id, build_id, job_id):
    job = get_job(ident, job_id)

    return render_template('job.html', identity=ident, project_id=project_id, build_id=build_id, job_id=job_id, job=job)


@app.route('/logs/<int:job_id>')
@identity
def log_view(ident, job_id):
    offset = request.args.get('offset', 0)

    return get_log(ident, job_id, offset)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        token = request.form['token']
        identity = get_identity(token)
        if identity is None:
            flash('Invalid token', 'error')
            redirect(url_for('login'))
        session['token'] = identity.token
        session['email'] = identity.email
        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('email', None)
    flash('Logged out')
    return redirect('/')

if __name__ == '__main__':
    app.run()
