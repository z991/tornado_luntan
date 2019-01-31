import os

import peewee_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = {
    "static_path": "/Users/zhuxuanyu/python_xuexi/tornado_luntan/media",
    "static_url_prefix": "/media/",
    "template_path": "templates",
    "secret_key":"ZGGA#Mp4yL4w5CDu",
    "jwt_expire":7*24*3600,
    "MEDIA_ROOT": os.path.join(BASE_DIR, "media"),
    "SITE_URL": "http://127.0.0.1:8000",
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "111111",
        "name": "tornado_luntan",
        "port": 3306
    },
    "redis":{
        "host":"127.0.0.1"
    }
}

database = peewee_async.MySQLDatabase(
    'tornado_luntan', host="127.0.0.1", port=3306, user="root", password="111111"
)