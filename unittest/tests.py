from nose.tools import *
from knet.knet import KNet


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

    def test_init_inputs(self):
        assert_raises(ValueError, KNet, '12km', 32, 'n')
        assert_raises(ValueError, KNet, '1000m', 32, 'n')
        assert_raises(ValueError, KNet, '100m', 0, 'n')
        assert_raises(ValueError, KNet, '100m', -1, 'n')
        assert_raises(ValueError, KNet, '100m', 61, 'n')
        assert_raises(ValueError, KNet, '10km', 32, 'p')
        assert_raises(ValueError, KNet, '10km', 32, 'w')

    def test_validate_coordinate_inputs(self):
        N = KNet('100m', 32, 'n')
        S = KNet('250m', 19, 's')
        assert(N._validate_coordinate(0, -1) == False)
        assert(N._validate_coordinate(-1, 500000) == False)
        assert(N._validate_coordinate(-1, -1) == False)

        for P in self.Pn:
            assert(N._validate_coordinate(P[0], P[1]) == True)
        for P in self.Ps:
            assert(S._validate_coordinate(P[0], P[1]) == True)

    def test_tilename_from_point(self):
        K100m = KNet('100m', 32, 'N')
        K250m = KNet('250m', 32, 'N')

        P = self.Pn[0]
        assert(K100m.tilename_from_point(-1, -1) == None)
        assert(K100m.tilename_from_point(P[0], P[1]) == '100m_62238_5757')
        assert(K250m.tilename_from_point(P[0], P[1]) == '250m_622400_57575')

