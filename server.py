from tornado import web
import tornado
from peewee_async import Manager

from MxForm.urls import urlpattern
from MxForm.settings import settings, database



if __name__ == '__main__':
    # 集成json到wtforms中
    import wtforms_json
    wtforms_json.init()

    app = web.Application(urlpattern, debug=True, **settings)
    app.listen(8000)

    objects = Manager(database)
    database.set_allow_sync(False)
    app.objects = objects

    tornado.ioloop.IOLoop.current().start()