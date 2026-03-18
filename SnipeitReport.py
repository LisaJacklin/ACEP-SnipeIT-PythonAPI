# File: SnipeitAssetReport.py
# Date: 2026-03-17
#
# Run: 
# Description: 
#

import requests
import json #formatting
from pathlib import Path
from collections import Counter

# Configuration for API
api_key = Path('prod.cred').read_text().strip()
base_url = "http://snipeit.camio.acep.uaf.edu/api/v1/"
headers = {
 "Authorization": f"Bearer {api_key}", 
 "Accept": "application/json", 
 "Content-Type": "application/json"
}
# end of configuration


