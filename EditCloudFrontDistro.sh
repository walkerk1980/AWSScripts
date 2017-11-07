#!/bin/bash
#requires jq, you can get this via apt/yum install jq on linux or brew install jq on a mac with brew installed

distroid=E14G27FBGS5G7M
aws cloudfront get-distribution --id $distroid >distro.config
etag=$(cat distro.config |jq '.ETag'|sed 's/"//g')
cat distro.config | jq '.Distribution.DistributionConfig' >distro.json

#set preferred editor vim, nano, etc
nano distro.json

echo "Press Enter three times to update your distribution now, or press ctrl+c to cancel"
read $input
read $input
read $input

aws cloudfront update-distribution --id $distroid --distribution-config file://distro.json --if-match $etag

#optional
rm -v distro.config distro.json
