#!/usr/bin/env python

import json
from snipeit import Users
from pathlib import Path

server='http://10.8.0.197:8000'
token = Path('../creds/snipeitkey.cred').read_text().strip()

U = Users()
#r = U.get(server, token, 5) # With a limit of results
r = U.get(server, token) # Using default limit of 50 for results

#decode output for tabulate to process
if isinstance(r, bytes):
    r = r.decode("utf-8")
if isinstance(r, str):
    r = json.loads(r)

# writes to assets.json file all assets w/tags
with open("users.json", "w") as file:
    print(json.dump(r,file, indent=4))

