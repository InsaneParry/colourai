#these are the libraries that we have used in the program
import cv2
import pandas as pd
import argparse
from numpy.distutils.fcompiler import none

#here we have created an argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
image_path = args['image']

photo = cv2.imread(image_path)

index = ["colour", "colour_name", "hexadecimal", "r", "g", "b"]
csv = pd.read_csv("dataset.csv", names=index, header=none)

cv2.namedWindow("image")
cv2.setMouseCallBack("image", draw)


def draw(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = photo[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

#this function calculates the distance for gathering the colour name from the dataset used
def getColorName(R, G, B):
    minimum = 10000
    for counter in range(len(csv)):
        d = abs(R - int(csv.loc[counter, "R"])) + abs(G - int(csv.loc[counter, "G"])) + abs(
            B - int(csv.loc[counter, "B"]))
        if d <= minimum:
            minimum = d
            colour_name = csv.loc[counter, "color_name"]
    return colour_name


while 1:
    cv2.imageshow("image", photo)
    if (clicked):
        cv2.rectangle(photo, (20, 20), (750, 60), (b, g, r), -1)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(photo, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        if r + g + b >= 600:
            cv2.putText(photo, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            clicked = False

        if cv2.waitKey(20) & 0xFF == 27:
            break

cv2.destroyAllWindows()

