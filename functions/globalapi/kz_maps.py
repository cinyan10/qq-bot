import json
import requests


def fetching_maps(use_local=True):
    if use_local:
        with open('functions/globalapi/maps.json', 'r', encoding='utf-8') as json_file:
            maps_data = json.load(json_file)
    else:
        api_url = "https://kztimerglobal.com/api/v2.0/maps?is_validated=true&limit=2000"
        response = requests.get(api_url)
        response.raise_for_status()
        maps_data = response.json()
        with open('functions/globalapi/maps.json', 'w', encoding="utf-8") as json_file:
            json.dump(maps_data, json_file)

    return maps_data


def get_map_tier(map_name=None, map_id=None):
    maps_data = fetching_maps()
    if map_name is not None:
        for kz_map in maps_data:
            if kz_map['name'] == map_name:
                return kz_map['difficulty']
    elif map_id is not None:
        for kz_map in maps_data:
            if kz_map['id'] == map_id:
                return kz_map['difficulty']


if __name__ == '__main__':
    tier = get_map_tier(map_id=842)
    print(tier)
    pass


def fetch_map_tier(map_name: str):
    try:
        response = requests.get('https://kztimerglobal.com/api/v2.0/maps/name/' + map_name)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response as JSON (assuming the API returns JSON)
            data = response.json()
            return data['difficulty']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
