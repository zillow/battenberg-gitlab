from typing import List, Tuple
from enum import Enum
from gitlab import Gitlab


class ProjectFilter(Enum):
    TAG = 'tag'


ProjectFilters = List[Tuple[ProjectFilter, str]]
Projects = List[Gitlab.v4.objects.Project]


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


def get_projects(gl: Gitlab, group_ids: List[int] = None,
                 project_filters: ProjectFilters = None) -> Projects:
    if group_ids is None:
        group_ids = []

    projects = []
    for group_id in group_ids:
        group = gl.groups.get(group_id)
        group_projects = group.projects.list(per_page=50)
        projects.extend(group_projects)
    else:
        projects = filter_projects(projects, project_filters)

    return projects
