from nose.tools import *
from knet.tools import tilename_from_point


class TestKNet(object):
    def setUp(self):
        self.tile_sizes = ['100m', '250m', '1km', '10km', '100km']

        # Some valid coordinates from both hemispheres
        self.Pn = [(6223777, 575617),  # Aarhus, Denmark
                   (7894489, 457373),  # Nordkap, Norway
                   (8598903, 494465)]  # Thule, Greenland

        self.Ps = [(3794420, 608144),  # Cape Horn, Chile
                   (8501476, 179542)]  # Cusco, Peru

    def tearDown(self):
        pass

    def test_tilename_from_point(self):

        P = self.Pn[0]
        assert_raises(ValueError, tilename_from_point, -1, -1)

        assert(tilename_from_point(P[0], P[1], tile_size='100km') == '100km_62_5')
        assert(tilename_from_point(P[0], P[1], tile_size='50km') == '50km_620_55')
        assert(tilename_from_point(P[0], P[1], tile_size='10km') == '10km_622_57')
        assert(tilename_from_point(P[0], P[1], tile_size='1km') == '1km_6223_575')
        assert(tilename_from_point(P[0], P[1], tile_size='100m') == '100m_62237_5756')
        assert(tilename_from_point(P[0], P[1], tile_size='250m') == '250m_622375_57550')

