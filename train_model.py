from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing import image
import keras as K
import tensorflow as tf
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from tqdm import tqdm

width, height = 48, 48
train = pd.read_csv('training_set/images.csv')

train_image = []

for i in tqdm(range(train.shape[0])):
    img = image.load_img('training_set/' + train.loc[i, 'id'], target_size=(width, height, 3), grayscale=False)
    img = image.img_to_array(img)
    img = img/255
    train_image.append(img)

X = np.array(train_image)
y = train['label'].values
y = to_categorical(y)

#Own model
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(width, height, 3), bias_initializer='zeros'))
model.add(Conv2D(64, (3, 3), activation='relu', bias_initializer='zeros'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax', kernel_initializer='random_uniform', bias_initializer='zeros'))

model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

#mobilenet model
# base_model = MobileNet(input_shape=(width, height, 3), alpha=1.0, depth_multiplier=1, dropout=1e-3, include_top=False,
#                        weights=None, input_tensor=None, pooling=None, classes=1000)
#
# CLASSES = 2
# x = base_model.output
# x = GlobalAveragePooling2D(name='avg_pool')(x)
# x = Dropout(0.4)(x)
# predictions = Dense(CLASSES, activation='softmax')(x)
# model_mobile = Model(inputs=base_model.input, outputs=predictions)
#
# for layer in base_model.layers:
#     layer.trainable = False
#
# model_mobile.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#
# model_mobile.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

#save model to disk
#save to keras model
K.models.save_model(model, "keras_model.h5")
# K.models.save_model(model_mobile, "keras_model_mobile.h5")

#serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
#serialize weights to HDF5
model.save_weights("model.h5")

print("Saved model to disk")