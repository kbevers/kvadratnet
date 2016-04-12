"""
Command line utils for kvadratnet.
"""

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

def main():
    """
    Entry point for the knet command line interface of kvadratnet
    """
    parser = argparse.ArgumentParser(prog='knet', description='CLI for kvadratnet')
    subparsers = parser.add_subparsers()

    create = subparsers.add_parser('create',
                                   help="""Create a OGR-writable kvadratnet tile grid that covers
                                        'either a bounding box or a vector-layer""")
    create.add_argument('area',
                        help="""Area that defines the extent of the created kvadratnet
                             tile grid. Can be either a path to a vector geometry file
                             (shp etc., anything that can be read by OGR) or a bounding
                             box on the form [uly ulx lly llx]""")
    create.add_argument('out', help='Output file that stores tile grid. Can be any OGR-writable file type.')
    create.set_defaults(func=run_create)

    tindex = subparsers.add_parser('tindex', help='Create a tile index')
    tindex.add_argument('path', help='Path to index files')
    tindex.add_argument('--exclude', help='Exclude files from path')
    tindex.set_defaults(func=run_tindex)

    args = parser.parse_args()
    args.func(args)
