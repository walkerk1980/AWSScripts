#!/bin/bash
akid=0123456789012
region='us-west-2'
bucket='cloudtrail-bucket-name'
#prefix if your Trail has one
prefix='CloudTrail'
account=0123456789012

year=$(date +%Y)
month=$(date +%m)
day=$(date +%d)
mkdir ctlogs
cd ctlogs/

#pull from s3
aws s3 cp s3://$bucket/AWSLogs/$account/CloudTrail/$region/$year/$month/$day/ ./ --recursive
aws s3 cp s3://$bucket/$prefix/AWSLogs/$account/CloudTrail/$region/$year/$month/$day/ ./ --recursive

#parse API calls via used AKID
#without jq package installed
zgrep -r $akid *|cut -d ':' -f2-999

#with jq installed
zgrep -r $akid *|cut -d ':' -f2-999|jq -r
