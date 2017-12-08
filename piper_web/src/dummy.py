from piper_web.src.identity import Identity


class DummyFacade:

    def __init__(self, base_url: str):
        pass

    commands = [
        {
            'id': 1,
            'order': 0,
            'cmd': 'echo Hello!',
        },
        {
            'id': 1,
            'order': 0,
            'cmd': 'echo Hello!',
        },
    ]

    db = {
        'projects': [
            {'id': 1, 'origin': 'origin@origin', 'url': 'http://url.com', 'status': 'running'},
            {'id': 2, 'origin': 'origin@origin', 'url': 'http://url.com', 'status': 'running'},
            {'id': 3, 'origin': 'origin@origin', 'url': 'http://url.com', 'status': 'running'},
        ],
        'builds': [
            {'id': 1, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a',
             'status': 'running'},
            {'id': 2, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a',
             'status': 'running'},
            {'id': 3, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a',
             'status': 'running'},
            {'id': 4, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a',
             'status': 'running'},
            {'id': 5, 'project': 2, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a',
             'status': 'running'},
        ],
        'stages': [
            {'id': 1, 'status': 'running', 'build': 1},
            {'id': 2, 'status': 'running', 'build': 1},
            {'id': 3, 'status': 'running', 'build': 1},
        ],
        'jobs': [
            {'id': 1, 'stage': 1, 'status': 'running', 'image': 'alpine', 'when': 'branch == master',
             'commands': commands},
            {'id': 2, 'stage': 1, 'status': 'running', 'image': 'alpine', 'when': 'branch == master',
             'commands': commands},
            {'id': 3, 'stage': 1, 'status': 'running', 'image': 'alpine', 'when': 'branch == master',
             'commands': commands},
        ],
        'commands': [

        ],
    }

    log = '\033[1;33;40m 33;40 '

    log = 100000 * log

    def get_project(self, identity: Identity, project_id: int):
        for project in self.db['projects']:
            if project['id'] == project_id:
                return project

    def list_projects(self, identity: Identity, offset: int = 0, limit: int = 10):
        return self.db['projects']

    def list_builds(self, identity: Identity, project_id: int, offset: int = 0, limit: int = 10):
        builds = [x for x in self.db['builds'] if x['project'] == project_id]

        return builds

    def list_stages(self, identity: Identity, build_id: int, offset: int = 0, limit: int = 10):
        stages = [x for x in self.db['stages'] if x['build'] == build_id]

        return stages

    def get_job(self, identity: Identity, job_id: int):
        for job in self.db['jobs']:
            if job['id'] == job_id:
                return job

    def list_jobs(self, identity: Identity, stage_id: int, offset: int = 0, limit: int = 10):
        return self.db['jobs']

    def get_log(self, identity: Identity, job_id: int, offset: int):
        limit = 100

        return self.log[offset:offset + limit]

    def get_build(self, identity: Identity, build_id: int):
        for build in self.db['builds']:
            if build['id'] == build_id:
                return build

    def get_identity(self, token: str) -> Identity:
        identity = Identity(token=token, email='me@martinfranc.eu')

        return identity
