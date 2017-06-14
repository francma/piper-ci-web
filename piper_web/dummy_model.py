from piper_web.identity import Identity


db = {
    'projects': [
        {'id': 1, 'origin': 'origin@origin', 'url': 'http://url.com', 'status': 'running'},
        {'id': 2, 'origin': 'origin@origin', 'url': 'http://url.com', 'status': 'running'},
        {'id': 3, 'origin': 'origin@origin', 'url': 'http://url.com', 'status': 'running'},
    ],
    'builds': [
        {'id': 1, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a', 'status': 'running'},
        {'id': 2, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a', 'status': 'running'},
        {'id': 3, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a', 'status': 'running'},
        {'id': 4, 'project': 1, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a', 'status': 'running'},
        {'id': 5, 'project': 2, 'branch': 'master', 'commit': '634721d9da222050d41dce164d9de35fe475aa7a', 'status': 'running'},
    ],
    'stages': [
        {'id': 1, 'status': 'running', 'build': 1},
        {'id': 2, 'status': 'running', 'build': 1},
        {'id': 3, 'status': 'running', 'build': 1},
    ],
    'jobs': [
        {'id': 1, 'stage': 1, 'status': 'running'},
        {'id': 2, 'stage': 1, 'status': 'running'},
        {'id': 3, 'stage': 1, 'status': 'running'},
    ],
}


def list_projects(identity: Identity, offset: int=0, limit: int=10):
    return db['projects']


def list_builds(identity: Identity, project_id: int, offset: int=0, limit: int=10):
    builds = [x for x in db['builds'] if x['project'] == project_id]

    return builds


def get_build(identity: Identity, build_id: int):
    for build in db['builds']:
        if build['id'] == build_id:
            return build
