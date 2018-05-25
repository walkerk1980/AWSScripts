#!/bin/bash

region='us-west-2'

for key in $(aws kms list-keys --region $region --query 'Keys[].KeyId' --output text);do aws kms list-grants --region $region --key-id $key; done
