from pyproj import Transformer

# 鹿児島県（第2系）
EPSG_CODE = "epsg:6670"
transformer = Transformer.from_crs(EPSG_CODE, "epsg:4326", always_xy=True)

def xy_to_latlon(x, y):
    lon, lat = transformer.transform(y, x)
    return lat, lon