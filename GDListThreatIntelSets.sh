#!/bin/bash

detector=$(aws guardduty list-detectors --query DetectorIds --output text --region $region) && for setid in $(aws guardduty list-threat-intel-sets --detector-id $detector --output text --query ThreatIntelSetIds --region $region); do aws guardduty get-threat-intel-set --threat-intel-set-id $setid --detector-id $detector --region $region; done

for list in $(for setid in $(aws guardduty list-threat-intel-sets --detector-id $detector --output text --query ThreatIntelSetIds --region $region); do aws guardduty get-threat-intel-set --threat-intel-set-id $setid --detector-id $detector --query Location --output text --region $region; done); do aws s3 cp $list -; done
