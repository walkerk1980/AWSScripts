#!/usr/bin/perl
#pull a cert from curling a URL

#set the URL
my $url='https://good.sca2a.amazontrust.com';

my $cmd="curl -s $url";

my $certoutput=`$cmd`;

#cut junk off beginning of last cert
my $lastcertsub1=substr(substr($certoutput, rindex($certoutput, 'BEGIN')-5), 'END');
#cut junk off end of last cert
my $lastcert=substr($lastcertsub1, 0, index($lastcertsub1, 'END')+20);

#cut junk off beginning of first cert
my $firstcertsub1=substr(substr($certoutput, index($certoutput, 'BEGIN')-5), 'END');
#cut junk off end of first cert
my $firstcert=substr($firstcertsub1, 0, index($firstcertsub1, 'END')+20);

print($lastcert . "\n" . $firstcert);

#uncomment below lines to create pem file
#$cmd='echo "' . $lastcert . "\n" . $firstcert . '" >lastcert.pem';
#system($cmd);
