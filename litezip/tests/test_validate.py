# -*- coding: utf-8 -*-
import pytest


def test_is_valid_identifier():
    from litezip.validate import is_valid_identifier as target
    assert target('m40646')
    assert target('col11405')
    assert not target('mi5')


def test_validate_collection(datadir):
    from litezip.main import parse_collection
    data_struct = parse_collection(datadir / 'litezip')

    from litezip.validate import validate_content
    errors = validate_content(data_struct)

    assert not errors


def test_validate_module(datadir):
    from litezip.main import parse_module
    data_struct = parse_module(datadir / 'litezip' / 'm40646')

    from litezip.validate import validate_content
    errors = validate_content(data_struct)

    assert not errors
