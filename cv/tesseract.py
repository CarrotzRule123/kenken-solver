import cv2
import numpy as np

sprites = cv2.imread("../assets/spritesheet.png", 0)
digits = {
    "0":sprites[:,0:17],
    "1":sprites[:,17:31],
    "2":sprites[:,31:50],
    "3":sprites[:,50:68],
    "4":sprites[:,68:89],
    "5":sprites[:,89:109],
    "6":sprites[:,109:127],
    "7":sprites[:,127:146],
    "8":sprites[:,146:164],
    "9":sprites[:,164:182],
    "+":sprites[:,182:202],
    "-":sprites[:,202:230],
    "x":sprites[:,230:248],
    "/":sprites[:,248:268]
}

def matchTemplate(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    threshold = 0.9
    result = []
    for digit in digits:
        template = digits[digit]
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            pos = (pt[0]+w/2, pt[1]+h/2)
            if(verifyBox(result, pos, w)):
                result.append({
                    "key": digit,
                    "pos": pos
                })
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
    print(arrange(result))
    return img

def verifyBox(result, pos, w):
    for rect in result:
        dist = np.hypot(rect["pos"][0] - pos[0],rect["pos"][1] - pos[1])
        if(dist < w/2):
            return False
    return True

def sort(e):
    return e["pos"][0]

def arrange(result):
    result.sort(key=sort)
    txt = ""
    for rect in result:
        txt += rect["key"]
    return txt
    
