"""Generisk Kvadranet Generator"""


class KNet(object):

    def __init__(self, tile_size, utm_zone, hemisphere='north'):
        self.tile_sizes = {"100m": 100,
                           "250m": 250,
                           "1km": 1000,
                           "10km": 10000,
                           "100km": 100000}

        if tile_size not in self.tile_sizes.keys():
            raise ValueError('Wrong tile-size. Valid inputs are: %s.' % str(list(self.tile_sizes.keys())))

        if hemisphere.lower() not in ['north', 'n', 'south', 's']:
            raise ValueError("Wrong hemisphere-format. Valid inputs are: 'north', 'n', 'south', 's'.")

        self.tile_size = tile_size
        self.utm_zone = utm_zone
        self.hemisphere = hemisphere

    def _validate_coordinate(self, x, y):
        """Test if (x,y) is a valid point for given UTM zone."""
        if x < 0 or y < 0:
            return False



    def tilename_from_point(self, x, y):
        """Return tilename that containts (x,y)"""

class DKNet(KNet):

    def __init(self, tile_size):
        super(KNet, self).__init__(tile_size, 32, 'north')


