#!/usr/bin/env python3
import sys
if sys.version_info[0] < 3:
  print('This script requires python3 or later..')
  exit(1)
import urllib.request
import urllib.error
import json
import argparse

default_regions = ['us-east-1','us-east-2','us-west-1','us-west-2','ap-northeast-1','ap-northeast-2','ap-northeast-3','ap-south-1','ap-southeast-1','ap-southeast-2','ca-central-1','cn-north-1','cn-northwest-1','eu-central-1','eu-west-1','eu-west-2','eu-west-3','sa-east-1']

parser = argparse.ArgumentParser()
parser.add_argument('-4', '--ipv4', nargs='?', const='4', help='Display IPv4 Addresses only')
parser.add_argument('-6', '--ipv6',  nargs='?', const='6', help='Display IPv6 Addresses only')
parser.add_argument('-64', '-46', '--ipAll',  nargs='?', const='46', help='Display IPv4 IPv6 Addresses')
parser.add_argument('-r', '--regions', default=default_regions, help='Display Addresses only for Regions specified as csv')
args = parser.parse_args()

def get_ranges(url):
  try:
    response = urllib.request.urlopen(url, timeout=5)
    response_str = response.read().decode("utf-8")
    response_json = json.loads(response_str)
    return response_json
  except urllib.error.URLError as err:
    print("bad connection")

def get_ipv4(range_json,region=default_regions):
  ipv4_prefixes=''
  for prefix in range_json['prefixes']:
    if (prefix['region'] in region):
      ipv4_prefixes += '\n'
      ipv4_prefixes += prefix['ip_prefix']
  return ipv4_prefixes

def get_ipv6(range_json,region=default_regions):
  ipv6_prefixes=''
  for prefix in range_json['ipv6_prefixes']:
    if (prefix['region'] in region):
      ipv6_prefixes += '\n'
      ipv6_prefixes += prefix['ipv6_prefix']
  return ipv6_prefixes

ranges = get_ranges('https://ip-ranges.amazonaws.com/ip-ranges.json')

if args.ipv4:
  print(get_ipv4(ranges,args.regions))

if args.ipv6:
  print(get_ipv6(ranges,args.regions))

if args.ipAll:
  print(get_ipv4(ranges,args.regions))
  print(get_ipv6(ranges,args.regions))

