#!/bin/bash

roletoassumearn='arn:aws:iam::123456789012:role/rolename'
sessionname='session1'

if [ "unset" == "$1" ];then
  unset AWS_ACCESS_KEY_ID; unset AWS_SECRET_ACCESS_KEY; unset AWS_SESSION_TOKEN; unset AWS_CREDENTIAL_EXPIRATION; return 0;
fi
if [ -n "$1" ];then
  roletoassumearn=$1
  else
    echo -e "usage: source $0 "$roletoassumearn" "$sessionname"\n\r";
    echo -e "to unset variables: source $0 "unset"\n\r"; exit 0;
fi
if [ -n "$2" ];then
  sessionname=$2
fi

creds=$(echo $(echo $(aws sts assume-role --role-arn $roletoassumearn --role-session-name $sessionname --query Credentials --output text)))
echo $creds

akid=$(echo $creds|cut -d' ' -f1)
sac=$(echo $creds|cut -d' '  -f3)
tok=$(echo $creds|cut -d' ' -f4)
sessionExpiration=$(echo $creds|cut -d' ' -f2)

export AWS_ACCESS_KEY_ID=$akid
export AWS_SECRET_ACCESS_KEY=$sac
export AWS_SESSION_TOKEN=$tok
export AWS_CREDENTIAL_EXPIRATION=$sessionExpiration

echo -e "\nThe credentials you have exported will expire at $sessionExpiration"
