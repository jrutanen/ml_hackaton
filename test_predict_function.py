import image_prediction as im
from os import listdir
from os.path import isfile, join

images = [f for f in listdir("Korvbilder") if isfile(join("Korvbilder", f))]

im.init()

predictions = []

for image in images:
    p = im.predict('Korvbilder/' + image)
    print(image + ": " + str(p))


