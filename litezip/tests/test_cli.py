# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

import pytest

from .utils import convert_to_relative_paths


@pytest.fixture
def data_path(datadir, tmpdir):
    """Copies the completezip to a place where we can write over it."""
    data_path = Path(str(tmpdir)) / 'col11405'
    shutil.copytree(str(datadir / 'completezip'), str(data_path))
    return data_path


def assert_equal(data_path, expected_path):
    """Asserts the data at `data_path` is equal to that at `expected_path`."""

    from litezip.main import parse_litezip
    data_struct = parse_litezip(data_path)
    expected = parse_litezip(expected_path)

    def _keyed(s): return sorted({t[0]: t[1:] for t in s}.keys())

    assert _keyed(data_struct) == _keyed(expected)

    relative_expected = convert_to_relative_paths(expected,
                                                  expected_path)
    relative_data_struct = convert_to_relative_paths(data_struct, data_path)
    assert relative_data_struct == relative_expected


def test_completezip2litezip(data_path, datadir):
    from litezip.cli import completezip2litezip
    retcode = completezip2litezip([str(data_path)])

    assert retcode == 0
    assert_equal(data_path, datadir / 'litezip')