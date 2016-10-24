# -*- coding: utf-8 -*-
from collections import namedtuple


__all__ = (
    'parse_module',
    'Module',
)


Module = namedtuple('Module', 'id, file, resources')



def parse_module(path):
    """Parse the file structure to a data structure given the path to
    a module directory.

    """
    id = path.name
    file = path / 'index.cnxml'
    resources = tuple(r for r in path.glob('*') if r.name != 'index.cnxml')

    return Module(id, file, resources)
