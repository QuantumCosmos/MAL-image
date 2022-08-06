import json
import requests
from decouple import config
API_KEY = config('MAL_API_KEY')
def getdata(username):
    headers = {
        'Authorization': 'Bearer ' + API_KEY,
    }
    response = requests.get(
        url="https://api.myanimelist.net/v2/users/" + username + "/animelist?offset=0&limit=25&status=watching&sort=list_updated_at&nsfw=1", headers=headers)
    data = response.json()
    with open(username + ".json", 'w') as file:
            json.dump(data, file, indent=4)
            print('data saved')

    image_urls = []

    for node in data["data"]:
        image_urls.append(node["node"]["main_picture"]["large"])

    return image_urls