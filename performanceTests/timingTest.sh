#!/usr/bin/env bash

generate_post_data()
{
  cat <<EOF
{
  "bucket": "ditto-test"
}
EOF
}

USER=$1
PASSWORD=$2

function runUploadTest {
  # unix time in nanoseconds
  T0=$(date +%s%N)

  #curl -i \
  #-H "Accept: application/json" \
  #-H "Content-Type:application/json" \
  #-X POST \
  #--user "${USER}:${PASSWORD}" \
  #--data "$(generate_post_data)" \
  #"http://172.28.129.160:8888/copydir/"

  # unix time in nanoseconds
  T1=$(date +%s%N)

  # time difference in milliseconds
  T=$(($(($T1 - $T0))/1000000))
  
  echo "$T"
}

T=`runUploadTest`

echo ""
echo "Took $T milliseconds to upload"