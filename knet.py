"""
Command line utils for kvadratnet.
"""

import os
import sys
import shutil
import glob
import argparse
from collections import Counter
import kvadratnet


def run_rename(args):
    """
    Batch rename files by adding either a prefix or post to kvadranet identifier.
    """
    files = glob.glob(args.filespec)
    for f in files:
        (folder, filename) = os.path.split(f)
        (base, ext) = os.path.splitext(filename)

        try:
            tilename = kvadratnet.tile_name(base)
        except ValueError:
            print("{}: No kvadratnet tile name found. Skipping.".format(f))
            continue

        new_filename = args.prefix + tilename + args.postfix + ext
        dst = os.path.join(folder, new_filename)
        if args.verbose:
            print("Renaming {src} to {dst}".format(src=base + ext, dst=new_filename))
        os.rename(f, dst)


def run_organize(args):
    """
    Organize files in folders according to a chosen kvadratnet-level.
    """
    # are input units known?
    units = args.unit
    for unit in units:
        if not unit in kvadratnet.UNITS:
            raise ValueError("Unknown unit in units list ({})".format(unit))

    files = glob.glob(args.filespec)

    for f in files:
        (_, filename) = os.path.split(f)
        (base, ext) = os.path.splitext(filename)

        try:
            tilename = kvadratnet.tile_name(base)
        except ValueError:
            print("{}: No kvadratnet tile name found. Skipping.".format(f))
            continue

        sub_dirs = []
        for unit in reversed(kvadratnet.UNITS):
            if not unit in units:
                continue
            try:
                sub_dirs.append(kvadratnet.parent_tile(tilename, unit))
            except ValueError:
                print("ERROR: {0} is smaller than {1}".format(unit, tilename))
                sys.exit(1)

        folder = os.path.sep.join(sub_dirs)
        try:
            os.makedirs(folder)
        except OSError:
            pass

        dst = os.path.join(folder, filename)
        if args.verbose:
            print(
                "Moving {filename} into {folder}".format(
                    filename=filename, folder=folder
                )
            )
        shutil.move(f, dst)


def run_parents(args):
    """
    Create a list of parent tiles from a list of inputs child tiles.
    """
    counter = Counter()
    parents = []
    for line in args.infile:
        try:
            tilename = kvadratnet.tile_name(line.rstrip())
        except ValueError:
            pass
        parent = kvadratnet.parent_tile(tilename)
        parents.append(parent)
        counter[parent] += 1

    if args.unique:
        for key, value in counter.items():
            if args.count:
                print("{:<20} {}".format(key, value))
            else:
                print(key)
    else:
        for parent in parents:
            if args.count:
                print("{:<20} {}".format(parent, counter[parent]))
            else:
                print(parent)


def main():
    """
    Entry point for the knet command line interface of kvadratnet
    """
    parser = argparse.ArgumentParser(prog="knet", description="CLI for kvadratnet")
    subparsers = parser.add_subparsers()

    rename = subparsers.add_parser(
        "rename",
        help="""Rename files with kvadranet-names in them, e.g. add a prefix
                before the cell identifier. If a pre- or postfix is not specified,
                everything but the kvadratnet identifier is stripped from the filename""",
    )
    rename.add_argument(
        "filespec", help="Files to rename. Should be a globbing expression"
    )
    rename.add_argument(
        "--prefix",
        default="",
        help="Text before kvadratnet cell identifier, e.g. prefix_1km_6666_444.tif",
    )
    rename.add_argument(
        "--postfix",
        default="",
        help="Text after kvadratnet cell identifier, e.g. 1km_6666_444_postfix.tif",
    )
    rename.add_argument(
        "--verbose", "-v", action="store_true", help="Be verbose",
    )
    rename.set_defaults(func=run_rename)

    organize = subparsers.add_parser(
        "organize",
        help="""Organize files into subfolders according to supplied
                  list of tile units.""",
    )
    organize.add_argument(
        "filespec",
        help="""Files to move into subfolders. Globbing expression, e.g. "dtm/*.tif".
                Remember the quotation marks.""",
    )
    organize.add_argument(
        "unit",
        nargs="+",
        help="Unit-folders to subdivide files into. More than one unit can be supplied.",
    )
    organize.add_argument(
        "--verbose", "-v", action="store_true", help="Be verbose",
    )
    organize.set_defaults(func=run_organize)

    parents = subparsers.add_parser(
        "parents", help="Create a list of parent tiles based on a list of input tiles",
    )
    parents.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    parents.add_argument(
        "--unique", action="store_true", help="Only show unique parents"
    )
    parents.add_argument(
        "--count", action="store_true", help="Show number of childs for each parent"
    )
    parents.set_defaults(func=run_parents)

    args = parser.parse_args()
    args.func(args)
