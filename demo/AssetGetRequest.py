#!/usr/bin/env python

from snipeit import Assets
from pathlib import Path

server='http://10.8.0.197:8000'
token = Path('../creds/snipeitkey.cred').read_text().strip()


A = Assets()
#r = A.get(server, token, 5) # With a limit of results
r = A.get(server, token, 1) # Using default limit of 50 for results
print (r)
