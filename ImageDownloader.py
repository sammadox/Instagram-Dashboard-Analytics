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
        st.success(f"Image saved as {file_name}")
    except Exception as e:
        st.error(f"Error saving image: {e}")

image_data = download_image('https://scontent-sjc3-1.cdninstagram.com/v/t51.2885-19/454721520_465533593112167_5024545900891783443_n.jpg?stp=dst-jpg_s150x150&_nc_ht=scontent-sjc3-1.cdninstagram.com&_nc_cat=107&_nc_ohc=BJVfbHqQsZYQ7kNvgFleFN1&edm=APs17CUBAAAA&ccb=7-5&oh=00_AYCKpYdXZhuOeCyzMe-hpRMgRjV3EmrlNI5NJstWws3XJQ&oe=66DF5C63&_nc_sid=10d13b')

if image_data:
    save_image_locally(image_data, "downloaded_image.jpg")
