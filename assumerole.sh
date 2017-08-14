#!/bin/bash

roletoassumearn='arn:aws:iam::123456789012:role/rolename'
sessionname='session1'
rolename='rolename'

echo "usage assumeRole.sh 'arn:aws:iam::123456789012:role/rolename' 'session1'"

curlResult=$(curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/$rolename)

KeyId=$(echo $curlresult|grep 'KeyId'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')
Secret=$(echo $curlresult|grep 'SecretAcc'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')
Tok=$(echo $curlresult|grep 'Token'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')

session=$(aws sts assume-role --role-arn $roletoassumearn --role-session-name $sessionname)

SessionTok=$(echo $session| sed 's/{\|}\|,/\n/g'|grep 'SessionToken'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')
SessionAccessKey=$(echo $session| sed 's/{\|}\|,/\n/g'|grep 'AccessKeyId'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')
SessionSecretAccessKey=$(echo $session| sed 's/{\|}\|,/\n/g'|grep 'SecretAccess'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')
SessionExpiration=$(echo $session| sed 's/{\|}\|,/\n/g'|grep 'Expiration'|cut -d':' -f2|sed 's/,//g'|sed 's/ //g'|sed 's/"//g')

export AWS_ACCESS_KEY_ID=$SessionAccessKey
export AWS_SECRET_ACCESS_KEY=$SessionSecretAccessKey
export AWS_SESSION_TOKEN=$SessionTok

echo -e "\nThe credentials you have exported will expire at $SessionExpiration"
