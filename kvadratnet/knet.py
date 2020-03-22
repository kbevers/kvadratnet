"""
Command line utils for kvadratnet.
"""

import os
import sys
import shutil
from collections import Counter

import click

import kvadratnet as kn


@click.group()
def cli():
    """
    CLI for kvadratnet
    """


@cli.command()
@click.argument(
    "files", nargs=-1, required=True, type=click.Path("r"),
)
@click.option(
    "--prefix",
    default="",
    help="Text before kvadratnet cell identifier, e.g. prefix_1km_6666_444.tif",
)
@click.option(
    "--postfix",
    default="",
    help="Text after kvadratnet cell identifier, e.g. 1km_6666_444_postfix.tif",
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Be verbose",
)
def rename(files, prefix, postfix, verbose):
    """
    Batch rename files with kvadranet-names in them, e.g. add a prefix
    before the cell identifier. If a pre- or postfix is not specified,
    everything but the kvadratnet identifier is stripped from the filename


    FILES is a list of files to be renamed. Can be a globbing expression,
    e.g. 'dtm/*.tif'.
    """
    for f in files:
        (folder, filename) = os.path.split(f)
        (base, ext) = os.path.splitext(filename)

        try:
            tilename = kn.tile_name(base)
        except ValueError:
            print("{}: No kvadratnet tile name found. Skipping.".format(f))
            continue

        new_filename = prefix + tilename + postfix + ext
        dst = os.path.join(folder, new_filename)
        if verbose:
            print("Renaming {src} to {dst}".format(src=base + ext, dst=new_filename))
        os.rename(f, dst)


@cli.command()
@click.argument(
    "units", required=True,
)
@click.argument(
    "files", nargs=-1, type=click.Path("r"),
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Be verbose",
)
def organize(units, files, verbose):
    """
    Organize files into subfolders according to supplied
    list of tile units.

    FILES is a list of files thatrepresents files to be organized. Can be a
    globbing expression, e.g. 'dtm/*.tif'.

    UNITS is a list of units representing folders that files will be re-organized
    into. Allowed units are 100m, 250m, 1km, 10kmm 50km, and 100km. The list has
    to be quoted string, e.g. "100km 10km".
    """

    # are input units known?
    for unit in units.split():
        if not unit in kn.UNITS:
            raise ValueError("Unknown unit in units list ({})".format(unit))

    for f in files:
        (_, filename) = os.path.split(f)
        (base, ext) = os.path.splitext(filename)

        try:
            tilename = kn.tile_name(base)
        except ValueError:
            print("{}: No kvadratnet tile name found. Skipping.".format(f))
            continue

        sub_dirs = []
        for unit in reversed(kn.UNITS):
            if not unit in units:
                continue
            try:
                sub_dirs.append(kn.parent_tile(tilename, unit))
            except ValueError:
                print("ERROR: {0} is smaller than {1}".format(unit, tilename))
                sys.exit(1)

        folder = os.path.sep.join(sub_dirs)
        try:
            os.makedirs(folder)
        except OSError:
            pass

        dst = os.path.join(folder, filename)
        if verbose:
            print(
                "Moving {filename} into {folder}".format(
                    filename=filename, folder=folder
                )
            )
        shutil.move(f, dst)


@cli.command()
@click.argument(
    "files", nargs=-1, required=True, type=click.Path("r"),
)
@click.option(
    "--unique", is_flag=True, help="Only show unique parents",
)
@click.option(
    "--count", is_flag=True, help="Show number of childs for each parent",
)
def parents(files, unique, count):
    """
    Create a list of parent tiles from a list of inputs child tiles.

    FILES is a list of files that represent child files. Can be globbing
    expression, e.g. dtm/*.tif.
    """

    counter = Counter()
    parent_list = []
    for filename in files:
        try:
            tilename = kn.tile_name(filename.rstrip())
        except ValueError:
            continue
        parent = kn.parent_tile(tilename)
        parent_list.append(parent)
        counter[parent] += 1

    if unique:
        for key, value in counter.items():
            if count:
                print("{:<20} {}".format(key, value))
            else:
                print(key)
    else:
        for parent in parent_list:
            if count:
                print("{:<20} {}".format(parent, counter[parent]))
            else:
                print(parent)
