#!/bin/bash

region='us-west-2';

detector=$(aws guardduty list-detectors --query DetectorIds --output text --region $region) && for setid in $(aws guardduty list-ip-sets --detector-id $detector --output text --query IpSetIds --region $region); do aws guardduty get-ip-set --ip-set-id $setid --detector-id $detector --region $region; done

for list in $(for setid in $(aws guardduty list-ip-sets --detector-id $detector --output text --query IpSetIds --region $region); do aws guardduty get-ip-set --ip-set-id $setid --detector-id $detector --query Location --output text --region $region; done); do aws s3 cp $list -; done
