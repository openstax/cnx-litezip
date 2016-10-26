# -*- coding: utf-8 -*-


def test_validate_litezip(datadir):
    args = [str(datadir / 'litezip')]

    from litezip.cli.validate import main
    retcode = main(args)

    assert retcode == 0


def test_validate_invalid_litezip(datadir, capsys):
    args = [str(datadir / 'invalid_litezip')]

    from litezip.cli.validate import main
    retcode = main(args)

    assert retcode == 1

    out, err = capsys.readouterr()
    assert not out
