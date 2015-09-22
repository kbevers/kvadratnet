"""Generisk Kvadranet Generator"""

import math

class KNet(object):

    def __init__(self, tile_size, utm_zone, hemisphere='north'):
        self.tile_sizes = {'100m': 100,
                           '250m': 250,
                           '1km': 1000,
                           '10km': 10000,
                           '50km': 50000,
                           '100km': 100000}

        """ Minimums and maximums. Approximate values. Source:
        https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system """

        self._Nmax_n = 9300000
        self._Nmin_n = 0
        self._Nmax_s = 10000000
        self._Nmin_s = 1100000
        self._Emax = 830000
        self._Emin = 167000

        if tile_size not in self.tile_sizes.keys():
            raise ValueError('Wrong tile-size. Valid inputs are: %s.' % str(list(self.tile_sizes.keys())))

        if utm_zone not in range(1,61):
            raise ValueError('Wrong UTM Zone. Valid numbers are 1..60.')

        if hemisphere.lower() not in ['north', 'n', 'south', 's']:
            raise ValueError("Wrong hemisphere-format. Valid inputs are: 'north', 'n', 'south', 's'.")

        self.tile_size = tile_size
        self.tile_res = self.tile_sizes[self.tile_size]
        self.utm_zone = utm_zone
        self.hemisphere = hemisphere

    def _validate_coordinate(self, N, E):
        """Test if (x,y) is a valid point for given UTM zone.

        At this point the validation is very basic. Probably needs more math to be exact.
        The UTM zone is not taking into account - should be good for now, though."""

        if E > self._Emax or E < self._Emin:
            return False

        if self.hemisphere.lower()[0] == 'n':
            if N > self._Nmax_n or N < self._Nmin_n:
                return False

        if self.hemisphere.lower()[0] == 's':
            if N > self._Nmax_s or N < self._Nmin_s:
                return False

        # If we reach this point, the coordinates are valid!
        return True

    def _reduce_ordinate(self, x):
        ordinate = None

        if math.log10(self.tile_res) % 1 == 0.0:
            # resolution is a power of 10. Use integer division.
            ordinate = math.ceil(x/self.tile_res)
        else:
            # resolution is not a power of 10. Find ratio between current resolution
            # and resolution of the parent tile.
            if self.tile_res == 50000:
                ordinate = math.ceil(x / self.tile_res) * 5

            if self.tile_res == 250:
                ordinate = math.ceil(x / self.tile_res) * 25

        return ordinate

    def tilename_from_point(self, N, E):
        """Return tilename that containts (x,y)"""
        if not self._validate_coordinate(N, E):
            return None

        s = None
        ns = self._reduce_ordinate(N)
        es = self._reduce_ordinate(E)
        s = '%s_%s_%s' % (self.tile_size, ns, es)

        if s is not None:
            print(s)
            return s
        else:
            return None



class DKNet(KNet):

    def __init(self, tile_size):
        super(KNet, self).__init__(tile_size, 32, 'north')


