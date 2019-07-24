import requests
import math
import random
from PIL import Image
# https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
EarthRadius = 6378137;
MinLatitude, MaxLatitude = -85.05112878, 85.05112878
MinLongitude, MaxLongitude = -180, 180
def clip(n, minv, maxv):
    return min(max(n, minv), maxv)
def map_size(level):
    return 256 << level
def ground_resolution(lat, level):
    lat = clip(lat, MinLatitude, MaxLatitude);
    return math.cos(lat * math.pi / 180) * 2 * math.pi * EarthRadius / map_size(level)
def latlon2PixXY(lat, lon, level):
    lat, lon = clip(lat, MinLatitude, MaxLatitude), clip(lon, MinLongitude, MaxLongitude)
    x = (lon + 180) / 360
    sinlat = math.sin(lat * math.pi / 180)
    y = 0.5 - math.log((1 + sinlat) / (1 - sinlat)) / (4 * math.pi);
    mapSize = map_size(level)
    return [int(clip(i * mapSize + .5, 0, mapSize - 1)) for i in [x, y]]
def pixXY2LatLon(pX, pY, level):
    mapSize = map_size(level)
    x = clip(pX, 0, mapSize - 1) / mapSize - .5
    y = .5 - clip(pY, 0, mapSize - 1) / mapSize
    return 90 - 360 * math.atan(math.exp(-y * 2 * math.py)) / math.pi, 360 * x
def pixXY2tileXY(pX, pY):
    return int(pX / 256), int(pY / 256)
def tileXY2pixXY(tX, tY):
    return tX * 256, tY * 256
def tileXY2QKey(tX, tY, level):
    ret, i = "", level
    while i > 0:
        mask = 1 << i - 1
        v = (1 if tX & mask != 0 else 0) + (2 if tY & mask != 0 else 0)
        ret, i = ret + str(v), i - 1
    return ret
def dfm2float(d, f, s):
    return d + f / 60.0 + s / 3600.0
def QKey2Url( qkey ):
    return 'http://a'+random.choice(['0','1','2','3'])+'.ortho.tiles.virtualearth.net/tiles/a' + qkey + '.png?g=50'
def getTile( qkey ):
    url , fn= QKey2Url(qkey) ,qkey+'.jpg'
    if os.path.exists( fn ):
    	return Image.open(fn)
    r = requests.get(url)
    with open(fn, 'ab') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.flush()
    return Image.open(fn)
def getQKeys(latD, latM, latS, lonD, lonM, lonS, level,w):
    h = w
    lat, lon = dfm2float(latD, latM, latS), dfm2float(lonD, lonM, lonS)
    px, py = latlon2PixXY(lat, lon, level)
    tx, ty = pixXY2tileXY(px,py)
    qkeys = []
    for i in range(h+1+h):
        qkeys.append(["" ]*(w+1+w) )
    for i in range(1+2*w):
        for j in range(1+2*h):
            qkeys [i][j]= tileXY2QKey( tx+i-w,ty + j -h ,level)
    return qkeys

def merge_up( qkeys ):
    rows,cols ,(w,h)= len(qkeys),len(qkeys[0]) , getTile(qkeys[0][0]).size
    val = Image.new( 'RGB', ( w*cols, h*rows ), 255)
    for i in range(rows):
        for j in range(cols):
            print(i,j,qkeys[i][j])            
            val.paste(getTile( qkeys[i][j] ), ( i*w,j*h ) )
    return  val

def GetMyImg(  latD, latM, latS, lonD, lonM, lonS, level, width):
    keys = getQKeys(latD, latM, latS, lonD, lonM, lonS, level, width )
    merge_up(keys).save( keys[width][width]+'-'+ str(level) +"-" + str(width)+'.jpg' )

for level in [18]:
	for width in [30]:
		GetMyImg(35,54,10,126,36,59,level,width)
