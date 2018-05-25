#!/bin/bash
region="us-west-2"

for keyid in `aws kms list-keys --query "Keys[].KeyId" --region $region --output text`; do aws kms describe-key --key-id $keyid; done
