from PIL import Image
def qMerge(imgs):
	w,h = imgs[0].size
	ret,pos = Image.new( 'RGB',(w+w,h+h),255), [[0,0],[w,0],[0,h],[w,h]]
	for img,x,y in [ imgs[i],pos[i][0],pos[i][1] for i range(4) ]:
		ret.paste(img,(x,y))
	return ret
def merge(qkey,level):
	keys = [qkey+str(i) for i in range(4)]
	return qMerge([Image.open(k) if level==1 else merge(k,level-1) for k in keys])
def merge_save(key,sublevel):
  merge(key,sublevel).save(key+'.jpg')
merge_save('a1',3)
