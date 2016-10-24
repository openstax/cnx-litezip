# -*- coding: utf-8 -*-
import hashlib
import shutil
from pathlib import Path


def _convert_to_relative_paths(struct, base):
    """Makes the given litezip `struct`'s `Path` objects relative to `base`.

    """
    def _rel(p): return p.relative_to(base)

    new_struct = []
    for obj in struct:
        new_obj = type(obj)(obj.id, _rel(obj.file),
                            tuple([_rel(y) for y in obj.resources]))
        new_struct.append(new_obj)
    return tuple(new_struct)


def test_convert_completezip(datadir, tmpdir):
    data_path = Path(str(tmpdir)) / 'col11405'
    shutil.copytree(str(datadir / 'completezip'), str(data_path))

    from litezip.completezip import convert_completezip
    data_struct = convert_completezip(data_path)

    def _keyed(s): return sorted({t[0]: t[1:] for t in s}.keys())

    from litezip.main import parse_litezip
    expected = parse_litezip(datadir / 'litezip')
    assert _keyed(data_struct) == _keyed(expected)

    relative_expected = _convert_to_relative_paths(expected,
                                                   datadir / 'litezip')
    relative_data_struct = _convert_to_relative_paths(data_struct, data_path)
    assert relative_data_struct == relative_expected

    def _hash_it(x):
        h = hashlib.sha1()
        h.update(x.open('rb').read())
        return h.hexdigest()
    hashes_expected = list([_hash_it(x) for _, x, __ in expected])
    hashes = list([_hash_it(x) for _, x, __ in data_struct])
    assert hashes == hashes_expected
