from PIL import Image, ImageFilter
from os import listdir
from os.path import isfile, join
from random import shuffle
from enum import Enum
import shutil
import os


class Data(Enum):
    LABEL = 0
    NAME = 1
    FOLDER = 2
    IMAGES = 3

def image_center(image):
    """
    Calculate center coordinates of an image.

    :param image: picture
    :returns: returns a tuple with x and y coordinate of the image center
    """
    width, height = image.size
    return (width/2, height/2)


def expand_image_canvas(image):
    """
    Expands the image canvas so that the image will be square. Shorter
    side of the image will be expanded to match the longer side.

    :param image: picture
    :returns: returns an square image
    """
    width, height = image.size
    image_size = max(width, height)
    expanded_image = Image.new(image.mode, (image_size, image_size))
    expanded_image.paste(image, (0, 0, width, height))
    return expanded_image


def standardize_image(image_path, output_path, new_size):
    """
    Resizes image to the given size. Image is first converted to
    a square image and then resized

    :param image_path: picture to be resized
    :param output_path: location where the resized picture is to be saved
    :param new_size: x and y lenghts of the resized image
    :returns: nothing
    """
    im = Image.open(image_path)
    square_im = crop_image(im)#expand_image_canvas(im)
    square_im.thumbnail(new_size, Image.ANTIALIAS)
    square_im.save(output_path, "JPEG")


def rotate_image_90(image_path, output_path, new_size):
    """
    Rotates the image 90 degrees and resizes image to the given size. Image is first converted to
    a square image and rotated and resized

    :param image_path: picture to be resized
    :param output_path: location where the resized picture is to be saved
    :param new_size: x and y lenghts of the resized image
    :returns: nothing
    """
    im = Image.open(image_path)
    square_im = crop_image(im)
    square_im = square_im.rotate(90)
    square_im.thumbnail(new_size, Image.ANTIALIAS)
    square_im.save(output_path, "JPEG")


def rotate_image(image_path, output_path, new_size, degrees):
    """
    Rotates the image 45 degrees and resizes image to the given size. Image is first rotated
    and then converted to a square image and resized

    :param image_path: picture to be resized
    :param output_path: location where the resized picture is to be saved
    :param new_size: x and y lenghts of the resized image
    :returns: nothing
    """
    im = Image.open(image_path)
    im = im.rotate(degrees)
    square_im = crop_image(im)
    square_im.thumbnail(new_size, Image.ANTIALIAS)
    square_im.save(output_path, "JPEG")


def crop_image(image):
    """
    Crops the image to be square using the shortest side as the size.

    :param image: picture to be cropped
    :returns: cropped image
    """
    box = []
    width, height = image.size
    box_size = min(width, height)
    offset = box_size/2
    center = image_center(image)
    image_center_x = center[0]
    image_center_y = center[1]
    #left and upper coordinates
    box.append(image_center_x - offset)
    box.append(image_center_y - offset)
    #right and lower coordinates
    box.append(image_center_x + offset)
    box.append(image_center_y + offset)
    return image.crop(box)

#get raw images for different image classes
hotdogs = [f for f in listdir("hotdog_pics") if isfile(join("hotdog_pics", f))]
non_hotdogs = [f for f in listdir("other_pics") if isfile(join("other_pics", f))]

#create tuples for the image classes (label, name, folder, raw images)
hotdog = (0, "hotdog", "hotdog_pics", hotdogs)
non_hotdog = (1, "non_hotdog", "other_pics", non_hotdogs)

image_data = [hotdog, non_hotdog]

#loop through all images and standardize them to size 100 x 100 pixels
#standardized images are saved in standard_pic folder
size = 224, 224
for image_class in image_data:
    i = 0
    for image in image_class[Data.IMAGES.value]:
        outfile = "standard_pics/" + image_class[Data.NAME.value] + "_" + str(i) + ".jpg"
        rotated_90_outfile = "standard_pics/" + image_class[Data.NAME.value] + "_rot90_" + str(i) + ".jpg"
        rotated_45_outfile = "standard_pics/" + image_class[Data.NAME.value] + "_rot45_" + str(i) + ".jpg"
        image_path = image_class[Data.FOLDER.value] + "/" + image
        i += 1
        try:
            standardize_image(image_path, outfile, size)
            rotate_image_90(image_path, rotated_90_outfile, size)
            rotate_image(image_path, rotated_45_outfile, size, 45)
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


