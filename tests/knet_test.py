from nose.tools import *
from knet import knet
#from knet.knet import *


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

    @raises(ValueError)
    def test_reduce_ordinate(self):
        knet._reduce_ordinate(6223700, '300m')

    def test_enlarge_ordinate(self):
        assert(knet._enlarge_ordinate(62237, '100m') == 6223700)
        assert(knet._enlarge_ordinate(622375, '250m') == 6223750)
        assert(knet._enlarge_ordinate(6432, '1km') == 6432000)
        assert(knet._enlarge_ordinate(57, '10km') == 570000)
        assert(knet._enlarge_ordinate(620, '50km') == 6200000)
        assert(knet._enlarge_ordinate(62, '100km') == 6200000)

    @raises(ValueError)
    def test_enarge_ordinate2(self):
        knet._enlarge_ordinate(2342, '5km')

    def test_tilename_from_point(self):

        P = self.Pn[0]
        assert_raises(ValueError, knet.tilename_from_point, -1, -1)

        assert(knet.tilename_from_point(P[0], P[1], tile_size='100km') == '100km_62_5')
        assert(knet.tilename_from_point(P[0], P[1], tile_size='50km') == '50km_620_55')
        assert(knet.tilename_from_point(P[0], P[1], tile_size='10km') == '10km_622_57')
        assert(knet.tilename_from_point(P[0], P[1], tile_size='1km') == '1km_6223_575')
        assert(knet.tilename_from_point(P[0], P[1], tile_size='100m') == '100m_62237_5756')
        assert(knet.tilename_from_point(P[0], P[1], tile_size='250m') == '250m_622375_57550')

    def test_validate_tilename(self):
        assert(knet.validate_tilename('1km_2342_234') == True)
        assert(knet.validate_tilename('250m_622375_57550') == True)
        assert(knet.validate_tilename('100m_62237_5756') == True)
        assert(knet.validate_tilename('10km_622_57') == True)
        assert(knet.validate_tilename('50km_620_55') == True)
        assert(knet.validate_tilename('100km_62_5') == True)

        assert(knet.validate_tilename('2km_232_23') == False)
        assert(knet.validate_tilename('100km_234_23') == False)
        assert(knet.validate_tilename('10km_23a_53') == False)
        assert(knet.validate_tilename('notevenatile') == False)

    def test_extent_from_tilename(self):
        xt = knet.extent_from_tilename('1km_6223_575')
        assert(xt == (575000, 6223000, 576000, 6224000))
        xt = knet.extent_from_tilename('10km_622_57')
        assert(xt == (570000, 6220000, 580000, 6230000))


    def test_wkt_from_tilename(self):
        wkt = knet.wkt_from_tilename('1km_6223_575')
        expected_wkt = 'POLYGON((575000.00 6223000.00, 575000.00 6224000.00, 576000.00 6224000.00, '
        expected_wkt+= '576000.00 6223000.00, 575000.00 6223000.00))'
        assert(wkt == expected_wkt)

    def test_parent_tile(self):
        assert(knet.parent_tile('1km_6223_575', '10km') == '10km_622_57')
        assert(knet.parent_tile('100m_62237_5756', '250m') == '250m_622375_57550')
