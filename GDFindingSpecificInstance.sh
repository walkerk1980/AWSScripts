#!/bin/bash

instanceid=\`i-05dfa7572db3b272d\`;region='us-west-2'
detector=$(aws guardduty list-detectors --query DetectorIds --output text --region=$region) && for finding in $(aws guardduty list-findings --detector-id $detector --query FindingIds --output text --region=$region); do aws guardduty get-findings --detector-id $detector --finding-ids $finding --query Findings[?Resource.InstanceDetails.InstanceId==$instanceid] --region=$region; done
