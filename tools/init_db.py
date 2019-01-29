from apps.users.models import User
from peewee import MySQLDatabase
from MxForm.settings import database

database = MySQLDatabase(
    'tornado_luntan', host="127.0.0.1", port=3306, user="root", password="111111"
)

def init():
    #生成表
    database.create_tables([User])

if __name__ == "__main__":
    init()