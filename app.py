from flask import Flask, render_template, request, send_from_directory,Response
import cv2
import keras
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, BatchNormalization, Flatten
import numpy as np


model_right = load_model('vgg16_1.h5',compile=True)
model_left = load_model('vgg16_2.h5',compile=True)
labels_dict={0:'no_retinal',1:'mild',2:'moderate',3:'sever',4:'proliferate_dr'}
COUNT = 0
    
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1

@app.route('/')
def man():
    return render_template('index.html')


@app.route('/home', methods=['POST'])
def home():
    global COUNT
    img_right = request.files['image_right']
    img_left = request.files['image_left']

    img_right.save('static/{}.jpg'.format(COUNT))    
    img_arr_right = cv2.imread('static/{}.jpg'.format(COUNT))

    img_arr_right = cv2.resize(img_arr_right, (224,224))
    img_arr_right = img_arr_right / 255.0
    img_arr_right = img_arr_right.reshape(1, 224,224,3)
    result_right = model_right.predict(img_arr_right)
    print(result_right)
    label=np.argmax(result_right,axis=1)[0]
    prediction_right=labels_dict[label]
    print(prediction_right)


    img_left.save('static/{}.jpg'.format(COUNT))    
    img_arr_left = cv2.imread('static/{}.jpg'.format(COUNT))

    img_arr_left = cv2.resize(img_arr_left, (224,224))
    img_arr_left = img_arr_left / 255.0
    img_arr_left = img_arr_left.reshape(1, 224,224,3)
    result_left = model_left.predict(img_arr_left)
    print(result_left)
    label=np.argmax(result_left,axis=1)[0]
    prediction_left=labels_dict[label]
    print(prediction_left)

    if (prediction_left == 'no_retinal') and (prediction_right == 'no_retinal'):
        print('no_retinal')
        prediction = 'No Retinal diseases detected'
    else:
        print('have Retinal diseases kindly consult the doctor')
        prediction = 'Have Retinal diseases kindly consult the doctor'



    COUNT +=1;
    return render_template('prediction.html', data=prediction)


@app.route('/load_img')
def load_img():
    global COUNT
    return send_from_directory('static', "{}.jpg".format(COUNT-1))



if __name__ == '__main__':
    app.run(debug=True)
