import mysql.connector as con
from datetime import date, datetime
import line_noti
import time
import cv2
import numpy as np

today = date.today()
now = datetime.now()
today_date = today.strftime("%d/%m/%Y")
now_time = now.strftime("%H:%M:%S")

db = con.connect(
    host="localhost",
    user="root",
    passwd="",
    database="license-plate"
)

sql = db.cursor()


def check_plate(_plate, image):
    if len(_plate) < 2:
        return 0

    _plate = _plate.replace(" ", "").replace("\n", "").replace("'", "")

    sql.execute("SELECT plate FROM license")
    plates = sql.fetchall()

    for x in plates:
        if _plate.find(str(x[0])) != -1:
            _name = "SELECT * FROM license WHERE plate LIKE '" + \
                str(x[0]) + "'"
            sql.execute(_name)
            res = sql.fetchone()
            cv2.imwrite('./image/detected.jpg', image)
            line_noti.notifyFile(res[0], res[1], res[2])
            time.sleep(2)
            break
