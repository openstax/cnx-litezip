# -*- coding: utf-8 -*-
from pathlib import Path

import pytest


def test_parse_module(datadir):
    module_id = 'm40645'
    data_path = datadir / 'litezip' / module_id

    from litezip.main import parse_module
    data_struct = parse_module(data_path)

    assert data_struct[0] == module_id
    assert data_struct[1] == data_path / 'index.cnxml'
    assert data_struct[2] == (data_path / 'Lab4 Fill Order.png',)


def test_Module_struct(datadir):
    module_id = 'm40645'
    data_path = datadir / 'litezip' / module_id
    content = data_path / 'index.cnxml'
    resources = (data_path / 'Lab4 Fill Order.png',)

    from litezip.main import Module
    data_struct = Module(module_id, content, resources)

    assert len(data_struct) == 3
    assert data_struct.id == module_id
    assert data_struct.file == content
    assert data_struct.resources == (data_path / 'Lab4 Fill Order.png',)


def test_parse_module_without_resources(datadir):
    module_id = 'm42304'
    data_path = datadir / 'litezip' / module_id

    from litezip.main import parse_module
    data_struct = parse_module(data_path)

    assert data_struct[0] == module_id
    assert data_struct[1] == data_path / 'index.cnxml'
    assert data_struct[2] == tuple()


def test_parse_module_raises_missing_file(tmpdir):
    module_id = 'm42000'
    data_path = Path(str(tmpdir.mkdir(module_id)))
    missing_file = data_path / 'index.cnxml'

    from litezip.main import parse_module
    from litezip.exceptions import MissingFile
    with pytest.raises(MissingFile) as exc_info:
        parse_module(data_path)

    assert missing_file == exc_info.value.args[0]
