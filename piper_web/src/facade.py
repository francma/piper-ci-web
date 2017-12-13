from http import HTTPStatus

import requests

from piper_web.src.exceptions import *
from piper_web.src.identity import Identity


class Facade:

    def __init__(self, core_url: str):
        if core_url[-1] != '/':
            core_url += '/'
        self.base_url = core_url

    def get_project(self, identity: Identity, project_id: int):
        return self._get(identity, 'projects/%d' % project_id)

    def list_projects(self, identity: Identity, offset: int=0, limit: int=10):
        return self._get(identity, 'projects')

    def list_builds(self, identity: Identity, project_id: int, offset: int=0, limit: int=10):
        return self._get(identity, 'projects/%d/builds' % project_id)

    def get_build(self, identity: Identity, build_id: int):
        return self._get(identity, 'builds/%d' % build_id)

    def cancel_build(self, identity: Identity, build_id: int):
        self._cancel(identity, 'builds', build_id)

    def restart_build(self, identity: Identity, build_id: int):
        self._restart(identity, 'builds', build_id)

    def get_stage(self, identity: Identity, stage_id: int):
        return self._get(identity, 'stages/%d' % stage_id)

    def list_stages(self, identity: Identity, build_id: int, offset: int=0, limit: int=10):
        return self._get(identity, 'builds/%d/stages?order=order-asc' % build_id)

    def cancel_stage(self, identity: Identity, stage_id: int):
        self._cancel(identity, 'stages', stage_id)

    def restart_stage(self, identity: Identity, stage_id: int):
        self._restart(identity, 'stages', stage_id)

    def list_jobs(self, identity: Identity, stage_id: int, offset: int=0, limit: int=10):
        return self._get(identity, 'stages/%d/jobs' % stage_id)

    def get_job(self, identity: Identity, job_id: int):
        return self._get(identity, 'jobs/%d' % job_id)

    def cancel_job(self, identity: Identity, job_id: int):
        self._cancel(identity, 'jobs', job_id)

    def restart_job(self, identity: Identity, job_id: int):
        self._restart(identity, 'jobs', job_id)

    def get_log(self, identity: Identity, job_id: int, offset: int):
        url = self.base_url + 'jobs/%d/log' % job_id
        headers = {
            'Range': 'bytes %d-' % offset,
        }
        if identity:
            headers['Authorization'] = 'Bearer ' + identity.token

        r = requests.get(url, headers=headers)
        if r.status_code in [HTTPStatus.FORBIDDEN, HTTPStatus.UNAUTHORIZED]:
            raise PiperPermissionError
        if r.status_code not in [HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT]:
            raise PiperException(r.status_code)

        return r.content

    def get_identity(self, token: str) -> Identity:
        temp_identity = Identity(token=token, email='')
        r = self._get(temp_identity, 'identity')
        identity = Identity(token=r['token'], email=r['email'])

        return identity

    def _get(self, identity, url, *args, **kwargs):
        if identity:
            if 'headers' not in kwargs:
                kwargs['headers'] = dict()
            kwargs['headers']['Authorization'] = 'Bearer ' + identity.token
        url = self.base_url + url
        r = requests.get(url, *args, **kwargs)
        if r.status_code in [HTTPStatus.FORBIDDEN, HTTPStatus.UNAUTHORIZED]:
            raise PiperPermissionError
        if r.status_code != HTTPStatus.OK:
            raise PiperException(r.status_code)

        return r.json()

    def _restart(self, identity, what, idx):
        url = self.base_url + what + '/' + str(idx) + '/restart'
        headers = dict()
        headers['Authorization'] = 'Bearer ' + identity.token
        r = requests.post(url, headers=headers)
        if r.status_code in [HTTPStatus.FORBIDDEN, HTTPStatus.UNAUTHORIZED]:
            raise PiperPermissionError
        if r.status_code != HTTPStatus.OK:
            raise PiperInvalidOperation(r.status_code)

    def _cancel(self, identity, what, idx):
        url = self.base_url + what + '/' + str(idx) + '/cancel'
        headers = dict()
        headers['Authorization'] = 'Bearer ' + identity.token
        r = requests.post(url, headers=headers)
        if r.status_code in [HTTPStatus.FORBIDDEN, HTTPStatus.UNAUTHORIZED]:
            raise PiperPermissionError
        if r.status_code != HTTPStatus.OK:
            raise PiperInvalidOperation(r.status_code)
