from copy import copy
import json
import re
import requests
from decouple import config
API_KEY = config('MAL_API_KEY')

def comp_list(username):
    headers = {
        'Authorization': 'Bearer ' + API_KEY,
    }
    response_comp = requests.get(url="https://api.myanimelist.net/v2/users/" + username +
                                 "/animelist?offset=0&limit=50&status=completed&sort=list_updated_at&nsfw=1", headers=headers)
    data_comp = response_comp.json()
    image_ids = []
    image_url_dict = {}
    for node in data_comp["data"]:
        image_url_dict[node["node"]["title"]
                       ] = node["node"]["main_picture"]["large"]
        image_ids.append(node["node"]["id"])
    return image_url_dict, image_ids

def writejson(data, username):
    file = open(username + "com" + ".json", 'w')
    json.dump(data, file, indent=4)
    print("\"{}\": Data Saved".format(username))
    
def last_comp_list(data, username):
    titles = []
    with open(username + ".txt", 'w') as file:
        for d in data:
            if 'Completed' in d:
                s = (re.search("<title>(.*)</title>", d).group(1).split(' - ')[0])
                file.write("%s\n"%s)
                titles.append(s)
    return titles


def get_final_image_urls(titles=[], file_data=[], image_url_dict={}):
    titles_final = copy(titles)
    titles_final.extend(t for t in file_data if t not in titles)
    titles_final = titles_final[:10]
    titles_final.pop()
    image_urls = []
    for t in titles_final:
        image_urls.append(image_url_dict[t])
    return image_urls





def getdata_comp(username, IGNORE=True):
    response = requests.get(
        url="https://myanimelist.net/rss.php?type=rw&u=" + username)

    data = str(response.content)
    file_data = []
    head = ""
    try:
        f = open(username + ".txt", "r")
        file_data = f.read().split('\n')
        head = file_data[0]
        f.close()
    except FileNotFoundError:
        pass

    data = data.split("<item>")[0:]
    x = [d for d in data if 'Completed' in d][0]
    new_head = re.search("<title>(.*)</title>", x).group(1).split(' - ')[0]
    print("\"{}\": Head: {}".format(username, head))
    print("\"{}\": New Head: {}".format(username, new_head))

    if (head == new_head) and IGNORE:
        print("\"{}\": no change".format(username))
        return []
    else:
        image_url_dict, image_ids = comp_list(username)
        print("\"{}\": Completed-List aquired".format(username))
        titles = last_comp_list(data, username)
        print("\"{}\": File updated".format(username))
        return get_final_image_urls(titles, file_data, image_url_dict), image_ids




if __name__ == "__main__":
    getdata_comp("Chronon", False)
