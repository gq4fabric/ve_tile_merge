import math
#https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system
EarthRadius = 6378137;  
MinLatitude = -85.05112878;  
MaxLatitude = 85.05112878;  
MinLongitude = -180;  
MaxLongitude = 180;  

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
	pixelX = clip(x * mapSize + 0.5, 0, mapSize - 1)
	pixelY = clip(y * mapSize + 0.5, 0, mapSize - 1)  
	return int(pixelX),int(pixelY)

def pixXY2LatLon(pX,pY,level):
	mapSize = map_size(level)  
	x = clip( pX,0,mapSize-1)/mapSize -.5
	y = .5 - clip(pY,0,mapSize-1)/mapSize
	lat = 90 -360* math.atan( math.exp(-y*2*math.py))/math.pi
	lon = 360 * x
	return lat,lon

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

def dms2float( d ,m,s):
	return d + m/60.0 + s/3600.0

def getQKey(latD,latM,latS, lonD,lonM,lonS,level):
	lat ,lon = dms2float(latD,latM,latS),dms2float(lonD,lonM,lonS)
	px,py = latlon2PixXY(lat,lon,level)
	tx,ty = pixXY2tileXY(px,py)
	return tileXY2QKey( tx,ty, level)
	
def ToQid(level,idx):
	_max, mask,ret = (1<<(2*level)) -1,3,""
	if idx > _max:
		return ret
	while level > 0:
		ret = str( idx&mask ) + ret
		idx = idx >>2
		level = level -1
	return ret

def download(pic):
	u = 'http://a1.ortho.tiles.virtualearth.net/tiles/a' + pic + '.png?g=50'
	print ( "wget " + u + " -O " + pic )
	
def getQKeyPics( latD,latM,latS, lonD,lonM,lonS,level,sub):
	primary = getQKey( latD,latM,latS, lonD,lonM,lonS,level);
	for i in range( 1 << (sub*2)):
		download( primary + ToQid(sub,i))
		
l1=14,l2=5
getQKeyPics(35,54,10,126,36,59,l1,l2)
