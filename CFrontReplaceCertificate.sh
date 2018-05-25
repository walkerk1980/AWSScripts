#!/bin/bash

#The ID of the distribution to update
distid=E2OF53FBHS5B8K

#get config and ETAG
config=$(aws cloudfront get-distribution-config --id $distid --query 'DistributionConfig')
etag=$(aws cloudfront get-distribution-config --id $distid --query 'ETag')

#replace the ID of the old certificate with the ID of the new certificate
config=$(echo $config | sed 's/8cfd7dae-9b6a-4d08-94bb-111111111111/8cfd7dae-9b6a-4d08-94bb-222222222222/')

aws cloudfront update-distribution --id $distid --distribution-config file://<(echo $config) --if-match $(echo $etag|sed 's/"//g')
