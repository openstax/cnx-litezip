from pathlib import Path

import pytest

from litezip.main import (
    extract_metadata, parse_collection, parse_litezip, parse_module,
    Module, Collection,
)
from litezip.exceptions import MissingFile


def test_Module_struct(datadir):
    id = 'm40645'
    data_path = datadir / 'litezip' / id
    content = data_path / 'index.cnxml'
    resources = (data_path / 'Lab4 Fill Order.png',)

    data_struct = Module(id, content, resources)

    assert len(data_struct) == 3
    assert data_struct.id == id
    assert data_struct.file == content
    assert data_struct.resources == (data_path / 'Lab4 Fill Order.png',)


def test_Collection_struct(datadir):
    id = 'col11405'
    data_path = datadir / 'litezip'
    content = data_path / 'collection.xml'
    resources = tuple()

    data_struct = Collection(id, content, resources)

    assert len(data_struct) == 3
    assert data_struct.id == id
    assert data_struct.file == content
    assert data_struct.resources == tuple()


def test_parse_module(datadir):
    module_id = 'm40645'
    data_path = datadir / 'litezip' / module_id

    data_struct = parse_module(data_path)

    assert data_struct[0] == module_id
    assert data_struct[1] == data_path / 'index.cnxml'
    assert data_struct[2] == (data_path / 'Lab4 Fill Order.png',)


def test_parse_module_without_resources(datadir):
    module_id = 'm42304'
    data_path = datadir / 'litezip' / module_id

    data_struct = parse_module(data_path)

    assert data_struct[0] == module_id
    assert data_struct[1] == data_path / 'index.cnxml'
    assert data_struct[2] == tuple()


def test_parse_module_raises_missing_file(tmpdir):
    module_id = 'm42000'
    data_path = Path(str(tmpdir.mkdir(module_id)))
    missing_file = data_path / 'index.cnxml'

    with pytest.raises(MissingFile) as exc_info:
        parse_module(data_path)

    assert missing_file == exc_info.value.args[0]


def test_parse_collection(datadir):
    col_id = 'col11405'
    data_path = datadir / 'litezip'

    data_struct = parse_collection(data_path)

    assert data_struct[0] == col_id
    assert data_struct[1] == data_path / 'collection.xml'
    assert data_struct[2] == tuple()


def test_parse_collection_raises_missing_file(tmpdir):
    col_id = 'col11405'
    data_path = Path(str(tmpdir.mkdir(col_id)))
    missing_file = data_path / 'collection.xml'

    with pytest.raises(MissingFile) as exc_info:
        parse_collection(data_path)

    assert missing_file == exc_info.value.args[0]


def test_parse_litezip(datadir):
    data_path = datadir / 'litezip'

    data_struct = parse_litezip(data_path)

    assert len(data_struct) == 8
    from litezip.main import Collection, Module
    col = Collection('col11405', data_path / 'collection.xml', tuple())
    assert data_struct[0] == col
    mods = [
        Module('m37154', data_path / 'm37154' / 'index.cnxml', tuple()),
        Module('m40646', data_path / 'm40646' / 'index.cnxml',
               tuple([data_path / 'm40646' / 'Photodiode.png'])),
    ]
    for mod in mods:
        assert mod in data_struct


def test_extract_metadata(litezip_valid_litezip):
    module_filepath = litezip_valid_litezip / 'm42304'

    expected_metadata = {
        'repository': 'http://cnx.org/content',
        'url': 'http://cnx.org/content/m42304/latest',
        'id': 'm42304',
        'title': 'Lab 1-1: 4-Bit Mux and all NAND/NOR Mux',
        'version': '1.3',
        'created': '2012/01/19 22:11:40 -0600',
        'revised': '2012/01/23 22:20:24 -0600',
        'license_url': 'http://creativecommons.org/licenses/by/3.0/',
        'keywords': ['Altera', 'ELEC 220', 'FPGA', 'multiplexor', 'mux',
                     'NAND', 'NOR', 'Quartus'],
        'subjects': ['Science and Technology'],
        'abstract': ('Briefly describes the tasks for Lab 1.1 '
                     'of Rice University\'s ELEC 220 course.'),
        'language': 'en',
    }
    expected_metadata['people'] = {
        'cavallar': {
            'firstname': 'Joseph',
            'surname': 'Cavallaro',
            'fullname': 'Joseph Cavallaro',
            'email': 'cavallar@rice.edu',
        },
        'jedifan42': {
            'firstname': 'Chris',
            'surname': 'Stevenson',
            'fullname': 'Chris Stevenson',
            'email': 'cms11@rice.edu',
        },
    }
    expected_metadata['authors'] = ['jedifan42', 'cavallar']
    expected_metadata['maintainers'] = ['jedifan42', 'cavallar']
    expected_metadata['licensors'] = ['jedifan42', 'cavallar']

    module = parse_module(module_filepath)
    metadata = extract_metadata(module)

    assert metadata == expected_metadata
