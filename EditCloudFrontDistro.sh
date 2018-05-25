#!/bin/bash

distroid=E14G27FBGS5G7M

if [ -z "$1" ];then
  echo
else
  distroid=$1
fi

aws cloudfront get-distribution --id $distroid --query Distribution.DistributionConfig >distro.json
etag=$(aws cloudfront get-distribution --id $distroid --query ETag|sed 's/"//g')

#set preferred editor vim, nano, etc
nano distro.json

echo "Press Enter three times to update your distribution now, or press ctrl+c to cancel"
read $input
read $input
read $input

aws cloudfront update-distribution --id $distroid --distribution-config file://distro.json --if-match $etag

#optional
rm -v distro.json
