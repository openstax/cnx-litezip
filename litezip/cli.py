# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

from litezip import convert_completezip


def _arg_parser():
    """Factory for creating the argument parser"""
    description = "Converts a completezip to a litezip"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('location',
                        help="Location of the unpacked completezip")
    return parser


def completezip2litezip(argv=None):
    parser = _arg_parser()
    args = parser.parse_args(argv)

    completezip_path = Path(args.location)
    struct = convert_completezip(completezip_path)

    return 0
