# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

from .utils import convert_to_relative_paths


def test_completezip2litezip(datadir, tmpdir):
    data_path = Path(str(tmpdir)) / 'col11405'
    shutil.copytree(str(datadir / 'completezip'), str(data_path))

    from litezip.cli import completezip2litezip
    retcode = completezip2litezip([str(data_path)])

    assert retcode == 0

    def _keyed(s): return sorted({t[0]: t[1:] for t in s}.keys())

    from litezip.main import parse_litezip
    data_struct = parse_litezip(data_path)
    expected = parse_litezip(datadir / 'litezip')
    assert _keyed(data_struct) == _keyed(expected)

    relative_expected = convert_to_relative_paths(expected,
                                                  datadir / 'litezip')
    relative_data_struct = convert_to_relative_paths(data_struct, data_path)
    assert relative_data_struct == relative_expected
