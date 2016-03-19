"""Quadratic tile naming instpired by the danish 'Kvadratnet'.

Glossary:

    Tile:               A square tile in the kvadratnet. A tile has a name, unit, position
                        and size. The tiles extents are described in UTM coordinates.
                        By design the tile naming scheme is indifferent to which UTM zone
                        they are used in. Originally the tiling scheme was created for use
                        in Danish public administration but is now also used in other parts
                        of the world.

    (Tile) name         A tile name consists of a unit descriptor and reduced coordinates
                        of the lower left corner. E.g. 1km_6342_523, 10km_543_73

    (Tile) unit:        The first part of a tile name, i.e. 1km, 250m or 100km.

    Tile coordinates:   The numbers in the tile name. In combination with the tile unit
                        they describe the UTM coordinates of the lower left corner of the tile.

    (Tile) size:        Side length of tile. In meters.

    Tile ordinate:      One of the values in a set of tile coordinates.

    UTM ordinate:       One of the values in a set of UTM coordinates.


TODO:

    Implement as an app and an API.

    App:

      knet tindex --zone=24 *.tif output.json
      knet create 10km --bbox=[Nmin Nmax Emin Emax]


"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import math
from collections import namedtuple
import re

# actual size of tiles. In meters.
TILE_SIZES = {'100m': 100,
              '250m': 250,
              '1km': 1000,
              '10km': 10000,
              '50km': 50000,
              '100km': 100000}

# zeros needed to convert N/E in tile name to full coordinate values.
TILE_FACTORS = {'100m': 100,
                '250m': 10,
                '1km': 1000,
                '10km': 10000,
                '50km': 10000,
                '100km': 100000}

TileInfo = namedtuple('TileInfo', 'northing, easting, size, unit')
TileExtent = namedtuple('TileExtent', 'min_easting, min_northing, max_easting, max_northing')

def _reduce_ordinate(ordinate, unit='1km'):
    """Reduces UTM ordinate to tile-ordinate.

    Example:
        _reduce_ordinate(6432523, '1km') returns 6432.

    Arguments:
        ordinate:
        unit:      Tile unit that ordinate should be reduced to.

    Returns:
        Reduced tile ordinate.
    """
    reduced = None
    try:
        tile_res = TILE_SIZES[unit]
    except:
        raise ValueError('Tile unit not recognised!')

    if math.log10(tile_res) % 1 == 0.0:
        # resolution is a power of 10. Use integer division.
        reduced = math.floor(ordinate / tile_res)
    else:
        # resolution is not a power of 10. Find ratio between current resolution
        # and resolution of the parent tile.
        if tile_res == 50000:
            reduced = math.floor(ordinate / tile_res) * 5

        if tile_res == 250:
            reduced = math.floor(ordinate / tile_res) * 25

    return int(reduced)

def _enlarge_ordinate(ordinate, unit='1km'):
    """Enlarges tile ordinate to UTM ordinate.

    Example:
        knet._enlarge_ordinate(6432, '1km') returns 6432000.

    Arguments:
        ordinate:              Tile ordinate.
        unit:           Tile unit that the tile ordinate corresponds to.

    Returns.
        Enlarged UTM ordinate.
    """
    try:
        factor = TILE_FACTORS[unit]
    except:
        raise ValueError('Tile unit not recognised!')

    return factor*int(ordinate)

def _parse_name(name):
    """Converts tile name to northing, easting, tile unit and tile size in meters.

    Arguments:
      name:         Name of kvadranet tile

    Returns:
      namedtuple with members northing, easting, size and unit
    """

    if not validate_name(name):
        raise ValueError('Not a valid tile name!')

    (unit, northing, easting) = name.split('_')
    northing = _enlarge_ordinate(northing, unit)
    easting = _enlarge_ordinate(easting, unit)
    size = TILE_SIZES[unit]

    return TileInfo(northing, easting, size, unit)

def name_from_point(northing, easting, unit='1km'):
    """Return tile name that containts (x,y)"""
    if unit not in TILE_SIZES:
        raise ValueError('Tile size not regocnized')

    if northing < 0 or easting < 0:
        raise ValueError('Only positive Northing or Easting accepted')

    reduced_northing = _reduce_ordinate(northing, unit)
    reduced_easting = _reduce_ordinate(easting, unit)
    return '{0}_{1}_{2}'.format(unit, reduced_northing, reduced_easting)


def validate_name(name):
    """Check if a tile name is valid.

    Arguments:
        name:     Kvadratnet cell identifier
        strict:
    """

    regex = ['100m_[0-9]{5}_[0-9]{4}',
             '250m_[0-9]{6}_[0-9]{5}',
             '1km_[0-9]{4}_[0-9]{3}',
             '10km_[0-9]{3}_[0-9]{2}',
             '50km_[0-9]{3}_[0-9]{2}',
             '100km_[0-9]{2}_[0-9]']

    for expr in regex:
        if re.match(expr, name):
            return True

    return False

def extent_from_name(name):
    """Converts a generic string with a tile name into a bounding box."""
    if not validate_name(name):
        raise ValueError('Not a valid tile name')

    tile = _parse_name(name)

    return TileExtent(tile.easting,
                      tile.northing,
                      tile.easting + tile.size,
                      tile.northing + tile.size)

def wkt_from_name(name):
    """Create a wkt-polygon from a generic tile name-string."""
    #pylint: disable=invalid-name
    # dx and dy seems quite sensible here...

    extent = extent_from_name(name)

    wkt = "POLYGON(("
    for dx, dy in ((0, 0), (0, 1), (1, 1), (1, 0)):
        wkt += "{0:.2f} {1:.2f},".format(extent[2*dx], extent[2*dy+1])
    wkt += "{0:.2f} {1:.2f}))".format(extent[0], extent[1])

    return wkt

def parent_tile(name, parent_unit):
    """Return parent tile."""
    tile = _parse_name(name)
    return name_from_point(tile.northing, tile.easting, parent_unit)

