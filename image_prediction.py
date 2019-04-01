from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tqdm import tqdm



def load_model(model_name):
    # load json and create model
    json_file = open(model_name + '.json', 'r')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    # load weights into new model
    model.load_weights(model_name + '.h5')
    print("Loaded model from disk")

    return model


def compile_model(model):
    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])


def predict(image_path):
    test_image = []
    img = image.load_img(image_path, target_size=(width, height, 3), grayscale=False)
    img = image.img_to_array(img)
    img = img / 255
    test_image.append(img)
    test = np.array(test_image)

    prediction = m_model.predict_classes(test)

    return prediction


def init():
    compile_model(m_model)


width, height = 48, 48
m_model = load_model("model")
