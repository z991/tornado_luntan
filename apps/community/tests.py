import json
from datetime import datetime
import requests
import jwt

current_time = datetime.utcnow()
from MxForm.settings import settings

web_site_url = "http://127.0.0.1:8000"

jwt_data = jwt.encode({
    "name": "bobby",
    "id":1,
    "exp":current_time
}, settings["secret_key"]).decode("utf-8")


headers = {
    "tsessionid": jwt_data
}


def new_group():
    """
    新增小组
    :return:
    """
    files = {
        "front_image": open("/Users/zhuxuanyu/python_xuexi/tornado_luntan/media/SpiderQueen.jpg", "rb")
    }
    data = {
        "name": "学前教育交流角",
        "desc": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "notice": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "category": "教育同盟"
    }
    res = requests.post("{}/groups/".format(web_site_url), headers=headers, data=data, files=files)
    print('headers===', headers)
    print(res.status_code)
    print(json.loads(res.text))


def apply_group(group_id):
    """
    申请加入小组
    :param group_id:
    :return:
    """
    data = {
        "apply_reason": "nihaoa,develop",
    }
    res = requests.post("{}/groups/{}/members/".format(web_site_url, group_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))


def add_post(group_id):
    data = {
        "title": "tornado从入门到实战",
        "content": "从入门到放弃吧"
    }

    res = requests.post("{}/groups/{}/posts/".format(web_site_url, group_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == "__main__":
    # 新建小组
    # new_group()

    # 申请加入小组
    # apply_group(2)
    # 发帖
    add_post(2)