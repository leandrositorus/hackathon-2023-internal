import cv2
import numpy as np


background = cv2.imread('surface_of_a_smooth_ceramic_table.jpeg')  # Replace with your background image
product = cv2.imread('ath-earbuds-r.jpeg', -1) 

# Resize product image to fit within the background
product_resized = cv2.resize(product, (150, 150))  # Adjust size as needed

# Coordinates to place the product on the background
x_offset = 50  # Replace with desired x-coordinate
y_offset = 100  # Replace with desired y-coordinate

# Extract alpha channel from product image (if exists)
if product_resized.shape[2] == 4:
    alpha_product = product_resized[:, :, 3] / 255.0  # Normalize alpha channel
    alpha_background = 1.0 - alpha_product

    # Remove alpha channel from product image
    product_resized = product_resized[:, :, :3]

    # Region of Interest (ROI) for placing product on background
    roi = background[y_offset:y_offset+product_resized.shape[0], x_offset:x_offset+product_resized.shape[1]]

    # Blend the product and background using alpha channels
    for c in range(0, 3):
        roi[:, :, c] = (alpha_product * product_resized[:, :, c] +
                        alpha_background * roi[:, :, c])

else:
    # Overlay product on background without alpha channel
    background[y_offset:y_offset + product_resized.shape[0], x_offset:x_offset + product_resized.shape[1]] = product_resized

# Display or save the composite image
cv2.imshow('Composite Image', background)
cv2.waitKey(0)
cv2.destroyAllWindows()