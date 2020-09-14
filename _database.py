import mysql.connector as con
from datetime import date, datetime

today = date.today()
now = datetime.now()
today_date = today.strftime("%d/%m/%Y")
now_time = now.strftime("%H:%M:%S")

db = con.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "license-plate"
)

sql = db.cursor()

def check_plate(_plate):
    if len(_plate) < 2:
        return 0

    _plate = _plate.replace(" ","").replace("\n","").replace("'","")

    sql.execute("SELECT plate FROM license")
    plates = sql.fetchone()
    
    for x in plates:
        if _plate.find(str(x)) != -1:
            _name = "SELECT name FROM license WHERE plate LIKE '" + str(x) + "'"
            sql.execute(_name)
            res = sql.fetchone()
            print(res[0])
            break
