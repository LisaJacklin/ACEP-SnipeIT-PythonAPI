#filename: model_manager.py
# created: 2026-04-08
# 
# description: 
#

import difflib

class ModelManager:
    def __init__(self, api_client):
        self.client = api_client
        self.session_cache = {}

    #used by: 
    # checks to see if a model from system_specs already exists or has a similar name 
    # to prevent as much duplication of similar models as possible.
    def verify_model_name(self, requested_name, existing_models):
        for model in existing_models:
            if model.lower() == requested_name.lower():
                return model
        
        print(f"Model {requested_name} does not exist as written. Searching for similar model titles...")
        close_matches = difflib.get_close_matches(requested_name, existing_models, n=3, cutoff=0.5)

        #if one or more close matches appear, it will ask the user for checks....
        # should adjust this at some point.
        if close_matches: 
            print("Do any of thes models look correct?")
            for i, match in enumerate(close_matches, 1):
                print(f" {i}. {match}")
            print(f"0. No create a brand new model: '{requested_name}")

            #note that adjusting the new model to be limited in name is another change to make
            while True: 
                choice = input("\n Enter number: ").strip()
                if choice.isdigit() and 0 <= int(choice) <= len(close_matches):
                    choice_idx = int(choice)
                    break
                print("invalid input")

            if choice_idx >0: 
                choice_name = close_matches[choice_idx -1]
                print(f"Using existing mode: {choice_name}")
                return choice_name

            print(f"Creating a new Model: {requested_name}")
            return requested_name
    
    # search for model, and creates if it doesn't exist
    def pull_create_model_id(
        self, raw_model_name, category_id, manufacturer_id, 
        existing_models=None, fieldset_id=None):

        if existing_models:
            model_name = self.verify_model_name(raw_model_name, existing_models)
        else:
            model_name = raw_model_name

        if model_name in self.session_cache:
            return self.session_cache[model_name]

        try: 
            search_results = self.client.get_all(f"models?search={model_name}")
            rows = []

            if isinstance(search_results, list):
                rows = search_results
            elif isinstance(search_results, dict):
                rows = search_results.get("rows", [])

            for row in rows:
                if isinstance(row, dict) and row.get("name", "").lower() == model_name.lower():
                    found_id = row.get("id")
                    print(f"Found existing model: {model_name}")
                    self.session_cache[model_name] = found_id
                    return found_id
        except Exception as e:
            print(f"Failed to create model: {e}")
        
        new_id = self.create_new_model(
            model_name=model_name,
            category_id=category_id,
            manufacturer_id=manufacturer_id,
            fieldset_id=fieldset_id)
        if new_id:
            self.session_cache[model_name] = new_id
        
        return new_id
     
        # #and if the model isn't found: 
    def create_new_model(self, model_name, category_id, manufacturer_id, fieldset_id=None):    
        print(f"Creating new model...")

        payload = {
            "name": model_name, 
            "category_id": category_id,
            "manufacturer_id": manufacturer_id,
            "fieldset_id": fieldset_id,
            "notes": "UPDATE INFO!"
        }

        try:
            result = self.client.create_model(payload)
            if result.get("status") == "success":
                new_model_id = result.get("payload", {}).get("id")
                print("\n" + "="*50)
                print(f" WARNING: Created rough model '{model_name}' (ID: {new_model_id}).")
                print(" Please log into Snipe-IT later to verify/update its details.")
                return new_model_id
            else:
                error_msg = result.get('messages') if result else "Unknown Error"
                print(f"API rejected creating the model: {e}")
                return None

        except Exception as e:
            print(f"Failed to create model: {e}")
            return None


   
