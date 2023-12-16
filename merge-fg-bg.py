# merge this code later on the final product
# https://stackoverflow.com/questions/72904392/when-i-put-foreground-image-on-the-background-why-this-distortion-happens
import cv2
import numpy as np

foreground = cv2.imread("iphone_15.jpeg")
background = cv2.imread('3625454299.png')

gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)

_, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# figure out to now crop the background, but resize the foreground (product image) to fit into the background
crop_background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]), interpolation = cv2.INTER_NEAREST)
_, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
mask = mask.astype(np.float64) / 255

result = (foreground * mask + crop_background * (1 - mask))
result = result.clip(0, 255).astype(np.uint8)

cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()