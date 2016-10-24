# -*- coding: utf-8 -*-
from pathlib import Path

from .main import parse_litezip


__all__ = (
    'convert_completezip',
)


def convert_completezip(path):
    """Converts a completezip file structure to a litezip file structure.
    Returns a litezip data structure.

    """
    for filepath in path.glob('**/index_auto_generated.cnxml'):
        filepath.rename(filepath.parent / 'index.cnxml')
    return parse_litezip(path)
