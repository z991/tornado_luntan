import json
from datetime import datetime
import requests
import jwt

current_time = datetime.utcnow()
from MxForm.settings import settings

web_site_url = "http://127.0.0.1:8000"

data = jwt.encode({
    "name": "bobby",
    "id":1,
    "exp":current_time
}, settings["secret_key"]).decode("utf-8")

headers = {
    "tsessionid": data
}

def new_group():
    files = {
        "front_image": open("/Users/zhuxuanyu/python_xuexi/tornado_luntan/media/SpiderQueen.jpg", "rb")
    }
    data = {
        "name": "学前教育交流角",
        "desc": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "notice": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "category": "教育同盟"
    }
    print(files["front_image"], type(files["front_image"]))
    res = requests.post("{}/groups/".format(web_site_url), headers=headers, data=data, files=files)
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == "__main__":
    # 新建小组
    new_group()