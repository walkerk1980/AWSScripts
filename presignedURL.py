#!/usr/bin/python3
import boto3
#http://docs.python-requests.org/en/master/
import requests
from botocore.client import Config

region = input('Please enter your bucket's region (e.g. \'us-east-1\'):')

#instantiate client
s3 = boto3.client('s3',region_name=region, config=Config(s3={'addressing_style': 'path'}))

# Bucket Name
upload_bucket = input('Enter the name of the bucket to upload file to: ')

#Destination object name
key_name = input('What would you like the file to be name in your bucket: ')

#local file to upload
fileName = input('What is the full path of the local file you want to upload: ')

#http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.generate_presigned_post
#param for request, file handle, read binary
file = {'file': open(fileName, 'rb')}

#param for request
post = s3.generate_presigned_post(
    ExpiresIn=172800,
    Bucket=upload_bucket,
    Key=key_name
)

#http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.generate_presigned_url
#upload file
requests.post(post['url'], data=post['fields'], files=file)

#generate presgined download url
get = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': upload_bucket,'Key': key_name},
    ExpiresIn=172800,
)

#print presigned url
print()
print("This is the presigned URL to download the s3 object you just uploaded: ")
print(get)
