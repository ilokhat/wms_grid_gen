This is a small python script to generate grids of images from a WMS server.
You must modify `cfg.py` with your own parameters, they are self-explicit : 
 - url for the server
 - your selection of layers

Then launch the script with the correct parameters (as seen below).

Coordinates are specified in Lambert93.

Please note that it's very crude, with no error checks..

_(Optionaly you could specify a wmts server and some levels of zoom if you want wmts tiles.)_


## Requirements
* Python 3
* OWSLib
* pyproj

## Usage
```
$ python gen_tiles_wms.py --help
usage: gen_tiles_wms.py [-h] [-s SIZE] [-x XL93] [-y YL93] [-n NBTILES] [-f FORMAT] [-d DELTA] [-o OUTPUT_DIR] [--centered] [--wmts]

Generate images in a grid fashion from a wms server (or tiles from wmts)

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  image size in pixels (default=512)
  -x XL93, --xl93 XL93  lower left x L93 (default=498465.5 )
  -y YL93, --yl93 YL93  lower left y L93 (default=6601459.5)
  -n NBTILES, --nbtiles NBTILES
                        nb of tiles per line and column (square grid, default=1)
  -f FORMAT, --format FORMAT
                        format of images, 'jpeg', 'png' or 'geotiff' (default='jpeg')
  -d DELTA, --delta DELTA
                        length of one square tile side (meters, default=3000)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        output directory for images (default=.)
  --centered            generate wms tiles centered around x, y for zoom level(s) and layer in config file. discard all other options except -o and -s
  --wmts                generate wmts tiles for zoom level(s) and layer in config file. discard all other options except -x -y and -o
```
![Grid](./grid.png)


## Examples
### Getting images from a WMS server, defined by a 3x3 grid, its lower left coordinate, and a (default) 3000 m length for each tile's side for a list of layers defined in `cfg.py`.
```
$ python gen_tiles_wms.py -x 649257.2 -y 6858461.9 -n 3 -o out 
1/9
out/scan50_1.jpg written
out/etatmajor_1.jpg written
out/cassini_1.jpg written
out/ortho_1.jpg written
2/9
out/scan50_2.jpg written
out/etatmajor_2.jpg written
out/cassini_2.jpg written
out/ortho_2.jpg written
3/9
out/scan50_3.jpg written
out/etatmajor_3.jpg written
out/cassini_3.jpg written
out/ortho_3.jpg written
4/9
out/scan50_4.jpg written
out/etatmajor_4.jpg written
out/cassini_4.jpg written
out/ortho_4.jpg written
5/9
out/scan50_5.jpg written
out/etatmajor_5.jpg written
out/cassini_5.jpg written
out/ortho_5.jpg written
6/9
out/scan50_6.jpg written
out/etatmajor_6.jpg written
out/cassini_6.jpg written
out/ortho_6.jpg written
7/9
out/scan50_7.jpg written
out/etatmajor_7.jpg written
out/cassini_7.jpg written
out/ortho_7.jpg written
8/9
out/scan50_8.jpg written
out/etatmajor_8.jpg written
out/cassini_8.jpg written
out/ortho_8.jpg written
9/9
out/scan50_9.jpg written
out/etatmajor_9.jpg written
out/cassini_9.jpg written
out/ortho_9.jpg written

```

The WMS server and the layers to get is set in the relevant section of `cfg.py` and should look like : 
```py
# layers auxquels on peut acceder
LAYERS = ['HR.ORTHOIMAGERY.ORTHOPHOTOS', 'GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40', 'GEOGRAPHICALGRIDSYSTEMS.CASSINI',
 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950', 'ORTHOIMAGERY.ORTHOPHOTOS.1950-1965',
 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD', 'GEOGRAPHICALGRIDSYSTEMS.MAPS', ]

#################################################################################################################
# WMS config
#################################################################################################################
WMS_SERVER = 'https://wxs.ign.fr/xxx_key_xxx/geoportail/r/wms'

# selection des layers parmi ceux definis au dessus par indice, et préfixe utilisé dans le nom des images générées
WMS_SELECTION = {4: 'scan50', 1:'etatmajor', 2:'cassini', 0:'ortho'}

```

### Getting 256x256 images from a WMS server, containing each coordinate and the levels of zoom for each layer set in `cfg.py`. 

