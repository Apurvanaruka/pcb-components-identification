import streamlit as st
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
from gemini import get_response

st.set_page_config(layout="wide")


@st.cache_data
def load_model(path):
    return YOLO(path)

def upload_file():
    img = None
    img_path = None
    # contents = os.listdir('../dataset/test/images')
    # if st.sidebar.button('Choose random image from test dir'):
    #     img_path ='../dataset/test/images/' + np.random.choice(contents)    
    if not img:
        img = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if img_path:
        return img_path
    return img

model = load_model("../models/runs/detect/train5/weights/best.pt")
# model = load_model("../models/yolo_v1.1.pt")
names= ['Capecitor 1', 'Capecitor 2', 'Capecitor 3', 'Capecitor 4', 'MOSFET', 'Metal Oxide Varistors', 'Resistor', 'Resistor', 'Transformer']
component_list = {'Capecitor':[], 'MOSFET':[], 'Metal Oxide Varistors':[], 'Resistor':[], 'Transformer':[]}
image_array = None

def show_img_info(box):
    # Get the bounding box coordinates
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cropped_image = Image.fromarray(image_array[y1:y2, x1:x2])
    confidence = box.conf.item()
    return cropped_image,  f"Confidence: {confidence:.2f}"



st.title("PCB Component Detection.")

uploaded_file = upload_file()

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    with st.spinner('Finding coponents...'):
        results = model(image)
    image_array = results[0].orig_img

    col1, col2 = st.columns(2)
    with col1:
        st.write('Input PCB Image')
        st.image(image, caption="Uploaded Image", use_column_width=True)

    with col2:
        st.write('Output PCB Image')
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(np.array(results[0].plot()))
        plt.axis('off')
        st.pyplot(fig)
        
    with st.spinner('Response Generating...'):
        response = get_response(image)
        st.markdown(response)
        
    for i, box in enumerate(results[0].boxes):
        label = int(box.cls.item())
        if label in [0,1,2,3]:
            component_list['Capecitor'].append(box)
        elif label in [4]:
            component_list['MOSFET'].append(box)
        elif label in [5]:
            component_list['Metal Oxide Varistors'].append(box)
        elif label in [6,7]:
            component_list['Resistor'].append(box)
        elif label in [8]:
            component_list['Transformer'].append(box)

    capecitor,mosfet, metal_oxide_varistors, resistor, transformer = st.columns(5)
    with capecitor:
        st.write(f'Capecitor - {len(component_list['Capecitor'])}')
        for box in component_list['Capecitor']:
            img, confidence = show_img_info(box)
            st.image(img,width=200,caption=confidence)
    with mosfet:
        st.write(f'MOSFET - {len(component_list['MOSFET'])}')
        for box in component_list['MOSFET']:
            img, confidence = show_img_info(box)
            st.image(img,width=200,caption=confidence)
    with metal_oxide_varistors:
        st.write(f'Metal Oxide Varistors - {len(component_list['Metal Oxide Varistors'])}')
        for box in component_list['Metal Oxide Varistors']:
            img, confidence = show_img_info(box)
            st.image(img,width=200,caption=confidence)
    with resistor:
        st.write(f'Resistor - {len(component_list['Resistor'])}')
        for box in component_list['Resistor']:
            img, confidence = show_img_info(box)
            st.image(img,width=200,caption=confidence)
    with transformer:
        st.write(f'Transformer - {len(component_list['Transformer'])}')
        for box in component_list['Transformer']:
            img, confidence = show_img_info(box)
            st.image(img,width=200,caption=confidence)

else:
    path = '../models/runs/detect/train5/'
    images = os.listdir(path)
    for img in images:
        if img[-4:] == '.jpg' or img[-4:] == '.png':
            st.write(f'### {img[:-4]}')
            st.image(path+img, )