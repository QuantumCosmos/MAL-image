from math import ceil
from time import sleep
from PIL import Image
from io import BytesIO
import pyrebase
from decouple import config
import requests
import os
from getdata import getdata
from imagebase import upload

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
    print("Successful upload")

def get_users():
  with open("users.txt", 'r') as file:
    users = file.readlines()
    users = [line.rstrip() for line in users]
  return users

def get_images(urls):
  r = [requests.get(url) for url in urls]
  print(len(r), "Images loaded")
  images = [Image.open(BytesIO(x.content)).resize((400, 600)) for x in r]
  widths, heights = zip(*(i.size for i in images))
  return images

def create_canvas(url_len):
  total_width = 400*min(5, url_len)
  max_height = 600*ceil(url_len/5)

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
  return new_im

users = get_users()
storage = init()
while True:
  for username in users:
    print("User loaded:", username)
    urls = getdata(username)

    new_im, total_width = create_canvas(len(urls))
    images = get_images(urls)
    new_image = build_collage(images, total_width)
    print("Collage building compleat")
    image_name = username + ".png"
    new_im.save(image_name)
    print("Image Saved")
    upload(image_name, storage)
    os.remove(image_name)
    print("Image deleted from local storage")
    sleep(30)
  sleep(300)