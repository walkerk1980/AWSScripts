#!/usr/bin/env python3
import sys
import boto3
import configparser
import base64
import xml.etree.ElementTree as ET
from os.path import expanduser

class saml:
    def __init__(self, assertion):
        self.assertion = assertion

    def parse(self):
        # Better error handling is required for production use.
        if self.assertion == '':
            #TODO: Insert valid error checking/handling
            print('SAML Response did not contain a valid SAML assertion')
            sys.exit(1)

        # Parse the returned assertion and extract the first authorized role
        awsroles = []
        root = ET.fromstring(base64.b64decode(self.assertion))
        for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
            if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
                for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                    awsroles.append(saml2attributevalue.text)
        arns = {}
        arns['role_arn'] = awsroles[0].split(',')[0]
        arns['principal_arn'] = awsroles[0].split(',')[1]
        return arns

    def assume_role(self, role_arn, principal_arn, region):
        # Use the assertion to get an AWS STS token using Assume Role with SAML
        client = boto3.client(
            'sts',
            region_name=region
        )
        token = client.assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=self.assertion,
        )
        return token

    def write_credentials_file(self, token, region, output_format = 'json', awsconfigfile = '/.aws/credentials'):
        # Write the AWS STS token into the AWS credential file
        home = expanduser("~")
        filename = home + awsconfigfile

        # Read in the existing config file
        config = configparser.RawConfigParser()
        config.read(filename)

        # Put the credentials into a saml specific section instead of clobbering
        # the default credentials
        if not config.has_section('saml'):
            config.add_section('saml')

        config.set('saml', 'output', output_format)
        config.set('saml', 'region', region)
        config.set('saml', 'aws_access_key_id', token['Credentials']['AccessKeyId'])
        config.set('saml', 'aws_secret_access_key', token['Credentials']['SecretAccessKey'])
        config.set('saml', 'aws_session_token', token['Credentials']['SessionToken'])

        # Write the updated config file
        with open(filename, 'w+') as configfile:
            config.write(configfile)

        print('\n\rSTS credentials have been stored in the AWS configuration file {0} under the saml profile.'.format(filename))
        print('Note that they will expire at {0}.'.format(token['Credentials']['Expiration']))
        print('To use these credentials, call the AWS CLI with the --profile option. See example below: \n\r')
        print('aws sts get-caller-identity --profile saml \n\r')

if __name__ == "__main__":
    # STS endpoint region
    sts_region = 'us-east-1'

    # location of base64 encoded saml file
    base64_encoded_saml_file = expanduser('~/saml_assertion.b64')

    # open the saml assertion file
    with open(base64_encoded_saml_file, 'r+') as saml_assertion:
        print(base64_encoded_saml_file + ' found, parsing SAML assertion...')
        # read the saml assertion file and use it to initialize the saml class
        saml = saml(saml_assertion.read())
        # get the first role in the saml assertion
        roles_to_assume = saml.parse()
        # assume the first role in the saml assertion
        credentials = saml.assume_role(role_arn=roles_to_assume.get('role_arn'), principal_arn=roles_to_assume.get('principal_arn'), region=sts_region)

        # Optionally place the assumed role credentials in config file
        saml.write_credentials_file(credentials, sts_region)
        client_region = 'us-east-1'
        # Use the credentials that you have placed in the config file with an sts client
        sts_client_from_profile = boto3.Session(profile_name='saml').client(service_name='sts', region_name=client_region)
        # use the STS client to GetCallerIdentity
        caller_arn_from_profile = sts_client_from_profile.get_caller_identity().get('Arn')
        print('Client credential ARN from profile saml: ' + caller_arn_from_profile)

        # OR

        # use credentials directly with AWS in boto3 Session
        # use the credentials to create a session
        session = boto3.Session(
            aws_access_key_id=credentials.get('Credentials').get('AccessKeyId'),
            aws_secret_access_key=credentials.get('Credentials').get('SecretAccessKey'),
            aws_session_token=credentials.get('Credentials').get('SessionToken')
        )
        # create an STS client with the session
        sts_client_with_direct_credentials = session.client(service_name='sts', region_name=client_region)
        # use the STS client to GetCallerIdentity
        caller_arn_from_direct_credentials = sts_client_with_direct_credentials.get_caller_identity().get('Arn')
        print('Client credential ARN used directly:' + caller_arn_from_direct_credentials)
