import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # noqa: E402


import logging
from typing import List
from gitlab import Gitlab
from battenberg_gitlab.utils import init_gitlab
from battenberg_gitlab.apply import apply


logging.basicConfig(level=logging.INFO)


# TODO Stop hard coding the ZO & ZOML specific stuff.
def main(config_file: str = None,
         gitlab_server: str = 'zgtools',
         group_ids: List[int] = None,
         project_filter: str = 'archetype.py-ml',
         workspace_path: str = None,
         checkout: str = 'archetypev1.1'):

    # TODO Remove hard-code of zoml Gitlab group.
    group_ids = [109, 108, 106]
    
    gl = init_gitlab(config_file, gitlab_server)
    apply(gl, group_ids, project_filter, workspace_path, checkout)


if __name__ == '__main__':
    # TODO Add in click CLI.
    main()
