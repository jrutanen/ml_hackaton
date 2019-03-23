from PIL import Image, ImageFilter
from os import listdir
from os.path import isfile, join
from random import shuffle
import shutil
import os, sys


def image_center(image):
    width, height = image.size
    return (width/2, height/2)


def expand_image_canvas(original_image):
    width, height = original_image.size
    image_size = max(width, height)
    expanded_image = Image.new(original_image.mode, (image_size, image_size))
    expanded_image.paste(original_image, (0, 0, width, height))
    return expanded_image


def standardize_image(image_path, output_path):
    im = Image.open(image_path)
    square_im = crop_image(im)#expand_image_canvas(im)
    square_im.thumbnail(size, Image.ANTIALIAS)
    square_im.save(output_path, "JPEG")


def crop_image(image):
    box = []
    width, height = image.size
    box_size = min(width, height)
    offset = box_size/2
    center = image_center(image)
    image_center_x = center[0]
    image_center_y = center[1]
    # Left coordinate and Upper coordinate
    box.append(image_center_x - offset)
    box.append(image_center_y - offset)
    # Right coordinate and Lower coordinate
    box.append(image_center_x + offset)
    box.append(image_center_y + offset)
    return image.crop(box)


hotdogs = [f for f in listdir("hotdog_pics") if isfile(join("hotdog_pics", f))]
non_hotdogs = [f for f in listdir("other_pics") if isfile(join("other_pics", f))]

image_folders = [hotdogs, non_hotdogs]

i = 0
size = 100, 100
for f in hotdogs:
    outfile = "standard_pics/hotdog_" + str(i) + ".jpg"
    image_path = "hotdog_pics/" + f
    i += 1
    try:
        standardize_image(image_path, outfile)
    except IOError:
        print("error while modifying picture. Image deleted")
        os.remove(outfile)


i = 0
for f in non_hotdogs:
    outfile = "standard_pics/non_hotdog_" + str(i) + ".jpg"
    image_path = "other_pics/" + f
    i += 1
    try:
        standardize_image(image_path, outfile)
    except IOError:
        print("error while modifying picture. Image deleted")
        os.remove(outfile)

#get list of standardized images
images = [f for f in listdir("standard_pics") if isfile(join("standard_pics", f))]

#List is shuffled to randomize the order of filenames
shuffle(images)

#create training and test data lists
#training set ~80% and test set ~20%
cut_off_point = int(len(images) * 0.8)
training_images = images[:cut_off_point]
test_images = images[cut_off_point:]

#create csv file for training set
file = open("training_set/images.csv", "w")
file.write("id,label\n")
for image_name in training_images:
    label = ""
    image_path = "images/" + image_name
    if image_path.find("non_hotdog") == -1:
        label = "1"
    else:
        label = "0"
    #update csv file
    file.write(image_path + "," + label + "\n")
    #copy image file to training set images
    shutil.copyfile("standard_pics/" + image_name, "training_set/images/" + image_name)
#close open file
file.close()

#create csv file for test set
file = open("test_set/images.csv", "w")
file.write("id, label\n")
for image_name in test_images:
    image_path = "images/" + image_name
    #update csv file
    file.write(image_path + "\n")
    # copy image file to test set images
    shutil.copyfile("standard_pics/" + image_name, "test_set/images/" + image_name)
#close open file
file.close()

