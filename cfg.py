#################################################################################################################
# WMS config
#################################################################################################################
WMS_SERVER = 'https://wxs.ign.fr/xxx_key_xxx/geoportail/r/wms'

# layers auxquels on peut acceder
LAYERS = ['HR.ORTHOIMAGERY.ORTHOPHOTOS', 'GEOGRAPHICALGRIDSYSTEMS.ETATMAJOR40', 'GEOGRAPHICALGRIDSYSTEMS.CASSINI',
 'GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2', 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN50.1950', 'ORTHOIMAGERY.ORTHOPHOTOS.1950-1965',
 'GEOGRAPHICALGRIDSYSTEMS.MAPS.SCAN-EXPRESS.STANDARD']

# selection des layers parmi ceux definis au dessus par indice, et préfixe utilisé dans le nom des images générées
WMS_SELECTION = {4: 'scan50', 1:'etatmajor', 2:'cassini', 0:'ortho'}

#################################################################################################################
# WMTS config (optional).. not really useful
#################################################################################################################
WMTS_SERVER = "http://wxs.ign.fr/xxx_key_xxx/geoportail/wmts?SERVICE=WMTS&REQUEST=GetCapabilities"
# index dans LAYERS et prefixe à utiliser 
WMTS_LAYER = {'idx': 6, 'prefix': 'scanex'}

#################################################################################################################
# if --wmts or --centered option is set, it will get all tiles containing (resp. centered around)
# each coordinate in COORDS for all zoom levels in WMTS_LEVELS
#################################################################################################################
COORDS = [(923115.73, 6321563.12), (659972.58, 7087925.63), (357197.12, 6684541.92)]
# MAX = 18
WMTS_LEVELS = [8, 9, 10] #[5, 6, 7, 8, 9, 10, 11, 12, 13, 14]