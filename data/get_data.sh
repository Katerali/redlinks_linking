#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo ${CURRENT_DIR}
cd ${CURRENT_DIR}

declare -A files

files[redlinks_3171.csv]=https://ndownloader.figshare.com/files/20780958
files[redlinks_candidates.csv]=https://ndownloader.figshare.com/files/20780961
files[train_indexes.csv]=https://ndownloader.figshare.com/files/20781792
files[test_indexes.csv]=https://ndownloader.figshare.com/files/20781795



for file in "${!files[@]}"; do
  if [ -f ${file} ]; then
    echo "file exists"
  else
    echo "* downloading file ..."
    wget -O ${file} ${files[$file]}
  fi
done



