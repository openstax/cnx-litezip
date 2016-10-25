# -*- coding: utf-8 -*-
import argparse
import shutil
from pathlib import Path

from litezip import convert_completezip


def _arg_parser():
    """Factory for creating the argument parser"""
    description = "Converts a completezip to a litezip"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-o', '--output-dir',
        help="Location to output, rather than converting inplace")
    parser.add_argument(
        'location',
        help="Location of the unpacked completezip")
    return parser


def completezip2litezip(argv=None):
    parser = _arg_parser()
    args = parser.parse_args(argv)

    completezip_path = Path(args.location)
    output_dir = args.output_dir
    if output_dir:
        output_path = Path(output_dir)
        shutil.copytree(str(completezip_path), str(output_path))
        completezip_path = output_path

    struct = convert_completezip(completezip_path)

    return 0
