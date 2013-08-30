#!/usr/bin/env python

from suds.client import Client
from suds.xsd.sxbasic import Import
import sys

for s in ('Authority','Common','Message','Notification','Recipient','Sender','Service'): 
   Import.bind('http://minameddelanden.gov.se/schema/%s' %s,'file:///home/leifj/work/sunet.se/pymmclient/schema/%s.xsd' % s)

client = Client(sys.argv[1])
print client
