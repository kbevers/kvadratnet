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
""""
Test suite for the kvadratnet module.
"""

import pytest

import kvadratnet as kn

# pylint: disable=protected-access
# we want to test protected functions without pylint complaining


def test_reduce_ordinate():
    """kvadratnet._reduce_ordinate"""

    with pytest.raises(ValueError):
        kn._reduce_ordinate(6223700, "300m")


def test_enlarge_ordinate():
    """kvadratnet._enlarge_ordinate"""

    with pytest.raises(ValueError):
        kn._enlarge_ordinate(2342, "5km")

    assert kn._enlarge_ordinate(62237, "100m") == 6223700
    assert kn._enlarge_ordinate(622375, "250m") == 6223750
    assert kn._enlarge_ordinate(6432, "1km") == 6432000
    assert kn._enlarge_ordinate(57, "10km") == 570000
    assert kn._enlarge_ordinate(620, "50km") == 6200000
    assert kn._enlarge_ordinate(62, "100km") == 6200000


def test_parse_name():
    """kvadratnet._parse_name"""

    with pytest.raises(ValueError):
        kn._parse_name("BadName")
    assert kn._parse_name("1km_6234_234") == (6234000, 234000, 1000, "1km")
    assert kn._parse_name("punktsky_1km_6234_234.laz") == (
        6234000,
        234000,
        1000,
        "1km",
    )


def test_name_from_point():
    """kvadratnet.name_from_point"""

    point = (6223777, 575617)
    with pytest.raises(ValueError):
        kn.name_from_point(-1, -1)
        kn.name_from_point(point[0], point[1], "23km")

    assert kn.name_from_point(point[0], point[1], unit="100km") == "100km_62_5"
    assert kn.name_from_point(point[0], point[1], unit="50km") == "50km_620_55"
    assert kn.name_from_point(point[0], point[1], unit="10km") == "10km_622_57"
    assert kn.name_from_point(point[0], point[1], unit="1km") == "1km_6223_575"
    assert kn.name_from_point(point[0], point[1], unit="100m") == "100m_62237_5756"
    assert kn.name_from_point(point[0], point[1], unit="250m") == "250m_622375_57550"


def test_validate_name():
    """kvadratnet.validate_name"""

    assert kn.validate_name("1km_2342_234")
    assert kn.validate_name("250m_622375_57550")
    assert kn.validate_name("100m_62237_5756")
    assert kn.validate_name("10km_622_57")
    assert kn.validate_name("50km_620_55")
    assert kn.validate_name("100km_62_5")

    assert kn.validate_name("50km_620_55", units="50km")

    assert kn.validate_name("1km_2342_523", units=["1km", "250m"])
    assert kn.validate_name("1km_2342_523", units=["1km", "250m"], strict=True)

    assert not kn.validate_name("1km_2342_523", units=["10km", "250m"], strict=True)
    assert not kn.validate_name("DTM_1km_5233_782.tif", strict=True)

    assert not kn.validate_name("2km_232_23")
    assert not kn.validate_name("100km_234_23")
    assert not kn.validate_name("10km_23a_53")
    assert not kn.validate_name("notevenatile")

    with pytest.raises(ValueError):
        kn.validate_name("1km_4141_524", ["59km", "1000km"])


def test_extent_from_name():
    """kvadratnet.extent_from_name"""

    with pytest.raises(ValueError):
        kn.extent_from_name("BadName")

    extent = kn.extent_from_name("1km_6223_575")
    assert extent == (575000, 6223000, 576000, 6224000)
    extent = kn.extent_from_name("10km_622_57")
    assert extent == (570000, 6220000, 580000, 6230000)


def test_wkt_from_name():
    """kvadratnet.wkt_from_name"""

    wkt = kn.wkt_from_name("1km_6223_575")
    expected_wkt = (
        "POLYGON((575000.00 6223000.00,575000.00 6224000.00,576000.00 6224000.00,"
    )
    expected_wkt += "576000.00 6223000.00,575000.00 6223000.00))"
    print(wkt)
    print(expected_wkt)
    assert wkt == expected_wkt


def test_parent_tile():
    """kvadratnet.parent_tile"""

    assert kn.parent_tile("1km_6223_575", "10km") == "10km_622_57"
    assert kn.parent_tile("1km_6223_575") == "10km_622_57"
    print(kn.parent_tile("100m_62237_5756", "250m"))
    assert kn.parent_tile("100m_62237_5756", "250m") == "250m_622350_57550"

    with pytest.raises(ValueError):
        kn.parent_tile("100km_62_5")
        kn.parent_tile("10km_423_23", "1km")


def test_tile_name():
    """kvadratnet.tile_name"""
    name = kn.tile_name("dtm_1km_5232_624.tif")
    print(name)
    assert name == "1km_5232_624"

    with pytest.raises(ValueError):
        kn.tile_name("not_a_tile_name")


def test_tile_to_index():
    """kvadratnet.tile_to_index"""
    name = "1km_6232_623"
    idy, idx = kn.tile_to_index(name, 6200000, 600000)
    print(name, idy, idx)
    assert (idy, idx) == (-32, 23)

    name = "1km_6200_600"
    idy, idx = kn.tile_to_index(name, 6200000, 600000)
    print(name, idy, idx)
    assert (idy, idx) == (0, 0)

    name = "1km_6200_600"
    idy, idx = kn.tile_to_index(name, 6200123, 600123)
    print(name, idy, idx)
    assert (idy, idx) == (0, 0)

    name = "1km_6201_599"
    idy, idx = kn.tile_to_index(name, 6200000, 600000)
    print(name, idy, idx)
    assert (idy, idx) == (-1, -1)

    name = "250m_622375_57550"
    idy, idx = kn.tile_to_index(name, 6223750, 575500)
    print(name, idy, idx)
    assert (idy, idx) == (0, 0)
