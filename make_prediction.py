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

def print_thruth_table(prediction, test_data):
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    for i in range(test_files.shape[0]):
        if test_files.loc[i, 'id'].find("non_hotdog") == -1:
            if prediction[i] == 1:
                true_positive += 1
            else:
                false_positive += 1
        else:
            if prediction[i] == 0:
                true_negative += 1
            else:
                false_negative += 1

    print(str(true_positive) + " | " + str(false_positive) + "\n----\n"
          + str(false_negative) + " | " + str(true_negative))

width, height = 48, 48
csv_folder = "test_set/"
image_folder = "test_set/"
#csv_folder = "Korvbilder/"
#image_folder = "Korvbilder/"

#load json and create model
json_file = open('model.json', 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
#load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")

model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

test_files = pd.read_csv(csv_folder + 'images.csv')

test_image = []
for i in tqdm(range(test_files.shape[0])):
    print(test_files.loc[i, 'id'])
    img = image.load_img(image_folder + test_files.loc[i, 'id'], target_size=(width, height, 3), grayscale=False)
    img = image.img_to_array(img)
    img = img/255
    test_image.append(img)
test = np.array(test_image)

prediction = model.predict_classes(test)

print(prediction)

print_thruth_table(prediction, test_files)