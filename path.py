from pyproj import CRS, Transformer
from shapely.geometry import Point
from shapely.ops import transform

def geodesic_point_buffer(lat, lon, km):
	# Azimuthal equidistant projection
	aeqd_proj = CRS.from_proj4(
		f"+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0")
	tfmr = Transformer.from_proj(aeqd_proj, aeqd_proj.geodetic_crs)
	buf = Point(0, 0).buffer(km * 1000)  # distance in metres
	return transform(tfmr.transform, buf).exterior.coords[:]

km = 0.100

f = open('cityringen.csv')
f.readline() # skip first

print(f"""
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Folder>
<name>{km} km radii</name>
<open>1</open>
<description>
A folder is a container that can hold multiple other objects
</description>
""")

for line in f:
	name,lat,lon = line.split(',')
	print(f"""
<Placemark>
<name>{name}</name>
<Polygon>
<tessellate>1</tessellate>
<outerBoundaryIs>
<LinearRing>
<coordinates>""")
	for (lat,lon) in geodesic_point_buffer(float(lat), float(lon), km):
		print(f"{lat},{lon}")
	print("""
</coordinates>
</LinearRing>
</outerBoundaryIs>
</Polygon>
</Placemark>
""")

print("""
</Folder>
</kml>
""")