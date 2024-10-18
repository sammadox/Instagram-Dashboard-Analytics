from deepface import DeepFace
import cv2
import os
import re
import ast

from PIL import Image
from io import BytesIO
import requests
import streamlit as st

def download_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful
        return BytesIO(response.content)
    except Exception as e:
        st.error(f"Error downloading image: {e}")
        return None

def save_image_locally(image_data, file_name):
    try:
        image = Image.open(image_data)
        image.save(file_name, format='JPEG')  # Save as JPEG
       
    except Exception as e:
        st.error(f"Error saving image: {e}")


# Function to analyze age, gender, and race from an image
def analyze_attributes(img_path):
    try:
        # Analyze the image to estimate age, gender, and race
        analysis = DeepFace.analyze(img_path=img_path, actions=['age', 'gender'])

        # Extract the attributes from the analysis result
        if len(analysis) > 0:
            # analysis is a list where each element is a dictionary with 'age', 'gender', and 'race' keys
            first_result = analysis[0]
            age = first_result['age']
            gender = first_result['gender']
            return age, gender
        else:
            return None, "No faces detected", None
    except Exception as e:
        return None, str(e), None
    
#image_data = download_image('https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/454721520_465533593112167_5024545900891783443_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=BJVfbHqQsZYQ7kNvgFleFN1&edm=APs17CUBAAAA&ccb=7-5&oh=00_AYCKpYdXZhuOeCyzMe-hpRMgRjV3EmrlNI5NJstWws3XJQ&oe=66DF5C63&_nc_sid=10d13b')

def GetAgeandGender(ImageLink):
    image_data = download_image(ImageLink)
    if image_data:
        save_image_locally(image_data, "downloaded_image.jpg")

    response=analyze_attributes('downloaded_image.jpg')
    print(response[0])

    data=response[1]
    highest_percentage_key = max(data, key=data.get)

    print(highest_percentage_key)


    # Specify the file path
    file_path = "downloaded_image.jpg"

    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")
    return(response[0],highest_percentage_key)
#print(GetAgeandGender('https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/454721520_465533593112167_5024545900891783443_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=BJVfbHqQsZYQ7kNvgFleFN1&edm=APs17CUBAAAA&ccb=7-5&oh=00_AYCKpYdXZhuOeCyzMe-hpRMgRjV3EmrlNI5NJstWws3XJQ&oe=66DF5C63&_nc_sid=10d13b'))