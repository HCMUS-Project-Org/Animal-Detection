import os
import requests
import urllib
# import wget
image_url = 'https://drive.google.com/uc?export=download&id=1p_m4-SqCVQ8TGxdri95hmp0M-lLSfmjq'
modelWeights = '../config/yolov3.weights'


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response =requests.get(url, allow_redirects=True)
        # write to file
        file.write(response.content)


os.system('git config --global --unset http.proxy')

isExist = (os.path.isfile(modelWeights))
if isExist == False:
    
    # image_url = 'https://www.python.org/static/img/python-logo@2x.png'
    # image_url = 'https://vinasupport.com/assets/img/vinasupport_logo.png'
    
    # save path
    # image_save_path = '/' + os.path.basename(image_url)
    # # Download file from url
    # urllib.request.urlretrieve(image, image_save_path)
    # print(image_save_path)
    download(image_url, 'hi.weights')
    print('done')

with open('hi.weights', 'rb') as f:
    file = f.read().decode("utf-8") 
    print(type(file))