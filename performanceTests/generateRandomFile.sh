#!/usr/bin/env bash

rootdir=$1

function generateFile {
	dirpath=$1
	filename=$2
	batchsize=$3
	count=$4

	if [ ! -d "${dirpath}" ]; then
      	mkdir "${dirpath}"
	fi
	
	dd if=/dev/urandom of="${dirpath}/${filename}" bs=${batchsize} count=${count}
}


generateFile "${rootdir}/single16mb" "16MB.bin" 16M 1
generateFile "${rootdir}/single32mb" "32MB.bin" 32M 1
generateFile "${rootdir}/single64mb" "64MB.bin" 64M 1
generateFile "${rootdir}/single128mb" "124MB.bin" 64M 2
generateFile "${rootdir}/single256mb" "256MB.bin" 64M 4
generateFile "${rootdir}/single512mb" "512MB.bin" 64M 8
generateFile "${rootdir}/single1gb" "1GB.bin" 64M 16
generateFile "${rootdir}/single2gb" "2GB.bin" 64M 32
generateFile "${rootdir}/single4gb" "4GB.bin" 64M 64
for n in {1..8}; do {
  generateFile "${rootdir}/eight64mb" "64mb_${n}.bin" 64M 1
} done
