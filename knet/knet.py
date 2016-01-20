"""Quadratic tile naming instpired by the danish 'Kvadratnet'.

TODO:

    Implement as an app and an API.

    App:

      knet tindex --zone=24 *.tif output.json
      knet create 10km --bbox=[Nmin Nmax Emin Emax]


    API:

      tilename2wkt() / wkt2tilename()?
      point2tilename(x,y)

"""

import math
import re

# actual size of tiles. In meters.
TILE_SIZES = {'100m': 100,
              '250m': 250,
              '1km': 1000,
              '10km': 10000,
              '50km': 50000,
              '100km': 100000}

# zeros needed to convert N/E in tilename to full coordinate values.
TILE_FACTORS = {'100m': 100,
                '250m': 10,
                '1km': 1000,
                '10km': 10000,
                '50km': 10000,
                '100km': 100000}

def _reduce_ordinate(x, tile_size='1km'):
    ordinate = None
    try:
      tile_res = TILE_SIZES[tile_size]
    except:
        raise ValueError('Tile size not recognised!')

    if math.log10(tile_res) % 1 == 0.0:
        # resolution is a power of 10. Use integer division.
        ordinate = math.floor(x / tile_res)
    else:
        # resolution is not a power of 10. Find ratio between current resolution
        # and resolution of the parent tile.
        if tile_res == 50000:
            ordinate = math.floor(x / tile_res) * 5

        if tile_res == 250:
            ordinate = math.floor(x / tile_res) * 25

    return ordinate

def _enlarge_ordinate(x, tile_size='1km'):
    try:
        f = TILE_FACTORS[tile_size]
    except:
        raise ValueError('Tile size not recognised!')

    return f*int(x)

def _parse_tilename(tilename):
    """Converts tilename to Northing, Easting and cell size in meters.

    Arguments:
      tilename:     Kvadranet cell

    Returns:
      4-tuple:      (N, E, cell_size, unit). All values in meters.
    """

    if not validate_tilename(tilename):
        raise ValueError('Not a valid tilename!')

    (tile_size, N, E) = tilename.split('_')
    N = _enlarge_ordinate(N, tile_size)
    E = _enlarge_ordinate(E, tile_size)
    cell_size = TILE_SIZES[tile_size]
    return (N, E, cell_size, tile_size)

def tilename_from_point(N, E, tile_size='1km'):
    """Return tilename that containts (x,y)"""
    if tile_size not in TILE_SIZES:
        raise ValueError('Tile size not regocnized')

    if N < 0 or E < 0:
        raise ValueError('Only positive Northing or Easting accepted')

    ns = _reduce_ordinate(N, tile_size)
    es = _reduce_ordinate(E, tile_size)
    s = '%s_%d_%d' % (tile_size, ns, es)
    return s


def validate_tilename(tilename):
    """Check if a tilename is valid.

    Arguments:
        tilename:     Kvadratnet cell identifier
        strict:       """

    regex = ['100m_[0-9]{5}_[0-9]{4}',
             '250m_[0-9]{6}_[0-9]{5}',
             '1km_[0-9]{4}_[0-9]{3}',
             '10km_[0-9]{3}_[0-9]{2}',
             '50km_[0-9]{3}_[0-9]{2}',
             '100km_[0-9]{2}_[0-9]']

    for expr in regex:
        if re.match(expr, tilename):
            return True

    return False

def extent_from_tilename(tilename):
    """Converts a generic string with a tilename into a bounding box."""
    if not validate_tilename(tilename):
        raise ValueError('Not a valid tilename')

    (N, E, cell_size, _) = _parse_tilename(tilename)
    N, E = tilename.split("_")[1:3]
    N = int(N)
    E = int(E)
    xt = (E*cell_size, N*cell_size, (E+1)*cell_size, (N+1)*cell_size)
    return xt

def wkt_from_tilename(tilename, epsg=None):
    """Create a wkt-polygon from a generic tilename-string."""
    xt = extent_from_tilename(tilename)

    wkt="POLYGON(("
    for dx, dy in ((0,0), (0,1), (1,1), (1,0)):
        wkt += "{0:.2f} {1:.2f}, ".format(xt[2*dx], xt[2*dy+1])
    wkt += "{0:.2f} {1:.2f}))".format(xt[0], xt[1])

    return wkt

def parent_tile(tilename, parent_tilesize):
    """Return parent tile."""
    (N, E, cell_size, unit) = _parse_tilename(tilename)
    return tilename_from_point(N, E, parent_tilesize)

