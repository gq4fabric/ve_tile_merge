# ve_tile_merge
down load tiles from virtual earth and merge tiles to a jped map

usage:
in file tiles.py  set the latD,latM,latS,lonD,LonM,LonS level sub_level of the location you want to get.
run:
  python tiles.py | sh
will download images from MS's server. the number of the images is exp(4,sub_level),and must end with 3...3

run:
python mergy.py
will generate a .jpg file 
