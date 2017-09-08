#!/usr/bin/perl

# The purpose of this script is to automate the process described in the link below
# Use this script at your own risk
# Obtaining the Thumbprint for an OpenID Connect Identity Provider 
# http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html

#requires jq package
#requires perl
#requires openssl

#set the oidc idp URL
my $idpURL='https://login.microsoftonline.com/fabrikamb2c.onmicrosoft.com/v2.0/.well-known/openid-configuration';

my $cmd='curl -s ' . $idpURL . ' |jq -r \'.jwks_uri\'';

#run output of curl through jq
my $jwksURI=`$cmd`;

#cut off prepended https://
my $fullURL=substr($jwksURI, 8);

#cut off host of URL
my $hostURL=substr($fullURL, 0, index($fullURL, '/'));

$cmd='openssl s_client -showcerts -connect ' . $hostURL . ':443 </dev/null 2>/dev/null';

#use ssl_connect to get certificate chain
my $sslclientoutput=`$cmd`;

#cut junk off beginning of last cert
my $lastcertsub1=substr(substr($sslclientoutput, rindex($sslclientoutput, 'BEGIN')-5), 'END');
#cut junk off end of cert
my $lastcert=substr($lastcertsub1, 0, index($lastcertsub1, 'END')+20);

#create pem file
$cmd='echo "' . $lastcert . '" >oidcert.pem';
system($cmd);

$cmd='openssl x509 -fingerprint -noout -in oidcert.pem';
my $opensslfinger=`$cmd`;

#cut off junk at beginning
my $fingerprint=substr($opensslfinger, index($opensslfinger, '=')+1);

#get rid of colons
$fingerprint =~  s/://g;

print $fingerprint
