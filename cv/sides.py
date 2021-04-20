from lines import main
from tesseract import matchTemplate
import numpy as np
import cv2

img, dist, count = main('../img/test-3.png')

grid = np.zeros((count, count))
width, height, shape = img.shape
def getBox(x, y, pad):
    x1 = max(x*dist-pad, 0)
    x2 = min((x+1)*dist+pad, width)
    y1 = max(y*dist-pad, 0)
    y2 = min((y+1)*dist+pad, height)
    copy = np.copy(img[x1:x2, y1:y2])
    return copy

def getSides(x, y):
    crop = matchTemplate(getBox(x, y, 15))
    w, h, shape = crop.shape
    sides = {
        "top": crop[:round(w/2),:],
        "bottom": crop[round(w/2):,:],
        "right": crop[:,:round(w/2)],
        "left": crop[:,round(w/2):],
    }
    print("top:", preprocess(crop, sides, w, "h", "top", (0, 0)))
    print("bottom:", preprocess(crop, sides, w, "h", "bottom", (0, round(w/2))))
    print("left:", preprocess(crop, sides, w, "v", "right", (0, 0)))
    print("right:", preprocess(crop, sides, w, "v", "left", (round(w/2), 0)))
    cv2.imshow("output", crop)
    cv2.waitKey()

def preprocess(crop, sides, w, key, side, offset):
    gray = cv2.cvtColor(sides[side], cv2.COLOR_BGR2GRAY)
    pw, ph = gray.shape
    gray = cv2.resize(gray, (ph * 3, pw * 3))
    kernel = np.ones((13, 13), np.uint8)
    erode = cv2.erode(~gray, kernel)
    erode = cv2.resize(erode, (ph, pw))
    edges = cv2.Canny(erode, 50, 150)
    empty = np.zeros((dist, dist), np.uint8)
##    edges = empty + edges
##    cv2.imshow("output", edges)
##    cv2.waitKey()
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 15, None, round(w/3), 10)
    if lines is None:
        return False
##    x, y = offset
##    for line in lines:    
##        for x1,y1,x2,y2 in line:
##            cv2.line(crop,(x1+x,y1+y),(x2+x,y2+y),(255,255,255),2)
    return isThick(crop, key, lines, offset)

def isThick(crop, key, lines, offset):
    for line in lines:    
        for x1,y1,x2,y2 in line:
            x, y = offset
            if(x2-x1 == 0):
                if(key == "v"):
                    cv2.line(crop,(x1+x,y1+y),(x2+x,y2+y),(0,0,255),2)
                    return True
            elif((y2-y1)/(x2-x1) == 0):
                if(key == "h"):
                    cv2.line(crop,(x1+x,y1+y),(x2+x,y2+y),(0,0,255),2)
                    return True
        return False

for i in range(0, count):
    for j in range(0, count):
        print("")
        print(i, j)
        getSides(i, j)
