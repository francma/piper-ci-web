from http import HTTPStatus

import requests

from piper_web.identity import Identity

BASE_URI = 'http://localhost:5001/'


class PiperException(Exception):
    pass


class PiperPermissionError(PiperException):
    pass


def list_projects(identity: Identity, offset: int=0, limit: int=10):
    return _get(identity, 'projects')


def list_builds(identity: Identity, project_id: int, offset: int=0, limit: int=10):
    return _get(identity, 'projects/%d/builds' % project_id)


def get_build(identity: Identity, build_id: int):
    return _get(identity, 'builds/%d' % build_id)


def get_stage(identity: Identity, stage_id: int):
    return _get(identity, 'stages/%d' % stage_id)


def list_stages(identity: Identity, build_id: int, offset: int=0, limit: int=10):
    return _get(identity, 'builds/%d/stages' % build_id)


def list_jobs(identity: Identity, stage_id: int, offset: int=0, limit: int=10):
    return _get(identity, 'stages/%d/jobs' % stage_id)


def get_job(identity: Identity, job_id: int):
    return _get(identity, 'jobs/%d' % job_id)


def get_log(identity: Identity, job_id: int, offset: int):
    return _get(identity, 'jobs/%d/log' % job_id, headers={'Range': ('bytes %d-%d' % offset, offset + 100)})


def get_identity(token: str) -> Identity:
    temp_identity = Identity(token=token, email='')
    r = _get(temp_identity, 'identity')
    identity = Identity(token=r['token'], email=r['email'])

    return identity


def _get(identity, url, *args, **kwargs):
    if identity:
        kwargs['headers'] = {
            'Authorization': 'Bearer ' + identity.token,
        }
    url = BASE_URI + url
    r = requests.get(url, *args, **kwargs)
    if r.status_code in [HTTPStatus.FORBIDDEN, HTTPStatus.UNAUTHORIZED]:
        raise PiperPermissionError
    if r.status_code != HTTPStatus.OK:
        raise PiperException

    return r.json()
