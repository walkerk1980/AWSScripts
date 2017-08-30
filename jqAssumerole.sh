#!/bin/bash
#comment out line3 after run once -keith
#brew install jq >/dev/null 2&>1 || sudo /bin/bash -c 'apt-get install jq -y >/dev/null 2&>1 || yum install jq -y >/dev/null 2&>1'

roletoassumearn='arn:aws:iam::123456789012:role/rolename'
sessionname='session1'

if [ "unset" == "$1" ];then
  unset AWS_ACCESS_KEY_ID; unset AWS_SECRET_ACCESS_KEY; unset AWS_SESSION_TOKEN; exit 0;
fi
if [ -n "$1" ];then
  roletoassumearn=$1
  else
    echo -e "usage: source $0 "$roletoassumearn" "$sessionname"\n\r";
    echo -e "to unset variables: $0 "unset"\n\r"; exit 0;
fi
if [ -n "$2" ];then
  sessionname=$2
fi

creds=$(echo $(echo $(aws sts assume-role --role-arn $roletoassumearn --role-session-name $sessionname) | jq -r '.Credentials'))
echo $creds
akid=$(echo $creds|jq -r '.AccessKeyId')
sac=$(echo $creds|jq -r '.SecretAccessKey')
tok=$(echo $creds|jq -r '.SessionToken')
sessionExpiration=$(echo $creds|jq -r '.Expiration')

export AWS_ACCESS_KEY_ID=$akid
export AWS_SECRET_ACCESS_KEY=$sac
export AWS_SESSION_TOKEN=$tok

echo -e "\nThe credentials you have exported will expire at $sessionExpiration"
