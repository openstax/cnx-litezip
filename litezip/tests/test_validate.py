# -*- coding: utf-8 -*-


def test_is_valid_identifier():
    from litezip.validate import is_valid_identifier as target
    assert target('m40646')
    assert target('col11405')
    assert not target('mi5')
