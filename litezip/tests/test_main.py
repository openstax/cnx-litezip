# -*- coding: utf-8 -*-
from pathlib import Path


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
