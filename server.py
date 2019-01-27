from tornado import web
import tornado


from MxForm.urls import urlpattern
from MxForm.settings import settings


if __name__ == '__main__':
    # 集成json到wtforms中
    import wtforms_json
    wtforms_json.init()

    app = web.Application(urlpattern, debug=True, **settings)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()