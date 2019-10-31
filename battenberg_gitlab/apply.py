import logging
from typing import List
from gitlab import Gitlab
from battenberg import Battenberg
from battenberg.errors import MergeConflictException
from battenberg_gitlab.search import clone_projects, ProjectFilters


logger = logging.getLogger(__name__)


def apply(gl: Gitlab,
          group_names: List[str] = None,
          project_filters: ProjectFilters = None,
          workspace_path: str = None,
          checkout: str = None):
    logger.info(f'Searching Gitlab for projects matching {project_filters}.')
    project_repos = clone_projects(gl, group_names, project_filters, workspace_path)

    merge_conflicts = []
    for project, repo in project_repos.items():
        battenberg = Battenberg(repo)
        try:
            battenberg.upgrade(
                checkout=checkout,
                no_input=True,
                merge_target=f'archetype-update-{checkout}'
            )
        except MergeConflictException:
            logger.warning(f'Merge conflicts found for {project.name} in {repo.workdir}')
            merge_conflicts.append({
                'project': project,
                'repo': repo
            })
            continue

        # TODO ZOMLINFRA-498 Automatically create a merge request if no conflicts detected.
    else:
        if merge_conflicts:
            logger.info('Please resolve the merge conflicts listed.')
