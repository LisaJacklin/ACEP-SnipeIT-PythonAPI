# Filename: user-query.py
# date: 2026-08-04
#
# Use: 
# Description: 

from pathlib import Path
import requests

## Standard Configuration ---
URL = "https://snipeit.camio.acep.uaf.edu/api/v1"
snipeit_api_token = Path('prod.cred').read_text().strip()

header = {
    "Accept": "application/json",
    "Authorization": f"Bearer {snipeit_api_token}",
    "Content-Type": "application/json"
}
## End Standard Configuration ---

#need to gather the group names
def get_group_lookup_table() -> dict[int, str]:
    """Fetches all groups once and creates a {group_id: group_name} lookup dict."""
    url = f"{URL}/groups"
    response = requests.get(url, headers=header)
    
    group_map = {}
    if response.status_code == 200:
        groups = response.json().get("rows", [])
        for group in groups:
            group_map[group.get("id")] = group.get("name")
        print(f"Loaded {len(group_map)} group definitions.")
    else:
        print(f"Failed to fetch groups: {response.status_code}")
        
    return group_map

def get_users_groups():
    group_lookup = get_group_lookup_table()
    
    end_url = f"{URL}/users"
    limits = 50
    offset = 0
    total_users = None
    all_users_data = []

    #time to get the users
    while total_users is None or offset < total_users:
        response = requests.get(end_url, headers=header, params={"limit": limits, "offset": offset})
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}: {response.text}")
            break

        data = response.json()
        total_users = data.get("total", 0)
        rows = data.get("rows", [])

        for user in rows:
            # Extract group IDs from the user payload
            # Snipe-IT returns groups as a dict/list structure or a list of IDs
            raw_groups = user.get("groups", {})
            group_ids = []

            if isinstance(raw_groups, dict) and "rows" in raw_groups:
                group_ids = [g.get("id") for g in raw_groups.get("rows", []) if g.get("id")]
            elif isinstance(raw_groups, list):
                # Handles cases where groups is returned directly as a list of IDs or dicts
                group_ids = [g.get("id") if isinstance(g, dict) else g for g in raw_groups]

            # Map the IDs to names using our pre-fetched lookup table
            group_names = [
                group_lookup.get(gid, f"Unknown Group (ID: {gid})") 
                for gid in group_ids
            ]

            all_users_data.append({
                "id": user.get("id"),
                "name": user.get("name"),
                "username": user.get("username"),
                "email": user.get("email"),
                "group_ids": group_ids,
                "group_names": group_names
            })

        offset += limits

    return all_users_data

def main():

    #what do I want to share out to terminal?
    users = get_users_groups()
    print(f"\nRetrieved {len(users)} users:\n" + "="*50)

    for u in users:
        groups_str = ", ".join(u["group_names"]) if u["group_names"] else "No Groups Assigned"
        print(f"ID: {u['id']} | Name: {u['name']} ({u['username']})")
        print(f"  └─ Email:  {u['email']}")
        print(f"  └─ Groups: {groups_str}")
        print("-" * 50)

if __name__ == "__main__":
    main()
