#!/bin/bash

queueurl=https://sqs.us-west-2.amazonaws.com/319351118808/test2.fifo
messagebody="HelloWorld2"

#This script will only work once if you do not change the deduplication id after each run
dedupid=3

#put a message in the queue
aws sqs send-message --queue-url $queueurl --message-body $messagebody --message-group-id 1 --message-deduplication-id $dedupid

#receive a message
message=$(aws sqs receive-message --queue-url $queueurl --output text --query 'Messages[].{id:MessageId,rh:ReceiptHandle,md5:MD5OfBody,body:Body}')

sleep 5

#echo message id
echo $message|cut -d' ' -f1

#echo message body MD5
echo $message|cut -d' ' -f2

#echo message body
echo $message|cut -d' ' -f3

#delete message
aws sqs delete-message --queue-url $queueurl --receipt-handle $(echo $message|cut -d' ' -f4)
