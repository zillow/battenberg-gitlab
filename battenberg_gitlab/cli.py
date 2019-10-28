import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # noqa: E402


import logging
from typing import List
from battenberg_gitlab.utils import init_gitlab
from battenberg_gitlab.apply import apply
from battenberg_gitlab.search import parse_project_filters
from battenberg_gitlab.errors import ProjectNotFoundError


logging.basicConfig(level=logging.INFO)


def main(config_file: str = None,
         gitlab_server: str = None,
         group_ids: List[int] = None,
         # Expect filters to be in "<filter type>=<keyword>" format.
         cli_filters: List[str] = None,
         workspace_path: str = None,
         checkout: str = None):

    # TODO ZOMLINFRA-480 Add in click CLI.
    # TODO ZOMLINFRA-480 Stop hard coding the ZO & ZOML specific stuff.
    gitlab_server = 'zgtools'
    group_ids = [109, 108, 106]  # ZOML Gitlab groups
    cli_filters = ['tag=archetype.py-ml']
    checkout = 'v1.1.0'

    project_filters = parse_project_filters(cli_filters)

    gl = init_gitlab(gitlab_server, config_file)

    try:
        apply(gl, group_ids, project_filters, workspace_path, checkout)
    except ProjectNotFoundError:
        print(f'No projects found matching filters: {cli_filters}')


if __name__ == '__main__':
    main()
