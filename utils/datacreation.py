import os
import shutil

def organize_files(image_dir, label_dir, train_dir, label_output_dir):
    # Create train and label output directories if they don't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(label_output_dir, exist_ok=True)

    # Get list of all image and label files
    image_files = os.listdir(image_dir)
    label_files = os.listdir(label_dir)

    # Iterate through image files and check for corresponding label files
    for image_file in image_files:
        # Get the base file name without extension
        base_name = os.path.splitext(image_file)[0]
        
        # Construct the expected label file name
        label_file = f"{base_name}.txt"
        
        # Check if the label file exists in the label directory
        if label_file in label_files:
            # Move image file to the train directory
            shutil.move(os.path.join(image_dir, image_file), os.path.join(train_dir, image_file))
            
            # Move label file to the label output directory
            shutil.move(os.path.join(label_dir, label_file), os.path.join(label_output_dir, label_file))

    print("Files organized successfully!")

# Usage
image_directory = "cropped_components"
label_directory = "labels"
train_directory = "Data/train"
label_output_directory = "Data/label"

organize_files(image_directory, label_directory, train_directory, label_output_directory)
