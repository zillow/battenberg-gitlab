import os
import shutil
from unittest.mock import patch, ANY
import pytest
from battenberg_gitlab.utils import init_gitlab, ensure_workspace, clone_or_discover_repo



@pytest.fixture
def Repository():
    with patch('battenberg_gitlab.utils.Repository') as Repository:
        yield Repository


@pytest.fixture
def discover_repository():
    with patch('battenberg_gitlab.utils.discover_repository') as discover_repository:
        yield discover_repository


@pytest.mark.parametrize('config_file,expected', (
    (None, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-gitlab.cfg'))),
    ('test-config_file', 'test-config_file')
))
@patch('battenberg_gitlab.utils.Gitlab.from_config')
def test_init_gitlab(from_config, config_file, expected):
    gitlab_id = 'test-gitlab_id'
    assert init_gitlab(gitlab_id, config_file) == from_config.return_value
    from_config.assert_called_once_with(gitlab_id, [expected])


@patch('battenberg_gitlab.utils.tempfile')
def test_ensure_workspace(tempfile_mock):
    tempfile_mock.mkdtemp.return_value = 'test-mkdtemp'
    assert ensure_workspace() == 'test-mkdtemp'


def test_ensure_workspace_tmpdir(tmpdir):
    shutil.rmtree(tmpdir)
    assert ensure_workspace(tmpdir) == tmpdir
    assert os.path.exists(tmpdir)


def test_discover_repo(Repository, discover_repository):
    path = 'test-path'
    assert clone_or_discover_repo('test-repo_url', path) == Repository.return_value
    Repository.assert_called_once_with(discover_repository.return_value)
    discover_repository.assert_called_once_with(path)


@patch('battenberg_gitlab.utils.clone_repository')
def test_clone_repo(clone_repository, Repository, discover_repository):
    repo_url = 'test-repo_url'
    path = 'test-path'
    discover_repository.side_effect = Exception('No repo found')
    assert clone_or_discover_repo(repo_url, path) == clone_repository.return_value
    clone_repository.assert_called_once_with(repo_url, path, callbacks=ANY)
