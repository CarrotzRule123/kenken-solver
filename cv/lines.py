import cv2
import numpy as np
import math

def main(path):
    img = cv2.imread(path)
    height, width, line_image, lines = preprocess(img)
    horizontal_lines, vertical_lines, border = presetBorders(width, height)
    defineLines(lines, width, height, border, vertical_lines, horizontal_lines)
    dist, count = getClosestDistance(vertical_lines, horizontal_lines, border)

    img_crop = img[border["top"][1]:border["top"][1]+border["right"][0]-border["left"][0],
                   border["left"][0]:border["right"][0]]
    print("Difficulty:", str(count)+"x"+str(count))
    return img_crop, dist, count

def preprocess(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur_gray = cv2.GaussianBlur(gray,(5, 5),0)
    edges = cv2.Canny(blur_gray, 50, 150)
    line_image = np.copy(img)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, np.array([]), 50, 20)
    height, width, channels = line_image.shape
    return height, width, line_image, lines

def presetBorders(width, height):
    horizontal_lines = []
    vertical_lines = []
    border = {"top":[], "right":[], "left":[], "bottom":[]}
    for side in border:
        border[side] = [width / 2, height / 2,  width / 2, height / 2]
    return horizontal_lines, vertical_lines, border

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

def defineLines(lines, width, height, border, vertical_lines, horizontal_lines):
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
        elif((y2-y1)/(x2-x1) == 0):
            if(x2-x1 < width*0.9 and x2-x1 > width/5):
                if(y1 <  border["top"][1]):
                    border["top"] = line[0]
                if(y1 >  border["bottom"][1]):
                    border["bottom"] = line[0]
                if(verifyLines(line, horizontal_lines, "h")):
                    horizontal_lines.append(line)

def sortX(e):
    return e[0][0]

def sortY(e):
    return e[0][-1]

def getClosestDistance(vertical_lines, horizontal_lines, border):
    closestX = 1000
    closestY = 1000
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
    count = getCount(border, closestX, closestY)
    boxwidth = border["right"][0] - border["left"][0]
    dist = round(boxwidth / count)
    return dist, count

def getCount(border, closestX, closestY):
    boxwidth = border["right"][0] - border["left"][0]
    boxheight = border["bottom"][1] - border["top"][1]
    countX = math.floor(boxwidth / closestX)
    countY = math.floor(boxheight / closestY)
    count = 0
    if(countX > countY and countX < 10):
        count = countX
    elif(countY > countX and countY < 10):
        count = countY
    else:
        count = countX
    return count
