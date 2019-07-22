# ve_tile_merge
down load tiles from virtual earth and merge tiles to a jpg image.

usage:
   step1: get tiles from ve server.
      python tiles.py wget 35 54 10 126 36 59 13 6 | sh
   while the argvs 34 54 10 / 126 36 59 is the lat/lon of the point you are interested in.
      and 13 is the base level of the image and 6 is the details of the image
   step2: merge tiles and you will get a jpg file in current directory.
     python tiles.py merge 35 54 10 126 36 59 13 6 
 
 if you have many points of interest to download, you can edit a config file in plant text( e.g. download.conf)
     35 54 10 126 36 59 13 6 
     37  7 54 126 48 20 13 6 
     37 26 34 127  6 55 13 6  
     35  5 27 128  4 18 13 6
and use the following to line to get all interested pictures
  `awk '{printf "python tiles.py wget %s %s %s %s %s %s %s %s\n",$1,$2,$3,$4,$5,$6,$7,$8}' download.conf ` | sh
  `awk '{printf "python tiles.py merge %s %s %s %s %s %s %s %s\n",$1,$2,$3,$4,$5,$6,$7,$8}' download.conf ` 
 
  
