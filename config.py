# config.py 
# Enter in required info here!

import os
from pathlib import Path

# Look for .cred in project directory, or default to home directory ~/.snipeit.cred
# note that currently I have prod.cred so edited this to match below
cred_file = Path(__file__).parent / "prod.cred"

def get_api_token() -> str:
    # Check if token exists in environment variables first
    if os.getenv("snipeit_api_token"):
        return os.getenv("snipeit_api_token").strip()

    # Now read raw string directly from .cred file
    if cred_file.exists():
        token = cred_file.read_text().strip()
        if token:
            return token

    #error checking for api problems
    raise ValueError(f"API token not found! Add it to {cred_file} or set snipeit_api_token.")

# Export config variables
snipeit_api_token = get_api_token()
snipeit_url = os.getenv("snipeit_url", "https://snipeit.camio.acep.uaf.edu")
