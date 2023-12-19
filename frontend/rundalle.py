import cv2
import numpy as np
from openai import OpenAI
import tempfile
from PIL import Image, ImageDraw, ImageFont
import shutil
import os
from io import BytesIO
import requests
import uuid
import base64


API_KEY = "put-your-api-key-here"
if (os.getenv("OPENAI_API_KEY") is not None):
  API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def generate_mask_img(in_img, out_path):
  input = cv2.imread(in_img)
  rgba = cv2.cvtColor(input, cv2.COLOR_BGR2RGBA)

  white = np.array([255, 255, 255, 255], dtype=np.uint8)
  mask = cv2.inRange(rgba, white, white)

  rgba[mask != 0] = [0, 0, 0, 0]
  cv2.imwrite(out_path, rgba)


def generate_mask_img_v2(in_img, out_path):
      # Read the input image
    input_image = cv2.imread(in_img)
 
    # Create a mask initialized with zeros
    mask = np.zeros(input_image.shape[:2], np.uint8)
 
    # Define a rectangle around the region of interest (ROI) in the image
    rect = (10, 10, input_image.shape[1]-10, input_image.shape[0]-10)
 
    # Initialize the background and foreground models for GrabCut
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
 
    # Apply GrabCut algorithm
    cv2.grabCut(input_image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
 
    # Modify the mask to create a binary mask for the foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
 
    input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2RGBA)
    # Bitwise AND the input image with the binary mask to get the foreground
    foreground_image = cv2.bitwise_and(input_image, input_image, mask=mask2)
    cv2.imwrite(out_path, foreground_image)

def ft_color(im, x, y):
  width, height = im.size
  # Crop the region of interest (ROI) from the image
  roi = im.crop((x, y, x+width, y+height))

  # Convert the region to grayscale
  gray_roi = roi.convert('L')

  # Get pixel values of the grayscale ROI
  pixel_values = list(gray_roi.getdata())

  # Calculate the average pixel intensity of the ROI
  average_intensity = sum(pixel_values) / len(pixel_values)

  # Threshold to determine leaning towards black or white
  black_threshold = 100  # Adjust as needed
  white_threshold = 200  # Adjust as needed

  if average_intensity < black_threshold:
    return (255, 255, 255)
  elif average_intensity > white_threshold:
     return (0, 0, 0)
  else:
    return (0, 0, 0)

def draw_text_desc(im, brand, name, price):
  image = Image.open(im)
  text_x = 60
  text_y = 850
  text_size = 42

  fontpath = "Biospace.ttf"     
  font = ImageFont.truetype(fontpath, text_size)
  draw = ImageDraw.Draw(image)
  draw.text((text_x, text_y + text_size),  brand, font = font, fill = (0, 0, 0))
  draw.text((text_x, text_y + 2 * text_size + 20),  name, font = font, fill = (0, 0, 0))
  draw.text((text_x * 9, text_y + 35),  price, font = font, fill = (0, 0, 0))
  return image

def cvt_to_png(img_path, out_path):
  jpeg_image = Image.open(img_path)
  jpeg_image.save(out_path, format='PNG')

def generate_file_path(folder, img_name, ext, mask=False):
  path = img_name
  if mask:
    return path + '_mask' + ext
  return path + ext

def generate_ai(path, prompt, brand, name, price):
  img_id = str(uuid.uuid4())
  fp = generate_file_path('in_images', img_id, '.png')
  fp_mask = generate_file_path('in_images', img_id, '.png', True)

  cvt_to_png(path, fp)
  generate_mask_img(path, fp_mask)

  response = client.images.edit(
    model="dall-e-2",
    image=open(fp, 'rb'),
    mask=open(fp_mask, 'rb'),
    prompt=prompt,
    n=1,
    size="1024x1024"
  )

  # print(response.data[0].url)

  response = requests.get(response.data[0].url, stream=True)

  img_id = str(uuid.uuid4())
  gen_img_path = generate_file_path('output_imgs', img_id, '.png')
  with open(gen_img_path, 'wb') as f:
    f.write(response.content)

  final = draw_text_desc(gen_img_path, brand, name, price)
  gen_img_path_final = generate_file_path('output_imgs', img_id + '-final', '.png')
  final.save(gen_img_path_final)

  buffered = BytesIO()
  final.save(buffered, format="PNG")
  b64_img = base64.b64encode(buffered.getvalue())


  return b64_img.decode('UTF-8')