import json
import requests
from decouple import config
API_KEY = config('MAL_API_KEY')

def writejson(data, username):
    file = open(username + ".json", 'w')
    image_urls = []
    json.dump(data, file, indent=4)
    print("\"{}\": Data Saved".format(username))
    for node in data["data"]:
        image_urls.append(node["node"]["main_picture"]["large"])
    return image_urls


def getdata(username):
    headers = {
        'Authorization': 'Bearer ' + API_KEY,
    }
    response = requests.get(
        url="https://api.myanimelist.net/v2/users/" + username + "/animelist?offset=0&limit=25&status=watching&sort=list_updated_at&nsfw=1", headers=headers)
    data = response.json()
    
    try:

        if data == json.load(open(username + ".json", 'r')):
            print("\"{}\": No Changes made".format(username))
            return []
        else:
            return writejson(data, username)
    except FileNotFoundError:
        return writejson(data, username)
