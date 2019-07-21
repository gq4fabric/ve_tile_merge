import math
from PIL import Image
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
	#return [ int(clip(i*mapSize+.5,0,mapSize-1)) for i in [x,y] ]

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


def dfm2float( d ,f,s):
	return d + f/60.0 + s/3600.0

def getQKey(latD,latM,latS, lonD,lonM,lonS,level):
	lat ,lon = dfm2float(latD,latM,latS),dfm2float(lonD,lonM,lonS)
	px,py = latlon2PixXY(lat,lon,level)
	tx,ty = pixXY2tileXY(px,py)
	return tileXY2QKey( tx,ty, level)
	
def aaa(level,idx):
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
#	urllib.urlretrieve(u, filename=pic+'.png')

def getQKeyPics( latD,latM,latS, lonD,lonM,lonS,level,sub):
	primary = getQKey( latD,latM,latS, lonD,lonM,lonS,level);
	for i in range( 1 << (sub*2)):
		download( primary + aaa(sub,i))
		
def qMerge(imgs):
	w,h = imgs[0].size
	ret,pos = Image.new( 'RGB',(w+w,h+h),255), [[0,0],[w,0],[0,h],[w,h]]
	for img,x,y in [ imgs[i],pos[i][0],pos[i][1] for i range(4) ]:
		ret.paste(img,(x,y))
	return ret

def merge(qkey,level):
	keys = [qkey+str(i) for i in range(4)]
	return qMerge([Image.open(k) if level==1 else merge(k,level-1) for k in keys])
		
l1=14,l2=5
getQKeyPics(35,54,10,126,36,59,l1,l2)

l1=14,l2=5
keys =[]
keys.append(getQKey(35,54,10,126,36,59,l1))

for k in keys:
	merge(k,l2).save(k+'.jpg')
