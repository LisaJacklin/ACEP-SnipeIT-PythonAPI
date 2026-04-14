#filename: asset_automate.py
# created: 2026-04-07
#
# run: python3 asset-automate.py
# requires: config.yaml
# Description:
#

import yaml
from SnipeIT_APIclient import SnipeITClient
from automate.asset_manager import AssetManager
from automate.model_manager import ModelManager
from automate.reference_manager import ReferenceManager

def main():
    #start with loading in the config:
    with open('sample-config.yaml', 'r') as file:
       full_config = yaml.safe_load(file)

    current_env = full_config['active_env']
    config = full_config[current_env]

    cred_file_path = config['cred_file']

    with open(cred_file_path, 'r') as cred_file:
        api_token = cred_file.read().strip()
 
    ref_manager = ReferenceManager(
        script_path=config['reference_script'],
        json_path=config['reference_json']
    )

    ref_manager.refresh_data()
    ref_manager.load_data()

    # now load in the references based off the load data
    status_id=ref_manager.get_id('statuslabels', config['target_status_name'])
    model_id=ref_manager.get_id('models', config['target_model_name'])
    category_id=ref_manager.get_id('categories', config['default_category_name'])
    mfg_id=ref_manager.get_id('manufacturer', config['default_manufacturer_name'])
    fieldset_id=ref_manager.get_id('fieldsets', config['default_fieldset_name'])
    if not status_id:
        print(f"ERROR: Could not find a Status ID for {config['target_status_name']}")
        return
    
    # and get the API requirements filled
    client = SnipeITClient(
        base_url=config['domain'],
        api_key = api_token
    )

    #adding in the asset and model managers to do their thing!
    asset_manager = AssetManager(client)
    model_manager = ModelManager(client)
    
    #additional model items
    target_name = config['target_model_name']
    model_id = model_manager.pull_create_model_id(
        target_name,
        category_id,
        mfg_id,
        fieldset_id
        )

    # add in model safe exit mode
    if not model_id:
        print("Cannot proceed without a valid Model ID")
        return
    
    status_id = 1 #need to remove from
    count = config.get('asset_count', 1)

    print(f"attempting to create {count} assets...")
    print(f"model attempting to be added: {model_id}")
    tags = asset_manager.add_assets(model_id=model_id, status_id=status_id, count=count)

    print("\n---Summary---")
    print(f"Successfully created {len(tags)} assets.")
    if tags:
        print("generated Asset Tags:")
        for tag in tags:
            print(f" - {tag}")

if __name__ == "__main__":
    main()