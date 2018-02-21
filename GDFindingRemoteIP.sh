#!/bin/bash

remoteip=\`8.8.8.8\`;region='us-west-2'
#!/bin/bash
detector=$(aws guardduty list-detectors --query DetectorIds --output text --region $region) && for finding in $(aws guardduty list-findings --detector-id $detector --query FindingIds --output text --region $region); do aws guardduty get-findings --detector-id $detector --finding-ids $finding --query Findings[?Service.Action.NetworkConnectionAction.RemoteIpDetails.IpAddressV4==$remoteip]; done
