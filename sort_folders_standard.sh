#!/bin/bash
#
# Bash script to organise spectral files and remove data that is no longer needed.
# Run the script after the spectral synthesis and averaging calculations.
#
# Example run:
#
#  $ bash sort_folders_standard.sh /absolute/path/to/dir/to/sort_me_1 cube_prefix
#
# For sorting multiple folders at the same time:
#
#  $ bash sort_folders_standard.sh /absolute/path/to/dir/to/sort_me\* cube_prefix
#
# The provided path to folder(s) to sort can be relative. 
#
# cube_prefix: the prefix of the cubes used for synthesise (i.e. G2_mh00)
#

GREEN=`tput setaf 2`
reset=`tput sgr0`

FOLDERS=$1
FOLDERS=$(ls -d ${FOLDERS})

CUBE_PREFIX=$2

echo ""

for k in $FOLDERS
do 
  echo "${GREEN}$k${reset}"
  cd $k

  FILES=$(ls -d ${CUBE_PREFIX}*)

  stopcalc=0
  echo "Counting files..."
  for f in ${FILES}
  do
    filename=$(basename -- "$f")
    number="${filename##*_}"
    # echo "  cube ID: $number"
    cd $f
    cd OUT_INTEN
    for j in 0 1 2 3 4 5 6 7 8 9
    # for j in 0
    do
      if [ -f "av_inten_mu_$j.dat" ]
      then
        echo "File av_inten_mu$j.dat in folder $f is there" >> "files_$f.dat"
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
      echo "Check ${k}/availability.dat for missing files"
      echo ""
      continue
  fi

  ###### now move nc cubes to full_nc_cubes folder
  #
  if [ ! -d "full_nc_cubes" ]; then
    mkdir full_nc_cubes
  fi

  echo "Moving .nc cubes..."
  for f in $FILES
  do
    cd $f
    mv ./OUT_NC $f
    mv $f ../full_nc_cubes
    cd ../
  done

  ###### move the averages out
  #
  if [ ! -d "av_files" ]; then
    mkdir av_files
  fi

  echo "Moving the average spectra..."
  for f in $FILES
  do
    cd $f
    mv ./OUT_INTEN ../av_files/$f
    mv ./collect/mpsa.wave ../av_files
    cd ../
  done

  ###### delete everything that is not needed
  #
  if [ ! -d "other_data" ]; then
    mkdir other_data
  fi

  echo "Deleting unnecessary files..."
  for f in $FILES
  do
    cd $f
    mv examplef/INPUT/flux.input ../other_data
    cd ../
    rm -rf $f
  done

  #
  #save important information for later
  mv executables ./other_data
  mv cut_folder ./other_data
  rm -r error
  rm -r muram
  rm -r ready_cubes*
  rm -r rt_example
  rm *.*

  cd ../
done
