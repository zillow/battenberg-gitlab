import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # noqa: E402


import logging
from typing import List
import click
from battenberg_gitlab.utils import init_gitlab
from battenberg_gitlab.apply import apply as apply_projects
from battenberg_gitlab.search import search as search_projects, parse_project_filters
from battenberg_gitlab.errors import ProjectNotFoundError


logger = logging.getLogger('battenberg_gitlab')
# Ensure we always receive debug messages.
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


@click.group()
@click.option(
    '--config-file',
    default=None,
    help='Where to read the python-gitlab configuration from.',
    type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option(
    '--gitlab-id',
    default=None,
    help='Where to read the python-gitlab configuration from.',
    type=click.STRING
)
@click.option(
    '--verbose',
    default=False,
    is_flag=True,
    help='Enables the debug logging.'
)
@click.pass_context
def main(ctx, config_file: str, gitlab_id: str, verbose: bool):
    """
    \f

    Script entry point for Battenberg-gitlab commands.
    """
    ctx.obj = dict()
    ctx.obj.update({
        'config_file': config_file,
        'gitlab_id': gitlab_id,
        'verbose': verbose
    })

    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)


@main.command()
@click.option(
    '--workspace',
    help='Where to locally clone found repos to in the local filesystem. Defaults to /tmp',
    default=None,
    type=click.Path(exists=False)
)
@click.option(
    '--group-name',
    help='Name of the Gitlab group to .',
    type=click.STRING,
    multiple=True
)
@click.option(
    '--project-filter',
    help='Expected to be in "<filter type>=<keyword>" format. Supported types: "tag".',
    type=click.STRING,
    multiple=True
)
@click.pass_context
def search(ctx, workspace: str, group_name: List[str], project_filter: List[str]):
    gl = init_gitlab(ctx.obj['gitlab_id'], ctx.obj['config_file'])
    project_filters = parse_project_filters(project_filter)

    try:
        projects = search_projects(gl, group_name, project_filters, workspace)
    except ProjectNotFoundError:
        logger.info(f'No projects found matching filters: {project_filter}')
        return

    for project, version in projects.items():
        logger.info(f'{project.name}: {version}')


@main.command()
@click.option(
    '--workspace',
    help='Where to locally clone found repos to in the local filesystem. Defaults to /tmp',
    default=None,
    type=click.Path(exists=False)
)
@click.option(
    '--checkout',
    help='Template branch, tag or commit to checkout to apply the upgrade from.',
    default='master',
    type=click.STRING
)
@click.option(
    '--group-name',
    help='Name of the Gitlab group to .',
    type=click.STRING,
    multiple=True
)
@click.option(
    '--project-filter',
    help='Expected to be in "<filter type>=<keyword>" format. Supported types: "tag".',
    type=click.STRING,
    multiple=True
)
@click.pass_context
def apply(ctx, workspace: str, checkout: str, group_name: List[str], project_filter: List[str]):
    gl = init_gitlab(ctx.obj['gitlab_id'], ctx.obj['config_file'])
    project_filters = parse_project_filters(project_filter)

    try:
        apply_projects(gl, group_name, project_filters, workspace, checkout)
    except ProjectNotFoundError:
        logger.info(f'No projects found matching filters: {project_filter}')
