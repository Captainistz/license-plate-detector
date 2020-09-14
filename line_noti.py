from datetime import datetime
from io import BytesIO
from PIL import Image

url = 'https://notify-api.line.me/api/notify'
token = '4yOP5dsdx4aYTBxRAXEEtANyQSnMvH1qIlkrk9IxpVk'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def notifyFile(plate, name, lname):
    file = {'imageFile':open("./image/detected.jpg",'rb')}
    text = '\n' + plate + " | " + name + ' ' + lname + '\n' + "เวลา : " + datetime.now().strftime("%H:%M:%S")
    payload = {'message':text}
    return _lineNotify(payload,file)

def _lineNotify(payload, file=None):
    import requests
    url = 'https://notify-api.line.me/api/notify'
    token = '4yOP5dsdx4aYTBxRAXEEtANyQSnMvH1qIlkrk9IxpVk'	#EDIT
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)


if __name__ == "__main__":
    #noti_pic("./image/detected.jpg")
    notifyFile('กพ888','กัปตัน','พึ่งเป็นสุข')