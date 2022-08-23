from datetime import datetime
from pickle import FALSE
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import pyrebase
from decouple import config
import requests
import os
from get_last_comp import getdata_comp
from getdata import getdata
from seasonal import seasonals

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
    seasonal = Image.open(r"seasonal.png").resize((200, 200))
    return storage, seasonal


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

def get_images(urls, height=600, width=400, ids=[]):
  r = [requests.get(url) for url in urls]
  print("\"{}\": {} Images loaded".format(username, len(r)))
  images = [Image.open(BytesIO(x.content)).resize((width, height)) for x in r]
  return images

def create_canvas(height=600, width=400):
  total_width = 400*3 +100
  max_height = 600*2
  new_im = Image.new('RGBA', (total_width, max_height))
  return new_im, total_width


def build_collage(images, total_width, s_en=True, ids=[], seasonals_id_list=[]):
  x_offset = 0
  y_offset = 150
  for i in range(len(images)):
    im = images[i]
    if x_offset == total_width+50:
      x_offset = 200
      y_offset += im.size[1]-150
    if s_en:
      if ids[i] in seasonals_id_list:
        im.paste(seasonal, (1, -5), seasonal)
    new_im.paste(im, (x_offset, y_offset))
    x_offset += im.size[0]+50

  new_im.thumbnail((320, 350))
  return new_im

users = get_users()
storage, seasonal = init()
IGNORE = False
titles = []
pre_season = None
seasons = {0: "winter",
          1: "spring",
          2: "summer",
          3: "fall"
          }
while True:
  year = str(datetime.now().year)
  season = seasons[datetime.now().month//4]
  if not season == pre_season:
    seasonals_id_list = seasonals(year, season)
    IGNORE = False
  for username in users:
    print("Command:", username)
    if ":w" in username:
      username = username.split(":")[0]
      urls, titles = getdata(username, IGNORE)
      text = "Currently Watching"
      fill_color = (45, 176, 58)
      bind = ":w"
      s_en = True
    elif ":c" in username:
      username = username.split(":")[0]
      urls = getdata_comp(username, IGNORE)
      text = "Last Completed"
      fill_color = (39, 68, 144)
      bind = ":c"
      s_en = True
    else:
      url = []
      print("\"{}\": Task not Specified or Unknown Task".format(username))
      continue

    urls = urls[:5]
    
    if urls == []:
      print("\"{}\": Upload Ignored".format(username))
      continue
    new_im, total_width = create_canvas()
    images = get_images(urls)
    # break


    new_image = build_collage(images, total_width, s_en, titles, seasonals_id_list)
    print("\"{}\": Collage building complete".format(username))
    image_name = username + bind + ".png"
    d1 = ImageDraw.Draw(new_image)
    myFont = ImageFont.truetype('Lato-Bold.ttf', 30)
    w, h = d1.textsize(text, myFont)
    d1.text(((320-w)/2, 0), text, font=myFont, fill=fill_color)
    # new_image.show()
    # img.save("images/image_text.jpg")
    new_im.save(image_name)
    print("\"{}\": Image Saved".format(username))
    upload(image_name, storage)
    os.remove(image_name)
    print("\"{}\": Image deleted from local storage".format(username))
  #   break
  # break
    sleep(30*IGNORE)
  IGNORE = True
  pre_season = season
  sleep(300)
