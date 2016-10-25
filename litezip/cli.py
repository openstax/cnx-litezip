# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import shutil
import sys
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
        if output_path.exists():
            print("ERROR: output-dir cannot exist prior to conversion",
                  file=sys.stderr)
            return 1
        shutil.copytree(str(completezip_path), str(output_path))
        completezip_path = output_path

    struct = convert_completezip(completezip_path)

    return 0
