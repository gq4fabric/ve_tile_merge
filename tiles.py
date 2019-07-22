import math
import sys
from PIL import Image
# reference : https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
EarthRadius = 6378137;  
MinLatitude,MaxLatitude = -85.05112878, 85.05112878
MinLongitude ,MaxLongitude = -180, 180

def clip(n, minv,maxv):
	return min(max(n,minv),maxv)

def map_size( level):
	return  256 << level

def ground_resolution(lat, level):
	lat = clip(lat , MinLatitude, MaxLatitude);  
	return math.cos(lat* math.pi / 180) * 2 * math.pi * EarthRadius / map_size(level)

def latlon2PixXY(lat,lon,level):
	lat ,lon = clip(lat, MinLatitude, MaxLatitude) , clip(lon, MinLongitude,MaxLongitude)
	x =(lon + 180)/ 360
	sinlat = math.sin( lat * math.pi/180)
	y = 0.5 - math.log((1 + sinlat) / (1 - sinlat)) / (4 * math.pi);  
	mapSize = map_size(level)  
	return [ int(clip(i*mapSize+.5,0,mapSize-1)) for i in [x,y] ]

def pixXY2LatLon(pX,pY,level):
	mapSize = map_size(level)  
	x = clip( pX,0,mapSize-1)/mapSize -.5
	y = .5 - clip(pY,0,mapSize-1)/mapSize
	return 90 -360* math.atan( math.exp(-y*2*math.py))/math.pi , 360 * x

def pixXY2tileXY( pX,pY):
	return int(pX/256),int(pY/256)

def tileXY2pixXY( tX,tY):
	return tX*256,tY*256

def tileXY2QKey(tX,tY,level):
	ret ,i = "", level
	while i>0:
		mask = 1<< i-1
		v = (1 if tX & mask!=0 else 0)+(2 if tY & mask!=0 else 0)
		ret,i= ret + str(v),i-1
	return ret

def dfm2float( d ,f,s):
	return d + f/60.0 + s/3600.0

def getQKey(latD,latM,latS, lonD,lonM,lonS,level):
	lat ,lon = dfm2float(latD,latM,latS),dfm2float(lonD,lonM,lonS)
	px,py = latlon2PixXY(lat,lon,level)
	tx,ty = pixXY2tileXY(px,py)
	return tileXY2QKey( tx,ty, level)
	
def QID(level,idx):
	_max, mask,ret = (1<<(2*level)) -1,3,""
	if idx > _max:
		return ret
	while level > 0:
		ret = str( idx&mask ) + ret
		idx , level = idx >>2,level -1
	return ret

def download(pic):
	u = 'http://a1.ortho.tiles.virtualearth.net/tiles/a' + pic + '.png?g=50'
	print ( "wget " + u + " -O " + pic )

def getQKeyPics(latD,latM,latS, lonD,lonM,lonS,level,sub):
	for i in range( 1 << (sub*2)):
		download( getQKey( latD,latM,latS, lonD,lonM,lonS,level) + QID(sub,i))
		
def qMerge(imgs):
	w,h = imgs[0].size
	ret,pos = Image.new( 'RGB',(w+w,h+h),255), [[0,0],[w,0],[0,h],[w,h]]
	for i in range(4):
		ret.paste( imgs[i],pos[i])
	return ret

def merge(qkey,level):
	keys = [qkey+str(i) for i in range(4)]
	return qMerge([Image.open(k) if level==1 else merge(k,level-1) for k in keys])
		
latD,latM,latS = int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4])
lonD,lonM,lonS = int(sys.argv[5]),int(sys.argv[6]),float(sys.argv[7])
level,sub= int(sys.argv[8]),int(sys.argv[9])
key = getQKey(latD,latM,latS, lonD,lonM,lonS,level)

if( sys.argv[1] =='wget'):
	getQKeyPics( latD,latM,latS, lonD,lonM,lonS,level,sub)
if( sys.argv[1] == 'merge'):
	merge(key,sub).save(key + '.jpg')
#`awk '{printf "python tiles.py wget %s %s %s %s %s %s %s %s\n",$1,$2,$3,$4,$5,$6,$7,$8}' download.conf `
#`awk '{printf "python tiles.py merge %s %s %s %s %s %s %s %s\n",$1,$2,$3,$4,$5,$6,$7,$8}' download.conf `
