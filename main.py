import cv2
import imutils
import numpy as np
import pytesseract
import time
import mysql.connector
import _database
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

vid = cv2.VideoCapture(0)

while 1:
    ret, img = vid.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    gray = cv2.GaussianBlur(gray,(5,5),0)
    #gray = cv2.bilateralFilter(gray, 7, 15, 15) 
    
    edged = cv2.Canny(gray, 100, 200) 
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None
    
    for c in contours:
        
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    
        if len(approx) == 4:
            screenCnt = approx
            break
    
    if not screenCnt is None:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        
        text = pytesseract.image_to_string(Cropped, 'tha')
        _database.check_plate(text)
        
        Cropped = cv2.resize(Cropped,(400,200))
        cv2.imshow('Cropped',Cropped)

    cv2.imshow('Edge', img)
    
    time.sleep(0.2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()