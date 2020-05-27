import os
import glob

import torch
from flask import Flask, request, send_file, make_response
from flask_cors import CORS
from PIL import Image, ImageOps
from torchvision import transforms

from app.segmentation import segment
from app.enc_image import get_byte_image
from app.lenet import LeNet5

app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER='.',
        SEND_FILE_MAX_AGE_DEFAULT = 0
)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    return response

try:
    os.makedirs(app.instance_path)
except OSError:
    pass


@app.route('/', methods=['POST'])
def root():
    os.system("rm -rf segmented_image/*")
    os.system("rm -rf res.jpg")
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg'))
    segment('input_image.jpg')
    model = LeNet5()
    model.load_state_dict(torch.load('./model', map_location=torch.device('cpu')))
    model.eval()
    string_ind = 1
    word_ind = 1
    char_ind = 1
    al = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    files = sorted(glob.glob('./segmented_image/*.jpg'))

    textResp = ''
    for file in files:
        print('file', file)
        img = Image.open(file)
        img = img.resize((28, 28), Image.ANTIALIAS)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img = img.rotate(90)
        img = img.convert('L')
        img = ImageOps.invert(img)

        to_tensor = transforms.ToTensor()
        t = (to_tensor(img))
        t = 255*t
        t = t.unsqueeze(0).float()
        pred = model.forward(t)

        textResp += al[pred.argmax(dim=1) -1]

   
    return {
        'recognizedText': textResp  
    }, 200

@app.route('/get_res', methods=['GET'])
def get_res():
    resp = make_response(send_file('../res.jpg'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    resp.headers['Cache-Control'] = 'public, max-age=0'
    return  resp