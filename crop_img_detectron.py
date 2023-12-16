import cv2
import numpy as np

import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

foreground = cv2.imread("iphone_15.jpeg")
background = cv2.imread('3625454299.png')

# Convert BGR image to grayscale
gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)

# Threshold to create a mask for the white background
_, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)


crop_background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]), interpolation = cv2.INTER_NEAREST)
_, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
mask = mask.astype(np.float64) / 255

result = (foreground * mask + crop_background * (1 - mask))
result = result.clip(0, 255).astype(np.uint8)


# Invert the mask to highlight the background
# mask_inv = cv2.bitwise_not(mask)

# Create an alpha channel for the image
# alpha = np.zeros(image.shape[:2], dtype=image.dtype)

# Assign alpha channel where the background is not white
# alpha[mask_inv > 0] = 255

# Create a 4-channel RGBA image
# rgba = cv2.merge((image, alpha))



cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# os.environ['STABILITY_KEY'] = 'sk-dLsfsiQPh2JbbeVFKHfbBSDb9H4q9DXFC7AHSb3jqdwS3siP'


# stability_api = client.StabilityInference(
#     key=os.environ['STABILITY_KEY'], # API Key reference.
#     verbose=True, # Print debug messages.
#     engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
#     # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
# )

# answers2 = stability_api.generate(style_preset="photographic",
#                                   adapter_strength=1.0,
#                                   prompt="river flowing", 
#                                   steps=100, cfg_scale=35.0, width=1152, height=896, sampler=generation.SAMPLER_K_DPMPP_2M)

# for resp in answers2:
#     for artifact in resp.artifacts:
#         if artifact.finish_reason == generation.FILTER:
#             warnings.warn("Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.")
#         if artifact.type == generation.ARTIFACT_IMAGE:
#             global background
#             background = Image.open(io.BytesIO(artifact.binary))
#             background.save(str(artifact.seed) + ".png")

# background = cv2.imread('3625454299.png')

# # Load the background and foreground images
# # background = cv2.imread('background_image.jpg')
# # foreground = cv2.imread('foreground_image.png', cv2.IMREAD_UNCHANGED)  # Load with alpha channel if present

# width = 640
# height = 480

# # Resize the foreground image to fit within a region of the background image
# foreground_resized = cv2.resize(foreground, (width, height))  # Specify width and height

# # Get the dimensions of the foreground image
# f_height, f_width, f_channels = foreground.shape

# # Define the region where you want to place the foreground image
# top_left_x = 100  # Adjust these coordinates as needed
# top_left_y = 100

# # Create a mask for the foreground image if it has an alpha channel
# if f_channels == 4:
#     alpha = foreground[:, :, 3] / 255.0
#     alpha = cv2.merge((alpha, alpha, alpha))

#     # Remove the alpha channel from the foreground
#     foreground_resized = foreground[:, :, :3]

#     # Calculate the weighted sum of the foreground and background images
#     for c in range(0, 3):
#         background[top_left_y:top_left_y + f_height, top_left_x:top_left_x + f_width, c] = \
#             alpha[:, :, c] * foreground[:, :, c] + \
#             (1 - alpha[:, :, c]) * background[top_left_y:top_left_y + f_height, top_left_x:top_left_x + f_width, c]
# else:
#     # If the foreground image doesn't have an alpha channel, directly blend the images
#     background[top_left_y:top_left_y + f_height, top_left_x:top_left_x + f_width] = foreground

# # Display or save the final image
# cv2.imshow('Result', background)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# To save the result
# cv2.imwrite('result_image.jpg', background)