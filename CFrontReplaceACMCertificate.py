#!/usr/bin/python
import boto3

cf = boto3.client('cloudfront')

distributions=cf.list_distributions()

print("\nAvailable Distributions:\n")
for distribution in distributions['DistributionList']['Items']:
	print("Domain: " + distribution['DomainName'])
	print("Distribution Id: " + distribution['Id'])
	print("Certificate Source: " + distribution['ViewerCertificate']['CertificateSource'])
        if (distribution['ViewerCertificate']['CertificateSource'] == "acm"):
		print("Certificate: " + distribution['ViewerCertificate']['Certificate'])
	print("")

print('Enter the Distribution Id of the CloudFront Distribution who\'s ACM Certificate you would like to replace. ')
distribution_id = raw_input('Note that certificate source must be ACM - DistributionId: ')

distribution_config_response=cf.get_distribution_config(Id=distribution_id)
distribution_config=distribution_config_response['DistributionConfig']
distribution_etag=distribution_config_response['ETag']

if (distribution_config['ViewerCertificate']['CertificateSource'] != "acm"):
	print("\nThe DistributionId you have entered is not currently using an ACM Certificate, exiting...\n")
	exit()

old_cert_arn=distribution_config['ViewerCertificate']['ACMCertificateArn']

new_cert_arn=raw_input("Please enter the ARN of the new ACM Certificate you would like to attach to Distribution " + distribution_id + ": ")

print("Replacing: " + old_cert_arn + "\nwith: " + new_cert_arn + "\n")

distribution_config['ViewerCertificate']['ACMCertificateArn']=new_cert_arn
distribution_config['ViewerCertificate']['Certificate']=new_cert_arn

cf.update_distribution(DistributionConfig=distribution_config,Id=distribution_id,IfMatch=distribution_etag)
