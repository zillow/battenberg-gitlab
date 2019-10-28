import os
import shutil
from unittest.mock import patch
from battenberg_gitlab.utils import ensure_workspace


@patch('battenberg_gitlab.utils.tempfile')
def test_ensure_workspace(tempfile_mock):
    tempfile_mock.mkdtemp.return_value = 'test-mkdtemp'
    assert ensure_workspace() == 'test-mkdtemp'


def test_ensure_workspace_tmpdir(tmpdir):
    shutil.rmtree(tmpdir)
    assert ensure_workspace(tmpdir) == tmpdir
    assert os.path.exists(tmpdir)
