# Permission to use, copy, modify, and/or distribute this
# software for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission
# notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
# CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF

"""Tiling scheme instpired by the danish 'Kvadratnet'.

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
"""

from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import math
from collections import namedtuple
import re

__version__ = '0.3.0'

UNITS = ['100m', '250m', '1km', '10km', '50km', '100km']

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

REGEX = {'100m': '100m_[0-9]{5}_[0-9]{4}',
         '250m': '250m_[0-9]{6}_[0-9]{5}',
         '1km': '1km_[0-9]{4}_[0-9]{3}',
         '10km': '10km_[0-9]{3}_[0-9]{2}',
         '50km': '50km_[0-9]{3}_[0-9]{2}',
         '100km': '100km_[0-9]{2}_[0-9]'}

TileInfo = namedtuple('TileInfo', 'northing, easting, size, unit')
TileExtent = namedtuple('TileExtent', 'min_easting, min_northing, max_easting, max_northing')

def _reduce_ordinate(ordinate, unit='1km'):
    """
    Reduces UTM ordinate to tile-ordinate.

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
    """
    Enlarges tile ordinate to UTM ordinate.

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

def _parse_name(string):
    """
    Converts tile name to northing, easting, tile unit and tile size in meters.

    Arguments:
      string:         String containing a kvadranet tile identifie identifier

    Returns:
      namedtuple with members northing, easting, size and unit
    """

    name = tile_name(string)

    if not validate_name(name):
        raise ValueError('Not a valid tile name!')

    (unit, northing, easting) = name.split('_')
    northing = _enlarge_ordinate(northing, unit)
    easting = _enlarge_ordinate(easting, unit)
    size = TILE_SIZES[unit]

    return TileInfo(northing, easting, size, unit)

def name_from_point(northing, easting, unit='1km'):
    """
    Return tile name that containts (northing, easting)

    Arguments:
        northing:       y-coordinate of point
        easting:        x-coordinate of point
        unit:           Unit of output tile name. Defaults to 1km.

    Returns:
        tile name containging (northing, easting)
    """
    if unit not in TILE_SIZES:
        raise ValueError('Tile size not regocnized')

    if northing < 0 or easting < 0:
        raise ValueError('Only positive Northing or Easting accepted')

    reduced_northing = _reduce_ordinate(northing, unit)
    reduced_easting = _reduce_ordinate(easting, unit)
    return '{0}_{1}_{2}'.format(unit, reduced_northing, reduced_easting)

def validate_name(name, units=None, strict=False):
    """
    Check if a tile name is valid.

    Arguments:
        name:       Kvadratnet cell identifier
        units:      Unit descriptor or list of unit descriptors to validate against
        strict:     When True names are only valid if the are an exact match,
                    i.e. '1km_6234_423' and not 'DTM_1km_6234_423.tif'

    Returns:
        Boolean
    """

    if not units:
        units = TILE_SIZES.keys()
    else:
        if isinstance(units, str):
            units = [units]

    for unit in units:
        if unit not in TILE_SIZES.keys():
            raise ValueError('{0} is not a valid kvadratnet unit.'.format(unit))

    if strict:
        begin, end = '^', '$'
    else:
        begin, end = '', ''

    for unit in units:
        expr = '{begin}{expr}{end}'.format(begin=begin, expr=REGEX[unit], end=end)
        if re.match(expr, name):
            return True

    return False

def tile_name(string):
    """
    Return only the tile name from a string, e.g. a filename.

    Arguments:
        String:         String containing a tile identifier.

    Returns:
        First detected tile name identifier in string.

    Raises:
        ValueError:     If a tile name identifier was not detected
                        a ValueError exception is raised.
    """
    for expr in REGEX.values():
        match = re.search(expr, string)
        if match:
            return match.group()

    raise ValueError('Tile name identier not detected in string')

def extent_from_name(name):
    """
    Converts a generic string with a tile name into a bounding box.

    Arguments:
        name:       Tile name.

    Returns:
        namedtuple with members min_easting, min_northing, max_easting, max_northing
    """
    if not validate_name(name):
        raise ValueError('Not a valid tile name: {name}'.format(name=name))

    tile = _parse_name(name)

    return TileExtent(tile.easting,
                      tile.northing,
                      tile.easting + tile.size,
                      tile.northing + tile.size)

def wkt_from_name(name):
    """
    Create a wkt-polygon from a generic tile name-string.

    Arguments:
        name:       Tile name.

    Returns:
        WKT polygon with the extent of the input tile.
    """
    #pylint: disable=invalid-name
    # dx and dy seems quite sensible here...

    extent = extent_from_name(name)

    wkt = "POLYGON(("
    for dx, dy in ((0, 0), (0, 1), (1, 1), (1, 0)):
        wkt += "{0:.2f} {1:.2f},".format(extent[2*dx], extent[2*dy+1])
    wkt += "{0:.2f} {1:.2f}))".format(extent[0], extent[1])

    return wkt

def parent_tile(name, parent_unit=''):
    """
    Return parent tile.

    Arguments:
        name:           Name of child tile.
        parent_unit:    Unit of the parent tile, must be large than
                        unit of child tile. Optional.

    Returns:
       Name of parent tile.

    Raises:
        ValueError:     When a tile has not parent or when the tile is
                        larger than the request parent.
    """
    tile = _parse_name(name)
    if parent_unit == '':
        try:
            parent_unit = UNITS[UNITS.index(tile.unit)+1]
        except IndexError:
            # In case we reach the end of UNITS, use the same unit as the original tile input
            raise ValueError('{tile} has no parent tile.'.format(tile=name))

    if TILE_SIZES[tile.unit] >= TILE_SIZES[parent_unit]:
        raise ValueError('Child tile unit is larger than or equal to child unit')

    return name_from_point(tile.northing, tile.easting, parent_unit)

def tile_to_index(name, northing_origin, easting_origin):
    """
    Create indices from tilename.

    Returns a 2D index, (i,j), that is increasing in the eastern direction
    and decreasing in the northern direction. This behaviour is emulating
    that of image files, where the origo is in the top left corner.
    Depending on your origin offsets you might get negative indices. This
    is by design. Usually you would put your origin coordinates in the midle
    of the area your are working in.
    Origin coordinates are given in the same unit as the tiles you are using.
    For instance using (6200, 600) as origin for the 1km_6232_623 tile will
    give you an index of (-32, 23).

    Any origin coordinate can be used, but it will be rounded to the nearest
    multiple of the tile unit, i.e. (6200342, 600421) will be rounded to
    (6200000, 600000)

    Arguments:

        name:               Tile name
        northing_origin:    Northing coordinate of index origin. In same units
                            as tile.
        easting_origin:     Easting coordinate of index origin. In same units
                            as tile.
    Returns:
        2D-index (northing, easting)
    """
    if not validate_name(name):
        raise ValueError('Invalid tile name')

    tile = _parse_name(name)

    # round origin to nearest multiple of tile unit
    easting_rounded = round(easting_origin/tile.size)*tile.size
    northing_rounded = round(northing_origin/tile.size)*tile.size

    idx = (tile.easting - easting_rounded) / tile.size
    idy = (northing_rounded - tile.northing) / tile.size

    return idy, idx
