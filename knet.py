"""
Command line utils for kvadratnet.
"""

import os
import glob
import argparse

import kvadratnet

def run_create(args):
    """
    Create kvadratnet CLI option.
    """
    print('knet create')

def run_tindex(args):
    """
    Create tile index.
    """
    print('knet tindex')

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
            if args.verbose:
                print('{}: No kvadratnet tile name found. Skipping.'.format(f))
            continue

        new_filename = args.prefix + tilename + args.postfix + ext
        dst = os.path.join(folder, new_filename)
        if args.verbose:
            print('Renaming {src} to {dst}'.format(src=base+ext, dst=new_filename))
        os.rename(f, dst)



def main():
    """
    Entry point for the knet command line interface of kvadratnet
    """
    parser = argparse.ArgumentParser(prog='knet', description='CLI for kvadratnet')
    subparsers = parser.add_subparsers()

    #create = subparsers.add_parser(
    #    'create',
    #   help="""Create a OGR-writable kvadratnet tile grid that covers
    #           'either a bounding box or a vector-layer""",
    #)
    #create.add_argument(
    #    'area',
    #    help="""Area that defines the extent of the created kvadratnet
    #         tile grid. Can be either a path to a vector geometry file
    #         (shp etc., anything that can be read by OGR) or a bounding
    #         box on the form [uly ulx lly llx]""",
    #)
    #create.add_argument(
    #    'out',
    #    help='Output file that stores tile grid. Can be any OGR-writable file type.',
    #)
    #create.set_defaults(func=run_create)

    #tindex = subparsers.add_parser('tindex', help='Create a tile index')
    #tindex.add_argument('path', help='Path to index files')
    #tindex.add_argument('--exclude', help='Exclude files from path')
    #tindex.set_defaults(func=run_tindex)

    rename = subparsers.add_parser(
        'rename',
        help='''Rename files with kvadranet-names in them, e.g. add a prefix
                before the cell identifier. If a pre- or postfix is not specified,
                everything but the kvadratnet identifier is stripped from the filename''',
    )
    rename.add_argument('filespec', help='Files to rename. Should be a globbing expression')
    rename.add_argument(
        '--prefix',
        default='',
        help='Text before kvadratnet cell identifier, eg prefix_1km_6666_444.tif',
    )
    rename.add_argument(
        '--postfix',
        default='',
        help='Text after kvadratnet cell identifier, eg 1km_6666_444_postfix.tif',
    )
    rename.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Be verbose',
    )
    rename.set_defaults(func=run_rename)

    args = parser.parse_args()
    args.func(args)
