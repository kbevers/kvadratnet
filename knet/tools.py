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

TILE_SIZES = {'100m': 100,
              '250m': 250,
              '1km': 1000,
              '10km': 10000,
              '50km': 50000,
              '100km': 100000}

def _reduce_ordinate(x, tile_size='1km'):
    ordinate = None
    if not tile_size in TILE_SIZES:
        raise ValueError('Tile size not recognised!')

    tile_res = TILE_SIZES[tile_size]

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

def tilename_from_point(N, E, tile_size='1km'):
    """Return tilename that containts (x,y)"""
    s = None

    if tile_size not in TILE_SIZES:
        raise ValueError('Tile size not regocnized')

    if N < 0 or E < 0:
        raise ValueError('Only positive Northing or Easting accepted')

    ns = _reduce_ordinate(N, tile_size)
    es = _reduce_ordinate(E, tile_size)
    s = '%s_%d_%d' % (tile_size, ns, es)
    print(s)
    return s

def _parse_tilename(tilename):
    raise NotImplemented

    return (N, E)

def bb_from_tilename(tilename):
    """Converts a generic string with a tilename into a bounding box."""
    raise NotImplemented

def wkt_from_tilename(tilename, epsg=None):
    """Create a wkt-polygon from a generic tilename-string."""
    raise NotImplemented

def NE_from_tilename(tilename):
    """Returns reduced eorthing/Easting from tilename."""
    raise NotImplemented
