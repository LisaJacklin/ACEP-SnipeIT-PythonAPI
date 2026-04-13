#filename: model_manager.py
# created: 2026-04-08
# 
# description: 
#

class ModelManager:
    def __init__(self, api_client):
        self.client = api_client

    # search for model, and creates if it doesn't exist
    def pull_create_model_id(self, model_name, category_id, manufacturer_id):
        # print(f"Searching for model: '{model_name}...")
        # existing_models = self.client.get_all("models")

        # for model in existing_models:
        #     if model.get('name', '').strip().lower() ==model_name.strip().lower():
        #         model_id = model.get('id')
        #         print(f" Found existing model! ID: {model_id}")
        #         return model_id
        
        # #and if the model isn't found: 
        print(f"Creating new model...")

        payload = {
            "name": model_name, 
            "category_id": category_id,
            "manufacturer_id": manufacturer_id,
            "notes": "UPDATE INFO!"
        }

        try:
            result = self.client.create_model(payload)
            if result.get("status") == "success":
                new_model_id = result.get("payload", {}).get("id")
                print("\n" + "="*50)
                print(f" WARNING: Created rough model '{model_name}' (ID: {new_model_id}).")
                print(" Please log into Snipe-IT later to verify/update its details.")
                print("="*50 + "\n")
                return new_model_id
            else:
                raise Exception(f"API rejected model creation: {result.get('messages')}")

        except Exception as e:
            print(f"Failed to create model: {e}")
            return None
