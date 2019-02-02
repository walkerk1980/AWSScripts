#!/usr/bin/python
try:
  import boto3
except:
  print('\n\rboto3 module is not installed, please run: pip install boto3\n\r')
  exit(1)
import random
try:
  import dns.resolver
except:
  print('\n\rdnspython module is not installed, please run: pip install dnspython\n\r')
  exit(1)
import sys
import argparse
import json

default_regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1']
region='us-west-2'

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', default=region, choices=default_regions, help='Region where you wish to check certificates.')
args = parser.parse_args()

dns_resolver = dns.resolver.Resolver()
all_nameservers = ['8.8.8.8', '4.2.2.2', '1.1.1.1', '8.8.4.4']
ns_index=random.randint(0,len(all_nameservers)-1)
nameserver = [all_nameservers[ns_index]]
dns_resolver.nameservers = nameserver

acm = boto3.client('acm', region_name=region)
r53 = boto3.client('route53')

def read():
  if sys.version_info[0] < 3:
    return(raw_input())
  else:
    return(input())

def exit_prog(return_code):
    print('Exiting..')
    exit(return_code)

def continue_or_exit(message):
  print(message)
  print('Do you want to continue? (y/n)')
  if str(read()).lower() == 'y':
    print('Continuing...')
  else:
    exit_prog(0)

def continue_yn(message):
  print(message)
  print('Do you want to continue? (y/n)')
  if str(read()).lower() == 'y':
    print('Continuing...')
    return(1)
  else:
    return(0)

def get_record(name, type):
  return dns_resolver.query(name, type)

def list_all_public_hosted_zones():
  print('\n\rPublic Hosted Zones: ')
  hosted_zones = r53.list_hosted_zones()
  for hz in hosted_zones['HostedZones']:
    if hz['Config']['PrivateZone'] == False:
      print('\n\rHosted Zone Id: ' + str(hz['Id'].split('/')[2]) )
      print('Hosted Zone Name: ' + str(hz['Name']) )

def get_hz_delegation(hz_id):
  try:
    hz_delegation = []
    get_hz_response = r53.get_hosted_zone(Id=hz_id)
    print('Hosted Zone Delegation Set: ')
    for ns in get_hz_response['DelegationSet']['NameServers']:
      if not str(ns).endswith('.'):
        ns = str(ns) + '.'
      hz_delegation.extend([str(ns)])
    print(hz_delegation)
    return(hz_delegation)
  except:
    print('Error pulling hosted zone delegation')
    return(hz_delegation)

def get_domain_ns(domain):
  try:
    domain_ns = []
    domain_ns_records=get_record(domain, 'NS')
    print('Domain NS records pulled from DNS: ')
    for ns_rr in domain_ns_records:
      if not str(ns_rr).endswith('.'):
        ns_rr = str(ns_rr) + '.'
      domain_ns.extend([str(ns_rr)])
    print(domain_ns)
    return(domain_ns)
  except:
    print('Could not pull NS records for ' + domain)
    return([])

def get_domain_rr(domain, type):
  try:
    domain_rr = []
    domain_rr_records=get_record(domain, type)
    print('Domain ' + str(type) + ' records pulled from DNS: ')
    for rr in domain_rr_records:
      if type == 'NS'  and not str(rr).endswith('.'):
        rr = str(ns_rr) + '.'
      domain_ns.extend([str(rr)])
    print(domain_rr)
    return(domain_rr)
  except:
    print('Could not pull ' + type + ' records for ' + domain)
    return([])


def get_hosted_zone_by_domain(domain):
  print('\n\rSearching for HZ for ' + domain + '\n\r')
  hosted_zones = r53.list_hosted_zones()
  if len(hosted_zones['HostedZones']) <1:
    print('No Hosted Zones found in Account\n\r')
  for hz in hosted_zones['HostedZones']:
    hz_delegation = []
    domain_ns = []
    if hz['Config']['PrivateZone'] == False:
      if str(hz['Name']) == str(domain) or str(hz['Name']) == str(domain) + '.':
        print('Found Hosted Zone with matching domain..')
        hosted_zone_id = str(hz['Id'].split('/')[2])
        print('\n\rHosted Zone Id: ' + hosted_zone_id )
        print('Hosted Zone Name: ' + str(hz['Name']) )
        domain_ns = get_domain_ns(domain)
#        domain_ns = get_domain_rr(domain, type='NS')
        hz_delegation = get_hz_delegation(hosted_zone_id)
        domain_ns.sort()
        hz_delegation.sort()
        if domain_ns == hz_delegation:
          print('\n\rThis Hosted Zone\'s Delegation and NS records for domain match!')
          print(hz_delegation)
          print(domain_ns)
          create_rr=continue_yn('\n\rI can add a CNAME record for this certificate in this hosted zone: ' + hosted_zone_id)
          if create_rr == 1:
            create_record_set()
        else:
          print('This Hosted Zone\'s Delegation does not match NS records for domain.')


def create_record_set():
  print('Creating DNS Record')
  #TODO

def list_pending_certs():
  print('\n\rCertificates pending DNS Validation: ')
  certs = acm.list_certificates()
  for cert in certs['CertificateSummaryList']:
    cert_description=acm.describe_certificate(CertificateArn=cert['CertificateArn'])
    validation_method=cert_description['Certificate']['DomainValidationOptions'][0]['ValidationMethod']
    issuer=cert_description['Certificate']['Type']
    if issuer == 'AMAZON_ISSUED' and validation_method=='DNS':
      for domain in cert_description['Certificate']['DomainValidationOptions']:
        if domain['ValidationStatus'] == 'PENDING_VALIDATION':
          print('\n\rCertificate: ' + cert['CertificateArn'])
          print('Domain: ' + domain['DomainName'])
          print('Expected RecordName: ' + domain['ResourceRecord']['Name'])
          print('Expected RecordValue: ' + domain['ResourceRecord']['Value'])
          try:
            dns_result=get_record(domain['ResourceRecord']['Name'], 'TXT')
            for txt_rr in dns_result:
              print('Sucessfully pulled TXT record from CNAME: ')
              print(txt_rr)
          except:
            print('could not pull TXT record')
            try:
              dns_result=get_record(domain['ResourceRecord']['Name'], 'CNAME')
              print('CNAME record does exist, but does not point to existing TXT record')
              print('Current incorrect CNAME value: ')
              for cname_rr in dns_result:
                print(cname_rr)
            except:
              print('could not pull CNAME record')
            cert_full_domain=domain['DomainName']
            cert_domain=cert_full_domain[cert_full_domain.index('.')+1:]
            get_hosted_zone_by_domain(cert_domain)



list_pending_certs()

#list_all_public_hosted_zones()


#continue_or_exit("I am going to list your hosted zones.")
