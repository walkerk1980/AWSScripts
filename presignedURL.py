#!/usr/bin/python3

# This script is provided 'AS IS' - use is at own risk!
# Importing base modules
import boto3
import requests
from botocore.client import Config

# Getting the bucket region and setting client:
region = input('Please enter the region your bucket is hosted in (e.g. \'us-west-1\'):')

s3 = boto3.client('s3',region_name=region, config=Config(s3={'addressing_style': 'path'}))

# Getting bucket name:
customer_bucket = input('Enter the name of the bucket to upload logs to(e.g. \'my-bucket\'): ')

# Name of the object that will be uploaded to S3 - something logical is suggested,
key_name = input('Enter the object name of the file to be upload(e.g. \'file_name.tar\'): ')

url = s3.generate_presigned_url(
    ClientMethod='put_object',
    Params={
        'Bucket': customer_bucket,
        'Key': key_name
    },
    ExpiresIn=172800,
    HttpMethod='PUT'
)

print('Please copy the below and share it with the person you wish to receive the file from:\n\r\n\r' + 'curl --request PUT --upload-file /path/to/file.tar ' + '"' + str(url) + '"' + '\n\r')
