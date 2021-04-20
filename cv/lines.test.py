import cv2
import numpy as np
import math

img = cv2.imread('../img/test-5.png')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
kernel = np.ones((5, 5), np.uint8)
blur_gray = cv2.erode(~gray, kernel)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 0  # minimum number of pixels making up a line
max_line_gap = 5  # maximum gap in pixels between connectable line segments
line_image = np.copy(img)  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)
height, width, channels = line_image.shape

horizontal_lines = []
vertical_lines = []
border = {"top":[], "right":[], "left":[], "bottom":[]}
for side in border:
    border[side] = [width / 2, height / 2,  width / 2, height / 2]

def verifyLines(line, lines, key):
    x1,y1,x2,y2 = line[0]
    for other in lines:
        px1,py1,px2,py2 = other[0]
        if(key == "v"):
            if(x1-px1 < 50 and x1-px1 > -50):
                return False
        elif(key == "h"):
            if(y1-py1 < 50 and y1-py1 > -50):
                return False
    return True

for line in lines:
    x1,y1,x2,y2 = line[0]
    if(x2-x1 == 0):
        if(y1-y2 > height/5):
            if(x1 <  border["left"][0]):
                border["left"] = line[0]
            if(x1 >  border["right"][0]):
                border["right"] = line[0]
            if(verifyLines(line, vertical_lines, "v")):
                vertical_lines.append(line)
                cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),5)
    elif((y2-y1)/(x2-x1) == 0):
        if(x2-x1 < width*0.9 and x2-x1 > width/5):
            if(y1 <  border["top"][1]):
                border["top"] = line[0]
            if(y1 >  border["bottom"][1]):
                border["bottom"] = line[0]
            if(verifyLines(line, horizontal_lines, "h")):
                horizontal_lines.append(line)
                cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),5)

for side in border:
    x1,y1,x2,y2 = border[side]
    cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

closestX = 1000
closestY = 1000
def sortX(e):
    return e[0][0]
def sortY(e):
    return e[0][-1]
vertical_lines.sort(key=sortX)
horizontal_lines.sort(key=sortY)
for x in range(1, len(vertical_lines)):
    dist = vertical_lines[x][0][0]-vertical_lines[x-1][0][0]
    if(dist < closestX):
        closestX = dist
for x in range(1, len(horizontal_lines)):
    dist = horizontal_lines[x][0][1]-horizontal_lines[x-1][0][1]
    if(dist < closestY):
        closestY = dist

boxwidth = border["right"][0] - border["left"][0]
boxheight = border["bottom"][1] - border["top"][1]
countX = math.floor(boxwidth / closestX)
countY = math.floor(boxheight / closestY)
count = 0
print("Closest X dist:", closestX, "Closest Y dist:", closestY)
print("Box width:", boxwidth, "Box Height:", boxheight)
print("X count:", countX, "Y count:", countY)
if(countY > countX and countY < 10):
    count = countY
else:
    count = countX
print("Count:", count)
dist = round(boxwidth / count)
img_crop = img[border["top"][1]:border["top"][1]+boxwidth, border["left"][0]:border["right"][0]]

grid = np.zeros((count, count))
def getBox(x, y):
    return img_crop[x*dist:(x+1)*dist, y*dist:(y+1)*dist]
def getBoxFree(x, y):
    return img_crop[x*dist-20:(x+1)*dist+20, y*dist-20:(y+1)*dist+20]

img_box = getBoxFree(4, 2)
        
imS = cv2.resize(line_image, (round(boxwidth / 2), round(boxwidth / 2)))
cv2.imshow("output", imS)
