#!/bin/bash
#comment out line3 after run once -keith
brew install jq >/dev/null 2&>1 || sudo /bin/bash -c 'apt-get install jq -y >/dev/null 2&>1 || yum install jq -y >/dev/null 2&>1'

command='aws ec2 describe-instances'
if [ -n "$1" ]; then
  command="$1"
fi

creds=$(echo $(echo $(aws sts get-session-token) | jq -r '.Credentials'))
echo $creds
akid=$(echo $creds|jq -r '.AccessKeyId')
sac=$(echo $creds|jq -r '.SecretAccessKey')
tok=$(echo $creds|jq -r '.SessionToken')

AWS_ACCESS_KEY_ID=$akid AWS_SECRET_ACCESS_KEY=$sac AWS_SESSION_TOKEN=$tok $command
