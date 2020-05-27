import io
import base64
from PIL import Image

def get_byte_image(image_path):
    img = Image.open(image_path, mode='r')
    img_byte_arr = io.BytesIO()
    encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    print(encoded_img)
    return encoded_img