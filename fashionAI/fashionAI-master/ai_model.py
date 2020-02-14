# Dependencies
import matplotlib.pyplot as plt
# %matplotlib inline

import os
import numpy as np
import tensorflow as tf
import urllib

from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import (
    VGG19, 
    preprocess_input, 
    decode_predictions
)

pred = []
acc = []
pred_accuracy = dict()
def predict(image_path):
    """Use VGG19 to label image"""
    pred = [] 
    acc = [] 
    model = VGG19(include_top=True, weights='imagenet')
    img = image.load_img(urllib.request.urlopen(image_path), target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    predictions = model.predict(x)
    plt.imshow(img)
    
    for i in range(3):
        pred.append(decode_predictions(predictions, top=3)[0][i][1])
        acc.append(decode_predictions(predictions, top=3)[0][i][2])

    pred_accuracy = {'Predicted':  pred,
                'Accuracy': acc}
                
    return pred_accuracy


