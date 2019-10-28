import os
import logging
import json
from typing import List
from functools import reduce
from gitlab import Gitlab
from pygit2 import Repository
from battenberg import Battenberg
from battenberg.errors import MergeConflictException
from battenberg_gitlab.search import get_projects
from battenberg_gitlab.utils import clone_or_discover_repo, ensure_workspace


logger = logging.getLogger(__name__)


# TODO Remove these once we've we've backfilled .cookiecutter.json
with open(os.path.join(os.path.dirname(__file__), '..', 'templates.json')) as f:
    templates = json.load(f)

def construct_template(project_name: str) -> dict:
    template = {
        **templates['defaults'],
        'project_name': project_name,
        'module_name': project_name.replace('-', '_'),
        **templates['projects'][project_name]
    }
    logging.info(f'Constructing template for {project_name}')
    # logging.info(template)
    return template


def add_template(project_name: str, local_path: str, repo: Repository, merge_target: str):
    # TODO Remove these once we've we've backfilled .cookiecutter.json
    cookiecutter_json_path = os.path.join(local_path, '.cookiecutter.json')
    logger.info(f'Creating .cookiecutter.json file at {cookiecutter_json_path}')
    template = construct_template(project_name)
    with open(cookiecutter_json_path, 'w') as f:
        json.dump(template, f, sort_keys=True, indent=4)

    # Create a new merge_target branch.
    merge_target_ref = f'refs/heads/{merge_target}'
    repo.branches.local.create(merge_target, repo.get(repo.head.target))
    repo.checkout(merge_target_ref)

    # Actually write the .cookiecutter.json to a new commit on the merge_target branch.
    repo.index.add_all()
    repo.index.write()
    tree = repo.index.write_tree()
    repo.create_commit(
        'HEAD',
        repo.default_signature,
        repo.default_signature,
        'Add .cookiecutter.json',
        tree,
        [repo.head.target]
    )
    repo.state_cleanup()
    repo.checkout('HEAD')


def apply(gl: Gitlab,
          group_ids: List[int] = None,
          project_filter: str = None,
          workspace_path: str = None,
          checkout: str = None):
    logger.info(f'Searching Gitlab for projects matching "{project_filter}".')
    projects = get_projects(gl, group_ids, project_filter)
    if not projects:
        raise Exception('No projects found')

    # Create a working directory where we can clone all the projects we've found into.
    workspace_path = ensure_workspace(workspace_path)
    logger.info(f'Created workspace at {workspace_path}')

    merge_conflicts = []
    for project in projects:
        local_path = os.path.join(workspace_path, project.name)
        logger.info(f'Cloning {project.ssh_url_to_repo} to {local_path}')
        repo = clone_or_discover_repo(project.ssh_url_to_repo, local_path)
        
        # TODO Remove add_template once this merge is over.
        merge_target = f'archetype-update-{checkout}'
        try:
            add_template(project.name, local_path, repo, merge_target)
        except KeyError as e:
            logger.error(f'Skipping {project.name}')
            logger.error(e)
            continue

        battenberg = Battenberg(repo)
        try:
            battenberg.upgrade(checkout=checkout, no_input=True, merge_target=merge_target)
        except MergeConflictException as e:
            logger.error(f'Merge conflicts found for {project.name} in {local_path}')
            merge_conflicts.append({
                'project': project,
                'local_path': local_path
            })
    else:
        if merge_conflicts:
            logger.info('Please resolve the merge conflicts listed.')
