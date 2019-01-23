#!/usr/bin/env bash

# processing the data for beiluhe site
# don' exit
#set -e

# use python2
# failed to use python3 due to "TypeError: in method 'BandRasterIONumPy', argument 3 of type 'double'"
#export PATH=~/programs/anaconda2/bin:$PATH
#Cryo06
export PATH=/usr/bin:$PATH

refdem_fn=$1

dem_name=$(basename "$refdem_fn")
dem_name_no_ext="${dem_name%.*}"
echo $dem_name_no_ext
#refdem_fn=~/Data/Qinghai-Tibet/beiluhe/DEM/srtm_30/beiluhe_strm30.tif
#icesat_fn=~/Data/Qinghai-Tibet/beiluhe/icesat/GLAH14_634_2107_002_0281_0_01_0001.H5
#icesat_fn=~/Data/Qinghai-Tibet/beiluhe/icesat/GLAH14_634_1102_001_0099_0_01_0001.H5

icesat_dir=~/Data/Qinghai-Tibet/beiluhe/icesat

##get the extent using ./get_raster_extent.py ${refdem_fn}
#ext='"92.536475 93.22801111111112 34.791311111111106 35.291127777777774"'
#./glas_proc.py ${icesat_fn} hma -extent ${ext} -refdem_fn ${refdem_fn}

# test 1
#./glas_proc.py ${icesat_fn} hma -extent "92.536475 93.22801111111112 34.791311111111106 35.291127777777774" \
# -refdem_fn ${refdem_fn}
#
# ./glas_proc.py ${icesat_fn} hma -extent "read" \
# -refdem_fn ${refdem_fn}

# test 2
#./glas_proc.py ${icesat_fn} hma -extent "60 120 30 40" \
# -refdem_fn ${refdem_fn}


parallel --progress --delay 1 -j 16 "~/codes/PycharmProjects/yghlc_icesat_tools/glas_proc.py {} hma -extent read  -refdem_fn ${refdem_fn}" ::: ${icesat_dir}/*.H5
#Combine output

for ext in hma.csv hma_refdemfilt.csv ; do

    first=$(ls *${ext} | head -1)
    head -1 $first > ${dem_name_no_ext}_GLAH14_${ext}
    cat *${ext}| sort -n | grep -v lat >> ${dem_name_no_ext}_GLAH14_${ext}

done






