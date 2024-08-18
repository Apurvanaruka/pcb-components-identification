import xml.etree.ElementTree as ET
import os

# Define the class labels as per your dataset
classes = ["capicitor 1", "ic", "register", "transformer"]  # Modify this list as per your dataset

def convert_xml_to_yolo(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Iterate through each image in the XML file
    for image in root.findall('image'):
        file_name = image.get('name')
        image_width = int(image.get('width'))
        image_height = int(image.get('height'))
        
        output_file = os.path.join(output_dir, os.path.splitext(file_name)[0] + '.txt')
        
        with open(output_file, 'w') as f:
            for box in image.findall('box'):
                label = box.get('label')
                print(label)
                if label not in classes:
                    continue
                
                class_id = classes.index(label)
                
                xtl = float(box.get('xtl'))
                ytl = float(box.get('ytl'))
                xbr = float(box.get('xbr'))
                ybr = float(box.get('ybr'))
                
                # Calculate YOLO format values
                x_center = (xtl + xbr) / 2.0 / image_width
                y_center = (ytl + ybr) / 2.0 / image_height
                width = (xbr - xtl) / image_width
                height = (ybr - ytl) / image_height
                print(f"{class_id} {x_center} {y_center} {width} {height}\n")
                
                # Write the YOLO format annotation
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

def convert_all_annotations(xml_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith('.xml'):
            convert_xml_to_yolo(os.path.join(xml_dir, xml_file), output_dir)

# Paths
xml_dir = './'  # Directory containing your XML files
output_dir = 'labels'  # Directory to save YOLO format .txt files

convert_all_annotations(xml_dir, output_dir)
