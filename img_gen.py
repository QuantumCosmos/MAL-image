from time import sleep
from PIL import Image
from io import BytesIO
import pyrebase
from decouple import config
import requests
import os
from get_last_comp import getdata_comp
from getdata import getdata

def init():
    config_info = {
        "apiKey": config("apiKey"),
        "authDomain": config("authDomain"),
        "databaseURL": config("databaseURL"),
        "projectId": config("projectId"),
        "storageBucket": config("storageBucket"),
        "messagingSenderId": config("messagingSenderId"),
        "appId": config("appId"),
        "measurementId": config("measurementId")
        }
    firebase = pyrebase.initialize_app(config_info)
    storage = firebase.storage()
    return storage


def upload(image, storage):
    # storage = init()
    path_on_cloud = "images/" + image
    path_local = image
    storage.child(path_on_cloud).put(path_local)
    print("\"{}\": Image Successfully Uploaded".format(username))

def get_users():
  with open("users.txt", 'r') as file:
    users = file.readlines()
    users = [line.rstrip() for line in users]
  return users

def get_images(urls, height=600, width=400):
  r = [requests.get(url) for url in urls]
  print("\"{}\": {} Images loaded".format(username, len(r)))
  images = [Image.open(BytesIO(x.content)).resize((width, height)) for x in r]
  return images

def create_canvas(height=600, width=400):
  total_width = 800
  max_height = 1800
  new_im = Image.new('RGBA', (total_width, max_height))
  return new_im, total_width


def build_collage(images, total_width):
  x_offset = y_offset = 0
  for im in images:
    if x_offset == total_width:
      x_offset = 0
      y_offset += im.size[1]
    new_im.paste(im, (x_offset, y_offset))
    x_offset += im.size[0]

  # new_im.thumbnail((400, 900))
  return new_im

users = get_users()
storage = init()
IGNORE = False
while True:
  for username in users:
    print("Command:", username)
    if ":w" in username:
      username = username.split(":")[0]
      urls = getdata(username, IGNORE)
      bind = ":w"
    elif ":c" in username:
      username = username.split(":")[0]
      urls = getdata_comp(username, IGNORE)
      bind = ":c"
    else:
      url = []
      print("\"{}\": Task not Specified or Unknown Task".format(username))
      continue

    urls = urls[:6]
    
    if urls == []:
      print("\"{}\": Upload Ignored".format(username))
      continue
    new_im, total_width = create_canvas()
    images = get_images(urls)


    new_image = build_collage(images, total_width)
    print("\"{}\": Collage building complete".format(username))
    image_name = username + bind + ".png"
    new_im.save(image_name)
    print("\"{}\": Image Saved".format(username))
    upload(image_name, storage)
    os.remove(image_name)
    print("\"{}\": Image deleted from local storage".format(username))
    sleep(30)
  IGNORE = True
  sleep(300)
