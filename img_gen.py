from math import ceil
from PIL import Image
from io import BytesIO
import requests
from getdata import getdata

def get_users():
  with open("users.txt", 'r') as file:
    users = file.readlines()
    users = [users.rstrip() for line in users]
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
for username in users:
  urls = getdata(username)

  new_im, total_width = create_canvas(len(urls))
  images = get_images(urls)
  new_image = build_collage(images, total_width)
  print("Collage building compleat")

  new_im.save(username + ".png")
  print("Image Saved")
