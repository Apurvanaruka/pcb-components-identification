from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

# Load the pre-trained YOLOv10n model
model = YOLO("fine-tuned-yolov10n.pt")

import os
from PIL import Image

def load_images_from_folder(folder_path):
    images = []
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is an image based on its extension
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            img_path = os.path.join(folder_path, filename)
            # Open the image using PIL and append it to the list
            img = Image.open(img_path)
            images.append(img)
    return images

# Specify the path to your folder containing images
folder_path = "dataset/drive-download-20240817T043918Z-001"

# Load all images into a list
images_list = load_images_from_folder(folder_path)

# Print the number of images loaded
print(f"Total images loaded: {len(images_list)}")

for image in images_list:
    results = model(image)
    image_array = results[0].orig_img
    for i, box in enumerate(results[0].boxes):
        # Get the bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Crop the component from the original image
        cropped_image = Image.fromarray(image_array[y1:y2, x1:x2])

        # Save the cropped image
        component_label = box.cls.item()  # Get the class label (e.g., resistor, capacitor)
        cropped_image_path = f"dataset/cropped_components/component_{i}_{component_label}.jpg"
        cropped_image.save(cropped_image_path)