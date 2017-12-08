from http import HTTPStatus

import requests

from piper_web.src.exceptions import *
from piper_web.src.identity import Identity


class Facade:

    def __init__(self, core_url: str):
        self.base_url = core_url

    def list_projects(self, identity: Identity, offset: int=0, limit: int=10):
        return self._get(identity, 'projects')

    def list_builds(self, identity: Identity, project_id: int, offset: int=0, limit: int=10):
        return self._get(identity, 'projects/%d/builds' % project_id)

    def get_build(self, identity: Identity, build_id: int):
        return self._get(identity, 'builds/%d' % build_id)

    def get_stage(self, identity: Identity, stage_id: int):
        return self._get(identity, 'stages/%d' % stage_id)

    def list_stages(self, identity: Identity, build_id: int, offset: int=0, limit: int=10):
        return self._get(identity, 'builds/%d/stages' % build_id)

    def list_jobs(self, identity: Identity, stage_id: int, offset: int=0, limit: int=10):
        return self._get(identity, 'stages/%d/jobs' % stage_id)

    def get_job(self, identity: Identity, job_id: int):
        return self._get(identity, 'jobs/%d' % job_id)

    def get_log(self, identity: Identity, job_id: int, offset: int):
        return self._get(identity, 'jobs/%d/log' % job_id, headers={'Range': ('bytes %d-%d' % offset, offset + 100)})

    def get_identity(self, token: str) -> Identity:
        temp_identity = Identity(token=token, email='')
        r = self._get(temp_identity, 'identity')
        identity = Identity(token=r['token'], email=r['email'])

        return identity

    def _get(self, identity, url, *args, **kwargs):
        if identity:
            kwargs['headers'] = {
                'Authorization': 'Bearer ' + identity.token,
            }
        url = self.base_url + url
        r = requests.get(url, *args, **kwargs)
        if r.status_code in [HTTPStatus.FORBIDDEN, HTTPStatus.UNAUTHORIZED]:
            raise PiperPermissionError
        if r.status_code != HTTPStatus.OK:
            raise PiperException

        return r.json()
