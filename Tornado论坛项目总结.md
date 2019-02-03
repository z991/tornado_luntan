# Tornado论坛项目总结

Tornado介绍

[* tornado](http://www.tornadoweb.org/)是一个Python Web框架和异步网络库，最初是在[FriendFeed上](https://en.wikipedia.org/wiki/FriendFeed)开发的。通过使用非阻塞网络I / O，Tornado可以扩展到数万个开放连接，使其成为[长轮询](http://en.wikipedia.org/wiki/Push_technology#Long_polling)， [WebSockets](http://en.wikipedia.org/wiki/WebSocket)和其他需要与每个用户建立长期连接的应用程序的理想选择 。*

*龙卷风大致可分为四个主要部分：*

- *Web框架（包括[`RequestHandler`](https://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler)子类，用于创建Web应用程序和各种支持类）。*
- *HTTP（[`HTTPServer`](https://www.tornadoweb.org/en/stable/httpserver.html#tornado.httpserver.HTTPServer)和 [`AsyncHTTPClient`](https://www.tornadoweb.org/en/stable/httpclient.html#tornado.httpclient.AsyncHTTPClient)）的客户端和服务器端实现。*
- *异步网络库包括类[`IOLoop`](https://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop) 和[`IOStream`](https://www.tornadoweb.org/en/stable/iostream.html#tornado.iostream.IOStream)，其充当用于HTTP组件的构建块，并且还可以用于实现其它协议。*
- *一个协程库（[`tornado.gen`](https://www.tornadoweb.org/en/stable/gen.html#module-tornado.gen)），它允许以比链接回调更直接的方式编写异步代码。这类似于Python 3.5（）中引入的本机协同程序功能。如果可用，建议使用本机协程代替模块。`async def`[`tornado.gen`](https://www.tornadoweb.org/en/stable/gen.html#module-tornado.gen)*

*Tornado Web框架和HTTP服务器一起提供了[WSGI](http://www.python.org/dev/peps/pep-3333/)的全栈替代方案。虽然可以在WSGI容器（[`WSGIAdapter`](https://www.tornadoweb.org/en/stable/wsgi.html#tornado.wsgi.WSGIAdapter)）中使用Tornado Web框架，或者使用Tornado HTTP服务器作为其他WSGI框架（[`WSGIContainer`](https://www.tornadoweb.org/en/stable/wsgi.html#tornado.wsgi.WSGIContainer)）的容器，但是这些组合中的每一个都有局限性并且要充分利用Tornado，您将需要一起使用Tornado的Web框架和HTTP服务器。*

### 现有模型设计**

```python
from datetime import datetime
from MxForm.settings import database
from peewee import Model, DateTimeField

class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    class Meta:
        database = database
```

```python
class CommunityGroup(BaseModel):
    creator = ForeignKeyField(User, verbose_name="创建者")
    name = CharField(max_length=100, null=True, verbose_name="名称")
    category = CharField(max_length=20, verbose_name="分类", null=True)
    # peewee_async 如果一个model有个外键，需要对改模型增加一个方法。
    @classmethod
    def extend(cls):
        return cls.select(cls, User.id, User.nick_name).join(User)
```

```python
class User(BaseModel):
    mobile = CharField(max_length=11, verbose_name="手机号码", index=True, unique=True)
    password = PasswordField(verbose_name="密码")  # 1. 密文，2.不可反解
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
```

```python
def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} is not serializable".format(type(obj)))
```

### 1.查询操作​    

```python
from playhouse.shortcuts import model_to_dict
async def get(self, *args, **kwargs):
    # 获取小组列表
    re_data = []
    # 先生成sql语句（用peewee生产query对象），这时并没有和数据库打交道，
    community_query = CommunityGroup.extend()

    # 根据类别进行过滤，继承RequestHandler，通过self.get_argument获取前端GET请求参数
    c = self.get_argument("c", None)
    if c:
        community_query = community_query.filter(CommunityGroup.category==c)
    # 然后再利用peewee_async的objects.execute方法执行。
    groups = await self.application.objects.execute(community_query)
    for group in groups:
        # model_to_dict  可以将模型对象转换成字典类型
        group_dict = model_to_dict(group)
        re_data.append(group_dict)
    # 如果字段中有datetime类型，返回时候要用json.dumps转换一下
    self.finish(json.dumps(re_data, default=json_serial))
```

###  2.新增操作

```python
import uuid
import json
import aiofiles

@authenticated_async
async def post(self, *args, **kwargs):
    re_data = {}
	# 继承RequestHandler，通过self.request.body_arguments获取前端POST请求参数
    # 不能使用jsonform，上传文件前端会传过来一个form表单
    group_form = CommunityGroupForm(self.request.body_arguments)
    if group_form.validate():
        # 自己完成图片字段的认证
        files_meta = self.request.files.get("front_image", None)
        if not files_meta:
            self.set_status(400)
            re_data["front_image"] = "请上传图片"
        else:
            # 完成图片保存并将值设置给对应的记录
            # 通过aiofiles写文件
            # 1. 文件名
            meta = files_meta[0]
            filename = meta["filename"]
            # 新的文件名
            new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(),     filename=filename)
            # 新的文件路径
            files_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)
            # 将上传的文件写入到存储文件夹
            async with aiofiles.open(files_path, 'wb') as f:
                await f.write(meta["body"])
			# 写入数据
            group = await self.application.objects.create(CommunityGroup,
                                                          	          creator=self.current_user,name=group_form.name.data,
                                                          category=group_form.category.data, desc=group_form.desc.data,
                                                          notice=group_form.notice.data, front_image=new_filename)
         re_data["id"] = group.id
    else:
        self.set_status(400)
        for field in group_form.errors:
            re_data[field] = group_form.errors[field][0]
    self.finish(re_data)
```



​     

​     

m

