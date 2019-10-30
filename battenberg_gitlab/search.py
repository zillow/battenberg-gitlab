import os
import logging
from typing import Dict, List, Tuple
from functools import reduce
from enum import Enum
from gitlab import Gitlab
from gitlab.v4.objects import Project
from pygit2 import Repository, RemoteCallbacks
from battenberg import construct_keypair
from battenberg_gitlab.utils import clone_or_discover_repo, ensure_workspace


logger = logging.getLogger(__name__)


class ProjectFilter(Enum):
    TAG = 'tag'


ProjectFilters = List[Tuple[ProjectFilter, str]]
Projects = List[Project]
ProjectRepos = Dict[Project, Repository]
SearchResults = Dict[Project, str]


def parse_project_filters(cli_filters: List[str]) -> ProjectFilters:
    # The CLI accepts filters in "<filter type>=<keyword>" format.
    project_filters = []
    for cli_filter in cli_filters:
        project_filter, keyword = cli_filter.split('=')
        project_filters.append((ProjectFilter(project_filter), keyword))

    return project_filters


def filter_projects(projects: Projects, project_filters: ProjectFilters = None) -> Projects:
    filtered_projects = []
    for project in projects:
        for project_filter, keyword in project_filters:
            if project_filter == ProjectFilter.TAG:
                if keyword in project.tag_list:
                    filtered_projects.append(project)

    return filtered_projects


def get_projects(gl: Gitlab, group_names: List[str] = None,
                 project_filters: ProjectFilters = None) -> Projects:
    if group_names is None:
        group_names = []

    groups = reduce(lambda groups, gn: groups + gl.groups.list(search=gn), group_names, [])
    projects = []
    for group in groups:
        group_projects = group.projects.list(all=True, include_subgroups=True)
        projects.extend(group_projects)
    else:
        projects = filter_projects(projects, project_filters)

    if not projects:
        raise ProjectNotFoundError('No projects found')

    return projects


def clone_projects(gl: Gitlab, group_names: List[str] = None,
                   project_filters: ProjectFilters = None, workspace_path: str = None
                   ) -> ProjectRepos:
    projects = get_projects(gl, group_names, project_filters)

    # Create a working directory where we can clone all the projects we've found into.
    workspace_path = ensure_workspace(workspace_path)
    logger.info(f'Created workspace at {workspace_path}')

    project_repos = {}
    for project in projects:
        local_path = os.path.join(workspace_path, project.name)
        logger.info(f'Cloning {project.ssh_url_to_repo} to {local_path}')
        repo = clone_or_discover_repo(project.ssh_url_to_repo, local_path)
        project_repos[project] = repo
    
    return project_repos


def find_version(repo: Repository) -> str:
    keypair = construct_keypair()
    repo.remotes['origin'].fetch(['template'], callbacks=RemoteCallbacks(credentials=keypair))
    # Return the commit message for the HEAD of the "template" branch.
    return repo[repo.references.get(f'refs/remotes/origin/template').target].message

def search(gl: Gitlab, group_names: List[str] = None,
           project_filters: ProjectFilters = None, workspace_path: str = None) -> SearchResults:
    project_repos = clone_projects(gl, group_names, project_filters, workspace_path)
    return {project: find_version(repo) for project, repo in project_repos.items()}
