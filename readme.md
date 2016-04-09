# kvadratnet

Kvadratnet is a set of tools that makes working with the Danish Kvadratnet easier.

[![Build Status](https://travis-ci.org/kbevers/kvadratnet.svg?branch=master)](https://travis-ci.org/kbevers/kvadratnet)
[![Coverage Status](https://coveralls.io/repos/github/kbevers/kvadratnet/badge.svg?branch=master)](https://coveralls.io/github/kbevers/kvadratnet?branch=master)

## Introduction

The Danish Kvadratnet is a geographical tiling scheme based on UTM coordinates.
The tiling scheme is a national standard for dividing nation-wide geographical
datasets into smaller pieces.

Originally created as collaboration between [Statitics Denmark](http://dst.dk/) and the
[National Survey and Cadastre of Denmark](http://sdfe.dk/) the Danish Kvadratnet was created
as a static administrative subdivision, since using municipal boundaries etc. has been know
to change and are therefore not suitable as a geographical administrative index.

The Danish Kvadratnet consist of a several **networks** that covers the country with square tiles
of varying sizes.
Supported tile sizes are: 100m, 250m, 1km, 10km, 50km and 100km.
Individual tiles are identified by tile size and the coordinates of the lower left corner of a tile.
The coordinates are truncated accordinging to the size of the tile i.e. 1km_6452_523.
Examples of tile identifiers can be seen in the table below:

| Network   | Tile name example |
|-----------|-------------------|
|  100km    | 100km_62_5        |
|  50km     | 50km_620_55       |
|  10km     | 10km_622_57       |
|  1km      | 1km_6223_576      |
|  250m     | 250m_622375_57550 |
|  100m     | 100m_62237_5756   |


Use of the kvadratnet module is not limited to the geographical area of Denmark.
The tiling scheme can be applied to any region on earth as the UTM coordinate system is defined worlwide.
Care has to be taken in case use of the tiling scheme spans more than one UTM zone, since
coordinates are duplicated across zones.
This can be solved by keeping all data in the same UTM zone, even though some of it might
be placed outside the zone.
By using robust UTM coordinate transformation libraries, such as the Extended Transverse Mercator
implementation in ```proj.4```, data can be kept in the same coordinate system
even though it spans several UTM zones.
This exact procedure is used by the Grenland Survey, [Asiaq](http://www.asiaq.gl/), which organizes
data across 10 UTM zones.

## Example

Example of using kvadratnet.py

Suppose you have a range of files organized in the 1km network.
We want to count how many 1km tiles are present in each parent
10km tile.

```python
from collections import Counter
import kvadratnet

files = ['dtm_1km_6121_867.tif', 'dtm_1km_6125_866.tif',
         'dtm_1km_6125_862.tif', 'dtm_1km_6423_512.tif',
         'dtm_1km_6253_234.tif', 'dtm_1km_6235_634.tif',
         'dtm_1km_6424_513.tif', 'dtm_lkm_5223_523.tif',
         'dtm_1km_6251_236.tif', 'dtm_1km_6424_517.til']

counter = Counter()

for filename in files:
    try:
        name = kvadratnet.tile_name(filename)
    except:
        counter['bad_name'] += 1
    parent = kvadratnet.parent_tile(name, '10km')
    counter[parent] += 1

print(counter)
# Counter({'10km_642_51': 4, '10km_612_86': 3, '10km_625_23': 2, '10km_623_63': 1, 'bad_name': 1})
```


## Installation

Installation can be done either via

```
pip install kvadranet
```

or by downloading the source code and running

```
python setup.py install
```

## testing

```nose``` is used for testing. The test-suite can be invoked by running

```
nosetests -v
```

