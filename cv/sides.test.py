from lines import main
from tesseract import matchTemplate
import numpy as np
import cv2

img, dist, count = main('../img/test-2.png')

grid = np.zeros((count, count))
width, height, shape = img.shape
def getBox(x, y, pad):
    x1 = max(x*dist-pad, 0)
    x2 = min((x+1)*dist+pad, width)
    y1 = max(y*dist-pad, 0)
    y2 = min((y+1)*dist+pad, height)
    return img[x1:x2, y1:y2]

crop = matchTemplate(getBox(7, 5, 20))
w, h, shape = getBox(7, 5, 20).shape
sides = {
    "top": crop[:round(w/2),:],
    "bottom": crop[round(w/2):,:],
    "right": crop[:,:round(w/2)],
    "left": crop[:,round(w/2):],
}
top = crop[round(w/2):,:]

gray = cv2.cvtColor(top, cv2.COLOR_BGR2GRAY)
kernel = np.ones((3, 3), np.uint8)
erode = cv2.erode(~gray, kernel)
edges = cv2.Canny(erode, 50, 150)
cv2.imshow("", erode)
lines = cv2.HoughLinesP(edges, 1, np.pi / 2, 15, None, round(w/2), 10)
print(lines)

key="h"
def isThick():
    for line in lines:    
        for x1,y1,x2,y2 in line:
            if(x2-x1 == 0):
                if(key == "v"):
                    return True
            elif((y2-y1)/(x2-x1) == 0):
                if(key == "h"):
                    return True
        return False

print(isThick())
