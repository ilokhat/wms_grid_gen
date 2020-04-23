import cfg
import argparse
import sys
import os
sys.path.append(os.path.abspath("./"))
from owslib.wms import WebMapService
from owslib.wmts import WebMapTileService
from pyproj import Transformer

# taken from https://geoservices.ign.fr/documentation/geoservices/wmts.html
# m/px for each zoom level
ZOOM_RES_L93 = {
    0: 156543.0339280410, 1: 78271.5169640205, 2: 39135.7584820102, 
    3: 19567.8792410051, 4: 9783.9396205026, 5: 4891.9698102513, 	
    6: 2445.9849051256, 7: 1222.9924525628, 8: 611.4962262814, 
    9: 305.7481131407, 10: 152.8740565704, 11: 76.4370282852, 	
    12: 38.2185141426, 13: 19.1092570713, 14: 9.5546285356, 	
    15: 4.7773142678, 16: 2.3886571339, 17: 1.1943285670, 
    18: 0.5971642835, 19: 0.2985821417, 20: 0.1492910709, 21: 0.0746455354 
}

def build_envelopes(x0, y0, width, n):
    envs = []
    for i in range(n):
        xll = x0 + i * width 
        for j in range(n):
            yll = y0 + j * width
            xur = xll + width
            yur = yll + width
            env = (xll, yll, xur, yur)
            envs.append(env)
    return envs


def build_wms_tile(image_path, wms, env, layer, size=512):
    LAYER = layer
    SRS = 'EPSG:2154'
    IMG_DIMS = (size, size)
    img = wms.getmap(layers=[LAYER], srs=SRS, bbox=env, size=IMG_DIMS, format='image/jpeg')
    out = open(image_path, 'wb')
    out.write(img.read())
    out.close()

def build_wmst_tile(image_path, wmts, layer, x93, y93, zoom_level):
    taille_tuile = ZOOM_RES_L93[zoom_level] * 256
    X0, Y0 = wmts.tilematrixsets['PM'].tilematrix['13'].topleftcorner
    proj = Transformer.from_crs(2154, 3857, always_xy=True)
    x_m, y_m = proj.transform(x93, y93)
    x_g = x_m - X0
    y_g = Y0 - y_m 
    tilecol = int(x_g / taille_tuile)
    tilerow = int(y_g / taille_tuile)
    tile = wmts.gettile(layer=layer, tilematrixset='PM', tilematrix=f'{zoom_level}', 
                            row=tilerow, column=tilecol, format="image/jpeg")
    out = open(image_path, 'wb')
    bytes_written = out.write(tile.read())
    out.close()


parser = argparse.ArgumentParser(
    description="Generate images in a grid fashion from wms server (or tiles from wmts)")

parser.add_argument("-s", "--size", help="image size in pixels (default=512)", default=512, type=int)
parser.add_argument("-x", "--xl93", help="lower left x L93 (default=498465.5 )",
                    default=498465.5, type=float)
parser.add_argument("-y", "--yl93", help="lower left y L93 (default=6601459.5)",
                    default=6601459.5, type=float)
parser.add_argument(
    "-n", "--nbtiles", help="nb of tiles per line and column (square grid, default=1)", default=1, type=int)
parser.add_argument(
    "-d", "--delta", help="length of one square tile side (meters, default=3000)", default=3000, type=int)
parser.add_argument("-o", "--output_dir",
                    help="output directory for images (default=.)", default='.')
parser.add_argument("--wmts", help="generate wmts tiles for zoom level(s) and layer in config file. discard all other options except -x -y and -o",
                    action="store_true")

args = parser.parse_args()

S = args.size
X, Y = args.xl93, args.yl93
N = args.nbtiles
DELTA = args.delta
output_dir = args.output_dir

LAYERS = cfg.LAYERS
SELECTION = cfg.WMS_SELECTION
WMTS_LAYER = cfg.WMTS_LAYER


if (args.wmts):
    wmts = WebMapTileService(cfg.WMTS_SERVER)
    for ZOOM_LEVEL in cfg.WMTS_LEVELS:
        img = f"{output_dir}/{WMTS_LAYER['prefix']}_{ZOOM_LEVEL}.jpg"
        build_wmst_tile(img, wmts,
                        LAYERS[WMTS_LAYER['idx']], X, Y, ZOOM_LEVEL)
        print(img, 'written')
else:
    wms = WebMapService(cfg.WMS_SERVER, version='1.3.0')
    envs = build_envelopes(X, Y, DELTA, N)
    for i, env in enumerate(envs, start=1):
        print(f'{i}/{len(envs)}')
        for k, v in SELECTION.items():
            img = f'{output_dir}/{v}_{i}.jpg'
            build_wms_tile(img, wms, env, layer=LAYERS[k], size=S)
            print(img, 'written')