import os
import logging
from typing import List
from gitlab import Gitlab
from battenberg import Battenberg
from battenberg.errors import MergeConflictException
from battenberg_gitlab.errors import ProjectNotFoundError
from battenberg_gitlab.search import get_projects
from battenberg_gitlab.utils import clone_or_discover_repo, ensure_workspace


logger = logging.getLogger(__name__)


def apply(gl: Gitlab,
          group_ids: List[int] = None,
          project_filter: str = None,
          workspace_path: str = None,
          checkout: str = None):
    logger.info(f'Searching Gitlab for projects matching "{project_filter}".')
    projects = get_projects(gl, group_ids, project_filter)
    if not projects:
        raise ProjectNotFoundError('No projects found')

    # Create a working directory where we can clone all the projects we've found into.
    workspace_path = ensure_workspace(workspace_path)
    logger.info(f'Created workspace at {workspace_path}')

    merge_conflicts = []
    for project in projects:
        local_path = os.path.join(workspace_path, project.name)
        logger.info(f'Cloning {project.ssh_url_to_repo} to {local_path}')
        repo = clone_or_discover_repo(project.ssh_url_to_repo, local_path)

        battenberg = Battenberg(repo)
        try:
            battenberg.upgrade(
                checkout=checkout,
                no_input=True,
                merge_target=f'archetype-update-{checkout}'
            )
        except MergeConflictException:
            logger.error(f'Merge conflicts found for {project.name} in {local_path}')
            merge_conflicts.append({
                'project': project,
                'local_path': local_path
            })
    else:
        if merge_conflicts:
            logger.info('Please resolve the merge conflicts listed.')
