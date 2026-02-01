# bash script to organise files and remove data that is no longer needed
# run this script after the spectral synthesis and averaging calculations
# change FOLDERS and FILES entries, and line 86

#!/bin/bash
FOLDERS=380390nm_vald*sun_ssd_mu10

for k in $FOLDERS
do 
cd $k 

FILES=SSD_set2*
stopcalc=0
for f in $FILES
do
echo "Processing $f files..."
filename=$(basename -- "$f")
number="${filename##*_}"
echo "and the number is $number "
cd $f 
cd OUT_INTEN
for j in 0 1 2 3 4 5 6 7 8 9
do 
if [ -f "av_inten_mu_$j.dat" ]
then
 echo "file av_inten_mu$j.dat in folder $f is there" >> "files_$f.dat"
else
  echo "File av_inten_mu_$j.dat in folder $f is not found" >> "files_$f.dat"
  stopcalc=1
fi
done
mv files*.dat ../../
cd ../../
done
cat files*.dat > availability.dat


rm files*.dat
if [ $stopcalc == 1 ]
then
    echo "Some files are missing, going to abort"
    exit 
fi 
####### now move nc cubes to full_nc_cubes folder
#
mkdir full_nc_cubes

for f in $FILES
do
echo "Processing $f files..."
cd $f
mv ./OUT_NC $f
mv $f ../full_nc_cubes
cd ../
done
#################
## delete everything that is not needed
#
#
#
mkdir other_data
for f in $FILES
do
echo "Processing $f files..."
cd $f
mv examplef/INPUT/flux.input ../other_data
rm -r running*
rm -r examplef
rm -r CARDS
rm -r collect
rm *
cd ../
done
######### move the averages out
#
for f in $FILES
do
echo "Processing $f files..."
cd $f
mv ./OUT_INTEN/* ./
rmdir OUT_INTEN
cd ../
done

mkdir av_files
mv SSD_set2* av_files
#
#save important information for later
mv executables ./other_data
mv cut_folder ./other_data
rm -r error
rm -r muram
rm -r ready_cubes*
rm -r rt_example
rm *

cd ../
done