```
$ python gen_tiles_wms.py -o out_wms_centered --centered -s 256
out_wms_centered/c0_classic_zl_8.jpg written
out_wms_centered/c0_scan50_zl_8.jpg written
out_wms_centered/c0_classic_zl_9.jpg written
out_wms_centered/c0_scan50_zl_9.jpg written
out_wms_centered/c0_classic_zl_10.jpg written
out_wms_centered/c0_scan50_zl_10.jpg written
out_wms_centered/c1_classic_zl_8.jpg written
out_wms_centered/c1_scan50_zl_8.jpg written
out_wms_centered/c1_classic_zl_9.jpg written
out_wms_centered/c1_scan50_zl_9.jpg written
out_wms_centered/c1_classic_zl_10.jpg written
out_wms_centered/c1_scan50_zl_10.jpg written
out_wms_centered/c2_classic_zl_8.jpg written
out_wms_centered/c2_scan50_zl_8.jpg written
out_wms_centered/c2_classic_zl_9.jpg written
out_wms_centered/c2_scan50_zl_9.jpg written
out_wms_centered/c2_classic_zl_10.jpg written
out_wms_centered/c2_scan50_zl_10.jpg written

```

The WMS server, layers to get, zoom levels, and the coordinates are set in the relevant section of `cfg.py` and should look like : 
```py
# layers auxquels on peut acceder
LAYERS = ['HR.ORTHOIMAGERY.ORTHOPHOTOS', 'GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40', 'GEOGRAPHICALGRIDSYSTEMS.CASSINI',
 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950', 'ORTHOIMAGERY.ORTHOPHOTOS.1950-1965',
 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD', 'GEOGRAPHICALGRIDSYSTEMS.MAPS', ]

#################################################################################################################
# WMS config
#################################################################################################################
WMS_SERVER = 'https://wxs.ign.fr/xxx_key_xxx/geoportail/r/wms'

# selection des layers parmi ceux definis au dessus par indice, et préfixe utilisé dans le nom des images générées
WMS_SELECTION = {7: 'classic', 4: 'scan50'}
# ...
# ...
# ...

COORDS = [(923115.73, 6321563.12), (659972.58, 7087925.63), (357197.12, 6684541.92)]
# MAX = 18
WMTS_LEVELS = [8, 9, 10]

```


### Getting tiles from a WMTS server, containing each coordinate and for the levels of zoom set in `cfg.py` for the layer specified.

```
$ python gen_tiles_wms.py -o out_wmts --wmts
out_wmts/c0_classic_zl_10.jpg written
out_wmts/c0_classic_zl_11.jpg written
out_wmts/c0_classic_zl_12.jpg written
out_wmts/c1_classic_zl_10.jpg written
out_wmts/c1_classic_zl_11.jpg written
out_wmts/c1_classic_zl_12.jpg written
out_wmts/c2_classic_zl_10.jpg written
out_wmts/c2_classic_zl_11.jpg written
out_wmts/c2_classic_zl_12.jpg written
```

The relevant section of `cfg.py` should look like this : 
```py
# layers auxquels on peut acceder
LAYERS = ['HR.ORTHOIMAGERY.ORTHOPHOTOS', 'GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40', 'GEOGRAPHICALGRIDSYSTEMS.CASSINI',
 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950', 'ORTHOIMAGERY.ORTHOPHOTOS.1950-1965',
 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD', 'GEOGRAPHICALGRIDSYSTEMS.MAPS', ]
 # ...
 # ...
 # ...
 
#################################################################################################################
# WMTS config
#################################################################################################################
WMTS_SERVER = "http://wxs.ign.fr/xxx_key_xxx/geoportail/wmts?SERVICE=WMTS&REQUEST=GetCapabilities"
# index dans LAYERS et prefixe à utiliser 
WMTS_LAYER = {'idx': 7, 'prefix': 'classic'}


#################################################################################################################
# if --wmts or --centered option is set, it will get all tiles containing (resp. centered around)
# each coordinate in COORDS for all zoom levels in WMTS_LEVELS
#################################################################################################################
COORDS = [(923115.73, 6321563.12), (659972.58, 7087925.63), (357197.12, 6684541.92)]
# MAX = 18
WMTS_LEVELS = [10, 11, 12]

```