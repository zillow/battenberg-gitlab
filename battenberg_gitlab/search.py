from typing import List
from gitlab import Gitlab


def get_projects(gl: Gitlab, group_ids: List[int] = None, project_filter: str = None):
    if group_ids is None:
        group_ids = []

    projects = []
    for group_id in group_ids:
        group = gl.groups.get(group_id)
        group_projects = group.projects.list(per_page=50)
        if project_filter:
            # TODO Make the filtering smarter.
            group_projects = [gp for gp in group_projects if project_filter in gp.tag_list]
        projects.extend(group_projects)

    return projects
