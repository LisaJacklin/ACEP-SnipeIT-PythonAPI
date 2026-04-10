#filename: asset_manager.py 
# created: 2024-04-07
#
# Description:
#

class AssetManager:
    def __init__(self, api_client):
        self.client = api_client
    
    def add_assets(self, model_id, status_id, count=1, **kwargs):
        created_tags = []

        #go through and create a payload for each asset
        for i in range(count):
            payload = {
                "model_id": model_id, 
                "status_id": status_id
            }
        
        payload.update(kwargs)

        #now get things pushed to snipeIT
        try:
            result = self.client.create_asset(payload)

            if result.get("status") == "success":
                asset_tag = result.get("payload", {}).get("asset_tag")
                created_tags.append(asset_tag)
                print(f"[{i+1}/{count}] Success: Created asset with tag {asset_tag}")
            else:
                messages = result.get('messages', 'Unknown Error')
                print(f"[{i+1}/{count}] Failed to create asset: {messages}")
        
        except Exception as e:
            print(f"[{i+1}/{count}] Exception occurred: {e}")
        
        return created_tags