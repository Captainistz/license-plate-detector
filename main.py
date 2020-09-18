import os
import cv2
import time
import urllib
import imutils
import _database
import pytesseract
import numpy as np
import mysql.connector
from dotenv import load_dotenv

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#vid = cv2.VideoCapture(0)

load_dotenv()

while 1:
    #ret, img = vid.read()
    url = os.getenv('CAMERA_URL')

    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)

    og_im = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(gray, 100, 200)
    
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.008 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if not screenCnt is None:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1,)
        new_image = cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        
        text = pytesseract.image_to_string(Cropped, 'tha')
        _database.check_plate(text, og_im)
        #print(text)
        text = pytesseract.image_to_string(img, 'tha')
        _database.check_plate(text, og_im)
        #   print(text)
        Cropped = cv2.resize(Cropped, (400, 200))
        cv2.imshow('Cropped', Cropped)

    cv2.imshow('Edge', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#vid.release()
cv2.destroyAllWindows()
