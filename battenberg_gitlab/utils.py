import os
import logging
import tempfile
from gitlab import Gitlab
from pygit2 import clone_repository, discover_repository, RemoteCallbacks, Repository
from battenberg import construct_keypair


logger = logging.getLogger(__name__)


def init_gitlab(gitlab_id: str = None, config_file: str = None) -> Gitlab:
    if not config_file:
        config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                                   'python-gitlab.cfg'))
    logger.debug(f'Reading gitlab config for gitlab id {gitlab_id} from {config_file}')
    return Gitlab.from_config(gitlab_id, [config_file])


def ensure_workspace(workspace_path: str = None) -> str:
    if not workspace_path:
        workspace_path = tempfile.mkdtemp()
    elif not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    return workspace_path


def clone_or_discover_repo(repo_url: str, local_path: str) -> Repository:
    try:
        return Repository(discover_repository(local_path))
    except Exception:
        # Not found any repo, let's make one.
        pass

    keypair = construct_keypair()
    return clone_repository(repo_url, local_path, callbacks=RemoteCallbacks(credentials=keypair))
