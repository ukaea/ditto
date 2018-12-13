#!/usr/bin/env bash

rootdir=$1
user=$2
password=$3

function totalDirSize {
  dir=$1
  
  total="0"
  for file in $(ls ${dir}); do {
    if [ ! -d "${dir}/${file}" ]; then {
	  fs=$(stat --printf="%s" "${dir}/${file}")
	  total=$(( ${total}+${fs} ))
    }; fi
} done
  echo "$total"
}

function runUploadTest {
  dir=$1

  # unix time in nanoseconds
  T0=$(date +%s%N)

  output=`curl -i \
  --silent \
  -H "Accept: application/json" \
  -H "Content-Type:application/json" \
  -X POST \
  --user "${user}:${password}" \
  --data '{"bucket":"ditto-test","directory":"'${dir}'"}' \
  "http://172.28.129.160:8888/copydir/"`

  # unix time in nanoseconds
  T1=$(date +%s%N)

  # time difference in milliseconds
  T=$(($(($T1 - $T0))/1000000))
  
  echo "$T"
}

echo -e "directory,totalBytes,millisecondsToUpload" > results.csv

for x in $(ls ${rootdir}); do {
  if [ -d "${rootdir}/${x}" ]; then {
    echo "Copying ${x}"
	S=`totalDirSize "${rootdir}/${x}"`
    T=`runUploadTest ${x}`
	echo -e "${x},${S},${T}" >> results.csv
  }; fi
} done
