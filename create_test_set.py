from PIL import Image, ImageFilter
from os import listdir
from os.path import isfile, join
from random import shuffle
from enum import Enum
import shutil
import os


#create csv file for test images
file = open("Korvbilder/images.csv", "w")
file.write("id,label\n")
images = [f for f in listdir("Korvbilder") if isfile(join("Korvbilder", f))]

for image_name in images:
    #update csv file
    if image_name.find(".csv") == -1:
        file.write(image_name + "\n")
#close open file
file.close()


