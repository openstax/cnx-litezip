# -*- coding: utf-8 -*-
from pathlib import Path

from litezip.main import (
    parse_collection,
    parse_litezip,
    parse_module,
)
from litezip.validate import (
    is_new_identifier,
    is_valid_identifier,
    validate_content,
    validate_litezip,
)


def test_is_valid_identifier():
    assert is_valid_identifier('m40646')
    assert is_valid_identifier('col11405')
    assert is_valid_identifier('NEW')  # for new collection content
    assert is_valid_identifier('mNEW')  # for new module content
    assert is_valid_identifier('mNEW99')  # for new module content
    assert not is_valid_identifier('mi5')


def test_is_new_identifier():
    assert not is_new_identifier('m40646')
    assert not is_new_identifier('col11405')
    assert is_new_identifier('NEW')
    assert is_new_identifier('mNEW')
    assert is_new_identifier('mNEW99')


def test_validate_collection(datadir):
    data_struct = parse_collection(datadir / 'litezip')

    errors = validate_content(data_struct)

    assert not errors


def test_validate_module(datadir):
    data_struct = parse_module(datadir / 'litezip' / 'm40646')

    errors = validate_content(data_struct)

    assert not errors


def test_validate_litezip(datadir):
    data_path = datadir / 'invalid_litezip'
    data_struct = parse_litezip(data_path)

    validation_msgs = validate_litezip(data_struct)

    expected = [
        (Path(data_path / 'collection.xml'),
         '114:13 -- error: element "para" from namespace '
         '"http://cnx.rice.edu/cnxml" not allowed in this context'),
        (Path(data_path / 'mux'), 'mux is not a valid identifier'),
        (Path(data_path / 'mux/index.cnxml'),
         '61:10 -- error: unknown element "foo" from namespace '
         '"http://cnx.rice.edu/cnxml"'),
    ]
    assert validation_msgs == expected
