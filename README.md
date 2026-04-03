# ACEP-SnipeIT-PythonAPI
## Overview
This repo contains a collection of scripts and tools designed to interact with ACEP's SnipeIT instance using the REST API interface. This toolkit works to provide an automated routine for different admin tasks which I hope will allow for quick, high level overviews of the Asset inventory and status.

### Snipe-IT Reporting
1. Setup a `/reports folder if one is not already setup
2. `python3 SnipeitReport.py`

By running this script, you will be provided a printout within your terminal of the current system count, and ready to deploy assets by location. You will also be given the location and name of the report markdown file.
`Report saved to: reports/snipeit_report_2026-04-03.md`


## Directory Structure
```
├── demo
│   ├── AssetGetRequestAll.py
│   ├── AssetGetRequest.py
│   ├── AssetUpdateDeviceRequest.py
│   └── UsersGetRequest.py
├── pull-ids.py
├── README.md
├── reporting
│   ├── api_client.py
│   ├── asset.py
│   ├── formatter.py
│   └── visuals.py
├── reports # may need to be created
├── SnipeitReport.py
└── templates
    ├── asset-create-template.py
    ├── asset-update-template.py
    ├── manufacturer-create-template.py
    └── models-create-template.py
```
