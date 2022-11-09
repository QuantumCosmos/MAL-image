import json
import requests
from decouple import config
API_KEY = config('mal_api')

def seasonals(year, season):
    headers = {
        'Authorization': 'Bearer ' + API_KEY,
    }
    response = requests.get(
        url="https://api.myanimelist.net/v2/anime/season/{}/{}?limit=200&nsfw=1".format(year, season), headers=headers)
    data = response.json()
    file = open("anime"+year+season + ".json", 'w')
    json.dump(data, file, indent=4)
    seasonals_id_list = []
    for node in data["data"]:
        seasonals_id_list.append(node["node"]["id"])
    print("Data Saved")
    return seasonals_id_list

